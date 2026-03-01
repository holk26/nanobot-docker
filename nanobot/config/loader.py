"""Configuration loading utilities."""

import json
import os
from pathlib import Path

from nanobot.config.schema import Config


def get_config_path() -> Path:
    """Get the default configuration file path."""
    return Path.home() / ".nanobot" / "config.json"


def get_data_dir() -> Path:
    """Get the nanobot data directory."""
    from nanobot.utils.helpers import get_data_path
    return get_data_path()


def load_config(config_path: Path | None = None) -> Config:
    """
    Load configuration from file or create default.

    Environment variables for providers (e.g. ANTHROPIC_API_KEY, OPENAI_API_KEY)
    are applied automatically when not already set in the config file.
    NANOBOT_PROVIDERS__<PROVIDER>__API_KEY env vars are also supported via
    pydantic-settings when no config file is present.

    Args:
        config_path: Optional path to config file. Uses default if not provided.

    Returns:
        Loaded configuration object.
    """
    path = config_path or get_config_path()

    data: dict = {}
    if path.exists():
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            data = _migrate_config(data)
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Warning: Failed to load config from {path}: {e}")
            print("Using default configuration.")
            data = {}

    data = _apply_provider_env_vars(data)
    return Config.model_validate(data)


def _apply_provider_env_vars(data: dict) -> dict:
    """
    Inject standard provider env vars (e.g. ANTHROPIC_API_KEY) into config data.

    Only fills in providers that are not already configured in the data dict,
    so explicit config file values always take precedence.
    """
    from nanobot.providers.registry import PROVIDERS

    providers = dict(data.get("providers", {}))
    changed = False

    for spec in PROVIDERS:
        if not spec.env_key:
            continue
        env_val = os.environ.get(spec.env_key)
        if not env_val:
            continue
        provider_data = dict(providers.get(spec.name, {}))
        # Don't override if already explicitly set (accepts both camelCase and snake_case)
        if not provider_data.get("apiKey") and not provider_data.get("api_key"):
            provider_data["apiKey"] = env_val
            providers[spec.name] = provider_data
            changed = True

    if changed:
        return {**data, "providers": providers}
    return data


def save_config(config: Config, config_path: Path | None = None) -> None:
    """
    Save configuration to file.

    Args:
        config: Configuration to save.
        config_path: Optional path to save to. Uses default if not provided.
    """
    path = config_path or get_config_path()
    path.parent.mkdir(parents=True, exist_ok=True)

    data = config.model_dump(by_alias=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _migrate_config(data: dict) -> dict:
    """Migrate old config formats to current."""
    # Move tools.exec.restrictToWorkspace → tools.restrictToWorkspace
    tools = data.get("tools", {})
    exec_cfg = tools.get("exec", {})
    if "restrictToWorkspace" in exec_cfg and "restrictToWorkspace" not in tools:
        tools["restrictToWorkspace"] = exec_cfg.pop("restrictToWorkspace")
    return data
