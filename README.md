# JuniorFetch a JuniorCloudllc development
Tired of api? host local

**Free, fully local semantic file search for your entire computer.**

The open-source, private alternative to Google Gemini File Search / Apple Intelligence file search.

No cloud. No API keys. No payments. No data leaving your machine.

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Local](https://img.shields.io/badge/100%25%20Local-Offline-brightgreen)

## Why JuniorFetch?

Google's File Search (via Gemini API) requires uploading your files to the cloud and paying for embeddings.

**JuniorFetch** gives you the same powerful semantic search experience — but **completely local**, using advanced **Topological Data Analysis (TDA)**, **Bit Drift inference**, and the **Sovereign Omni Math kernel**.

### Features

- Index entire folders or whole disks (~/Documents, /Users, external drives, etc.)
- Fast semantic search across all your files (text, code, markdown, logs, etc.)
- Pure local TDA meshes + Bit Drift inference (no ChromaDB, no FAISS, no paid embeddings)
- Extremely efficient on Apple Silicon (M1/M2/M3/M4)
- CLI + beautiful Streamlit dashboard
- Incremental & multiprocessing indexing
- 100% private — everything stays on your machine

## Quick Start

```bash
# 1. Clone and enter directory
git clone https://github.com/cloudcover95/JuniorFetch.git
cd JuniorFetch

# 2. Create and activate venv
python3.11 -m venv .venv
source .venv/bin/activate

# 3. Install
pip install -e ".[ui]"

# 4. Index your files (first time may take a few minutes)
juniorfetch index ~/Documents

# 5. Launch the beautiful dashboard
juniorfetch dashboard