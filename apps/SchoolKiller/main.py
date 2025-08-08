"""
SchoolKiller main module.
Contains the main application logic for the Universal Prompting Engine.
"""

from apps.core.gemini_service import GeminiService

def handle_prompt(data):
    """Handles the prompt for the SchoolKiller application."""
    gemini_service = GeminiService()

    prompt = f"Solve the following {data.get('subject')} problem: {data.get('problem_description')}. Show the steps and the final answer."
    
    response = gemini_service.generate_content({
        "parts": [{"text": prompt}]
    })

    return {"response": response}