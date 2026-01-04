# src package
# 
# This file has been refactored into a multi-agent architecture.
# The old monolithic code is preserved in __init__.old.py
#
# New structure:
# - agents/: BaseAgent, PromptGenerator, ToolFinder, Orchestrator
# - utils/: colors, db_manager
# - main.py: Entry point
#
# To run the application, use: python src/main.py
