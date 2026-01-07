# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is the **AADNA Guide** — a comprehensive Russian-language documentation project for DNA genealogy focused on Adyghe-Abkhaz peoples and the Caucasus region. The repository contains educational materials, research guides, and haplogroup reference documentation.

**Key characteristics:**
- Language: Russian (primary content), English (technical scripts)
- Format: Markdown documentation with embedded visualizations
- Domain: Population genetics, Y-DNA/mtDNA haplogroups, ancient DNA analysis
- Target audience: Beginner to advanced DNA genealogy enthusiasts

---

## Tools & MCP Servers

**Context7 MCP:** Always use Context7 MCP when I need library/API documentation, code generation, setup or configuration steps without me having to explicitly ask.

---

## Project Structure

```
dna_guide/
├── 00_General/          # Main reference work
├── 01_Beginner/         # Introductory content (5 guides)
├── 02_Practical/        # How-to guides for YFull, GEDmatch, etc.
├── 03_Advanced/         # Ancient DNA, private SNPs, branch structures
├── 04_Women/            # mtDNA and female-specific guides
├── 05_Autosomal/        # Autosomal DNA and relative matching
├── 06_Motivation/       # motivational content
├── 07_Branches/         # L1264 branch narratives
├── 08_Diaspora/         # Muhajir diaspora guides
├── 09_Statistics/       # Statistical reports and visualizations
├── 10_Haplogroups/      # Haplogroup reference (G, J, R, E, C)
├── assets/              # Images and diagrams (128+ files)
├── .agent/              # Claude Code workflow configs
├── current_tree.json    # Y-DNA phylogenetic tree (14.6MB)
├── validate_hierarchy.py # Validation script
├── README.md            # Main navigation index
└── task.md              # Project task list
```

---

## Common Commands

### Running the Validation Script

The `validate_hierarchy.py` script validates haplogroup hierarchy consistency between the CSV data (from Google Sheets) and `current_tree.json`:

```bash
python3 validate_hierarchy.py
```

**What it does:**
- Loads `current_tree.json` to build node maps and SNP mappings
- Fetches CSV data from the configured Google Sheets URL
- Validates that haplogroup hierarchies are consistent (child nodes are actual descendants)
- Checks that terminal haplogroups match the expected hierarchy
- Generates `hierarchy_validation_report.md` with any inconsistencies found

**Note:** The script has hardcoded Windows paths (`TREE_JSON_PATH`, `REPORT_PATH`) that need adjustment for Linux environments.

---

## Architecture & Key Files

### Data Structures

**current_tree.json (14.6MB):**
- Hierarchical Y-DNA phylogenetic tree data
- Structure: nested nodes with `id`, `name`, `snps`, `children` fields
- Used for validation and haplogroup reference documentation
- Contains SNP mappings for tree traversal

**Content Organization:**
- `00_Haplogroup_Reference.md` — Main index for all haplogroups (G, J, R, E, C)
- Individual haplogroup directories (`G2/`, `J/`, `R/`) contain detailed subclade guides
- TMRCA (Time to Most Recent Common Ancestor) dates are consistently tracked and verified against `current_tree.json`

### Documentation Patterns

**Haplogroup Reference Files:**
- Status indicators: ✅ (verified), 🔄 (in progress), ⚠️ (needs verification)
- Verification notes reference both `aadna.ru` and `current_tree.json`
- Consistent structure: General info → Path from Adam → Branches → Ancient DNA → Historical context → External links
- TMRCA dates marked with `*verified*` when validated

**Naming Conventions:**
- Haplogroup names use YFull nomenclature (e.g., G-L1264, J2a-M67)
- File names use underscores: `00_G2_Overview.md`, `01_G2a1.md`
- Assets use descriptive names with prefixes: `AADNA_`, general topic indicators

### Cross-References

- Internal links use relative paths: `../10_Haplogroups/00_Haplogroup_Reference.md`
- External references consistently link to:
  - YFull tree pages (e.g., `https://www.yfull.com/tree/G-L1264/`)
  - Project website: `https://aadna.ru/`
  - Ancient DNA maps on `haplotree.info`

---

## Working with This Repository

### Adding New Haplogroup Content

1. **Create directory** under `10_Haplogroups/` if new major haplogroup
2. **Create overview file** `00_{Haplogroup}_Overview.md` with:
   - Status indicators
   - TMRCA dates (verified against `current_tree.json`)
   - "Path from Adam" showing full Y-DNA lineage
   - Ancient DNA references
   - Historical context
   - YFull and aadna.ru links
3. **Create subclade files** for major branches (01_, 02_, etc.)
4. **Update** `00_Haplogroup_Reference.md` to link to new overview

### Content Style Guidelines

- **Tone:** Educational but scientifically rigorous, accessible to beginners
- **Language:** Russian content with English technical terms in parentheses where helpful
- **Formatting:**
  - Use blockquotes (`>`) for status notes and metadata
  - Use code blocks for lineage paths
  - Use tables for structured data (branch ages, statistics)
  - Include emoji sparingly for navigation (🧬, 📖, ✅, etc.)
- **Verification:** Always mark TMRCA dates as `✅ *verified*` when confirmed against `current_tree.json`

### Validating Haplogroup Data

Before adding haplogroup information:
1. Check `current_tree.json` for node existence and structure
2. Verify parent-child relationships in the tree
3. Run `validate_hierarchy.py` to check consistency with CSV data
4. Reference YFull for external verification

---

## Important Notes

- **File size considerations:** `current_tree.json` is 14.6MB — use streaming or careful parsing when processing
- **Path hardcoding:** The validation script uses Windows absolute paths that need adjustment for other OSes
- **Asset management:** 128+ image files in `assets/` — maintain consistent naming when adding new visuals
- **Language mixing:** Russian content with English technical terms is intentional and should be preserved
- **Version tracking:** All changes should be documented in `CHANGELOG.md` with semantic versioning

---

## Project Status

Current version: 2.0.0 (2026-01-06)

**Completed phases:**
- ✅ Structure & content migration
- ✅ Visual diagrams and AI-generated illustrations
- ✅ Statistical overview and extended gallery
- ✅ Haplogroup reference documentation (G, J, R, E, C)

**See `task.md` for current project roadmap.**
