"""
Chat Service Layer for MPAssist Gradio Integration.

This service layer provides stateless functions that decouple the core
orchestration logic from the UI layer (Gradio). It converts between
Gradio's OpenAI-style message format and the internal agent workflow.

Responsibilities:
- Convert Gradio history format to internal format
- Handle conversational requirement gathering
- Process config generation pipeline
- Provide simple Q&A functionality
"""

from typing import List, Dict, Tuple, Optional, Generator
from agents.orchestrator import Orchestrator
from utils import db_manager
from langchain_core.prompts import PromptTemplate
from template import TEMPLATE_SIMPLE


class ChatService:
    """
    Service layer for chat functionality.
    Provides stateless methods for Gradio integration.
    """

    def __init__(self):
        """Initialize the chat service with orchestrator."""
        self.orchestrator = Orchestrator()
        # Ensure vector store is initialized for Q&A
        if db_manager._retriever is None:
            db_manager._init_vector_store()

    def chat_config_generation(
        self, message: str, history: List[Dict]
    ) -> Tuple[str, Optional[str]]:
        """
        Handle chat for configuration generation mode.

        This function manages the multi-turn conversation for requirement gathering
        and triggers config generation when requirements are ready.

        Args:
            message: User's current message
            history: Gradio conversation history in OpenAI format:
                     [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}, ...]

        Returns:
            Tuple of (assistant_response, config_json)
            - assistant_response: The LLM's response to show in chat
            - config_json: The generated config.json if ready, otherwise None
        """
        # Convert Gradio history to internal format and add current message
        conversation_history = self._convert_gradio_history(history)
        conversation_history.append({"role": "user", "content": message})

        # Use PromptGenerator to gather requirements
        llm_message = self.orchestrator.prompt_generator.gather_requirements(
            conversation_history
        )

        # Check if requirements are ready
        if "[REQUIREMENTS_READY]" in llm_message:
            # Extract requirements
            requirements = self.orchestrator._extract_requirements_from_message(
                llm_message
            )

            # Generate config.json
            config_json = self._generate_config_from_requirements(requirements)

            # Return both the message and the config
            return llm_message, config_json
        else:
            # Continue gathering requirements
            return llm_message, None

    def chat_simple_qa(self, message: str, history: List[Dict]) -> str:
        """
        Handle simple Q&A chat about Masterportal documentation.

        Uses RAG to retrieve relevant documentation and answer questions.

        Args:
            message: User's question
            history: Gradio conversation history (not used for Q&A, each question is independent)

        Returns:
            The assistant's answer
        """
        # Retrieve relevant context
        docs = db_manager._retriever.invoke(message)

        # Add metadata labels to context
        context_parts = []
        for d in docs:
            category = d.metadata.get("category", "unknown").upper()
            source = d.metadata.get("source", "unknown")
            labeled_chunk = (
                f"[CATEGORY: {category}] [SOURCE: {source}]\n{d.page_content}"
            )
            context_parts.append(labeled_chunk)

        context_text = "\n\n---\n\n".join(context_parts)

        # Format prompt with TEMPLATE_SIMPLE
        prompt_template = PromptTemplate.from_template(TEMPLATE_SIMPLE)
        try:
            full_prompt = prompt_template.format(context=context_text, question=message)
        except Exception:
            full_prompt = TEMPLATE_SIMPLE.replace("{context}", context_text).replace(
                "{question}", message
            )

        # Get answer from LLM
        answer = self.orchestrator.prompt_generator.invoke_llm(full_prompt)

        return answer

    def generate_config_from_requirements(self, requirements_text: str) -> str:
        """
        Generate config.json from requirements text.

        This is a direct wrapper around the orchestrator's process_query method.

        Args:
            requirements_text: User requirements as text

        Returns:
            Generated config.json as string
        """
        requirements = [
            req.strip() for req in requirements_text.split("\n") if req.strip()
        ]
        return self._generate_config_from_requirements(requirements)

    def _generate_config_from_requirements(self, requirements: List[str]) -> str:
        """
        Internal method to generate config from requirements list.

        Args:
            requirements: List of requirement strings

        Returns:
            Generated config.json as string
        """
        # Use orchestrator's process_query which handles the full pipeline
        config_json = self.orchestrator.process_query(requirements)
        return config_json

    def _convert_gradio_history(self, gradio_history: List[Dict]) -> List[Dict]:
        """
        Convert Gradio's OpenAI-style history to internal format.

        Gradio history format:
        [
            {"role": "user", "content": [{"type": "text", "text": "..."}]},
            {"role": "assistant", "content": [{"type": "text", "text": "..."}]}
        ]

        Internal format:
        [
            {"role": "user", "content": "..."},
            {"role": "assistant", "content": "..."}
        ]

        Args:
            gradio_history: History in Gradio's format

        Returns:
            History in internal format
        """
        internal_history = []
        for msg in gradio_history:
            role = msg.get("role")
            content = msg.get("content")

            # Handle different content formats
            if isinstance(content, list):
                # Extract text from content list
                text_parts = []
                for item in content:
                    if isinstance(item, dict) and item.get("type") == "text":
                        text_parts.append(item.get("text", ""))
                content_str = " ".join(text_parts)
            elif isinstance(content, str):
                content_str = content
            else:
                content_str = str(content)

            internal_history.append({"role": role, "content": content_str})

        return internal_history


# Singleton instance for use in Gradio app
_chat_service = None


def get_chat_service() -> ChatService:
    """
    Get or create the singleton ChatService instance.

    Returns:
        ChatService instance
    """
    global _chat_service
    if _chat_service is None:
        _chat_service = ChatService()
    return _chat_service
