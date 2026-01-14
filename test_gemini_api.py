#!/usr/bin/env python3
"""
A simple test script to verify if the Gemini API key is valid.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    """Check if the Gemini API key is valid and usable."""
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    
    if not gemini_api_key:
        print("Error: GEMINI_API_KEY environment variable not found.")
        print("Please add your Gemini API key to the .env file.")
        return False
    
    print(f"Found Gemini API key: {gemini_api_key[:10]}...")
    
    # Try to import and configure Google GenerativeAI
    try:
        import google.generativeai as genai
        genai.configure(api_key=gemini_api_key)
        
        # Try a simple API call to verify the key
        print("Testing API key with a simple request...")
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content("Hello, World!")
        
        print("API test successful! Response:")
        print(response.text)
        return True
        
    except ImportError:
        print("Error: google-generativeai package not installed.")
        print("Please install it with: pip install google-generativeai")
        return False
        
    except Exception as e:
        print(f"Error: The Gemini API key appears to be invalid.")
        print(f"Error details: {e}")
        print("\nPlease follow these steps to get a valid API key:")
        print("1. Go to https://ai.google.dev/ and sign in")
        print("2. Click on 'Get API key' in the top navigation")
        print("3. Create a new API key or use an existing one")
        print("4. Update your .env file with the new key")
        return False

if __name__ == "__main__":
    print("==== Gemini API Key Validation ====")
    success = main()
    sys.exit(0 if success else 1)
