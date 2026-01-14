# Gemini API Integration 

This document explains how to set up and use the Gemini API for text-to-speech conversion in this project.

## What's Included

- `gemini_tts_integration.py`: An extension of the Advanced TTS Integration that uses the Gemini API
- `gemini_news_example.py`: An example script showing how to use Gemini API for converting news to speech
- `test_gemini_api.py`: A utility to test if your Gemini API key is valid

## Getting a Valid Gemini API Key

The sample Gemini API key in the `.env` file is a placeholder and will not work. To get a valid API key:

1. Go to the [Google AI Studio](https://ai.google.dev/) and sign in with your Google account
2. Click on "Get API key" in the top navigation
3. Create a new API key or use an existing one
4. Copy the API key

## Configuration

1. Open your `.env` file and replace the placeholder API key with your valid Gemini API key:

```
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

2. Ensure you have installed the required packages:

```bash
pip install -r requirements.txt
```

3. Test your API key:

```bash
python test_gemini_api.py
```

If successful, you should see a confirmation message. If not, the script will provide troubleshooting guidance.

## Usage

### Running the Gemini News Example

```bash
python gemini_news_example.py
```

### Using the Gemini TTS Integration in Your Code

```python
from gemini_tts_integration import GeminiTTSIntegration
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Gemini TTS integration instance
tts = GeminiTTSIntegration(output_dir="gemini_audio")

# Convert text to speech
audio_file = tts.text_to_speech(
    text="This is a test of the Gemini Text-to-Speech integration.",
    filename="gemini_test"
)

# Play the audio
if audio_file:
    tts.play_audio(audio_file)
```

## How It Works

1. The `GeminiTTSIntegration` class extends `AdvancedTTSIntegration` to use the Gemini API
2. It first validates your Gemini API key during initialization
3. When converting text to speech:
   - If the Gemini API is available, it processes the text using Gemini's language capabilities
   - It then passes the processed text to Google TTS for the actual audio generation
   - If the Gemini API is unavailable (invalid key, API error), it gracefully falls back to Google TTS

## Fallback Behavior

The integration is designed with robust fallback mechanisms:

- If the Gemini API key is missing, it falls back to Google TTS
- If the key is invalid or the API returns an error, it falls back to Google TTS
- If the API request times out, it falls back to Google TTS

In all cases, you'll still get audio output, just without the Gemini processing enhancements.

## Error Handling and Logging

All Gemini API interactions are logged to `tts_integration.log`, including:
- API key validation attempts
- Successful processing through Gemini
- API errors and fallbacks

## Future Enhancements

- Direct audio output from Gemini API when available
- Support for more voice styles and emotions
- Advanced language processing for better narration of news content
