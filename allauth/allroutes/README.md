# allauth.allroutes

Route-based checks for the four selected django-allauth vulnerability targets.

Register in your Django project:

```python
from django.urls import include, path

urlpatterns = [
    path("routes/", include("allauth.allroutes.urls")),
]
```

Routes:

- `/routes/notion/`
- `/routes/okta/`
- `/routes/netiq/`
- `/routes/idp/`

Each route returns JSON containing `passed`, `checks`, and `data`.
