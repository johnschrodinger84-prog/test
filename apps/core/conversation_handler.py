from .gemini_service import GeminiService, GeminiAPIKeyMissingError

class ConversationHandler:
    def __init__(self):
        self.model_cache = {}

    def get_model(self, model_name):
        """Get or create a GeminiService instance for the specified model."""
        if model_name not in self.model_cache:
            self.model_cache[model_name] = GeminiService(model_name)
        return self.model_cache[model_name]

    def process_conversation(self, image_urls=None, file_paths=None, text=None, model_name='gemini-pro-vision'):
        """
        Process a conversation request with Gemini AI.
        
        Args:
            image_urls (list): List of image URLs to process
            file_paths (list): List of local file paths to process
            text (str): Text prompt to include
            model_name (str): Name of the Gemini model to use
            
        Returns:
            tuple: (response_text, error_message)
        """
        try:
            gemini_service = self.get_model(model_name)
            prompt_data = []
            uploaded_files = []

            # Process local files
            if file_paths:
                for path in file_paths:
                    uploaded = gemini_service.upload_image(path)
                    if uploaded:
                        uploaded_files.append(uploaded)
                    else:
                        return None, f"Failed to upload file: {path}"

            # Process remote URLs
            elif image_urls:
                for url in image_urls:
                    uploaded = gemini_service.upload_image(url)
                    if uploaded:
                        uploaded_files.append(uploaded)
                    else:
                        return None, f"Failed to upload image from URL: {url}"

            # Add uploaded images to prompt
            prompt_data.extend(uploaded_files)

            # Add text if provided
            if text:
                prompt_data.append("\n\n")
                prompt_data.append(text)

            # Generate response
            response = gemini_service.generate_response(prompt_data)
            return response, None

        except GeminiAPIKeyMissingError:
            # Re-raise to allow route-level handling
            raise
        except Exception as e:
            return None, f"Gemini API request failed: {str(e)}" 