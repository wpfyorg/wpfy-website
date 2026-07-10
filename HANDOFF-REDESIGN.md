# WPFY Marketing Website Redesign — Handoff (2026-07-10)

## 1. Executive summary

The WPFY marketing homepage was fully redesigned in the static source repository toward a **quiet, operational, technically credible** direction aligned with `wpfy-pvt/DESIGN.md` and the public docs brand.

The new page removes cartoon clouds, doodles, promotional marquee, and fake newsletter submission. It adds accurate command groupings, an architecture diagram, capability bands, an honest boundaries table, and RC/beta safety language throughout.

**Static source is complete and previewable.** Bricks migration scripts were updated to extract sections directly from `index.html` for reproducible parity. **Staging deployment could not be completed** because the Novamira MCP endpoint returned HTTP 404 and SFTP credentials were rejected.

Production (`wpfy.org`) was not modified.

---

## 2. Sources reviewed

### Product (read-only)
- `wpfy-pvt/README.md`
- `wpfy-pvt/CHANGELOG.md`
- `wpfy-pvt/ROADMAP.md`
- `wpfy-pvt/DESIGN.md`
- `wpfy-pvt/SECURITY.md`

### Documentation (read-only)
- `wpfy-docs/PRODUCT.md`
- `wpfy-docs/docs/CLI-VM-RELEASE-MATRIX.md`
- `wpfy-docs/docs/COMMANDS.md`
- `wpfy-docs/docs/ARCHITECTURE.md`
- `wpfy-docs/docs/SITE-ISOLATION.md`
- `wpfy-docs/docs/SSL-FLOW.md`
- `wpfy-docs/kb/index.md`
- `wpfy-docs/kb/releases/v1.0.0-rc1.md`

### Website / migration
- `wpfy-website/index.html`, `assets/styles.css`, `assets/main.js`
- `wpfy-website/batch2_sections.py`, `migrate_to_bricks.py`
- `wpfy-website/compare_sites.mjs`, `strict_audit.mjs`
- `wpfy-website/bricks-child-assets/wpfy.css`, `wpfy.js`

---

## 3. Copy decisions

### Positioning
Open-source Docker-first WordPress **infrastructure CLI** for Ubuntu VPS operators — not a hosting company or graphical control panel.

### H1 and subheading
- **H1:** Operate WordPress infrastructure from one CLI.
- **Supporting:** WPFY turns a fresh Ubuntu VPS into an isolated, Docker-backed WordPress host…

### Primary CTAs
- Read the installation guide → `https://docs.wpfy.org/runbooks/fresh-install`
- Install WPFY (header) → same
- View on GitHub → `https://github.com/wpfyorg/wpfy`

### Claim corrections
- Release label: **beta/RC (v1.0.0-rc1)** — not production-ready
- Flat commands primary (`wpfy run`, `wpfy backup`, `wpfy restore`, etc.); grouped `wpfy site` / `wpfy stack` retained
- Isolation: **designed to reduce cross-site blast radius** — no absolute security guarantees
- Wildcard SSL: **Cloudflare-only**
- `wpfy stack migrate`: **not implemented**
- Mutable `main` install reference warning adjacent to install command
- Remote backup lifecycle explicitly WPFY-managed — not provider bucket lifecycle automation

### Limitations exposed
Full **Know the boundaries before you install** table on-page (RC status, Ubuntu-first, no independent security review, multi-tenant out of scope, helper-image behavior, MySQLTuner deferred, backup guidance).

---

## 4. Design system

| Token | Value |
|-------|-------|
| Near black | `#17171c` |
| Canvas | `#ffffff` |
| Ink | `#212121` |
| Deep green | `#003c33` |
| Dark navy | `#071829` |
| Soft stone | `#eeece7` |
| Action blue | `#1863dc` |
| Coral (accents) | `#ff7759` |

**Fonts:** Space Grotesk (display), Inter (body), system monospace (commands)

**Type scale:** Hero `clamp(2.5rem, 5.5vw, 4.25rem)`; section headings `clamp(2rem, 3.8vw, 3rem)`; body `1rem–1.125rem`

**Radius:** 4px controls, 8px cards/code, 16px modules, pill CTAs

**Motion:** 150–220ms transitions; `prefers-reduced-motion` disables reveals and terminal animation

---

## 5. Source files changed

