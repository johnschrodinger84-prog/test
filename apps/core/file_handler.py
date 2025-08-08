import os
import uuid
import shutil
from flask import current_app
from werkzeug.utils import secure_filename

class FileHandler:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initialize the file handler with the Flask app."""
        # Set up upload folder in the user's home directory
        home_dir = os.path.expanduser('~')
        self.upload_folder = os.path.join(home_dir, 'uploads')
        app.config['UPLOAD_FOLDER'] = self.upload_folder
        os.makedirs(self.upload_folder, exist_ok=True)

    def get_app_upload_folder(self, app_name):
        """Get the upload folder for a specific app."""
        app_folder = os.path.join(self.upload_folder, app_name)
        os.makedirs(app_folder, exist_ok=True)
        return app_folder

    def process_uploaded_file(self, file, app_name):
        """
        Save the uploaded file and return its file path and URL.
        
        Args:
            file: The uploaded file object
            app_name: The name of the app requesting the upload
            
        Returns:
            tuple: (file_path, file_url)
        """
        if not file or file.filename == '':
            raise ValueError("No file provided")

        # Secure the filename and get extension
        filename = secure_filename(file.filename)
        file_extension = filename.rsplit('.', 1)[-1].lower()
        
        # Generate unique filename
        unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
        
        # Get app-specific upload folder
        app_folder = self.get_app_upload_folder(app_name)
        file_path = os.path.join(app_folder, unique_filename)

        # Save the file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.stream, buffer)

        # Construct the public URL (you'll need to configure this based on your deployment)
        file_url = f"/uploads/{app_name}/{unique_filename}"

        return file_path, file_url

    def cleanup_file(self, file_path):
        """Safely remove a file if it exists."""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
        except Exception:
            return False
        return False 