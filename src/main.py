# main.py - CLI Entry Point

"""
MPAssist - Multi-Agent RAG System for Masterportal Configuration

This is the main entry point for the application.
It initializes the Orchestrator agent and starts the interactive CLI.
"""

from agents.orchestrator import Orchestrator


def main():
    """Main entry point for the MPAssist application."""
    try:
        orchestrator = Orchestrator()
        orchestrator.run()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Exiting...")
    except Exception as e:
        print(f"\n\nFatal error: {e}")
        raise


if __name__ == "__main__":
    main()
