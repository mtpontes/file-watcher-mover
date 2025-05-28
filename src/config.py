import os, json


def load_extension_mapping(config_path='config.json') -> dict:
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, 'r', encoding='utf-8') as file:
        return json.load(file)