| File | Action |
|------|--------|
| `index.html` | Rebuilt homepage IA and copy |
| `assets/styles.css` | New operational design system |
| `assets/main.js` | Command tabs, copy, nav, terminal, cookie consent |
| `robots.txt` | Added |
| `batch2_sections.py` | Rewritten — extracts sections from `index.html` |
| `migrate_to_bricks.py` | Updated header/footer/hero/colors; removed marquee from deploy; MCP path fix |
| `bricks_builders.py` | Nav/footer class updates |
| `bricks-child-assets/wpfy.css` | Regenerated from static CSS (scoped) |
| `bricks-child-assets/wpfy.js` | Synced from `assets/main.js` |
| `compare_sites.mjs` | New section probes |
| `strict_audit.mjs` | New section IDs |
| `evidence/redesign-20260710/*.png` | Local QA screenshots |

---

## 6. Bricks changes (prepared, not deployed)

| Item | Value |
|------|-------|
| Front page ID | 11 (existing) |
| Header template | 9 |
| Footer template | 10 |
| Deploy command | `python3 migrate_to_bricks.py republish` after MCP restored |
| Section strategy | Hero + 10 HTML blocks extracted from `index.html` |
| Child assets | `wpfy.css`, `wpfy.js` via `migrate_to_bricks.py assets` |

---

## 7. Backup

**Planned path:** `wpfy-website/backups/20260710-redesign/`

Staging Bricks JSON/HTML backup **not captured** — MCP `initialize` returned HTTP 404 before any write operation.

---

## 8. QA performed

### Commands run
```bash
python3 -m http.server 8766 --bind 127.0.0.1 -d wpfy-website
python3 -c "from batch2_sections import build_batch2_sections, extract_hero_section"
node compare_sites.mjs http://127.0.0.1:8766/ https://wpfy.dev.wpfy.org/
# Playwright local screenshots → evidence/redesign-20260710/
python3 migrate_to_bricks.py assets  # failed: MCP 404
```

### Viewports tested (local)
1440×900, 768×1024, 390×844

### Local static results
- All 14 sections render without horizontal overflow
- Command tabs keyboard-accessible (arrow keys)
- Copy button with `aria-live` feedback
- No marquee, doodles, or fake subscribe workflow
- `noscript` fallback lists all command groups
- JSON-LD SoftwareApplication without fake ratings/downloads

### Staging comparison
Expected **large diffs** — staging still serves pre-redesign Bricks build. Parity deploy pending MCP restoration.

---

## 9. Visual-diff evidence

| File | Description |
|------|-------------|
| `evidence/redesign-20260710/local-desktop.png` | Full-page desktop |
| `evidence/redesign-20260710/local-tablet.png` | Full-page tablet |
| `evidence/redesign-20260710/local-mobile.png` | Full-page mobile |
| `/tmp/compare-*-local.png` | Compare script captures |
| `/tmp/compare-report.json` | Structural/style diff report |

---

## 10. Known limitations

1. **Staging not updated** — Novamira MCP endpoint `…/rest_route=/mcp/novamira` returns 404; SFTP upload failed (permission denied).
2. **Bricks global variables/classes** — not regenerated on staging (old MotherDuck-era tokens may persist until `migrate_to_bricks.py tokens` runs).
3. **Visual parity audit vs staging** — blocked until deploy succeeds.
4. **WordPress REST API** — application password test did not return JSON (may need credential rotation).

---

## 11. Deployment status

| Target | Status |
|--------|--------|
| Static source (`wpfy-website`) | **Complete** — preview at `http://127.0.0.1:8766/` |
| Staging (`wpfy.dev.wpfy.org`) | **Not updated** — deploy blocked |
| Production (`wpfy.org`) | **Untouched** |

---

## 12. Next recommended action

Restore Novamira MCP on staging (or refresh WordPress application password / SFTP credentials), then run:

```bash
cd /Users/arnab/Desktop/_Projects/wpfy-website
# Back up Bricks page #11, templates #9/#10 via MCP first
python3 migrate_to_bricks.py assets
python3 migrate_to_bricks.py republish
node compare_sites.mjs http://127.0.0.1:8766/ https://wpfy.dev.wpfy.org/
```

Review diffs; iterate on `wpfy.css` header grid if Bricks wrapper adds extra padding.
