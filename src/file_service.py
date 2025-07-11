import os
import shutil

from watchdog.events import FileCreatedEvent, FileMovedEvent

from src.config_model import ConfigModel
from src.constants import Constants
from src.log import log
from src.utils import get_path_str, resolve_destiny_path


class FileService:
    def __init__(self, config: ConfigModel):
        self.config: ConfigModel = config

    def handle_moved(self, event: FileMovedEvent):
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

            if os.path.dirname(src_path) != os.path.dirname(dest_path):
                log.warning(
                    "%s - handle_moved - Output - Moving files out of the target directory. Ignoring event.",
                    self.__class__.__name__,
                )
                return

            src_extension: str = os.path.splitext(src_path)[1].lower()
            if src_extension in Constants.TEMPORARY_FILE_EXTENSIONS.value:
                log.info("%s - handle_moved - handling file: %s", self.__class__.__name__, src_path)
                if not self._process_and_move_file(dest_path):
                    return

            log.info("%s - handle_moved - Output - File moved successfully", self.__class__.__name__)

        except Exception as e:
            log.error("%s - handle_moved - Error moving file: %s", self.__class__.__name__, e)

    def handle_created(self, event: FileCreatedEvent):
        """
        Handles a created file event.

        Args:
            event (FileCreatedEvent): The created file event.
        """
        log.info("%s - handle_created - Input", self.__class__.__name__)
        try:
            if event.is_directory:
                return
            event: FileCreatedEvent = event

            src_path: str = get_path_str(event.src_path)
            if self._is_temporary_file(src_path):
                log.warning(
                    "%s - handle_created - Output - Temporary file detected: %s", self.__class__.__name__, src_path,
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
                        file_path = os.path.join(root, file)
                        self._process_and_move_file(file_path)
                    except Exception as e:
                        log.error("Error moving %s: %s", file_path, e)

    def _is_temporary_file(self, file_path: str) -> bool:
        for temp_extension in Constants.TEMPORARY_FILE_EXTENSIONS.value:
            if file_path.endswith(temp_extension):
                return True
        return False

    def _process_and_move_file(self, file_path: str) -> bool:
        """
        Processes a file by resolving its destiny path and moving it if a valid destination is found.

        Args:
            file_path (str): The path of the file to process and move.

        Returns:
            bool: True if the file was successfully moved, False otherwise.
        """
        file_name: str = os.path.basename(file_path)
        destiny_path: str | None = resolve_destiny_path(file_name, self.config)

        if not destiny_path:
            log.warning(
                "%s - _process_and_move_file - Output - No configuration mapped to file: %s",
                self.__class__.__name__,
                file_name,
            )
            return False

        self._move_file(file_path, destiny_path)
        return True

    def _move_file(self, src_path: str, destiny: str) -> None:
        """
        Moves a file from the source path to the destination path.

        Args:
            src_path (str): The path of the file to be moved.
            destiny (str): The path where the file should be moved.

        Returns:
            None
        """
        log.info("%s - _move_file - Input - src_path: %s, destiny: %s", self.__class__.__name__, src_path, destiny)
        base_name = os.path.basename(src_path)
        name, ext = os.path.splitext(base_name)
        result_file_path = os.path.join(destiny, base_name)
        result_file_path = os.path.abspath(result_file_path)

        counter = 1
        while os.path.exists(result_file_path):
            result_file_path = os.path.join(destiny, f"{name} ({counter}){ext}")
            result_file_path = os.path.abspath(result_file_path)
            counter += 1

        file_abs_path = os.path.abspath(src_path)
        os.makedirs(destiny, exist_ok=True)
        shutil.move(file_abs_path, result_file_path)
        log.info("%s - _move_file - Output", self.__class__.__name__)
