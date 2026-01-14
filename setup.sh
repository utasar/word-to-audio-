#!/bin/bash
# Setup script for Gemini TTS Integration

echo "Setting up Gemini TTS Integration..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Setup complete!"
echo ""
echo "To use the system:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Get a Gemini API key from https://ai.google.dev/"
echo "3. Update your .env file with the API key"
echo "4. Test your API key: python test_gemini_api.py"
echo "5. Run the news example: python gemini_news_example.py"
echo ""
echo "For more information, see README.md and GEMINI_README.md"
