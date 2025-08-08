"""
DietTracker main module.
Contains the main application logic for the Universal Prompting Engine.
"""

from apps.core.gemini_service import GeminiService

def handle_prompt(data):
    """Handles the prompt for the DietTracker application."""
    gemini_service = GeminiService()

    prompt = f"Provide a detailed nutritional analysis for the following food item: {data.get('food_item')}. Include calories, protein, carbohydrates, and fat."
    
    response = gemini_service.generate_content({
        "parts": [{"text": prompt}]
    })

    return {"response": response}