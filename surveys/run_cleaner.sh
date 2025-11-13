#!/bin/bash
#
# Survey Cleaner - Orchestrator Wrapper
#
# This script activates the Python venv and runs the orchestrator,
# which handles all survey processing via Anthropic API calls.
#
# Usage:
#   ./surveys/run_cleaner.sh <survey_name> [--limit N]
#
# Examples:
#   ./surveys/run_cleaner.sh ces19              # Process all variables
#   ./surveys/run_cleaner.sh test --limit 5     # Process first 5 variables
#

set -e  # Exit on error

# Check if survey name provided
if [ -z "$1" ]; then
    echo "Usage: ./surveys/run_cleaner.sh <survey_name> [--limit N]"
    echo ""
    echo "Examples:"
    echo "  ./surveys/run_cleaner.sh ces19"
    echo "  ./surveys/run_cleaner.sh test --limit 5"
    exit 1
fi

# Activate virtual environment
if [ ! -f "venv/bin/activate" ]; then
    echo "Error: Virtual environment not found."
    echo "Please run: ./setup.sh"
    exit 1
fi

echo "Activating virtual environment..."
source venv/bin/activate

# Verify Python from venv
PYTHON_PATH=$(which python)
if [[ "$PYTHON_PATH" != *"venv/bin/python"* ]]; then
    echo "Error: Virtual environment not activated correctly"
    echo "Python path: $PYTHON_PATH"
    exit 1
fi

echo "Python: $PYTHON_PATH"
echo ""

# Run Python orchestrator (handles everything via Anthropic API)
# Note: ANTHROPIC_API_KEY is loaded from .env by Python's dotenv
echo "Starting survey processing orchestrator..."
echo "Orchestrator will call agents via Anthropic API..."
echo ""
python surveys/process_survey.py "$@"
