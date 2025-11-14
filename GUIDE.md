Certainly. Here is the updated documentation including all five application examples for the Universal Prompting Engine.

### **Unified Core Server API Documentation**

**Version**: 1.0
**Date**: August 8, 2025

-----

### \#\# 1. Objective

To consolidate multiple backend services into a single, efficient Core Server. This server provides a centralized and standardized interface for all front-end applications—including diverse apps like **StyleTranslator**, **Diet Tracker**, **OneClickTrip**, and **School Killer**—to interact with the Gemini API. 🚀

-----

### \#\# 2. Core Architecture

The server is designed with two primary functions, exposed via two distinct API endpoints:

1.  **Direct Tunnel** (`/api/direct`): Provides raw, unstructured access to the Gemini API for general-purpose queries.
2.  **Universal Prompting Engine** (`/api/prompt`): Provides structured, application-aware access to the Gemini API by using predefined prompt templates.

-----

### \#\# 3. API Endpoints

#### \#\#\# 3.1 Direct Tunnel

Provides direct access to the Gemini API. Use this for general conversations or simple file analysis where no application-specific logic is needed.

  * **Endpoint**: `POST /api/direct`
  * **Description**: Forwards a request directly to the Gemini API and returns the raw response.
  * **Request Body**: `application/json`
    ```json
    {
      "model_name": "gemini-2.5-flash",
      "parts": [
        {"text": "What is in this image?"},
        {"file_url": "https://.../uploads/image.jpg"}
      ]
    }
    ```
  * **Success Response (200 OK)**:
    ```json
    {
      "response": "This image contains a dog playing fetch in a park."
    }
    ```

#### \#\#\# 3.2 Universal Prompting Engine

This is the primary endpoint for all front-end applications. It uses internal logic to select the correct prompt template based on `app_name`, processes the request with that template, and returns a structured response.

  * **Endpoint**: `POST /api/prompt`

  * **Description**: Executes a predefined, application-specific prompt template.

  * **Request Body**: `application/json`

      * **`app_name`** (string, required): The unique identifier for the calling application.
      * **`data`** (object, required): The payload containing data specific to that application's prompt.

  * **Example 1: Calories Request**

    ```json
    {
      "app_name": "calorie_tracker",
      "data": {
        "user_task": "Analyze the nutritional content of this meal.",
        "is_image_used": true,
        "selected_solution_language": "English",
        "edited_recognized_text": "A plate of pasta with tomato sauce and meatballs."
      }
    }
    ```

  * **Example 2: Diet Tracker Request**

    ```json
    {
      "app_name": "diet_tracker",
      "data": {
        "user_task": "Provide a daily meal plan for weight loss.",
        "is_image_used": false,
        "selected_solution_language": "English",
        "physical_activity": "moderate",
        "gender": "female",
        "age": 30,
        "height": 165.0,
        "weight": 65.0,
        "edited_recognized_text": "I prefer vegetarian meals."
      }
    }
    ```

  * **Example 3: Matter of Choice Request**

    ```json
    {
      "app_name": "matter_of_choice",
      "data": {
        "user_task": "Analyze the user's choices in a behavioral scenario.",
        "is_image_used": false,
        "selected_solution_language": "English",
        "role": "Psychologist",
        "cases": [
          {
            "question": "You find a wallet on the street. What do you do?",
            "user_answer": "Return it to the owner."
          }
        ],
        "edited_recognized_text": "User is generally honest."
      }
    }
    ```

  * **Example 4: One-Click Trip Request**

    ```json
    {
      "app_name": "one_click_trip",
      "data": {
        "user_task": "Plan a romantic getaway.",
        "is_image_used": false,
        "selected_solution_language": "English",
        "origin_location": "New York",
        "city_paths": ["Paris", "Rome"],
        "transportation_types": ["flight"],
        "trip_styles": ["romantic", "sightseeing"],
        "max_budget": 5000,
        "trip_duration": 7,
        "travelers_number": 2,
        "is_one_way": false
      }
    }
    ```

  * **Example 5: School Killer Request**

    ```json
    {
      "app_name": "school-killer",
      "data": {
        "user_task": "Solve this math problem.",
        "is_image_used": false,
        "selected_solution_language": "English",
        "subject": "Mathematics",
        "problem_description": "What is the derivative of x^2?",
        "edited_recognized_text": "Show step-by-step solution."
      }
    }
    ```

  * **Example 6: Style Translator Request**

    ```json
    {
      "app_name": "style-translator",
      "data": {
        "user_task": "Translate and rephrase this text.",
        "selected_solution_language": "French",
        "edited_recognized_text": "Hello, how are you doing today?",
        "tone_preference": "formal",
        "style": "polite"
      }
    }
    ```

  * **Success Response (200 OK)**: The server returns a structured JSON object, the format of which depends on the `app_name`'s prompt template. For instance, a response for the **Style Translator** request would look like this:

    ```json
    {
      "response": {
        "translated_text": "OMG yes! I'd love to come to the gala! Can't wait!",
        "style_detected": "formal",
        "style_applied": "informal and excited"
      }
    }
    ```

-----

### \#\# 4. Configuration

The server is configured using environment variables. ⚙️

  * `GEMINI_API_KEY`: **Required**. Your API key for the Gemini service.
  * `SECRET_KEY`: **Required**. A secret key used for signing session data.
  * `BASE_URL`: The public base URL where the server is hosted (e.g., `https://api.intelliverse.com`), used for constructing file URLs.