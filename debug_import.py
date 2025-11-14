import sys
import importlib
import os

# Get the absolute path to the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
print(f"Project root: {project_root}")

# Add the project root to the Python path
sys.path.insert(0, project_root)
print(f"sys.path after modification: {sys.path}")

try:
    app_module = importlib.import_module('apps.MatterOfChoice.main')
    if hasattr(app_module, 'handle_prompt'):
        print("handle_prompt found in module.")
    else:
        print("handle_prompt NOT found in module.")
except Exception as e:
    print(f"Error during import or attribute check: {e}")
    import traceback
    traceback.print_exc()
