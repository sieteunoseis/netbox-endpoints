"""Navigation menu items for NetBox Endpoints plugin."""

from django.conf import settings
from netbox.plugins import PluginMenu, PluginMenuButton, PluginMenuItem

_menu = PluginMenu(
    label="Endpoints",
    groups=(
        (
            "Endpoints",
            (
                PluginMenuItem(
                    link="plugins:netbox_endpoints:endpoint_list",
                    link_text="Endpoints",
                    permissions=["netbox_endpoints.view_endpoint"],
                    buttons=(
                        PluginMenuButton(
                            link="plugins:netbox_endpoints:endpoint_add",
                            title="Add",
                            icon_class="mdi mdi-plus-thick",
                            permissions=["netbox_endpoints.add_endpoint"],
                        ),
                        PluginMenuButton(
                            link="plugins:netbox_endpoints:endpoint_bulk_import",
                            title="Import",
                            icon_class="mdi mdi-upload",
                            permissions=["netbox_endpoints.add_endpoint"],
                        ),
                    ),
                ),
                PluginMenuItem(
                    link="plugins:netbox_endpoints:endpointtype_list",
                    link_text="Endpoint Types",
                    permissions=["netbox_endpoints.view_endpointtype"],
                    buttons=(
                        PluginMenuButton(
                            link="plugins:netbox_endpoints:endpointtype_add",
                            title="Add",
                            icon_class="mdi mdi-plus-thick",
                            permissions=["netbox_endpoints.add_endpointtype"],
                        ),
                    ),
                ),
            ),
        ),
    ),
    icon_class="mdi mdi-access-point",
)


# top_level_menu=False puts this plugin's items under the shared "Plugins" menu
# (grouped by plugin name) instead of its own top-level sidebar menu.
if settings.PLUGINS_CONFIG.get("netbox_endpoints", {}).get("top_level_menu", True):
    menu = _menu
else:
    menu_items = tuple(item for group in _menu.groups for item in group.items)
