"""Configuration management for Hancock."""

import os
import yaml
from pathlib import Path
from typing import Optional, Dict


class Config:
    """Manages Hancock configuration."""

    def __init__(self):
        self.config_dir = Path.home() / ".hancock"
        self.config_file = self.config_dir / "config.yaml"
        self._data = None

    def exists(self) -> bool:
        """Check if config file exists."""
        return self.config_file.exists()

    def load(self) -> Dict:
        """Load configuration from file."""
        if not self.exists():
            return {}

        with open(self.config_file, 'r') as f:
            self._data = yaml.safe_load(f) or {}
        return self._data

    def save(self, data: Dict):
        """Save configuration to file."""
        # Create config directory if it doesn't exist
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # Save config
        with open(self.config_file, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)

        self._data = data

    def get(self, key: str, default=None):
        """Get a configuration value."""
        if self._data is None:
            self.load()
        return self._data.get(key, default)

    def set(self, key: str, value):
        """Set a configuration value."""
        if self._data is None:
            self.load()
        self._data[key] = value
        self.save(self._data)

    def get_service_account_path(self) -> Optional[Path]:
        """Get the path to the service account JSON file."""
        path_str = self.get('service_account_file')
        if not path_str:
            return None

        path = Path(path_str).expanduser()
        if path.exists():
            return path
        return None

    def get_admin_email(self) -> Optional[str]:
        """Get the admin email."""
        return self.get('admin_email')

    def is_configured(self) -> bool:
        """Check if Hancock is fully configured."""
        return (
            self.exists() and
            self.get_service_account_path() is not None and
            self.get_admin_email() is not None
        )

    def get_config_path(self) -> Path:
        """Get the path to the config file."""
        return self.config_file


# Global config instance
_config = Config()


def get_config() -> Config:
    """Get the global config instance."""
    return _config
