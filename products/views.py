"""Представления каталога товаров."""
from __future__ import annotations

from django.db.models import Avg
from django.views.generic import DetailView, ListView

from .filters import ProductFilter
from .models import Category, Product


class ProductListView(ListView):
    """Каталог товаров с фильтрами, поиском и сортировкой."""

    model = Product
    template_name = "products/list.html"
    context_object_name = "products"
    paginate_by = 9

    def get_queryset(self):
        qs = (
            Product.objects.filter(is_active=True)
            .select_related("category")
            .annotate(avg_rating=Avg("reviews__rating"))
        )

        # Применяем фильтры из django-filter
        self.filterset = ProductFilter(self.request.GET, queryset=qs)
        qs = self.filterset.qs

        # Сортировка
        ordering = self.request.GET.get("sort", "-created_at")
        allowed = {"price", "-price", "-created_at", "name", "-avg_rating"}
        if ordering in allowed:
            qs = qs.order_by(ordering)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["filter"] = self.filterset
        ctx["categories"] = Category.objects.all()
        ctx["current_sort"] = self.request.GET.get("sort", "-created_at")
        ctx["selected_category"] = self.request.GET.getlist("category")
        return ctx


class ProductDetailView(DetailView):
    """Детальная страница товара с отзывами."""

    model = Product
    template_name = "products/detail.html"
    context_object_name = "product"

    def get_queryset(self):
        return (
            Product.objects.filter(is_active=True)
            .select_related("category")
            .prefetch_related("reviews__user")
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # Список отзывов
        ctx["reviews"] = self.object.reviews.select_related("user")

        # Форма для отзыва
        from reviews.forms import ReviewForm
        ctx["review_form"] = ReviewForm()

        # Может ли текущий пользователь оставить отзыв?
        ctx["can_review"] = self._can_review()
        return ctx

    def _can_review(self) -> bool:
        """Отзыв доступен только после покупки и только один раз."""
        user = self.request.user
        if not user.is_authenticated:
            return False

        from orders.models import OrderItem

        purchased = OrderItem.objects.filter(
            order__user=user,
            product=self.object,
            order__status__in=["paid", "shipped", "delivered"],
        ).exists()
        already = self.object.reviews.filter(user=user).exists()
        return purchased and not already
