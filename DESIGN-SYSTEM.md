# WPFY Design System

**Concept:** Sealed Stack Cross-Section  
**Register:** Brand (marketing)  
**Live guide:** `design-system/index.html`

## Brand premise

WPFY manages WordPress infrastructure from a CLI. Each site is an isolated Docker Compose stack. The brand visual is the **sealed stack** — a vertical cross-section with hard isolation rails.

## Visual metaphor

A rackmount faceplate + sealed container cross-section. Layers are stamped, not carded. Boundaries are structural, not decorative.

## Logo treatment

Text mark `wpfy_` in Bricolage Grotesque, weight 700. Underscore is part of the mark. No icon required in chrome; stack object carries identity in hero.

## Color system (OKLCH → hex working values)

| Role | Token | Value | Use |
|------|-------|-------|-----|
| Canvas | `--color-canvas` | `#ffffff` | Page background |
| Ink | `--color-ink` | `#141714` | Primary text |
| Ink muted | `--color-ink-muted` | `#3d453f` | Secondary text |
| Olive (primary) | `--color-olive` | `#3a4a28` | Brand bands, primary CTA |
| Olive deep | `--color-olive-deep` | `#243018` | Dark surfaces |
| Olive soft | `--color-olive-soft` | `#e8efe0` | Soft bands |
| Oxide (accent) | `--color-oxide` | `#b54a2a` | Signal, focus accents, WARN |
| Slate rail | `--color-rail` | `#c5cbc0` | Borders, stack rails |
| Surface | `--color-surface` | `#f4f6f2` | Code/terminal wells |
| Status ok | `--color-ok` | `#2f6b45` | PASS |
| Status warn | `--color-warn` | `#9a6b12` | WARN |
| Status fail | `--color-fail` | `#9b1c1c` | FAIL |
| Focus | `--color-focus` | `#b54a2a` | Focus ring |

Strategy: **Committed** olive. Pure white canvas. Oxide ≤10% accent. No purple, no cream body, no neon.

## Typography

| Role | Family | Notes |
|------|--------|-------|
| Display / UI | Bricolage Grotesque | Stamped industrial; weights 500–800 |
| Mono / commands | JetBrains Mono | Commands, labels, terminal |

### Type scale

| Token | Size |
|-------|------|
| `--text-xs` | 0.75rem |
| `--text-sm` | 0.875rem |
| `--text-base` | 1rem |
| `--text-md` | 1.125rem |
| `--text-lg` | 1.25rem |
| `--text-xl` | clamp(1.5rem, 2.2vw, 1.75rem) |
| `--text-2xl` | clamp(1.875rem, 3vw, 2.25rem) |
| `--text-3xl` | clamp(2.25rem, 4vw, 3rem) |
| `--text-hero` | clamp(2.5rem, 5.5vw, 4rem) |

Line heights: display 1.05–1.15; body 1.55; mono 1.45.  
Letter-spacing display: -0.02em to -0.03em (floor -0.04em).

## Spacing / containers

Spacing scale: 4, 8, 12, 16, 24, 32, 48, 64, 96, 128.  
Containers: `--container-sm` 40rem, `--container` 72rem, `--container-wide` 88rem.

## Borders / radius / elevation

- Borders: 1px `--color-rail`; stack rails 2px `--color-olive`
- Radius: `--radius-sm` 2px, `--radius-md` 4px, `--radius-lg` 8px — **no pills, no 16px+ cards**
- Elevation: prefer borders over shadows; max `--shadow-sm` for sticky header only

## Iconography / illustration

- Prefer SVG stack layers, rails, status stamps
- No cartoon doodles, no floating logos, no fake screenshots
- Generated imagery optional for atmosphere only; meaning must survive without it

## Diagram language

- Vertical stack modules with layer labels
- Connectors = thin rails, not arrows soup
- Technical labels: uppercase tracked mono, short

## Code / terminal

- Surface `--color-surface` or olive-deep for dark terminal
- Mono 0.8125–0.875rem
- Copy control adjacent, not inside fake window chrome excess
- Real commands only

## Motion

- Durations: 120 / 200 / 320ms
- Easing: `cubic-bezier(0.16, 1, 0.3, 1)`
- Hero: layer assemble (stagger ≤80ms)
- Scroll: opacity/transform only; content visible by default
- `prefers-reduced-motion: reduce` → static assembled stack, no stagger

## Focus / a11y

- Focus ring: 2px oxide outline, 2px offset
- Skip link required
- Contrast: body ≥4.5:1; large text ≥3:1

## Responsive

- Mobile: stack object becomes compact vertical strip; commands scroll-x inside wells
- Breakpoints: 640 / 768 / 1024 / 1280

## Dark surfaces

Olive-deep bands for architecture / CTA. Ink inverted to `#f4f6f2`. Oxide remains accent.

## Components

See `design-system/index.html` for rendered states: announce, header, nav, buttons, badges, command chip/block, terminal, stack node, connectors, comparison row, notices, CTA, footer, form, mobile nav.
