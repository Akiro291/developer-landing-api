import logging
from typing import Optional
import os
import re
import json

logger = logging.getLogger(__name__)

def analyze_comment_with_gemini(text: str) -> Optional[dict]:
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        logger.warning("GEMINI_API_KEY not found in environment")
        return None
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        prompt = f"""Analyze customer comment and return JSON:
- category: main topic (1-2 words)
- sentiment: "positive", "negative", "neutral"
- response: automated reply in Russian

Comment: {text}

Return ONLY valid JSON."""

        response = model.generate_content(prompt)
        
        json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        
        return None
        
    except ImportError:
        logger.error("google-generativeai package not installed")
        return None
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        return None
