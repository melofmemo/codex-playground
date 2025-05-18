# AGENTS.md ─ Codex 실행 지침 (오프라인 환경 버전)

## ENV
- Linux x86-64
- Python 3.12
- Node 20  ❮옵션: 필요 없으면 삭제❯
- **No outbound network** (pip/npm install 불가)

## PRE-BUILT VIRTUAL ENV
- A relocatable virtualenv lives at `.venv/` in the repo root.
- It already contains all Python dependencies (built on Ubuntu 24.04 with `--copies`).
- Use `source .venv/bin/activate` for every run step.

## SETUP   ❮오프라인에서 최소한으로 처리❯
```bash
# 1) Activate the vendored venv
source .venv/bin/activate

# 2) (Node) Use the vendored node_modules/.bin if needed
#    All JS deps are checked into node_modules/; no `npm install`.