"""URL-маршруты корзины."""
from django.urls import path
from . import views_cart

app_name = "cart"

urlpatterns = [
    path("", views_cart.cart_detail, name="detail"),
    path("add/<int:product_id>/", views_cart.cart_add, name="add"),
    path("update/<int:product_id>/", views_cart.cart_update, name="update"),
    path("remove/<int:product_id>/", views_cart.cart_remove, name="remove"),
]