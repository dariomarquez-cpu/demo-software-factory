# Runbook: de Vibe Coding a Software Factory con agentes de IA

Guía para replicar el flujo **Ticket → Spec → Implementación → Convergencia → PR** en tu máquina, después de la charla.

Tiempo estimado: 5 a 10 minutos. Nada de esto se instala en vivo.

---

## 1. Prerrequisitos

- **OS:** Linux, macOS o WSL2.
- **Runtime:** Python 3.11+ (`uv` recomendado, `pip` también sirve).
- **Git** y **GitHub CLI** con sesión iniciada (`gh auth login`).
- **Proveedor LLM:** una API key configurada (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY` o `DEEPSEEK_API_KEY`).

## 2. Herramientas del stack

### A. Agente y harness en terminal (OpenCode)

```bash
curl -fsSL https://opencode.ai/install | bash
opencode --version
```

El harness es lo que le da al modelo manos sobre el repo: leer archivos, correr comandos, ver sus propios errores.

### B. Filtro de salidas largas (rtk)

```bash
cargo install rtk
# Alternativas: brew install rtk, o bajar el binario de los releases del proyecto
rtk --help
```

`rtk` no reemplaza a tus herramientas: las envuelve y deja solo lo importante.

```bash
rtk err ruff check src tests    # solo errores y warnings
rtk test pytest -q              # solo tests que fallan
rtk diff                        # diff condensado: solo líneas cambiadas
rtk read src/pricing/calculator.py
```

Sin `rtk`, 80 líneas de traceback entran al contexto del modelo. Con `rtk`, entran las 4 líneas de la aserción que falló.
Menos ruido, mejor razonamiento, menos tokens.

### C. Proxy de contexto (Headroom)

```bash
uv tool install headroom-ai      # o: pip install headroom-ai
headroom proxy --port 8787 &
```

Se para entre el agente y la API del modelo: comprime y cachea contexto repetitivo sin perder información técnica.

### D. GitHub CLI

```bash
gh auth login
gh auth status
```

## 3. Clonar y preparar el repo

```bash
git clone https://github.com/<usuario>/demo-software-factory.git
cd demo-software-factory

uv venv && source .venv/bin/activate
uv pip install -e . --group dev
# sin uv:
# python -m venv .venv && source .venv/bin/activate
# pip install pytest pytest-cov ruff

chmod +x scripts/converge.sh
```

Verificación rápida:

```bash
./scripts/converge.sh
```

En `main` tiene que dar verde. Si no da verde, el entorno está mal, no el código.

## 4. Configuración para consumir menos tokens

```bash
# Apuntar el cliente al proxy local
export OPENAI_BASE_URL="http://localhost:8787/v1"

# Estilo de respuesta denso (sin relleno conversacional)
export OPENCODE_SYSTEM_STYLE="caveman"
```

Tres capas, tres problemas distintos:

| Capa            | Qué resuelve                                  |
|-----------------|-----------------------------------------------|
| Headroom        | Contexto repetido y costo por request          |
| caveman         | Relleno conversacional en las respuestas       |
| rtk             | Ruido de consola (logs, tracebacks, diffs)     |

Aclaración importante: `caveman` cambia el **estilo** de la respuesta, no la calidad del razonamiento.
Nunca sacrifiques un test por ahorrar tokens.

## 5. Flujo punta a punta (Ticket → PR)

```bash
# 1. Leer el contrato
cat specs/TICKET-104.md

# 2. Arrancar desde el estado rojo de la demo
git switch demo-ready
git switch -c feat/ticket-104-descuentos

# 3. Ver el rojo con tus propios ojos
./scripts/converge.sh

# 4. Disparar el agente
opencode run "Implementá specs/TICKET-104.md siguiendo estrictamente AGENTS.md.
Ejecutá ./scripts/converge.sh en cada iteración y no termines hasta que pase.
No modifiques tests existentes."
```

El agente lee la spec, inspecciona `src/pricing/calculator.py`, implementa, corre `converge.sh`, lee el error y corrige
hasta converger.

```bash
# 5. Auditoría humana
git diff src/

# 6. PR con evidencia
git add -A && git commit -m "feat(pricing): aplicar reglas de descuento TICKET-104"
git push -u origin feat/ticket-104-descuentos
gh pr create --fill --base main
```

## 6. Checklist del revisor (anti-"fruta")

Antes de aprobar un PR generado por un agente:

- [ ] ¿El diff toca únicamente los archivos esperados (`src/`)?
- [ ] ¿Los tests cubren los casos borde del ticket sin haber sido debilitados o borrados?
- [ ] ¿La cobertura y el linter pasaron con evidencia real en el log, no escrita a mano?
- [ ] ¿Entendés la lógica de negocio del cambio? Si no la podés explicar, no la aprobés.

## 7. Plan B para la demo en vivo

- Rama `demo-ready`: estado inicial, todo rojo.
- Rama `demo-backup-pr`: la misma tarea ya ejecutada y en verde.

Si falla internet, la API o el modelo: cambiás de pestaña al PR ya generado y explicás los mismos logs guardados.
Nunca dependas de una corrida perfecta en vivo.

## 8. Ideas para seguir

1. Reemplazar `specs/TICKET-104.md` por un ticket real de tu tracker (Jira, Linear, GitHub Issues).
2. Sumar un gate de tipos (`mypy`) y otro de seguridad (`pip-audit`) al mismo `converge.sh`.
3. Medir el costo real por ticket con `rtk gain` y compararlo con el tiempo humano.
