import gradio as gr
import json

from agents.orchestrator import Orchestrator
from utils.settings import IONOS_API_TOKEN

orchestrator = Orchestrator()


def chat_fn(message: str, history: list, review_mode: bool):
    """Handle chat messages with streaming responses."""
    if not message.strip():
        return (
            history,
            "",
            gr.update(visible=False),
            gr.update(interactive=False),
            gr.update(interactive=False),
            review_mode,
            gr.update(),
        )

    try:
        history.append({"role": "user", "content": message})

        if review_mode:
            response_text = ""
            for chunk in orchestrator.review_config(message, history):
                response_text = chunk

                yield history + [{"role": "assistant", "content": response_text}], "", gr.update(
                    visible=False
                ), gr.update(interactive=False), gr.update(interactive=False), review_mode, gr.update()

            history.append({"role": "assistant", "content": response_text})

            try:
                config_json_str = (
                    json.dumps(json.loads(orchestrator.latest_config_json), indent=2)
                    if orchestrator.latest_config_json
                    else ""
                )
            except (json.JSONDecodeError, TypeError) as e:
                print(f"Error parsing config JSON in review mode: {str(e)}")
                config_json_str = orchestrator.latest_config_json or ""

            yield history, "", gr.update(visible=False), gr.update(interactive=True), gr.update(
                interactive=True
            ), review_mode, gr.update(value=config_json_str)
        else:
            response_text = ""
            for chunk in orchestrator.run(message, history):
                response_text = chunk
                yield history + [{"role": "assistant", "content": response_text}], "", gr.update(
                    visible=False
                ), gr.update(interactive=False), gr.update(interactive=False), review_mode, gr.update()

            history.append({"role": "assistant", "content": response_text})

            yield history, "", gr.update(visible=True), gr.update(interactive=True), gr.update(
                interactive=True
            ), review_mode, gr.update()

    except Exception as e:
        error_msg = f"An error occurred: {str(e)}"
        print(f"Error in chat_fn: {str(e)}")
        history.append({"role": "assistant", "content": error_msg})

        yield history, "", gr.update(visible=False), gr.update(interactive=True), gr.update(
            interactive=True
        ), review_mode, gr.update()


def generate_config_fn(history: list, review_mode: bool):
    """Generate configuration based on conversation history."""
    try:
        for response in orchestrator.generate_config(history):
            print(f"[DEBUG] Status update: {response}")

            yield response, history, gr.update(interactive=False), gr.update(interactive=False), gr.update(
                interactive=False
            ), gr.update(visible=False), review_mode, gr.update()

        print(f"[DEBUG] Checking latest_config_json...")

        if not orchestrator.latest_config_json:
            raise Exception("Config generation completed but latest_config_json is None")

        print(f"[DEBUG] latest_config_json type: {type(orchestrator.latest_config_json)}")
        print(f"[DEBUG] latest_config_json first 200 chars: {str(orchestrator.latest_config_json)[:200]}")

        try:
            config_json_obj = json.loads(orchestrator.latest_config_json) if orchestrator.latest_config_json else None
        except json.JSONDecodeError as e:
            print(f"[ERROR] JSON Parse Error in app.py: {str(e)}")
            print(f"[ERROR] Problematic JSON (first 500 chars): {orchestrator.latest_config_json[:500]}")
            raise Exception(
                f"Failed to parse generated config: {str(e)}\n\nJSON preview: {orchestrator.latest_config_json[:200]}"
            )
        except Exception as e:
            print(f"[ERROR] Unexpected error parsing config JSON: {str(e)}")
            raise

        review_mode = True
        orchestrator.review_mode = True

        review_msg = "\n\nKonfiguration wurde generiert! Sie können jetzt Änderungen vorschlagen."
        history.append({"role": "assistant", "content": review_msg})

        try:
            config_json_str = json.dumps(config_json_obj, indent=2) if config_json_obj else ""
        except Exception as e:
            print(f"Error formatting JSON: {str(e)}")
            config_json_str = orchestrator.latest_config_json or ""

        yield "Fertig! ✓", history, gr.update(visible=False), gr.update(interactive=True), gr.update(
            interactive=True
        ), gr.update(value=config_json_str, visible=True), review_mode, gr.update(
            placeholder="Änderungen vorschlagen...", value=""
        )

    except Exception as e:
        error_msg = f"❌ Configuration generation failed: {str(e)}"

        print(error_msg)

        history.append({"role": "assistant", "content": error_msg})

        yield f"Fehler: {str(e)}", history, gr.update(visible=False), gr.update(interactive=True), gr.update(
            interactive=True
        ), gr.update(visible=False), review_mode, gr.update()


