"""
KubeTUI - A modern, fast, and intuitive TUI for Kubernetes cluster management.

Copyright (c) 2026 SOLO Agent
Licensed under MIT License
"""

__version__ = "1.0.0"
__author__ = "SOLO Agent"
__license__ = "MIT"

from kubetui.app import KubeTUI
from kubetui.main import main

__all__ = ["KubeTUI", "main", "__version__"]
