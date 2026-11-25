"""Tests del motor de precios.

En ``main`` solo vive el comportamiento actual: cálculo de subtotal y total sin
descuentos. Los tests de aceptación de TICKET-104 viven en la rama ``demo-ready``.
"""

from src.pricing.calculator import calculate_final_total, calculate_subtotal
from src.pricing.models import CartItem


def test_subtotal_basico():
    items = [CartItem(name="Mouse", category="ACCESORIOS", unit_price=25000.0, quantity=2)]

    assert calculate_subtotal(items) == 50000.0


def test_subtotal_carrito_vacio_es_cero():
    assert calculate_subtotal([]) == 0.0


def test_subtotal_redondea_a_dos_decimales():
    items = [CartItem(name="Cable", category="ACCESORIOS", unit_price=19.999, quantity=1)]

    assert calculate_subtotal(items) == 20.0


def test_subtotal_nunca_es_negativo():
    items = [CartItem(name="Ajuste", category="HOGAR", unit_price=-100.0, quantity=2)]

    assert calculate_subtotal(items) == 0.0


def test_final_total_sin_descuentos_igual_al_subtotal():
    items = [
        CartItem(name="Mochila", category="HOGAR", unit_price=50000.0, quantity=1),
        CartItem(name="Mouse", category="ACCESORIOS", unit_price=25000.0, quantity=2),
    ]

    assert calculate_final_total(items) == 100000.0
    assert calculate_final_total(items, coupon_code="BIENVENIDA15") == 100000.0
