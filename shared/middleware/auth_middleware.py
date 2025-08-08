from functools import wraps
from flask import request, jsonify
from shared.utils.response_utils import error_response

def require_api_key(f):
    """Decorator to require API key in request headers"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            return error_response("API key is required", 401)
        # Add your API key validation logic here
        return f(*args, **kwargs)
    return decorated_function

def require_auth_token(f):
    """Decorator to require authentication token in request headers"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_token = request.headers.get('Authorization')
        if not auth_token:
            return error_response("Authentication token is required", 401)
        # Add your token validation logic here
        return f(*args, **kwargs)
    return decorated_function 