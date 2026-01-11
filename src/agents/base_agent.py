from abc import ABC
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from utils.settings import LLM_MODEL, IONOS_API_BASE_URL, IONOS_API_TOKEN
from utils import db_manager


class BaseAgent(ABC):
    """
    Base class for all agents.
    Provides common functions.
    """

    def __init__(self):
        self.model = LLM_MODEL
        # Get API token from environment variable
        self.api_token = IONOS_API_TOKEN
        self.base_url = IONOS_API_BASE_URL
        if not self.api_token:
            raise ValueError(
                "IONOS_API_TOKEN environment variable not set. "
                "Please set it to your IONOS AI Model Hub API token."
            )

    def invoke_llm(self, prompt: str, **kwargs) -> str:
        """
        Common LLM invocation method using IONOS AI Model Hub.
        Subclasses can override this for custom parameters (temperature, top_p, etc.).

        Args:
            prompt: The prompt to send to the LLM
            **kwargs: Additional parameters to pass to ChatOpenAI (temperature, top_p, etc.)

        Returns:
            The LLM response as a string (or generator if stream=True)
        """
        # Initialize the LLM with IONOS endpoint
        llm = ChatOpenAI(
            model=self.model,
            base_url=self.base_url,
            api_key=self.api_token,
            **kwargs,
        )

        response = llm.invoke(prompt)

        return str(response.content)

    def get_chunks(self, query: str, k: int = 3, filter: dict = {}, **kwargs) -> list:
        try:
            chunks = db_manager._vector_store.similarity_search(
                query,
                k,
                filter,
                **kwargs,
            )
        except Exception:
            chunks = []

        return chunks

    def create_prompt_template(self, template: str, context: str, **kwargs) -> str:
        prompt_template = PromptTemplate.from_template(template)
        variables = {"context": context, **kwargs}

        try:
            full_prompt = prompt_template.format(**variables)
        except Exception:
            full_prompt = template
            for key, value in variables.items():
                full_prompt = full_prompt.replace(f"{{{key}}}", str(value))

        return full_prompt

    def print_nice(self, message: str, title: str = "INFO"):
        print(f"\033[94m┌─ {title} {'─' * (100 - len(title) - 4)}┐\033[91m")
        print(message)
        print(f"\033[94m└{'─' * 100}┘\033[0m")
