"""Фильтры для каталога товаров."""
from __future__ import annotations

import django_filters
from .models import Category, Product


class ProductFilter(django_filters.FilterSet):
    """Фильтр товаров по категории, диапазону цен и ключевому слову."""

    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        field_name="category",
        label="Категория",
    )
    min_price = django_filters.NumberFilter(
        field_name="price", lookup_expr="gte", label="Цена от",
    )
    max_price = django_filters.NumberFilter(
        field_name="price", lookup_expr="lte", label="Цена до",
    )
    q = django_filters.CharFilter(
        field_name="name", lookup_expr="icontains", label="Поиск",
    )

    class Meta:
        model = Product
        fields = ["category", "min_price", "max_price", "q"]