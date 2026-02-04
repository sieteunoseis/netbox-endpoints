"""Views for NetBox Endpoints plugin."""

from django.db.models import Count

from netbox.views import generic

from .filtersets import EndpointFilterSet, EndpointTypeFilterSet
from .forms import (
    EndpointBulkEditForm,
    EndpointFilterForm,
    EndpointForm,
    EndpointImportForm,
    EndpointTypeBulkEditForm,
    EndpointTypeFilterForm,
    EndpointTypeForm,
    EndpointTypeImportForm,
)
from .models import Endpoint, EndpointType
from .tables import EndpointTable, EndpointTypeTable


#
# EndpointType Views
#


class EndpointTypeListView(generic.ObjectListView):
    """List view for EndpointType objects."""

    queryset = EndpointType.objects.annotate(
        endpoint_count=Count("endpoints")
    ).prefetch_related("manufacturer", "tags")
    table = EndpointTypeTable
    filterset = EndpointTypeFilterSet
    filterset_form = EndpointTypeFilterForm


class EndpointTypeView(generic.ObjectView):
    """Detail view for EndpointType objects."""

    queryset = EndpointType.objects.prefetch_related("manufacturer", "default_platform", "tags")

    def get_extra_context(self, request, instance):
        endpoints = Endpoint.objects.filter(endpoint_type=instance)
        endpoints_table = EndpointTable(endpoints, user=request.user)
        endpoints_table.configure(request)

        return {
            "endpoints_table": endpoints_table,
            "endpoint_count": endpoints.count(),
        }


class EndpointTypeEditView(generic.ObjectEditView):
    """Create/Edit view for EndpointType objects."""

    queryset = EndpointType.objects.all()
    form = EndpointTypeForm


class EndpointTypeDeleteView(generic.ObjectDeleteView):
    """Delete view for EndpointType objects."""

    queryset = EndpointType.objects.all()


class EndpointTypeBulkImportView(generic.BulkImportView):
    """Bulk import view for EndpointType objects."""

    queryset = EndpointType.objects.all()
    model_form = EndpointTypeImportForm


class EndpointTypeBulkEditView(generic.BulkEditView):
    """Bulk edit view for EndpointType objects."""

    queryset = EndpointType.objects.prefetch_related("manufacturer", "tags")
    filterset = EndpointTypeFilterSet
    table = EndpointTypeTable
    form = EndpointTypeBulkEditForm


class EndpointTypeBulkDeleteView(generic.BulkDeleteView):
    """Bulk delete view for EndpointType objects."""

    queryset = EndpointType.objects.all()
    filterset = EndpointTypeFilterSet
    table = EndpointTypeTable


#
# Endpoint Views
#


class EndpointListView(generic.ObjectListView):
    """List view for Endpoint objects."""

    queryset = Endpoint.objects.prefetch_related(
        "endpoint_type",
        "endpoint_type__manufacturer",
        "site",
        "location",
        "tenant",
        "contact",
        "primary_ip4",
        "tags",
    )
    table = EndpointTable
    filterset = EndpointFilterSet
    filterset_form = EndpointFilterForm


class EndpointView(generic.ObjectView):
    """Detail view for Endpoint objects."""

    queryset = Endpoint.objects.prefetch_related(
        "endpoint_type",
        "endpoint_type__manufacturer",
        "site",
        "location",
        "tenant",
        "contact",
        "platform",
        "primary_ip4",
        "primary_ip6",
        "connected_interface",
        "tags",
    )


class EndpointEditView(generic.ObjectEditView):
    """Create/Edit view for Endpoint objects."""

    queryset = Endpoint.objects.all()
    form = EndpointForm


class EndpointDeleteView(generic.ObjectDeleteView):
    """Delete view for Endpoint objects."""

    queryset = Endpoint.objects.all()


class EndpointBulkImportView(generic.BulkImportView):
    """Bulk import view for Endpoint objects."""

    queryset = Endpoint.objects.all()
    model_form = EndpointImportForm


class EndpointBulkEditView(generic.BulkEditView):
    """Bulk edit view for Endpoint objects."""

    queryset = Endpoint.objects.prefetch_related("endpoint_type", "site", "tags")
    filterset = EndpointFilterSet
    table = EndpointTable
    form = EndpointBulkEditForm


class EndpointBulkDeleteView(generic.BulkDeleteView):
    """Bulk delete view for Endpoint objects."""

    queryset = Endpoint.objects.all()
    filterset = EndpointFilterSet
    table = EndpointTable
