"""Модели пользователей и адресов."""
from __future__ import annotations

from django.conf import settings
from django.db import models


class Address(models.Model):
    """Адрес доставки пользователя."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="addresses",
    )
    title = models.CharField(max_length=64, help_text="Например, «Дом»")
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=32)
    address_line = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    is_default = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.title} — {self.city}"