# WPFY Website → Bricks Migration

Migrating `website/` static HTML/CSS/JS to the WordPress staging site at **https://wpfy.dev.wpfy.org** using Bricks Builder + Novamira MCP.

## Architecture

| Layer | Location | Purpose |
|-------|----------|---------|
| Design tokens | Bricks color palette + 22 CSS variables | Brand colors, spacing, shadows |
| Global classes | Bricks `wpfy-*` classes (**101**) | Buttons, cards, tags, sections, layout |
| Theme style | Bricks "WPFY Main" | Inter body + IBM Plex Mono headings |
| Templates | Bricks header (#9) + footer (#10) | Site chrome |
| Page content | Bricks native elements on front page (#11) | Marketing sections (292 nodes) |
| Behaviors | `bricks-child/assets/wpfy.{css,js}` | Marquee, terminal loop, reveals, eco pipes |
| PHP hooks | `bricks-child/functions.php` + `wpfy-theme.php` | Body class, document title, Gutenberg shell |
| Asset loader | `novamira-sandbox/wpfy-assets.php` | Legacy no-op (enqueue lives in `functions.php`) |

## Native build (2026-06)

All marketing sections use native Bricks `section` / `container` / `block` / `heading` / `text` / `button` / `image` elements. **`html` elements are kept only where Bricks has no equivalent:**

- SVG decorations (clouds, doodles, drifts)
- Eco-pipes `<svg>` (drawn by `wpfy.js`)
- Hero terminal `<pre id="wpfy-hero-term">` + copy button with `data-copy`
- Subscribe form `<input>` + privacy checkbox

Source: `batch2_sections.py`, `bricks_builders.py`, `migrate_to_bricks.py`.

## Rem base

Staging uses Advanced Themer clamp settings (`base-font: 10`). Global classes use **CSS variables with px values** from the static site to avoid rem scaling surprises.

## Deploy

```bash
cd website
python3 migrate_to_bricks.py tokens    # palette, 22 variables, 101 classes, theme style
python3 migrate_to_bricks.py assets    # child theme CSS/JS + theme PHP + marketing hooks
python3 migrate_to_bricks.py templates # header, footer, home page (creates if missing)
python3 migrate_to_bricks.py batch2    # hero + marquee + all sections on front page
python3 migrate_to_bricks.py republish  # refresh templates #9/#10 + re-push batch2
python3 migrate_to_bricks.py legal     # legal pages + Gutenberg templates
python3 migrate_to_bricks.py all       # everything
```

Canonical class/variable JSON is generated from Python:

```bash
python3 bricks_global_classes.py   # → bricks-classes.json (101 classes)
python3 bricks_global_variables.py # → bricks-variables.json (22 variables)
```

## Visual parity (2026-06)

Compare static vs staging at three breakpoints:

```bash
# Terminal 1 — local reference
python3 -m http.server 8766 --bind 127.0.0.1 -d website

# Terminal 2
node compare_sites.mjs http://127.0.0.1:8766/ https://wpfy.dev.wpfy.org/
```

Screenshots: `/tmp/compare-{desktop,tablet,mobile}-{local,wp}.png`  
Report: `/tmp/compare-report.json`

**Desktop audit (final):** 3 non-visual diffs only — announce whitespace (+2 chars), hero `textLen` (terminal animation state), beta `childCount` (static flat DOM vs Bricks container wrapper). All style probes, section presence, and text checks pass.

Parity fixes applied in this pass:

- `bricks-lazy-hidden` override in `wpfy.css`
- Above-fold `.wpfy-reveal.in` in `wpfy.js`
- Hero terminal + copy button as `html` elements
- Subscribe privacy checkbox in form HTML
- `body.wpfy-site` + front-page `<title>` via `functions.php` hooks
- `compare_sites.mjs`: multi-selector style probes, scroll/lazy prime, scoped card counts

## Global classes (101)

Regenerate the full list: `python3 bricks_global_classes.py` or inspect `bricks-classes.json`.

Core layout/chrome: `wpfy-wrap`, `wpfy-section-pad`, `wpfy-section-sky`, `wpfy-site-header`, `wpfy-site-footer`, `wpfy-hero`, `wpfy-heading-mono`, `wpfy-btn`, `wpfy-btn-blue`, `wpfy-btn-ink`, `wpfy-card`, `wpfy-tag*`, `wpfy-code-well`, `wpfy-cta-band`, `wpfy-compare-card`, `wpfy-logo`, plus eco/marquee/step/who/subscribe utilities.

## Sections (static site → Bricks)

- [x] Announce bar + header + hero + marquee
- [x] Problem vs solution (`#problem`)
- [x] Ecosystem diagram (`#stack`) — `wpfy-eco-*` + JS pipes
- [x] Features grid (`#features`) — 8 cards
- [x] How it works (`#how-it-works`) — 3 step cards
- [x] Who is it for (`#who`)
- [x] Use cases (`#use-cases`)
- [x] CTA band (`#beta`)
- [x] Subscribe band (with privacy checkbox)

## Polish / follow-ups

- [ ] Merge marketing hooks from `functions.php` into deployable `wpfy-theme.php` once theme dir is writable via MCP/SFTP
- [ ] `wp bricks regenerate_assets` when WP-CLI is available on staging
- [ ] Happyforms or FluentSMTP wiring for subscribe form (currently placeholder)
- [ ] Decorative edge doodles + drift elements (optional; omitted for cleaner Bricks tree)
- [ ] Legal pages: static HTML in `website/legal/`; import via `python3 migrate_to_bricks.py legal`

## Implementation notes

- Bricks `code` elements do **not** render raw HTML on the frontend when `executeCode: false` — use the `html` element with an `html` setting instead.
- Empty `text-basic` with `tag: pre` may not render — use `html` for terminal output.
- `novamira/write-file` cannot write theme PHP; use `execute-php` + base64 or SFTP.
- Front page: `page_on_front = 11`, slug `home`.

## Child theme note

Asset loading and marketing hooks live in `bricks-child/functions.php`. Gutenberg shell logic is in `wpfy-theme.php` (required from `functions.php`).
