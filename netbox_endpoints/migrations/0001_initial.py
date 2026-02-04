"""Initial migration for netbox_endpoints plugin."""

import django.db.models.deletion
import taggit.managers
import utilities.json
from django.db import migrations, models


class Migration(migrations.Migration):
    """Initial migration creating EndpointType and Endpoint models."""

    initial = True

    dependencies = [
        ("dcim", "0001_initial"),
        ("ipam", "0001_initial"),
        ("tenancy", "0001_initial"),
        ("extras", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="EndpointType",
            fields=[
                (
                    "id",
                    models.BigAutoField(auto_created=True, primary_key=True, serialize=False),
                ),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder),
                ),
                ("model", models.CharField(max_length=100)),
                ("part_number", models.CharField(blank=True, max_length=50)),
                ("description", models.TextField(blank=True)),
                ("comments", models.TextField(blank=True)),
                (
                    "manufacturer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="endpoint_types",
                        to="dcim.manufacturer",
                    ),
                ),
                (
                    "default_platform",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="endpoint_types",
                        to="dcim.platform",
                        help_text="Default platform/OS for this endpoint type",
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(through="extras.TaggedItem", to="extras.Tag"),
                ),
            ],
            options={
                "verbose_name": "Endpoint Type",
                "verbose_name_plural": "Endpoint Types",
                "ordering": ["manufacturer", "model"],
                "unique_together": {("manufacturer", "model")},
            },
        ),
        migrations.CreateModel(
            name="Endpoint",
            fields=[
                (
                    "id",
                    models.BigAutoField(auto_created=True, primary_key=True, serialize=False),
                ),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder),
                ),
                (
                    "mac_address",
                    models.CharField(
                        max_length=17,
                        unique=True,
                        help_text="MAC address in format XX:XX:XX:XX:XX:XX",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        help_text="Optional name (e.g., Badge 1234, hostname)",
                    ),
                ),
                ("serial", models.CharField(blank=True, max_length=50, verbose_name="Serial Number")),
                (
                    "asset_tag",
                    models.CharField(blank=True, max_length=50, null=True, unique=True),
                ),
                (
                    "connection_type",
                    models.CharField(
                        default="wireless",
                        max_length=20,
                    ),
                ),
                (
                    "ssid",
                    models.CharField(
                        blank=True,
                        max_length=32,
                        verbose_name="SSID",
                        help_text="Current or default SSID (for wireless endpoints)",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        default="active",
                        max_length=20,
                    ),
                ),
                ("description", models.TextField(blank=True)),
                ("comments", models.TextField(blank=True)),
                (
                    "endpoint_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="endpoints",
                        to="netbox_endpoints.endpointtype",
                    ),
                ),
                (
                    "site",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="endpoints",
                        to="dcim.site",
                    ),
                ),
                (
                    "location",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="endpoints",
                        to="dcim.location",
                        help_text="Specific location within the site (room, floor, etc.)",
                    ),
                ),
                (
                    "primary_ip4",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="primary_ip4_for_endpoints",
                        to="ipam.ipaddress",
                        verbose_name="Primary IPv4",
                    ),
                ),
                (
                    "primary_ip6",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="primary_ip6_for_endpoints",
                        to="ipam.ipaddress",
                        verbose_name="Primary IPv6",
                    ),
                ),
                (
                    "connected_interface",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="connected_endpoints",
                        to="dcim.interface",
                        help_text="Switch port this endpoint is connected to (for wired endpoints)",
                    ),
                ),
                (
                    "tenant",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="endpoints",
                        to="tenancy.tenant",
                    ),
                ),
                (
                    "contact",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="endpoints",
                        to="tenancy.contact",
                        help_text="Person who has/owns this endpoint",
                    ),
                ),
                (
                    "platform",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="endpoints",
                        to="dcim.platform",
                        help_text="Operating system or platform",
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(through="extras.TaggedItem", to="extras.Tag"),
                ),
            ],
            options={
                "verbose_name": "Endpoint",
                "verbose_name_plural": "Endpoints",
                "ordering": ["mac_address"],
            },
        ),
    ]
