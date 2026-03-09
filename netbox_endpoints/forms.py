"""Forms for NetBox Endpoints plugin."""

from dcim.models import Interface, Location, Manufacturer, Platform, Site
from django import forms
from ipam.models import IPAddress
from netbox.forms import NetBoxModelBulkEditForm, NetBoxModelFilterSetForm, NetBoxModelForm, NetBoxModelImportForm
from tenancy.models import Contact, Tenant
from utilities.forms.fields import (
    CommentField,
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
    TagFilterField,
)
from utilities.forms.rendering import FieldSet

from .models import Endpoint, EndpointConnectionTypeChoices, EndpointStatusChoices, EndpointType

#
# EndpointType Forms
#


class EndpointTypeForm(NetBoxModelForm):
    """Form for creating/editing EndpointType objects."""

    manufacturer = DynamicModelChoiceField(queryset=Manufacturer.objects.all())
    default_platform = DynamicModelChoiceField(
        queryset=Platform.objects.all(),
        required=False,
    )
    comments = CommentField()

    fieldsets = (
        FieldSet("manufacturer", "model", "part_number", "default_platform", name="Endpoint Type"),
        FieldSet("description", "comments", "tags", name="Details"),
    )

    class Meta:
        model = EndpointType
        fields = [
            "manufacturer",
            "model",
            "part_number",
            "default_platform",
            "description",
            "comments",
            "tags",
        ]


class EndpointTypeFilterForm(NetBoxModelFilterSetForm):
    """Filter form for EndpointType list view."""

    model = EndpointType

    manufacturer_id = DynamicModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        label="Manufacturer",
    )
    tag = TagFilterField(model)


class EndpointTypeImportForm(NetBoxModelImportForm):
    """Import form for EndpointType objects."""

    manufacturer = forms.ModelChoiceField(
        queryset=Manufacturer.objects.all(),
        to_field_name="name",
    )
    default_platform = forms.ModelChoiceField(
        queryset=Platform.objects.all(),
        to_field_name="name",
        required=False,
    )

    class Meta:
        model = EndpointType
        fields = ["manufacturer", "model", "part_number", "default_platform", "description", "comments", "tags"]


class EndpointTypeBulkEditForm(NetBoxModelBulkEditForm):
    """Bulk edit form for EndpointType objects."""

    model = EndpointType

    manufacturer = DynamicModelChoiceField(queryset=Manufacturer.objects.all(), required=False)
    default_platform = DynamicModelChoiceField(queryset=Platform.objects.all(), required=False)
    description = forms.CharField(max_length=200, required=False)
    comments = CommentField()

    nullable_fields = ["default_platform", "description", "comments"]


#
# Endpoint Forms
#


class EndpointForm(NetBoxModelForm):
    """Form for creating/editing Endpoint objects."""

    endpoint_type = DynamicModelChoiceField(queryset=EndpointType.objects.all())
    site = DynamicModelChoiceField(queryset=Site.objects.all())
    location = DynamicModelChoiceField(
        queryset=Location.objects.all(),
        required=False,
        query_params={"site_id": "$site"},
    )
    primary_ip4 = DynamicModelChoiceField(
        queryset=IPAddress.objects.all(),
        required=False,
        label="Primary IPv4",
    )
    primary_ip6 = DynamicModelChoiceField(
        queryset=IPAddress.objects.all(),
        required=False,
        label="Primary IPv6",
    )
    connected_interface = DynamicModelChoiceField(
        queryset=Interface.objects.all(),
        required=False,
        label="Connected Interface",
        help_text="Switch port for wired endpoints",
    )
    tenant = DynamicModelChoiceField(queryset=Tenant.objects.all(), required=False)
    contact = DynamicModelChoiceField(queryset=Contact.objects.all(), required=False)
    platform = DynamicModelChoiceField(queryset=Platform.objects.all(), required=False)
    comments = CommentField()

    fieldsets = (
        FieldSet("mac_address", "name", "endpoint_type", "serial", "asset_tag", name="Identity"),
        FieldSet("site", "location", name="Location"),
        FieldSet(
            "connection_type",
            "primary_ip4",
            "primary_ip6",
            "connected_interface",
            "ssid",
            name="Network",
        ),
        FieldSet("status", "tenant", "contact", "platform", name="Assignment"),
        FieldSet("description", "comments", "tags", name="Details"),
    )

    class Meta:
        model = Endpoint
        fields = [
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
        ]


