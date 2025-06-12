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
            
            download_in_progress_extensions: list[str] = ['.tmp', '.crdownload', '.part', '.download']
            if (src_extension in download_in_progress_extensions) and dest_extension in self.extension_to_dir.keys():
                print(f'{self.__class__.__name__} - handle_moved - Tratando arquivo: {src_path}')
                dest_final: str = self.extension_to_dir.get(dest_extension.lower())
                self.move_file(dest_path, dest_final)
            
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
                print(f'{self.__class__.__name__} - handle_created - Format not supported: {src_path}')
                return
            
            self.move_file(src_path, dest_path)
            
            print(f'{self.__class__.__name__} - handle_created - Output')
        except Exception as e:
            print(f'{self.__class__.__name__} - handle_created - Error moving file: {e}')

    def move_file(self, src_path: str, destiny: str) -> None:
        print(f'{self.__class__.__name__} - _move_file - Input - src_path: {src_path}, destiny: {destiny}')
        try:
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
            print(f'{self.__class__.__name__} - _move_file - Output')
        except Exception as e:
            print(f'Exception: {e}, type: {{type(e)}}')