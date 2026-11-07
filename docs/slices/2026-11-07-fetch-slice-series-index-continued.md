# Slice 2026-11-07: JuniorFetch slice series index, continued

Daily home-slice (JuniorCloud LLC, docs only). Written from a shallow clone at
tip `91de8c6` (2026-11-04, the dashboard tab guide). It continues the ledger
in `docs/slices/2026-11-01-fetch-slice-series-index.md`, which stopped at the
2026-10-29 slice, and adds the two slices that landed after it. The full
table is repeated so this file can be read alone. No code was run and no
existing file was changed.

## JuniorFetch slices

| Date | Path | Lines | Title | Commit |
|---|---|---|---|---|
| 2026-10-17 | `docs/STORAGE.md` | 55 | Palace storage format | `dcb6808` |
| 2026-10-20 | `docs/slices/2026-10-20-fetch-config-wiring.md` | 58 | JuniorFetch settings wiring and packaging scope | `587deb3` |
| 2026-10-23 | `docs/slices/2026-10-23-fetch-read-write-paths.md` | 77 | JuniorFetch on-disk read/write paths | `c3fd7ab` |
| 2026-10-26 | `docs/slices/2026-10-26-fetch-doc-index.md` | 52 | JuniorFetch doc index and slice ledger | `4324683` |
| 2026-10-29 | `docs/slices/2026-10-29-fetch-core-math-notes.md` | 83 | JuniorFetch core math, mesh and sandbox notes | `1d1b31a` |
| 2026-11-01 | `docs/slices/2026-11-01-fetch-slice-series-index.md` | 37 | JuniorFetch slice series index | `924b1e1` |
| 2026-11-04 | `docs/slices/2026-11-04-fetch-dashboard-tab-guide.md` | 71 | JuniorFetch dashboard tab guide | `91de8c6` |

Line counts are `wc -l` on the clone at `91de8c6`. Each commit added exactly
one file. Runs land every third day because the rotation goes JuniorHome,
then JuniorDrive, then JuniorFetch.

## Reading order

1. `docs/STORAGE.md` for the palace format on disk.
2. The 2026-10-20 and 2026-10-23 slices for settings and file paths.
3. The 2026-10-29 slice for the math behind search and the mesh.
4. The 2026-11-04 slice for the dashboard that sits on top.
5. The 2026-10-26 and 2026-11-01 slices, and this one, are indexes only.

## Sibling ledgers (other repos in this rotation)

- cloudcover95/JuniorDrive: `docs/slices/2026-10-28-drive-slice-series-index.md`,
  then `docs/slices/2026-11-06-drive-rotation-ledger-nov-continued.md`
- cloudcover95/JuniorHome: `docs/slices/2026-10-30-home-slice-series-index.md`

## Guards

One new file, one commit, one push. Additive only: nothing edited, deleted
or force-pushed, and no `.github`. Written in the LLC window (02:00 to 04:45
America/Denver), outside the personal quant window (05:05 to 07:05). No GitHub
Actions, Copilot or Dependabot; no remote scripts, no model pulls, no repo
code executed. No trit pack here (`docs/STORAGE.md`), so no rate or close
line. Not a quant file, so no ports are named.

Next rotation stop: cloudcover95/JuniorHome.
