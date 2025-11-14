# Intelliverse Server

## Overview

The Intelliverse Server is a Python-based backend application designed to host a suite of AI-powered tools. It leverages the Gemini API to provide various functionalities, from diet tracking and trip planning to style translation and educational assistance. The server is built with a modular architecture, allowing for easy integration of new applications.

## Features

The server currently includes the following applications:

*   **Calories:** A tool for tracking and analyzing calorie intake, likely based on user input or recognized text from images.
*   **DietTracker:** A comprehensive diet tracking application that considers physical activity, gender, age, height, and weight to provide personalized dietary insights.
*   **MatterOfChoice:** An interactive application that handles user prompts related to roles and cases, suggesting a decision-making or scenario-based tool.
*   **OneClickTrip:** A trip planning application that helps users organize travel based on origin, city paths, transportation types, trip styles, budget, duration, and number of travelers.
*   **SchoolKiller:** An educational assistant designed to help with various school subjects by processing problem descriptions.
*   **StyleTranslator:** A tool for translating text style, offering parameters like tone, mentality, transformation level, and demographic considerations.

## Project Structure

The project is organized into the following key directories:

*   `apps/`: Contains individual AI-powered applications, each in its own subdirectory.
    *   `apps/core/`: Houses core functionalities shared across applications, such as `PromptService` for building prompts and `GeminiService` for interacting with the Gemini API.
*   `shared/`: Contains common utilities, middleware, and constants used throughout the server.
*   `templates/`: Stores HTML templates for the web interface.
*   `config.py`: Configuration settings for the server.
*   `main.py`: The primary entry point for running the Flask server and routing requests to the appropriate applications.
*   `app.py`: Initializes the Flask application and registers blueprints.
*   `requirements.txt`: Lists all Python dependencies required for the project.
*   `test_all_apps.py`: Contains tests for the various applications.

## Setup and Installation

To set up and run the Intelliverse Server, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd Intelliverse-server
    ```
    (Note: You are already in the project directory, so this step is for future reference.)

2.  **Create a virtual environment:**
    It's highly recommended to use a virtual environment to manage project dependencies.
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    *   **On Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    *   **On macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install dependencies:**
    Install all required Python packages using pip:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Configure the server:**
    Edit `config.py` to set up any necessary configurations, such as API keys for the Gemini API.

## Running the Server

Once the setup is complete, you can run the server using `main.py`:

```bash
python main.py
```

This will start the Flask development server, and you should see output indicating that the server is running, typically on `http://127.0.0.1:5000/` or a similar address.

## API Endpoints

The server exposes various API endpoints, primarily handled by the `main.py` and `app.py` files in the root, which route requests to the `handle_prompt` function within each application's `main.py` file.

Each application's `handle_prompt` function expects a `data` dictionary containing specific parameters. Common parameters include:

*   `user_task` (str): The user's specific request or task.
*   `is_image_used` (bool): Indicates whether an image is part of the input.
*   `selected_solution_language` (str): The desired language for the solution.
*   `edited_recognized_text` (str, optional): Text recognized from an image, potentially edited by the user.

Application-specific parameters are also required, as detailed in each application's `main.py` file.

## Configuration

The `config.py` file is used for server-wide configurations. This is where you would typically store sensitive information like API keys or adjust server settings.

## Testing

The project includes a `test_all_apps.py` file for testing the functionality of the integrated applications. To run the tests, ensure you have `pytest` installed (it should be included in `requirements.txt`) and run:

```bash
pytest
```