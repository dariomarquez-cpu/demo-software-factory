# demo-software-factory

Repositorio de la charla **"De Vibe Coding a Software Factory: cómo automatizar con IA sin que genere fruta"**.

Contiene un caso de negocio mínimo (motor de descuentos de un checkout) pensado para mostrar el ciclo completo:

```
Ticket → Spec → Implementación → Convergencia (tests + cobertura + linter) → Pull Request
```

## Por qué este caso

La regla de negocio se entiende en 10 segundos, pero tiene una trampa: los descuentos no se acumulan y hay un tope
del 10% cuando el carrito tiene productos de categoría `ELECTRONICA`. Un modelo sin verificación suele aplicar el
15% del cupón e ignorar el tope. El bucle de convergencia lo detecta antes de que llegue a un PR.

## Estructura

```
.
├── AGENTS.md                     # Contrato operativo del agente (límites, criterio de parada)
├── RUNBOOK.md                    # Instalación + comandos para replicar el flujo
├── specs/
│   └── TICKET-104.md             # Especificación con criterios de aceptación verificables
├── scripts/
│   └── converge.sh               # Loop de verificación: ruff + pytest + cobertura
├── src/pricing/
│   ├── models.py                 # CartItem
│   └── calculator.py             # Implementación base (sin descuentos)
├── tests/
│   └── test_calculator.py        # Tests del comportamiento actual
└── .github/
    ├── pull_request_template.md  # Evidencia obligatoria en cada PR
    └── workflows/ci.yml          # Gate automático: ruff + pytest en cada push/PR
```

## Arranque rápido

```bash
git clone https://github.com/<usuario>/demo-software-factory.git
cd demo-software-factory

uv venv && source .venv/bin/activate
uv pip install -e . --group dev   # o: pip install pytest pytest-cov ruff

./scripts/converge.sh
```

## Ramas de la demo

| Rama         | Estado | Uso |
|--------------|--------|-----|
| `main`       | Verde  | Código base. Solo tests del comportamiento actual. |
| `demo-ready` | Rojo   | Agrega los tests de aceptación de `TICKET-104`. Es el punto de partida del agente. |

El "momento ajá" en vivo:

```bash
git switch demo-ready
./scripts/converge.sh            # rojo: 4 tests de aceptación fallan
# el agente implementa, corre converge.sh, lee el error y corrige
./scripts/converge.sh            # verde + cobertura >= 95%
gh pr create --fill
```

## Reglas de oro

1. Nunca confíes en código generado sin un bucle determinista que lo verifique (tests, tipos, linter).
2. Cuidá el contexto como cuidás la RAM del servidor: menos ruido en consola = mejores respuestas y menos costo.
3. La IA acelera la escritura; la responsabilidad del merge sigue siendo del desarrollador.

## Licencia

MIT.
