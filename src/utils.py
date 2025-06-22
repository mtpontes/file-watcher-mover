import json, re, os, sys

import jsonschema

from src.log import log
from src.config_model import ConfigModel


def config_loader() -> dict:
    def read_config_schema() -> dict:
        if getattr(sys, 'frozen', False):
            # Packaged with PyInstaller
            base_dir = sys._MEIPASS  # Temporary folder where files are extracted
            schema_path = os.path.join(base_dir, "src", "config_schema.json")
        else:
            # Running as script
            current_dir = os.path.dirname(os.path.abspath(__file__))  # /src
            schema_path = os.path.join(current_dir, "config_schema.json")

        if not os.path.exists(schema_path):
            raise FileNotFoundError(f"Schema file not found: {schema_path}")

        with open(schema_path, 'r', encoding='utf-8') as file:
            schema: dict = json.load(file)

        return schema

    def read_config_file() -> dict:
        # Always seek config.json in the same directory as main.py or .exe
        if getattr(sys, 'frozen', False):
            # Executable: sys.executable supports the .exe
            base_dir: str  = os.path.dirname(sys.executable)
        else:
            # Script: __file__ points to config.py, go up one level to the main.py directory
            base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path: str = os.path.join(base_dir, 'config.json')
        
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(config_path, 'r', encoding='utf-8') as file:
            configs: dict = json.load(file)

        return configs
    
    schema, configs = read_config_schema(), read_config_file()
    try:
        jsonschema.validate(instance=configs, schema=schema)
    except Exception as e:
        log.error("Erro: %s", e)
        raise e

    return configs


def get_path_str(path: str | bytes) -> str:
    if isinstance(path, bytes):
        return path.decode('utf-8', errors='replace')
    return path

def display_start_message(extension_to_dir_map: dict):
    log.info("=" * 50)
    log.info("🗂️  File Watcher Mover")
    log.info("Directory configuration:")
    log.info(json.dumps(extension_to_dir_map, ensure_ascii=False, indent=2))
    log.info("Press Ctrl+C to exit.")
    log.info("=" * 50)

def resolve_destiny_path(filename: str, config: ConfigModel) -> str | None:
    """
    Returns the destination path for a file based on patterns and extensions.
    :param filename: Name of the file (ex: foto.png)
    :param config: Instance of ConfigModel
    :return: Destination path or None
    """
    name, ext = os.path.splitext(filename)
    
    for pattern, path in config.pattern_config.pattern_to_path.items():
        log.debug("Pattern: %s, Path: %s, Name: %s", pattern, path, name)
        log.debug("Is valid: %s", re.match(pattern, name))
        if re.fullmatch(pattern, name) is not None:
            return path
    
    return config.extension_config.extension_to_path.get(ext.lower())
