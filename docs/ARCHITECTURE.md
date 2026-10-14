# JuniorFetch architecture (as of c3cde61)

A code map of what is in this repo today. Read-only notes; no behavior changes.

## Entry points
- `juniorfetch/cli.py` — Typer app, exposed as the `juniorfetch` script (`pyproject.toml`).
  - `index [PATH] --max-files N` — default path `~/Documents`, default 100000 files. Runs `JuniorFetchCrawler.index`.
  - `dashboard` — runs `streamlit run juniorfetch/playground/app.py` (Streamlit is the `ui`/`dev` extra).
- `lean_read.py`, `src/hardware/backend_router.py` — top-level helpers outside the package.

## Indexing flow
1. `core/crawler.py` `JuniorFetchCrawler` walks the root with `rglob`, keeping files whose suffix is one of:
   `.txt .md .py .json .csv .log .pdf .html .yml .yaml .ini .toml .js .ts .cpp .h .c .rs .go .sh`.
2. Each file is read as text (first 50000 chars; `.pdf` is also read as raw text, not parsed). Empty files are skipped.
3. Files go into `core/palace.py` `MemoryPalace.store` under wing `files`, hall = parent dir relative to root.
4. `store` calls `core/tda_mesh.py` `TDAMemoryMesh.encode`; on success it appends a `MemoryObject`
   (content capped at 25000 chars) to `<storage_path>/<wing>/<hall>/<room>/data.jsonl`.

## Search
`MemoryPalace.semantic_search` calls `TDAMemoryMesh.bit_drift_search` (default threshold 0.18).

## Math / LLM modules
- `core/omni_math.py` `SovereignOmniKernel` — MLX embedding, quantum matrix, QR manifold projection.
- `core/llm_sandbox.py` `SovereignAgenticSandbox` — `mlx_lm` load/generate; default model id
  `mlx-community/Meta-Llama-3-8B-Instruct-4bit`. Constructing it loads a model; do not do that in automated runs.

## Configuration
`config.py` `Settings` (pydantic-settings, env prefix `JUNIORFETCH_`):
- `storage_path` = `~/.juniorfetch/palace`
- `etch_threshold` = 0.50
- `embedding_dim` = 512

## Known gaps (observed, not fixed here)
- `MemoryPalace.store` and `semantic_search` currently use `np.random.normal` vectors, not real text embeddings.
- Package code imports `juniorfetch.config`, but `config.py` lives at the repo root.
- `pydantic-settings`, `altair` are imported but not listed in `pyproject.toml` dependencies.

## Local rules
See `docs/LOCAL.md`: services bind 127.0.0.1 only, never 0.0.0.0.
