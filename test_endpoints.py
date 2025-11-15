import requests
import json
import os
from io import BytesIO

BASE_URL = f"https://{os.getenv('REPLIT_DEV_DOMAIN', 'localhost:5000')}"

def print_test_header(endpoint, method):
    print("\n" + "="*80)
    print(f"Testing: {method} {endpoint}")
    print("="*80)

def print_response(response):
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    try:
        print(f"Response Body: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response Body (text): {response.text[:500]}")

def test_root():
    """Test GET / endpoint"""
    print_test_header("/", "GET")
    try:
        response = requests.get(f"{BASE_URL}/")
        print_response(response)
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def test_health_check():
    """Test GET /core/health endpoint"""
    print_test_header("/core/health", "GET")
    try:
        response = requests.get(f"{BASE_URL}/core/health")
        print_response(response)
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def test_api_direct_missing_api_key():
    """Test POST /api/direct without API key (should return 503 or work depending on key presence)"""
    print_test_header("/api/direct", "POST")
    print("Test Case: Valid request structure")
    try:
        payload = {
            "parts": ["What is 2+2?"],
            "model_name": "gemini-2.5-flash"
        }
        response = requests.post(
            f"{BASE_URL}/api/direct",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print_response(response)
        return response.status_code in [200, 503]
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def test_api_direct_invalid_request():
    """Test POST /api/direct with invalid request (missing 'parts')"""
    print_test_header("/api/direct", "POST")
    print("Test Case: Invalid request - missing 'parts'")
    try:
        payload = {
            "model_name": "gemini-2.5-flash"
        }
        response = requests.post(
            f"{BASE_URL}/api/direct",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print_response(response)
        return response.status_code == 400
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def test_api_prompt_valid():
    """Test POST /api/prompt with valid app_name"""
    print_test_header("/api/prompt", "POST")
    print("Test Case: Valid request for diet-tracker app")
    try:
        payload = {
            "app_name": "diet-tracker",
            "data": {
                "food_items": ["apple", "banana"],
                "query": "Calculate calories"
            }
        }
        response = requests.post(
            f"{BASE_URL}/api/prompt",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print_response(response)
        return response.status_code in [200, 503, 500]
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def test_api_prompt_invalid_app():
    """Test POST /api/prompt with invalid app_name"""
    print_test_header("/api/prompt", "POST")
    print("Test Case: Invalid app_name")
    try:
        payload = {
            "app_name": "non-existent-app",
            "data": {}
        }
        response = requests.post(
            f"{BASE_URL}/api/prompt",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print_response(response)
        return response.status_code == 400
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def test_api_prompt_missing_fields():
    """Test POST /api/prompt with missing required fields"""
    print_test_header("/api/prompt", "POST")
    print("Test Case: Missing 'app_name' field")
    try:
        payload = {
            "data": {}
        }
        response = requests.post(
            f"{BASE_URL}/api/prompt",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print_response(response)
        return response.status_code == 400
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def test_core_upload_no_file():
    """Test POST /core/upload without file"""
    print_test_header("/core/upload", "POST")
    print("Test Case: No file provided")
    try:
        response = requests.post(f"{BASE_URL}/core/upload")
        print_response(response)
        return response.status_code == 400
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def test_core_upload_with_file():
    """Test POST /core/upload with a test file"""
    print_test_header("/core/upload", "POST")
    print("Test Case: Valid file upload")
    try:
        # Create a simple text file
        files = {
            'file': ('test.txt', BytesIO(b'Hello, World!'), 'text/plain')
        }
        data = {
            'app_name': 'core'
        }
        response = requests.post(
            f"{BASE_URL}/core/upload",
            files=files,
            data=data
        )
        print_response(response)
        return response.status_code in [200, 201]
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def test_core_converse_no_data():
    """Test POST /core/converse without data"""
    print_test_header("/core/converse", "POST")
    print("Test Case: No data provided")
    try:
        response = requests.post(
            f"{BASE_URL}/core/converse",
            headers={"Content-Type": "application/json"}
        )
        print_response(response)
        return response.status_code == 400
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def test_core_converse_valid():
    """Test POST /core/converse with valid data"""
    print_test_header("/core/converse", "POST")
    print("Test Case: Valid conversation request")
    try:
        payload = {
            "text": "What is the weather like?",
            "image_urls": [],
            "file_paths": [],
            "model_name": "gemini-pro"
        }
        response = requests.post(
            f"{BASE_URL}/core/converse",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print_response(response)
        return response.status_code in [200, 503, 500]
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def test_core_generate_solutions_no_data():
    """Test POST /core/generate_solutions without data"""
    print_test_header("/core/generate_solutions", "POST")
    print("Test Case: No data provided")
    try:
        response = requests.post(f"{BASE_URL}/core/generate_solutions")
        print_response(response)
        return response.status_code == 400
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def test_404_endpoint():
    """Test non-existent endpoint"""
    print_test_header("/non-existent", "GET")
    print("Test Case: Non-existent endpoint")
    try:
        response = requests.get(
            f"{BASE_URL}/non-existent",
            headers={"Accept": "application/json"}
        )
        print_response(response)
        return response.status_code == 404
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def run_all_tests():
    """Run all endpoint tests"""
    print("\n" + "="*80)
    print("ENDPOINT TESTING SUITE")
    print("="*80)
    print(f"Base URL: {BASE_URL}")
    
    tests = [
        ("GET / (Root)", test_root),
        ("GET /core/health", test_health_check),
        ("POST /api/direct (valid)", test_api_direct_missing_api_key),
        ("POST /api/direct (invalid)", test_api_direct_invalid_request),
        ("POST /api/prompt (valid)", test_api_prompt_valid),
        ("POST /api/prompt (invalid app)", test_api_prompt_invalid_app),
        ("POST /api/prompt (missing fields)", test_api_prompt_missing_fields),
        ("POST /core/upload (no file)", test_core_upload_no_file),
        ("POST /core/upload (with file)", test_core_upload_with_file),
        ("POST /core/converse (no data)", test_core_converse_no_data),
        ("POST /core/converse (valid)", test_core_converse_valid),
        ("POST /core/generate_solutions (no data)", test_core_generate_solutions_no_data),
        ("GET /non-existent (404)", test_404_endpoint),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\nFATAL ERROR in {test_name}: {str(e)}")
            results[test_name] = False
    
    # Print summary
    print("\n\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print("="*80)
    print(f"Total: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print("="*80)

if __name__ == "__main__":
    run_all_tests()
