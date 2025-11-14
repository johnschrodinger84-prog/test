"""
SchoolKiller main module.
Contains the main application logic for the Universal Prompting Engine.
"""

from flask import Blueprint, request, jsonify
from apps.core.prompt_service import PromptService
from apps.core.gemini_service import GeminiService

bp = Blueprint('schoolkiller', __name__, url_prefix='/schoolkiller')
prompt_service = PromptService()

def handle_prompt(data):
    """Handles the prompt for the SchoolKiller application."""

    required_params = {
        'user_task': str,
        'is_image_used': bool,
        'selected_solution_language': str,
        'subject': str,
        'problem_description': str
    }

    for param, param_type in required_params.items():
        if param not in data or not isinstance(data[param], param_type):
            return {'error': f'Missing or invalid required parameter: {param}'}

    # Handle optional edited_recognized_text separately
    edited_recognized_text = data.get('edited_recognized_text')

    prompt = prompt_service.build_prompt(
        app_name='school-killer',
        base_params={
            'user_task': data['user_task'],
            'is_image_used': data['is_image_used'],
            'selected_solution_language': data['selected_solution_language'],
            'edited_recognized_text': data.get('edited_recognized_text')
        },
        app_specific_params={
            'subject': data['subject'],
            'problem_description': data['problem_description']
        }
    )

    gemini_service = GeminiService(model_name='gemini-1.5-flash-latest')
    response = gemini_service.generate_response([None, prompt])

    return {"response": response}