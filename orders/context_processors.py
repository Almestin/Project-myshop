"""Контекст-процессоры приложения orders."""
from __future__ import annotations

from django.http import HttpRequest


def cart_summary(request: HttpRequest) -> dict:
    """Добавляет в контекст всех шаблонов количество товаров в корзине.

    Пока корзина не реализована (шаг 6), возвращает 0.
    После реализации шага 6 функция будет использовать Cart из orders.cart.
    """
    return {"cart_total_qty": 0}