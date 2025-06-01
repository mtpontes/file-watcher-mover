import os, json, sys


def get_base_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable) # Rodando como .exe (PyInstaller)

    main_file: str = sys.argv[0]
    main_file_abs_path: str = os.path.abspath(main_file)
    return os.path.dirname(main_file_abs_path)

def load_extension_mapping(config_filename='config.json') -> dict:
    base_dir = get_base_dir()
    config_path = os.path.join(base_dir, config_filename)

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, 'r', encoding='utf-8') as file:
        return json.load(file)