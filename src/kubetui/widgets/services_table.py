"""
Services Table Widget.
"""

from typing import Optional
from textual.widgets import DataTable

from kubetui.k8s_client import ServiceInfo


class ServicesTable(DataTable):
    """Table widget for displaying services."""
    
    def __init__(self, id: Optional[str] = None) -> None:
        """Initialize the services table."""
        super().__init__(id=id)
        self._services: list[ServiceInfo] = []
    
    def on_mount(self) -> None:
        """Set up the table on mount."""
        self.add_columns(
            "Name", "Type", "Cluster-IP", "External-IP", "Ports", "Age"
        )
        self.cursor_type = "row"
        self.zebra_stripes = True
    
    def update_data(self, services: list[ServiceInfo]) -> None:
        """Update the table with new service data."""
        self._services = services
        self.clear()
        
        for svc in services:
            # Color based on type
            type_style = "cyan" if svc.type == "LoadBalancer" else "white"
            
            self.add_row(
                svc.name,
                (svc.type, type_style),
                svc.cluster_ip,
                svc.external_ip,
                svc.ports[:50] + "..." if len(svc.ports) > 50 else svc.ports,
                svc.age,
            )
    
    def get_selected_service(self) -> Optional[ServiceInfo]:
        """Get the currently selected service."""
        if self.cursor_row is not None and 0 <= self.cursor_row < len(self._services):
            return self._services[self.cursor_row]
        return None
