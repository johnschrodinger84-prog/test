import os
import logging
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)

# Model cache for reuse
model_cache = {}

def get_model(model_name):
    """Get cached GenerativeModel instance or create a new one."""
    if model_name not in model_cache:
        model_cache[model_name] = genai.GenerativeModel(model_name)
    return model_cache[model_name]

class GeminiAPIKeyMissingError(Exception):
    """Raised when GEMINI_API_KEY is not configured."""
    pass

class GeminiService:
    def __init__(self, model_name):
        try:
            logger.debug(f"Initializing GeminiService with model: {model_name}")
            self.api_key = os.getenv("GEMINI_API_KEY")
            logger.debug(f"API Key: {self.api_key}")
            if not self.api_key:
                logger.error("GEMINI_API_KEY is not set")
                raise GeminiAPIKeyMissingError("GEMINI_API_KEY is not set")

            logger.debug("Configuring Gemini API")
            genai.configure(api_key=self.api_key)
            self.model = get_model(model_name)
            logger.debug("GeminiService initialized successfully")

        except GeminiAPIKeyMissingError:
            raise
        except Exception as e:
            logger.error(f"Failed to initialize AI services: {str(e)}", exc_info=True)
            raise RuntimeError(f"Failed to initialize AI services: {str(e)}")

    def generate_response(self, prompt_data):
        """Generate a response using the Gemini model."""
        try:
            logger.debug("Generating response with Gemini")
            logger.debug(f"Prompt data type: {type(prompt_data)}")
            
            # Validate input
            if not isinstance(prompt_data, list) or len(prompt_data) != 2:
                logger.error("Invalid prompt data format")
                return None

            image, prompt = prompt_data
            if image and not isinstance(image, Image.Image):
                logger.error("Invalid image format")
                return None

            logger.debug("Generating content with image and prompt")
            # Generate content
            if image:
                response = self.model.generate_content([image, prompt])
            else:
                response = self.model.generate_content([prompt])
            logger.debug(f"Received response from Gemini: {response}")
            
            if response and hasattr(response, 'text'):
                logger.debug("Successfully extracted text from response")
                return response.text
            else:
                logger.error("Invalid response format from Gemini")
                return None

        except Exception as e:
            logger.error(f"Failed to generate response: {str(e)}", exc_info=True)
            return None