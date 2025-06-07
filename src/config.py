import os
import sys
import json


def load_extension_mapping(config_path=None) -> dict:
    if config_path is None:
        # Always seek config.json in the same directory as main.py or .exe
        if getattr(sys, 'frozen', False):
            # Executable: sys.executable supports the .exe
            base_dir = os.path.dirname(sys.executable)
        else:
            # Script: __file__ points to config.py, go up one level to the main.py directory
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(base_dir, 'config.json')
        
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def get_targets(configs: dict) -> list[str]:
    targets: list[str] = configs.get("targets")
    if not targets:
        raise ValueError("'targets' config is not set or empty.")
    return targets

def get_extensions_map(configs: dict) -> dict:
    extension_map: dict = configs.get("extension")
    if not extension_map:
        raise ValueError("'extensions' config is not set or empty.")
    return extension_map