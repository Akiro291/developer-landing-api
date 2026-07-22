import logging
from typing import Optional
import os
import json
import re
from app.core.config import settings

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.model_name = "llama-3.1-8b-instant"
        self.is_configured = bool(self.api_key)
        
        if not self.is_configured:
            logger.warning("Groq API key not configured in .env file")
        
        self._initialize_groq()

    def _initialize_groq(self):
        if not self.is_configured:
            self.model = None
            return

        try:
            from groq import Groq
            self.client = Groq(api_key=self.api_key)
            logger.info("Groq API initialized successfully")
        except ImportError:
            logger.error("groq package not installed")
            self.model = None
        except Exception as e:
            logger.error(f"Failed to initialize Groq: {e}")
            self.model = None

    async def analyze_comment(self, text: str) -> dict:
        if not self.is_configured or not self.client:
            return self._get_fallback_response()

        if not text or not text.strip():
            return self._get_fallback_response()

        try:
            prompt = self._build_analysis_prompt(text)
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "Return only JSON with category, sentiment, response"},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            return self._parse_ai_response(content)
            
        except Exception as e:
            logger.error(f"Groq API error: {e}")
            return self._get_fallback_response()

    def _build_analysis_prompt(self, text: str) -> str:
        return f"""Analyze this customer comment and return JSON with:
1. category: main topic category (1-2 words)
2. sentiment: "positive", "negative", or "neutral"
3. response: professional automated reply in Russian

Return ONLY valid JSON, no other text.

Comment: {text}"""

    def _parse_ai_response(self, text: str) -> dict:
        try:
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                return {
                    "category": data.get("category", "unknown"),
                    "sentiment": data.get("sentiment", "neutral"),
                    "response": data.get("response", "Thank you for your message.")
                }
            return self._get_fallback_response()
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            return self._get_fallback_response()

    def _get_fallback_response(self) -> dict:
        return {
            "category": "unknown",
            "sentiment": "neutral",
            "response": "Спасибо за ваше обращение. Мы его получили и рассмотрим."
        }

ai_service = AIService()
