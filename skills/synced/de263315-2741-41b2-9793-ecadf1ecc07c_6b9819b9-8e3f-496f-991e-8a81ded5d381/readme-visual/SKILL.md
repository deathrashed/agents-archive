---
name: readme-visual
description: Generate visually stunning README.md files following canonical local design standards. Use when creating, writing, generating, improving, refactoring, or polishing a project README.md. Also use when documenting local projects, CLI utilities, shell configs, automation pipelines, desktop apps, knowledge bases, or multimedia toolkits that require visual structure (hero blocks, badges, Iconify headers, directory trees, interactive tables, collapsible sections, video/image showcase grids).
---

# README Visual

Generate high-impact, polished `README.md` files matching the 6 canonical local README archetypes.

## Workflow

1. **Interview** – Determine what the README should enable and which archetype matches.
2. **Inspect** – Scan the target repo for entry points, config, directory structure, assets, dependencies, integrations.
3. **Select Archetype** – Pick from 6 canonical styles based on project type.
4. **Draft** – Build hero block, badges, Iconify sections, tables, ASCII tree, details cards, alerts.
5. **Verify** – Run through the Mandatory Checklist.

## Progressive Disclosure Design

**SKILL.md** contains the 5-step workflow and the 12-point Mandatory Checklist.

**references/** contains variant-specific templates and token specifications:
- `local-visual-archetypes.md` — Exact badge colors, nav separators, header icons per archetype
- `icons-and-shields.md` — Iconify SVG syntax, shields.io formulas, color hexes
- `readme-style-contract.md` — Structural requirements (hero block, table format, alerts)

Scripts in `scripts/` generate deterministic outputs:
- `scripts/generate-badge-row.py` — Produces shields.io badge HTML from YAML

---

## Archetype Selection

Match project to one of 6 archetypes. Read the matching reference for exact visual signatures.

| Archetype | Use Case | Badge Color | Nav Separator | Header Icon |
| --- | --- | --- | --- | --- |
| **Mp3tag Collection** | Modular bundles, tag sources, action groups | Gold `#faa701` on dark `#1e1e1e` | Dot `·` | Gold Iconify |
| **Zsh Shell Config** | Shell environments, dotfiles, lazy loading | White on dark `#1e1e1e` | Bullet `•` | Unicode glyphs |
| **KB System Base** | Knowledge bases, architecture docs | Cyan `#01acd7` on dark | Pipe `\|` | Cyan Iconify |
| **Go CLI Utility** | Go binaries, provider grids, TUI apps | Cyan `#01acd7` | Pipe `\|` | Cyan Iconify |
| **Blogger Pipeline** | Scraping, automation bots, API pipelines | Black | Pipe `\|` | Readmecodegen |
| **Clipped Toolkit** | Media processing, video generation | Green `#11c866` on dark | Pipe `\|` | Green Iconify |

---

## Workflow Steps

### Step 1: Interview

Determine:
- What should the README enable? (first-time install, daily reference, automation integration?)
- Which archetype matches? (use table above)
- Expected visual elements? (hero + badges + Iconify sections + tables + tree + details)
- **Color palette**: does a header image exist, and which of its colors should drive badges/Iconify headers? If unclear or multiple candidates, ask the user before drafting.

### Step 2: Inspect Repository

Scan for:
- **Entry points**: `bin/`, `src/`, `cmd/`, `main.go`, `pom.xml`, `package.json`
- **Config files**: `config.toml`, `.env.example`, `pyproject.toml`, `Cargo.toml`
- **Assets**: `assets/icon.png`, `assets/banner.png`, `data/header.png`
- **Integrations**: `integrations/`, `macros/`, `scripts/`
- **Dependencies**: `go.mod`, `requirements.txt`, `Cargo.lock`, `package.json`

### Step 3: Select Archetype

Read `references/local-visual-archetypes.md` and match project type to archetype. If hybrid (e.g., Go CLI that renders video), pick dominant form and borrow secondary elements.

### Step 4: Draft README

Build in this order:
1. Centered hero block (`\<div align="center">`)
2. Shields.io badge row (dark base, `style=for-the-badge`, archetype-appropriate color)
3. Quick-nav bar (`·` or `\|` separator per archetype)
4. Quick start code block (clone, build, execute)
5. Iconify section headers (`## \<img src="https://api.iconify.design/mdi:..." ...\>`)
6. Structured data tables (commands, config, providers, templates, macros)
7. ASCII directory tree in fenced code block with inline comments
8. Collapsible details cards for verbose content
9. GitHub alerts (`> [!TIP]`, `> [!NOTE]`, `> [!WARNING]`)

### Color Harmony (Header-Image-Derived)

When the project has a header/logo image, derive the accent palette from it instead of defaulting to the archetype color:

1. **Extract 2 colors from the header image**: a dominant accent (badge backgrounds, primary Iconify color) and a secondary accent (badge `logoColor`, alternating Iconify color).
2. **Apply consistently**: badge background = dominant accent, `logoColor` = secondary accent; Iconify section headers **alternate** between the two accents down the document.
3. **Ask the user when ambiguous**: if the image has more than two strong colors, or the user hasn't provided an image, ask which colors they want before drafting. Never silently pick a palette that clashes with their image.
4. **shields.io constraints**: the badge color field takes ONE hex (no `#`, URL-encode as-is, e.g. `badge/label-value-cf1f25`); two-tone label/value badges (`-colorA-colorB`) are unreliable on GitHub — prefer single background color + `logoColor`. Hex in query params (`logoColor`, Iconify `?color=`) must be `%23`-prefixed.

### Hero Centering Rule

GitHub's renderer does not reliably inherit `align` from a wrapper `<div>`. Every hero child element must carry its own `align="center"`:

```html
<div align="center">
  <img src="assets/icon.png" width="200">
  <h1 align="center">NAME</h1>
  <p align="center"><strong>Summary.</strong></p>
  <p align="center">badges</p>
  <p align="center">nav</p>
</div>
```

Verify after drafting: image, title, summary, badges, and quick-nav are ALL centered — not just the wrapper.

### Step 5: Verify Quality

Run through all 12 Mandatory Checklist items below. Every item must pass.

---

## Mandatory Checklist (13 Items)

Before yielding, confirm each item:

1. **Hero block**: `<div align="center">` with logo/icon, styled title, bold summary, badges — and **every hero child carries its own `align="center"`** (GitHub does not inherit it from the div).
2. **Badge palette**: Dark base (`#1e1e1e` or `#111111`) + archetype color (`style=for-the-badge`) — **or colors derived from the header image** (see Color Harmony).
3. **Color harmony**: badge backgrounds, `logoColor`, and Iconify header colors all derive from the header image's palette (dominant + secondary accent, Iconify alternating); user asked for color preferences when ambiguous.
4. **Navigation bar**: Links with correct separator (`·` for Mp3tag, `\|` for others, `•` for Zsh).
5. **Quick start near top**: Code block within first 40 lines, after hero/nav, before long sections.
6. **Section headers**: Every `##` starts with Iconify SVG or readmecodegen icon (no bare headings).
7. **URL-encoded colors**: Iconify uses `%23` for `#` (e.g., `%2301acd7` for cyan).
8. **At least one table**: Commands, config, providers, templates, or dependencies.
9. **ASCII tree**: Fenced code block with file comments (`# Executable binaries`, `# Source code`).
10. **Collapsible cards**: At least one `<details><summary>` for verbose content.
11. **GitHub alerts**: Used only for setup requirements or critical notes.
12. **No emoji headers**: Iconify SVG or readmecodegen icons only in section headers.
13. **Relative links work**: `README.md`, `docs/INTEGRATIONS.md`, etc., match actual paths.

---

## Reference Files

Load these references as needed (not all at once):

- `references/local-visual-archetypes.md` — Badge colors, nav separators, header icons per archetype
- `references/icons-and-shields.md` — Iconify syntax (`https://api.iconify.design/mdi:...`), shields.io (`style=for-the-badge`), color hex encoding
- `references/readme-style-contract.md` — Hero block structure, table formats, alert syntax

---

## Script Utilities

Run these scripts for deterministic tasks:

```bash
# Generate badge row from YAML config
python scripts/generate-badge-row.py config.yaml

# Validate README against checklist
python scripts/validate-readme.py README.md
```

Scripts execute without loading into context (zero context cost).

---

## Red Flags & Corrections

| Claim | Reality |
| --- | --- |
| Plain `# Title` header is enough | All 8 canonical READMEs use `<div align="center">` hero block |
| `align="center"` on the wrapper div is enough | GitHub does not inherit it — every hero child needs its own `align="center"` |
| Standard GitHub badges are fine | Dark badge palette (`#1e1e1e`) + custom logo colors |
| Any badge colors will do | Badge + Iconify colors should derive from the header image palette (or be confirmed with the user) |
| Emojis are okay for headers | Iconify SVG or readmecodegen icons render consistently across OS |
| Bullet lists replace ASCII trees | Trees in code blocks are faster to scan |
| 50 lines of setup inline | Wrap in `<details><summary>` collapsible cards |
| Single archetype for all projects | Some projects need hybrid approaches (e.g., Go CLI + video showcase) |

---

## Reference Artifacts

This skill is verified against 8 canonical READMEs:

- Mp3tag: `/Users/rd/.config/mp3tag/README.md` (905 lines)
- Zsh: `/Users/rd/.agents/README.md` (324 lines)  
- Kov/COVIT: `/Users/rd/Projects/cov/README.md` (301 lines)
- Audio/COV: `/Users/rd/Scripts/Riley/audio/cov/README.md`
- Clipped-go: `/Users/rd/Scripts/Riley/clipped-go/README.md`
- Clipped: `/Users/rd/Scripts/Riley/clipped/README.md`
- Deemon: `/Users/rd/Scripts/Riley/deemon/README.md` (1195 lines)
- Lastfm-scrobbler: `/Users/rd/Scripts/Riley/lastfm-scrobbler/README.md` (786 lines)
- Metallum-nim: `/Users/rd/Scripts/Riley/metallum-nim/README.md` (463 lines)

---

## Cross-Reference to Skill-Creator Methodology

This skill follows the **skill-progressive-disclosure-design** principles:
- Metadata (name/description) triggers loading (~100 words)
- SKILL.md body loads when skill triggers (~3k words)
- References load only when explicitly pointed to (lazy loading)

Pointer hygiene guidelines:
- Read `references/local-visual-archetypes.md` when selecting visual style
- Read `references/icons-and-shields.md` when adding badges/icons
- Read `references/readme-style-contract.md` for structural requirements