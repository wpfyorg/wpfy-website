"""Canonical WPFY Bricks global class definitions — single source for bricks-classes.json + migrate."""
from __future__ import annotations

import json
from pathlib import Path

from bricks_common import MONO_TYPO

INK_BORDER = {
    "width": {"top": "2px", "right": "2px", "bottom": "2px", "left": "2px"},
    "style": "solid",
    "color": {"raw": "var(--wpfy-ink)"},
}

RADIUS_SM = {"top": "2px", "right": "2px", "bottom": "2px", "left": "2px"}
RADIUS_WIN = {"top": "6px", "right": "6px", "bottom": "6px", "left": "6px"}

CAT_LAYOUT = "cat-f2kike"
CAT_COMPONENTS = "cat-h2505r"
CAT_TYPO = "cat-xui2px"
CAT_SECTIONS = "cat-82wfpb"

CATEGORY_NAMES = {
    CAT_LAYOUT: "WPFY Layout",
    CAT_COMPONENTS: "WPFY Components",
    CAT_TYPO: "WPFY Typography",
    CAT_SECTIONS: "WPFY Sections",
}

# Stable Bricks global-class ids (preserve existing site references).
CLASS_IDS: dict[str, str] = {
    "wpfy-announce": "kwlgfy",
    "wpfy-btn": "rqhdzw",
    "wpfy-btn-blue": "zmaaq6",
    "wpfy-btn-ink": "pvk9yi",
    "wpfy-card": "x7dq9w",
    "wpfy-code-well": "341dll",
    "wpfy-compare-card": "om1ed2",
    "wpfy-cta-band": "j6275y",
    "wpfy-heading-mono": "8fd8sm",
    "wpfy-hero": "rcxsri",
    "wpfy-lede": "vdu3ou",
    "wpfy-logo": "nh1um4",
    "wpfy-section-pad": "ho2lt9",
    "wpfy-section-sky": "2m37s0",
    "wpfy-site-footer": "jt3z16",
    "wpfy-site-header": "ddl72q",
    "wpfy-tag": "j5e7vr",
    "wpfy-tag-blue": "wms9b9",
    "wpfy-tag-red": "tmnqph",
    "wpfy-tag-teal": "exqp6o",
    "wpfy-tag-yellow": "i07w6l",
    "wpfy-wrap": "4prbti",
    # batch 2 — layout
    "wpfy-section-head": "sh1k9m",
    "wpfy-compare": "cm9p2x",
    "wpfy-grid": "gr4d01",
    "wpfy-grid-3": "gr3d02",
    "wpfy-grid-4": "gr4d03",
    "wpfy-who-grid": "whgr01",
    "wpfy-nav": "nv64px",
    "wpfy-footer-grid": "ftgr01",
    "wpfy-footer-inner": "ftin01",
    "wpfy-footer-col": "ftcl01",
    "wpfy-sub-inner": "sbin01",
    # sections
    "wpfy-marquee": "mq001a",
    "wpfy-marquee-yellow": "mqyel1",
    "wpfy-marquee-teal": "mqtel1",
    "wpfy-marquee-track": "mqtrk1",
    "wpfy-subscribe-band": "subbd1",
    "wpfy-eco-section": "ecsec1",
    "wpfy-eco-sky": "ecsky1",
    "wpfy-eco-head": "echd01",
    "wpfy-term-stage": "tmstg1",
    "wpfy-hero-ctas": "hrcta1",
    "wpfy-cta-actions": "ctact1",
    # components
    "wpfy-card-top": "crdtp1",
    "wpfy-step-num": "stpnm1",
    "wpfy-step-card": "stpcr1",
    "wpfy-who-card": "whcrd1",
    "wpfy-who-doodle": "whdoo1",
    "wpfy-eco-box": "ecbox1",
    "wpfy-box-blue": "bxblu1",
    "wpfy-box-teal": "bxtel1",
    "wpfy-box-yellow": "bxyel1",
    "wpfy-box-red": "bxred1",
    "wpfy-box-cream": "bxcrm1",
    "wpfy-eco-item": "ecitm1",
    "wpfy-eco-node": "ecnod1",
    "wpfy-eco-node-bar": "ecnbr1",
    "wpfy-eco-node-body": "ecnby1",
    "wpfy-eco-center": "eccen1",
    "wpfy-eco-center-label": "eclbl1",
    "wpfy-eco-center-sub": "ecsub1",
    "wpfy-eco-diagram": "ecdia1",
    "wpfy-eco-col": "eccol1",
    "wpfy-terminal": "term01",
    "wpfy-term-bar": "trmbar",
    "wpfy-term-dot": "trmdot",
    "wpfy-term-title": "trmtit",
    "wpfy-copy-btn": "cpybtn",
    "wpfy-term-body": "trmbdy",
    "wpfy-bubble": "bubbl1",
    "wpfy-doodle": "doodl1",
    "wpfy-edge-doodle": "edgd01",
    "wpfy-edge-doodle-b": "edgdb1",
    "wpfy-drift": "drift1",
    "wpfy-cta-cloud": "ctcld1",
    "wpfy-cmd-chip": "cmdch1",
    "wpfy-nav-links": "navln1",
    "wpfy-menu-btn": "menub1",
    "wpfy-footer-col-title": "ftctt1",
    "wpfy-footer-links": "ftlnk1",
    "wpfy-footer-meta": "ftmet1",
    "wpfy-footer-bar": "ftbar1",
    "wpfy-sub-copy": "subcp1",
    "wpfy-sub-form": "subfm1",
    "wpfy-sub-status": "subst1",
    "wpfy-uc-row": "ucrow1",
    "wpfy-uc-copy": "uccpy1",
    "wpfy-uc-well": "ucwel1",
    "wpfy-tag-ink": "tagink",
    "wpfy-affiliate-banner": "affbn1",
    # typography / utilities
    "wpfy-eco-sub": "ecsub2",
    "wpfy-li-x": "lix001",
    "wpfy-li-check": "lichk1",
    "wpfy-t-prompt": "tprom1",
    "wpfy-t-cmd": "tcmd01",
    "wpfy-t-out": "tout01",
    "wpfy-t-ok": "took01",
    "wpfy-t-dim": "tdim01",
    "wpfy-sr-only": "sronly",
    "wpfy-reveal": "reveal",
}

