# Slice 2026-11-10: JuniorFetch backend router and lean_read notes

Daily home-slice (JuniorCloud LLC, docs only). Written from a shallow clone at
tip `115b651` (2026-11-07, the slice series index continued). It covers the two
small top-level helpers that no earlier slice describes in detail:
`src/hardware/backend_router.py` and `lean_read.py`. Read-only notes from the
source text. No code was run and no existing file was changed.

## `src/hardware/backend_router.py` (17 lines)

- `Backend` is an `Enum` with two members: `MLX = "mlx"` and `CUDA = "cuda"`.
- `BackendRouter` holds one private value, `_current`, which starts as
  `Backend.MLX`.
- `set_backend(backend)` replaces `_current`. It does no validation and does
  not import or probe MLX or CUDA.
- `get_current_backend()` returns `_current`.

So today the router is a plain state holder: it records which backend a caller
wants, and nothing in it executes work on either backend.

### Wiring

- `src/` has one subfolder, `hardware/`, and it has no `__init__.py`.
- A text search of the clone found no import of `BackendRouter` or `Backend`
  outside the file itself (only the README and `docs/ARCHITECTURE.md` mention
  it). The package under `juniorfetch/` does not use it.
- `README.md` calls it "hardware-agnostic execution". That is the intent; the
  file does not yet route anything.

## `lean_read.py` (4 lines)

- Builds the path `~/.juniorhome/os/lean.json`.
- If that file exists, it parses it as JSON and prints it back as one line.
- If it does not exist, it prints `{"ok": false, "port": "JuniorFetch", "writes": 0}`.
- It only reads. It never writes the file, never opens a socket and never
  imports anything outside the standard library (`json`, `pathlib`).
- The `port` value in the fallback names JuniorFetch as the reporting port for
  the JuniorHome OS layer, whose state lives under `~/.juniorhome/os/`.

## `config.py` in one line

`Settings` (prefix `JUNIORFETCH_`) holds `storage_path`
(`~/.juniorfetch/palace`), `etch_threshold` (0.50) and `embedding_dim` (512).
`docs/slices/2026-10-20-fetch-config-wiring.md` covers how it is used.

## Local rules that apply

- Per `docs/LOCAL.md`, anything that serves must bind `127.0.0.1` only, never
  `0.0.0.0`.
- This repo has no trit pack, so the 0.05 rate and the close rule do not apply
  here. This is not a quant file.
- No remote script was downloaded or run. No model was pulled. No `.github`
  or GitHub Actions content was added.

## Open items (observed, not fixed here)

- The router is unused, so choosing `CUDA` today changes nothing.
- `src/hardware/` is not a package, and `pyproject.toml` sets
  `packages = ["juniorfetch"]` (line 32), so an install does not ship the
  router or `lean_read.py`.
- `lean_read.py` is a script, not an importable module with a function, so
  other code would need to run it as a subprocess to reuse it.
