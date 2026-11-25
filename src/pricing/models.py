"""Modelos de dominio del motor de precios."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CartItem:
    """Un ítem del carrito.

    Attributes:
        name: Nombre visible del producto.
        category: Categoría comercial (por ejemplo ``HOGAR`` o ``ELECTRONICA``).
        unit_price: Precio unitario en pesos.
        quantity: Cantidad de unidades.
    """

    name: str
    category: str
    unit_price: float
    quantity: int
