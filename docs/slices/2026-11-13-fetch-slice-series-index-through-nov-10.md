# Slice 2026-11-13: JuniorFetch slice series index, through Nov 10

Daily home-slice (JuniorCloud LLC, docs only). Written from a shallow clone at
tip `6484c51` (2026-11-10, backend router and lean_read notes). This extends
the earlier series indexes (`2026-11-01`, `2026-11-07`) by listing every file
now in `docs/slices/`, taken from the directory listing and each file's title
line. No code was run and no existing file was changed.

## Slices on main at this tip

| Date | File | Title line |
|---|---|---|
| 2026-10-20 | `2026-10-20-fetch-config-wiring.md` | JuniorFetch settings wiring and packaging scope |
| 2026-10-23 | `2026-10-23-fetch-read-write-paths.md` | JuniorFetch on-disk read/write paths |
| 2026-10-26 | `2026-10-26-fetch-doc-index.md` | JuniorFetch doc index and slice ledger |
| 2026-10-29 | `2026-10-29-fetch-core-math-notes.md` | JuniorFetch core math, mesh and sandbox notes |
| 2026-11-01 | `2026-11-01-fetch-slice-series-index.md` | JuniorFetch slice series index |
| 2026-11-04 | `2026-11-04-fetch-dashboard-tab-guide.md` | JuniorFetch dashboard tab guide |
| 2026-11-07 | `2026-11-07-fetch-slice-series-index-continued.md` | JuniorFetch slice series index, continued |
| 2026-11-10 | `2026-11-10-fetch-backend-router-and-lean-read.md` | JuniorFetch backend router and lean_read notes |

Eight slices, one every three days, oldest first.
This file is the ninth.

## Top-level docs these slices sit beside

`docs/ARCHITECTURE.md`, `docs/CLI.md`, `docs/GAIA_PROTOCOL.md`,
`docs/GOLDEND_FETCH.md`, `docs/LOCAL.md`, `docs/STORAGE.md`. The CLI sheet
documents `juniorfetch index` and `juniorfetch dashboard`; the dashboard note
there says to keep any server bound to 127.0.0.1 only.

## Not yet covered

The slices so far do not give a file-by-file note for `config.py` beyond the
2026-10-20 wiring slice, and `docs/GAIA_PROTOCOL.md` is a one-line file with
nothing further to summarize. Later slices can take whichever source file has
no note yet.

## Guard check

Docs only. One new file, additive. No `.github`, no scripts, no remote code
fetched or run. Nothing here binds a port; any server stays on 127.0.0.1.
mint false, socket false, layer_one false.
