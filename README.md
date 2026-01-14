# word-to-audio-
Text-to-Speech
README.md# Gemini Text-to-Speech Integration

This project provides a text-to-speech system that uses Google's Gemini API for enhanced natural language processing, with automatic fallback to Google TTS.

## Features

### Advanced TTS Integration (`advanced_tts_integration.py`)
- Support for multiple TTS engines
- Multiple audio formats (MP3, WAV, OGG)
- Enhanced API data extraction with path navigation
- Improved error handling and logging
- Support for different HTTP methods (GET, POST)
- Audio file format conversion
- Various playback options

### Gemini TTS Integration (`gemini_tts_integration.py`)
- Uses Google's Gemini API to enhance text processing
- Automatic fallback to Google TTS if Gemini API is unavailable
- Improved natural language processing for better speech output
- Detailed logging of API interactions
- See [GEMINI_README.md](GEMINI_README.md) for Gemini-specific setup

## Requirements

- Python 3.6+
- Internet connection (for API access and Google TTS)
- Gemini API key (for Gemini TTS features)

## Installation

### Quick Setup

Run the setup script:
```bash
./setup.sh
```

### Manual Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
   - Create a `.env` file in the project root
   - Add your API credentials (see [Environment Variables](#environment-variables))

## Usage

### Basic Usage

```python
from tts_integration import TTSIntegration

# Initialize TTS with API URL
tts = TTSIntegration(api_url="https://api.example.com/data")

# Fetch data, extract text, and convert to speech
audio_file = tts.text_to_speech("Hello, world!")

# Play the audio
tts.play_audio(audio_file)
```

### Advanced Usage

```python
from advanced_tts_integration import AdvancedTTSIntegration

# Initialize Advanced TTS
tts = AdvancedTTSIntegration(
    api_url="https://api.example.com/data",
    output_dir="audio_files",
    tts_engine="gtts",
    audio_format="mp3"
)

# Complete pipeline: fetch, extract, convert, and play
tts.process_pipeline(
    method="GET",
    headers={"Authorization": "Bearer token123"},
    text_key="data.content",
    output_filename="example_output",
    lang="en",
    auto_play=True
)
```

### Using Gemini TTS

```python
from gemini_tts_integration import GeminiTTSIntegration
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Gemini TTS
tts = GeminiTTSIntegration(output_dir="gemini_audio")

# Convert text to speech using Gemini API
audio_file = tts.text_to_speech(
    text="This is processed through Gemini API for improved natural language processing.",
    filename="gemini_example"
)

# Play the audio
tts.play_audio(audio_file)
```

## Environment Variables

Create a `.env` file with the following variables:

```
# For news API example
NEWS_API_BASE_URL="https://your-news-api.com/api"
NEWS_API_TOKEN="your_api_token"

# For Gemini TTS integration
GEMINI_API_KEY="your_gemini_api_key"
```

## Examples

Example scripts provided:

- `gemini_news_example.py`: Uses Gemini API to process news text before TTS conversion
- `test_gemini_api.py`: Tests if your Gemini API key is valid

Run the news example:

```bash
python gemini_news_example.py
```

Test your Gemini API key:

```bash
python test_gemini_api.py
```

## Extending

You can extend the integration with new TTS engines or API sources by:

1. Subclassing `AdvancedTTSIntegration`
2. Implementing your own `text_to_speech` method
3. Adding any additional functionality needed

See `gemini_tts_integration.py` for an example of extending the base functionality.
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   ```bash
   # On Linux/macOS
   source venv/bin/activate
   
   # On Windows
   venv\Scripts\activate
   ```
4. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

Run the basic script with default settings:

```bash
python tts_integration.py
```

Or run the example script:

```bash
python example.py
```

### Advanced Usage

Run the advanced script:

```bash
python advanced_tts_integration.py
```

Or run the advanced example script:

```bash
python advanced_example.py
```

### Integration in Your Own Code

#### Basic TTS Integration

```python
from tts_integration import TTSIntegration

# Initialize with custom API URL and output directory
tts = TTSIntegration(
    api_url="https://your-api-endpoint.com/data",
    output_dir="custom_audio_folder"
)

# Run the complete pipeline with custom parameters
audio_file = tts.process_pipeline(
    text_key='content',      # The key to extract text from in the JSON response
    output_filename='my_audio',  # Custom filename for the output audio
    lang='fr'                # Language code (default is 'en' for English)
)

# Or run individual steps
data = tts.fetch_data()
text = tts.extract_text(data, text_key='body')
audio_file = tts.text_to_speech(text, filename='speech_output')
tts.play_audio(audio_file)
```

#### Advanced TTS Integration

```python
from advanced_tts_integration import AdvancedTTSIntegration

# Initialize with custom settings
tts = AdvancedTTSIntegration(
    api_url="https://your-api-endpoint.com/data",
    output_dir="custom_audio_folder",
    tts_engine="gtts",       # TTS engine to use
    audio_format="wav"       # Output audio format
)

# Run the complete pipeline with custom parameters
audio_file = tts.process_pipeline(
    method="POST",           # HTTP method
    headers={"Authorization": "Bearer YOUR_TOKEN"},  # Custom headers
    params={"param1": "value1"},  # URL parameters
    json_data={"key": "value"},  # JSON data for POST requests
    text_key='content',      # The key to extract text from in the JSON response
    output_filename='my_audio',  # Custom filename for the output audio
    lang='fr',               # Language code (default is 'en' for English)
    max_length=1000,         # Maximum text length to process
    auto_play=True           # Whether to automatically play the audio
)
```

## Customization

### Basic TTS Integration
- Change the API URL in the script to fetch data from different sources
- Modify the `text_key` parameter to extract text from different fields in the API response
- Change the language using the `lang` parameter (e.g., 'en' for English, 'fr' for French)

### Advanced TTS Integration
- Choose different TTS engines (currently supports Google TTS)
- Select output audio formats (MP3, WAV, OGG)
- Use dot notation to extract text from complex nested structures
- Set maximum text length for processing
- Configure HTTP request parameters (headers, method, etc.)
- Enable/disable auto-playback of generated audio

## Supported TTS Engines

Currently, the following TTS engines are supported:

- `gtts`: Google Text-to-Speech (default)

## Supported Audio Formats

- MP3: MPEG Audio Layer III (default)
- WAV: Waveform Audio File Format
- OGG: Ogg Vorbis Audio

## Supported Languages

The script uses Google TTS which supports multiple languages. Use the appropriate language code:

- English: 'en'
- French: 'fr'
- Spanish: 'es'
- German: 'de'
- Italian: 'it'
- And many more...

## Troubleshooting

- Ensure you have an active internet connection
- Check that the API URL is correct and accessible
- Make sure the required packages are installed
- Verify that your system has audio capabilities for playback
- Check the log file (`tts_integration.log`) for detailed error information in the advanced version

## License

This project is licensed under the MIT License.
