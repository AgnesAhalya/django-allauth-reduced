from django.urls import path

from . import views

app_name = "allroutes"

urlpatterns = [
    path("notion/", views.notion, name="notion"),
    path("okta/", views.okta, name="okta"),
    path("netiq/", views.netiq, name="netiq"),
    path("idp/", views.idp, name="idp"),
]