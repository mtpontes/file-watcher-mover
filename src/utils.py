import json
import re
import sys
from pathlib import Path

import jsonschema

from src.config_model import ConfigModel
from src.log import log


def config_loader() -> dict:
    def read_config_schema() -> dict:
        # Packaged with PyInstaller
        if getattr(sys, "frozen", False):
            # Temporary folder where files are extracted
            base_dir = sys._MEIPASS  # noqa: SLF001
            schema_path = base_dir / "src" / "config_schema.json"
        else:
            # Running as script
            current_dir = Path(__file__).resolve().parent
            schema_path = current_dir / "config_schema.json"

        if not Path(schema_path).exists():
            msg = f"Schema file not found: {schema_path}"
            raise FileNotFoundError(msg)

        with Path(schema_path).open(encoding="utf-8") as file:
            schema: dict = json.load(file)

        return schema

    def read_config_file() -> dict:
        # Always seek config.json in the same directory as main.py or .exe
        if getattr(sys, "frozen", False):
            # Executable: sys.executable supports the .exe
            base_dir: str = Path(sys.executable).parent
        else:
            # Script: __file__ points to config.py, go up one level to the main.py directory
            base_dir: str = str(Path(__file__).resolve().parent.parent)
        config_path: str = Path(base_dir) / "config.json"

        if not Path(config_path).exists():
            msg = f"Config file not found: {config_path}"
            raise FileNotFoundError(msg)

        with Path(config_path).open(encoding="utf-8") as file:
            return json.load(file)

    schema, configs = read_config_schema(), read_config_file()
    try:
        jsonschema.validate(instance=configs, schema=schema)
    except Exception as e:
        log.error("Erro: %s", e)
        raise

    return configs


def get_path_str(path: str | bytes) -> str:
    if isinstance(path, bytes):
        return path.decode("utf-8", errors="replace")
    return path


def display_start_message(extension_to_dir_map: dict) -> None:
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
    path_filename = Path(filename)
    name = path_filename.stem
    ext = path_filename.suffix.lower()

    for pattern, path in config.pattern_config.pattern_to_path.items():
        log.debug("Pattern: %s, Path: %s, Name: %s", pattern, path, name)
        log.debug("Is valid: %s", re.match(pattern, name))
        if re.fullmatch(pattern, name) is not None:
            return path

    return config.extension_config.extension_to_path.get(ext.lower())
