from importlib.metadata import PackageNotFoundError, version

from vex.config import VexConfig
from vex.exceptions import ConfigurationError, VexBlockError
from vex.guard import Session, Vex
from vex.models import ConversationTurn, VexResult

__all__ = [
    "Vex",
    "VexBlockError",
    "ConfigurationError",
    "ConversationTurn",
    "VexConfig",
    "VexResult",
    "Session",
]

try:
    __version__ = version("vex-sdk")
except PackageNotFoundError:
    # Running from source without installing (e.g. editable dev install)
    __version__ = "0.0.0-dev"
