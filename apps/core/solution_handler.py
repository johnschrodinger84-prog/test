import logging
from typing import List, Dict, Tuple, Optional
from PIL import Image
from flask import current_app
from .gemini_service import GeminiService, GeminiAPIKeyMissingError

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class SolutionHandler:
    def __init__(self):
        self.max_retries = 3
        self.model_name = 'gemini-1.5-flash'  # Updated to use the newer model

    def process_solution_request(self, prompt: str, images: List[Image.Image]) -> Tuple[List[Dict[str, str]], Optional[str]]:
        """
        Process a solution generation request.
        
        Args:
            prompt: The prompt to use for generation
            images: List of PIL Image objects
            
        Returns:
            Tuple containing:
            - List of solutions with recognized text
            - Error message if any, None if successful
        """
        try:
            logger.debug(f"Processing solution request with prompt: {prompt}")
            logger.debug(f"Number of images to process: {len(images)}")

            # Initialize Gemini service with updated model
            logger.debug(f"Initializing Gemini service with model: {self.model_name}")
            gemini_service = GeminiService(self.model_name)
            solutions = []
            failed_images = []

            # Process each image
            for idx, image in enumerate(images):
                logger.debug(f"Processing image {idx + 1}")
                try:
                    # Try to generate solution with retries
                    solution = None
                    for attempt in range(self.max_retries):
                        try:
                            logger.debug(f"Attempt {attempt + 1} of {self.max_retries} to generate solution")
                            # Generate solution using the prompt and image
                            response = gemini_service.generate_response([image, prompt])
                            if response:
                                solution = response
                                logger.debug("Solution generated successfully")
                                break
                        except Exception as e:
                            logger.error(f"Attempt {attempt + 1} failed: {str(e)}", exc_info=True)
                            if attempt == self.max_retries - 1:
                                return [], f"AI generation failed after {self.max_retries} attempts: {str(e)}"
                            continue

                    if solution:
                        logger.debug("Adding solution to results")
                        solutions.append({
                            "solution": solution,
                            "recognized_text": ""
                        })
                    else:
                        logger.error(f"Failed to generate solution for image {idx + 1}")
                        failed_images.append(f"image_{idx + 1}")

                except Exception as e:
                    logger.error(f"Error processing image {idx + 1}: {str(e)}", exc_info=True)
                    failed_images.append(f"image_{idx + 1}")
                    continue

            # If we have any solutions, return them with failed images info
            if solutions:
                if failed_images:
                    logger.warning(f"Some images failed to process: {failed_images}")
                    return solutions, f"Some images failed to process: {', '.join(failed_images)}"
                logger.info("All images processed successfully")
                return solutions, None
            
            # If no solutions were generated
            if failed_images:
                logger.error(f"All images failed to process: {failed_images}")
                return [], f"All images failed to process: {', '.join(failed_images)}"
            logger.error("No solutions could be generated")
            return [], "No solutions could be generated"

        except GeminiAPIKeyMissingError:
            # Re-raise to allow route-level handling
            raise
        except Exception as e:
            logger.error(f"Solution generation failed: {str(e)}", exc_info=True)
            return [], f"Solution generation failed: {str(e)}" 