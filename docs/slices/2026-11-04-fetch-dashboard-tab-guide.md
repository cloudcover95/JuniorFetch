# Slice 2026-11-04: JuniorFetch dashboard tab guide

Daily home-slice (JuniorCloud LLC, docs only). Written from a shallow clone at
tip `924b1e1` (2026-11-01, the slice series index). It walks the Streamlit
dashboard in `juniorfetch/playground/app.py` (157 lines) one tab at a time:
what each control reads, what it calls, and what it writes. Earlier slices
cover storage paths and the math; this one is the user-facing view. No code
was run and no existing file was changed.

## Startup

- Launched by `juniorfetch dashboard` (`juniorfetch/cli.py`), which runs
  `streamlit run juniorfetch/playground/app.py` through `os.system`. See
  `docs/CLI.md` for the 127.0.0.1 bind.
- Page config: title `JuniorFetch | Sovereign Node`, `layout="wide"`.
- Module level builds `palace = MemoryPalace()` and
  `crawler = JuniorFetchCrawler()`. The crawler builds its own
  `MemoryPalace()` in `__init__`, so the page holds two palace objects, each
  with its own `TDAMemoryMesh`.
- Imports: `streamlit`, `os`, `json`, `pandas`, `altair`, `pathlib.Path`.

## Tabs

| # | Tab label | Controls | Calls | Reads | Writes |
|---|---|---|---|---|---|
| 1 | Search & Edit | text input, `Execute Vector Search`, per-hit text area, `Save Edit & Re-Etch` | `palace.semantic_search(query, wing="files")`, `palace.store(...)` | every `data.jsonl` under the storage root | the user's file on disk, plus one appended palace line |
| 2 | Registry Snapshot | hall select box | none | dir names under `<root>/files/`, `drawers.jsonl` presence | nothing |
| 3 | FSD Heart (Telemetry) | `Scan Mesh Telemetry` | `fetch_mesh_telemetry()` (`st.cache_data(ttl=60)`) | every `drawers.jsonl` under `<root>/files/` | nothing |
| 4 | Disk Indexer | target dir (default `~/Documents`), max files (min 100, max 500000, default 10000), `Run Indexer` | `crawler.index(target_dir, max_files=int(max_f))` | the target tree | palace lines via the crawler |

## Per-tab notes from the source

1. **Search & Edit.** `semantic_search` ignores its `wing` argument and the
   random query tensor; it scans every `data.jsonl` under the root and keeps
   lines where the lower-cased query is a substring of the raw JSON line,
   capped at 20. The tab shows the first 15. Because the match runs on the
   whole JSON line, a query such as `path` or `metadata` matches field names
   and returns every record. Each hit shows its `q_mark`, which `store`
   always sets to `0.85`.
2. **Save path.** `Save Edit & Re-Etch` calls `file_path.write_text(...)` on
   the real file, then `palace.store` with `hall` from the hit's metadata or
   `root`. This is the only place in the repo that writes to a file outside
   the storage root. The save button sits inside the
   `if st.button("Execute Vector Search") and query:` branch. Streamlit reruns
   the script on each click and a button is true only on its own click run,
   so the save click reruns with the outer button false and the save block is
   not reached as written.
3. **Missing file.** If the hit's path no longer exists, the tab shows a
   warning and the first 2000 chars of the stored `content`.
4. **Registry Snapshot.** Lists up to 50 rooms per hall and only those with
   `drawers.jsonl`. `store` writes `data.jsonl`, so crawler output lists no
   rooms (already noted in `docs/STORAGE.md`).
5. **FSD Heart.** Builds a DataFrame of `Extension`, `Q_Mark`, `Size_KB`, then
   three metrics (count, mean Q-Mark, total MB), an Altair donut of extension
   counts and a 30-bin Q-Mark histogram. A bare `except: pass` hides any read
   or parse error per file. Same `drawers.jsonl` name, so it shows
   `Mesh is empty` for crawler output.
6. **Disk Indexer.** Default cap here is 10000; the CLI `index` default is
   100000. Indexing runs in the Streamlit process on the crawler's 8 threads.

## Guards

One new file, one commit, one push. Additive only: nothing edited, deleted
or force-pushed, and no `.github`. Written in the LLC window (02:00 to 04:45
America/Denver), outside the personal quant window (05:05 to 07:05). No GitHub
Actions, Copilot or Dependabot; no remote scripts, no model pulls, no repo
code executed. Any dashboard check binds 127.0.0.1 only. No trit pack here
(`docs/STORAGE.md`), so no rate or close line. Not a quant file, so no ports
are named.

Next rotation stop: cloudcover95/JuniorHome.
