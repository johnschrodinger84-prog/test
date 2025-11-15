# API Client Guide

Complete API reference with predefined request examples for all applications.

## Table of Contents
- [Base URL & Authentication](#base-url--authentication)
- [Core Endpoints](#core-endpoints)
- [Universal Prompting Engine](#universal-prompting-engine)
- [Application-Specific Requests](#application-specific-requests)
  - [DietTracker](#1-diettracker)
  - [OneClickTrip](#2-oneclicktrip)
  - [SchoolKiller](#3-schoolkiller)
  - [StyleTranslator](#4-styletranslator)
  - [Calories](#5-calories)
  - [MatterOfChoice](#6-matterofchoice)

---

## Base URL & Authentication

**Base URL:** `https://your-domain.replit.dev`

**Authentication:** API key should be configured server-side via `GEMINI_API_KEY` environment variable.

---

## Core Endpoints

### Health Check
Check if the API is running.

**Endpoint:** `GET /core/health`

**Request:**
```bash
curl -X GET https://your-domain.replit.dev/core/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "core"
}
```

---

### File Upload
Upload files to the server.

**Endpoint:** `POST /core/upload`

**Request:**
```bash
curl -X POST https://your-domain.replit.dev/core/upload \
  -F "file=@/path/to/your/file.jpg" \
  -F "app_name=core"
```

**Response:**
```json
{
  "file_path": "/uploads/core/file_12345.jpg",
  "url": "https://your-domain.replit.dev/uploads/core/file_12345.jpg"
}
```

---

### Conversation
Have a conversation with Gemini AI using text, images, or files.

**Endpoint:** `POST /core/converse`

**Request:**
```bash
curl -X POST https://your-domain.replit.dev/core/converse \
  -H "Content-Type: application/json" \
  -d '{
    "text": "What is in this image?",
    "image_urls": ["https://example.com/image.jpg"],
    "file_paths": [],
    "model_name": "gemini-pro-vision"
  }'
```

**Response:**
```json
{
  "response": "I can see a beautiful landscape with mountains..."
}
```

---

### Generate Solutions
Generate solutions from images with OCR and AI processing.

**Endpoint:** `POST /core/generate_solutions`

**Request:**
```bash
curl -X POST https://your-domain.replit.dev/core/generate_solutions \
  -F "prompt=Solve this math problem" \
  -F "image_files=@/path/to/problem.jpg"
```

**Response:**
```json
{
  "solutions": [
    {
      "recognized_text": "2x + 5 = 15",
      "solution": "x = 5"
    }
  ]
}
```

---

## Universal Prompting Engine

### Direct Gemini Access
Raw access to Gemini API for general-purpose queries.

**Endpoint:** `POST /api/direct`

**Request:**
```bash
curl -X POST https://your-domain.replit.dev/api/direct \
  -H "Content-Type: application/json" \
  -d '{
    "parts": ["What is the capital of France?"],
    "model_name": "gemini-2.5-flash"
  }'
```

**Response:**
```json
{
  "response": "The capital of France is Paris."
}
```

---

### Universal Prompt Endpoint
Structured access to specialized AI applications.

**Endpoint:** `POST /api/prompt`

**Base Request Structure:**
```json
{
  "app_name": "app-identifier",
  "data": {
    // App-specific parameters
  }
}
```

---

## Application-Specific Requests

### 1. DietTracker
Personalized dietary insights based on user metrics.

**App Name:** `diet-tracker`

**Request Example:**
```bash
curl -X POST https://your-domain.replit.dev/api/prompt \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "diet-tracker",
    "data": {
      "user_task": "Create a meal plan for weight loss",
      "is_image_used": false,
      "selected_solution_language": "English",
      "physical_activity": "moderate",
      "gender": "male",
      "age": 30,
      "height": 175.5,
      "weight": 80.0,
      "edited_recognized_text": ""
    }
  }'
```

**Required Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `user_task` | string | The dietary task or question |
| `is_image_used` | boolean | Whether an image is being analyzed |
| `selected_solution_language` | string | Language for the response |
| `physical_activity` | string | Activity level (e.g., "sedentary", "moderate", "active") |
| `gender` | string | User's gender |
| `age` | integer | User's age |
| `height` | float | User's height in cm |
| `weight` | float | User's weight in kg |

**Optional Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `edited_recognized_text` | string | OCR text from food images |

**Response:**
```json
{
  "response": "Based on your profile (30-year-old male, 175.5cm, 80kg, moderate activity)...\n\nDaily caloric needs: ~2500 calories\n\nMeal Plan:\n..."
}
```

---

### 2. OneClickTrip
Comprehensive trip planning based on preferences and budget.

**App Name:** `one-click-trip`

**Request Example:**
```bash
curl -X POST https://your-domain.replit.dev/api/prompt \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "one-click-trip",
    "data": {
      "user_task": "Plan a romantic vacation",
      "is_image_used": false,
      "selected_solution_language": "English",
      "origin_location": "New York",
      "city_paths": ["Paris", "Rome", "Barcelona"],
      "transportation_types": ["flight", "train"],
      "trip_styles": ["romantic", "cultural"],
      "max_budget": 5000,
      "trip_duration": 14,
      "travelers_number": 2,
      "is_one_way": false,
      "edited_recognized_text": ""
    }
  }'
```

**Required Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `user_task` | string | Trip planning request |
| `is_image_used` | boolean | Whether an image is being analyzed |
| `selected_solution_language` | string | Language for the response |
| `origin_location` | string | Starting location |
| `city_paths` | array | List of cities to visit |
| `transportation_types` | array | Preferred transportation modes |
| `trip_styles` | array | Trip styles (e.g., "adventure", "luxury") |
| `max_budget` | integer | Maximum budget in USD |
| `trip_duration` | integer | Trip duration in days |
| `travelers_number` | integer | Number of travelers |

**Optional Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `is_one_way` | boolean | Whether it's a one-way trip |
| `edited_recognized_text` | string | Additional text input |

**Response:**
```json
{
  "response": "14-Day Romantic European Tour for 2 ($5000 budget)\n\nDay 1-5: Paris...\n\nTransportation:\n- Flight NYC → Paris: $1200 (both)\n..."
}
```

---

### 3. SchoolKiller
Educational assistant for homework and school subjects.

**App Name:** `school-killer`

**Request Example:**
```bash
curl -X POST https://your-domain.replit.dev/api/prompt \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "school-killer",
    "data": {
      "user_task": "Help me solve this problem",
      "is_image_used": false,
      "selected_solution_language": "English",
      "subject": "Mathematics",
      "problem_description": "Solve the quadratic equation: x² + 5x + 6 = 0",
      "edited_recognized_text": ""
    }
  }'
```

**Required Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `user_task` | string | What you need help with |
| `is_image_used` | boolean | Whether an image is being analyzed |
| `selected_solution_language` | string | Language for the response |
| `subject` | string | School subject (Math, Physics, etc.) |
| `problem_description` | string | Detailed problem description |

**Optional Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `edited_recognized_text` | string | OCR text from problem images |

**Response:**
```json
{
  "response": "Let's solve x² + 5x + 6 = 0\n\nStep 1: Factor the quadratic...\n\nAnswer: x = -2 or x = -3"
}
```

---

### 4. StyleTranslator
Translate text style, tone, and demographic targeting.

**App Name:** `style-translator`

**Request Example:**
```bash
curl -X POST https://your-domain.replit.dev/api/prompt \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "style-translator",
    "data": {
      "user_task": "Make this message sound more professional",
      "selected_solution_language": "English",
      "is_image_used": false,
      "tone_preference": "formal",
      "style": "business",
      "mentality": "corporate",
      "transformation_level": 8,
      "category": "email",
      "source_gender": "neutral",
      "target_gender": "neutral",
      "source_age": 25,
      "target_age": 45,
      "edited_recognized_text": "Hey, can u send me that report ASAP? Thx!"
    }
  }'
```

**Required Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `user_task` | string | Style transformation request |
| `selected_solution_language` | string | Language for the response |

**Optional Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `is_image_used` | boolean | Whether an image is being analyzed |
| `tone_preference` | string | Desired tone (formal, casual, etc.) |
| `style` | string | Writing style |
| `mentality` | string | Target mentality |
| `transformation_level` | integer | Intensity of transformation (1-10) |
| `category` | string | Content category |
| `source_gender` | string | Original gender perspective |
| `target_gender` | string | Target gender perspective |
| `source_age` | integer | Original age perspective |
| `target_age` | integer | Target age perspective |
| `edited_recognized_text` | string | Text to transform |

**Response:**
```json
{
  "response": "Dear Colleague,\n\nI would appreciate if you could forward the requested report at your earliest convenience.\n\nBest regards"
}
```

---

### 5. Calories
Track and analyze calorie intake from food descriptions or images.

**App Name:** `calories`

**Request Example:**
```bash
curl -X POST https://your-domain.replit.dev/api/prompt \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "calories",
    "data": {
      "user_task": "Calculate calories from my meal",
      "is_image_used": true,
      "selected_solution_language": "English",
      "edited_recognized_text": "Grilled chicken breast (200g), steamed broccoli (150g), brown rice (100g)"
    }
  }'
```

**Required Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `user_task` | string | Calorie tracking request |
| `is_image_used` | boolean | Whether analyzing a food image |
| `selected_solution_language` | string | Language for the response |

**Optional Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `edited_recognized_text` | string | Food description or OCR text |

**Response:**
```json
{
  "response": "Meal Analysis:\n\n- Grilled Chicken Breast (200g): 330 calories\n- Steamed Broccoli (150g): 50 calories\n- Brown Rice (100g): 112 calories\n\nTotal: 492 calories"
}
```

---

### 6. MatterOfChoice
Decision-making assistant based on role and multiple scenarios.

**App Name:** `matter_of_choice`

**Request Example:**
```bash
curl -X POST https://your-domain.replit.dev/api/prompt \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "matter_of_choice",
    "data": {
      "user_task": "Help me decide which job offer to accept",
      "is_image_used": false,
      "selected_solution_language": "English",
      "role": "Software Engineer",
      "cases": [
        "Startup: $120k, equity, flexible hours, high risk",
        "Big Tech: $180k, stability, benefits, less flexibility",
        "Remote: $140k, work from anywhere, small team"
      ],
      "edited_recognized_text": ""
    }
  }'
```

**Required Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `user_task` | string | Decision request |
| `is_image_used` | boolean | Whether an image is being analyzed |
| `selected_solution_language` | string | Language for the response |
| `role` | string | Your role/perspective |
| `cases` | array | List of options to choose from |

**Optional Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `edited_recognized_text` | string | Additional context |

**Response:**
```json
{
  "response": "Analysis for Software Engineer Role Selection:\n\nOption 1 (Startup):\nPros: ...\nCons: ...\n\nOption 2 (Big Tech):\n...\n\nRecommendation: Based on your career stage..."
}
```

---

## Error Handling

All endpoints return standard HTTP status codes:

- `200` - Success
- `201` - Created (file uploads)
- `400` - Bad Request (invalid parameters)
- `404` - Not Found
- `500` - Internal Server Error
- `503` - Service Unavailable (API key not configured)

**Error Response Format:**
```json
{
  "error": "Error message describing what went wrong"
}
```

---

## Rate Limits

Please refer to [Gemini API Rate Limits](https://ai.google.dev/gemini-api/docs/rate-limits) for current quota information.

---

## Support

For issues or questions, please contact the development team or check the project repository.
