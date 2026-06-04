# JuniorFetch

**Sovereign, edge-native data ingestion and knowledge pipeline for the JuniorCloud LLC ecosystem.**

JuniorFetch is the ingestion layer that feeds high-quality, structured data into your local-first knowledge and memory systems (Obsidian + JuniorMemSys + SecondBrainPipeline).

It is designed for air-gapped, low-power, and sovereign environments (including future JuniorOS deployments on 48V edge hardware).

## What JuniorFetch Actually Does

- Fetches data from multiple sources (web, APIs, local files, RSS, bookmarks, etc.)
- Parses and normalizes data into clean, queryable formats (primarily Markdown + structured .parquet)
- Routes data into your Obsidian vault or JuniorMemSys with rich metadata
- Supports topological tagging and TDA-aware ingestion when used with ManifoldFoldingQuantizer
- Designed to work offline-first with optional kernel-level persistence via JuniorOS

## Architecture Position

JuniorFetch sits in the **Ingestion Layer** of the broader sovereign stack:

```
HighLevelOrchestrator
    ↓
TriStateExecutionEngine (User / Swarm / Industry)
    ↓
EdgeRuntime + JuniorOSKernelBridge
    ↓
JuniorFetch (Ingestion) → SecondBrainPipeline / JuniorMemSys / Obsidian
    ↓
ManifoldFoldingQuantizer + TDA (optional enrichment)
```

It is the "front door" for external information entering your sovereign memory palace.

## Key Design Principles

- **Local-first & Air-gapped friendly** — Works completely offline when needed
- **Ternary / TDA aware** — Can feed directly into BitNet-mlx style manifold folding
- **Low bloat** — Minimal dependencies, optimized for Apple Silicon and future edge hardware
- **Event-sourced** — Plays nicely with the SecondBrainPipeline (CQRS + Event Sourcing)
- **End-user simple** — High-level tasks can be triggered via natural language through the HighLevelOrchestrator

## Current Status (June 2026)

- Core fetching and normalization pipeline stable
- Basic Obsidian vault integration working
- TDA / manifold enrichment hooks in development
- Kernel-level persistence (via JuniorOS) planned
- Strong integration with JuniorMemSys and SecondBrainPipeline

## Related Projects

- [BitNet-mlx](https://github.com/cloudcover95/BitNet-mlx) — Core ternary quantization engine
- [JuniorHome](https://github.com/cloudcover95/JuniorHome) — High-level orchestration and execution layer
- [JuniorMemSys-Suite](https://github.com/cloudcover95/JuniorMemSys-Suite) — Topological memory system
- [JuniorStock](https://github.com/cloudcover95/JuniorStock) — Sovereign quant trading infrastructure

## Getting Started (High-Level)

Most users should interact with JuniorFetch through the `HighLevelOrchestrator`:

```python
high_level.run("fetch latest research papers and store in second brain")
high_level.run_task("capital_accumulation_monitor")
```

Direct usage is also supported for power users and automation scripts.

## Roadmap

See [ROADMAP.md](ROADMAP.md) for current priorities and long-term vision.

## Philosophy

JuniorFetch is part of a larger effort to build **sovereign, air-gapped, edge-native intelligence infrastructure** that does not depend on cloud APIs, subscriptions, or centralized services.

Everything is designed to run locally, persist intelligently, and improve over time through topological memory and agentic workflows.

---

**Maintained by JuniorCloud LLC** — Building the tools for a truly sovereign technological future.