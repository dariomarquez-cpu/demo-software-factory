#!/usr/bin/env bash
# Bucle de convergencia: linter + tests + cobertura.
# Sale con código != 0 si algún gate falla, para que el agente lea el error y corrija.
set -euo pipefail

cd "$(dirname "$0")/.."

have_rtk() { command -v rtk >/dev/null 2>&1; }

echo "=== [1/3] Linter (ruff) ==="
if have_rtk; then
  rtk err ruff check src tests
else
  ruff check src tests
fi

echo "=== [2/3] Tests + Cobertura ==="
if have_rtk; then
  rtk test pytest --cov=src/pricing --cov-branch --cov-fail-under=95 --cov-report=term-missing -q
else
  pytest --cov=src/pricing --cov-branch --cov-fail-under=95 --cov-report=term-missing -q
fi

echo "=== [3/3] CONVERGENCIA ALCANZADA ==="
