# Intelliverse Server

## Overview
The Intelliverse Server is a Python-based backend application that hosts a suite of AI-powered tools leveraging Google's Gemini API. The server provides various functionalities including diet tracking, trip planning, style translation, educational assistance, and more.

**Last Updated:** November 15, 2025  
**Python Version:** 3.11  
**Framework:** Flask 3.1.2

## Project Structure

```
.
├── app.py                 # Universal Prompting Engine entry point
├── main.py               # Main Flask application entry point
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── apps/                 # Application modules
│   ├── Calories/         # Calorie tracking application
│   ├── DietTracker/      # Comprehensive diet tracking
│   ├── MatterOfChoice/   # Interactive decision-making tool
│   ├── OneClickTrip/     # Trip planning application
│   ├── SchoolKiller/     # Educational assistant
│   ├── StyleTranslator/  # Text style translation
│   └── core/             # Core shared functionalities
│       ├── gemini_service.py      # Gemini API integration
│       ├── prompt_service.py      # Prompt building service
│       ├── conversation_handler.py # Conversation management
│       ├── file_handler.py        # File upload handling
│       └── solution_handler.py    # Solution generation
├── shared/               # Shared utilities and middleware
│   ├── constants/        # Error codes and constants
│   ├── middleware/       # Authentication middleware
│   └── utils/            # Response and validation utilities
└── templates/            # HTML templates
    └── index.html        # Landing page

```

## Features

### Available Applications

1. **Calories** - Track and analyze calorie intake
2. **DietTracker** - Personalized dietary insights based on user metrics
3. **MatterOfChoice** - Interactive scenario-based decision tool with image generation
4. **OneClickTrip** - AI-powered trip planning with budget and style preferences
5. **SchoolKiller** - Educational assistant for various school subjects
6. **StyleTranslator** - Text style and tone transformation tool

### Core Services

- **Gemini Service** (`apps/core/gemini_service.py`) - Handles all Gemini API interactions
- **Prompt Service** (`apps/core/prompt_service.py`) - Builds structured prompts for different applications
- **File Handler** (`apps/core/file_handler.py`) - Manages file uploads
- **Conversation Handler** (`apps/core/conversation_handler.py`) - Processes conversations with AI

## API Endpoints

### Main Application (main.py)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Landing page - shows server status |
| `/core/upload` | POST | Upload files for processing |
| `/core/converse` | POST | Conversation with Gemini AI |
| `/core/generate_solutions` | POST | Generate AI solutions from prompts |
| `/core/health` | GET | Health check endpoint |

### Universal Prompting Engine (app.py)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/direct` | POST | Direct access to Gemini API |
| `/api/prompt` | POST | Structured prompt handling via app modules |

**Supported app_name values:**
- `diet-tracker`
- `one-click-trip`
- `matter_of_choice`
- `style-translator`
- `school-killer`

### MatterOfChoice Standalone App

The MatterOfChoice application has its own Flask instance with additional endpoints:
- `/cases` - Case generation interface
- `/casesv2` - Updated case interface
- `/v2/` - Version 2 interface
- `/start_case_generation` - Start background case generation
- `/get_job_status/<job_id>` - Poll job status
- `/analyze-image` - Image analysis
- `/analysis` - User response analysis
- `/submit_responses` - Submit user answers

## Environment Variables

### Required
- `GEMINI_API_KEY` - Google Gemini API key for AI functionality

### Optional
- `SECRET_KEY` - Flask secret key (defaults to 'dev-key-please-change-in-production')
- `HUGGINGFACE_API_KEY` - For MatterOfChoice image generation (if using that feature)

## Setup and Installation

### Prerequisites
- Python 3.11
- Gemini API key from https://makersuite.google.com/app/apikey

### Environment Setup
1. The GEMINI_API_KEY is configured in Replit Secrets
2. All dependencies are installed via requirements.txt
3. Flask runs on 0.0.0.0:5000 for Replit compatibility

### Running the Server
The server automatically starts via the configured workflow:
```bash
python main.py
```

## Development Notes

### Flask Configuration
- **Host:** 0.0.0.0 (required for Replit)
- **Port:** 5000 (required for Replit webview)
- **Debug Mode:** Enabled in development

### Architecture Patterns
- **Blueprint System:** Each application module uses Flask blueprints for modular routing
- **Service Layer:** Core services (Gemini, Prompt, File) are reusable across applications
- **Dependency Injection:** Services can be injected for testing (see handle_prompt functions)

### Architecture Overview

### Single Entry Point Design
The application uses **main.py** as the single entry point with a unified Flask application structure:

