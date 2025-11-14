
import pytest
import json
import requests

# List of apps and their corresponding data files
apps_to_test = [
    ("diet-tracker", "temp_diet_tracker.json"),
    ("matter_of_choice", "temp_matter_of_choice.json"),
    ("one-click-trip", "temp_one_click_trip.json"),
    ("school-killer", "temp_school_killer.json"),
    ("style-translator", "temp_style_translator.json"),
]

@pytest.mark.parametrize("app_name, data_file", apps_to_test)
def test_app_prompt(app_name, data_file):
    """
    Tests the /api/prompt endpoint for a given app.
    """
    with open(data_file, 'r') as f:
        json_data = json.load(f)
        app_data = json_data.get('data', {}) # Extract the nested data object

    payload = {
        "app_name": app_name,
        "data": app_data
    }

    response = requests.post("http://127.0.0.1:5000/api/prompt", json=payload)

    assert response.status_code == 200
    response_data = response.json()
    assert "response" in response_data
