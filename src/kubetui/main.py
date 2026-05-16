#!/usr/bin/env python3
"""
KubeTUI Main Entry Point.

A modern, fast, and intuitive TUI for Kubernetes cluster management.
"""

import asyncio
import sys
from typing import Optional

from kubetui.app import KubeTUI
from kubetui.config import Config
from kubetui.k8s_client import K8sClient


def main() -> int:
    """Main entry point for KubeTUI."""
    try:
        # Initialize Kubernetes client
        k8s_client = K8sClient()
        
        # Check if kubeconfig is available
        if not k8s_client.is_available():
            print("❌ Error: No Kubernetes configuration found!")
            print("   Please ensure kubeconfig is set up correctly.")
            print("   Run: kubectl config view")
            return 1
        
        # Load configuration
        config = Config.load()
        
        # Create and run the app
        app = KubeTUI(k8s_client=k8s_client, config=config)
        app.run()
        
        return 0
        
    except KeyboardInterrupt:
        print("\n👋 KubeTUI closed.")
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
