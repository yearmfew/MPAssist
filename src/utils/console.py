# utils/console.py
"""
Terminal output utilities with colored printing and icons.
Provides helper functions for consistent, readable console output.
"""

import sys
import os


def _supports_color():
    """
    Check if the terminal supports ANSI color codes.

    Returns:
        bool: True if colors are supported, False otherwise
    """
    # Force disable if NO_COLOR environment variable is set
    if os.environ.get("NO_COLOR"):
        return False

    # Force enable if FORCE_COLOR environment variable is set
    if os.environ.get("FORCE_COLOR"):
        return True

    # Windows check
    if sys.platform == "win32":
        # Windows 10+ modern terminal check
        # WT_SESSION = Windows Terminal
        # TERM_PROGRAM = VS Code, other modern terminals
        return bool(os.environ.get("WT_SESSION") or os.environ.get("TERM_PROGRAM"))

    # Unix/Linux/Mac check
    # Check if stdout is a TTY (interactive terminal)
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


# --- ANSI Color Codes for Terminal Output ---
class Colors:
    """
    ANSI color codes for terminal output.
    Automatically disables colors on unsupported terminals.
    """

    if _supports_color():
        HEADER = "\033[95m"  # Magenta
        BLUE = "\033[94m"  # Blue
        CYAN = "\033[96m"  # Cyan
        GREEN = "\033[92m"  # Green
        YELLOW = "\033[93m"  # Yellow
        RED = "\033[91m"  # Red
        BOLD = "\033[1m"  # Bold
        UNDERLINE = "\033[4m]"  # Underline
        END = "\033[0m"  # Reset
    else:
        # Unsupported terminals: empty strings (no color codes)
        HEADER = ""
        BLUE = ""
        CYAN = ""
        GREEN = ""
        YELLOW = ""
        RED = ""
        BOLD = ""
        UNDERLINE = ""
        END = ""


# --- Colored Print Functions ---


def print_header(text: str, icon: str = ""):
    """Print header message (magenta, bold)."""
    icon_str = f"{icon} " if icon else ""
    print(f"{Colors.BOLD}{Colors.HEADER}{icon_str}{text}{Colors.END}")


def print_info(text: str, icon: str = "ℹ️"):
    """Print info message (cyan)."""
    icon_str = f"{icon} " if icon else ""
    print(f"{Colors.CYAN}{icon_str}{text}{Colors.END}")


def print_success(text: str, icon: str = "✓"):
    """Print success message (green)."""
    icon_str = f"{icon} " if icon else ""
    print(f"{Colors.GREEN}{icon_str}{text}{Colors.END}")


def print_warning(text: str, icon: str = "⚠"):
    """Print warning message (yellow)."""
    icon_str = f"{icon} " if icon else ""
    print(f"{Colors.YELLOW}{icon_str}{text}{Colors.END}")


def print_error(text: str, icon: str = "✗"):
    """Print error message (red)."""
    icon_str = f"{icon} " if icon else ""
    print(f"{Colors.RED}{icon_str}{text}{Colors.END}")


def print_step(text: str, icon: str = "🔹"):
    """Print step message (cyan, bold)."""
    icon_str = f"{icon} " if icon else ""
    print(f"{Colors.CYAN}{Colors.BOLD}{icon_str}{text}{Colors.END}")


def print_box(text: str, color: str = "BLUE", width: int = 60):
    """
    Print text in a box with borders.

    Args:
        text: Text to display
        color: Color name (BLUE, GREEN, CYAN, etc.)
        width: Box width
    """
    color_code = getattr(Colors, color, Colors.BLUE)
    print(f"{color_code}┌─ {text} {'─' * (width - len(text) - 4)}┐{Colors.END}")


def print_box_end(width: int = 60, color: str = "BLUE"):
    """Print box closing border."""
    color_code = getattr(Colors, color, Colors.BLUE)
    print(f"{color_code}└{'─' * width}┘{Colors.END}")


def print_separator(char: str = "=", width: int = 60, color: str = "BLUE"):
    """Print a separator line."""
    color_code = getattr(Colors, color, Colors.BLUE)
    print(f"{Colors.BOLD}{color_code}{char * width}{Colors.END}")


def print_assistant(text: str):
    """Print assistant/bot message (green with robot icon)."""
    print(f"{Colors.GREEN}🤖 Assistant: {Colors.END}{text}")


def print_user_prompt(text: str):
    """Print user input prompt (simple, single-line)."""
    return input(f"{Colors.YELLOW}👤 {text}{Colors.END}")


def print_user_prompt_multiline(text: str):
    """User input with multi-line support."""
    print(f"{Colors.YELLOW}👤 {text}{Colors.END}")
    print(
        f"{Colors.CYAN}   (Paste your text, then press Enter on empty line to finish){Colors.END}"
    )
    lines = []
    while True:
        try:
            line = input()
            if not line.strip():
                break
            lines.append(line)
        except (EOFError, KeyboardInterrupt):
            break
    return "\n".join(lines).strip()


def print_question_prompt(text: str):
    """Print question prompt (yellow with question icon)."""
    return input(f"{Colors.YELLOW}❓ {text}{Colors.END}")


# Backward compatibility: Keep Colors class exportable
__all__ = [
    "Colors",
    "print_header",
    "print_info",
    "print_success",
    "print_warning",
    "print_error",
    "print_step",
    "print_box",
    "print_box_end",
    "print_separator",
    "print_assistant",
    "print_user_prompt",
    "print_user_prompt_multiline",
    "print_question_prompt",
]
