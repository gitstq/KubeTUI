"""
Kubernetes client wrapper for KubeTUI.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional
import asyncio
from concurrent.futures import ThreadPoolExecutor

from kubernetes import client, config as k8s_config
from kubernetes.client import (
    V1Pod,
    V1Deployment,
    V1Service,
    V1Node,
    V1Namespace,
    V1ConfigMap,
    V1Secret,
    V1PodList,
    V1DeploymentList,
    V1ServiceList,
    V1NodeList,
    V1NamespaceList,
)
from kubernetes.stream import stream


@dataclass
class PodInfo:
    """Pod information."""
    name: str
    namespace: str
    status: str
    ready: str
    restarts: int
    age: str
    ip: str
    node: str
    labels: dict[str, str]
    cpu_request: Optional[str] = None
    memory_request: Optional[str] = None


@dataclass
class DeploymentInfo:
    """Deployment information."""
    name: str
    namespace: str
    ready: str
    up_to_date: int
    available: int
    age: str
    replicas: int
    labels: dict[str, str]


@dataclass
class ServiceInfo:
    """Service information."""
    name: str
    namespace: str
    type: str
    cluster_ip: str
    external_ip: str
    ports: str
    age: str
    labels: dict[str, str]


@dataclass
class NodeInfo:
    """Node information."""
    name: str
    status: str
    roles: str
    age: str
    version: str
    ip: str
    os: str
    kernel: str
    cpu_capacity: str
    memory_capacity: str


@dataclass
class ContextInfo:
    """Kubernetes context information."""
    name: str
    cluster: str
    user: str
    is_current: bool


class K8sClient:
    """Kubernetes API client wrapper."""
    
    def __init__(self) -> None:
        """Initialize the Kubernetes client."""
        self._core_v1: Optional[client.CoreV1Api] = None
        self._apps_v1: Optional[client.AppsV1Api] = None
        self._current_context: Optional[str] = None
        self._current_namespace: str = "default"
        self._executor = ThreadPoolExecutor(max_workers=4)
        self._available = False
        
        self._try_load_config()
    
    def _try_load_config(self) -> None:
        """Try to load Kubernetes configuration."""
        try:
            # Try in-cluster config first
            try:
                k8s_config.load_incluster_config()
                self._available = True
                return
            except k8s_config.ConfigException:
                pass
            
            # Try kubeconfig
            k8s_config.load_kube_config()
            
            # Get current context
            contexts, current_context = k8s_config.list_kube_config_contexts()
            self._current_context = current_context["name"]
            
            self._available = True
            
        except Exception:
            self._available = False
    
    def is_available(self) -> bool:
        """Check if Kubernetes is available."""
        return self._available
    
    @property
    def core_v1(self) -> client.CoreV1Api:
        """Get CoreV1 API client."""
        if self._core_v1 is None:
            self._core_v1 = client.CoreV1Api()
        return self._core_v1
    
    @property
    def apps_v1(self) -> client.AppsV1Api:
        """Get AppsV1 API client."""
        if self._apps_v1 is None:
            self._apps_v1 = client.AppsV1Api()
        return self._apps_v1
    
    @property
    def current_context(self) -> Optional[str]:
        """Get current context name."""
        return self._current_context
    
    @property
    def current_namespace(self) -> str:
        """Get current namespace."""
        return self._current_namespace
    
    def set_namespace(self, namespace: str) -> None:
        """Set current namespace."""
        self._current_namespace = namespace
    
    def get_contexts(self) -> list[ContextInfo]:
        """Get all available contexts."""
        contexts, current = k8s_config.list_kube_config_contexts()
        current_name = current["name"]
        
        result = []
        for ctx in contexts:
            result.append(ContextInfo(
                name=ctx["name"],
                cluster=ctx["context"].get("cluster", ""),
                user=ctx["context"].get("user", ""),
                is_current=ctx["name"] == current_name,
            ))
        
        return result
    
    def switch_context(self, context_name: str) -> bool:
        """Switch to a different context."""
        try:
            k8s_config.load_kube_config(context=context_name)
            self._current_context = context_name
            self._core_v1 = None
            self._apps_v1 = None
            return True
        except Exception:
            return False
    
    def get_namespaces(self) -> list[str]:
        """Get all namespaces."""
        try:
            namespaces: V1NamespaceList = self.core_v1.list_namespace()
            return sorted([ns.metadata.name for ns in namespaces.items])
        except Exception:
            return []
    
    def _calculate_age(self, creation_timestamp: datetime) -> str:
        """Calculate age from creation timestamp."""
        now = datetime.now(creation_timestamp.tzinfo)
        delta = now - creation_timestamp
        
        days = delta.days
        hours = delta.seconds // 3600
        minutes = (delta.seconds % 3600) // 60
        
        if days > 0:
            return f"{days}d"
        elif hours > 0:
            return f"{hours}h"
        else:
            return f"{minutes}m"
    
    def get_pods(self, namespace: Optional[str] = None) -> list[PodInfo]:
        """Get pods in namespace."""
        ns = namespace or self._current_namespace
        
        try:
            pods: V1PodList = self.core_v1.list_namespaced_pod(ns)
            result = []
            
            for pod in pods.items:
                # Calculate ready containers
                ready_count = 0
                total_count = 0
                restarts = 0
                
                if pod.status.container_statuses:
                    total_count = len(pod.status.container_statuses)
                    ready_count = sum(1 for cs in pod.status.container_statuses if cs.ready)
                    restarts = sum(cs.restart_count for cs in pod.status.container_statuses)
                
                # Get age
                age = self._calculate_age(pod.metadata.creation_timestamp)
                
                # Get IP and node
                pod_ip = pod.status.pod_ip or ""
                node_name = pod.spec.node_name or ""
                
                # Get labels
                labels = pod.metadata.labels or {}
                
                result.append(PodInfo(
                    name=pod.metadata.name,
                    namespace=ns,
                    status=pod.status.phase,
                    ready=f"{ready_count}/{total_count}",
                    restarts=restarts,
                    age=age,
                    ip=pod_ip,
                    node=node_name,
                    labels=labels,
                ))
            
            return sorted(result, key=lambda p: p.name)
            
        except Exception:
            return []
    
    def get_deployments(self, namespace: Optional[str] = None) -> list[DeploymentInfo]:
        """Get deployments in namespace."""
        ns = namespace or self._current_namespace
        
        try:
            deployments: V1DeploymentList = self.apps_v1.list_namespaced_deployment(ns)
            result = []
            
            for deploy in deployments.items:
                # Calculate ready replicas
                ready = deploy.status.ready_replicas or 0
                total = deploy.status.replicas or 0
                up_to_date = deploy.status.updated_replicas or 0
                available = deploy.status.available_replicas or 0
                
                # Get age
                age = self._calculate_age(deploy.metadata.creation_timestamp)
                
                # Get labels
                labels = deploy.metadata.labels or {}
                
                result.append(DeploymentInfo(
                    name=deploy.metadata.name,
                    namespace=ns,
                    ready=f"{ready}/{total}",
                    up_to_date=up_to_date,
                    available=available,
                    age=age,
                    replicas=total,
                    labels=labels,
                ))
            
            return sorted(result, key=lambda d: d.name)
            
        except Exception:
            return []
    
    def get_services(self, namespace: Optional[str] = None) -> list[ServiceInfo]:
        """Get services in namespace."""
        ns = namespace or self._current_namespace
        
        try:
            services: V1ServiceList = self.core_v1.list_namespaced_service(ns)
            result = []
            
            for svc in services.items:
                # Get service type
                svc_type = svc.spec.type or "ClusterIP"
                
                # Get cluster IP
                cluster_ip = svc.spec.cluster_ip or "None"
                
                # Get external IP
                external_ips = ""
                if svc.status.load_balancer.ingress:
                    external_ips = ", ".join(
                        ingress.ip or ingress.hostname 
                        for ingress in svc.status.load_balancer.ingress
                    )
                elif svc.spec.external_ips:
                    external_ips = ", ".join(svc.spec.external_ips)
                
                # Get ports
                ports = ""
                if svc.spec.ports:
                    port_strs = []
                    for port in svc.spec.ports:
                        if port.node_port:
                            port_strs.append(f"{port.port}:{port.node_port}/{port.protocol}")
                        else:
                            port_strs.append(f"{port.port}/{port.protocol}")
                    ports = ", ".join(port_strs)
                
                # Get age
                age = self._calculate_age(svc.metadata.creation_timestamp)
                
                # Get labels
                labels = svc.metadata.labels or {}
                
                result.append(ServiceInfo(
                    name=svc.metadata.name,
                    namespace=ns,
                    type=svc_type,
                    cluster_ip=cluster_ip,
                    external_ip=external_ips or "None",
                    ports=ports,
                    age=age,
                    labels=labels,
                ))
            
            return sorted(result, key=lambda s: s.name)
            
        except Exception:
            return []
    
    def get_nodes(self) -> list[NodeInfo]:
        """Get all nodes."""
        try:
            nodes: V1NodeList = self.core_v1.list_node()
            result = []
            
            for node in nodes.items:
                # Get node status
                status = "Unknown"
                for condition in node.status.conditions or []:
                    if condition.type == "Ready":
                        status = "Ready" if condition.status == "True" else "NotReady"
                        break
                
                # Get roles
                roles = []
                labels = node.metadata.labels or {}
                if "node-role.kubernetes.io/control-plane" in labels:
                    roles.append("control-plane")
                if "node-role.kubernetes.io/master" in labels:
                    roles.append("master")
                if "node-role.kubernetes.io/worker" in labels:
                    roles.append("worker")
                if not roles:
                    roles.append("worker")
                
                # Get version
                version = node.status.node_info.kubelet_version if node.status.node_info else ""
                
                # Get IP
                ip = ""
                for addr in node.status.addresses or []:
                    if addr.type == "InternalIP":
                        ip = addr.address
                        break
                
                # Get OS info
                os_name = ""
                kernel = ""
                if node.status.node_info:
                    os_name = node.status.node_info.os_image
                    kernel = node.status.node_info.kernel_version
                
                # Get capacity
                cpu_cap = node.status.capacity.get("cpu", "") if node.status.capacity else ""
                mem_cap = node.status.capacity.get("memory", "") if node.status.capacity else ""
                
                # Get age
                age = self._calculate_age(node.metadata.creation_timestamp)
                
                result.append(NodeInfo(
                    name=node.metadata.name,
                    status=status,
                    roles=",".join(roles),
                    age=age,
                    version=version,
                    ip=ip,
                    os=os_name,
                    kernel=kernel,
                    cpu_capacity=cpu_cap,
                    memory_capacity=mem_cap,
                ))
            
            return sorted(result, key=lambda n: n.name)
            
        except Exception:
            return []
    
    def get_pod_logs(
        self, 
        pod_name: str, 
        namespace: Optional[str] = None,
        container: Optional[str] = None,
        tail_lines: int = 100,
        follow: bool = False,
    ) -> str:
        """Get pod logs."""
        ns = namespace or self._current_namespace
        
        try:
            logs = self.core_v1.read_namespaced_pod_log(
                name=pod_name,
                namespace=ns,
                container=container,
                tail_lines=tail_lines,
                follow=follow,
                _preload_content=True,
            )
            return logs or "No logs available"
        except Exception as e:
            return f"Error getting logs: {e}"
    
    def delete_pod(self, pod_name: str, namespace: Optional[str] = None) -> bool:
        """Delete a pod."""
        ns = namespace or self._current_namespace
        
        try:
            self.core_v1.delete_namespaced_pod(name=pod_name, namespace=ns)
            return True
        except Exception:
            return False
    
    def scale_deployment(
        self, 
        deploy_name: str, 
        replicas: int, 
        namespace: Optional[str] = None
    ) -> bool:
        """Scale a deployment."""
        ns = namespace or self._current_namespace
        
        try:
            body = {"spec": {"replicas": replicas}}
            self.apps_v1.patch_namespaced_deployment_scale(
                name=deploy_name,
                namespace=ns,
                body=body,
            )
            return True
        except Exception:
            return False
    
    def restart_deployment(self, deploy_name: str, namespace: Optional[str] = None) -> bool:
        """Restart a deployment by updating annotation."""
        ns = namespace or self._current_namespace
        
        try:
            # Add restart annotation to trigger rollout
            import time
            body = {
                "spec": {
                    "template": {
                        "metadata": {
                            "annotations": {
                                "kubectl.kubernetes.io/restartedAt": datetime.now().isoformat()
                            }
                        }
                    }
                }
            }
            self.apps_v1.patch_namespaced_deployment(
                name=deploy_name,
                namespace=ns,
                body=body,
            )
            return True
        except Exception:
            return False
    
    def delete_deployment(self, deploy_name: str, namespace: Optional[str] = None) -> bool:
        """Delete a deployment."""
        ns = namespace or self._current_namespace
        
        try:
            self.apps_v1.delete_namespaced_deployment(name=deploy_name, namespace=ns)
            return True
        except Exception:
            return False
    
    def get_pod_describe(self, pod_name: str, namespace: Optional[str] = None) -> str:
        """Get detailed pod description."""
        ns = namespace or self._current_namespace
        
        try:
            pod: V1Pod = self.core_v1.read_namespaced_pod(name=pod_name, namespace=ns)
            
            lines = []
            lines.append(f"Name:         {pod.metadata.name}")
            lines.append(f"Namespace:    {pod.metadata.namespace}")
            lines.append(f"Priority:     {pod.spec.priority}")
            lines.append(f"Node:         {pod.spec.node_name}/{pod.status.host_ip}")
            lines.append(f"Start Time:   {pod.metadata.creation_timestamp}")
            lines.append(f"Status:       {pod.status.phase}")
            lines.append(f"IP:           {pod.status.pod_ip}")
            lines.append("")
            
            # Containers
            if pod.status.container_statuses:
                lines.append("Containers:")
                for cs in pod.status.container_statuses:
                    lines.append(f"  {cs.name}:")
                    lines.append(f"    Image:      {cs.image}")
                    lines.append(f"    State:      {cs.state}")
                    lines.append(f"    Ready:      {cs.ready}")
                    lines.append(f"    Restarts:   {cs.restart_count}")
            
            return "\n".join(lines)
            
        except Exception as e:
            return f"Error describing pod: {e}"
    
    def exec_in_pod(
        self,
        pod_name: str,
        command: list[str],
        namespace: Optional[str] = None,
        container: Optional[str] = None,
    ) -> tuple[int, str, str]:
        """Execute command in pod."""
        ns = namespace or self._current_namespace
        
        try:
            result = stream(
                self.core_v1.connect_get_namespaced_pod_exec,
                pod_name,
                ns,
                container=container,
                command=command,
                stderr=True,
                stdin=False,
                stdout=True,
                tty=False,
                _preload_content=True,
            )
            return 0, result, ""
        except Exception as e:
            return 1, "", str(e)
