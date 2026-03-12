"""Navigation menu items for NetBox Endpoints plugin."""

from netbox.plugins import PluginMenu, PluginMenuButton, PluginMenuItem

menu = PluginMenu(
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
