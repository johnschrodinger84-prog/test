"""
DietTracker main module.
Contains the main application logic for the Universal Prompting Engine.
"""

from apps.core.prompt_service import PromptService
from apps.core.gemini_service import GeminiService

prompt_service = PromptService()

def handle_prompt(data):
    """Handles the prompt for the DietTracker application."""

    required_params = {
        'user_task': str,
        'is_image_used': bool,
        'selected_solution_language': str,
        'physical_activity': str,
        'gender': str,
        'age': int,
        'height': float,
        'weight': float
    }

    for param, param_type in required_params.items():
        if param not in data or not isinstance(data[param], param_type):
            return {'error': f'Missing or invalid required parameter: {param}'}

    # Handle optional edited_recognized_text separately
    edited_recognized_text = data.get('edited_recognized_text')

    # Extract diet-specific parameters
    diet_params = {
        'physical_activity': data['physical_activity'],
        'gender': data['gender'],
        'age': data['age'],
        'height': data['height'],
        'weight': data['weight']
    }

    prompt = prompt_service.build_prompt(
        app_name='diet_tracker',
        base_params={
            'user_task': data['user_task'],
            'is_image_used': data['is_image_used'],
            'selected_solution_language': data['selected_solution_language'],
            'edited_recognized_text': edited_recognized_text
        },
        app_specific_params=diet_params
    )

    gemini_service = GeminiService(model_name='gemini-1.5-flash-latest')
    response = gemini_service.generate_response([None, prompt])

    return {"response": response}
