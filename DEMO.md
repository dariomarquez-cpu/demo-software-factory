# DEMO.md — Guion técnico de los 14 minutos

Choreografía para la demo en vivo (bloque 4 de la charla). Cada paso tiene su comando exacto y su frase pedagógica.

## Antes de entrar a la llamada

```bash
# 1. Clonar la copia de trabajo (no el repo base: el PR sale de acá)
gh repo clone dariomarquez-cpu/demo-software-factory-demo demo-live
cd demo-live

# 2. Entorno listo y verde en main
uv venv && source .venv/bin/activate
uv pip install -e . --group dev
./scripts/converge.sh

# 3. Dejar el repo apuntando al base para los PRs
gh repo set-default dariomarquez-cpu/demo-software-factory

# 4. Precalentar el modelo (una corrida corta) para que no arranque en frío
```

Checklist de pantallas abiertas: terminal grande con fuente legible, editor con `src/pricing/calculator.py`,
pestaña del PR de referencia ya abierta (plan B), y el `RUNBOOK.md` para compartir.

## Minuto a minuto

### 20:00 – 22:00 · El contrato antes del código

```bash
cat specs/TICKET-104.md
cat AGENTS.md
```

Frase: "No arrancamos tirando un prompt mágico. Arrancamos con un contrato: qué se espera y qué está prohibido.
Miren esta línea: prohibido tocar los tests para que pasen. Ese es el error clásico que queremos evitar."

### 22:00 – 24:00 · Contexto barato

```bash
headroom proxy --port 8787 &
export OPENAI_BASE_URL="http://localhost:8787/v1"
export OPENCODE_SYSTEM_STYLE="caveman"

# contraste de ruido vs. señal
pytest -q                      # salida completa
rtk test pytest -q             # solo lo que falló
```

Frase: "Cada línea de log basura que lee el agente cuesta plata y le baja la atención. Esto no es cosmética: es
calidad de razonamiento."

### 24:00 – 28:00 · Disparo (iteración 1, rojo)

```bash
git switch demo-ready
git switch -c feat/ticket-104-descuentos
./scripts/converge.sh          # 5 tests de aceptación fallando

opencode run "Implementá specs/TICKET-104.md siguiendo estrictamente AGENTS.md.
Ejecutá ./scripts/converge.sh en cada iteración y no termines hasta que pase.
No modifiques tests existentes."
```

Frase mientras corre: "Está leyendo el spec, mirando `calculator.py`, escribiendo la lógica y corriendo el bucle.
No le pedí que adivine: le di un juez."

### 28:00 – 31:00 · El momento ajá

Cuando falla `test_tope_10_porciento_si_hay_electronica_con_cupon`:

Frase: "Miren esto. Código prolijo, lógica razonable, y sin embargo aplicó el 15% del cupón ignorando el tope de
electrónica. Si yo copiaba y pegaba esto, tenía un bug de facturación. Los tests no son burocracia: son el
detector de fruta."

### 31:00 – 34:00 · Convergencia y PR

```bash
git diff src/                                  # auditoría humana del diff
git add -A && git commit -m "feat(pricing): aplicar reglas de descuento TICKET-104"
git push -u origin feat/ticket-104-descuentos
gh pr create --fill --base main
```

Frase: "No perdí 40 minutos escribiendo boilerplate, pero tampoco entregué el control. Ahora soy el revisor técnico
frente a un diff chico y respaldado por evidencia."

## Plan B (si algo falla)

Rama `demo-solution` ya resuelta, más un PR de referencia abierto con la implementación verde:

```bash
gh pr list --repo dariomarquez-cpu/demo-software-factory
```

Cambiás de pestaña, mostrás el PR y contás la misma historia con los logs ya guardados. La charla no depende de la red.

## Preguntas previsibles de la audiencia

- **¿Y si el agente borra un test?** `AGENTS.md` lo prohíbe y el revisor lo detecta en el diff; además el test
  original vive en `main`, así que el CI del PR compara contra el estado conocido.
- **¿Esto reemplaza al dev?** No. Mueve el trabajo del dev de escribir boilerplate a especificar y auditar.
- **¿Cuánto cuesta?** Menos que el ruido: `rtk gain` mide el ahorro real por sesión.
- **¿Sirve para un repo legacy?** Sí, pero empezando por un módulo con tests rápidos; sin tests no hay convergencia.
