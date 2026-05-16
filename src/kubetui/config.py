"""
Configuration management for KubeTUI.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
import yaml


@dataclass
class Config:
    """Application configuration."""
    
    # Refresh interval in seconds
    refresh_interval: float = 2.0
    
    # Default namespace
    default_namespace: str = "default"
    
    # Log lines to show
    log_lines: int = 100
    
    # Theme
    theme: str = "dark"
    
    # Show system namespaces
    show_system_namespaces: bool = False
    
    # Favorite namespaces
    favorite_namespaces: list[str] = field(default_factory=lambda: ["default", "kube-system"])
    
    # Favorite contexts
    favorite_contexts: list[str] = field(default_factory=list)
    
    @classmethod
    def load(cls, config_path: Optional[Path] = None) -> "Config":
        """Load configuration from file."""
        if config_path is None:
            config_path = Path.home() / ".config" / "kubetui" / "config.yaml"
        
        if not config_path.exists():
            return cls()
        
        try:
            with open(config_path, "r") as f:
                data = yaml.safe_load(f) or {}
            
            return cls(
                refresh_interval=data.get("refresh_interval", 2.0),
                default_namespace=data.get("default_namespace", "default"),
                log_lines=data.get("log_lines", 100),
                theme=data.get("theme", "dark"),
                show_system_namespaces=data.get("show_system_namespaces", False),
                favorite_namespaces=data.get("favorite_namespaces", ["default", "kube-system"]),
                favorite_contexts=data.get("favorite_contexts", []),
            )
        except Exception:
            return cls()
    
    def save(self, config_path: Optional[Path] = None) -> None:
        """Save configuration to file."""
        if config_path is None:
            config_path = Path.home() / ".config" / "kubetui" / "config.yaml"
        
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            "refresh_interval": self.refresh_interval,
            "default_namespace": self.default_namespace,
            "log_lines": self.log_lines,
            "theme": self.theme,
            "show_system_namespaces": self.show_system_namespaces,
            "favorite_namespaces": self.favorite_namespaces,
            "favorite_contexts": self.favorite_contexts,
        }
        
        with open(config_path, "w") as f:
            yaml.dump(data, f, default_flow_style=False)
