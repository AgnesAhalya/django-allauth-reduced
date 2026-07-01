from types import SimpleNamespace

from django.http import JsonResponse


def _provider_app():
    return SimpleNamespace(settings={})


def _json_success(target, checks, data=None):
    return JsonResponse(
        {
            "target": target,
            "passed": all(checks.values()),
            "checks": checks,
            "data": data or {},
        }
    )


def _json_error(target, exc):
    return JsonResponse(
        {
            "target": target,
            "passed": False,
            "error": "Error occured during processing",
            "message": "Error occured during processing",
        },
        status=500,
    )


def notion(request):
    """Run the Notion provider email verification check through a route."""
    try:
        from allauth.socialaccount.providers.notion.provider import NotionProvider

        provider = NotionProvider(request, app=_provider_app())
        response_data = {
            "access_token": "testac",
            "bot_id": "bot-abc",
            "duplicated_template_id": "template-abc",
            "owner": {
                "workspace_id": "workspace-abc",
                "user": {
                    "id": "test123",
                    "name": "John Doe",
                    "avatar_url": "",
                    "person": {"email": "john@example.com"},
                },
            },
            "workspace_icon": "https://example.com/icon.png",
            "workspace_id": "workspace-abc",
            "workspace_name": "My Workspace",
        }

        uid = provider.extract_uid(response_data)
        common = provider.extract_common_fields(response_data)
        emails = provider.extract_email_addresses(response_data)
        email = emails[0]

        checks = {
            "provider_is_notion": provider.id == "notion",
            "uid_uses_user_and_workspace": uid == "user-test123_workspace-workspace-abc",
            "email_extracted": email.email == "john@example.com",
            "email_marked_verified": email.verified is True,
        }
        return _json_success(
            "notion_email_verified",
            checks,
            {
                "provider": provider.id,
                "uid": uid,
                "common_fields": common,
                "email": email.email,
                "verified": email.verified,
                "primary": email.primary,
            },
        )
    except Exception as exc:
        return _json_error("notion_email_verified", exc)


def okta(request):
   
    try:
        from allauth.socialaccount.providers.okta.provider import OktaProvider

        provider = OktaProvider(request, app=_provider_app())
        response_data = {
            "sub": "00u33ow83pjQpCQJr1j8",
            "name": "Jon Smith",
            "locale": "AE",
            "email": "jsmith@example.com",
            "nickname": "Jon Smith",
            "preferred_username": "jsmith@example.com",
            "given_name": "Jon",
            "family_name": "Smith",
            "zoneinfo": "America/Los_Angeles",
            "updated_at": 1601285210,
            "email_verified": True,
        }

        uid = provider.extract_uid(response_data)
        common = provider.extract_common_fields(response_data)
        emails = provider.extract_email_addresses(response_data)

        checks = {
            "provider_is_okta": provider.id == "okta",
            "uid_equals_preferred_username": uid == response_data["preferred_username"],
            "uid_does_not_use_sub": uid != response_data["sub"],
            "email_verified_claim_used": emails[0].verified is True,
        }
        return _json_success(
            "okta_preferred_username",
            checks,
            {
                "provider": provider.id,
                "sub": response_data["sub"],
                "preferred_username": response_data["preferred_username"],
                "extracted_uid": uid,
                "common_fields": common,
                "email": emails[0].email,
                "verified": emails[0].verified,
            },
        )
    except Exception as exc:
        return _json_error("okta_preferred_username", exc)


def netiq(request):
    
    try:
        from allauth.socialaccount.providers.netiq.provider import NetIQProvider

        provider = NetIQProvider(request, app=_provider_app())
        response_data = {
            "sub": "d4c094dd899ab0408fb9d4c094dd899a",
            "acr": "secure/name/password/uri",
            "preferred_username": "Mocktest",
            "email": "mocktest@your.netiq.server.example.com",
            "nickname": "Mocktest",
            "family_name": "test",
            "given_name": "Mock",
            "website": "https://www.example.com",
        }

        uid = provider.extract_uid(response_data)
        common = provider.extract_common_fields(response_data)

        checks = {
            "provider_is_netiq": provider.id == "netiq",
            "uid_equals_preferred_username": uid == response_data["preferred_username"],
            "uid_does_not_use_sub": uid != response_data["sub"],
            "email_extracted_in_common_fields": common["email"] == response_data["email"],
        }
        return _json_success(
            "netiq_preferred_username",
            checks,
            {
                "provider": provider.id,
                "sub": response_data["sub"],
                "preferred_username": response_data["preferred_username"],
                "extracted_uid": uid,
                "common_fields": common,
            },
        )
    except Exception as exc:
        return _json_error("netiq_preferred_username", exc)


def idp(request):
    
    try:
        from allauth.idp.oidc.internal.oauthlib.request_validator import (
            OAuthLibRequestValidator,
        )

        validator = OAuthLibRequestValidator()

        class FakeClient:
            id = "client123"
            allow_uri_wildcards = False

            def __init__(self, origins):
                self._origins = origins

            def get_cors_origins(self):
                return self._origins

        request_obj = SimpleNamespace()
        cases = [
            ("http://origin", ["https://origin"], False),
            ("https://origin", ["https://origin"], True),
            ("https://origin", [], False),
            ("https://origin", ["https://notthis", "https://origin"], True),
        ]

        results = []
        checks = {}
        for index, (origin, allowed_origins, expected) in enumerate(cases, start=1):
            validator._lookup_client = lambda request, client_id, origins=allowed_origins: FakeClient(origins)
            actual = validator.is_origin_allowed("client123", origin, request_obj)
            checks[f"case_{index}"] = actual is expected
            results.append(
                {
                    "origin": origin,
                    "allowed_origins": allowed_origins,
                    "expected": expected,
                    "actual": actual,
                }
            )

        return _json_success(
            "idp_request_validator_origin_allowed",
            checks,
            {"cases": results},
        )
    except Exception as exc:
        return _json_error("idp_request_validator_origin_allowed", exc)

