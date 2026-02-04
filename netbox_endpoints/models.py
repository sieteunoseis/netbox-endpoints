"""Models for NetBox Endpoints plugin."""

from dcim.models import Device, Interface, Location, Manufacturer, Platform, Site
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from ipam.models import IPAddress
from netbox.models import NetBoxModel
from tenancy.models import Contact, Tenant
from utilities.choices import ChoiceSet


class EndpointStatusChoices(ChoiceSet):
    """Status choices for Endpoint model."""

    key = "Endpoint.status"

    STATUS_ACTIVE = "active"
    STATUS_OFFLINE = "offline"
    STATUS_STAGED = "staged"
    STATUS_DECOMMISSIONED = "decommissioned"

    CHOICES = [
        (STATUS_ACTIVE, "Active", "green"),
        (STATUS_OFFLINE, "Offline", "gray"),
        (STATUS_STAGED, "Staged", "blue"),
        (STATUS_DECOMMISSIONED, "Decommissioned", "black"),
    ]


class EndpointConnectionTypeChoices(ChoiceSet):
    """Connection type choices for Endpoint model."""

    key = "Endpoint.connection_type"

    TYPE_WIRELESS = "wireless"
    TYPE_WIRED = "wired"

    CHOICES = [
        (TYPE_WIRELESS, "Wireless", "blue"),
        (TYPE_WIRED, "Wired", "gray"),
    ]


class EndpointType(NetBoxModel):
    """
    Endpoint type model (like DeviceType but for endpoints).

    Examples: Vocera B3000n, Cisco CP-8845, iPhone 14, etc.
    """

    manufacturer = models.ForeignKey(
        to=Manufacturer,
        on_delete=models.PROTECT,
        related_name="endpoint_types",
    )
    model = models.CharField(max_length=100)
    part_number = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    default_platform = models.ForeignKey(
        to=Platform,
        on_delete=models.SET_NULL,
        related_name="endpoint_types",
        blank=True,
        null=True,
        help_text="Default platform/OS for this endpoint type",
    )

    # Standard NetBox fields
    comments = models.TextField(blank=True)

    class Meta:
        ordering = ["manufacturer", "model"]
        unique_together = ["manufacturer", "model"]
        verbose_name = "Endpoint Type"
        verbose_name_plural = "Endpoint Types"

    def __str__(self):
        return f"{self.manufacturer} {self.model}"

    def get_absolute_url(self):
        return reverse("plugins:netbox_endpoints:endpointtype", args=[self.pk])


class Endpoint(NetBoxModel):
    """
    Endpoint model for wireless and wired endpoints.

    Examples: Vocera badges, Cisco IP phones, tablets, IoT devices, etc.
    """

    # Identity
    mac_address = models.CharField(
        max_length=17,
        unique=True,
        help_text="MAC address in format XX:XX:XX:XX:XX:XX",
    )
    name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Optional name (e.g., Badge 1234, hostname)",
    )
    endpoint_type = models.ForeignKey(
        to=EndpointType,
        on_delete=models.PROTECT,
        related_name="endpoints",
    )
    serial = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Serial Number",
    )
    asset_tag = models.CharField(
        max_length=50,
        blank=True,
        unique=True,
        null=True,
    )

    # Location
    site = models.ForeignKey(
        to=Site,
        on_delete=models.PROTECT,
        related_name="endpoints",
    )
    location = models.ForeignKey(
        to=Location,
        on_delete=models.SET_NULL,
        related_name="endpoints",
        blank=True,
        null=True,
        help_text="Specific location within the site (room, floor, etc.)",
    )

    # Network
    primary_ip4 = models.ForeignKey(
        to=IPAddress,
        on_delete=models.SET_NULL,
        related_name="primary_ip4_for_endpoints",
        blank=True,
        null=True,
        verbose_name="Primary IPv4",
    )
    primary_ip6 = models.ForeignKey(
        to=IPAddress,
        on_delete=models.SET_NULL,
        related_name="primary_ip6_for_endpoints",
        blank=True,
        null=True,
        verbose_name="Primary IPv6",
    )
    connection_type = models.CharField(
        max_length=20,
        choices=EndpointConnectionTypeChoices,
        default=EndpointConnectionTypeChoices.TYPE_WIRELESS,
    )

    # Wired-specific
    connected_interface = models.ForeignKey(
        to=Interface,
        on_delete=models.SET_NULL,
        related_name="connected_endpoints",
        blank=True,
        null=True,
        help_text="Switch port this endpoint is connected to (for wired endpoints)",
    )

    # Wireless-specific
    ssid = models.CharField(
        max_length=32,
        blank=True,
        verbose_name="SSID",
        help_text="Current or default SSID (for wireless endpoints)",
    )

    # Ownership
    tenant = models.ForeignKey(
        to=Tenant,
        on_delete=models.PROTECT,
        related_name="endpoints",
        blank=True,
        null=True,
    )
    contact = models.ForeignKey(
        to=Contact,
        on_delete=models.SET_NULL,
        related_name="endpoints",
        blank=True,
        null=True,
        help_text="Person who has/owns this endpoint",
    )
    platform = models.ForeignKey(
        to=Platform,
        on_delete=models.SET_NULL,
        related_name="endpoints",
        blank=True,
        null=True,
        help_text="Operating system or platform",
    )

    # Status
    status = models.CharField(
        max_length=20,
        choices=EndpointStatusChoices,
        default=EndpointStatusChoices.STATUS_ACTIVE,
    )

    # Standard NetBox fields
    description = models.TextField(blank=True)
    comments = models.TextField(blank=True)

    # Clone fields for bulk operations
    clone_fields = [
        "endpoint_type",
        "site",
        "location",
        "connection_type",
        "ssid",
        "tenant",
        "platform",
        "status",
    ]

    class Meta:
        ordering = ["mac_address"]
        verbose_name = "Endpoint"
        verbose_name_plural = "Endpoints"

    def __str__(self):
        if self.name:
            return f"{self.name} ({self.mac_address})"
        return self.mac_address

    def get_absolute_url(self):
        return reverse("plugins:netbox_endpoints:endpoint", args=[self.pk])

    @property
    def primary_ip(self):
        """Return primary IPv4 or IPv6 address."""
        return self.primary_ip4 or self.primary_ip6

    def clean(self):
        """Validate the endpoint."""
        from django.core.exceptions import ValidationError

        super().clean()

        # Normalize MAC address to uppercase with colons
        if self.mac_address:
            mac = self.mac_address.upper().replace("-", ":").replace(".", ":")
            # Handle formats like AABBCCDDEEFF
            if len(mac) == 12 and ":" not in mac:
                mac = ":".join(mac[i : i + 2] for i in range(0, 12, 2))
            self.mac_address = mac

        # Validate wired endpoints should have connected_interface
        # and wireless endpoints should have ssid
        # (not enforced, just helpful)

    def save(self, *args, **kwargs):
        """Save the endpoint after cleaning."""
        self.full_clean()
        super().save(*args, **kwargs)
