"""
Calories main module.
Contains the main application routes and prompt building functionality.
"""

from flask import Blueprint, request, jsonify
from apps.core.prompt_service import PromptService

# Create blueprint with consistent name
bp = Blueprint('calories', __name__)

# Initialize prompt service
prompt_service = PromptService()

@bp.route('/')
def index():
    """Welcome endpoint for Calories API."""
    return jsonify({
        'message': 'Welcome to Calories API',
        'status': 'active',
        'endpoints': {
            'build_prompt': {
                'method': 'PUT',
                'path': '/build_prompt',
                'description': 'Builds a prompt for calorie tracking and nutrition',
                'parameters': {
                    'required_base': [
                        'user_task (string)',
                        'is_image_used (boolean)',
                        'selected_solution_language (string)',
                        'edited_recognized_text (string, optional)'
                    ]
                }
            }
        }
    })

@bp.route('/build_prompt', methods=['PUT'])
def build_prompt():
    """Builds a prompt for calorie tracking and nutrition based on user parameters."""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Required parameters
        required_params = {
            'user_task': str,
            'is_image_used': bool,
            'selected_solution_language': str,
            'edited_recognized_text': str  # Optional base parameter
        }

        # Validate required parameters
        for param, param_type in required_params.items():
            if param not in data or not isinstance(data[param], param_type):
                if param == 'edited_recognized_text' and param not in data:
                    continue  # Skip validation for optional parameter
                return jsonify({'error': f'Missing or invalid required parameter: {param}'}), 400

        # Build the prompt using the shared service
        prompt = prompt_service.build_prompt(
            app_name='calorie_tracker',
            base_params={
                'user_task': data['user_task'],
                'is_image_used': data['is_image_used'],
                'selected_solution_language': data['selected_solution_language'],
                'edited_recognized_text': data.get('edited_recognized_text')
            },
            app_specific_params={}  # Calories app doesn't have specific parameters
        )

        return jsonify({'prompt': prompt}), 200

    except Exception as e:
        return jsonify({'error': f'Failed to build prompt: {str(e)}'}), 500 