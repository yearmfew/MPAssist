# utils/spinner.py

import sys
import threading
import time
from utils.console import Colors


class Spinner:
    """
    Simple terminal spinner for showing progress during LLM processing.
    """

    def __init__(self, message="Processing"):
        self.message = message
        self.spinner_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.is_spinning = False
        self.thread = None

    def _spin(self):
        """Internal method that runs the spinner animation."""
        idx = 0
        while self.is_spinning:
            sys.stdout.write(
                f"\r{Colors.CYAN}{self.spinner_chars[idx]} {self.message}...{Colors.END}"
            )
            sys.stdout.flush()
            idx = (idx + 1) % len(self.spinner_chars)
            time.sleep(0.1)
        # Clear the spinner line
        sys.stdout.write("\r" + " " * (len(self.message) + 10) + "\r")
        sys.stdout.flush()

    def start(self):
        """Start the spinner in a separate thread."""
        if not self.is_spinning:
            self.is_spinning = True
            self.thread = threading.Thread(target=self._spin, daemon=True)
            self.thread.start()

    def stop(self):
        """Stop the spinner and clean up."""
        if self.is_spinning:
            self.is_spinning = False
            if self.thread:
                self.thread.join()


# Context manager for easy usage
class SpinnerContext:
    """Context manager for spinner - automatically starts and stops."""

    def __init__(self, message="Processing"):
        self.spinner = Spinner(message)

    def __enter__(self):
        self.spinner.start()
        return self.spinner

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.spinner.stop()
        return False
