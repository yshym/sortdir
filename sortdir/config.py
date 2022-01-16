import os
from pathlib import Path

import toml


class Config:
    def __init__(self):
        possible_paths = [
            Path("~/.sortdir.toml").expanduser(),
            Path("~/.config/sortdir/config.toml").expanduser(),
        ]

        # use first existent path
        self.path = None
        for path in possible_paths:
            if os.path.isfile(path):
                self.path = path

        if not self.path:
            raise FileNotFoundError("config file does not exist")

        with open(self.path) as f:
            self.dict_ = toml.load(f)

    def __getitem__(self, key):
        return self.dict_[key]
