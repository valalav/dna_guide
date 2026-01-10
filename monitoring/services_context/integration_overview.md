# Integration Overview: Automation & Services

This directory contains context for integrating local automation scripts with remote STR analysis services.

## 📂 Local Automation Scripts (Root)
Located in `dna_guide/`:

1.  **`generate_batch.py`**
    *   **Purpose**: Batch generation of publication markdown files.
    *   **Integration Point**: Reads from a Google Sheet `publications.csv`.
    *   **Status**: Active, local.

2.  **`generate_publication.py`**
    *   **Purpose**: Core logic for phylogenetic tree traversal and template rendering.
    *   **Integration Point**: Uses `current_tree.json` and local templates.
    *   **Status**: Active, local.

## ☁️ Remote Services (LXC 109)
Hosted on `pystr.valalav.ru` (192.168.10.170 / 100.101.218.57):

1.  **STR Matcher** (`str-matcher`)
    *   **Context**: [str_matcher_README.md](str_matcher_README.md)
    *   **Port**: 3000 (Frontend), 9005 (Backen API)
    *   **Role**: Web UI for finding STR matches.
    *   **New Feature**: Google Sheets Import (Deployed 2026-01-10).

2.  **Y-STR Predictor** (`ystr_predictor`)
    *   **Context**: [ystr_predictor_app.py](ystr_predictor_app.py) (Source Header)
    *   **Port**: Likely 8080 or internal.
    *   **Role**: ML-based haplogroup prediction from STRs.

3.  **FTDNA Haplo client** (`ftdna_haplo`)
    *   **Context**: [ftdna_haplo_README.md](ftdna_haplo_README.md)
    *   **Role**: Client for fetching FTDNA data.

## 🔗 Potential Integration Paths

- **Current Flow**: Users use `str-matcher` web UI -> Results could be exported to Google Sheets -> `generate_batch.py` reads Google Sheets -> Generates website posts.
- **Goal**: Automate the feedback loop or direct API integration.
