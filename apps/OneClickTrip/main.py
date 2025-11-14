"""
OneClickTrip main module.
Contains the main application logic for the Universal Prompting Engine.
"""

from apps.core.prompt_service import PromptService
from apps.core.gemini_service import GeminiService

prompt_service = PromptService()

def handle_prompt(data):
    """Handles the prompt for the OneClickTrip application."""

    required_params = {
        'user_task': str,
        'is_image_used': bool,
        'selected_solution_language': str,
        'origin_location': str,
        'city_paths': list,
        'transportation_types': list,
        'trip_styles': list,
        'max_budget': int,
        'trip_duration': int,
        'travelers_number': int
    }

    for param, param_type in required_params.items():
        if param not in data or not isinstance(data[param], param_type):
            return {'error': f'Missing or invalid required parameter: {param}'}

    # Handle optional edited_recognized_text separately
    edited_recognized_text = data.get('edited_recognized_text')
    is_one_way = data.get('is_one_way') # Optional boolean

    # Extract trip-specific parameters
    trip_params = {
        'origin_location': data['origin_location'],
        'is_one_way': is_one_way,
        'city_paths': data['city_paths'],
        'transportation_types': data['transportation_types'],
        'trip_styles': data['trip_styles'],
        'max_budget': data['max_budget'],
        'trip_duration': data['trip_duration'],
        'travelers_number': data['travelers_number']
    }

    prompt = prompt_service.build_prompt(
        app_name='one_click_trip',
        base_params={
            'user_task': data['user_task'],
            'is_image_used': data['is_image_used'],
            'selected_solution_language': data['selected_solution_language'],
            'edited_recognized_text': edited_recognized_text
        },
        app_specific_params=trip_params
    )

    gemini_service = GeminiService(model_name='gemini-1.5-flash-latest')
    response = gemini_service.generate_response([None, prompt])

    return {"response": response}