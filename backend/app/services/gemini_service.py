"""
Gemini Service for DHARTI-X
Manages Google Gemini API interactions with graceful fallback when GEMINI_API_KEY is not configured or quota is exceeded.
"""

import os
from typing import Optional, Dict, Any, List

class GeminiService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client = None
        self.is_configured = False

        if self.api_key and self.api_key != "your_gemini_api_key_here":
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self.client = genai.GenerativeModel("gemini-1.5-flash")
                self.is_configured = True
            except Exception as e:
                self.is_configured = False
                self.client = None

    def generate_response(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """
        Generates reasoning text via Gemini or returns a structured fallback response.
        """
        if not self.is_configured or not self.client:
            return {
                "text": None,
                "is_fallback": True,
                "reason": "GEMINI_API_KEY not configured or client initialization failed."
            }
        
        try:
            full_prompt = f"{system_prompt}\n\nUser Question: {user_prompt}"
            response = self.client.generate_content(full_prompt)
            return {
                "text": response.text.strip(),
                "is_fallback": False,
                "reason": "Success"
            }
        except Exception as e:
            return {
                "text": None,
                "is_fallback": True,
                "reason": f"Gemini API invocation error: {str(e)}"
            }

