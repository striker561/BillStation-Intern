from django.urls import path
# from rest_framework_simplejwt.views import TokenRefreshView
from accounts.views import RegisterView, LoginView, RequestTokenView, ResetView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Auth API",
        default_version="v1",
        description="Intern Task: Django Authentication System with PostgreSQL, Redis & Deployment",
    ),
    public=True,
)

urlpatterns = [
    path("api/register/", RegisterView.as_view(), name="register"),
    path("api/login/", LoginView.as_view(), name="login"),
    path("api/request-recovery/", RequestTokenView.as_view(), name="request-recovery"),
    path("api/reset/", ResetView.as_view(), name="reset-password"),
    # path("api/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
