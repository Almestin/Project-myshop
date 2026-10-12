"""Представления корзины."""
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from products.models import Product
from .cart import Cart


def cart_detail(request):
    cart = Cart(request)
    return render(request, "orders/cart.html", {"cart": cart})


@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    try:
        qty = int(request.POST.get("quantity", 1))
    except ValueError:
        qty = 1
    if product.stock == 0:
        messages.error(request, "Товар отсутствует на складе.")
        return redirect(product.get_absolute_url())
    Cart(request).add(product, qty)
    messages.success(request, f"«{product.name}» добавлен в корзину.")
    return redirect("cart:detail")


@require_POST
def cart_update(request, product_id):
    qty = int(request.POST.get("quantity", 1))
    Cart(request).update(product_id, qty)
    return redirect("cart:detail")


@require_POST
def cart_remove(request, product_id):
    Cart(request).remove(product_id)
    return redirect("cart:detail")