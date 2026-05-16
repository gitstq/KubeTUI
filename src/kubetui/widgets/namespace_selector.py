"""
Namespace Selector Widget.
"""

from typing import Callable, Optional
from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Static, ListView, ListItem, Label, Header, Footer
from textual.binding import Binding


class NamespaceSelector(Screen):
    """Screen for selecting a namespace."""
    
    BINDINGS = [
        Binding("escape", "close", "Close"),
        Binding("enter", "select", "Select"),
    ]
    
    def __init__(
        self,
        namespaces: list[str],
        current: str,
        on_select: Callable[[str], None],
        *args,
        **kwargs
    ) -> None:
        """Initialize the namespace selector."""
        super().__init__(*args, **kwargs)
        self.namespaces = namespaces
        self.current = current
        self._on_select = on_select
    
    def compose(self) -> ComposeResult:
        """Compose the namespace selector."""
        yield Header()
        
        with Container(id="namespace-container"):
            yield Static("📁 Select Namespace", id="namespace-title")
            yield Static(f"Current: {self.current}", id="namespace-current")
            
            with ListView(id="namespace-list"):
                for ns in self.namespaces:
                    marker = "✓ " if ns == self.current else "  "
                    yield ListItem(Label(f"{marker}{ns}"))
        
        yield Footer()
    
    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle namespace selection."""
        index = event.list_view.index
        if index is not None and 0 <= index < len(self.namespaces):
            selected = self.namespaces[index]
            self._on_select(selected)
            self.app.pop_screen()
    
    def action_close(self) -> None:
        """Close the selector."""
        self.app.pop_screen()
    
    def action_select(self) -> None:
        """Select the highlighted namespace."""
        list_view = self.query_one(ListView)
        if list_view.index is not None:
            self.on_list_view_selected(ListView.Selected(list_view))
