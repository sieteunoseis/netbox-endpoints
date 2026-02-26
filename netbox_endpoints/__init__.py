"""
NetBox Endpoints Plugin

Manage wireless and wired endpoints (badges, phones, IoT devices) in NetBox.
Provides a dedicated model for mobile/endpoint devices that don't fit the
traditional Device model (no rack location, dynamic IPs, etc.).
"""

from netbox.plugins import PluginConfig

__version__ = "0.1.2"


class EndpointsConfig(PluginConfig):
    """Plugin configuration for NetBox Endpoints."""

    name = "netbox_endpoints"
    verbose_name = "NetBox Endpoints"
    description = "Manage wireless and wired endpoints (badges, phones, IoT devices)"
    version = __version__
    author = "Jeremy Worden"
    author_email = "jeremy.worden@gmail.com"
    base_url = "endpoints"
    min_version = "4.0.0"

    # Required settings
    required_settings = []

    # Default configuration values
    default_settings = {}


config = EndpointsConfig
