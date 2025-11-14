import importlib
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.abspath('.'))

try:
    module_name = "MatterOfChoice"
    app_module = importlib.import_module(f'apps.{module_name}.main')
    if hasattr(app_module, 'handle_prompt'):
        print("handle_prompt found in app_module")
    else:
        print("handle_prompt NOT found in app_module")
    print(f"app_module.__file__: {app_module.__file__}")
    print(f"dir(app_module): {dir(app_module)}")
except Exception as e:
    print(f"Error during import: {e}")
