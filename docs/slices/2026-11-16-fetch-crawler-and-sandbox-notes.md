# Fetch slice: crawler and sandbox notes (Nov 16, 2026)

Additive doc. Describes `juniorfetch/core/crawler.py` and `juniorfetch/core/llm_sandbox.py` as they are on main. No code was run to write this.

## Crawler (`JuniorFetchCrawler`)

- Builds a `MemoryPalace` on init.
- Supported suffixes (lowercased): `.txt .md .py .json .csv .log .pdf .html .yml .yaml .ini .toml .js .ts .cpp .h .c .rs .go .sh`.
- `index(root, max_files=100000)`: expands and resolves `root`, walks it with `rglob("*")`, keeps files with a supported suffix, and stops collecting at `max_files`.
- Files are processed by a `ThreadPoolExecutor` with 8 workers.
- Each file is read with `read_text(errors="ignore")` and cut to 50,000 characters. `.pdf` is read as plain text the same way, so no PDF parsing happens.
- Empty or whitespace-only text is skipped.
- Hall name: the file's parent path relative to `root`, with `/` replaced by `_`; `root` when the file sits directly in the root.
- Stored with wing `files`, the hall above, and room = file name. Metadata: `path`, `extension`, `mtime`, `size_bytes`.
- Any exception while processing one file is swallowed, so unreadable files are skipped silently.
- Prints `[SYNC]` at start and `[OK] Indexed N files` at the end. N is the number of files collected, not the number stored.

## Palace interaction worth knowing

- `MemoryPalace.store` caps content at 25,000 characters, so the crawler's 50,000-character read is cut again on store.
- Stored data lands in `<storage_path>/<wing>/<hall>/<room>/data.jsonl` (see docs/STORAGE.md).
- Writes happen only when the TDA mesh `encode` call accepts the item, so a file can be collected and counted yet not written.

## Sandbox (`SovereignAgenticSandbox`)

- Loads an MLX model with `mlx_lm.load`; the default is `mlx-community/Meta-Llama-3-8B-Instruct-4bit`. Construction pulls the model, so it is not run in this slice. Models are not pulled by LLC bots.
- `generate_context_prompt(query, mesh_results)`: joins results as `Path: <metadata.path>` plus the first 2,000 characters of `content`, separated by `---`, inside a Llama 3 chat template. The system line tells the model to answer only from the supplied local file context.
- `execute_inference(query, mesh_results, max_tokens=512)`: builds that prompt and calls `mlx_lm.generate` with `verbose=False`.
- Each result needs `metadata.path`, which the crawler sets; palace entries stored with default metadata (wing, hall, room) would not have it.
- `mlx` and `mlx-lm` are listed in `pyproject.toml`.

## Guards

Local only. Nothing here binds a network port. No GitHub Actions, no remote scripts, no model pull. Trit pack: none in this repo, so the rate 0.05 and close rule do not apply.
