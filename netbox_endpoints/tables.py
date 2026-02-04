"""Tables for NetBox Endpoints plugin."""

import django_tables2 as tables

from netbox.tables import NetBoxTable, ChoiceFieldColumn, columns

from .models import Endpoint, EndpointType


class EndpointTypeTable(NetBoxTable):
    """Table for displaying EndpointType objects."""

    manufacturer = tables.Column(linkify=True)
    model = tables.Column(linkify=True)
    endpoint_count = columns.LinkedCountColumn(
        viewname="plugins:netbox_endpoints:endpoint_list",
        url_params={"endpoint_type_id": "pk"},
        verbose_name="Endpoints",
    )
    tags = columns.TagColumn(url_name="plugins:netbox_endpoints:endpointtype_list")

    class Meta(NetBoxTable.Meta):
        model = EndpointType
        fields = (
            "pk",
            "id",
            "manufacturer",
            "model",
            "part_number",
            "default_platform",
            "endpoint_count",
            "tags",
        )
        default_columns = (
            "manufacturer",
            "model",
            "part_number",
            "endpoint_count",
        )


class EndpointTable(NetBoxTable):
    """Table for displaying Endpoint objects."""

    mac_address = tables.Column(linkify=True)
    name = tables.Column(linkify=True)
    endpoint_type = tables.Column(linkify=True)
    site = tables.Column(linkify=True)
    location = tables.Column(linkify=True)
    status = ChoiceFieldColumn()
    connection_type = ChoiceFieldColumn()
    primary_ip4 = tables.Column(linkify=True, verbose_name="IPv4")
    tenant = tables.Column(linkify=True)
    contact = tables.Column(linkify=True)
    tags = columns.TagColumn(url_name="plugins:netbox_endpoints:endpoint_list")

    class Meta(NetBoxTable.Meta):
        model = Endpoint
        fields = (
            "pk",
            "id",
            "mac_address",
            "name",
            "endpoint_type",
            "serial",
            "asset_tag",
            "site",
            "location",
            "status",
            "connection_type",
            "ssid",
            "primary_ip4",
            "connected_interface",
            "tenant",
            "contact",
            "platform",
            "tags",
            "created",
            "last_updated",
        )
        default_columns = (
            "mac_address",
            "name",
            "endpoint_type",
            "site",
            "status",
            "connection_type",
            "ssid",
            "primary_ip4",
        )
