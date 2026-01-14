#!/usr/bin/env python3
"""
Advanced Text-to-Speech Integration Script
Fetches data from multiple API sources, extracts text, and converts it to speech
using various TTS engines.
"""

import requests
import json
import os
import logging
import time
from typing import Dict, List, Union, Optional, Any
from gtts import gTTS  # Google Text-to-Speech
import pygame  # For audio playback
from dotenv import load_dotenv  # For loading environment variables

# Load environment variables from .env file
load_dotenv()

# Try to import pydub for audio manipulation, but provide a fallback if it fails
try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False
    logging.warning("pydub is not available. Some audio format conversion features will be disabled.")

import tempfile

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("tts_integration.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("AdvancedTTS")


class AdvancedTTSIntegration:
    """Advanced Text-to-Speech integration with multiple TTS engines and API support."""
    
    # Supported TTS engines
    ENGINES = {
        "gtts": "Google Text-to-Speech",
        # Add more engines as they become available
    }
    
    # Supported audio formats
    FORMATS = {
        "mp3": "MPEG Audio Layer III",
        "wav": "Waveform Audio File Format",
        "ogg": "Ogg Vorbis Audio"
    }
    
    def __init__(self, 
                 api_url: Optional[str] = None, 
                 output_dir: str = "audio_output",
                 tts_engine: str = "gtts",
                 audio_format: str = "mp3",
                 api_headers: Optional[Dict[str, str]] = None):
        """
        Initialize the Advanced TTS Integration class.
        
        Args:
            api_url: URL to fetch text data from
            output_dir: Directory to save audio files
            tts_engine: TTS engine to use (default: gtts)
            audio_format: Output audio format (default: mp3)
            api_headers: Headers to use for API requests
        """
        self.api_url = api_url
        self.output_dir = output_dir
        self.api_headers = api_headers or {}
        
        # Validate and set TTS engine
        if tts_engine not in self.ENGINES:
            supported = ", ".join(self.ENGINES.keys())
            logger.warning(f"TTS engine '{tts_engine}' not supported. Using 'gtts' instead. "
                          f"Supported engines: {supported}")
            self.tts_engine = "gtts"
        else:
            self.tts_engine = tts_engine
            
        # Validate and set audio format
        if audio_format not in self.FORMATS:
            supported = ", ".join(self.FORMATS.keys())
            logger.warning(f"Audio format '{audio_format}' not supported. Using 'mp3' instead. "
                          f"Supported formats: {supported}")
            self.audio_format = "mp3"
        else:
            self.audio_format = audio_format
            
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            logger.info(f"Created output directory: {output_dir}")
        
        # Initialize pygame mixer for audio playback
        try:
            pygame.mixer.init()
            logger.info("Initialized pygame mixer for audio playback")
        except Exception as e:
            logger.error(f"Failed to initialize pygame mixer: {e}")
    
    def fetch_data(self, 
                  api_url: Optional[str] = None, 
                  method: str = "GET", 
                  headers: Optional[Dict[str, str]] = None, 
                  params: Optional[Dict[str, Any]] = None,
                  json_data: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Fetch data from the specified API.
        
        Args:
            api_url: URL to fetch data from (overrides instance variable if provided)
            method: HTTP method to use (GET, POST, etc.)
            headers: HTTP headers to send with the request
            params: Query parameters to include in the request
            json_data: JSON data to include in the request body (for POST requests)
            
        Returns:
            dict: JSON response from the API or None if request failed
        """
        url = api_url or self.api_url
        
        if not url:
            logger.error("API URL must be provided")
            raise ValueError("API URL must be provided")
        
        # Merge headers with instance headers
        request_headers = {**self.api_headers, **(headers or {})}
        
        try:
            logger.info(f"Fetching data from {url} using {method} method")
            
            if method.upper() == "GET":
                response = requests.get(url, headers=request_headers, params=params)
            elif method.upper() == "POST":
                response = requests.post(url, headers=request_headers, params=params, json=json_data)
            else:
                logger.error(f"Unsupported HTTP method: {method}")
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()  # Raise exception for HTTP errors
            
            # Check if response is JSON
            content_type = response.headers.get("Content-Type", "")
            if "application/json" in content_type:
                return response.json()
            else:
                # Try to parse as JSON anyway, but log a warning
                logger.warning(f"Response is not JSON (Content-Type: {content_type}). Attempting to parse as JSON anyway.")
                return response.json()
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data from API: {e}")
            return None
        except json.JSONDecodeError:
            logger.error("Failed to decode response as JSON")
            return None
    
    def extract_text(self, 
                    data: Union[Dict[str, Any], List[Any]], 
                    text_key: str = 'text',
                    max_length: Optional[int] = None) -> str:
        """
        Extract text from the data, with intelligent traversal of complex data structures.
        
        Args:
            data: Data containing text
            text_key: Key to extract text from
            max_length: Maximum length of text to extract (None for no limit)
            
        Returns:
            str: Extracted text
        """
        if not data:
            logger.warning("No data provided for text extraction")
            return ""
        
        extracted_text = ""
        
        # Handle direct access via dot notation (e.g., "data.articles.0.title")
        if "." in text_key:
            parts = text_key.split(".")
            current = data
            try:
                for part in parts:
                    if isinstance(current, list) and part.isdigit():
                        current = current[int(part)]
                    elif isinstance(current, dict) and part in current:
                        current = current[part]
                    else:
                        logger.warning(f"Could not navigate to {part} in {text_key}")
                        return ""
                
                if isinstance(current, (str, int, float)):
                    extracted_text = str(current)
                else:
                    logger.warning(f"Final value for {text_key} is not a string: {type(current)}")
                    return ""
            except (IndexError, KeyError) as e:
                logger.warning(f"Error navigating path {text_key}: {e}")
                return ""
                
        # Handle different data structures
        elif isinstance(data, dict):
            # If text_key exists in the data, return its value
            if text_key in data:
                if isinstance(data[text_key], (str, int, float)):
                    extracted_text = str(data[text_key])
                elif isinstance(data[text_key], list):
                    # Join list items if they're strings
                    extracted_text = " ".join(str(item) for item in data[text_key] if isinstance(item, (str, int, float)))
            
            # Recursive search in nested dictionaries if no text found yet
            if not extracted_text:
                for key, value in data.items():
                    if isinstance(value, (dict, list)):
                        result = self.extract_text(value, text_key)
                        if result:
                            extracted_text = result
                            break
        
        # Handle list type data
        elif isinstance(data, list):
            # Concatenate all text items in the list
            all_text = []
            for item in data:
                if isinstance(item, (dict, list)):
                    extracted = self.extract_text(item, text_key)
                    if extracted:
                        all_text.append(extracted)
                elif isinstance(item, (str, int, float)) and text_key == "":
                    # If text_key is empty, collect all string items
                    all_text.append(str(item))
            
            extracted_text = " ".join(all_text)
        
        # Apply maximum length if specified
        if max_length and len(extracted_text) > max_length:
            logger.info(f"Trimming extracted text to {max_length} characters")
            extracted_text = extracted_text[:max_length]
        
        return extracted_text
    
    def text_to_speech(self, 
                      text: str, 
                      filename: Optional[str] = None, 
                      lang: str = 'en',
                      slow: bool = False) -> Optional[str]:
        """
        Convert text to speech using the selected TTS engine.
        
        Args:
            text: Text to convert to speech
            filename: Output filename (without extension)
            lang: Language code
            slow: Whether to speak slowly
            
        Returns:
            str: Path to the saved audio file or None if conversion failed
        """
        if not text:
            logger.warning("No text provided for conversion")
            return None
        
        # Generate filename if not provided
        if not filename:
            timestamp = int(time.time())
            filename = f"tts_output_{timestamp}"
        
        # Add extension if not present
        if not filename.endswith(f'.{self.audio_format}'):
            filename += f'.{self.audio_format}'
        
        output_path = os.path.join(self.output_dir, filename)
        
        try:
            if self.tts_engine == "gtts":
                logger.info(f"Using Google TTS to convert text to speech ({lang})")
                
                # If format is not mp3 and pydub is not available, fall back to mp3
                if self.audio_format != "mp3" and not PYDUB_AVAILABLE:
                    logger.warning(f"Cannot convert to {self.audio_format} without pydub. Falling back to mp3.")
                    original_path = os.path.splitext(output_path)[0] + ".mp3"
                    tts = gTTS(text=text, lang=lang, slow=slow)
                    tts.save(original_path)
                    return original_path
                
                # First create MP3 (gTTS only supports MP3)
                tts = gTTS(text=text, lang=lang, slow=slow)
                
                if self.audio_format == "mp3":
                    tts.save(output_path)
                elif PYDUB_AVAILABLE:
                    # For other formats, save to a temporary MP3 file and convert
                    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp_file:
                        temp_path = tmp_file.name
                        
                    tts.save(temp_path)
                    
                    # Convert to the desired format
                    audio = AudioSegment.from_mp3(temp_path)
                    audio.export(output_path, format=self.audio_format)
                    
                    # Remove temporary file
                    os.unlink(temp_path)
            
            else:
                logger.error(f"TTS engine '{self.tts_engine}' not implemented")
                return None
                
            logger.info(f"Text converted to speech and saved as '{output_path}'")
            return output_path
            
        except Exception as e:
            logger.error(f"Error converting text to speech: {e}")
            return None
    
    def play_audio(self, audio_file: str) -> bool:
        """
        Play the audio file.
        
        Args:
            audio_file: Path to the audio file
            
        Returns:
            bool: True if audio played successfully, False otherwise
        """
        if not os.path.exists(audio_file):
            logger.error(f"Audio file not found: {audio_file}")
            return False
        
        try:
            # Convert to a format pygame can play if needed
            temp_file_created = False
            
            if not audio_file.endswith('.mp3') and not audio_file.endswith('.wav'):
                if PYDUB_AVAILABLE:
                    logger.info(f"Converting {audio_file} to a format pygame can play")
                    audio = AudioSegment.from_file(audio_file)
                    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp_file:
                        temp_path = tmp_file.name
                    
                    audio.export(temp_path, format="mp3")
                    audio_file = temp_path
                    temp_file_created = True
                else:
                    logger.warning(f"Cannot play {audio_file} format without pydub. Only MP3 and WAV are supported directly.")
                    return False
            
            logger.info(f"Playing audio: {audio_file}")
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            
            # Wait for audio to finish playing
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
                
            # Remove temporary file if created
            if temp_file_created:
                os.unlink(audio_file)
                
            return True
        
        except Exception as e:
            logger.error(f"Error playing audio: {e}")
            return False
    
    def process_pipeline(self,
                        api_url: Optional[str] = None,
                        method: str = "GET",
                        headers: Optional[Dict[str, str]] = None,
                        params: Optional[Dict[str, Any]] = None,
                        json_data: Optional[Dict[str, Any]] = None,
                        text_key: str = 'text',
                        output_filename: Optional[str] = None,
                        lang: str = 'en',
                        slow: bool = False,
                        max_length: Optional[int] = None,
                        auto_play: bool = True) -> Optional[str]:
        """
        Run the complete pipeline: fetch data, extract text, convert to speech, and play.
        
        Args:
            api_url: API URL to fetch data from
            method: HTTP method to use
            headers: HTTP headers to send with the request
            params: Query parameters for the request
            json_data: JSON data for POST requests
            text_key: Key to extract text from the data
            output_filename: Output audio filename
            lang: Language code for TTS
            slow: Whether to speak slowly
            max_length: Maximum length of text to process
            auto_play: Whether to automatically play the audio
            
        Returns:
            str: Path to the generated audio file or None if pipeline failed
        """
        # Fetch data from API
        data = self.fetch_data(
            api_url=api_url, 
            method=method, 
            headers=headers, 
            params=params, 
            json_data=json_data
        )
        
        if not data:
            logger.error("No data fetched from API")
            return None
        
        # Extract text from data
        text = self.extract_text(data, text_key, max_length)
        
        if not text:
            logger.error("No text extracted from data")
            return None
        
        logger.info(f"Extracted text: {text[:100]}..." if len(text) > 100 else f"Extracted text: {text}")
        
        # Convert text to speech
        audio_file = self.text_to_speech(
            text=text, 
            filename=output_filename, 
            lang=lang,
            slow=slow
        )
        
        if audio_file and os.path.exists(audio_file) and auto_play:
            # Play the audio
            self.play_audio(audio_file)
        
        return audio_file


# Example usage
if __name__ == "__main__":
    # Example API URL
    API_URL = "https://jsonplaceholder.typicode.com/posts/1"
    
    # Create Advanced TTS integration instance
    tts = AdvancedTTSIntegration(
        api_url=API_URL,
        output_dir="audio_output",
        tts_engine="gtts",
        audio_format="mp3"
    )
    
    # Run the complete pipeline
    audio_file = tts.process_pipeline(text_key='body')
    
    if audio_file:
        print(f"Generated audio file: {audio_file}")
    else:
        print("Failed to generate audio file")
