"""
Shared prompt service for building prompts across different applications.
"""

from typing import Dict, Any, Optional
import hashlib
import json

class PromptService:
    def __init__(self):
        """Initialize the prompt service with an empty cache."""
        self._prompt_cache: Dict[str, str] = {}
        
        # App-specific prompt templates
        self.prompt_templates = {
            'school_killer': self._build_school_killer_prompt,
            'style_translator': self._build_style_translator_prompt,
            'diet_tracker': self._build_diet_tracker_prompt,
            'one_click_trip': self._build_one_click_trip_prompt,
            'calorie_tracker': self._build_calories_prompt
        }

    def _generate_cache_key(self, app_name: str, base_params: Dict[str, Any], app_specific_params: Dict[str, Any]) -> str:
        """Generate a unique cache key for the given parameters."""
        # Create a dictionary with all parameters
        params_dict = {
            'app_name': app_name,
            'base_params': base_params,
            'app_specific_params': app_specific_params
        }
        # Convert to JSON string and hash it
        params_json = json.dumps(params_dict, sort_keys=True)
        return hashlib.md5(params_json.encode()).hexdigest()

    def build_prompt(self, app_name: str, base_params: Dict[str, Any], app_specific_params: Dict[str, Any]) -> str:
        """
        Builds a prompt based on the app name and parameters.
        Uses caching to avoid rebuilding the same prompt multiple times.
        
        Args:
            app_name: Name of the application
            base_params: Base parameters common to all apps
            app_specific_params: Parameters specific to the app
            
        Returns:
            The built prompt string
        """
        # Generate cache key
        cache_key = self._generate_cache_key(app_name, base_params, app_specific_params)
        
        # Check if prompt is in cache
        if cache_key in self._prompt_cache:
            return self._prompt_cache[cache_key]
        
        # Get the appropriate prompt builder
        prompt_builder = self.prompt_templates.get(app_name)
        if not prompt_builder:
            raise ValueError(f"Unknown app: {app_name}")
        
        # Build the prompt
        prompt = prompt_builder(base_params, app_specific_params)
        
        # Cache the prompt
        self._prompt_cache[cache_key] = prompt
        
        return prompt

    def _build_school_killer_prompt(self, base_params, app_params):
        """Builds a prompt for SchoolKiller app."""
        prompt = f"Task: {base_params['user_task']}\n"
        prompt += f"Language: {base_params['selected_solution_language']}\n"
        
        if base_params.get('edited_recognized_text'):
            prompt += f"Context: {base_params['edited_recognized_text']}\n"
            
        if app_params.get('details_level'):
            prompt += f"Detail Level: {app_params['details_level']}\n"
        if app_params.get('grade'):
            prompt += f"Grade Level: {app_params['grade']}\n"
            
        return prompt

    def _build_style_translator_prompt(self, base_params, app_params):
        """Builds a prompt for StyleTranslator app."""
        prompt = f"Task: {base_params['user_task']}\n"
        prompt += f"Language: {base_params['selected_solution_language']}\n"
        
        if base_params.get('edited_recognized_text'):
            prompt += f"Text to Transform: {base_params['edited_recognized_text']}\n"
            
        # Add style-specific parameters
        style_params = [
            'tone_preference', 'style', 'mentality', 'translation_scale',
            'transformation_level', 'category', 'source_gender', 'target_gender',
            'source_age', 'target_age'
        ]
        
        for param in style_params:
            if app_params.get(param):
                prompt += f"{param.replace('_', ' ').title()}: {app_params[param]}\n"
                
        return prompt

    def _build_diet_tracker_prompt(self, base_params, app_params):
        """Builds a prompt for DietTracker app."""
        prompt = f"Task: {base_params['user_task']}\n"
        prompt += f"Language: {base_params['selected_solution_language']}\n"
        
        if base_params.get('edited_recognized_text'):
            prompt += f"Additional Context: {base_params['edited_recognized_text']}\n"
            
        # Add diet-specific parameters
        diet_params = ['physical_activity', 'gender', 'age', 'height', 'weight']
        for param in diet_params:
            if app_params.get(param):
                prompt += f"{param.replace('_', ' ').title()}: {app_params[param]}\n"
                
        return prompt

    def _build_one_click_trip_prompt(self, base_params, app_params):
        """Builds a prompt for OneClickTrip app."""
        prompt = f"Task: {base_params['user_task']}\n"
        prompt += f"Language: {base_params['selected_solution_language']}\n"
        
        if base_params.get('edited_recognized_text'):
            prompt += f"Additional Requirements: {base_params['edited_recognized_text']}\n"
            
        # Add trip-specific parameters
        if app_params.get('origin_location'):
            prompt += f"Origin: {app_params['origin_location']}\n"
        if app_params.get('is_one_way') is not None:
            prompt += f"Trip Type: {'One Way' if app_params['is_one_way'] else 'Round Trip'}\n"
        if app_params.get('city_paths'):
            prompt += f"Cities: {', '.join(app_params['city_paths'])}\n"
        if app_params.get('transportation_types'):
            prompt += f"Transportation: {', '.join(app_params['transportation_types'])}\n"
        if app_params.get('trip_styles'):
            prompt += f"Trip Styles: {', '.join(app_params['trip_styles'])}\n"
        if app_params.get('max_budget'):
            prompt += f"Budget: {app_params['max_budget']}\n"
        if app_params.get('trip_duration'):
            prompt += f"Duration: {app_params['trip_duration']} days\n"
        if app_params.get('travelers_number'):
            prompt += f"Travelers: {app_params['travelers_number']}\n"
            
        return prompt

    def _build_calories_prompt(self, base_params, app_params):
        """Builds a prompt for CalorieTracker app."""
        prompt = f"Task: {base_params['user_task']}\n"
        prompt += f"Language: {base_params['selected_solution_language']}\n"
        
        if base_params.get('edited_recognized_text'):
            prompt += f"Food Description: {base_params['edited_recognized_text']}\n"
            
        if base_params.get('is_image_used'):
            prompt += "Note: Image analysis will be performed for food recognition\n"
            
        return prompt 