# Modular Flask Server

This is a modular Flask server that hosts multiple independent applications under a single server instance. Each application is implemented as a Flask Blueprint, allowing for clean separation of concerns and easy addition of new applications.

## Project Structure

```
.
├── apps/                           # Contains all application modules
│   ├── core/                      # Core application services
│   │   ├── __init__.py           # Core package initialization
│   │   ├── prompt_service.py     # Shared prompt building service
│   │   └── README.md             # Core module documentation
│   ├── OneClickTrip/             # OneClickTrip application
│   │   ├── __init__.py          # Blueprint registration
│   │   ├── main.py              # Main application logic
│   │   └── routes.py            # Route definitions (future use)
│   ├── Calories/                # Calories application
│   │   ├── __init__.py         # Blueprint registration
│   │   ├── main.py            # Main application logic
│   │   └── routes.py          # Route definitions (future use)
│   ├── SchoolKiller/          # SchoolKiller application
│   │   ├── __init__.py       # Blueprint registration
│   │   ├── main.py          # Main application logic
│   │   └── routes.py        # Route definitions (future use)
│   └── StyleTranslator/     # StyleTranslator application
├── config.py                # Configuration settings
├── main.py                 # Main server file
├── requirements.txt        # Project dependencies
└── .gitignore             # Git ignore patterns
```

## Applications

Each application is accessible through its own URL prefix and provides a `/build_prompt` endpoint for prompt generation:

1. **OneClickTrip** - URL prefix: `/oneclicktrip`
   - Builds prompts for travel planning
   - Supports parameters like origin, trip type, cities, transportation, etc.

2. **Calories** - URL prefix: `/calories`
   - Builds prompts for calorie tracking and nutrition
   - Uses base parameters for prompt construction

3. **SchoolKiller** - URL prefix: `/schoolkiller`
   - Builds prompts for educational assistance
   - Supports parameters like grade level and detail level

4. **StyleTranslator** - URL prefix: `/styletranslator`
   - Builds prompts for style transformation
   - Supports various style parameters like tone, gender, age, etc.

## Common Endpoints

All applications implement the following endpoints:

1. **Index** (`GET /`)
   - Returns welcome message and API documentation
   - Lists available endpoints and their parameters

2. **Build Prompt** (`PUT /build_prompt`)
   - Common base parameters:
     - `user_task` (string): The main task description
     - `is_image_used` (boolean): Whether image analysis is needed
     - `selected_solution_language` (string): Language for the response
     - `edited_recognized_text` (string, optional): Additional context
   - App-specific parameters vary by application

## Recent Changes

1. **Blueprint Structure**
   - Standardized blueprint registration across all apps
   - Moved route definitions to `main.py`
   - Reserved `routes.py` for future route additions
   - Fixed blueprint naming conflicts

2. **Prompt Service**
   - Added shared `PromptService` in core module
   - Implemented app-specific prompt builders
   - Added caching for prompt generation
   - Standardized parameter handling

3. **Error Handling**
   - Added consistent error responses
   - Improved parameter validation
   - Added proper HTTP status codes

## Setup Instructions

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the server:
   ```bash
   python main.py
   ```

The server will start in development mode on `http://localhost:5000`

## Adding New Applications

To add a new application:

1. Create a new directory under `apps/`
2. Create the necessary files:
   - `__init__.py` - Import blueprint from main.py
   - `main.py` - Define blueprint and implement routes
   - `routes.py` - Reserved for future route additions
3. Implement the required endpoints:
   - Index route (`/`)
   - Build prompt route (`/build_prompt`)
4. Register the blueprint in `main.py`

## Error Handling

The server includes comprehensive error handling for:
- 404 Not Found errors
- 405 Method Not Allowed errors
- 400 Bad Request errors (invalid parameters)
- 500 Internal Server errors

All errors return JSON responses with appropriate status codes and error messages.

## Development Guidelines

1. **Blueprint Naming**
   - Use consistent naming (e.g., 'oneclicktrip', 'calories')
   - Match URL prefix with blueprint name

2. **Parameter Validation**
   - Validate all required parameters
   - Use type checking for parameters
   - Provide clear error messages

3. **Documentation**
   - Keep README.md updated
   - Document all endpoints
   - Include example requests/responses

4. **Code Organization**
   - Keep routes in main.py
   - Use routes.py for future additions
   - Follow consistent file structure 