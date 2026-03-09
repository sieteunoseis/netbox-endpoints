"""Dashboard widgets for the NetBox Endpoints plugin."""

import logging

from django import forms
from django.db.models import Count
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from extras.dashboard.utils import register_widget
from extras.dashboard.widgets import DashboardWidget, WidgetConfigForm

from .models import Endpoint, EndpointConnectionTypeChoices, EndpointStatusChoices

logger = logging.getLogger(__name__)

GROUPING_CHOICES = [
    ("status", "Status"),
    ("connection_type", "Connection Type"),
    ("endpoint_type", "Endpoint Type"),
]

# Build label lookups from 3-tuples: (value, label, color)
STATUS_LABELS = {choice[0]: choice[1] for choice in EndpointStatusChoices.CHOICES}
CONNECTION_TYPE_LABELS = {choice[0]: choice[1] for choice in EndpointConnectionTypeChoices.CHOICES}

STATUS_BADGE_CLASS = {
    "active": "text-bg-success",
    "offline": "text-bg-secondary",
    "staged": "text-bg-info",
    "decommissioned": "text-bg-dark",
}

CONNECTION_TYPE_BADGE_CLASS = {
    "wireless": "text-bg-primary",
    "wired": "text-bg-secondary",
}


@register_widget
class EndpointsSummaryWidget(DashboardWidget):
    """Dashboard widget showing endpoint counts by type, status, or connection type."""

    default_title = _("Endpoints Summary")
    description = _("Display endpoint counts grouped by type, status, or connection type.")
    template_name = "netbox_endpoints/widgets/endpoints_summary.html"
    width = 4
    height = 3

    class ConfigForm(WidgetConfigForm):
        grouping = forms.ChoiceField(
            choices=GROUPING_CHOICES,
            initial="status",
            required=False,
            label=_("Group by"),
            help_text=_("How to group endpoint counts."),
        )

    def render(self, request):
        grouping = self.config.get("grouping", "status")

        return render_to_string(
            self.template_name,
            {
                "grouping": grouping,
            },
        )


def get_endpoints_summary_context(grouping="status"):
    """Build endpoints summary context from local database."""
    total = Endpoint.objects.count()

    if total == 0:
        return {
            "statuses": [],
            "total": 0,
            "grouping_label": dict(GROUPING_CHOICES).get(grouping, grouping),
        }

    statuses = []

    if grouping == "status":
        counts = Endpoint.objects.values("status").annotate(count=Count("id")).order_by("-count")
        for row in counts:
            status_val = row["status"]
            label = STATUS_LABELS.get(status_val, status_val)
            badge_class = STATUS_BADGE_CLASS.get(status_val, "text-bg-secondary")
            statuses.append(
                {
                    "key": status_val,
                    "label": label,
                    "count": row["count"],
                    "badge_class": badge_class,
                }
            )

    elif grouping == "connection_type":
        counts = Endpoint.objects.values("connection_type").annotate(count=Count("id")).order_by("-count")
        for row in counts:
            ct_val = row["connection_type"]
            label = CONNECTION_TYPE_LABELS.get(ct_val, ct_val)
            badge_class = CONNECTION_TYPE_BADGE_CLASS.get(ct_val, "text-bg-secondary")
            statuses.append(
                {
                    "key": ct_val,
                    "label": label,
                    "count": row["count"],
                    "badge_class": badge_class,
                }
            )

    elif grouping == "endpoint_type":
        counts = (
            Endpoint.objects.values("endpoint_type__manufacturer__name", "endpoint_type__model")
            .annotate(count=Count("id"))
            .order_by("-count")[:10]
        )
        colors = [
            "text-bg-primary",
            "text-bg-success",
            "text-bg-info",
            "text-bg-warning",
            "text-bg-danger",
            "text-bg-secondary",
            "text-bg-dark",
        ]
        for i, row in enumerate(counts):
            manufacturer = row["endpoint_type__manufacturer__name"]
            model = row["endpoint_type__model"]
            statuses.append(
                {
                    "key": f"{manufacturer}_{model}",
                    "label": f"{manufacturer} {model}",
                    "count": row["count"],
                    "badge_class": colors[i % len(colors)],
                }
            )

    return {
        "statuses": statuses,
        "total": total,
        "grouping_label": dict(GROUPING_CHOICES).get(grouping, grouping),
    }
