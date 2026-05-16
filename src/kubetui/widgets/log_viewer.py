"""
Log Viewer Widget.
"""

from typing import Optional
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.screen import Screen
from textual.widgets import Static, Button, Header, Footer
from textual.binding import Binding

from kubetui.k8s_client import K8sClient


class LogViewer(Screen):
    """Screen for viewing pod logs."""
    
    BINDINGS = [
        Binding("escape", "close", "Close"),
        Binding("f", "follow", "Follow"),
        Binding("c", "copy", "Copy"),
    ]
    
    def __init__(
        self,
        k8s_client: K8sClient,
        pod_name: str,
        namespace: str,
        container: Optional[str] = None,
        *args,
        **kwargs
    ) -> None:
        """Initialize the log viewer."""
        super().__init__(*args, **kwargs)
        self.k8s_client = k8s_client
        self.pod_name = pod_name
        self.namespace = namespace
        self.container = container
        self._follow_mode = False
    
    def compose(self) -> ComposeResult:
        """Compose the log viewer."""
        yield Header()
        
        with Container(id="log-container"):
            yield Static(
                f"📋 Logs: {self.pod_name} ({self.namespace})",
                id="log-title"
            )
            yield Static(id="log-content")
        
        with Horizontal(id="log-buttons"):
            yield Button("Follow", id="follow-btn", variant="primary")
            yield Button("Copy", id="copy-btn")
            yield Button("Close", id="close-btn", variant="error")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Load logs on mount."""
        self._load_logs()
    
    def _load_logs(self) -> None:
        """Load pod logs."""
        logs = self.k8s_client.get_pod_logs(
            pod_name=self.pod_name,
            namespace=self.namespace,
            container=self.container,
            tail_lines=200,
        )
        
        content = self.query_one("#log-content", Static)
        content.update(logs)
    
    def action_close(self) -> None:
        """Close the log viewer."""
        self.app.pop_screen()
    
    def action_follow(self) -> None:
        """Toggle follow mode."""
        self._follow_mode = not self._follow_mode
        self.app.notify(f"Follow mode: {'ON' if self._follow_mode else 'OFF'}")
    
    def action_copy(self) -> None:
        """Copy logs to clipboard."""
        content = self.query_one("#log-content", Static)
        try:
            import pyperclip
            pyperclip.copy(str(content.renderable))
            self.app.notify("📋 Logs copied to clipboard!")
        except Exception:
            self.app.notify("Failed to copy logs", severity="error")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "close-btn":
            self.action_close()
        elif event.button.id == "follow-btn":
            self.action_follow()
        elif event.button.id == "copy-btn":
            self.action_copy()
