from abc import ABC, abstractmethod
from langchain_openai import ChatOpenAI
from settings import LLM_MODEL, IONOS_API_BASE_URL, IONOS_API_TOKEN


class BaseAgent(ABC):
    """
    Base class for all agents.
    Provides common LLM invocation functionality.
    Subclasses can override invoke_llm for custom behavior.
    """

    def __init__(self, model: str = LLM_MODEL):
        self.model = model
        # Get API token from environment variable
        self.api_token = IONOS_API_TOKEN
        self.base_url = IONOS_API_BASE_URL
        if not self.api_token:
            raise ValueError(
                "IONOS_API_TOKEN environment variable not set. "
                "Please set it to your IONOS AI Model Hub API token."
            )

    def invoke_llm(self, prompt: str, stream: bool = False, **kwargs) -> str:
        """
        Common LLM invocation method using IONOS AI Model Hub.
        Subclasses can override this for custom parameters (temperature, top_p, etc.).

        Args:
            prompt: The prompt to send to the LLM
            stream: Whether to stream the response (default: False)
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

        if stream:
            # Return a generator for streaming
            return llm.stream(prompt)
        else:
            # Use invoke() method - returns an AIMessage object
            response = llm.invoke(prompt)

            # Extract text from the response
            if hasattr(response, "content"):
                return response.content
            else:
                return str(response)

    @abstractmethod
    def execute(self, *args, **kwargs):
        """
        Each agent must implement this method.
        This is the main entry point for the agent's functionality.
        """
        pass
