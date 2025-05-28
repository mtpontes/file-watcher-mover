from src.file_service import FileService
from watchdog.events import (FileSystemEventHandler, DirCreatedEvent, FileCreatedEvent, DirMovedEvent, FileMovedEvent)


class DirHandler(FileSystemEventHandler):
    def __init__(self, extensions_map: dict):
        self.file_service = FileService(extensions_map)
    
    def on_moved(self, event: DirMovedEvent | FileMovedEvent) -> None:
        if event.is_directory: return 
        self.file_service.handle_moved(event)
            
    def on_created(self, event: DirCreatedEvent | FileCreatedEvent):
        if event.is_directory: return 
        self.file_service.handle_created(event)
