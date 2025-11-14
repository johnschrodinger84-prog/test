from flask import Flask, request, jsonify
import os
import google.generativeai as genai
import importlib
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("Warning: GEMINI_API_KEY environment variable not set.")

APP_NAME_TO_MODULE = {
    "diet-tracker": "DietTracker",
    "one-click-trip": "OneClickTrip",
    "matter_of_choice": "MatterOfChoice",
    "style-translator": "StyleTranslator",
    "school-killer": "SchoolKiller",
}

@app.route('/api/direct', methods=['POST'])
def direct_tunnel():
    """
    Provides raw, unstructured access to the Gemini API for general-purpose queries.
    """
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
    """
    Provides structured, application-aware access to the Gemini API 
    by using predefined prompt templates.
    """
    data = request.get_json()
    if not data or "app_name" not in data or "data" not in data:
        return jsonify({"error": "Invalid request body. 'app_name' and 'data' are required."}), 400

    app_name = data["app_name"]
    print(app_name)
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)