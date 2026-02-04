"""API views for NetBox Endpoints plugin."""

from django.db.models import Count

from netbox.api.viewsets import NetBoxModelViewSet

from ..filtersets import EndpointFilterSet, EndpointTypeFilterSet
from ..models import Endpoint, EndpointType
from .serializers import EndpointSerializer, EndpointTypeSerializer


class EndpointTypeViewSet(NetBoxModelViewSet):
    """API viewset for EndpointType objects."""

    queryset = EndpointType.objects.annotate(
        endpoint_count=Count("endpoints")
    ).prefetch_related("manufacturer", "default_platform", "tags")
    serializer_class = EndpointTypeSerializer
    filterset_class = EndpointTypeFilterSet


class EndpointViewSet(NetBoxModelViewSet):
    """API viewset for Endpoint objects."""

    queryset = Endpoint.objects.prefetch_related(
        "endpoint_type",
        "endpoint_type__manufacturer",
        "site",
        "location",
        "primary_ip4",
        "primary_ip6",
        "connected_interface",
        "tenant",
        "contact",
        "platform",
        "tags",
    )
    serializer_class = EndpointSerializer
    filterset_class = EndpointFilterSet
