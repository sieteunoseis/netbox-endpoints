"""Filtersets for NetBox Endpoints plugin."""

import django_filters

from dcim.models import Manufacturer, Platform, Site, Location
from netbox.filtersets import NetBoxModelFilterSet
from tenancy.models import Contact, Tenant

from .models import Endpoint, EndpointType, EndpointStatusChoices, EndpointConnectionTypeChoices


class EndpointTypeFilterSet(NetBoxModelFilterSet):
    """Filterset for EndpointType model."""

    manufacturer_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Manufacturer.objects.all(),
        label="Manufacturer (ID)",
    )
    manufacturer = django_filters.ModelMultipleChoiceFilter(
        field_name="manufacturer__slug",
        queryset=Manufacturer.objects.all(),
        to_field_name="slug",
        label="Manufacturer (slug)",
    )

    class Meta:
        model = EndpointType
        fields = ["id", "manufacturer_id", "model", "part_number"]

    def search(self, queryset, name, value):
        """Search across multiple fields."""
        if not value.strip():
            return queryset
        from django.db.models import Q

        return queryset.filter(
            Q(model__icontains=value)
            | Q(part_number__icontains=value)
            | Q(manufacturer__name__icontains=value)
        )


class EndpointFilterSet(NetBoxModelFilterSet):
    """Filterset for Endpoint model."""

    mac_address = django_filters.CharFilter(lookup_expr="icontains")
    name = django_filters.CharFilter(lookup_expr="icontains")

    endpoint_type_id = django_filters.ModelMultipleChoiceFilter(
        queryset=EndpointType.objects.all(),
        label="Endpoint Type (ID)",
    )

    site_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Site.objects.all(),
        label="Site (ID)",
    )
    site = django_filters.ModelMultipleChoiceFilter(
        field_name="site__slug",
        queryset=Site.objects.all(),
        to_field_name="slug",
        label="Site (slug)",
    )

    location_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Location.objects.all(),
        label="Location (ID)",
    )

    status = django_filters.MultipleChoiceFilter(
        choices=EndpointStatusChoices,
    )

    connection_type = django_filters.MultipleChoiceFilter(
        choices=EndpointConnectionTypeChoices,
    )

    ssid = django_filters.CharFilter(lookup_expr="icontains", label="SSID")

    tenant_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Tenant.objects.all(),
        label="Tenant (ID)",
    )
    tenant = django_filters.ModelMultipleChoiceFilter(
        field_name="tenant__slug",
        queryset=Tenant.objects.all(),
        to_field_name="slug",
        label="Tenant (slug)",
    )

    contact_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Contact.objects.all(),
        label="Contact (ID)",
    )

    platform_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Platform.objects.all(),
        label="Platform (ID)",
    )

    # Filter by manufacturer through endpoint_type
    manufacturer_id = django_filters.ModelMultipleChoiceFilter(
        field_name="endpoint_type__manufacturer",
        queryset=Manufacturer.objects.all(),
        label="Manufacturer (ID)",
    )

    class Meta:
        model = Endpoint
        fields = [
            "id",
            "mac_address",
            "name",
            "endpoint_type_id",
            "serial",
            "asset_tag",
            "site_id",
            "location_id",
            "status",
            "connection_type",
            "ssid",
            "tenant_id",
            "contact_id",
            "platform_id",
        ]

    def search(self, queryset, name, value):
        """Search across multiple fields."""
        if not value.strip():
            return queryset
        from django.db.models import Q

        return queryset.filter(
            Q(mac_address__icontains=value)
            | Q(name__icontains=value)
            | Q(serial__icontains=value)
            | Q(asset_tag__icontains=value)
            | Q(ssid__icontains=value)
            | Q(endpoint_type__model__icontains=value)
        )
