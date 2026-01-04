#!/bin/bash

# MPAssist - Run Script with Virtual Environment
# This script activates the virtual environment and runs the application

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Error: Virtual environment not found."
    echo "Please run './setup.sh' first to create the virtual environment."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if we're in the virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "❌ Error: Failed to activate virtual environment."
    exit 1
fi

echo "✅ Virtual environment activated: $VIRTUAL_ENV"

# Navigate to src directory and run the application
cd src
echo "🚀 Starting MPAssist..."
python main.py

# Deactivate is automatic when script ends, but good practice to include
deactivate
