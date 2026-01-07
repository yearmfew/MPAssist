"""
BACKUP - Full app.py with canvas and all features
This file is kept as backup for the right-side config display canvas
"""

import gradio as gr
import os
import json
import tempfile
from dotenv import load_dotenv
from services.chat_service import get_chat_service
from utils.console import Colors

# Load environment variables from .env file
load_dotenv()

# Initialize chat service
chat_service = get_chat_service()

# Global state for current config
current_config = {"json": None, "ready": False}


def chat_config_mode(message: str, history: list) -> str:
    """Handle chat in config generation mode."""
    global current_config

    try:
        assistant_response, config_json = chat_service.chat_config_generation(
            message, history
        )

        if config_json:
            current_config["json"] = config_json
            current_config["ready"] = True

        return assistant_response

    except Exception as e:
        error_msg = (
            f"Error: {str(e)}\n\nPlease check that IONOS_API_TOKEN is set correctly."
        )
        return error_msg


def update_config_display():
    """Update config display and download button based on current state."""
    if current_config["ready"] and current_config["json"]:
        return (
            current_config["json"],
            gr.update(interactive=True, variant="primary"),
        )
    else:
        return (
            "# Config.json will appear here once generated",
            gr.update(interactive=False, variant="secondary"),
        )


def download_config():
    """Create a temporary file with the current config.json for download."""
    if not current_config["ready"] or not current_config["json"]:
        return None

    temp_file = tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, prefix="config_"
    )

    try:
        json_obj = json.loads(current_config["json"])
        json.dump(json_obj, temp_file, indent=2)
    except json.JSONDecodeError:
        temp_file.write(current_config["json"])

    temp_file.close()
    return temp_file.name


# Create the Gradio interface with canvas
demo = gr.Blocks(
    title="MPAssist - Masterportal Configuration Assistant",
    theme=gr.themes.Soft(primary_hue="blue", secondary_hue="cyan"),
)

with demo:
    gr.Markdown("# 🗺️ MPAssist - Masterportal Configuration Assistant")

    with gr.Row():
        # Left: Chat Interface
        with gr.Column(scale=3):
            config_chat = gr.ChatInterface(
                fn=chat_config_mode,
                title="Configuration Assistant",
                description="Describe your requirements",
            )

        # Right: Config Display and Download
        with gr.Column(scale=2):
            gr.Markdown("### 📄 Generated Configuration")
            config_display = gr.Code(
                language="json",
                label="config.json",
                lines=25,
                value="# Config.json will appear here once generated",
                show_label=False,
            )
            download_btn = gr.DownloadButton(
                label="💾 Download config.json",
                variant="secondary",
                interactive=False,
                size="lg",
            )

    download_btn.click(fn=download_config, outputs=download_btn)

if __name__ == "__main__":
    demo.queue()
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_error=True,
        show_api=False,
    )
