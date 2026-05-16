"""
Status Bar Widget.
"""

from textual.widgets import Static
from textual.reactive import reactive


class StatusBar(Static):
    """Status bar widget for displaying connection status."""
    
    status_message: reactive[str] = reactive("Connecting...")
    
    def on_mount(self) -> None:
        """Initialize the status bar."""
        self.update_status("Connecting...")
    
    def update_status(self, message: str) -> None:
        """Update the status message."""
        self.status_message = message
        self.update(f" {message}")
    
    def watch_status_message(self, message: str) -> None:
        """Watch for status message changes."""
        self.update(f" {message}")
