import os
import json

def load_module_config(app_config):
    """
    this will be used to handle for getting the metadata.json file
    """
    module_path = os.path.join(app_config.path, 'metadata.json')

    if os.path.exists(module_path):
        with open(module_path, 'r') as f:
            return json.load(f)
    return None
