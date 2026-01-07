"""
Test script for MPAssist Gradio integration.

This script verifies that all components are properly configured
before running the web application.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


def test_imports():
    """Test that all required packages are installed."""
    print("Testing imports...")
    try:
        import gradio as gr

        print(f"  ✓ Gradio {gr.__version__}")
    except ImportError as e:
        print(f"  ✗ Gradio import failed: {e}")
        return False

    try:
        import openai

        print(f"  ✓ OpenAI package")
    except ImportError as e:
        print(f"  ✗ OpenAI import failed: {e}")
        return False

    try:
        from langchain_openai import ChatOpenAI

        print(f"  ✓ LangChain OpenAI")
    except ImportError as e:
        print(f"  ✗ LangChain OpenAI import failed: {e}")
        return False

    try:
        from langchain_chroma import Chroma

        print(f"  ✓ LangChain Chroma")
    except ImportError as e:
        print(f"  ✗ LangChain Chroma import failed: {e}")
        return False

    return True


def test_env_variables():
    """Test that required environment variables are set."""
    print("\nTesting environment variables...")
    token = os.environ.get("IONOS_API_TOKEN")
    if token:
        print(f"  ✓ IONOS_API_TOKEN is set (length: {len(token)})")
        return True
    else:
        print("  ✗ IONOS_API_TOKEN is not set")
        print("    Set it with: export IONOS_API_TOKEN='your-token'")
        return False


def test_database():
    """Test that the vector database exists."""
    print("\nTesting vector database...")
    db_path = os.path.join(os.path.dirname(__file__), "db")
    if os.path.exists(db_path):
        print(f"  ✓ Database found at {db_path}")
        return True
    else:
        print(f"  ✗ Database not found at {db_path}")
        print("    Run: python ingest.py")
        return False


def test_agents():
    """Test that agent modules can be imported."""
    print("\nTesting agent modules...")
    try:
        from agents.orchestrator import Orchestrator

        print("  ✓ Orchestrator")
    except Exception as e:
        print(f"  ✗ Orchestrator import failed: {e}")
        return False

    try:
        from services.chat_service import get_chat_service

        print("  ✓ ChatService")
    except Exception as e:
        print(f"  ✗ ChatService import failed: {e}")
        return False

    return True


def test_ionos_connection():
    """Test connection to IONOS API."""
    print("\nTesting IONOS API connection...")

    if not os.environ.get("IONOS_API_TOKEN"):
        print("  ⊘ Skipped (IONOS_API_TOKEN not set)")
        return None

    try:
        from langchain_openai import ChatOpenAI
        from settings import LLM_MODEL, IONOS_API_BASE_URL, IONOS_API_TOKEN

        llm = ChatOpenAI(
            model=LLM_MODEL,
            base_url=IONOS_API_BASE_URL,
            api_key=IONOS_API_TOKEN,
            timeout=10,
        )

        response = llm.invoke("Say 'test successful' and nothing else.")
        print(f"  ✓ IONOS API connection successful")
        print(f"    Model: {LLM_MODEL}")
        print(f"    Response: {response.content[:50]}...")
        return True
    except Exception as e:
        print(f"  ✗ IONOS API connection failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("MPAssist Gradio Integration Test")
    print("=" * 60)

    results = {
        "Imports": test_imports(),
        "Environment Variables": test_env_variables(),
        "Database": test_database(),
        "Agents": test_agents(),
        "IONOS Connection": test_ionos_connection(),
    }

    print("\n" + "=" * 60)
    print("Test Results:")
    print("=" * 60)

    for test_name, result in results.items():
        if result is True:
            status = "✓ PASS"
        elif result is False:
            status = "✗ FAIL"
        else:
            status = "⊘ SKIP"
        print(f"  {status}: {test_name}")

    # Count passes and fails
    passed = sum(1 for r in results.values() if r is True)
    failed = sum(1 for r in results.values() if r is False)

    print("\n" + "=" * 60)
    if failed == 0:
        print("✓ All tests passed! Ready to run the app.")
        print("\nRun the app with:")
        print("  ./run_web.sh")
        print("\nOr directly:")
        print("  cd src && python app.py")
        return 0
    else:
        print(f"✗ {failed} test(s) failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
