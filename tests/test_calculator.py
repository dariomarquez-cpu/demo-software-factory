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

    # Subtotal 100.000: no supera el umbral de volumen, así que no hay descuento.
    assert calculate_final_total(items) == 100000.0


# --- Tests de aceptación TICKET-104 (estado inicial: rojo) ---


def test_descuento_volumen_mayor_100k():
    items = [CartItem(name="Teclado", category="ACCESORIOS", unit_price=60000.0, quantity=2)]

    # Subtotal 120.000 -> 10% de descuento por volumen = 108.000
    assert calculate_final_total(items) == 108000.0


def test_cupon_bienvenida_15():
    items = [CartItem(name="Mochila", category="HOGAR", unit_price=50000.0, quantity=1)]

    # Subtotal 50.000 -> 15% del cupón = 42.500
    assert calculate_final_total(items, coupon_code="BIENVENIDA15") == 42500.0


def test_no_acumula_descuentos_toma_el_mayor():
    items = [CartItem(name="Silla", category="HOGAR", unit_price=120000.0, quantity=1)]

    # Subtotal 120.000: volumen 10% vs cupón 15% -> prevalece el mayor = 102.000
    assert calculate_final_total(items, coupon_code="BIENVENIDA15") == 102000.0


def test_tope_10_porciento_si_hay_electronica_con_cupon():
    items = [CartItem(name="Notebook", category="ELECTRONICA", unit_price=150000.0, quantity=1)]

    # Subtotal 150.000 con ELECTRONICA y cupón 15% -> tope total 10% = 135.000
    assert calculate_final_total(items, coupon_code="BIENVENIDA15") == 135000.0


def test_electronica_sin_volumen_igual_aplica_tope():
    items = [CartItem(name="Auriculares", category="ELECTRONICA", unit_price=90000.0, quantity=1)]

    # Subtotal 90.000 (no hay volumen) con cupón -> el tope de 10% igual aplica = 81.000
    assert calculate_final_total(items, coupon_code="BIENVENIDA15") == 81000.0
