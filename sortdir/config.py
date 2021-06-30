import os
from pathlib import Path

import toml

from sortdir.utils import print_error


def config_path():
    possible_paths = [
        os.path.join(Path.home(), p)
        for p in (
            ".sortdir.toml",
            os.path.join(".config", "sortdir", "config.toml"),
        )
    ]

    for p in possible_paths:
        if os.path.isfile(p):
            return p

    raise FileNotFoundError("config file does not exist")


def config():
    try:
        file_path = config_path()

        with open(file_path) as f:
            return toml.loads(f.read())
    except FileNotFoundError:
        print_error("Config file does not exist")


if __name__ == "__main__":
    print(config())
