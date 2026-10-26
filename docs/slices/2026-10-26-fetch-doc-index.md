# Slice 2026-10-26: JuniorFetch doc index and slice ledger

Read-only notes. No behavior changes. Written from a shallow clone at tip
`c3fd7ab` (2026-10-23, the read/write paths slice). JuniorHome Builder lane,
JuniorCloud LLC, cloudcover95. Additive only: this file is new and nothing
else changes.

## Docs in this repo

| File | Lines | First heading | What it covers |
|---|---|---|---|
| `README.md` | 6 | `# JuniorFetch` | Short summary: BackendRouter, TernarySpatialManifold and BitNet alignment |
| `docs/ARCHITECTURE.md` | 39 | `# JuniorFetch architecture (as of c3cde61)` | Code map: entry points, indexing flow |
| `docs/CLI.md` | 32 | `# CLI reference` | `juniorfetch` Typer commands (`index`, `dashboard`) |
| `docs/GAIA_PROTOCOL.md` | 1 | none | Local RAG notes go through JuniorLLM `handshake(note)`; protocol `goldend-osai-omega/1` |
| `docs/GOLDEND_FETCH.md` | 2 | none | Points to JuniorHome `web3node/goldend_fetch.py`; no embedding, no training |
| `docs/LOCAL.md` | 6 | `# Local compute` | Hook 127.0.0.1:8770, i2sd 127.0.0.1:8767, no 0.0.0.0 |
| `docs/STORAGE.md` | 55 | `# Palace storage format` | Palace on-disk format; notes no trit pack in this repo |

## Slice ledger

| Date | File | Commit |
|---|---|---|
| 2026-10-17 | `docs/STORAGE.md` | `dcb6808` |
| 2026-10-20 | `docs/slices/2026-10-20-fetch-config-wiring.md` | `587deb3` |
| 2026-10-23 | `docs/slices/2026-10-23-fetch-read-write-paths.md` | `c3fd7ab` (current tip) |
| 2026-10-26 | `docs/slices/2026-10-26-fetch-doc-index.md` | this commit |

Earlier SHAs come from the builder's run log; the shallow clone only carries
the tip commit, which matches `c3fd7ab`.

## Code files the docs describe

`juniorfetch/cli.py`, `juniorfetch/core/` (`crawler.py`, `llm_sandbox.py`,
`omni_math.py`, `palace.py`, `tda_mesh.py`), `juniorfetch/playground/app.py`,
`config.py`, `lean_read.py`, `src/hardware/backend_router.py`. The package
list in `pyproject.toml` is `["juniorfetch"]`.

## Gaps worth a later slice

- `docs/GAIA_PROTOCOL.md` and `docs/GOLDEND_FETCH.md` have no Markdown heading.
- `docs/ARCHITECTURE.md` says "as of c3cde61"; later slices (config wiring,
  read/write paths) are not linked from it.
- `juniorfetch/core/omni_math.py`, `tda_mesh.py`, and `llm_sandbox.py` are
  mentioned in `docs/ARCHITECTURE.md` but have no dedicated doc.

## Guards

No trit pack here (`docs/STORAGE.md`), so no rate or close line. Not a quant
file, so no ports named. Services bind 127.0.0.1 only. mint false, socket
false, layer_one false, fetch false, ue5_launch false. No `.github`, no GitHub
Actions, no model pull. Nothing here was run.
