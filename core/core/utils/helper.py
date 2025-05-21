import os
import json
from django.apps import apps

def load_module_config(app_label):
    """
    this will be used to handle for getting the metadata.json file
    """
    app_config = apps.get_app_config(app_label)
    module_path = os.path.join(app_config.path, 'metadata.json')

    if os.path.exists(module_path):
        with open(module_path, 'r') as f:
            return json.load(f)
    return None
