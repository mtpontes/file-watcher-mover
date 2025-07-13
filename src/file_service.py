import os
import shutil
from pathlib import Path

from watchdog.events import FileCreatedEvent, FileMovedEvent

from src.config_model import ConfigModel
from src.constants import Constants
from src.log import log
from src.utils import get_path_str, resolve_destiny_path


class FileService:
    def __init__(self, config: ConfigModel) -> None:
        self.config: ConfigModel = config

    def handle_moved(self, event: FileMovedEvent) -> None:
        """Handles file moved events.

        Args:
            event (FileMovedEvent): The file moved event to handle.
        """
        log.info("%s - handle_moved - Input", self.__class__.__name__)
        try:
            src_path: str = get_path_str(event.src_path)
            dest_path: str = get_path_str(event.dest_path)
            log.info("%s - handle_moved - Paths - src: %s, dest: %s", self.__class__.__name__, src_path, dest_path)

            if self._is_temporary_file(dest_path):
                log.warning(
                    "%s - handle_moved - Output - Final file will be temporary. Ignoring event.",
                    self.__class__.__name__,
                )
                return

            if Path(src_path).parent != Path(dest_path).parent:
                log.warning(
                    "%s - handle_moved - Output - Moving files out of the target directory. Ignoring event.",
                    self.__class__.__name__,
                )
                return

            src_extension: str = Path(src_path).suffix.lower()
            if src_extension in Constants.TEMPORARY_FILE_EXTENSIONS.value:
                log.info("%s - handle_moved - handling file: %s", self.__class__.__name__, src_path)
                if not self._process_and_move_file(dest_path):
                    return

            log.info("%s - handle_moved - Output - File moved successfully", self.__class__.__name__)

        except Exception as e:
            log.error("%s - handle_moved - Error moving file: %s", self.__class__.__name__, e)

    def handle_created(self, event: FileCreatedEvent) -> None:
        """
        Handles a created file event.

        Args:
            event (FileCreatedEvent): The created file event.
        """
        log.info("%s - handle_created - Input", self.__class__.__name__)
        try:
            if event.is_directory:
                return

            src_path: str = get_path_str(event.src_path)
            if self._is_temporary_file(src_path):
                log.warning(
                    "%s - handle_created - Output - Temporary file detected: %s",
                    self.__class__.__name__,
                    src_path,
                )
                return

            if not self._process_and_move_file(src_path):
                return

            log.info("%s - handle_created - Output - File moved successfully", self.__class__.__name__)

        except Exception as e:
            log.error("%s - handle_created - Error moving file: %s", self.__class__.__name__, e)

    def move_once(self, targets: list[str]) -> None:
        """
        Function that performs file movement only once.

        :param targets: List of source directories to scan and move.
        :param extension_to_dir_map: Dictionary mapping extensions to target directories.
        """
        for target_dir in targets:
            for root, _, files in os.walk(target_dir):
                for file in files:
                    try:
                        file_path = Path(root) / file
                        self._process_and_move_file(file_path)
                    except Exception as e:
                        log.error("Error moving %s: %s", file_path, e)

    def _is_temporary_file(self, file_path: str) -> bool:
        return any(file_path.endswith(ext) for ext in Constants.TEMPORARY_FILE_EXTENSIONS.value)

    def _process_and_move_file(self, file_path: Path) -> bool:
        """
        Processes a file by resolving its destiny path and moving it if a valid destination is found.

        Args:
            file_path (str): The path of the file to process and move.

        Returns:
            bool: True if the file was successfully moved, False otherwise.
        """
        destiny_path: str | None = resolve_destiny_path(file_path, self.config)
        if not destiny_path:
            log.info(
                "%s - _process_and_move_file - Output - No configuration mapped to file: %s",
                self.__class__.__name__,
                file_path.name,
            )
            return False

        self._move_file(file_path, destiny_path)
        return True

    def _move_file(self, file_path: Path, destiny: str) -> None:
        """
        Moves a file from the source path to the destination path.

        Args:
            src_path (Path): The path of the file to be moved.
            destiny (Path): The path where the file should be moved.

        Returns:
            None
        """
        log.info("%s - _move_file - Input - src_path: %s, destiny: %s", self.__class__.__name__, file_path, destiny)
        base_name: str = file_path.name
        name: str = file_path.stem
        extension: str = file_path.suffix
        result_file_path: Path = (Path(destiny) / base_name).resolve()

        counter = 1
        while Path(result_file_path).exists():
            result_file_path = Path(destiny) / f"{name} ({counter}){extension}"
            result_file_path = result_file_path.resolve()
            counter += 1

        file_absolute_path: str = str(file_path.absolute())
        Path(destiny).mkdir(parents=True, exist_ok=True)
        shutil.move(file_absolute_path, result_file_path)
        log.info("%s - _move_file - Output", self.__class__.__name__)
