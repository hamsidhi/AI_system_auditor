import json
import os
from pathlib import Path

class KeyManager:
    """Handles secure storage and retrieval of API keys."""

    def __init__(self, config_file="config/key.json"):
        self.config_path = Path(config_file)
        self.ensure_config_dir()

    def ensure_config_dir(self):
        """Ensures the configuration directory exists."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

    def save_key(self, key):
        """Saves the API key to a local JSON file."""
        with open(self.config_path, "w") as f:
            json.dump({"groq_api_key": key}, f)

    def get_key(self):
        """Retrieves the API key from the local JSON file or environment variable."""
        # 1. Try environment variable first
        env_key = os.environ.get("GROQ_API_KEY")
        if env_key:
            return env_key

        # 2. Try config file
        if self.config_path.exists():
            try:
                with open(self.config_path, "r") as f:
                    config = json.load(f)
                    return config.get("groq_api_key")
            except Exception:
                return None
        return None

    def clear_key(self):
        """Removes the stored API key."""
        if self.config_path.exists():
            self.config_path.unlink()
