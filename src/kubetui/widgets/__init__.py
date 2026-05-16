"""
Widgets package for KubeTUI.
"""

from kubetui.widgets.pods_table import PodsTable
from kubetui.widgets.deployments_table import DeploymentsTable
from kubetui.widgets.services_table import ServicesTable
from kubetui.widgets.nodes_table import NodesTable
from kubetui.widgets.log_viewer import LogViewer
from kubetui.widgets.namespace_selector import NamespaceSelector
from kubetui.widgets.context_selector import ContextSelector
from kubetui.widgets.status_bar import StatusBar

__all__ = [
    "PodsTable",
    "DeploymentsTable",
    "ServicesTable",
    "NodesTable",
    "LogViewer",
    "NamespaceSelector",
    "ContextSelector",
    "StatusBar",
]
