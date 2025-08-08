"""
StyleTranslator main module.
Contains the main application logic for the Universal Prompting Engine.
"""

from apps.core.gemini_service import GeminiService

def handle_prompt(data):
    """Handles the prompt for the StyleTranslator application."""
    gemini_service = GeminiService()

    prompt = f"Translate the following text to a '{data.get('target_style')}' style: '{data.get('source_text')}'"
    
    response = gemini_service.generate_content({
        "parts": [{"text": prompt}]
    })

    return {
        "response": {
            "translated_text": response,
            "style_detected": "unknown",
            "style_applied": data.get('target_style')
        }
    }