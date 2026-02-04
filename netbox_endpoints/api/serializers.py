"""API serializers for NetBox Endpoints plugin."""

from rest_framework import serializers

from dcim.api.serializers import ManufacturerSerializer, PlatformSerializer, SiteSerializer, LocationSerializer, InterfaceSerializer
from ipam.api.serializers import IPAddressSerializer
from netbox.api.serializers import NetBoxModelSerializer
from tenancy.api.serializers import TenantSerializer, ContactSerializer

from ..models import Endpoint, EndpointType


class EndpointTypeSerializer(NetBoxModelSerializer):
    """Serializer for EndpointType."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_endpoints-api:endpointtype-detail"
    )
    endpoint_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = EndpointType
        fields = [
            "id",
            "url",
            "display",
            "manufacturer",
            "model",
            "part_number",
            "default_platform",
            "description",
            "comments",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
            "endpoint_count",
        ]
        brief_fields = ["id", "url", "display", "manufacturer", "model"]


class EndpointSerializer(NetBoxModelSerializer):
    """Serializer for Endpoint."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_endpoints-api:endpoint-detail"
    )

    class Meta:
        model = Endpoint
        fields = [
            "id",
            "url",
            "display",
            "mac_address",
            "name",
            "endpoint_type",
            "serial",
            "asset_tag",
            "site",
            "location",
            "primary_ip4",
            "primary_ip6",
            "connection_type",
            "connected_interface",
            "ssid",
            "tenant",
            "contact",
            "platform",
            "status",
            "description",
            "comments",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        ]
        brief_fields = ["id", "url", "display", "mac_address", "name", "endpoint_type"]
