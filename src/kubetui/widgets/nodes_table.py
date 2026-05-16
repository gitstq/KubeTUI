"""
Nodes Table Widget.
"""

from typing import Optional
from textual.widgets import DataTable

from kubetui.k8s_client import NodeInfo


class NodesTable(DataTable):
    """Table widget for displaying nodes."""
    
    def __init__(self, id: Optional[str] = None) -> None:
        """Initialize the nodes table."""
        super().__init__(id=id)
        self._nodes: list[NodeInfo] = []
    
    def on_mount(self) -> None:
        """Set up the table on mount."""
        self.add_columns(
            "Name", "Status", "Roles", "Version", "IP", "OS", "Age"
        )
        self.cursor_type = "row"
        self.zebra_stripes = True
    
    def update_data(self, nodes: list[NodeInfo]) -> None:
        """Update the table with new node data."""
        self._nodes = nodes
        self.clear()
        
        for node in nodes:
            # Color based on status
            status_style = "green" if node.status == "Ready" else "red"
            
            self.add_row(
                node.name,
                (node.status, status_style),
                node.roles,
                node.version,
                node.ip,
                node.os[:20] + "..." if len(node.os) > 20 else node.os,
                node.age,
            )
    
    def get_selected_node(self) -> Optional[NodeInfo]:
        """Get the currently selected node."""
        if self.cursor_row is not None and 0 <= self.cursor_row < len(self._nodes):
            return self._nodes[self.cursor_row]
        return None
