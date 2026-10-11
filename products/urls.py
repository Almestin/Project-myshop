"""URL-маршруты приложения products."""
from django.urls import path

from .views import ProductDetailView, ProductListView

app_name = "products"

urlpatterns = [
    # Главная страница — тот же каталог
    path("", ProductListView.as_view(), name="list"),
    # Альтернативный URL /products/ — тот же каталог
    path("products/", ProductListView.as_view(), name="products"),
    # Детальная страница товара
    path("product/<slug:slug>/", ProductDetailView.as_view(), name="detail"),
]