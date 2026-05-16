"""
Deployments Table Widget.
"""

from typing import Optional
from textual.widgets import DataTable
from textual.binding import Binding

from kubetui.k8s_client import DeploymentInfo


class DeploymentsTable(DataTable):
    """Table widget for displaying deployments."""
    
    BINDINGS = [
        Binding("enter", "select", "Select"),
        Binding("s", "scale", "Scale"),
        Binding("ctrl+r", "restart", "Restart"),
    ]
    
    def __init__(self, id: Optional[str] = None) -> None:
        """Initialize the deployments table."""
        super().__init__(id=id)
        self._deployments: list[DeploymentInfo] = []
    
    def on_mount(self) -> None:
        """Set up the table on mount."""
        self.add_columns(
            "Name", "Ready", "Up-to-date", "Available", "Age", "Replicas"
        )
        self.cursor_type = "row"
        self.zebra_stripes = True
    
    def update_data(self, deployments: list[DeploymentInfo]) -> None:
        """Update the table with new deployment data."""
        self._deployments = deployments
        self.clear()
        
        for deploy in deployments:
            # Color based on ready state
            ready_style = "green" if deploy.ready.split("/")[0] == deploy.ready.split("/")[1] else "yellow"
            
            self.add_row(
                deploy.name,
                (deploy.ready, ready_style),
                str(deploy.up_to_date),
                str(deploy.available),
                deploy.age,
                str(deploy.replicas),
            )
    
    def get_selected_deployment(self) -> Optional[DeploymentInfo]:
        """Get the currently selected deployment."""
        if self.cursor_row is not None and 0 <= self.cursor_row < len(self._deployments):
            return self._deployments[self.cursor_row]
        return None
    
    def action_select(self) -> None:
        """Handle select action."""
        deploy = self.get_selected_deployment()
        if deploy:
            self.app.notify(f"Selected: {deploy.name}")
    
    def action_scale(self) -> None:
        """Scale the deployment."""
        deploy = self.get_selected_deployment()
        if deploy:
            self.app.notify(f"Scale: {deploy.name}", title="Scale Deployment")
    
    def action_restart(self) -> None:
        """Restart the deployment."""
        deploy = self.get_selected_deployment()
        if deploy:
            self.app.notify(f"Restarting: {deploy.name}", severity="warning")
