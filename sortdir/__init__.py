import os
import shutil

from watchdog.events import PatternMatchingEventHandler


def move_file(filepath, extension_to_directory, path):
    _, ext = os.path.splitext(filepath)
    directory_name = extension_to_directory[ext.lower()]
    directory_path = os.path.join(path, directory_name)

    if not os.path.isdir(directory_path):
        os.mkdir(directory_path)

    return shutil.move(filepath, directory_path)


def perform_initial_sorting(extension_to_directory, path):
    for filename in os.listdir(path):
        _, ext = os.path.splitext(filename)
        filepath = os.path.join(path, filename)

        if os.path.isfile(filepath) and ext.lower() in extension_to_directory:
            move_file(filepath, extension_to_directory, path)


def schedule_sorting_handler(observer, extension_to_directory, path):
    pattern_matching_event_handler = PatternMatchingEventHandler(
        patterns=[f"*{ext}" for ext in extension_to_directory.keys()]
    )
    pattern_matching_event_handler.on_created = lambda e: move_file(
        e.src_path, extension_to_directory, path
    )

    observer.schedule(pattern_matching_event_handler, path, recursive=False)

    return observer
