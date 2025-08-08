# HTTP Status Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_400_BAD_REQUEST = 400
HTTP_401_UNAUTHORIZED = 401
HTTP_403_FORBIDDEN = 403
HTTP_404_NOT_FOUND = 404
HTTP_500_INTERNAL_SERVER_ERROR = 500

# Error Messages
ERROR_MESSAGES = {
    'INVALID_REQUEST': 'Invalid request data',
    'UNAUTHORIZED': 'Unauthorized access',
    'FORBIDDEN': 'Access forbidden',
    'NOT_FOUND': 'Resource not found',
    'SERVER_ERROR': 'Internal server error',
    'VALIDATION_ERROR': 'Validation error',
    'INVALID_CREDENTIALS': 'Invalid credentials',
    'EXPIRED_TOKEN': 'Token has expired',
    'INVALID_TOKEN': 'Invalid token',
    'MISSING_FIELDS': 'Required fields are missing'
}

# Success Messages
SUCCESS_MESSAGES = {
    'CREATED': 'Resource created successfully',
    'UPDATED': 'Resource updated successfully',
    'DELETED': 'Resource deleted successfully',
    'RETRIEVED': 'Resource retrieved successfully'
} 