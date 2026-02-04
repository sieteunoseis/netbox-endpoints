"""API URL configuration for NetBox Endpoints plugin."""

from netbox.api.routers import NetBoxRouter

from . import views

router = NetBoxRouter()
router.register("endpoint-types", views.EndpointTypeViewSet)
router.register("endpoints", views.EndpointViewSet)

urlpatterns = router.urls
