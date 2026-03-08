from django.urls import path
from . import views

app_name = "tracker"

urlpatterns = [
    path("", views.request_list, name="request_list"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("export/csv/", views.request_export_csv, name="request_export_csv"),
    path("requests/new/", views.request_create, name="request_create"),
    path("requests/<int:pk>/", views.request_detail, name="request_detail"),
    path("requests/<int:pk>/edit/", views.request_update, name="request_update"),
    path("requests/<int:pk>/delete/", views.request_delete, name="request_delete"),
]