class EndpointFilterForm(NetBoxModelFilterSetForm):
    """Filter form for Endpoint list view."""

    model = Endpoint

    mac_address = forms.CharField(required=False)
    name = forms.CharField(required=False)
    endpoint_type_id = DynamicModelMultipleChoiceField(
        queryset=EndpointType.objects.all(),
        required=False,
        label="Endpoint Type",
    )
    site_id = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        required=False,
        label="Site",
    )
    location_id = DynamicModelMultipleChoiceField(
        queryset=Location.objects.all(),
        required=False,
        label="Location",
    )
    status = forms.MultipleChoiceField(
        choices=EndpointStatusChoices,
        required=False,
    )
    connection_type = forms.MultipleChoiceField(
        choices=EndpointConnectionTypeChoices,
        required=False,
    )
    ssid = forms.CharField(required=False, label="SSID")
    tenant_id = DynamicModelMultipleChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        label="Tenant",
    )
    contact_id = DynamicModelMultipleChoiceField(
        queryset=Contact.objects.all(),
        required=False,
        label="Contact",
    )
    tag = TagFilterField(model)


class EndpointImportForm(NetBoxModelImportForm):
    """Import form for Endpoint objects (CSV import)."""

    endpoint_type = forms.ModelChoiceField(
        queryset=EndpointType.objects.all(),
        to_field_name="model",
        help_text="Endpoint type model name",
    )
    site = forms.ModelChoiceField(
        queryset=Site.objects.all(),
        to_field_name="name",
    )
    location = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        to_field_name="name",
        required=False,
    )
    tenant = forms.ModelChoiceField(
        queryset=Tenant.objects.all(),
        to_field_name="name",
        required=False,
    )
    platform = forms.ModelChoiceField(
        queryset=Platform.objects.all(),
        to_field_name="name",
        required=False,
    )
    status = forms.ChoiceField(
        choices=EndpointStatusChoices,
        required=False,
    )
    connection_type = forms.ChoiceField(
        choices=EndpointConnectionTypeChoices,
        required=False,
    )

    class Meta:
        model = Endpoint
        fields = [
            "mac_address",
            "name",
            "endpoint_type",
            "serial",
            "asset_tag",
            "site",
            "location",
            "connection_type",
            "ssid",
            "tenant",
            "platform",
            "status",
            "description",
            "comments",
            "tags",
        ]


class EndpointBulkEditForm(NetBoxModelBulkEditForm):
    """Bulk edit form for Endpoint objects."""

    model = Endpoint

    endpoint_type = DynamicModelChoiceField(queryset=EndpointType.objects.all(), required=False)
    site = DynamicModelChoiceField(queryset=Site.objects.all(), required=False)
    location = DynamicModelChoiceField(queryset=Location.objects.all(), required=False)
    status = forms.ChoiceField(choices=EndpointStatusChoices, required=False)
    connection_type = forms.ChoiceField(choices=EndpointConnectionTypeChoices, required=False)
    ssid = forms.CharField(max_length=32, required=False, label="SSID")
    tenant = DynamicModelChoiceField(queryset=Tenant.objects.all(), required=False)
    contact = DynamicModelChoiceField(queryset=Contact.objects.all(), required=False)
    platform = DynamicModelChoiceField(queryset=Platform.objects.all(), required=False)
    description = forms.CharField(max_length=200, required=False)
    comments = CommentField()

    nullable_fields = [
        "name",
        "location",
        "primary_ip4",
        "primary_ip6",
        "connected_interface",
        "ssid",
        "tenant",
        "contact",
        "platform",
        "description",
        "comments",
    ]
