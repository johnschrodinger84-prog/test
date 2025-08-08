"""
MatterOfChoice main module.
Contains the main application logic for the Universal Prompting Engine.
"""

from apps.core.gemini_service import GeminiService

def handle_prompt(data):
    """Handles the prompt for the MatterOfChoice application."""
    gemini_service = GeminiService()

    case = data.get('cases', [{}])[0]
    prompt = f"As a {data.get('role')}, analyze the following answer to the question: '{case.get('question')}'. The user's answer is: '{case.get('user_answer')}'. Provide feedback and a score from 1 to 10."
    
    response = gemini_service.generate_content({
        "parts": [{"text": prompt}]
    })

    return {"response": response}
