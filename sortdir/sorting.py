import os
from pathlib import Path
from typing import Dict, Union

from watchdog.events import PatternMatchingEventHandler


class SortableDirectory:
    def __init__(
        self, extension_to_directory: Dict[str, str], path: Union[Path, str]
    ):
        self.extension_to_directory = extension_to_directory
        self.path = path.expanduser() if isinstance(path, Path) else path

    def move_file(self, filepath):
        """
        Move directory file to its place, defined in extension_to_directory
        """

        filename = os.path.basename(filepath)
        _, ext = os.path.splitext(filename)
        directory_name = self.extension_to_directory[ext.lower()]
        directory_path = os.path.join(self.path, directory_name)
        destination_path = os.path.join(directory_path, filename)

        # create directory if it does not exist
        if not os.path.isdir(directory_path):
            os.mkdir(directory_path)

        # check if file is already copied to its destination
        # by other thread
        if not os.path.isfile(filepath) and os.path.isfile(destination_path):
            return

        # remove file on destination path if it already exists
        if os.path.isfile(filepath) and os.path.isfile(destination_path):
            os.remove(destination_path)

        return os.rename(filepath, destination_path)

    def sort(self):
        """
        Sort directory
        """

        for filename in os.listdir(self.path):
            _, ext = os.path.splitext(filename)
            filepath = os.path.join(self.path, filename)

            if (
                os.path.isfile(filepath)
                and ext.lower() in self.extension_to_directory
            ):
                self.move_file(filepath)


class SortingEventHandler(PatternMatchingEventHandler):
    def __init__(self, extension_to_directory, *args, **kwargs):
        patterns = [f"*{ext}" for ext in extension_to_directory.keys()]
        super().__init__(patterns, *args, **kwargs)

        self.extension_to_directory = extension_to_directory

    def on_created(self, event):
        super().on_created(event)

        SortableDirectory(
            self.extension_to_directory, Path(event.src_path).parent.absolute()
        ).move_file(event.src_path)
