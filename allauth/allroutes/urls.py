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

    path("accounts/2fa/recovery-codes/", recovery_views.view_recovery_codes, name="mfa_view_recovery_codes"),
    path("accounts/2fa/recovery-codes/generate/", recovery_views.generate_recovery_codes, name="mfa_generate_recovery_codes"),
    path("accounts/2fa/recovery-codes/download/", recovery_views.download_recovery_codes, name="mfa_download_recovery_codes"),

    path("accounts/instagram/login/", instagram_views.oauth2_login, name="instagram_login"),
    path("accounts/instagram/login/callback/", instagram_views.oauth2_callback, name="instagram_callback"),

    path("idp/oidc/.well-known/openid-configuration", oidc_views.configuration, name="configuration"),
    path("idp/oidc/.well-known/jwks.json", oidc_views.jwks, name="jwks"),
    path("idp/oidc/identity/o/authorize", oidc_views.authorization, name="authorization"),
    path("idp/oidc/identity/o/device", oidc_views.device_authorization, name="device_authorization"),
    path("idp/oidc/identity/o/api/token", oidc_views.token, name="token"),
    path("idp/oidc/identity/o/api/revoke", oidc_views.revoke, name="revoke"),
    path("idp/oidc/identity/o/api/userinfo", oidc_views.user_info, name="userinfo"),
    path("idp/oidc/identity/o/api/device/code", oidc_views.device_code, name="device_code"),

    # path("accounts/2fa/recovery-codes/", include("allauth.mfa.recovery_codes.urls")),
    # path("accounts/", include("allauth.socialaccount.providers.instagram.urls")),
    # path("idp/oidc/", include("allauth.idp.urls")),
]