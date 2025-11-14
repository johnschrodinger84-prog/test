import sys
import os
import importlib

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

try:
    # Import the handle_prompt function from MatterOfChoice
    matter_of_choice_main = importlib.import_module('apps.MatterOfChoice.main')
    handle_prompt = matter_of_choice_main.handle_prompt

    # Sample data for testing with correct 'cases' format
    test_data = {
        "user_task": "Help me decide between two options.",
        "is_image_used": False,
        "selected_solution_language": "English",
        "role": "decision maker",
        "cases": [
            {"question": "What is your preference for Option A?", "user_answer": "I like Option A because it's simple."},
            {"question": "What is your preference for Option B?", "user_answer": "Option B offers more features."}
        ]
    }

    print("Calling handle_prompt with sample data...")
    response = handle_prompt(test_data)
    print("Response from handle_prompt:")
    print(response)

except Exception as e:
    print(f"An error occurred: {e}")
    import traceback
    traceback.print_exc()