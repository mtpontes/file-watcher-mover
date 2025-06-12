import sys, os

from src.file_service import FileService
from watchdog.observers import Observer

from src.handler import DirHandler
from src.config import load_extension_mapping, get_targets, get_extensions_map
from src.utils import display_start_message


def run():
    configs: dict = load_extension_mapping()
    targets: list[str] = get_targets(configs)
    extension_to_dir_map: dict = get_extensions_map(configs)
    
    if "--once" in sys.argv:
        move_once(targets, extension_to_dir_map)
        return
    
    display_start_message(configs)
    event_handler = DirHandler(extension_to_dir_map)
    start_observer(targets, event_handler)

def move_once(targets: list[str], extension_to_dir_map: dict):
    """
    Função que realiza a movimentação de arquivos uma única vez.

    :param targets: Lista de diretórios de origem para verificação e movimentação.
    :param extension_to_dir_map: Dicionário mapeando extensões para diretórios de destino.
    """

    file_service = FileService(extension_to_dir_map)
    for target_dir in targets:
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                file_path = os.path.join(root, file)
                ext = os.path.splitext(file)[1].lower()
                dest_dir = extension_to_dir_map.get(ext)
                if dest_dir:
                    try:
                        file_service.move_file(file_path, dest_dir)
                    except Exception as e:
                        print(f"Erro ao mover {file_path}: {e}")

def start_observer(targets: list[str], handler: DirHandler):
    observer = Observer()
    for target_dir in targets:
        observer.schedule(event_handler=handler, path=target_dir)
    observer.start()
    try:
        while observer.is_alive():
            observer.join(1)
    finally:
        observer.stop()
        observer.join()

if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        print(e)