import os
import logging
import time

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

from sortdir import perform_initial_sorting, schedule_sorting_handler
from sortdir.config import config as parse_config
from sortdir.utils import print_error


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# set up observer
observer = Observer()

logging_event_handler = LoggingEventHandler()

config = parse_config()
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
    perform_initial_sorting(extension_to_directory, path)

    observer.schedule(logging_event_handler, path, recursive=False)
    schedule_sorting_handler(observer, extension_to_directory, path)

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
    finally:
        observer.stop()
        observer.join()
