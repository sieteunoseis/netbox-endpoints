"""URL configuration for NetBox Endpoints plugin."""

from django.urls import path

from . import views

urlpatterns = [
    path("settings/", views.SettingsView.as_view(), name="settings"),
]
