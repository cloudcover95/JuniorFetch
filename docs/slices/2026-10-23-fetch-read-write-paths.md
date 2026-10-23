# Slice 2026-10-23: JuniorFetch on-disk read/write paths

Daily home-slice (JuniorCloud LLC, docs only). This note traces which file
names each module writes and reads under the palace root, and where they
disagree. It builds on `docs/ARCHITECTURE.md`, `docs/STORAGE.md` and
`docs/slices/2026-10-20-fetch-config-wiring.md`. No code was run and no
existing file was changed.

## Writer

`core/palace.py` `MemoryPalace.store` is the only writer. When
`TDAMemoryMesh.encode` returns true, it appends one `MemoryObject` JSON line to:

`<storage_path>/<wing>/<hall>/<room>/data.jsonl`

Callers:

| Caller | wing | hall | room | metadata |
| --- | --- | --- | --- | --- |
| `core/crawler.py` `index.process` | `files` | parent dir relative to root, `/` to `_`, or `root` | file name | `path`, `extension`, `mtime`, `size_bytes` |
| `playground/app.py` tab 1 "Save Edit & Re-Etch" | `files` | `r['metadata'].get('hall', 'root')` | file name | the search hit's metadata |

## Readers

| Reader | File name read | Matches writer? |
| --- | --- | --- |
| `palace.py` `semantic_search` | `data.jsonl` (`rglob` over the whole root) | yes |
| `playground/app.py` tab 2 Registry Snapshot | `<hall>/<room>/drawers.jsonl` | no |
| `playground/app.py` tab 3 FSD Heart `fetch_mesh_telemetry` | `drawers.jsonl` (`rglob` under `files/`) | no |

## Findings (observed, not fixed here)

1. **File name mismatch.** The store writes `data.jsonl`, but tabs 2 and 3
   look for `drawers.jsonl`. Tab 2 still lists hall directories, but its file
   list skips every room, so no `📝` rows render. Tab 3 always gets an empty
   frame and shows "Mesh is empty".
2. **Hall is lost on re-etch.** The crawler's metadata has no `hall` key, so
   a tab 1 save always re-etches under hall `root`, not the file's own hall.
3. **Search ignores the mesh and the wing.** `semantic_search` computes
   `valid = self.mesh.bit_drift_search(...)` from a random query tensor but
   never uses it. Results come from a case-insensitive substring match of the
   query against each raw JSON line (content and metadata), capped at 20.
   The `wing` argument is unused.
4. **Mesh state is per process.** `TDAMemoryMesh` holds its tensors in numpy
   arrays in memory with `head_pointer` starting at 0. Nothing persists them,
   so a fresh process (CLI `index`, then `dashboard`) starts with an empty mesh.
   Search still works only because of the substring scan above.
5. **Appends duplicate.** `store` opens `data.jsonl` in append mode, so
   re-indexing the same tree, or saving an edit, adds a second line for the
   same file. Search can return both.
6. **Etch gate always passes for crawler input.** With `z_score=1.8`,
   delta `0.5` and base vol `0.1`, `calculate_quantum_matrix` gives
   `1 - exp(-9)`, about `0.9999`, above `etch_threshold` `0.50`. The stored
   `q_mark` is a fixed `0.85`, not that value.
7. **Nested button in tab 1.** "Save Edit & Re-Etch" sits inside the
   `if st.button("Execute Vector Search")` branch. Streamlit reruns the script
   on each click with the outer button false, so the save branch likely never
   runs. Worth confirming locally on 127.0.0.1 before relying on the editor.
8. **Unlocked shared mesh.** The crawler runs `process` on 8 threads that all
   call `store` on one `MemoryPalace`, and `encode` bumps `head_pointer`
   with no lock.

## Suggested follow-up (code lane, not this slice)

1. Pick one file name (`data.jsonl`) for both writer and dashboard readers.
2. Add `hall` to the crawler metadata, or pass the hall through from the
   search hit's path.
3. Either use the `bit_drift_search` result or drop the call, and honor `wing`.
4. Dedupe on `metadata.path` before appending.

## Guards

Docs only. One new file, nothing edited or deleted, no `.github`, no Actions,
no remote scripts, no model pulls, no repo code executed. No trit pack in
this repo, so no rate or close line applies. Not a quant file. Storage stays
local under the user's home; any dashboard check binds 127.0.0.1 only
(`docs/LOCAL.md`).