# (name, category, settings)
GLOBAL_CLASS_DEFS: list[tuple[str, str, dict]] = [
    # ── Layout ──
    ("wpfy-wrap", CAT_LAYOUT, {
        "_widthMax": "var(--wpfy-container-max)",
        "_margin": {"left": "auto", "right": "auto"},
        "_padding": {"left": "24px", "right": "24px"},
    }),
    ("wpfy-section-pad", CAT_LAYOUT, {
        "_padding": {"top": "var(--wpfy-section-pad)", "bottom": "var(--wpfy-section-pad)"},
        "_padding:mobile_landscape": {"top": "var(--wpfy-section-pad-mobile)", "bottom": "var(--wpfy-section-pad-mobile)"},
    }),
    ("wpfy-announce", CAT_LAYOUT, {
        "_background": {"color": {"raw": "var(--wpfy-yellow)"}},
        "_border": {"width": {"bottom": "2px"}, "style": "solid", "color": {"raw": "var(--wpfy-ink)"}},
        "_typography": {**MONO_TYPO, "font-size": "0.75rem", "text-align": "center"},
        "_padding": {"top": "10px", "bottom": "10px", "left": "16px", "right": "16px"},
        "_cssCustom": (
            "%root% a { font-weight: 600; text-decoration: underline; text-underline-offset: 3px; } "
            "%root% a:hover { background: var(--wpfy-ink); color: var(--wpfy-yellow); text-decoration: none; }"
        ),
    }),
    ("wpfy-site-header", CAT_LAYOUT, {
        "_position": "sticky",
        "_top": "0",
        "_zIndex": "50",
        "_background": {"color": {"raw": "var(--wpfy-cream)"}},
        "_border": {"width": {"bottom": "2px"}, "style": "solid", "color": {"raw": "var(--wpfy-ink)"}},
    }),
    ("wpfy-nav", CAT_LAYOUT, {
        "_display": "flex",
        "_alignItems": "center",
        "_heightMin": "64px",
        "_columnGap": "28px",
        "_position": "relative",
    }),
    ("wpfy-site-footer", CAT_LAYOUT, {
        "_background": {"color": {"raw": "var(--wpfy-ink)"}},
        "_typography": {"color": {"raw": "var(--wpfy-cream)"}},
        "_padding": {"top": "64px", "bottom": "0"},
    }),
    ("wpfy-footer-inner", CAT_LAYOUT, {
        "_widthMax": "var(--wpfy-container-max)",
        "_margin": {"left": "auto", "right": "auto"},
        "_padding": {"left": "24px", "right": "24px"},
    }),
    ("wpfy-footer-grid", CAT_LAYOUT, {
        "_display": "grid",
        "_gridTemplateColumns": "repeat(4, minmax(0, 1fr))",
        "_gridGap": "32px 40px",
        "_padding": {"bottom": "48px"},
        "_gridTemplateColumns:mobile_landscape": "repeat(2, minmax(0, 1fr))",
        "_gridTemplateColumns:mobile_portrait": "1fr",
    }),
    ("wpfy-footer-col", CAT_LAYOUT, {}),
    ("wpfy-sub-inner", CAT_LAYOUT, {
        "_display": "flex",
        "_alignItems": "center",
        "_justifyContent": "space-between",
        "_flexWrap": "wrap",
        "_columnGap": "48px",
        "_rowGap": "32px",
        "_width": "100%",
    }),
    # ── Sections ──
    ("wpfy-section-sky", CAT_SECTIONS, {
        "_background": {"color": {"raw": "var(--wpfy-blue-deep)"}},
        "_border": {
            "width": {"top": "2px", "bottom": "2px"},
            "style": "solid",
            "color": {"raw": "var(--wpfy-ink)"},
        },
        "_cssCustom": "%root% { --wpfy-ink-soft: var(--wpfy-ink); }",
    }),
    ("wpfy-hero", CAT_SECTIONS, {
        "_padding": {"top": "88px", "bottom": "72px"},
        "_typography": {"text-align": "center"},
        "_position": "relative",
        "_padding:mobile_portrait": {"top": "64px"},
        "_cssCustom": (
            "@media (max-width:680px) { %root% { text-align: left; } "
            "%root% .wpfy-hero-ctas { justify-content: flex-start; } }"
        ),
    }),
    ("wpfy-hero-ctas", CAT_SECTIONS, {
        "_display": "flex",
        "_columnGap": "16px",
        "_justifyContent": "center",
        "_flexWrap": "wrap",
    }),
    ("wpfy-cta-band", CAT_SECTIONS, {
        "_background": {"color": {"raw": "var(--wpfy-yellow)"}},
        "_border": {
            "width": {"top": "2px", "bottom": "2px"},
            "style": "solid",
            "color": {"raw": "var(--wpfy-ink)"},
        },
        "_padding": {"top": "88px", "bottom": "88px"},
        "_typography": {"text-align": "center"},
        "_position": "relative",
        "_padding:mobile_landscape": {"top": "72px", "bottom": "72px"},
    }),
    ("wpfy-cta-actions", CAT_SECTIONS, {
        "_display": "flex",
        "_columnGap": "16px",
        "_justifyContent": "center",
        "_flexWrap": "wrap",
    }),
    ("wpfy-section-head", CAT_SECTIONS, {
        "_typography": {"text-align": "center"},
        "_margin": {"bottom": "48px"},
        "_width": "100%",
        "_cssCustom": "%root% .wpfy-lede { margin-left: auto; margin-right: auto; margin-bottom: 0; }",
    }),
    ("wpfy-marquee", CAT_SECTIONS, {
        "_border": {
            "width": {"top": "2px", "bottom": "2px"},
            "style": "solid",
            "color": {"raw": "var(--wpfy-ink)"},
        },
        "_overflow": "hidden",
        "_padding": {"top": "14px", "bottom": "14px"},
    }),
    ("wpfy-marquee-yellow", CAT_SECTIONS, {
        "_background": {"color": {"raw": "var(--wpfy-yellow)"}},
    }),
    ("wpfy-marquee-teal", CAT_SECTIONS, {
        "_background": {"color": {"raw": "var(--wpfy-teal)"}},
    }),
    ("wpfy-marquee-track", CAT_SECTIONS, {
        "_display": "flex",
        "_columnGap": "48px",
        "_typography": {
            "font-family": "IBM Plex Mono",
            "font-size": "1.4rem",
            "text-transform": "uppercase",
            "letter-spacing": "0.04em",
            "white-space": "nowrap",
        },
        "_cssCustom": (
            "%root% { width: max-content; animation: wpfy-marquee 45s linear infinite; } "
            "%root% span { flex: none; } "
            "@keyframes wpfy-marquee { from { transform: translateX(0); } to { transform: translateX(-50%); } } "
            "@media (max-width:768px) { %root% { font-size: 1.05rem; } } "
            "@media (prefers-reduced-motion: reduce) { %root% { animation: none; } }"
        ),
    }),
    ("wpfy-subscribe-band", CAT_SECTIONS, {
        "_background": {"color": {"raw": "var(--wpfy-blue-deep)"}},
        "_border": {"width": {"bottom": "2px"}, "style": "solid", "color": {"raw": "var(--wpfy-ink)"}},
        "_padding": {"top": "72px", "bottom": "72px"},
        "_position": "relative",
        "_overflow": "visible",
        "_width": "100%",
    }),
    ("wpfy-eco-section", CAT_SECTIONS, {
        "_padding": {"top": "0", "bottom": "var(--wpfy-section-pad)"},
        "_background": {"color": {"raw": "var(--wpfy-cream)"}},
        "_cssCustom": (
            "%root% { "
            "background-image: "
            "linear-gradient(rgba(56,56,56,0.07) 1px, transparent 1px), "
            "linear-gradient(90deg, rgba(56,56,56,0.07) 1px, transparent 1px); "
            "background-size: 56px 56px; "
            "}"
        ),
    }),
    ("wpfy-eco-sky", CAT_SECTIONS, {
        "_position": "relative",
        "_height": "130px",
        "_background": {"color": {"raw": "var(--wpfy-blue-deep)"}},
        "_border": {"width": {"bottom": "2px"}, "style": "solid", "color": {"raw": "var(--wpfy-ink)"}},
        "_margin": {"bottom": "56px"},
        "_height:mobile_portrait": "96px",
        "_margin:mobile_portrait": {"bottom": "40px"},
    }),
    ("wpfy-eco-head", CAT_SECTIONS, {
        "_typography": {"text-align": "center"},
    }),
    ("wpfy-eco-diagram", CAT_SECTIONS, {
        "_display": "grid",
        "_gridTemplateColumns": "minmax(0, 1fr) 200px minmax(0, 1fr)",
        "_gridGap": "32px 56px",
        "_alignItems": "center",
        "_margin": {"top": "56px"},
        "_position": "relative",
        "_gridTemplateColumns:tablet_portrait": "1fr",
        "_gridGap:tablet_portrait": "28px",
    }),
    ("wpfy-eco-col", CAT_SECTIONS, {
        "_display": "grid",
        "_rowGap": "28px",
        "_position": "relative",
        "_zIndex": "1",
    }),
    ("wpfy-term-stage", CAT_SECTIONS, {
        "_position": "relative",
        "_widthMax": "860px",
        "_margin": {"top": "64px", "left": "auto", "right": "auto"},
    }),
    ("wpfy-grid", CAT_SECTIONS, {
        "_display": "grid",
        "_gridGap": "24px",
        "_margin": {"top": "48px"},
    }),
    ("wpfy-grid-3", CAT_SECTIONS, {
        "_gridTemplateColumns": "repeat(3, 1fr)",
        "_gridTemplateColumns:mobile_landscape": "1fr",
    }),
    ("wpfy-grid-4", CAT_SECTIONS, {
        "_gridTemplateColumns": "repeat(4, 1fr)",
        "_gridTemplateColumns:tablet_portrait": "repeat(2, 1fr)",
        "_gridTemplateColumns:mobile_portrait": "1fr",
    }),
    ("wpfy-who-grid", CAT_SECTIONS, {
        "_gridGap:mobile_landscape": "40px",
    }),
    ("wpfy-compare", CAT_SECTIONS, {
        "_display": "grid",
        "_gridTemplateColumns": "1fr 1fr",
        "_gridGap": "32px",
        "_margin": {"top": "48px"},
        "_gridTemplateColumns:mobile_landscape": "1fr",
    }),
    ("wpfy-uc-row", CAT_SECTIONS, {
        "_display": "grid",
        "_gridTemplateColumns": "minmax(0, 1fr) minmax(0, 1fr)",
        "_gridGap": "48px",
        "_alignItems": "center",
        "_margin": {"top": "64px"},
        "_gridTemplateColumns:mobile_landscape": "1fr",
        "_gridGap:mobile_landscape": "24px",
        "_margin:mobile_landscape": {"top": "56px"},
    }),
    # ── Components ──
    ("wpfy-btn", CAT_COMPONENTS, {
        "_display": "inline-flex",
        "_alignItems": "center",
        "_justifyContent": "center",
        "_gap": "8px",
        "_typography": {**MONO_TYPO, "font-size": "0.8rem", "font-weight": "500"},
        "_background": {"color": {"raw": "var(--wpfy-cream)"}},
        "_border": {**INK_BORDER, "radius": RADIUS_SM},
        "_padding": {"top": "11px", "right": "20px", "bottom": "11px", "left": "20px"},
        "_boxShadow": {"values": {"offsetX": "3", "offsetY": "3", "blur": "0"}, "color": {"raw": "var(--wpfy-ink)"}},
        "_cssCustom": (
            "%root% { min-height: 44px; white-space: nowrap; "
            "transition: transform 0.15s cubic-bezier(0.23,1,0.32,1), box-shadow 0.15s cubic-bezier(0.23,1,0.32,1); } "
            "%root%:hover { transform: translate(-2px,-2px); box-shadow: var(--wpfy-shadow); } "
            "%root%:active { transform: translate(2px,2px); box-shadow: 0 0 0 var(--wpfy-ink); }"
        ),
    }),
    ("wpfy-btn-blue", CAT_COMPONENTS, {"_background": {"color": {"raw": "var(--wpfy-blue)"}}}),
    ("wpfy-btn-ink", CAT_COMPONENTS, {
        "_background": {"color": {"raw": "var(--wpfy-ink)"}},
        "_typography": {**MONO_TYPO, "font-size": "0.8rem", "font-weight": "500", "color": {"raw": "var(--wpfy-cream)"}},
    }),
    ("wpfy-card", CAT_COMPONENTS, {
        "_background": {"color": {"raw": "var(--wpfy-paper)"}},
        "_border": {**INK_BORDER, "radius": RADIUS_SM},
        "_padding": {"top": "24px", "right": "24px", "bottom": "24px", "left": "24px"},
        "_cssCustom": (
            "%root% { transition: transform 0.15s cubic-bezier(0.23,1,0.32,1), box-shadow 0.15s cubic-bezier(0.23,1,0.32,1); } "
            "@media (hover:hover) and (pointer:fine) { %root%:hover { transform: translate(-2px,-2px); box-shadow: var(--wpfy-shadow); } }"
        ),
    }),
    ("wpfy-card-top", CAT_COMPONENTS, {
        "_display": "flex",
        "_alignItems": "center",
        "_columnGap": "10px",
    }),
    ("wpfy-step-card", CAT_COMPONENTS, {}),
    ("wpfy-step-num", CAT_COMPONENTS, {
        "_display": "inline-flex",
        "_alignItems": "center",
        "_justifyContent": "center",
        "_width": "34px",
        "_height": "34px",
        "_typography": {"font-family": "IBM Plex Mono", "font-weight": "700", "font-size": "0.95rem"},
        "_background": {"color": {"raw": "var(--wpfy-yellow)"}},
        "_border": {**INK_BORDER, "radius": {"top": "50%", "right": "50%", "bottom": "50%", "left": "50%"}},
    }),
    ("wpfy-compare-card", CAT_COMPONENTS, {
        "_background": {"color": {"raw": "var(--wpfy-paper)"}},
        "_border": {**INK_BORDER, "radius": RADIUS_SM},
        "_padding": {"top": "28px", "right": "28px", "bottom": "28px", "left": "28px"},
        "_boxShadow": {"values": {"offsetX": "5", "offsetY": "5", "blur": "0"}, "color": {"raw": "var(--wpfy-ink)"}},
        "_cssCustom": (
            "%root% ul { list-style: none; display: grid; gap: 14px; margin: 0; padding: 0; } "
            "%root% .wpfy-tag { margin-bottom: 20px; } "
            "%root% li { display: grid; grid-template-columns: 22px 1fr; gap: 10px; "
            "font-size: 0.95rem; color: var(--wpfy-ink-soft); } "
            "%root% li strong { color: var(--wpfy-ink); display: block; font-weight: 600; }"
        ),
    }),
    ("wpfy-tag", CAT_COMPONENTS, {
        "_display": "inline-flex",
        "_alignItems": "center",
        "_gap": "6px",
        "_typography": {**MONO_TYPO, "font-size": "0.72rem", "font-weight": "600", "letter-spacing": "0.05em"},
        "_border": {**INK_BORDER, "radius": RADIUS_SM},
        "_padding": {"top": "4px", "right": "10px", "bottom": "4px", "left": "10px"},
    }),
    ("wpfy-tag-yellow", CAT_COMPONENTS, {"_background": {"color": {"raw": "var(--wpfy-yellow)"}}}),
    ("wpfy-tag-teal", CAT_COMPONENTS, {"_background": {"color": {"raw": "var(--wpfy-teal)"}}}),
    ("wpfy-tag-blue", CAT_COMPONENTS, {"_background": {"color": {"raw": "var(--wpfy-blue)"}}}),
    ("wpfy-tag-red", CAT_COMPONENTS, {
        "_background": {"color": {"raw": "var(--wpfy-red)"}},
        "_typography": {**MONO_TYPO, "font-size": "0.72rem", "font-weight": "600", "color": {"raw": "var(--wpfy-paper)"}},
    }),
    ("wpfy-tag-ink", CAT_COMPONENTS, {
        "_background": {"color": {"raw": "var(--wpfy-ink)"}},
        "_typography": {"color": {"raw": "var(--wpfy-cream)"}},
        "_border": {"color": {"raw": "var(--wpfy-ink)"}},
    }),
    ("wpfy-code-well", CAT_COMPONENTS, {
        "_background": {"color": {"raw": "var(--wpfy-ink)"}},
        "_typography": {"font-family": "IBM Plex Mono", "font-size": "0.76rem", "line-height": "1.85", "color": {"raw": "var(--wpfy-cream)"}},
        "_border": {"radius": RADIUS_SM},
        "_padding": {"top": "14px", "right": "16px", "bottom": "14px", "left": "16px"},
        "_margin": {"top": "16px"},
        "_cssCustom": "%root% { overflow-x: auto; white-space: pre; }",
    }),
    ("wpfy-uc-well", CAT_COMPONENTS, {
        "_margin": {"top": "0"},
        "_border": INK_BORDER,
        "_boxShadow": {"values": {"offsetX": "5", "offsetY": "5", "blur": "0"}, "color": {"raw": "var(--wpfy-ink)"}},
        "_typography": {"font-size": "0.8rem"},
        "_padding": {"top": "20px", "right": "22px", "bottom": "20px", "left": "22px"},
    }),
    ("wpfy-who-card", CAT_COMPONENTS, {
        "_display": "flex",
        "_direction": "column",
        "_alignItems": "center",
        "_typography": {"text-align": "center"},
        "_cssCustom": (
            "%root% .wpfy-tag { margin-bottom: 14px; } "
            "%root% p { font-size: 0.95rem; color: var(--wpfy-ink-soft); max-width: 300px; margin: 0 auto; }"
        ),
    }),
    ("wpfy-who-doodle", CAT_COMPONENTS, {
        "_width": "34px",
        "_margin": {"bottom": "18px"},
        "_cssCustom": "%root% svg { width: 100%; height: auto; }",
    }),
    ("wpfy-eco-box", CAT_COMPONENTS, {
        "_position": "relative",
        "_border": {**INK_BORDER, "radius": RADIUS_WIN},
        "_padding": {"top": "16px", "right": "18px", "bottom": "18px", "left": "18px"},
        "_background": {"color": {"raw": "var(--wpfy-paper)"}},
        "_zIndex": "1",
        "_cssCustom": (
            "%root% { transition: transform 0.15s cubic-bezier(0.23,1,0.32,1), box-shadow 0.15s, border-radius 0.15s; } "
            "%root% h3 { font-family: IBM Plex Mono, monospace; font-size: 0.78rem; text-align: center; "
            "margin: 0 0 12px; letter-spacing: 0.08em; text-transform: uppercase; } "
            "@media (hover:hover) and (pointer:fine) { "
            "%root%:hover { transform: translate(-2px,-2px); border-radius: 14px; box-shadow: var(--wpfy-shadow); } }"
        ),
    }),
    ("wpfy-box-blue", CAT_COMPONENTS, {
        "_background": {"color": {"raw": "color-mix(in srgb, var(--wpfy-blue) 38%, var(--wpfy-paper))"}},
    }),
    ("wpfy-box-teal", CAT_COMPONENTS, {
        "_background": {"color": {"raw": "color-mix(in srgb, var(--wpfy-teal) 30%, var(--wpfy-paper))"}},
    }),
    ("wpfy-box-yellow", CAT_COMPONENTS, {
        "_background": {"color": {"raw": "color-mix(in srgb, var(--wpfy-yellow) 28%, var(--wpfy-paper))"}},
    }),
    ("wpfy-box-red", CAT_COMPONENTS, {
        "_background": {"color": {"raw": "color-mix(in srgb, var(--wpfy-red) 18%, var(--wpfy-paper))"}},
    }),
    ("wpfy-box-cream", CAT_COMPONENTS, {
        "_background": {"color": {"raw": "var(--wpfy-cream)"}},
    }),
    ("wpfy-eco-item", CAT_COMPONENTS, {
        "_display": "inline-flex",
        "_alignItems": "center",
        "_gap": "7px",
        "_typography": {
            "font-family": "IBM Plex Mono",
            "font-size": "0.7rem",
            "font-weight": "600",
            "text-transform": "uppercase",
            "letter-spacing": "0.02em",
        },
        "_background": {"color": {"raw": "var(--wpfy-paper)"}},
        "_border": INK_BORDER,
        "_padding": {"top": "6px", "right": "10px", "bottom": "6px", "left": "10px"},
        "_cssCustom": "%root% img, %root% svg { width: 18px; height: 18px; flex: none; }",
    }),
    ("wpfy-eco-center", CAT_COMPONENTS, {
        "_display": "flex",
        "_direction": "column",
        "_alignItems": "center",
        "_rowGap": "14px",
        "_typography": {"text-align": "center"},
        "_position": "relative",
        "_zIndex": "1",
        "_order:tablet_portrait": "-1",
    }),
    ("wpfy-eco-center-label", CAT_COMPONENTS, {
        "_typography": {**MONO_TYPO, "font-size": "0.72rem", "letter-spacing": "0.08em"},
        "_background": {"color": {"raw": "var(--wpfy-cream)"}},
        "_padding": {"top": "2px", "bottom": "2px", "left": "8px", "right": "8px"},
        "_position": "relative",
    }),
    ("wpfy-eco-center-sub", CAT_COMPONENTS, {
        "_typography": {**MONO_TYPO, "font-size": "0.72rem", "letter-spacing": "0.08em", "color": {"raw": "var(--wpfy-ink-soft)"}},
        "_background": {"color": {"raw": "var(--wpfy-cream)"}},
        "_padding": {"top": "2px", "bottom": "2px", "left": "8px", "right": "8px"},
        "_position": "relative",
    }),
    ("wpfy-eco-node", CAT_COMPONENTS, {
        "_position": "relative",
        "_widthMax": "200px",
        "_width": "100%",
        "_background": {"color": {"raw": "var(--wpfy-paper)"}},
        "_border": {**INK_BORDER, "radius": {"top": "14px", "right": "14px", "bottom": "14px", "left": "14px"}},
        "_boxShadow": {"values": {"offsetX": "5", "offsetY": "5", "blur": "0"}, "color": {"raw": "var(--wpfy-ink)"}},
        "_overflow": "hidden",
    }),
    ("wpfy-eco-node-bar", CAT_COMPONENTS, {
        "_display": "flex",
        "_columnGap": "7px",
        "_alignItems": "center",
        "_background": {"color": {"raw": "var(--wpfy-ink)"}},
        "_padding": {"top": "9px", "right": "12px", "bottom": "9px", "left": "12px"},
    }),
    ("wpfy-eco-node-body", CAT_COMPONENTS, {
        "_typography": {"font-family": "IBM Plex Mono", "font-weight": "700", "font-size": "1.3rem"},
        "_padding": {"top": "26px", "right": "16px", "bottom": "26px", "left": "16px"},
    }),
    ("wpfy-terminal", CAT_COMPONENTS, {
        "_position": "relative",
        "_widthMax": "860px",
        "_width": "100%",
        "_background": {"color": {"raw": "var(--wpfy-paper)"}},
        "_border": {**INK_BORDER, "radius": RADIUS_WIN},
        "_boxShadow": {"values": {"offsetX": "5", "offsetY": "5", "blur": "0"}, "color": {"raw": "var(--wpfy-ink)"}},
        "_overflow": "hidden",
        "_typography": {"text-align": "left"},
        "_zIndex": "1",
    }),
    ("wpfy-term-bar", CAT_COMPONENTS, {
        "_display": "flex",
        "_alignItems": "center",
        "_columnGap": "8px",
        "_background": {"color": {"raw": "var(--wpfy-ink)"}},
        "_typography": {"color": {"raw": "var(--wpfy-cream)"}},
        "_padding": {"top": "10px", "right": "14px", "bottom": "10px", "left": "14px"},
    }),
    ("wpfy-term-dot", CAT_COMPONENTS, {
        "_width": "11px",
        "_height": "11px",
        "_border": {"radius": {"top": "50%", "right": "50%", "bottom": "50%", "left": "50%"}, "width": {"top": "2px", "right": "2px", "bottom": "2px", "left": "2px"}, "style": "solid", "color": {"raw": "var(--wpfy-cream)"}},
        "_cssCustom": "%root%.d1 { background: var(--wpfy-red); } %root%.d2 { background: var(--wpfy-yellow); } %root%.d3 { background: var(--wpfy-teal); }",
    }),
    ("wpfy-term-title", CAT_COMPONENTS, {
        "_typography": {"font-family": "IBM Plex Mono", "font-size": "0.72rem", "letter-spacing": "0.04em"},
        "_margin": {"left": "8px"},
        "_opacity": "0.85",
    }),
    ("wpfy-copy-btn", CAT_COMPONENTS, {
        "_display": "inline-flex",
        "_alignItems": "center",
        "_gap": "6px",
        "_margin": {"left": "auto"},
        "_typography": {**MONO_TYPO, "font-size": "0.68rem"},
        "_background": {"color": {"raw": "var(--wpfy-cream)"}},
        "_border": {"width": {"top": "2px", "right": "2px", "bottom": "2px", "left": "2px"}, "style": "solid", "color": {"raw": "var(--wpfy-cream)"}, "radius": RADIUS_SM},
        "_padding": {"top": "4px", "right": "10px", "bottom": "4px", "left": "10px"},
        "_cssCustom": (
            "%root% { cursor: pointer; transition: background-color 0.15s, transform 0.15s; } "
            "%root%:hover { background: var(--wpfy-yellow); border-color: var(--wpfy-yellow); } "
            "%root%:active { transform: scale(0.96); } "
            "%root% svg { width: 12px; height: 12px; }"
        ),
    }),
    ("wpfy-term-body", CAT_COMPONENTS, {
        "_padding": {"top": "20px", "right": "24px", "bottom": "24px", "left": "24px"},
        "_typography": {"font-family": "IBM Plex Mono", "font-size": "0.82rem", "line-height": "1.9"},
        "_height": "calc(7 * 1.9em + 44px)",
        "_overflow": "hidden auto",
        "_cssCustom": "%root% { overflow-x: auto; overflow-y: hidden; white-space: pre; }",
    }),
    ("wpfy-bubble", CAT_COMPONENTS, {
        "_position": "absolute",
        "_top": "-44px",
        "_right": "18px",
        "_background": {"color": {"raw": "var(--wpfy-paper)"}},
        "_border": {**INK_BORDER, "radius": RADIUS_SM},
        "_typography": {**MONO_TYPO, "font-size": "0.68rem"},
        "_padding": {"top": "8px", "right": "12px", "bottom": "8px", "left": "12px"},
        "_boxShadow": {"values": {"offsetX": "3", "offsetY": "3", "blur": "0"}, "color": {"raw": "var(--wpfy-ink)"}},
        "_zIndex": "2",
        "_cssCustom": (
            "%root%::after { content: ''; position: absolute; bottom: -10px; left: 26px; "
            "width: 12px; height: 12px; background: var(--wpfy-paper); "
            "border-right: var(--wpfy-border); border-bottom: var(--wpfy-border); transform: rotate(45deg); }"
        ),
    }),
    ("wpfy-doodle", CAT_COMPONENTS, {
        "_position": "absolute",
        "_pointerEvents": "none",
        "_cssCustom": "%root% svg { width: 100%; height: auto; }",
    }),
    ("wpfy-edge-doodle", CAT_COMPONENTS, {
        "_position": "absolute",
        "_top": "-26px",
        "_zIndex": "2",
        "_pointerEvents": "none",
        "_cssCustom": "%root% svg, %root% img { width: 100%; height: auto; }",
    }),
    ("wpfy-edge-doodle-b", CAT_COMPONENTS, {
        "_top": "auto",
        "_bottom": "-26px",
    }),
    ("wpfy-drift", CAT_COMPONENTS, {
        "_position": "absolute",
        "_pointerEvents": "none",
        "_zIndex": "0",
        "_cssCustom": (
            "%root% { animation: wpfy-drift-y 14s ease-in-out infinite alternate; } "
            "%root% svg, %root% img { width: 100%; height: auto; } "
            "%root%.d-icon { opacity: 0.16; } "
            "%root%.d-cloud, %root%.d-lock { opacity: 0.85; } "
            "@keyframes wpfy-drift-y { from { transform: translateY(14px); } to { transform: translateY(-14px); } } "
            "@supports (animation-timeline: view()) { "
            "%root% { animation: wpfy-drift-scroll linear both; animation-timeline: view(); } "
            "@keyframes wpfy-drift-scroll { from { transform: translateY(70px); } to { transform: translateY(-70px); } } } "
            "@media (prefers-reduced-motion: reduce) { %root% { animation: none; } }"
        ),
    }),
    ("wpfy-cta-cloud", CAT_COMPONENTS, {
        "_position": "absolute",
        "_top": "-26px",
        "_zIndex": "2",
        "_pointerEvents": "none",
        "_cssCustom": "%root% svg { width: 100%; height: auto; }",
    }),
    ("wpfy-cmd-chip", CAT_COMPONENTS, {
        "_display": "inline-flex",
        "_alignItems": "center",
        "_gap": "8px",
        "_background": {"color": {"raw": "var(--wpfy-ink)"}},
        "_typography": {"font-family": "IBM Plex Mono", "font-size": "0.72rem", "color": {"raw": "var(--wpfy-cream)"}},
        "_border": {"radius": RADIUS_SM},
        "_padding": {"top": "5px", "right": "10px", "bottom": "5px", "left": "10px"},
        "_margin": {"top": "14px"},
        "_cssCustom": (
            "%root% { cursor: pointer; border: 0; transition: transform 0.15s, background-color 0.15s; } "
            "%root%:hover { background: #2b2b2b; } "
            "%root%:active { transform: scale(0.97); } "
            "%root%.copied { background: #2b2b2b; } "
            "%root% .wpfy-cmd-chip-ico { width: 12px; height: 12px; flex: none; opacity: 0.5; } "
            "%root%:hover .wpfy-cmd-chip-ico { opacity: 0.85; } "
            "%root%.copied .wpfy-cmd-chip-ico { opacity: 1; color: var(--wpfy-teal); } "
            "%root% .ico-check { display: none; } "
            "%root%.copied .ico-copy { display: none; } "
            "%root%.copied .ico-check { display: block; }"
        ),
    }),
    ("wpfy-nav-links", CAT_COMPONENTS, {
        "_display": "flex",
        "_alignItems": "center",
        "_columnGap": "24px",
        "_margin": {"right": "auto"},
        "_cssCustom": (
            "%root% { list-style: none; margin: 0; padding: 0; flex-wrap: wrap; } "
            "%root% li { list-style: none; } "
            "%root% a { font-family: IBM Plex Mono, monospace; font-size: 0.75rem; text-transform: uppercase; "
            "letter-spacing: 0.05em; padding: 6px 2px; border-bottom: 2px solid transparent; "
            "text-decoration: none; color: inherit; "
            "transition: border-color 0.15s cubic-bezier(0.23,1,0.32,1); } "
            "%root% a:hover { border-bottom-color: var(--wpfy-ink); } "
            "%root% a:active { background: var(--wpfy-yellow); }"
        ),
    }),
    ("wpfy-menu-btn", CAT_COMPONENTS, {
        "_display": "none",
        "_border": {**INK_BORDER, "radius": RADIUS_SM},
        "_background": {"color": {"raw": "var(--wpfy-paper)"}},
        "_padding": "9px",
        "_margin": {"left": "auto"},
        "_cssCustom": (
            "%root% svg { width: 16px; height: 16px; } "
            "@media (max-width:768px) { %root% { display: inline-flex; margin-left: auto; } }"
        ),
    }),
    ("wpfy-footer-col-title", CAT_COMPONENTS, {
        "_typography": {**MONO_TYPO, "font-size": "0.72rem", "font-weight": "600", "letter-spacing": "0.08em"},
        "_margin": {"bottom": "14px"},
        "_opacity": "0.9",
    }),
    ("wpfy-footer-links", CAT_COMPONENTS, {
        "_cssCustom": (
            "%root% { list-style: none; margin: 0; padding: 0; display: grid; gap: 10px; } "
            "%root% a { font-family: IBM Plex Mono, monospace; font-size: 0.78rem; text-transform: uppercase; "
            "letter-spacing: 0.05em; border-bottom: 2px solid transparent; text-decoration: none; color: inherit; } "
            "%root% a:hover { border-bottom-color: var(--wpfy-cream); }"
        ),
    }),
    ("wpfy-footer-meta", CAT_COMPONENTS, {
        "_typography": {**MONO_TYPO, "font-size": "0.72rem", "line-height": "2"},
        "_margin": {"top": "14px"},
        "_opacity": "0.75",
    }),
    ("wpfy-footer-bar", CAT_COMPONENTS, {
        "_border": {"width": {"top": "2px"}, "style": "solid", "color": {"raw": "rgba(244, 239, 234, 0.2)"}},
        "_padding": {"top": "16px", "bottom": "20px"},
        "_typography": {**MONO_TYPO, "font-size": "0.68rem", "line-height": "1.8", "text-align": "center"},
        "_opacity": "0.8",
        "_cssCustom": (
            "%root% a { color: inherit; text-decoration: none; border-bottom: 2px solid var(--wpfy-teal); text-underline-offset: 3px; } "
            "%root% a:hover { color: var(--wpfy-teal); border-bottom-color: var(--wpfy-yellow); }"
        ),
    }),
    ("wpfy-sub-copy", CAT_COMPONENTS, {
        "_widthMax": "460px",
        "_cssCustom": (
            "%root% { flex: 1 1 300px; max-width: 460px; } "
            "%root% h2 { font-family: IBM Plex Mono, monospace; font-size: clamp(1.4rem, 1rem + 1.6vw, 1.9rem); "
            "text-transform: uppercase; margin-bottom: 10px; } "
            "%root% p { max-width: 460px; margin: 0; }"
        ),
    }),
    ("wpfy-sub-form", CAT_COMPONENTS, {
        "_display": "flex",
        "_columnGap": "12px",
        "_flexWrap": "wrap",
        "_cssCustom": (
            "%root% { flex: 0 1 auto; min-width: min(100%, 390px); } "
            "%root% input[type=email] { font-family: IBM Plex Mono, monospace; font-size: 0.85rem; line-height: normal; "
            "color: var(--wpfy-ink); background: var(--wpfy-paper); border: var(--wpfy-border); "
            "border-radius: var(--wpfy-radius); box-shadow: var(--wpfy-shadow-sm); padding: 11px 16px; "
            "min-height: 44px; height: 44px; min-width: 260px; flex: 1 1 auto; } "
            "%root% input[type=email]::placeholder { color: var(--wpfy-ink-soft); } "
            "%root% input[type=email]:focus-visible { outline: 3px solid var(--wpfy-yellow); outline-offset: 2px; } "
            "%root% .wpfy-sub-fields { display: flex; gap: 12px; flex-wrap: wrap; align-items: stretch; width: 100%; } "
            "%root% .wpfy-btn { background: var(--wpfy-yellow); color: var(--wpfy-ink); flex: 0 0 auto; } "
            "%root% .wpfy-btn:hover { background: var(--wpfy-yellow); } "
            "%root% .wpfy-sub-privacy { font-size: 0.78rem; color: var(--wpfy-ink-soft); margin-top: 10px; "
            "max-width: 420px; flex: 1 1 100%; } "
            "%root% .wpfy-sub-privacy label { display: flex; align-items: flex-start; gap: 8px; cursor: pointer; } "
            "%root% .wpfy-sub-privacy input[type=checkbox] { width: 16px; height: 16px; min-width: 16px; min-height: 16px; "
            "margin-top: 2px; padding: 0; border: 2px solid var(--wpfy-ink); box-shadow: none; flex: none; "
            "accent-color: var(--wpfy-yellow); } "
            "@media (max-width:680px) { %root% { width: 100%; } "
            "%root% input[type=email] { min-width: 0; width: 100%; } %root% .wpfy-btn { flex: 1 1 auto; } }"
        ),
    }),
    ("wpfy-sub-status", CAT_COMPONENTS, {
        "_typography": {**MONO_TYPO, "font-size": "0.85rem", "font-weight": "600"},
        "_background": {"color": {"raw": "var(--wpfy-paper)"}},
        "_border": {**INK_BORDER, "radius": RADIUS_SM},
        "_boxShadow": {"values": {"offsetX": "3", "offsetY": "3", "blur": "0"}, "color": {"raw": "var(--wpfy-ink)"}},
        "_padding": {"top": "12px", "right": "18px", "bottom": "12px", "left": "18px"},
    }),
    ("wpfy-uc-copy", CAT_COMPONENTS, {
        "_rowGap": "16px",
        "_cssCustom": (
            "%root% h3 { font-family: IBM Plex Mono, monospace; font-size: 1.25rem; text-transform: uppercase; margin-bottom: 14px; } "
            "%root% p { color: var(--wpfy-ink-soft); max-width: 440px; margin-bottom: 24px; }"
        ),
    }),
    ("wpfy-affiliate-banner", CAT_COMPONENTS, {
        "_background": {"color": {"raw": "var(--wpfy-yellow)"}},
        "_border": INK_BORDER,
        "_padding": {"top": "14px", "right": "18px", "bottom": "14px", "left": "18px"},
        "_margin": {"bottom": "28px"},
        "_boxShadow": {"values": {"offsetX": "3", "offsetY": "3", "blur": "0"}, "color": {"raw": "var(--wpfy-ink)"}},
        "_typography": {"font-size": "0.92rem"},
        "_cssCustom": "%root% p { margin: 0; max-width: none; } %root% a { font-weight: 600; }",
    }),
    # ── Typography / utilities ──
    ("wpfy-lede", CAT_TYPO, {
        "_typography": {"font-size": "1.05rem", "color": {"raw": "var(--wpfy-ink-soft)"}, "line-height": "1.6", "text-align": "center"},
        "_widthMax": "640px",
        "_margin": {"left": "auto", "right": "auto"},
    }),
    ("wpfy-heading-mono", CAT_TYPO, {
        "_typography": {
            "font-family": "IBM Plex Mono",
            "font-weight": "500",
            "text-transform": "uppercase",
            "letter-spacing": "0.02em",
            "line-height": "1.15",
        },
        "_cssCustom": (
            "%root% { font-size: clamp(1.5rem, 1rem + 2.4vw, 2.4rem); } "
            ".wpfy-section-head %root% { margin-bottom: 14px; } "
            ".wpfy-eco-head %root% { font-size: clamp(1.9rem, 1rem + 3.4vw, 3rem); letter-spacing: 0.06em; }"
        ),
    }),
    ("wpfy-logo", CAT_TYPO, {
        "_typography": {
            "font-family": "IBM Plex Mono",
            "font-size": "1.25rem",
            "font-weight": "700",
            "letter-spacing": "-0.01em",
        },
        "_cssCustom": "%root% .mark, %root% span { color: var(--wpfy-teal-deep); } .wpfy-site-footer %root% .mark, .wpfy-site-footer %root% span { color: var(--wpfy-teal); }",
    }),
    ("wpfy-eco-sub", CAT_TYPO, {
        "_typography": {**MONO_TYPO, "font-size": "1rem", "letter-spacing": "0.14em", "text-align": "center"},
        "_margin": {"top": "6px"},
    }),
    ("wpfy-li-x", CAT_TYPO, {
        "_typography": {"font-family": "IBM Plex Mono", "font-weight": "700", "color": {"raw": "var(--wpfy-red)"}},
    }),
    ("wpfy-li-check", CAT_TYPO, {
        "_typography": {"font-family": "IBM Plex Mono", "font-weight": "700", "color": {"raw": "var(--wpfy-green)"}},
    }),
    ("wpfy-t-prompt", CAT_TYPO, {
        "_typography": {"color": {"raw": "var(--wpfy-teal-deep)"}, "font-weight": "600"},
        "_cssCustom": ".wpfy-code-well %root% { color: var(--wpfy-teal); }",
    }),
    ("wpfy-t-cmd", CAT_TYPO, {
        "_typography": {"color": {"raw": "var(--wpfy-ink)"}, "font-weight": "600"},
    }),
    ("wpfy-t-out", CAT_TYPO, {
        "_typography": {"color": {"raw": "var(--wpfy-ink-soft)"}},
        "_cssCustom": ".wpfy-code-well %root% { color: #a8a8a8; }",
    }),
    ("wpfy-t-ok", CAT_TYPO, {
        "_typography": {"color": {"raw": "var(--wpfy-green)"}, "font-weight": "600"},
    }),
    ("wpfy-t-dim", CAT_TYPO, {
        "_typography": {"color": {"raw": "var(--wpfy-teal-deep)"}},
    }),
    ("wpfy-sr-only", CAT_TYPO, {
        "_position": "absolute",
        "_width": "1px",
        "_height": "1px",
        "_overflow": "hidden",
        "_cssCustom": "%root% { clip: rect(0 0 0 0); white-space: nowrap; }",
    }),
    ("wpfy-reveal", CAT_TYPO, {
        "_cssCustom": (
            "%root% { opacity: 1; transform: none; } "
            ".js %root% { opacity: 0; transform: translateY(14px); "
            "transition: opacity 0.5s cubic-bezier(0.23,1,0.32,1), transform 0.5s cubic-bezier(0.23,1,0.32,1); "
            "transition-delay: calc(var(--d, 0) * 70ms); } "
            ".js %root%.in { opacity: 1; transform: translateY(0); } "
            "@media (prefers-reduced-motion: reduce) { .js %root% { opacity: 1; transform: none; } }"
        ),
    }),
]

