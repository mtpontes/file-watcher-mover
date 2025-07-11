import sys
from dataclasses import asdict

from watchdog.observers import Observer

from src.config_model import ConfigModel
from src.file_service import FileService
from src.handler import DirHandler
from src.log import log
from src.utils import config_loader, display_start_message


def run():
    """
    Main function that initializes and runs the file monitoring service.

    This function loads the configuration, creates a FileService instance, and determines
    whether to run in single-execution mode (--once flag) or continuous monitoring mode.
    In continuous mode, it sets up file system observers to monitor specified directories
    for file changes.

    Command line arguments:
        --once: If present, performs a one-time file organization of existing files
                and exits. Otherwise, runs in continuous monitoring mode.

    Raises:
        Exception: Any exception during configuration loading, service initialization,
                  or observer setup will be propagated to the caller.
    """
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
    """
    Starts and manages file system observers for monitoring specified directories.

    This function creates a watchdog Observer instance, schedules it to monitor
    all target directories using the provided event handler, and runs the observer
    in a continuous loop until interrupted. It ensures proper cleanup by stopping
    and joining the observer thread when the monitoring ends.

    Args:
        targets (list[str]): List of directory paths to monitor for file system events.
        handler (DirHandler): Event handler instance that will process file system events
                            (created, moved, modified, deleted) in the monitored directories.

    Note:
        This function runs indefinitely until the process is interrupted (Ctrl+C)
        or the observer encounters an error. The observer thread is properly cleaned
        up in the finally block to prevent resource leaks.

    Raises:
        Exception: Any exception from the observer setup or monitoring will be
                  propagated after proper cleanup.
    """
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
