import logging
import os
import time

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

from sortdir.config import Config
from sortdir.sorting import SortableDirectory, SortingEventHandler
from sortdir.utils import print_error


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
directories = config["directories"]

directories_to_watch = []
for path in directories:
    if not os.path.isdir(path):
        print_error(f"Directory '{path}' does not exist")
        continue

    directories_to_watch.append(path)

    directory_to_extensions = directories[path]
    extension_to_directory = {
        pat: ext
        for ext, patterns in directory_to_extensions.items()
        for pat in patterns
    }

    # sort directory
    SortableDirectory(extension_to_directory, path).sort()

    logging_event_handler = LoggingEventHandler()
    sorting_event_handler = SortingEventHandler(extension_to_directory)

    observer.schedule(logging_event_handler, path, recursive=False)
    observer.schedule(sorting_event_handler, path, recursive=False)

# wait for events
if directories_to_watch:
    stringified_directories = ",\n".join(directories_to_watch)
    print(
        f"Watching for changes in following directories:\n{stringified_directories}",
        end="\n\n",
    )

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
