import json
from typing import Any


class Settings:
    def __init__(self, settings_path: str):
        self.settings_path = settings_path

        with open(self.settings_path) as settings_file:
            self.settings = json.load(settings_file)

    def get(self, key: str) -> Any:
        return self.settings[key]

    def modify(self, key: str, new_value: Any):
        self.settings[key] = new_value

    def save(self):
        with open(self.settings_path, "w") as settings_file:
            indent = self.get("jsonFormattingIndent")
            json.dump(self.settings, settings_file, indent=indent)
