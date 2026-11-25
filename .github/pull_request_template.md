## Qué hace este PR

<!-- Una línea: qué comportamiento agrega o corrige, con el ticket asociado. -->

Closes #

## Evidencia de convergencia

<!-- Pegar números reales del último ./scripts/converge.sh, no promesas. -->

- Tests: __/__ pasando
- Cobertura de ramas en `src/pricing/`: __%
- `ruff`: __ errores

## Checklist anti-fruta

- [ ] El diff toca únicamente `src/` (y, si corresponde, `tests/` con tests nuevos aprobados).
- [ ] Ningún test existente fue debilitado, borrado ni saltado (`xfail`, `skip`).
- [ ] Los casos borde de la spec están cubiertos por un test que falla sin el cambio.
- [ ] La evidencia de arriba salió de una corrida local real, no está escrita a mano.
- [ ] Revisé la lógica de negocio, no solo que el CI esté verde.
