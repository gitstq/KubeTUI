"""Tests for KubeTUI."""

import pytest
from kubetui import __version__


def test_version():
    """Test version is defined."""
    assert __version__ == "1.0.0"


def test_import():
    """Test main imports work."""
    from kubetui.app import KubeTUI
    from kubetui.config import Config
    from kubetui.main import main
    
    assert KubeTUI is not None
    assert Config is not None
    assert main is not None


class TestConfig:
    """Tests for Config class."""
    
    def test_default_config(self):
        """Test default configuration values."""
        from kubetui.config import Config
        
        config = Config()
        assert config.refresh_interval == 2.0
        assert config.default_namespace == "default"
        assert config.log_lines == 100
        assert config.theme == "dark"
    
    def test_config_save_load(self, tmp_path):
        """Test saving and loading configuration."""
        from kubetui.config import Config
        
        config = Config(
            refresh_interval=5.0,
            default_namespace="kube-system",
            log_lines=200,
        )
        
        config_path = tmp_path / "config.yaml"
        config.save(config_path)
        
        loaded = Config.load(config_path)
        assert loaded.refresh_interval == 5.0
        assert loaded.default_namespace == "kube-system"
        assert loaded.log_lines == 200


class TestK8sClient:
    """Tests for K8sClient class."""
    
    def test_calculate_age(self):
        """Test age calculation."""
        from datetime import datetime, timedelta, timezone
        from kubetui.k8s_client import K8sClient
        
        # Create a mock client
        client = K8sClient.__new__(K8sClient)
        
        # Test minutes
        now = datetime.now(timezone.utc)
        ts = now - timedelta(minutes=5)
        assert client._calculate_age(ts) == "5m"
        
        # Test hours
        ts = now - timedelta(hours=3)
        assert client._calculate_age(ts) == "3h"
        
        # Test days
        ts = now - timedelta(days=7)
        assert client._calculate_age(ts) == "7d"
