#!/usr/bin/env python3
"""
Example script demonstrating how to use Gemini API for TTS with news content.
This example shows how to fetch news from a custom API and convert it to speech using Gemini.
"""

import os
from gemini_tts_integration import GeminiTTSIntegration
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    """
    Main function demonstrating the Gemini TTS Integration with news API.
    """
    # Get API credentials from environment variables
    news_api_base_url = os.getenv("NEWS_API_BASE_URL")
    news_api_token = os.getenv("NEWS_API_TOKEN")
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    
    if not news_api_base_url or not news_api_token:
        print("Error: Missing API credentials in .env file")
        print("Make sure NEWS_API_BASE_URL and NEWS_API_TOKEN are set in the .env file")
        return
    
    if not gemini_api_key:
        print("Warning: GEMINI_API_KEY is not set in the .env file")
        print("Falling back to Google TTS")
    
    print(f"Using News API URL: {news_api_base_url}")
    print(f"API Token (first 10 chars): {news_api_token[:10]}...")
    print(f"Gemini API Key (first 10 chars): {gemini_api_key[:10]}..." if gemini_api_key else "Gemini API Key: Not provided")
    
    # Create an instance of the Gemini TTS Integration
    tts = GeminiTTSIntegration(
        output_dir="gemini_news_audio",
        gemini_api_key=gemini_api_key
    )
    
    # Set up headers with API token
    headers = {
        "Authorization": f"Bearer {news_api_token}",
        "Content-Type": "application/json"
    }
    
    print("\n=== Example: Fetching Latest News Headline with Gemini TTS ===")
    
    try:
        # First fetch the data to inspect its structure
        print("Fetching data from API...")
        data = tts.fetch_data(
            api_url=f"{news_api_base_url}/news?pagination[page]=1&pagination[pageSize]=12&populate=*&sort[0][createdAt]=desc",
            method="GET",
            headers=headers
        )
        
        if data:
            print("API response received successfully.")
            
            # Check if 'data' key exists and is a list
            if 'data' in data and isinstance(data['data'], list) and len(data['data']) > 0:
                print(f"Found {len(data['data'])} news items.")
                
                # Get first news item
                first_news = data['data'][0]
                
                # Check for news content fields
                if isinstance(first_news, dict):
                    # Extract available fields for TTS
                    content_fields = []
                    
                    if 'short_description' in first_news and first_news['short_description']:
                        content_fields.append(('short_description', first_news['short_description']))
                        print(f"Short description: {first_news['short_description'][:100]}..." if len(first_news['short_description']) > 100 else f"Short description: {first_news['short_description']}")
                    
                    if 'title' in first_news and first_news['title']:
                        content_fields.append(('title', first_news['title']))
                        print(f"Title: {first_news['title']}")
                    
                    # Process each field with Gemini TTS
                    for field_name, field_content in content_fields:
                        print(f"\nConverting {field_name} to speech using Gemini...")
                        
                        audio_file = tts.text_to_speech(
                            text=field_content,
                            filename=f"gemini_news_{field_name}",
                            lang="en"
                        )
                        
                        if audio_file:
                            print(f"Generated audio for {field_name}: {audio_file}")
                            print("Playing audio...")
                            tts.play_audio(audio_file)
                        else:
                            print(f"Failed to generate audio for {field_name}")
                
                # Try the complete pipeline as well
                print("\nRunning complete pipeline with Gemini TTS...")
                news_audio = tts.process_pipeline(
                    api_url=f"{news_api_base_url}/news?pagination[page]=1&pagination[pageSize]=12&populate=*&sort[0][createdAt]=desc",
                    method="GET",
                    headers=headers,
                    text_key="data.0.short_description",  # Only use short_description from first item in data array
                    output_filename="gemini_latest_news",
                    lang="en"
                )
                
                if news_audio:
                    print(f"Pipeline generated news audio: {news_audio}")
                else:
                    print("Pipeline failed to generate news audio with description. Trying with title...")
                    
                    # Try with title as fallback
                    title_audio = tts.process_pipeline(
                        api_url=f"{news_api_base_url}/news?pagination[page]=1&pagination[pageSize]=12&populate=*&sort[0][createdAt]=desc",
                        method="GET",
                        headers=headers,
                        text_key="data.0.title",  # Try title as fallback
                        output_filename="gemini_latest_news_title",
                        lang="en"
                    )
                    
                    if title_audio:
                        print(f"Pipeline generated news audio using title: {title_audio}")
                    else:
                        print("Pipeline failed to generate news audio. Check the log for details.")
            else:
                print("No news items found in the API response")
        else:
            print("Failed to fetch data from API")
            
    except Exception as e:
        print(f"Error processing news: {e}")

if __name__ == "__main__":
    main()
