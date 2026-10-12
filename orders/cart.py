"""Логика корзины на сессии."""
from __future__ import annotations
from decimal import Decimal
from products.models import Product

CART_SESSION_KEY = "cart"


class Cart:
    def __init__(self, request):
        self.session = request.session
        self.cart: dict[str, dict] = self.session.get(CART_SESSION_KEY, {})
        if CART_SESSION_KEY not in self.session:
            self.session[CART_SESSION_KEY] = {}

    def add(self, product: Product, quantity: int = 1) -> None:
        pid = str(product.id)
        if pid not in self.cart:
            self.cart[pid] = {"price": str(product.price), "qty": 0}
        self.cart[pid]["qty"] = min(self.cart[pid]["qty"] + quantity, product.stock)
        self.save()

    def update(self, product_id: int, quantity: int) -> None:
        pid = str(product_id)
        if pid in self.cart:
            if quantity <= 0:
                del self.cart[pid]
            else:
                product = Product.objects.get(id=product_id)
                self.cart[pid]["qty"] = min(quantity, product.stock)
            self.save()

    def remove(self, product_id: int) -> None:
        self.cart.pop(str(product_id), None)
        self.save()

    def clear(self) -> None:
        self.session[CART_SESSION_KEY] = {}
        self.save()

    def save(self) -> None:
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        mapping = {str(p.id): p for p in products}
        for pid, item in self.cart.items():
            product = mapping.get(pid)
            if product is None:
                continue
            yield {
                "product": product,
                "quantity": item["qty"],
                "price": Decimal(item["price"]),
                "total": Decimal(item["price"]) * item["qty"],
            }

    def __len__(self) -> int:
        return sum(i["qty"] for i in self.cart.values())

    def get_total(self) -> Decimal:
        return sum(
            (Decimal(i["price"]) * i["qty"] for i in self.cart.values()),
            Decimal("0"),
        )