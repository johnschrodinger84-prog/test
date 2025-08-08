"""
Core application main module.
Contains the main application setup and routes.
"""

import logging
import os
import io
from flask import Blueprint, request, jsonify, current_app
from .file_handler import FileHandler
from .conversation_handler import ConversationHandler
from .solution_handler import SolutionHandler
from PIL import Image

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize handlers
file_handler = FileHandler()
conversation_handler = ConversationHandler()
solution_handler = SolutionHandler()

# Create blueprint
bp = Blueprint('core', __name__, url_prefix='/core')

# Initialize file handler with app when blueprint is registered
@bp.record_once
def setup_file_handler(state):
    file_handler.init_app(state.app)

@bp.route('/upload', methods=['POST'])
@bp.route('/upload/', methods=['POST'])  # Add route with trailing slash
def upload_file():
    """Handles file uploads and returns both the file path and public URL."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        app_name = request.form.get('app_name', 'core')  # Default to 'core' if not specified
        
        file_path, file_url = file_handler.process_uploaded_file(file, app_name)
        return jsonify({'file_path': file_path, 'url': file_url}), 201

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@bp.route('/converse', methods=['POST'])
def converse():
    """Handles conversation requests with Gemini AI."""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Extract request data
        image_urls = data.get('image_urls', [])
        file_paths = data.get('file_paths', [])
        text = data.get('text', '')
        model_name = data.get('model_name', 'gemini-pro-vision')

        # Process conversation
        response, error = conversation_handler.process_conversation(
            image_urls=image_urls,
            file_paths=file_paths,
            text=text,
            model_name=model_name
        )

        if error:
            return jsonify({'error': error}), 500

        return jsonify({'response': response}), 200

    except Exception as e:
        return jsonify({'error': f'Request failed: {str(e)}'}), 500

@bp.route('/generate_solutions', methods=['POST'])
def generate_solutions():
    """
    Generate solutions based on prompt and images.
    
    Form data:
    - prompt: The prompt to use for generation
    - image_files: List of image files (multipart/form-data)
    
    Returns:
    - 200: List of solutions with recognized text
    - 400: Invalid request
    - 500: Server error
    """
    try:
        logger.debug("Received generate_solutions request")
        logger.debug(f"Request files: {request.files}")
        logger.debug(f"Request form: {request.form}")

        # Get prompt from form data
        prompt = request.form.get('prompt')
        if not prompt:
            logger.error("No prompt provided in request")
            return jsonify({'error': 'No prompt provided'}), 400

        # Get image files from form data
        image_files = request.files.getlist('image_files')
        if not image_files:
            logger.error("No image files provided in request")
            return jsonify({'error': 'No image files provided'}), 400

        logger.debug(f"Processing request with prompt: {prompt}")
        logger.debug(f"Number of image files: {len(image_files)}")
        
        # Process images directly from the request
        processed_images = []
        for file in image_files:
            if file and file.filename:
                try:
                    logger.debug(f"Processing file: {file.filename}")
                    # Read the file into memory
                    image_data = file.read()
                    # Create a PIL Image from the file data
                    image = Image.open(io.BytesIO(image_data))
                    processed_images.append(image)
                    logger.debug(f"Successfully processed image: {file.filename}")
                except Exception as e:
                    logger.error(f"Failed to process image {file.filename}: {str(e)}", exc_info=True)
                    continue

        if not processed_images:
            logger.error("No images were successfully processed")
            return jsonify({'error': 'Failed to process any images'}), 500

        # Process the request with the PIL images
        solutions, error = solution_handler.process_solution_request(
            prompt=prompt,
            images=processed_images  # Pass PIL images directly
        )

        # If we have an error but also some solutions, include both
        if error and solutions:
            logger.warning(f"Partial success with warning: {error}")
            return jsonify({
                'solutions': solutions,
                'warning': error
            }), 200

        # If we have only an error, return it
        if error:
            logger.error(f"Request failed with error: {error}")
            return jsonify({'error': error}), 500

        # Return successful solutions
        logger.info("Request completed successfully")
        return jsonify({'solutions': solutions}), 200

    except Exception as e:
        logger.error(f"Request failed with exception: {str(e)}", exc_info=True)
        return jsonify({'error': f'Request failed: {str(e)}'}), 500

@bp.route('/health')
def health_check():
    """Health check endpoint for the core application."""
    return jsonify({"status": "healthy", "service": "core"}) 