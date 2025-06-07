import json


import json


def get_path_str(path: str | bytes) -> str:
    if isinstance(path, bytes):
        return path.decode('utf-8', errors='replace')
    return path

def display_start_message(extension_to_dir_map: dict):
    print("=" * 50)
    print("🗂️  File Watcher Mover")
    print("Directory configuration:")
    print(json.dumps(extension_to_dir_map, ensure_ascii=False, indent=2))
    print("Press Ctrl+C to exit.")
    print("=" * 50)
