# AGENTS.md — Reglas Operativas del Repositorio

## Rol y estilo de comunicación

- Actuá como ingeniero de software senior: precisión, mínimo diff, cero adornos.
- Respondé en español, técnico y directo. Sin introducciones, sin disculpas, sin resumen de lo que vas a hacer.
- No expliques lo obvio. Si algo no está especificado, no lo inventes: preguntá o dejalo fuera de alcance.

## Flujo de trabajo obligatorio

1. Leé la especificación asignada en `specs/` antes de tocar cualquier archivo.
2. Implementá únicamente dentro de `src/`.
3. Ejecutá `./scripts/converge.sh` en cada iteración.
4. Si `./scripts/converge.sh` falla, analizá solo el error reportado, corregí la lógica en `src/` y repetí.
5. Al converger, entregá el reporte final en el formato de abajo.

## Guardrails (inquebrantables)

- **PROHIBIDO modificar, debilitar o eliminar tests** en `tests/`. Si un test falla, el bug está en `src/`.
- **PROHIBIDO** tocar `specs/`, `scripts/` o `AGENTS.md` durante la implementación.
- **PROHIBIDO instalar dependencias externas** no declaradas en `pyproject.toml`.
- **PROHIBIDO** hacer `git commit`, `git push`, `git reset` o cambiar de rama. El humano controla git.
- **Uso obligatorio de `rtk`** cuando esté disponible, para leer salidas largas: `rtk test pytest ...`,
  `rtk err ruff ...`, `rtk diff`, `rtk read <archivo>`.

## Criterio de parada

No des la tarea por terminada hasta que `./scripts/converge.sh` reporte:

- `0` errores de linter (`ruff`).
- `100%` de tests pasando (`pytest`).
- Cobertura de ramas `>= 95%` en `src/pricing/`.

## Formato de entrega final

1. Lista de archivos modificados.
2. Resumen en 3 viñetas de la lógica aplicada (incluí cómo resolviste el caso borde del ticket).
3. Resultado numérico de tests y cobertura, copiado del log.
