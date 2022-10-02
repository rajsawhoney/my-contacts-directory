"""phone_directory URL Configuration"""

from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path, re_path,include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Contacts Directory",
        default_version='v1',
        description="API Docs for Contacts Directory",
        terms_of_service="https://rajsahani.com.np",
        contact=openapi.Contact(email="rajsahani1819@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/',include('accounts.urls')),
    path('api/contacts/',include('contacts.urls')),
    re_path(r'^docs(?P<format>\.json|\.yaml)$', schema_view.without_ui(
        cache_timeout=0), name='schema-json'),
    re_path(r'^docs/$', schema_view.with_ui('swagger',
            cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc',
            cache_timeout=0), name='schema-redoc'),
    re_path(r'^.*', TemplateView.as_view(template_name='index.html'))
]
