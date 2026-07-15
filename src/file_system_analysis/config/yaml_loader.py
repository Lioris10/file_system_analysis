"""YAML configuration loading."""

from __future__ import annotations

from pathlib import Path

from file_system_analysis.config.settings import AppSettings
from file_system_analysis.domain.exceptions import ConfigurationError


DEFAULT_CONFIG_PATH = Path("config/config.example.yaml")


def load_settings(path: Path | str = DEFAULT_CONFIG_PATH) -> AppSettings:
    """Load application settings from a YAML file."""
    config_path = Path(path)
    if not config_path.exists():
        raise ConfigurationError(f"Configuration file not found: {config_path}")

    try:
        import yaml
    except ImportError as exc:  # pragma: no cover - environment dependent
        if config_path == DEFAULT_CONFIG_PATH:
            return AppSettings()
        raise ConfigurationError("PyYAML is required to load YAML configuration") from exc

    with config_path.open("r", encoding="utf-8") as config_file:
        data = yaml.safe_load(config_file) or {}

    if not isinstance(data, dict):
        raise ConfigurationError("YAML configuration root must be a mapping")
    return AppSettings.from_mapping(data)