# Tuple list consumed by migrate_to_bricks (name, category label, settings).
GLOBAL_CLASSES: list[tuple[str, str, dict]] = [
    (name, CATEGORY_NAMES[cat_id], settings)
    for name, cat_id, settings in GLOBAL_CLASS_DEFS
]


def _missing_ids() -> None:
    names = {name for name, _, _ in GLOBAL_CLASS_DEFS}
    missing = names - set(CLASS_IDS)
    if missing:
        raise ValueError(f"Missing CLASS_IDS for: {sorted(missing)}")


def build_classes_json() -> list[dict]:
    _missing_ids()
    out: list[dict] = []
    for name, cat_id, settings in GLOBAL_CLASS_DEFS:
        out.append({
            "id": CLASS_IDS[name],
            "name": name,
            "settings": settings,
            "category": cat_id,
            "_categoryData": {"id": cat_id, "name": CATEGORY_NAMES[cat_id]},
        })
    return out


def write_classes_json(path: Path | None = None) -> Path:
    target = path or Path(__file__).with_name("bricks-classes.json")
    target.write_text(json.dumps(build_classes_json(), indent=2) + "\n", encoding="utf-8")
    return target


def all_class_names() -> list[str]:
    return [name for name, _, _ in GLOBAL_CLASS_DEFS]


if __name__ == "__main__":
    out = write_classes_json()
    print(f"Wrote {len(GLOBAL_CLASS_DEFS)} classes → {out}")
