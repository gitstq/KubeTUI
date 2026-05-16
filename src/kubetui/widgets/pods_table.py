"""
Pods Table Widget.
"""

from typing import Optional
from textual.widgets import DataTable
from textual.binding import Binding

from kubetui.k8s_client import PodInfo


class PodsTable(DataTable):
    """Table widget for displaying pods."""
    
    BINDINGS = [
        Binding("enter", "select", "Select"),
        Binding("delete", "delete_pod", "Delete"),
    ]
    
    def __init__(self, id: Optional[str] = None) -> None:
        """Initialize the pods table."""
        super().__init__(id=id)
        self._pods: list[PodInfo] = []
        self._selected_pod: Optional[PodInfo] = None
    
    def on_mount(self) -> None:
        """Set up the table on mount."""
        self.add_columns(
            "Name", "Status", "Ready", "Restarts", "Age", "IP", "Node"
        )
        self.cursor_type = "row"
        self.zebra_stripes = True
    
    def update_data(self, pods: list[PodInfo]) -> None:
        """Update the table with new pod data."""
        self._pods = pods
        self.clear()
        
        for pod in pods:
            # Color based on status
            status_style = self._get_status_style(pod.status)
            
            self.add_row(
                pod.name,
                (pod.status, status_style),
                pod.ready,
                str(pod.restarts),
                pod.age,
                pod.ip,
                pod.node,
            )
    
    def _get_status_style(self, status: str) -> str:
        """Get style for status."""
        status_colors = {
            "Running": "green",
            "Pending": "yellow",
            "Succeeded": "blue",
            "Failed": "red",
            "Unknown": "dim",
        }
        return status_colors.get(status, "white")
    
    def get_selected_pod(self) -> Optional[PodInfo]:
        """Get the currently selected pod."""
        if self.cursor_row is not None and 0 <= self.cursor_row < len(self._pods):
            return self._pods[self.cursor_row]
        return None
    
    def action_select(self) -> None:
        """Handle select action."""
        self._selected_pod = self.get_selected_pod()
        if self._selected_pod:
            self.app.notify(f"Selected: {self._selected_pod.name}")
    
    def action_delete_pod(self) -> None:
        """Delete the selected pod."""
        pod = self.get_selected_pod()
        if pod:
            # Confirm deletion
            self.app.notify(
                f"Deleting pod: {pod.name}",
                severity="warning",
            )
