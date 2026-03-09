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

STATUS_COLORS = {
    "active": ("bg-success", "text-dark"),
    "offline": ("bg-secondary", "text-white"),
    "staged": ("bg-info", "text-dark"),
    "decommissioned": ("bg-dark", "text-white"),
}

CONNECTION_TYPE_COLORS = {
    "wireless": ("bg-primary", "text-white"),
    "wired": ("bg-secondary", "text-white"),
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
            bg_class, text_class = STATUS_COLORS.get(status_val, ("bg-secondary", "text-white"))
            statuses.append(
                {
                    "key": status_val,
                    "label": label,
                    "count": row["count"],
                    "bg_class": bg_class,
                    "text_class": text_class,
                }
            )

    elif grouping == "connection_type":
        counts = Endpoint.objects.values("connection_type").annotate(count=Count("id")).order_by("-count")
        for row in counts:
            ct_val = row["connection_type"]
            label = CONNECTION_TYPE_LABELS.get(ct_val, ct_val)
            bg_class, text_class = CONNECTION_TYPE_COLORS.get(ct_val, ("bg-secondary", "text-white"))
            statuses.append(
                {
                    "key": ct_val,
                    "label": label,
                    "count": row["count"],
                    "bg_class": bg_class,
                    "text_class": text_class,
                }
            )

    elif grouping == "endpoint_type":
        counts = (
            Endpoint.objects.values("endpoint_type__manufacturer__name", "endpoint_type__model")
            .annotate(count=Count("id"))
            .order_by("-count")[:10]
        )
        colors = [
            ("bg-primary", "text-white"),
            ("bg-success", "text-dark"),
            ("bg-info", "text-dark"),
            ("bg-warning", "text-dark"),
            ("bg-danger", "text-white"),
            ("bg-secondary", "text-white"),
            ("bg-dark", "text-white"),
        ]
        for i, row in enumerate(counts):
            manufacturer = row["endpoint_type__manufacturer__name"]
            model = row["endpoint_type__model"]
            bg_class, text_class = colors[i % len(colors)]
            statuses.append(
                {
                    "key": f"{manufacturer}_{model}",
                    "label": f"{manufacturer} {model}",
                    "count": row["count"],
                    "bg_class": bg_class,
                    "text_class": text_class,
                }
            )

    return {
        "statuses": statuses,
        "total": total,
        "grouping_label": dict(GROUPING_CHOICES).get(grouping, grouping),
    }
