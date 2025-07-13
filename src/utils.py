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


def _resolve_destiny_by_pattern(file_path: Path, config: ConfigModel) -> str | None:
    file_path_parent = file_path.parent.resolve()
    file_name_stem = file_path.stem

    for pattern, path in config.pattern_config.pattern_to_path.items():
        destiny_dir = Path(path).resolve()

        if file_path_parent == destiny_dir:
            log.debug("Skipping pattern %s because source and destiny are the same: %s", pattern, destiny_dir)
            continue

        is_match = re.fullmatch(pattern, file_name_stem)
        log.debug(
            "Checking pattern: %s | Directory: %s | File name: %s | Match: %s",
            pattern,
            destiny_dir,
            file_name_stem,
            bool(is_match),
        )
        if is_match:
            return str(destiny_dir)

    return None


def _resolve_destiny_by_extension(file_path: Path, config: ConfigModel) -> str | None:
    file_path_parent = file_path.parent.resolve()
    file_ext = file_path.suffix.lower()

    extension_destiny = config.extension_config.extension_to_path.get(file_ext)
    if extension_destiny:
        destiny_dir = Path(extension_destiny).resolve()
        if file_path_parent == destiny_dir:
            log.debug("Skipping extension mapping because source and destiny are the same: %s", destiny_dir)
            return None
        log.debug("Destination by extension: %s", destiny_dir)
        return str(destiny_dir)

    return None


def resolve_destiny_path(file_path: Path, config: ConfigModel) -> str | None:
    """
    Returns the destination directory for a file based on patterns and extensions.
    """
    destiny = _resolve_destiny_by_pattern(file_path, config)
    if destiny:
        return destiny

    destiny = _resolve_destiny_by_extension(file_path, config)
    if destiny:
        return destiny

    log.debug("No destination found for file: %s", file_path)
    return None
