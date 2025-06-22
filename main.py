from dataclasses import asdict
import sys

from watchdog.observers import Observer

from src.handler import DirHandler
from src.file_service import FileService
from src.config_model import ConfigModel
from src.utils import config_loader, display_start_message
from src.log import log

def run():
    configs: dict = config_loader()    
    config = ConfigModel(configs)
    file_service = FileService(config)
    targets: list[str] = [*config.extension_config.targets, *config.pattern_config.targets]
    
    if "--once" in sys.argv:
        file_service.move_once(targets)
        return

    display_start_message(asdict(config))
    event_handler = DirHandler(file_service)

    start_observer(targets, event_handler)

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
        log.error(e)