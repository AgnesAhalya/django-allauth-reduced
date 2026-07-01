from django.urls import include, path

from . import views

app_name = "allroutes"

urlpatterns = [
    path("notion/", views.notion, name="notion"),
    path("okta/", views.okta, name="okta"),
    path("netiq/", views.netiq, name="netiq"),
    path("idp/", views.idp, name="idp"),

    # MFA recovery codes
    path("accounts/2fa/recovery-codes/", include("allauth.mfa.recovery_codes.urls")),

    # Instagram provider
    path("accounts/", include("allauth.socialaccount.providers.instagram.urls")),

    # IDP/OIDC provider
    path("idp/oidc/", include("allauth.idp.urls")),
]