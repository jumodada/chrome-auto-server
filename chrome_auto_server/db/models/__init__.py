"""chrome_auto_server models."""

import pkgutil
from pathlib import Path


def load_all_models() -> None:
    """Load all models from this folder."""
    package_dir = Path(__file__).resolve().parent
    modules = pkgutil.walk_packages(
        path=[str(package_dir)],
        prefix="chrome_auto_server.db.models.",
    )
    for module in modules:
        __import__(module.name)
