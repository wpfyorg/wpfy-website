# Design Concept Decision

**Date:** 2026-07-10  
**Coordinator decision:** Concept B — Sealed Stack Cross-Section  
**Status:** Selected and binding for design system + homepage

---

## Concept A — Routing Field Map

| Field | Detail |
|-------|--------|
| Core idea | Page composition as Traefik routing map: host → edge → isolated site networks |
| Signature visual | Full-bleed SVG route graph that expands into site nodes |
| Page rhythm | Map → zoom into one site → operations along edges → boundaries as unreachable zones |
| Typography | Condensed industrial sans + mono labels |
| Color logic | Steel blue routes on near-black field; signal amber for active path |
| Diagram style | Network topology, labeled edges |
| Command presentation | Commands as route actions on selected node |
| Motion | Path draw-on, node pulse on focus |
| Strengths | Strong infra metaphor; unique vs SaaS cards |
| Risks | Reads as generic “network diagram SaaS”; Traefik-specific; dense on mobile |
| WPFY-specific? | Partial — routing is real, but isolation/backup underplayed |

**Score:** Product 18/25 · Originality 14/20 · Credibility 12/15 · Clarity 10/15 · A11y 7/10 · Perf 8/10 · Bricks 3/5 → **72**

---

## Concept B — Sealed Stack Cross-Section (SELECTED)

| Field | Detail |
|-------|--------|
| Core idea | Every WordPress site is a sealed vertical stack unit. Isolation is the brand. |
| Signature visual | Living site-stack object: Edge → App → Data → Cache → Backup, hard boundary rails |
| Page rhythm | Build stack in hero → why seal matters → architecture expand → ops as stack actions → install → boundaries outside the seal → CTA |
| Typography | Bricolage Grotesque (stamped/industrial) + JetBrains Mono (commands) |
| Color logic | Deep olive primary (seed hue ~110) committed on pure white; oxide signal accent; slate ink |
| Diagram style | Cross-section layers with stamped technical labels, not cards |
| Command presentation | Commands map to stack layers / operator verbs |
| Motion | Layer assemble on load; scroll reveals deepen stack; reduced-motion = static full stack |
| Strengths | Inseparable from WPFY architecture; memorable; explains isolation without docs dump |
| Risks | Over-diagramming; must keep copy primary in hero |
| WPFY-specific? | Yes — per-site Compose stack is the product |

**Score:** Product 24/25 · Originality 17/20 · Credibility 14/15 · Clarity 13/15 · A11y 8/10 · Perf 9/10 · Bricks 4/5 → **89**

---

## Concept C — Ops Field Manual

| Field | Detail |
|-------|--------|
| Core idea | Marketing page as numbered field manual: procedures, status stamps, checklists |
| Signature visual | Procedure strip with PASS/WARN/FAIL telemetry language |
| Page rhythm | Cover → procedure chapters → command appendix → safety sheet |
| Typography | Narrow grotesque + mono; heavy numbering |
| Color logic | Paper-white with ink stamps; olive headers; oxide WARN |
| Diagram style | Checklist + stamped callouts |
| Command presentation | Numbered runbooks |
| Motion | Stamp-in reveals; minimal |
| Strengths | Credible to operators; honest tone |
| Risks | Feels like docs, not brand; weak signature visual; easy to confuse with docs site |
| WPFY-specific? | Tone yes; visual identity weak |

**Score:** Product 20/25 · Originality 12/20 · Credibility 14/15 · Clarity 12/15 · A11y 9/10 · Perf 9/10 · Bricks 4/5 → **80**

---

## Decision

**Select Concept B.**

Compatible borrow from C only: stamped status badges, PASS/WARN/FAIL language in boundaries, numbered install steps — not the full field-manual layout.

Reject A (generic network-map SaaS risk) and full C (docs-site collision).

### Mood phrase

> Server rack at 03:00 — sealed containers, stamped labels, oxide signal lights under cool fluorescent work light.

### Brand test target

After removing the wordmark, the sealed stack cross-section alone must still read as “per-site WordPress infrastructure,” not generic DevOps.
