"""Корневые URL-маршруты проекта."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("products.urls")),
    path("", include("reviews.urls")),
    path("cart/", include("orders.urls_cart")),
    path(
        "guides/",
        TemplateView.as_view(template_name="static/guides_recipes.html"),
        name="guides",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
