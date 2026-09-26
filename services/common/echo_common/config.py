from pathlib import Path

import yaml


def load_cfg(path, missing_ok=False):
    """Read a yaml config file into a dict."""
    p = Path(path)

    if missing_ok and not p.exists():
        return {}

    return yaml.safe_load(p.read_text(encoding="utf-8")) or {}
