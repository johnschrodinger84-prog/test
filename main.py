from flask import Flask, jsonify, render_template, request
from config import Config
import importlib
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Configure Gemini API
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
    else:
        print("Warning: GEMINI_API_KEY environment variable not set.")

    # Import core blueprint (has actual routes)
    from apps.core.main import bp as core_bp
    
    # Register core blueprint
    app.register_blueprint(core_bp, url_prefix='/core')

    # App name to module mapping for Universal Prompting Engine
    APP_NAME_TO_MODULE = {
        "diet-tracker": "DietTracker",
        "one-click-trip": "OneClickTrip",
        "matter_of_choice": "MatterOfChoice",
        "style-translator": "StyleTranslator",
        "school-killer": "SchoolKiller",
        "calories": "Calories",
    }

    # Universal Prompting Engine endpoints
    @app.route('/api/direct', methods=['POST'])
    def direct_tunnel():
        """Provides raw, unstructured access to the Gemini API for general-purpose queries."""
        data = request.get_json()
        if not data or "parts" not in data:
            return jsonify({"error": "Invalid request body. 'parts' is required."}), 400

        model_name = data.get("model_name", "gemini-2.5-pro")
        model = genai.GenerativeModel(model_name)
        
        try:
            response = model.generate_content(data["parts"])
            return jsonify({"response": response.text})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/api/prompt', methods=['POST'])
    def universal_prompting_engine():
        """Provides structured, application-aware access to the Gemini API by using predefined prompt templates."""
        data = request.get_json()
        if not data or "app_name" not in data or "data" not in data:
            return jsonify({"error": "Invalid request body. 'app_name' and 'data' are required."}), 400

        app_name = data["app_name"]
        app_data = data["data"]

        module_name = APP_NAME_TO_MODULE.get(app_name)
        if not module_name:
            return jsonify({"error": f"Unknown app_name: {app_name}"}), 400

        try:
            app_module = importlib.import_module(f'apps.{module_name}.main')
            response_data = app_module.handle_prompt(app_data)
            return jsonify(response_data)

        except ImportError:
            return jsonify({"error": f'Application "{app_name}" not found'}), 404
        except AttributeError:
            return jsonify({"error": f'Application "{app_name}" does not have a handle_prompt function'}), 500
        except Exception as e:
            return jsonify({"error": f'Error processing prompt for "{app_name}": {str(e)}'}), 500

    # Root route - landing page
    @app.route('/')
    def index():
        return render_template('index.html')

    # Handle all other routes
    @app.route('/<path:path>')
    def catch_all(path):
        # Check if the request is an API request
        if request.headers.get('Accept') == 'application/json' or \
           request.headers.get('Content-Type') == 'application/json' or \
           path.startswith(('oneclicktrip/', 'calories/', 'schoolkiller/', 'styletranslator/', 'core/')):
            return jsonify({'error': 'Not found'}), 404
        # For browser requests, redirect to home page
        return render_template('index.html')

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        # Check if the request is an API request
        if request.headers.get('Accept') == 'application/json' or \
           request.headers.get('Content-Type') == 'application/json':
            return jsonify({'error': 'Not found'}), 404
        # For browser requests, redirect to home page
        return render_template('index.html')

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000) 