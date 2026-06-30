"""Canonical WPFY Bricks CSS variable definitions — single source for bricks-variables.json."""
from __future__ import annotations

import json
from pathlib import Path

CAT_WPFY = "cat-wpfy01"

# Order matters: base colors before tokens that reference var(--wpfy-ink).
VARIABLE_DEFS: list[tuple[str, str]] = [
    ("wpfy-cream", "#f4efea"),
    ("wpfy-paper", "#ffffff"),
    ("wpfy-ink", "#383838"),
    ("wpfy-ink-soft", "#5c5c5c"),
    ("wpfy-blue", "#97d4ff"),
    ("wpfy-blue-deep", "#6fc2ff"),
    ("wpfy-yellow", "#ffde00"),
    ("wpfy-teal", "#53dbc9"),
    ("wpfy-teal-deep", "#16aa98"),
    ("wpfy-red", "#f2655a"),
    ("wpfy-green", "#1fa04c"),
    ("wpfy-container-max", "1200px"),
    ("wpfy-section-pad", "96px"),
    ("wpfy-section-pad-mobile", "72px"),
    ("wpfy-shadow", "5px 5px 0 var(--wpfy-ink)"),
    ("wpfy-shadow-sm", "3px 3px 0 var(--wpfy-ink)"),
    ("wpfy-radius", "2px"),
    ("wpfy-radius-win", "6px"),
    ("wpfy-border", "2px solid var(--wpfy-ink)"),
    ("wpfy-ease-out", "cubic-bezier(0.23, 1, 0.32, 1)"),
    ("wpfy-t-fast", "0.15s"),
    ("wpfy-t-reveal", "0.5s"),
]

# Stable ids for re-import / merge on staging (name is what becomes --wpfy-* in CSS).
VARIABLE_IDS: dict[str, str] = {
    "wpfy-cream": "var-xa9jmk",
    "wpfy-paper": "var-stw7dd",
    "wpfy-ink": "var-onzvzh",
    "wpfy-ink-soft": "var-69j7t4",
    "wpfy-blue": "var-4bvdda",
    "wpfy-blue-deep": "var-p5zsef",
    "wpfy-yellow": "var-zwlfhr",
    "wpfy-teal": "var-t0up31",
    "wpfy-teal-deep": "var-hjpwsx",
    "wpfy-red": "var-o8oo51",
    "wpfy-green": "var-s2em1w",
    "wpfy-container-max": "var-zzwol6",
    "wpfy-section-pad": "var-w44ir6",
    "wpfy-section-pad-mobile": "var-oe5ypq",
    "wpfy-shadow": "var-ueajlw",
    "wpfy-shadow-sm": "var-jwq3x9",
    "wpfy-radius": "var-ti4us0",
    "wpfy-radius-win": "var-ncsko8",
    "wpfy-border": "var-g7irhu",
    "wpfy-ease-out": "var-ease01",
    "wpfy-t-fast": "var-tfst1",
    "wpfy-t-reveal": "var-trev1",
}

# (name, value, category label) — consumed by migrate_to_bricks.py
VARIABLES: list[tuple[str, str, str]] = [(name, value, "WPFY") for name, value in VARIABLE_DEFS]


def build_variables_json() -> dict:
    return {
        "variables": [
            {
                "id": VARIABLE_IDS[name],
                "name": name,
                "value": value,
                "category": CAT_WPFY,
            }
            for name, value in VARIABLE_DEFS
        ],
        "categories": [
            {
                "id": CAT_WPFY,
                "name": "WPFY",
            }
        ],
    }


def write_variables_json(path: Path | None = None) -> Path:
    target = path or Path(__file__).with_name("bricks-variables.json")
    target.write_text(json.dumps(build_variables_json(), indent=2) + "\n", encoding="utf-8")
    return target


if __name__ == "__main__":
    out = write_variables_json()
    print(f"Wrote {len(VARIABLE_DEFS)} WPFY variables → {out}")
