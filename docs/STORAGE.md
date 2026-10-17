# Palace storage format

How JuniorFetch lays out indexed files on local disk today (as of ba81227).
Read-only notes from the code; no behavior changes. Local disk only, no cloud.

## Root
`config.py` `Settings.storage_path`, default `~/.juniorfetch/palace`.
Override with the env var `JUNIORFETCH_STORAGE_PATH` (env prefix `JUNIORFETCH_`).
`MemoryPalace.__init__` creates the root with `mkdir(parents=True, exist_ok=True)`.

## Layout
`MemoryPalace.store(wing, hall, room, content, metadata, z_score=1.8)` appends one JSON line to:

```
<storage_path>/<wing>/<hall>/<room>/data.jsonl
```

From the crawler (`core/crawler.py`):
- `wing` is always `files`.
- `hall` is the file's parent directory relative to the indexed root, with `/` replaced by `_`.
- `room` is the file name (`f.name`), so each source file gets its own folder.

Writes are append-only (`open(path, "a")`). Re-indexing the same file adds another line; nothing is overwritten.

## Line schema (`MemoryObject`, pydantic)

| Field | Type | Source |
|---|---|---|
| `content` | str | file text, capped at 25000 chars in `store` (the crawler reads the first 50000) |
| `metadata` | dict | from the crawler: `path`, `extension`, `mtime`, `size_bytes` |
| `q_mark` | float | fixed at `0.85` in `store` |
| `timestamp` | float | `time.time()` at write |

If no metadata is passed, `store` falls back to `{"wing", "hall", "room"}`.

## When a line is written
`store` only writes when `TDAMemoryMesh.encode` returns true, which is when the computed
Q-Mark is at or above `settings.etch_threshold` (default 0.50). The vector passed to `encode`
is `np.random.normal`, not a text embedding (see `docs/ARCHITECTURE.md`, Known gaps).
The mesh tensors and signatures live in memory only; they are not saved to disk.

## Reading it back
`MemoryPalace.semantic_search(query)` scans every `data.jsonl` under the root and returns up to 20
lines whose raw JSON contains the query (case-insensitive substring match).

## Known mismatches (observed, not fixed here)
- `juniorfetch/playground/app.py` tabs "Registry Snapshot" and "FSD Heart" look for
  `drawers.jsonl`, but `store` writes `data.jsonl`. Those tabs will show nothing for crawler output.
- The dashboard "Save Edit & Re-Etch" button uses `metadata["hall"]`, which the crawler does not set,
  so re-etched edits land under hall `root`.
- `.gitignore` ignores `data/`, but the palace lives outside the repo, so it is never committed either way.

## Local rules
Services bind 127.0.0.1 only, never 0.0.0.0 (`docs/LOCAL.md`). No trit pack in this repo, so no
rate or close rule applies here.
