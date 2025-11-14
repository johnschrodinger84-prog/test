"""
StyleTranslator main module.
Contains the main application logic for the Universal Prompting Engine.
"""

from flask import Blueprint, request, jsonify
from apps.core.prompt_service import PromptService

bp = Blueprint('styletranslator', __name__, url_prefix='/styletranslator')
prompt_service = PromptService()

def handle_prompt(data):
    """Handles the prompt for the StyleTranslator application."""

    required_params = {
        'user_task': str,
        'selected_solution_language': str
    }

    for param, param_type in required_params.items():
        if param not in data or not isinstance(data[param], param_type):
            return {'error': f'Missing or invalid required parameter: {param}'}

    # Handle optional base parameters
    edited_recognized_text = data.get('edited_recognized_text')
    is_image_used = data.get('is_image_used', False) # Default to False if not provided

    # Extract style-specific parameters
    style_params = {}
    for param_name in ['tone_preference', 'style', 'mentality', 'translation_scale',
                       'transformation_level', 'category', 'source_gender', 'target_gender',
                       'source_age', 'target_age']:
        if param_name in data:
            style_params[param_name] = data[param_name]

    prompt = prompt_service.build_prompt(
        app_name='style-translator', # Use hyphenated name
        base_params={
            'user_task': data['user_task'],
            'is_image_used': is_image_used,
            'selected_solution_language': data['selected_solution_language'],
            'edited_recognized_text': edited_recognized_text
        },
        app_specific_params=style_params
    )

    from apps.core.gemini_service import GeminiService # Import GeminiService
    gemini_service = GeminiService(model_name='gemini-1.5-flash-latest') # Instantiate GeminiService
    response = gemini_service.generate_response([None, prompt]) # Generate response

    return {"response": response}
