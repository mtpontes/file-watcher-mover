import json



def get_path_str(path: str | bytes) -> str:
    if isinstance(path, bytes):
        return path.decode('utf-8', errors='replace')
    return path

def get_targets(configs: dict) -> list[str]:
    targets: list[str] = configs.get("targets")
    if not targets:
        raise ValueError("TARGETS environment variable is not set or empty.")
    return targets

def display_start_message(extension_to_dir_map: dict):
    print("=" * 50)
    print("🗂️  File Watcher Mover")
    print("Directory configuration:")
    print(json.dumps(extension_to_dir_map, ensure_ascii=False, indent=2))
    print("Press Ctrl+C to exit.")
    print("=" * 50)

def get_extensions_map(configs: dict) -> dict:
    extension_map: dict = configs.get("extension")
    if not extension_map:
        raise ValueError("TARGETS environment variable is not set or empty.")
    return extension_map
