from abc import ABC, abstractmethod
from langchain_ollama import ChatOllama
from utils.db_manager import LLM_MODEL


class BaseAgent(ABC):
    """
    Base class for all agents.
    Provides common LLM invocation functionality.
    Subclasses can override invoke_llm for custom behavior.
    """

    def __init__(self, model: str = LLM_MODEL):
        self.model = model

    def invoke_llm(self, prompt: str, **kwargs) -> str:
        """
        Common LLM invocation method.
        Subclasses can override this for custom parameters (temperature, streaming, etc.).

        Args:
            prompt: The prompt to send to the LLM
            **kwargs: Additional parameters to pass to ChatOllama (temperature, top_p, etc.)

        Returns:
            The LLM response as a string
        """
        # Initialize the LLM
        llm = ChatOllama(model=self.model, **kwargs)

        # Use invoke() method like the working chain does
        # invoke() returns an AIMessage object, we need to extract the content
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
