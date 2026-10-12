"""Представления для отзывов."""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from products.models import Product
from orders.models import OrderItem
from .forms import ReviewForm


class ReviewCreateView(LoginRequiredMixin, View):
    """Добавление отзыва (только после покупки)."""

    def post(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        purchased = OrderItem.objects.filter(
            order__user=request.user,
            product=product,
            order__status__in=["paid", "shipped", "delivered"],
        ).exists()
        if not purchased:
            messages.error(request, "Отзыв доступен только после покупки.")
            return redirect(product.get_absolute_url())

        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, "Спасибо за отзыв!")
        else:
            messages.error(request, "Проверьте форму.")
        return redirect(product.get_absolute_url())
