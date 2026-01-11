import gradio as gr

from agents.orchestrator import Orchestrator
from utils.settings import IONOS_API_TOKEN


def chat_fn(message: str, history: list):
    orchestrator = Orchestrator()
    try:
        yield from orchestrator.run(message, history)
    except Exception as e:
        print(f"❌ Error in chat_fn: {str(e)}")
        yield "An error occurred."


with gr.Blocks(fill_height=True) as GradioInterface:
    gr.ChatInterface(
        fn=chat_fn,
        fill_height=True,
        title="MPAssist",
        chatbot=gr.Chatbot(height="80vh"),
    )

if __name__ == "__main__":
    if not IONOS_API_TOKEN.get_secret_value():
        print("⚠️  WARNING: IONOS_API_TOKEN not set!")

    print("🚀 Starting MPAssist...")

    GradioInterface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
    )
