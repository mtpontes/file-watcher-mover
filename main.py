from watchdog.observers import Observer

from src.handler import DirHandler
from src.config import load_extension_mapping, get_targets, get_extensions_map
from src.utils import display_start_message


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

def run():
    configs: dict = load_extension_mapping()
    targets: list[str] = get_targets(configs)
    extension_to_dir_map: dict = get_extensions_map(configs)
    display_start_message(configs)
    event_handler = DirHandler(extension_to_dir_map)
    start_observer(targets, event_handler)

if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        print(e)