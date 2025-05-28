from watchdog.observers import Observer

from src.handler import DirHandler
from src.config import load_extension_mapping


def run():
    configs: dict = load_extension_mapping()
    targets: list[str] = get_targets(configs)
    extension_to_dir_map: dict = get_extensions_map(configs)
    
    event_handler = DirHandler(extension_to_dir_map)
    observer = Observer()
    
    for target_dir in targets:
        observer.schedule(event_handler=event_handler, path=target_dir)
        
    observer.start()
    try:
        while observer.is_alive():
            observer.join(1)
    finally:
        observer.stop()
        observer.join()
        
def get_targets(configs: dict) -> list[str]:
    targets: list[str] = configs.get("targets")
    if not targets:
        raise ValueError("TARGETS environment variable is not set or empty.")
    return targets

def get_extensions_map(configs: dict) -> dict:
    extension_map: dict = configs.get("extension")
    if not extension_map:
        raise ValueError("TARGETS environment variable is not set or empty.")
    return extension_map

if __name__ == "__main__":
    run()