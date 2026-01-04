from __future__ import annotations

from langchain_core.prompts import PromptTemplate

from agents.prompt_generator import PromptGenerator
from agents.tool_finder import ToolFinder
from agents.config_file_creator import ConfigFileCreator

from utils.console import *
from utils.spinner import SpinnerContext
from utils import db_manager

from template import TEMPLATE_SIMPLE


class Orchestrator:
    """
    Orchestrator Agent

    Responsibility: Coordinates the entire workflow between agents.
    - Core Logic: Manages multi-agent workflow (requirement gathering → tool finding → config generation)
    - Terminal UI: Provides CLI interaction (can be replaced with API in the future)

    Architecture:
    - find_requirements(): Conversational requirement gathering with user
    - process_query(): Process requirements through PromptGenerator → ToolFinder pipeline
    - run_terminal_interface(): Terminal-specific UI layer (future: replace with API)
    """

    def __init__(self):
        """Initialize the orchestrator with all agents."""
        self.prompt_generator = PromptGenerator()
        self.tool_finder = ToolFinder()
        self.config_creator = ConfigFileCreator()

    def find_requirements(self, initial_user_input: str) -> list[str]:
        """
        CORE ORCHESTRATION: Conversational requirement gathering with user.

        Uses the PromptGenerator in 'requirement gathering' mode to have a conversation
        with the user and collect requirements through multi-turn interaction.

        Workflow:
        1. User provides initial requirements via normal Python input
        2. LLM asks clarifying questions using TEMPLATE_REQUIREMENT_GATHERER
        3. User responds with information
        4. Conversation continues until LLM has enough information
        5. LLM outputs final requirements list

        Args:
            initial_user_input: Initial requirements from user (optional)

        Returns:
            List of gathered requirements (strings)
        """
        print_step("Starting requirement gathering conversation")
        print_info("The system will ask you questions to understand your needs.")

        # Multi-turn conversation history
        conversation_history = []

        # Add initial user input to conversation history if provided
        if initial_user_input:
            conversation_history.append({"role": "user", "content": initial_user_input})

        max_turns = 10  # Prevent infinite loops

        for turn in range(max_turns):
            # Use PromptGenerator in requirement gathering mode
            with SpinnerContext("Thinking"):
                llm_message = self.prompt_generator.gather_requirements(
                    conversation_history
                )

            print_assistant(llm_message)

            # Check if LLM has finished gathering (indicates ready with special marker)
            if "[REQUIREMENTS_READY]" in llm_message:
                # Extract the requirements from the message
                requirements = self._extract_requirements_from_message(llm_message)
                print_success("Requirements gathered successfully!")
                return requirements

            # Get user response
            try:
                user_response = print_user_prompt("You: ").strip()
                if not user_response:
                    print_error("Please provide a response.")
                    continue

                # Add to conversation history
                conversation_history.append(
                    {"role": "assistant", "content": llm_message}
                )
                conversation_history.append({"role": "user", "content": user_response})

            except (EOFError, KeyboardInterrupt):
                print_error("Conversation interrupted. Using partial requirements.")
                return self._extract_requirements_from_history(conversation_history)

        # Max turns reached
        print_warning("Maximum conversation turns reached. Finalizing requirements.")
        return self._extract_requirements_from_history(conversation_history)

    def _extract_requirements_from_message(self, message: str) -> list[str]:
        """
        Extract requirements list from LLM message containing [REQUIREMENTS_READY] marker.

        Args:
            message: LLM message with requirements

        Returns:
            List of requirement strings
        """
        import re

        requirements = []
        lines = message.split("\n")

        # Find "Final Requirements Summary:" section
        in_summary_section = False
        for line in lines:
            line_stripped = line.strip()

            # Detect start of summary section
            if "final requirements summary" in line_stripped.lower():
                in_summary_section = True
                continue

            # Stop at [REQUIREMENTS_READY] marker
            if "[REQUIREMENTS_READY]" in line_stripped:
                break

            # Extract numbered requirements (e.g., "1. Requirement text")
            if in_summary_section:
                match = re.match(r"^(\d+)\.\s+(.+?)$", line_stripped)
                if match:
                    requirement_text = match.group(2).strip()
                    # Skip meta-text like "These requirements are now complete"
                    if requirement_text and not requirement_text.lower().startswith(
                        ("these requirements", "ready to")
                    ):
                        requirements.append(requirement_text)

        return (
            requirements if requirements else ["User request captured in conversation"]
        )

    def _extract_requirements_from_history(self, history: list[dict]) -> list[str]:
        """
        Extract requirements from incomplete conversation history.

        Args:
            history: Conversation history

        Returns:
            List of requirement strings extracted from user messages
        """
        requirements = []
        for msg in history:
            if msg["role"] == "user":
                requirements.append(msg["content"])
        return requirements if requirements else ["No specific requirements captured"]

    def process_query(self, requirements: list[str]) -> str:
        """
        CORE ORCHESTRATION: Process requirements through the multi-agent pipeline.

        Workflow:
        1. ToolFinder analyzes requirements and finds suitable tools/layers
        2. ConfigFileCreator generates config.json using tools/layers

        Args:
            requirements: List of gathered requirements

        Returns:
            The final generated config.json from ConfigFileCreator
        """
        # Combine requirements into a structured text
        requirements_text = "\n".join(f"- {req}" for req in requirements)
        # =============================== #
        # Step 1: Find tools and layers
        # =============================== #

        print_step("Step 1: Finding suitable tools and layers")
        with SpinnerContext("Analyzing requirements and finding tools"):
            tools_and_layers = self.tool_finder.execute(requirements_text)
        print_box("Tools & Layers (from ToolFinder)", "BLUE", 60)
        # Optionally print the tools (commented out to reduce noise)
        print(tools_and_layers)
        print_box_end(60, "BLUE")

        # =============================== #
        # Step 2: Generate config.json
        # =============================== #

        print_step("Step 2: Generating config.json")
        with SpinnerContext("Generating configuration file"):
            config_json = self.config_creator.execute(tools_and_layers)

        return config_json

    def simple_chat(self):
        """
        CORE ORCHESTRATION: Simple Q&A chat about Masterportal using RAG.

        Uses TEMPLATE_SIMPLE for basic question-answering with vector DB retrieval.
        Allows users to ask questions about Masterportal documentation.
        """
        print_header("What do you want to know about Masterportal?", "💬")
        print_info("Type 'back' to return to main menu, 'exit' to quit")

        # Ensure vector store is initialized
        if db_manager._retriever is None:
            db_manager._init_vector_store()

        while True:
            # Get user question
            question = print_question_prompt("Your question: ")

            if question is None:
                break

            if question.lower() == "back":
                print_info("Returning to main menu...")
                break

            # Retrieve relevant context with metadata labels
            with SpinnerContext("Searching documentation"):
                docs = db_manager._retriever.invoke(question)

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
                    full_prompt = prompt_template.format(
                        context=context_text, question=question
                    )
                except Exception:
                    full_prompt = TEMPLATE_SIMPLE.replace(
                        "{context}", context_text
                    ).replace("{question}", question)

                # Get answer from LLM
                answer = self.prompt_generator.invoke_llm(full_prompt)

            # Display answer
            print_assistant(answer)

    # ============================================================================
    # TERMINAL UI LAYER (Future: Replace with API)
    # ============================================================================
    # This section contains terminal/CLI-specific code that handles user interaction
    # through the command line. In the future, this layer will be replaced with
    # an API endpoint that accepts requests and returns responses.
    #
    # Core orchestration logic (find_requirements, process_query) is separate
    # and can be called from API handlers without modification.
    # ============================================================================

    def run_terminal_interface(self):
        """
        TERMINAL UI: Main interactive command-line interface.

        This method provides terminal-based user interaction. It will be replaced
        with API endpoints in future versions.

        Future replacement: FastAPI/Flask endpoints that call find_requirements()
        and process_query() directly.
        """
        self._display_terminal_welcome()

        print_separator("=", 60, "BLUE")
        print_info("  Interactive Mode - Type 'exit' to quit")
        print_separator("=", 60, "BLUE")

        while True:
            # Ask if user wants to start
            start_input = self._get_terminal_input(
                "\nStart new configuration? (yes/no or 'exit' to quit): "
            )

            if start_input is None:
                break

            # If user says no, go directly to chat mode
            if start_input.lower() in ("no", "n"):
                self.simple_chat()
                continue

            if start_input.lower() not in ("yes", "y"):
                print_warning("Please answer 'yes' or 'no'")
                continue

            print_separator("─", 60, "YELLOW")
            print_header("Starting new configuration request", "📝")
            print_separator("─", 60, "YELLOW")

            # Invoke the multi-step flow: find_requirements → process_query
            try:
                # First, get initial requirements with normal Python input
                print_info(
                    "Please specify your requirements for the Masterportal configuration."
                )
                initial_requirements = print_user_prompt("Your requirements: ").strip()

                if not initial_requirements:
                    print_error("No requirements provided. Please try again.")
                    continue

                # Step 1: Gather requirements through conversation (starting with initial input)
                requirements = self.find_requirements(
                    initial_user_input=initial_requirements
                )

                # Display gathered requirements
                print_header("Gathered Requirements", "📋")
                for i, req in enumerate(requirements, 1):
                    print(f"  {i}. {req}")

                # Step 2: Process requirements to generate configuration
                answer = self.process_query(requirements)

                # Print the answer
                print_box("Generated Configuration", "GREEN", 60)
                print(answer)
                print_box_end(60, "GREEN")

            except Exception as e:
                print_error(f"Error in workflow: {e}")
                import traceback

                traceback.print_exc()

            print_success("Configuration complete. You can start another request.")

        print_header("Exiting interactive mode. Goodbye!", "👋")

    def _display_terminal_welcome(self):
        """TERMINAL UI: Display welcome message."""
        print_separator("=", 60, "HEADER")
        print_header("MPAssist - Masterportal Configuration Assistant")
        print_separator("=", 60, "HEADER")

        print_info("Loading chat model...")
        print_success("Setting up RAG components...")

    def _get_terminal_input(self, prompt_text: str) -> str | None:
        """
        TERMINAL UI: Get user input from terminal.

        Args:
            prompt_text: The prompt to display to user

        Returns:
            User input string, or None if interrupted/exit requested
        """
        try:
            user_input = input(prompt_text).strip()
        except (EOFError, KeyboardInterrupt):
            return None

        if not user_input or user_input.lower() in ("exit", "quit"):
            return None

        return user_input

    # Legacy method for backwards compatibility
    def run(self):
        """
        Main entry point. Delegates to terminal interface.

        In future versions, this would route to appropriate interface (terminal/API).
        """
        self.run_terminal_interface()
