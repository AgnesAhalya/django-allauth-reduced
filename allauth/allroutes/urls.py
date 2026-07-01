from django.urls import path

from . import views as allroute_views
from allauth.idp.oidc import views as oidc_views
from allauth.mfa.recovery_codes import views as recovery_views
from allauth.socialaccount.providers.instagram import views as instagram_views


app_name = "allroutes"

urlpatterns = [
    path("notion/", allroute_views.notion, name="notion"),
    path("okta/", allroute_views.okta, name="okta"),
    path("netiq/", allroute_views.netiq, name="netiq"),
    path("idp/", allroute_views.idp, name="idp"),


    path("accounts/2fa/recovery-codes/download/", allroute_views.download_recovery_codes, name="mfa_download_recovery_codes"),

    path("accounts/instagram/login/", allroute_views.oauth2_login, name="instagram_login"),
    path("accounts/instagram/login/callback/", allroute_views.oauth2_callback, name="instagram_callback"),

    path("idp/oidc/identity/o/authorize", allroute_views.authorization, name="authorization"),
    path("idp/oidc/identity/o/device", oidc_views.device_authorization, name="device_authorization"),

    # path("accounts/2fa/recovery-codes/", include("allauth.mfa.recovery_codes.urls")),
    # path("accounts/", include("allauth.socialaccount.providers.instagram.urls")),
    # path("idp/oidc/", include("allauth.idp.urls")),
]