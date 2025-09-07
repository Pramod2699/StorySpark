from pathlib import Path
import json


class ConfigHelper:
    """Helper class for managing configuration settings from JSON file."""

    def __init__(self):
        """Initialize ConfigHelper with configuration from JSON file.

        The configuration file is expected to be in the config/config.json
        relative to the project root directory.
        """
        current_dir = Path(__file__).parent
        self.project_root = current_dir.parent.parent
        self.config_file_path = self.project_root / "src" / "config" / "config.json"

        try:
            with open(self.config_file_path) as file:
                self.config = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Configuration file not found at {self.config_file_path}"
            )
        except json.JSONDecodeError:
            raise ValueError(
                f"Invalid JSON format in configuration file at {self.config_file_path}"
            )
