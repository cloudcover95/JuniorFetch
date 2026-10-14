# CLI reference

Source: `juniorfetch/cli.py` (Typer app). Installed as the `juniorfetch`
script via `[project.scripts]` in `pyproject.toml`
(`juniorfetch = "juniorfetch.cli:app"`). Also runnable as
`python -m juniorfetch.cli`.

## `juniorfetch index [PATH] [--max-files N]`

Index a directory with `JuniorFetchCrawler` (`juniorfetch/core/crawler.py`).

| Arg / option | Type | Default | Help |
|---|---|---|---|
| `PATH` (argument) | str | `~/Documents` | Target directory to index |
| `--max-files` | int | `100000` | Maximum number of files to process |

Prints `Initializing JuniorFetch crawler on <path>...`, then calls
`JuniorFetchCrawler().index(path, max_files)`.

## `juniorfetch dashboard`

Prints `Booting JuniorFetch Workspace...` and runs
`streamlit run juniorfetch/playground/app.py` via `os.system`.
Streamlit is an optional extra (`pip install -e ".[ui]"`).
Keep any server bound to 127.0.0.1 only, e.g.
`streamlit run juniorfetch/playground/app.py --server.address 127.0.0.1`.

## Notes

- No other commands are defined. `juniorfetch --help` lists them.
- Settings (storage path, thresholds) come from `config.py`; see
  `docs/ARCHITECTURE.md`.
