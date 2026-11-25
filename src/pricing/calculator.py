"""Cálculo de importes del carrito.

Implementa las reglas de ``specs/TICKET-104.md``: descuento por volumen, cupón
promocional no acumulable y tope para productos de electrónica.
"""

from .models import CartItem

VOLUME_THRESHOLD = 100000.0
VOLUME_DISCOUNT = 0.10
COUPON_BIENVENIDA15 = "BIENVENIDA15"
COUPON_DISCOUNT = 0.15
ELECTRONICS_CATEGORY = "ELECTRONICA"
ELECTRONICS_MAX_DISCOUNT = 0.10


def calculate_subtotal(items: list[CartItem]) -> float:
    """Suma ``unit_price * quantity`` y normaliza a 2 decimales."""
    total = sum(item.unit_price * item.quantity for item in items)
    return round(max(0.0, total), 2)


def calculate_discount_rate(
    items: list[CartItem],
    coupon_code: str | None = None,
) -> float:
    """Devuelve la tasa de descuento aplicable, entre 0 y 1.

    Los descuentos no se acumulan: prevalece el mayor. Si el carrito contiene
    electrónica, la tasa total queda topeada en 10%.
    """
    rate = 0.0

    if calculate_subtotal(items) > VOLUME_THRESHOLD:
        rate = VOLUME_DISCOUNT

    if coupon_code == COUPON_BIENVENIDA15:
        rate = max(rate, COUPON_DISCOUNT)

    has_electronics = any(item.category == ELECTRONICS_CATEGORY for item in items)
    if has_electronics:
        rate = min(rate, ELECTRONICS_MAX_DISCOUNT)

    return rate


def calculate_final_total(
    items: list[CartItem],
    coupon_code: str | None = None,
) -> float:
    """Devuelve el monto a facturar, ya con descuentos aplicados."""
    rate = calculate_discount_rate(items, coupon_code)
    total = calculate_subtotal(items) * (1 - rate)
    return round(max(0.0, total), 2)
