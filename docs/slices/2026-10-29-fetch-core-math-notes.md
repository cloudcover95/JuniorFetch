# Slice 2026-10-29: JuniorFetch core math, mesh and sandbox notes

Daily home-slice (JuniorCloud LLC, docs only). Written from a shallow clone at
tip `4324683` (2026-10-26, the doc index slice). It fills the gap that slice
listed: `juniorfetch/core/omni_math.py`, `tda_mesh.py` and `llm_sandbox.py`
had no dedicated doc. Read from the code only. No code was run and no
existing file was changed.

## `core/omni_math.py` (35 lines)

`SovereignOmniKernel(variance_retention=0.95, h_bar_mkt=0.01)`, MLX only.

| Method | What the code does |
|---|---|
| `embed_text_mlx(text, model, tokenizer)` | Tokenizes, runs `model(input_ids)`, mean-pools over axis 1. Needs a caller-supplied model; nothing in the repo calls it. |
| `calculate_quantum_matrix(z_scores, deltas, base_vols)` | Q-Mark: `1 - exp(-(abs(z) * delta / base))`, rounded to 4 decimals. A `base_vols` value of 0 or less is replaced by `h_bar_mkt`. |
| `qr_manifold_projection(tensor)` | `q, r = qr(tensor.T)`, returns `(q @ r).flatten()`. |

`variance_retention` is stored but not read anywhere in the repo.

Since `Q @ R` reproduces its input, `qr_manifold_projection` hands back the
input vector, flattened (up to float rounding). It does not change the basis.

## `core/tda_mesh.py` (57 lines)

`TDAMemoryMesh` keeps an in-memory ring of `capacity = 100000` rows with
`dim = settings.embedding_dim` (default 512): `mesh_tensors` (float32) and
`mesh_signatures` (int8). Nothing in it is written to disk.

`encode(signal_tensor, z_score=1.8)`:

1. Q-Mark from `calculate_quantum_matrix([z_score], [0.5], [0.1])`, so
   `delta / base` is fixed at 5.
2. Returns false if Q-Mark is below `settings.etch_threshold` (default 0.50).
3. Otherwise projects, takes the sign signature (`x > 0` gives 1, else -1),
   writes row `head_pointer % capacity`, and advances the pointer.

With the fixed inputs, Q-Mark is `1 - exp(-5 * abs(z))`. At the default
`z_score = 1.8` that is `0.9999`, so encode passes. It only fails when
`abs(z)` is below `ln 2 / 5`, about `0.139`, at the default threshold.

`bit_drift_search(query_tensor, threshold=0.18)` compares sign signatures over
the active rows and returns the row indexes whose normalized Hamming distance
(`mean(abs(a - b) / 2)`) is under 0.18. With no rows, it returns an empty array.

## How `core/palace.py` uses the mesh

- `MemoryPalace.store` builds a random normal vector (`np.random.normal`) as
  the signal, not an embedding of `content`, and calls `encode`. The callers
  (`core/crawler.py` and `playground/app.py`) do not pass `z_score`, so the
  default 1.8 applies and `store` writes the line. The stored `q_mark` is the
  constant `0.85`, not the computed Q-Mark.
- `MemoryPalace.semantic_search` also uses a random query vector. It assigns
  `valid = bit_drift_search(...)` but does not use it; results come from a
  case-insensitive substring scan of every `data.jsonl`, capped at 20.

## `core/llm_sandbox.py` (34 lines)

`SovereignAgenticSandbox(model_path="mlx-community/Meta-Llama-3-8B-Instruct-4bit")`
calls `mlx_lm.load(model_path)` in its constructor and prints an `[INIT]`
line. `generate_context_prompt` builds a Llama 3 chat prompt from mesh results
(`metadata.path` plus the first 2000 characters of `content`).
`execute_inference` runs `mlx_lm.generate` with `max_tokens=512`.

Nothing in the repo imports this class. Constructing it would load (and, if
not cached, download) a model, so under the LLC guards it stays unused: no
model pull. `mlx` and `mlx-lm` are listed in `pyproject.toml` dependencies.

## Gaps worth a later slice

- The embedding path (`embed_text_mlx`) is not wired into `store` or
  `semantic_search`; both use random vectors.
- `qr_manifold_projection` returns its input, so the name overstates it.
- The mesh ring lives in memory only; it is rebuilt empty on each
  `MemoryPalace()`.
- The stored `q_mark` (0.85) does not match the computed Q-Mark.

## Guards

No trit pack here (`docs/STORAGE.md`), so no rate or close line. Not a quant
file, so no ports named. Services bind 127.0.0.1 only. mint false, socket
false, layer_one false, fetch false, ue5_launch false. No `.github`, no GitHub
Actions, no model pull. Nothing here was run.
