import json
from pathlib import Path

def update_module_version(app_label):
    base_path = Path(__file__).resolve().parent.parent.parent / "apps" / app_label
    metadata_path = base_path / "metadata.json"

    print("metadata_path", metadata_path)

    if not metadata_path.exists():
        raise FileNotFoundError("metadata.json not found")

    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    old_version = metadata.get("version")
    new_version = round(old_version + 0.1, 1)

    metadata["version"] = new_version

    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)

    return new_version
