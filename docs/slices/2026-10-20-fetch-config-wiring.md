# Slice 2026-10-20: JuniorFetch settings wiring and packaging scope

Daily home-slice (JuniorCloud LLC, docs only). This note traces which modules
read each setting and what the wheel actually ships. It builds on
`docs/ARCHITECTURE.md` (Configuration and Known gaps) and `docs/STORAGE.md`.
No code was run and no existing file was changed.

## Settings and their env vars

`config.py` (repo root) defines `Settings(BaseSettings)` with env prefix
`JUNIORFETCH_` and exports one `settings` instance.

| Field | Default | Env var | Read by |
| --- | --- | --- | --- |
| `storage_path` | `~/.juniorfetch/palace` | `JUNIORFETCH_STORAGE_PATH` | `core/palace.py` (`self.root`) |
| `etch_threshold` | `0.50` | `JUNIORFETCH_ETCH_THRESHOLD` | `core/tda_mesh.py` (Q-Mark etch check) |
| `embedding_dim` | `512` | `JUNIORFETCH_EMBEDDING_DIM` | `core/tda_mesh.py` (`self.dim`), `core/palace.py` (vector shape in store and search) |

Both readers use `from juniorfetch.config import settings`. No other module
imports settings: `cli.py`, `core/crawler.py`, `core/omni_math.py`,
`core/llm_sandbox.py`, `playground/app.py`, `lean_read.py` and
`src/hardware/backend_router.py` take no values from `Settings`.

## Packaging scope (new finding)

`pyproject.toml` sets `[tool.hatch.build.targets.wheel] packages = ["juniorfetch"]`.
So the wheel ships only the `juniorfetch/` tree. These tracked files sit outside
it and are not packaged:

- `config.py` (the settings module itself)
- `lean_read.py`
- `src/hardware/backend_router.py`

This compounds the known gap in `docs/ARCHITECTURE.md`: the package imports
`juniorfetch.config`, the module lives at the root, and the root module would
not ship even if the import path matched. The console script
`juniorfetch = "juniorfetch.cli:app"` only reaches `crawler` and `palace`, and
`palace` imports `juniorfetch.config`, so an installed CLI depends on this fix.

## Dependency note

`config.py` imports `pydantic_settings`; `pyproject.toml` declares
`pydantic>=2.0.0` but not `pydantic-settings` (already listed in
`docs/ARCHITECTURE.md`). In pydantic v2, `BaseSettings` lives in that separate
package.

## Suggested follow-up (code lane, not this slice)

1. Move or re-export settings as `juniorfetch/config.py` so it ships in the wheel.
2. Declare `pydantic-settings` in `[project] dependencies`.
3. Decide whether `lean_read.py` and `src/hardware/` belong in the package.

## Guards

Docs only. One new file, nothing edited or deleted, no `.github`, no Actions,
no remote scripts, no model pulls, no repo code executed. No trit pack in this
repo, so no rate or close line applies. Not a quant file. Local-only storage
default stays under the user's home (`docs/LOCAL.md`, 127.0.0.1 only).