- **main.py** - Primary Flask application with all routes
  - Root routes (/, landing page)
  - Universal Prompting Engine routes (/api/direct, /api/prompt)
  - Blueprint for core services (/core/*)
  
- **app.py** - Legacy file, NOT USED (all functionality moved to main.py)

- **apps/*/main.py** - Application logic modules
  - These modules are NOT Flask blueprints
  - They provide `handle_prompt(data)` functions
  - Called programmatically via `/api/prompt` endpoint
  - Examples: DietTracker, OneClickTrip, SchoolKiller, etc.

- **apps/core/** - Core services blueprint
  - Only blueprint actually registered with Flask
  - Provides /core/upload, /core/converse, /core/generate_solutions
  - Shared services for file handling, Gemini API, prompts

- **apps/MatterOfChoice/app.py** - Standalone application
  - Separate Flask app with its own routes
  - NOT integrated with main.py
  - Can be run independently on a different port if needed
  - Contains UI routes for interactive case generation

### Routing Strategy

1. **Direct Gemini Access**: `POST /api/direct`
   - Raw access to Gemini API
   - No prompt templates
   - Direct model interaction

2. **Universal Prompting Engine**: `POST /api/prompt`
   - Structured access via application modules
   - Uses prompt templates
   - Routes to appropriate `handle_prompt()` function

3. **Core Services**: `/core/*`
   - File uploads: `/core/upload`
   - Conversations: `/core/converse`
   - Solution generation: `/core/generate_solutions`
   - Health check: `/core/health`

## Recent Changes (Import Setup)
1. Unified architecture: moved all routes to main.py (single entry point)
2. Removed empty blueprints from app modules (they're called programmatically)
3. Integrated Universal Prompting Engine into main.py
4. Standardized API key naming to `GEMINI_API_KEY`
5. Fixed missing imports in MatterOfChoice/app.py
6. Configured Flask to bind to 0.0.0.0:5000 for Replit compatibility
7. Updated .gitignore with Python and project-specific patterns
8. Added gunicorn for production deployment
9. Configured deployment for Replit autoscale

### Code Conventions
- All applications follow the `handle_prompt(data)` pattern
- API responses use JSON format
- Error handling returns descriptive error messages
- Logging is configured in core services for debugging

## Testing

Run the test suite:
```bash
pytest test_all_apps.py
```

Individual app tests:
```bash
pytest test_matter_of_choice.py
```

## Deployment

This application is configured to run on Replit with the following settings:

### Development
- Development server runs on port 5000
- Uses Flask's built-in development server
- Auto-reload enabled for code changes
- Debug mode enabled

### Production (Replit Autoscale)
- Deployment target: autoscale (stateless API server)
- WSGI server: Gunicorn with 4 workers
- Command: `gunicorn --bind=0.0.0.0:5000 --reuse-port --workers=4 main:create_app()`
- Port: 5000 (required for Replit)
- Auto-scaling enabled for traffic spikes

To deploy: Click the "Deploy" button in Replit and the configured deployment will run automatically.

## Troubleshooting

### Common Issues

1. **GEMINI_API_KEY not set**
   - Ensure the API key is added to Replit Secrets
   - The key is automatically loaded as an environment variable

2. **Import errors**
   - All dependencies should be installed via requirements.txt
   - Restart the workflow if needed

3. **Port conflicts**
   - The server runs on port 5000 by default
   - This is required for Replit's webview functionality

## API Usage Examples

### Using the Universal Prompting Engine

```python
# Example: Diet Tracker
POST /api/prompt
{
  "app_name": "diet-tracker",
  "data": {
    "user_task": "Create a meal plan",
    "is_image_used": false,
    "selected_solution_language": "en",
    "physical_activity": "moderate",
    "gender": "male",
    "age": 30,
    "height": 175.0,
    "weight": 70.0
  }
}
```

### Direct Gemini Access

```python
POST /api/direct
{
  "parts": ["What is the weather like today?"],
  "model_name": "gemini-2.5-pro"
}
```

### Core Conversation Endpoint

```python
POST /core/converse
{
  "text": "Explain quantum computing",
  "image_urls": [],
  "file_paths": [],
  "model_name": "gemini-pro-vision"
}
```

## Contributing

When adding new applications:
1. Create a new directory under `apps/`
2. Implement a `handle_prompt(data)` function in `main.py`
3. Create a Flask Blueprint with appropriate routes
4. Register the blueprint in the main `main.py` file
5. Add the app mapping to `app.py` if using the Universal Prompting Engine

## License

See individual application directories for licensing information.
