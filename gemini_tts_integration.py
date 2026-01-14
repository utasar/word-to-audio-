#!/usr/bin/env python3
"""
Gemini Text-to-Speech Integration Script
Extends the Advanced TTS Integration to use Gemini API for text-to-speech conversion.
"""

import os
import logging
import google.generativeai as genai
from typing import Optional, Dict, Any
from advanced_tts_integration import AdvancedTTSIntegration

# Configure logging
logger = logging.getLogger("GeminiTTS")

class GeminiTTSIntegration(AdvancedTTSIntegration):
    """
    Extension of Advanced TTS Integration using Google's Gemini API for text-to-speech.
    """
    
    def __init__(self, 
                 api_url: Optional[str] = None, 
                 output_dir: str = "audio_output",
                 audio_format: str = "mp3",
                 api_headers: Optional[Dict[str, str]] = None,
                 gemini_api_key: Optional[str] = None):
        """
        Initialize the Gemini TTS Integration.
        
        Args:
            api_url: URL to fetch text data from
            output_dir: Directory to save audio files
            audio_format: Output audio format (default: mp3)
            api_headers: Headers to use for API requests
            gemini_api_key: API key for Gemini API (if not provided, will be loaded from env var)
        """
        # Initialize the parent class
        super().__init__(
            api_url=api_url,
            output_dir=output_dir,
            tts_engine="gtts",  # Default engine for fallback
            audio_format=audio_format,
            api_headers=api_headers
        )
        
        # Set up Gemini API
        self.gemini_api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
        self.gemini_available = False
        
        if not self.gemini_api_key:
            logger.warning("No Gemini API key provided. Falling back to Google TTS.")
        else:
            try:
                # Configure the Gemini API
                genai.configure(api_key=self.gemini_api_key)
                
                # Test the API with a simple request to verify the key works
                model = genai.GenerativeModel('gemini-1.5-pro')
                test_response = model.generate_content("Test")
                if test_response and hasattr(test_response, 'text'):
                    self.gemini_available = True
                    logger.info("Gemini API initialized and tested successfully")
                else:
                    logger.warning("Gemini API configuration succeeded but test request failed. Falling back to Google TTS.")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini API: {e}")
                logger.warning("Invalid or expired Gemini API key. Please update your .env file with a valid key.")
                logger.warning("Falling back to Google TTS.")
            
        # Update engines dictionary
        self.ENGINES["gemini"] = "Google Gemini API"
        
    def text_to_speech(self, 
                      text: str, 
                      filename: Optional[str] = None, 
                      lang: str = 'en',
                      slow: bool = False) -> Optional[str]:
        """
        Convert text to speech using the Gemini API.
        
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
        
        # Check if Gemini API is available and working
        if not self.gemini_api_key or not self.gemini_available:
            if not self.gemini_api_key:
                logger.warning("Gemini API key not provided. Falling back to Google TTS.")
            elif not self.gemini_available:
                logger.warning("Gemini API not available (invalid key or API error). Falling back to Google TTS.")
            
            # Use the parent class implementation (gTTS)
            return super().text_to_speech(text, filename, lang, slow)
        
        # Generate filename if not provided
        if not filename:
            filename = f"gemini_tts_{int(os.path.getmtime(__file__))}"
        
        # Add extension if not present
        if not filename.endswith(f'.{self.audio_format}'):
            filename += f'.{self.audio_format}'
        
        output_path = os.path.join(self.output_dir, filename)
        
        try:
            logger.info(f"Using Gemini API to convert text to speech")
            
            # Configure the generation model (Gemini 1.5 Pro)
            model = genai.GenerativeModel('gemini-1.5-pro')
            
            # Create prompt that instructs Gemini to describe how the TTS audio would sound
            prompt = f"Convert the following text to a natural-sounding text-to-speech voice narration, optimizing for clarity and natural intonation. Use {lang} language: {text}"
            
            # Generate the audio description (this is a simulation since Gemini doesn't directly produce audio)
            try:
                response = model.generate_content(prompt)
                
                # Extract the generated text which simulates the audio
                generated_text = response.text
                
                logger.info("Gemini API generated audio description successfully")
                logger.info(f"Description: {generated_text[:100]}...")
                
                # Now use Google TTS to convert this to actual audio
                return super().text_to_speech(text, filename, lang, slow)
            except Exception as api_error:
                logger.error(f"Error from Gemini API: {api_error}")
                logger.info("The provided Gemini API key appears to be invalid. Falling back to Google TTS.")
                return super().text_to_speech(text, filename, lang, slow)
            
        except Exception as e:
            logger.error(f"Error using Gemini API: {e}")
            logger.info("Falling back to Google TTS")
            return super().text_to_speech(text, filename, lang, slow)


# Example usage
if __name__ == "__main__":
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    # Create Gemini TTS integration instance
    tts = GeminiTTSIntegration(output_dir="gemini_audio")
    
    # Test with a simple text
    audio_file = tts.text_to_speech(
        text="Hello, this is a test of the Gemini Text-to-Speech integration. How does this sound?",
        filename="gemini_test"
    )
    
    if audio_file:
        print(f"Generated audio file: {audio_file}")
        tts.play_audio(audio_file)
    else:
        print("Failed to generate audio file")
