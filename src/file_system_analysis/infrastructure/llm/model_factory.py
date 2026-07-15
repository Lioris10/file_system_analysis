"""LangChain chat model factory.

The MVP does not require a live LLM call, but this factory establishes the provider-neutral
integration point that later graph nodes can use.
"""

from __future__ import annotations

import importlib
import os
from typing import Any

from file_system_analysis.config.settings import LlmSettings
from file_system_analysis.domain.exceptions import ConfigurationError


class ModelFactory:
    """Create LangChain chat model instances from YAML-driven settings."""

    def __init__(self, settings: LlmSettings) -> None:
        self.settings = settings

    def create(self) -> Any:
        """Instantiate the configured LangChain chat model.

        Imports are intentionally lazy so the application can still run the local MVP
        pipeline when optional provider packages are not installed.
        """
        provider_config = self.settings.providers.get(self.settings.provider)
        if not provider_config:
            raise ConfigurationError(f"Unknown LLM provider: {self.settings.provider}")

        class_path = provider_config.get("class")
        if not class_path or "." not in class_path:
            raise ConfigurationError(f"Provider {self.settings.provider} must define a class path")

        module_name, class_name = class_path.rsplit(".", 1)
        try:
            module = importlib.import_module(module_name)
        except ImportError as exc:
            raise ConfigurationError(f"Provider package is not installed for {self.settings.provider}: {module_name}") from exc
        model_class = getattr(module, class_name)

        kwargs: dict[str, Any] = {
            "model": self.settings.model_name,
            "temperature": self.settings.temperature,
            "timeout": self.settings.timeout_seconds,
            "max_retries": self.settings.max_retries,
        }
        api_key_env = provider_config.get("api_key_env") or self.settings.api_key_env
        if api_key_env and os.getenv(api_key_env):
            kwargs["api_key"] = os.environ[api_key_env]
        if self.settings.provider == "bedrock":
            kwargs = self._bedrock_kwargs(provider_config, kwargs)
        if provider_config.get("base_url"):
            kwargs["base_url"] = provider_config["base_url"]
        kwargs.update(provider_config.get("model_kwargs", {}) or {})
        return model_class(**kwargs)

    def _bedrock_kwargs(self, provider_config: dict[str, Any], kwargs: dict[str, Any]) -> dict[str, Any]:
        bedrock_kwargs = dict(kwargs)
        bedrock_kwargs["model_id"] = bedrock_kwargs.pop("model")
        region_env = provider_config.get("region_name_env")
        profile_env = provider_config.get("profile_name_env")
        if region_env and os.getenv(region_env):
            bedrock_kwargs["region_name"] = os.environ[region_env]
        if profile_env and os.getenv(profile_env):
            bedrock_kwargs["credentials_profile_name"] = os.environ[profile_env]
        return bedrock_kwargs
