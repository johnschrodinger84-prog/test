"""
OneClickTrip main module.
Contains the main application logic for the Universal Prompting Engine.
"""

from apps.core.gemini_service import GeminiService

def handle_prompt(data):
    """Handles the prompt for the OneClickTrip application."""
    gemini_service = GeminiService()

    prompt = f"Create a detailed travel itinerary for a trip from {data.get('origin')} with stops in {', '.join(data.get('city_paths', []))}. The budget is ${data.get('max_budget')} for {data.get('travelers_number')} people. Include suggestions for flights, accommodations, and activities."
    
    response = gemini_service.generate_content({
        "parts": [{"text": prompt}]
    })

    return {"response": response}