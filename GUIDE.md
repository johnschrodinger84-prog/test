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
      "model_name": "gemini-1.5-flash-latest",
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

  * **Example 1: Diet Tracker Request**

    ```json
    {
      "app_name": "diet-tracker",
      "data": {
        "food_item": "1 large banana",
        "user_id": "user-123",
        "meal_type": "snack"
      }
    }
    ```

  * **Example 2: One-Click Trip Request**

    ```json
    {
      "app_name": "one-click-trip",
      "data": {
        "origin": "Addis Ababa",
        "city_paths": ["Nairobi", "Dar es Salaam"],
        "max_budget": 500,
        "travelers_number": 2
      }
    }
    ```

  * **Example 3: Matter of Choice Analysis Request**

    ```json
    {
      "app_name": "matter-of-choice-analysis",
      "data": {
        "language": "English",
        "role": "Hiring Manager",
        "question_type": "hiring",
        "cases": [
          {
            "case_id": "h-001",
            "question": "How do you handle tight deadlines?",
            "user_answer": "I prioritize tasks and communicate potential delays early."
          }
        ]
      }
    }
    ```

  * **Example 4: Style Translator Request**

    ```json
    {
      "app_name": "style-translator",
      "data": {
        "source_text": "It is with great pleasure that I accept your forthcoming invitation to the gala.",
        "target_style": "informal and excited"
      }
    }
    ```

  * **Example 5: School Killer Request**

    ```json
    {
      "app_name": "school-killer",
      "data": {
        "subject": "Physics",
        "problem_description": "A 2kg ball is dropped from a height of 10m. What is its velocity just before it hits the ground, ignoring air resistance?"
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