"""Navigation menu items for NetBox Endpoints plugin."""

from netbox.plugins import PluginMenuItem

menu_items = (
    PluginMenuItem(
        link="plugins:netbox_endpoints:settings",
        link_text="Endpoints Settings",
        permissions=["dcim.view_device"],
    ),
)
