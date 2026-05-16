"""
Context Selector Widget.
"""

from typing import Callable
from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Static, ListView, ListItem, Label, Header, Footer
from textual.binding import Binding

from kubetui.k8s_client import ContextInfo


class ContextSelector(Screen):
    """Screen for selecting a Kubernetes context."""
    
    BINDINGS = [
        Binding("escape", "close", "Close"),
        Binding("enter", "select", "Select"),
    ]
    
    def __init__(
        self,
        contexts: list[ContextInfo],
        on_select: Callable[[str], None],
        *args,
        **kwargs
    ) -> None:
        """Initialize the context selector."""
        super().__init__(*args, **kwargs)
        self.contexts = contexts
        self._on_select = on_select
    
    def compose(self) -> ComposeResult:
        """Compose the context selector."""
        yield Header()
        
        with Container(id="context-container"):
            yield Static("🔗 Select Context", id="context-title")
            
            with ListView(id="context-list"):
                for ctx in self.contexts:
                    marker = "✓ " if ctx.is_current else "  "
                    yield ListItem(Label(
                        f"{marker}{ctx.name} ({ctx.cluster})"
                    ))
        
        yield Footer()
    
    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle context selection."""
        index = event.list_view.index
        if index is not None and 0 <= index < len(self.contexts):
            selected = self.contexts[index]
            self._on_select(selected.name)
            self.app.pop_screen()
    
    def action_close(self) -> None:
        """Close the selector."""
        self.app.pop_screen()
    
    def action_select(self) -> None:
        """Select the highlighted context."""
        list_view = self.query_one(ListView)
        if list_view.index is not None:
            self.on_list_view_selected(ListView.Selected(list_view))
