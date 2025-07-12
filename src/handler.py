import time

from watchdog.events import DirCreatedEvent, DirMovedEvent, FileCreatedEvent, FileMovedEvent, FileSystemEventHandler

from src.file_service import FileService


class DirHandler(FileSystemEventHandler):
    def __init__(self, file_service: FileService) -> None:
        self.file_service = file_service

    def on_moved(self, event: DirMovedEvent | FileMovedEvent) -> None:
        time.sleep(0.5)  # Small delay to ensure the file system is updated
        if event.is_directory:
            return
        self.file_service.handle_moved(event)

    def on_created(self, event: DirCreatedEvent | FileCreatedEvent) -> None:
        time.sleep(0.5)  # Small delay to ensure the file system is updated
        if event.is_directory:
            return
        self.file_service.handle_created(event)
