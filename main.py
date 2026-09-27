from pathlib import Path

content = '''\
"""Small Python fixture repository for testing RepoLens.

This file intentionally includes:
- standard-library imports
- a constant
- standalone functions
- a class with methods
- an async function
- type hints
- function-to-function calls
- class method calls
- exception handling
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable

APP_NAME = "RepoLens Fixture"
DEFAULT_TAX_RATE = 0.20


def calculate_subtotal(prices: Iterable[float]) -> float:
    """Return the sum of all supplied prices."""
    return sum(prices)


def apply_discount(amount: float, discount_percent: float) -> float:
    """Apply a percentage discount to an amount."""
    if not 0 <= discount_percent <= 100:
        raise ValueError("discount_percent must be between 0 and 100")

    return amount * (1 - discount_percent / 100)


def calculate_tax(amount: float, tax_rate: float = DEFAULT_TAX_RATE) -> float:
    """Calculate tax for an amount."""
    if tax_rate < 0:
        raise ValueError("tax_rate cannot be negative")

    return amount * tax_rate


@dataclass
class Order:
    """Simple order model used by the test application."""

    customer_name: str
    prices: list[float]
    discount_percent: float = 0.0

    def subtotal(self) -> float:
        """Return the order subtotal."""
        return calculate_subtotal(self.prices)

    def discounted_subtotal(self) -> float:
        """Return subtotal after discount."""
        return apply_discount(self.subtotal(), self.discount_percent)

    def total(self) -> float:
        """Return the final order total including tax."""
        discounted = self.discounted_subtotal()
        return discounted + calculate_tax(discounted)


class OrderService:
    """Service responsible for validating and summarising orders."""

    def validate_order(self, order: Order) -> bool:
        """Validate that an order contains a customer and at least one price."""
        return bool(order.customer_name.strip()) and bool(order.prices)

    def build_summary(self, order: Order) -> dict[str, float | str]:
        """Return a structured summary for a valid order."""
        if not self.validate_order(order):
            raise ValueError("Invalid order")

        return {
            "customer": order.customer_name,
            "subtotal": round(order.subtotal(), 2),
            "total": round(order.total(), 2),
        }


async def process_order(order: Order, service: OrderService) -> dict[str, float | str]:
    """Async wrapper that processes an order through OrderService."""
    return service.build_summary(order)


def estimate_items_from_total(total: float, average_item_price: float) -> int:
    """Estimate item count using a deliberately simple calculation."""
    if average_item_price <= 0:
        raise ValueError("average_item_price must be greater than zero")

    return math.ceil(total / average_item_price)


def main() -> None:
    """Run a tiny demonstration."""
    order = Order(
        customer_name="Test User",
        prices=[12.50, 7.25, 5.00],
        discount_percent=10,
    )

    service = OrderService()
    summary = service.build_summary(order)

    print(APP_NAME)
    print(summary)


if __name__ == "__main__":
    main()
'''

path = Path("/mnt/data/repolens_test_app.py")
path.write_text(content, encoding="utf-8")

print(f"Created {path}")
