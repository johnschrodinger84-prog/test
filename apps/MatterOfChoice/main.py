"""
MatterOfChoice main module.
Contains the main application logic for the Universal Prompting Engine.
"""

from apps.core.prompt_service import PromptService
from apps.core.gemini_service import GeminiService

def handle_prompt(data, prompt_service=None, gemini_service=None):
    """Handles the prompt for the MatterOfChoice application."""

    if prompt_service is None:
        prompt_service = PromptService()

    if gemini_service is None:
        gemini_service = GeminiService(model_name='gemini-flash-latest')

    required_params = {
        'user_task': str,
        'is_image_used': bool,
        'selected_solution_language': str,
        'edited_recognized_text': str,  # Optional base parameter
        'role': str,
        'cases': list
    }

    for param, param_type in required_params.items():
        if param not in data or not isinstance(data[param], param_type):
            if param == 'edited_recognized_text' and param not in data:
                continue
            return {'error': f'Missing or invalid required parameter: {param}'}

    prompt = prompt_service.build_prompt(
        app_name='matter_of_choice',
        base_params={
            'user_task': data['user_task'],
            'is_image_used': data['is_image_used'],
            'selected_solution_language': data['selected_solution_language'],
            'edited_recognized_text': data.get('edited_recognized_text')
        },
        app_specific_params={
            'role': data['role'],
            'cases': data['cases']
        }
    )

    response = gemini_service.generate_response([None, prompt])

    return {"response": response}

# Added a comment to force recompile