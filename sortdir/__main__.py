import logging
import sys
import time

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

from sortdir import perform_initial_sorting, schedule_sorting_handler


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
path = sys.argv[1] if len(sys.argv) > 1 else "."

directory_to_extensions = {
    "documents": {
        ".doc",
        ".docx",
        ".ods",
        ".odt",
        ".pdf",
        ".ppt",
        ".pptx",
        ".txt",
        ".xls",
        ".xlsx",
    },
    "images": {".gif", ".png", ".jpeg", ".jpg"},
}
extension_to_directory = {
    pat: ext
    for ext, patterns in directory_to_extensions.items()
    for pat in patterns
}

# sort directory
perform_initial_sorting(extension_to_directory, path)

# set up observer
observer = Observer()

logging_event_handler = LoggingEventHandler()
observer.schedule(logging_event_handler, path, recursive=False)
schedule_sorting_handler(observer, extension_to_directory, path)

# wait for events
observer.start()
try:
    while True:
        time.sleep(1)
finally:
    observer.stop()
    observer.join()
