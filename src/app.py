"""
MPAssist - Minimal Gradio Web Application
Simple chatbot interface for testing API connection
"""

# from typing import IO
import gradio as gr
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from settings import IONOS_API_BASE_URL, LLM_MODEL, IONOS_API_TOKEN


def chat_fn(message: str, history: list) -> str:
    """
    Simple chat function that calls IONOS API.

    Args:
        message: User's message
        history: Chat history (not used yet)

    Returns:
        AI response
    """
    try:
        # Initialize IONOS LLM
        llm = ChatOpenAI(
            model=LLM_MODEL,
            api_key=IONOS_API_TOKEN,
            base_url=IONOS_API_BASE_URL,
            temperature=0.7,
        )
        chain = llm | StrOutputParser()

        # Simple prompt
        # response = llm.invoke(message)
        return chain.invoke(message)

    except Exception as e:
        return f"Error: {str(e)}"


# Create simple Gradio interface
demo = gr.ChatInterface(
    fn=chat_fn,
    title="MPAssist",
)

if __name__ == "__main__":
    if not os.environ.get("IONOS_API_TOKEN"):
        print("⚠️  WARNING: IONOS_API_TOKEN not set!")

    print("🚀 Starting MPAssist...")
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
        show_api=False,
    )
