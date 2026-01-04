from agents.base_agent import BaseAgent
import utils.db_manager as db_manager
from template import TEMPLATE_REQUIREMENT_GATHERER, TEMPLATE_CONFIG_GENERATOR
from langchain_core.prompts import PromptTemplate


class PromptGenerator(BaseAgent):
    """
    PromptGenerator Agent

    Responsibility: Two operational modes for different workflow stages:

    1. REQUIREMENT GATHERING MODE:
       - Conducts conversational requirement elicitation with user
       - Uses TEMPLATE_REQUIREMENT_GATHERER
       - Returns LLM responses for multi-turn conversation
       - Calls invoke_llm() to interact with user

    2. CONFIG GENERATION MODE:
       - Creates enriched prompts using RAG for config.json generation
       - Retrieves relevant context from vector database
       - Uses TEMPLATE_CONFIG_GENERATOR
       - Returns the final prompt string (deliverable)
       - Does NOT call LLM (only prepares prompt)
    """

    def __init__(self):
        # PromptGenerator uses LLM for requirement gathering mode
        super().__init__()
        # Initialize vector store and retriever for config generation mode
        db_manager._init_vector_store()

    def gather_requirements(self, conversation_history: list[dict]) -> str:
        """
        MODE 1: REQUIREMENT GATHERING

        Conducts conversational requirement elicitation using LLM.
        This method enables multi-turn conversation with the user to gather
        detailed requirements before generating configuration.

        Args:
            conversation_history: List of previous conversation turns
                                 Each turn: {"role": "user"|"assistant", "content": str}

        Returns:
            LLM's next message in the conversation (question or confirmation)
            When ready to finish, includes [REQUIREMENTS_READY] marker
        """
        # Build conversation context from history
        conversation_text = self._format_conversation_history(conversation_history)

        # Create prompt using requirement gatherer template
        prompt_template = PromptTemplate.from_template(TEMPLATE_REQUIREMENT_GATHERER)

        try:
            full_prompt = prompt_template.format(conversation_history=conversation_text)
        except Exception:
            # Fallback formatting
            full_prompt = TEMPLATE_REQUIREMENT_GATHERER.replace(
                "{conversation_history}", conversation_text
            )

        # Call LLM to generate next conversation turn
        llm_response = self.invoke_llm(full_prompt)

        return llm_response

    def _format_conversation_history(self, history: list[dict]) -> str:
        """
        Format conversation history into readable text for LLM.

        Args:
            history: List of conversation turns

        Returns:
            Formatted conversation string
        """
        if not history:
            return "This is the start of the conversation. Begin by greeting the user and asking about their needs."

        formatted_lines = []
        for turn in history:
            role = "User" if turn["role"] == "user" else "Assistant"
            formatted_lines.append(f"{role}: {turn['content']}")

        return "\n".join(formatted_lines)

    def generate_config_prompt(self, requirements: str) -> str:
        """
        MODE 2: CONFIG GENERATION

        Creates an enriched prompt using RAG for config.json generation.
        This is the original execute() functionality - retrieves relevant docs
        and formats them with requirements into a prompt.

        Args:
            requirements: User requirements (gathered from conversation)

        Returns:
            The enriched prompt ready for LLM (config generation)
        """
        # ensure retriever is initialized
        if db_manager._retriever is None:
            raise RuntimeError(
                "Retriever is not initialized. Ensure the vector DB exists and _init_vector_store() succeeded."
            )

        # retrieve documents relevant to the requirements
        docs = db_manager._retriever.invoke(requirements)

        # join retrieved chunks into a single context block
        context_text = "\n\n".join(d.page_content for d in docs)

        # create and format the prompt using CONFIG_GENERATOR template
        prompt_template = PromptTemplate.from_template(TEMPLATE_CONFIG_GENERATOR)

        try:
            full_prompt = prompt_template.format(
                context=context_text, question=requirements
            )
        except Exception:
            full_prompt = TEMPLATE_CONFIG_GENERATOR.replace(
                "{context}", context_text
            ).replace("{question}", requirements)

        return full_prompt

    # Legacy method for backwards compatibility
    def execute(self, user_query: str) -> str:
        """
        LEGACY: Wrapper for generate_config_prompt() for backwards compatibility.

        This method corresponds to the 'prompt creation' portion of the old RAG chain.
        It:
            a) Uses the retriever to fetch top-k relevant document chunks for the question,
            b) Joins them into a context block,
            c) Formats the full prompt template with context + question,
            d) Returns the final prompt string (the 'deliverable' query).
        This separates prompt construction from LLM invocation so other systems can consume the prompt.

        Args:
            user_query: The user's natural language question

        Returns:
            The enriched prompt ready for LLM
        """
        return self.generate_config_prompt(user_query)
