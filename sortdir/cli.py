import logging
import os
import time
from pathlib import Path
from typing import Dict, List

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

from sortdir.config import Config
from sortdir.sorting import SortableDirectory, SortingEventHandler
from sortdir.utils import print_error


def run():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # set up observer
    observer = Observer()

    try:
        config = Config()
    except FileNotFoundError:
        print_error("Config file does not exist")
        return
    directories: Dict[str, Dict] = config["directories"]

    directories_to_watch = []
    for path in directories:
        expanded_path = Path(path).expanduser()
        if not os.path.isdir(expanded_path):
            print_error(f"Directory '{path}' does not exist")
            continue

        directories_to_watch.append(path)

        directory_to_extensions: Dict[str, List[str]] = directories[path]
        extension_to_directory: Dict[str, str] = {
            pat: dir_
            for dir_, patterns in directory_to_extensions.items()
            for pat in patterns
        }

        # sort directory
        SortableDirectory(extension_to_directory, expanded_path).sort()

        logging_event_handler = LoggingEventHandler()
        sorting_event_handler = SortingEventHandler(extension_to_directory)

        observer.schedule(logging_event_handler, expanded_path, recursive=False)
        observer.schedule(sorting_event_handler, expanded_path, recursive=False)

    # wait for events
    if directories_to_watch:
        stringified_directories: str = ",\n".join(directories_to_watch)
        print(
            f"Watching for changes in following directories:\n{stringified_directories}",
            end="\n\n",
        )

        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping server...")
            observer.stop()
        observer.join()


if __name__ == "__main__":
    run()
