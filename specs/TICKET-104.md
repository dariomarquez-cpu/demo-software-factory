# TICKET-104 — Descuentos por volumen y cupón en el checkout

## Contexto

Necesitamos calcular el descuento final de un carrito de compras antes de facturar.
La implementación actual (`src/pricing/calculator.py`) solo calcula el subtotal: no aplica ninguna regla de descuento.

## Reglas de negocio

1. Si el subtotal **supera** los `100000`, aplicar un `10%` de descuento por volumen.
2. Si el usuario ingresa el cupón `BIENVENIDA15`, aplicar un `15%` de descuento.
3. **Restricción crítica — no acumulable con tope:** los descuentos **no se suman** (10% + 15% ≠ 25%).
   Si aplican ambos, prevalece el mayor (15%). **Excepción:** si el carrito contiene al menos un producto de
   categoría `ELECTRONICA`, el descuento máximo permitido en total es del `10%`, incluso con cupón.
4. El monto final nunca puede ser negativo y debe redondearse a 2 decimales.

## Casos borde obligatorios

| Subtotal | Cupón        | Categorías presentes | Descuento esperado | Total     |
|----------|--------------|----------------------|--------------------|-----------|
| 50000    | —            | HOGAR                | 0%                 | 50000.00  |
| 120000   | —            | ACCESORIOS           | 10% (volumen)      | 108000.00 |
| 50000    | BIENVENIDA15 | HOGAR                | 15% (cupón)        | 42500.00  |
| 120000   | BIENVENIDA15 | HOGAR                | 15% (el mayor)     | 102000.00 |
| 150000   | BIENVENIDA15 | ELECTRONICA          | 10% (tope)         | 135000.00 |
| 90000    | BIENVENIDA15 | ELECTRONICA          | 10% (tope, sin volumen) | 81000.00 |

> La quinta fila es la trampa del ticket: un cálculo apurado aplica 15% y devuelve `127500.00`.
> La sexta fila es la segunda trampa: el tope de `ELECTRONICA` aplica aunque no haya descuento por volumen.

## Criterios de aceptación (métrica de convergencia)

- `100%` de los tests pasan.
- Cobertura de ramas en `src/pricing/` `>= 95%`.
- `ruff` sin errores.

Verificación: `./scripts/converge.sh`

## Fuera de alcance

- Persistencia, API HTTP, UI, autenticación.
- Cupones distintos de `BIENVENIDA15`.
- Impuestos, envío y múltiples monedas.
- Modificar tests existentes o el script de convergencia.
