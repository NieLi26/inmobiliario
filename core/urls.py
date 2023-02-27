from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django admin
    path("admin/", admin.site.urls),
    # tailwind development
    path("__reload__/", include("django_browser_reload.urls")),
    # Local apps
    path("accounts/", include("apps.accounts.urls")),
    # User management
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("apps.pages.urls", namespace="pages")),
    path("properties/", include("apps.properties.urls",
                                namespace="properties")),
    path("newsletters/", include("apps.newsletters.urls",
                                 namespace="newsletters")),
    path("reports/", include("apps.reports.urls",
                               namespace="reports")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
