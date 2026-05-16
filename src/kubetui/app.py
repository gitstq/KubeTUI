"""
KubeTUI Application - Main TUI Application.
"""

from typing import Optional
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.reactive import reactive
from textual.widgets import (
    Header,
    Footer,
    Static,
    DataTable,
    TabbedContent,
    TabPane,
    Label,
    Button,
)

from kubetui.config import Config
from kubetui.k8s_client import K8sClient
from kubetui.widgets.namespace_selector import NamespaceSelector
from kubetui.widgets.pods_table import PodsTable
from kubetui.widgets.deployments_table import DeploymentsTable
from kubetui.widgets.services_table import ServicesTable
from kubetui.widgets.nodes_table import NodesTable
from kubetui.widgets.log_viewer import LogViewer
from kubetui.widgets.context_selector import ContextSelector
from kubetui.widgets.status_bar import StatusBar


class KubeTUI(App):
    """KubeTUI - Kubernetes Terminal User Interface."""
    
    CSS_PATH = "styles/app.tcss"
    TITLE = "🚀 KubeTUI"
    SUB_TITLE = "Kubernetes Terminal Manager"
    
    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
        Binding("r", "refresh", "Refresh", show=True),
        Binding("n", "select_namespace", "Namespace", show=True),
        Binding("c", "select_context", "Context", show=True),
        Binding("l", "view_logs", "Logs", show=True),
        Binding("d", "describe", "Describe", show=True),
        Binding("?", "help", "Help", show=True),
        Binding("1", "tab_pods", "Pods", show=True),
        Binding("2", "tab_deployments", "Deployments", show=True),
        Binding("3", "tab_services", "Services", show=True),
        Binding("4", "tab_nodes", "Nodes", show=True),
    ]
    
    current_namespace: reactive[str] = reactive("default")
    current_context: reactive[Optional[str]] = reactive(None)
    
    def __init__(
        self,
        k8s_client: K8sClient,
        config: Config,
        *args,
        **kwargs
    ) -> None:
        """Initialize the application."""
        super().__init__(*args, **kwargs)
        self.k8s_client = k8s_client
        self.config = config
        self.current_namespace = k8s_client.current_namespace
        self.current_context = k8s_client.current_context
    
    def compose(self) -> ComposeResult:
        """Compose the UI."""
        yield Header()
        
        with Container(id="main-container"):
            with Horizontal(id="top-bar"):
                yield Label(f"Context: {self.current_context or 'N/A'}", id="context-label")
                yield Label(f"Namespace: {self.current_namespace}", id="namespace-label")
            
            with TabbedContent(id="main-tabs", initial="pods"):
                with TabPane("_Pods", id="pods"):
                    yield PodsTable(id="pods-table")
                
                with TabPane("_Deployments", id="deployments"):
                    yield DeploymentsTable(id="deployments-table")
                
                with TabPane("_Services", id="services"):
                    yield ServicesTable(id="services-table")
                
                with TabPane("_Nodes", id="nodes"):
                    yield NodesTable(id="nodes-table")
        
        yield StatusBar(id="status-bar")
        yield Footer()
    
    def on_mount(self) -> None:
        """Handle mount event."""
        self.refresh_data()
        self.set_interval(self.config.refresh_interval, self.refresh_data)
    
    def refresh_data(self) -> None:
        """Refresh all data."""
        try:
            # Get current tab
            tabs = self.query_one(TabbedContent)
            current_tab = tabs.active
            
            if current_tab == "pods":
                self._refresh_pods()
            elif current_tab == "deployments":
                self._refresh_deployments()
            elif current_tab == "services":
                self._refresh_services()
            elif current_tab == "nodes":
                self._refresh_nodes()
            
            # Update status
            status = self.query_one(StatusBar)
            status.update_status(f"✅ Connected | Context: {self.current_context}")
            
        except Exception as e:
            status = self.query_one(StatusBar)
            status.update_status(f"❌ Error: {e}")
    
    def _refresh_pods(self) -> None:
        """Refresh pods table."""
        table = self.query_one(PodsTable)
        pods = self.k8s_client.get_pods(self.current_namespace)
        table.update_data(pods)
    
    def _refresh_deployments(self) -> None:
        """Refresh deployments table."""
        table = self.query_one(DeploymentsTable)
        deployments = self.k8s_client.get_deployments(self.current_namespace)
        table.update_data(deployments)
    
    def _refresh_services(self) -> None:
        """Refresh services table."""
        table = self.query_one(ServicesTable)
        services = self.k8s_client.get_services(self.current_namespace)
        table.update_data(services)
    
    def _refresh_nodes(self) -> None:
        """Refresh nodes table."""
        table = self.query_one(NodesTable)
        nodes = self.k8s_client.get_nodes()
        table.update_data(nodes)
    
    def action_refresh(self) -> None:
        """Refresh action."""
        self.refresh_data()
    
    def action_select_namespace(self) -> None:
        """Show namespace selector."""
        self.push_screen(NamespaceSelector(
            namespaces=self.k8s_client.get_namespaces(),
            current=self.current_namespace,
            on_select=self._on_namespace_selected,
        ))
    
    def _on_namespace_selected(self, namespace: str) -> None:
        """Handle namespace selection."""
        self.current_namespace = namespace
        self.k8s_client.set_namespace(namespace)
        
        # Update label
        label = self.query_one("#namespace-label", Label)
        label.update(f"Namespace: {namespace}")
        
        self.refresh_data()
    
    def action_select_context(self) -> None:
        """Show context selector."""
        self.push_screen(ContextSelector(
            contexts=self.k8s_client.get_contexts(),
            on_select=self._on_context_selected,
        ))
    
    def _on_context_selected(self, context: str) -> None:
        """Handle context selection."""
        if self.k8s_client.switch_context(context):
            self.current_context = context
            
            # Update label
            label = self.query_one("#context-label", Label)
            label.update(f"Context: {context}")
            
            self.refresh_data()
    
    def action_view_logs(self) -> None:
        """View logs for selected pod."""
        tabs = self.query_one(TabbedContent)
        if tabs.active != "pods":
            self.notify("Please select a pod first", severity="warning")
            return
        
        table = self.query_one(PodsTable)
        selected = table.get_selected_pod()
        
        if selected:
            self.push_screen(LogViewer(
                k8s_client=self.k8s_client,
                pod_name=selected.name,
                namespace=self.current_namespace,
            ))
    
    def action_describe(self) -> None:
        """Describe selected resource."""
        tabs = self.query_one(TabbedContent)
        
        if tabs.active == "pods":
            table = self.query_one(PodsTable)
            selected = table.get_selected_pod()
            if selected:
                describe = self.k8s_client.get_pod_describe(
                    selected.name, 
                    self.current_namespace
                )
                # Show in a modal
                self.notify(describe, title=f"Pod: {selected.name}")
    
    def action_help(self) -> None:
        """Show help."""
        help_text = """
🚀 KubeTUI Help

Navigation:
  ↑/↓     - Navigate rows
  Enter   - Select
  Tab     - Switch tabs
  
Actions:
  r       - Refresh
  n       - Change namespace
  c       - Change context
  l       - View logs (Pods)
  d       - Describe resource
  q       - Quit
  
Tabs:
  1       - Pods
  2       - Deployments
  3       - Services
  4       - Nodes
"""
        self.notify(help_text, title="Help", timeout=10)
    
    def action_tab_pods(self) -> None:
        """Switch to pods tab."""
        tabs = self.query_one(TabbedContent)
        tabs.active = "pods"
        self._refresh_pods()
    
    def action_tab_deployments(self) -> None:
        """Switch to deployments tab."""
        tabs = self.query_one(TabbedContent)
        tabs.active = "deployments"
        self._refresh_deployments()
    
    def action_tab_services(self) -> None:
        """Switch to services tab."""
        tabs = self.query_one(TabbedContent)
        tabs.active = "services"
        self._refresh_services()
    
    def action_tab_nodes(self) -> None:
        """Switch to nodes tab."""
        tabs = self.query_one(TabbedContent)
        tabs.active = "nodes"
        self._refresh_nodes()
