import gradio as gr

from agents.orchestrator import Orchestrator
from utils.settings import IONOS_API_TOKEN

orchestrator = Orchestrator()


def chat_fn(message: str, history: list):
    """Handle chat messages with streaming responses."""
    if not message.strip():
        # yield is a copilot suggestion. Check it later.
        # yield history, "", gr.update(visible=False), gr.update(interactive=False), gr.update(interactive=False)
        return history, "", gr.update(visible=False), gr.update(interactive=False), gr.update(interactive=False)

    try:
        history.append({"role": "user", "content": message})

        response_text = ""
        for chunk in orchestrator.run(message, history):
            response_text = chunk
            yield history + [{"role": "assistant", "content": response_text}], "", gr.update(visible=False), gr.update(
                interactive=False
            ), gr.update(interactive=False)

        history.append({"role": "assistant", "content": response_text})
        yield history, "", gr.update(visible=True), gr.update(interactive=True), gr.update(interactive=True)

    except Exception as e:
        error_msg = f"An error occurred: {str(e)}"
        print(f"Error in chat_fn: {str(e)}")
        history.append({"role": "assistant", "content": error_msg})
        yield history, "", gr.update(visible=False), gr.update(interactive=True), gr.update(interactive=True)


def generate_config_fn(history: list, progress=gr.Progress()):
    """Generate configuration based on conversation history."""
    try:
        progress(0, desc="Config Datei wurde erstellt....")

        for response in orchestrator.generate_config(history):
            progress(0.5, desc="Config Datei wurde erstellt...")
            yield history + [{"role": "assistant", "content": response}], gr.update(interactive=False), gr.update(
                interactive=False
            ), gr.update(interactive=False), gr.update(interactive=False)

        history.append({"role": "assistant", "content": response})

        progress(1.0, desc="Fertig!")
        yield history, gr.update(visible=False), gr.update(interactive=True), gr.update(interactive=True), gr.update(
            interactive=True
        )

    except Exception as e:
        error_msg = f"❌ Configuration generation failed: {str(e)}"

        print(error_msg)

        history.append({"role": "assistant", "content": error_msg})

        yield history, gr.update(visible=False), gr.update(interactive=True), gr.update(interactive=True), gr.update(
            interactive=True
        )


def reset_conversation():
    """Reset the conversation to initial state."""
    initial_msg = [{"role": "assistant", "content": "Frag MPAssist"}]
    return (
        initial_msg,
        gr.update(visible=False, interactive=True),
        gr.update(interactive=True),
        gr.update(interactive=True),
    )


with gr.Blocks(title="MPAssist") as GradioInterface:
    gr.Markdown("# MPAssist")

    chatbot = gr.Chatbot(
        label="Conversation",
        height=600,
        value=[
            {
                "role": "assistant",
                "content": "Hallo! Ich bin MPAssist, Ihr Assistent für die Erstellung von Masterportal-Konfigurationsdateien. "
                "Ich helfe Ihnen dabei, eine angepasste `config.json` Datei basierend auf Ihren Anforderungen zu erstellen. "
                "Bitte beschreiben Sie die Art des Portals, das Sie erstellen möchten, und seine Funktionen.",
            },
        ],  # type: ignore
    )

    with gr.Row():
        generate_button = gr.Button(
            "Generate Configuration",
            visible=False,
            variant="primary",
        )
        reset_button = gr.Button(
            "Reset",
            variant="secondary",
        )

    with gr.Row():
        msg = gr.Textbox(
            placeholder="Frag MPAssist?",
            show_label=False,
            scale=9,
            container=False,
        )
        submit_button = gr.Button("Senden", variant="primary", scale=1)

    msg.submit(
        chat_fn,
        inputs=[msg, chatbot],
        outputs=[chatbot, msg, generate_button, submit_button, reset_button],
    )

    submit_button.click(
        chat_fn,
        inputs=[msg, chatbot],
        outputs=[chatbot, msg, generate_button, submit_button, reset_button],
    )

    generate_button.click(
        generate_config_fn,
        inputs=[chatbot],
        outputs=[chatbot, generate_button, submit_button, reset_button, msg],
    )

    reset_button.click(
        reset_conversation,
        outputs=[chatbot, generate_button, submit_button, reset_button],
    )


if __name__ == "__main__":
    if not IONOS_API_TOKEN.get_secret_value():
        print("⚠️  WARNING: IONOS_API_TOKEN not set!")

    print("🚀 Starting MPAssist...")

    GradioInterface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
    )
