import os
import shutil

from watchdog.events import (FileCreatedEvent, FileMovedEvent)

from src.utils import get_path_str


class FileService:
    def __init__(self, extensions_map: dict):
        self.extension_to_dir = extensions_map

    def handle_moved(self, event: FileMovedEvent):
        print(f'{self.__class__.__name__} - handle_moved - Input')
        try:
            src_path: str = get_path_str(event.src_path)
            dest_path: str = get_path_str(event.dest_path)
            print(f'{self.__class__.__name__} - handle_moved - Paths - src: {src_path}, dest: {dest_path}')
            
            src_extension: str = os.path.splitext(src_path)[1].lower()
            dest_extension: str = os.path.splitext(dest_path)[1].lower()
            print(f'{self.__class__.__name__} - handle_moved - Extensions - src: {src_extension}, dest: {dest_extension}')
            
            if src_extension == '.tmp' and dest_extension in self.extension_to_dir.keys():
                print(f'{self.__class__.__name__} - handle_moved - Tratando arquivo: {src_path}')
                dest_final: str = self.extension_to_dir.get(dest_extension.lower())
                self._move_file(dest_path, dest_final)
            
            print(f'{self.__class__.__name__} - handle_moved - Output')
        except Exception as e:
            print(f'{self.__class__.__name__} - handle_moved - Error moving file: {e}')

    def handle_created(self, event: FileCreatedEvent):
        print(f'{self.__class__.__name__} - handle_created - Input')
        try:
            if event.is_directory:
                return
            event: FileCreatedEvent = event
            
            src_path: str = get_path_str(event.src_path)
            extension: str = os.path.splitext(src_path)[1].lower()
            dest_path: str = self.extension_to_dir.get(extension.lower())
            if not dest_path:
                print(f'{self.__class__.__name__} - handle_created - Formato não suportado: {src_path}')
                return
            
            self._move_file(src_path, dest_path)
            
            print(f'{self.__class__.__name__} - handle_created - Output')
        except Exception as e:
            print(f'{self.__class__.__name__} - handle_created - Error moving file: {e}')

    def _move_file(self, src_path: str, destiny: str) -> None:
        try:
            print(f'{self.__class__.__name__} - _move_file - Input - src_path: {src_path}, destiny: {destiny}')
            
            result_file_path: str = os.path.join(destiny, os.path.basename(src_path))
            print(f'{self.__class__.__name__} - _move_file - result_file_path-1: {result_file_path}')
            
            result_file_path: str = os.path.abspath(result_file_path)
            print(f'{self.__class__.__name__} - _move_file - result_file_path-2: {result_file_path}')
            
            if os.path.exists(result_file_path):
                print(f'{self.__class__.__name__} - _move_file - Removing existing file: {result_file_path}')
                os.remove(result_file_path)
                
            file_abs_path = os.path.abspath(src_path)
            destiny_abs_path = os.path.abspath(destiny)

            os.makedirs(destiny, exist_ok=True)
            shutil.move(file_abs_path, destiny_abs_path)
            print(f'{self.__class__.__name__} - _move_file - Output')
        except Exception as e:
            print(f'Exception: {e}, type: {{type(e)}}')