def reset_conversation():
    """Reset the conversation to initial state."""
    initial_msg = [{"role": "assistant", "content": "Nachricht eingeben..."}]
    orchestrator.latest_config_json = None
    orchestrator.review_mode = False
    orchestrator.conversation_for_requirements = ""
    review_mode = False
    return (
        "Bereit",
        initial_msg,
        gr.update(visible=False, interactive=True),
        gr.update(interactive=True),
        gr.update(interactive=True),
        gr.update(value=None, visible=False),
        review_mode,
        gr.update(placeholder="Nachricht eingeben...", value=""),
    )


with gr.Blocks(
    title="MPAssist",
    css="""
    .main-row {
        height: 90vh !important;
    }
    .main-row .column {
        height: 90vh !important;
    }
    footer {
        display: none !important;
    }
    """,
) as GradioInterface:
    gr.Markdown("# MPAssist")

    review_mode_state = gr.State(value=False)

    with gr.Row(elem_classes="main-row"):
        with gr.Column(scale=1):
            gr.Markdown(
                """
                ## Was ist MPAssist? 
                **MPAssist** ist ein KI-Assistent, der eine `config.json`-Datei für Masterportal erstellt.
                ## Wie funktioniert es?
                
                ### Starten Sie ein Gespräch
                Erklären Sie, was Sie für Ihre Masterportal-Instanz benötigen. Zum Beispiel:
                - "Ich möchte ein Portal für eine Stadt mit mehreren Layern, die öffentliche Verkehrsmittel, Fahrradwege und Grünflächen zeigen."
                - "Ich brauche ein einfaches Portal für eine Wanderwegkarte mit einem benutzerdefinierten Menü und bestimmten Kartensteuerungen."
                
                ### Anforderungserfassung
                MPAssist ermittelt Ihre Anforderungen durch ein Gespräch. Sie können während des Chats weitere Details, Beispiele oder spezifische Anforderungen angeben.
                
                ### Konfiguration generieren
                Wenn das Gespräch abgeschlossen ist, klicken Sie auf die Schaltfläche "Konfiguration generieren".
                
                ### Laden Sie Ihre config.json herunter
                Ihre `config.json`-Datei ist zum Download bereit.

                ---
                Wenn Sie information über Masterportal brauchen, können Sie dieses [Masterportal Dokumentation](https://www.masterportal.org/dokumentation/dokumentation) sehen.
                """
            )

        with gr.Column(scale=4):
            status_box = gr.Textbox(
                label="Status",
                value="Bereit",
                interactive=False,
                max_lines=3,
            )
            chatbot = gr.Chatbot(
                label="Conversation",
                scale=1,
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
                msg = gr.Textbox(
                    placeholder="Nachricht eingeben...",
                    show_label=False,
                    scale=9,
                    container=False,
                )
                submit_button = gr.Button("Senden", variant="primary", scale=1)

            with gr.Row():
                generate_button = gr.Button(
                    "Generate Configuration",
                    visible=False,
                    variant="primary",
                )
                reset_button = gr.Button(
                    "Zurücksetzen",
                    variant="secondary",
                )

        with gr.Column(scale=2):
            config_json_display = gr.Code(
                label="Generierte Konfiguration",
                language="json",
                visible=False,
                lines=100,
            )

    msg.submit(
        chat_fn,
        inputs=[msg, chatbot, review_mode_state],
        outputs=[chatbot, msg, generate_button, submit_button, reset_button, review_mode_state, config_json_display],
    )

    submit_button.click(
        chat_fn,
        inputs=[msg, chatbot, review_mode_state],
        outputs=[chatbot, msg, generate_button, submit_button, reset_button, review_mode_state, config_json_display],
    )

    generate_button.click(
        generate_config_fn,
        inputs=[chatbot, review_mode_state],
        outputs=[
            status_box,
            chatbot,
            generate_button,
            submit_button,
            reset_button,
            config_json_display,
            review_mode_state,
            msg,
        ],
    )

    reset_button.click(
        reset_conversation,
        outputs=[
            status_box,
            chatbot,
            generate_button,
            submit_button,
            reset_button,
            config_json_display,
            review_mode_state,
            msg,
        ],
    )


if __name__ == "__main__":
    if not IONOS_API_TOKEN.get_secret_value():
        print(" WARNING: IONOS_API_TOKEN not set!")

    print("Starting MPAssist...")

    GradioInterface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
    )
