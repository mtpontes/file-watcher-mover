import time

from watchdog.events import (FileSystemEventHandler, DirCreatedEvent, FileCreatedEvent, DirMovedEvent, FileMovedEvent)

from src.file_service import FileService


class DirHandler(FileSystemEventHandler):
    def __init__(self, extensions_map: dict):
        self.file_service = FileService(extensions_map)
    
    def on_moved(self, event: DirMovedEvent | FileMovedEvent) -> None:
        time.sleep(1.0)  # Small delay to ensure the file system is updated
        if event.is_directory: return 
        self.file_service.handle_moved(event)
            
    def on_created(self, event: DirCreatedEvent | FileCreatedEvent):
        time.sleep(1.0)  # Small delay to ensure the file system is updated
        if event.is_directory: return 
        self.file_service.handle_created(event)
