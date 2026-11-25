"""Cálculo de importes del carrito.

Estado base previo a TICKET-104: solo se calcula el subtotal.
Las reglas de descuento están especificadas en ``specs/TICKET-104.md``.
"""

from .models import CartItem


def calculate_subtotal(items: list[CartItem]) -> float:
    """Suma ``unit_price * quantity`` y normaliza a 2 decimales."""
    total = sum(item.unit_price * item.quantity for item in items)
    return round(max(0.0, total), 2)


def calculate_final_total(
    items: list[CartItem],
    coupon_code: str | None = None,
) -> float:
    """Devuelve el monto a facturar.

    Implementación base: todavía no aplica las reglas de TICKET-104, por eso
    ``coupon_code`` se acepta pero no se usa.
    """
    return calculate_subtotal(items)
