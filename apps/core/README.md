# Core Application

This is the core application module that provides essential functionality and shared services for the entire application.

## Features

- Health check endpoint
- Core application services
- Shared utilities

## API Endpoints

- `GET /core/health` - Health check endpoint
  - Returns the health status of the core application
  - Response: `{"status": "healthy", "service": "core"}`

## Usage

The core application is automatically included in the main Flask application. To use its services, import from the core package:

```python
from apps.core.main import bp as core_bp
```

## Development

To add new features to the core application:

1. Add new routes in `main.py` using Flask Blueprint decorators
2. Create new modules as needed
3. Update this README with new features and endpoints 