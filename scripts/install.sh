#!/bin/bash

# CalPal Installation Script

echo "Installing CalPal - The Smart Meeting Scheduler Agent"
echo "========================================================"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed."
    echo "   Please install Python 3.8 or higher and try again."
    exit 1
fi

echo "Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo " pip3 is required but not installed."
    echo "   Please install pip3 and try again."
    exit 1
fi

echo "pip3 found: $(pip3 --version)"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "Dependencies installed successfully"
else
    echo "Failed to install dependencies"
    exit 1
fi

# Install CalPal in development mode
echo ""
echo "Installing CalPal..."
pip3 install -e .

if [ $? -eq 0 ]; then
    echo "CalPal installed successfully"
else
    echo "Failed to install CalPal"
    exit 1
fi

# Run tests
echo ""
echo "🧪 Running tests..."
python3 test_calpal.py

if [ $? -eq 0 ]; then
    echo ""
    echo "Installation complete!"
    echo ""
    echo "Next steps:"
    echo "1. Set up your Google AI API key:"
    echo "   export GOOGLE_GENERATIVE_AI_API_KEY='your-google-ai-api-key'"
    echo ""
    echo "2. Set up Google Calendar API:"
    echo "   - Go to https://console.cloud.google.com/"
    echo "   - Create a project and enable Google Calendar API"
    echo "   - Create OAuth 2.0 credentials"
    echo "   - Download credentials.json to this directory"
    echo ""
    echo "3. Run CalPal:"
    echo "   calpal schedule 'Lunch with John next Thursday at 1pm'"
    echo ""
    echo "4. Or get help:"
    echo "   calpal --help"
else
    echo "Tests failed. Please check the errors above."
    exit 1
fi

