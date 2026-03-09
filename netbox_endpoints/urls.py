"""URL configuration for NetBox Endpoints plugin."""

from django.urls import path
from netbox.views.generic import ObjectChangeLogView, ObjectJournalView

from . import models, views

urlpatterns = [
    #
    # EndpointType URLs
    #
    path(
        "endpoint-types/",
        views.EndpointTypeListView.as_view(),
        name="endpointtype_list",
    ),
    path(
        "endpoint-types/add/",
        views.EndpointTypeEditView.as_view(),
        name="endpointtype_add",
    ),
    path(
        "endpoint-types/import/",
        views.EndpointTypeBulkImportView.as_view(),
        name="endpointtype_import",
    ),
    path(
        "endpoint-types/edit/",
        views.EndpointTypeBulkEditView.as_view(),
        name="endpointtype_bulk_edit",
    ),
    path(
        "endpoint-types/delete/",
        views.EndpointTypeBulkDeleteView.as_view(),
        name="endpointtype_bulk_delete",
    ),
    path(
        "endpoint-types/<int:pk>/",
        views.EndpointTypeView.as_view(),
        name="endpointtype",
    ),
    path(
        "endpoint-types/<int:pk>/edit/",
        views.EndpointTypeEditView.as_view(),
        name="endpointtype_edit",
    ),
    path(
        "endpoint-types/<int:pk>/delete/",
        views.EndpointTypeDeleteView.as_view(),
        name="endpointtype_delete",
    ),
    path(
        "endpoint-types/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="endpointtype_changelog",
        kwargs={"model": models.EndpointType},
    ),
    path(
        "endpoint-types/<int:pk>/journal/",
        ObjectJournalView.as_view(),
        name="endpointtype_journal",
        kwargs={"model": models.EndpointType},
    ),
    #
    # Endpoint URLs (at root since base_url is "endpoints")
    #
    path(
        "",
        views.EndpointListView.as_view(),
        name="endpoint_list",
    ),
    path(
        "add/",
        views.EndpointEditView.as_view(),
        name="endpoint_add",
    ),
    path(
        "import/",
        views.EndpointBulkImportView.as_view(),
        name="endpoint_import",
    ),
    path(
        "edit/",
        views.EndpointBulkEditView.as_view(),
        name="endpoint_bulk_edit",
    ),
    path(
        "delete/",
        views.EndpointBulkDeleteView.as_view(),
        name="endpoint_bulk_delete",
    ),
    path(
        "<int:pk>/",
        views.EndpointView.as_view(),
        name="endpoint",
    ),
    path(
        "<int:pk>/edit/",
        views.EndpointEditView.as_view(),
        name="endpoint_edit",
    ),
    path(
        "<int:pk>/delete/",
        views.EndpointDeleteView.as_view(),
        name="endpoint_delete",
    ),
    path(
        "<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="endpoint_changelog",
        kwargs={"model": models.Endpoint},
    ),
    path(
        "<int:pk>/journal/",
        ObjectJournalView.as_view(),
        name="endpoint_journal",
        kwargs={"model": models.Endpoint},
    ),
    # Widget HTMX endpoints
    path(
        "widget/endpoints-summary/",
        views.WidgetEndpointsSummaryContentView.as_view(),
        name="widget_endpoints_summary",
    ),
]


# Add URL patterns for views registered by other plugins
# These are added dynamically when those plugins register their views
def get_extra_urlpatterns():
    """Get URL patterns for views registered by other plugins."""
    from django.urls import path
    from utilities.views import registry

    extra_patterns = []
    views_dict = registry.get("views", {})
    endpoint_views = views_dict.get("netbox_endpoints", {}).get("endpoint", [])

    for view_config in endpoint_views:
        name = view_config.get("name")
        view_path = view_config.get("path")
        view_class = view_config.get("view")

        # Skip built-in views (journal, changelog)
        if name in ("journal", "changelog"):
            continue

        # Add URL pattern for this view
        if view_class and view_path:
            # Import the view class if it's a string
            if isinstance(view_class, str):
                from django.utils.module_loading import import_string

                view_class = import_string(view_class)

            extra_patterns.append(
                path(
                    f"<int:pk>/{view_path}/",
                    view_class.as_view(),
                    name=f"endpoint_{name}",
                )
            )

    return extra_patterns


# Extend urlpatterns with dynamically registered views
try:
    urlpatterns.extend(get_extra_urlpatterns())
except Exception:
    pass  # Fail silently if registry isn't ready yet
