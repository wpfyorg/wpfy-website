"""Batch 2 page sections — extracted from index.html for static/Bricks parity."""
from __future__ import annotations

import re
from pathlib import Path

from bricks_common import el

ROOT = Path(__file__).resolve().parent
_INDEX_HTML = (ROOT / "index.html").read_text(encoding="utf-8")

# Sections after hero, in page order.
SECTION_IDS = [
    "tech",
    "why-docker",
    "architecture",
    "commands",
    "capabilities",
    "quick-start",
    "users",
    "boundaries",
    "cta",
    "updates",
]

_ELEMENT_IDS = [
    "sc0001",
    "sc0002",
    "sc0003",
    "sc0004",
    "sc0005",
    "sc0006",
    "sc0007",
    "sc0008",
    "sc0009",
    "sc0010",
]


def extract_section(section_id: str) -> str:
    pattern = rf'(<section[^>]*\bid="{re.escape(section_id)}"[^>]*>.*?</section>)'
    match = re.search(pattern, _INDEX_HTML, re.DOTALL | re.IGNORECASE)
    if not match:
        raise ValueError(f"Section #{section_id} not found in index.html")
    return match.group(1)


def extract_hero_section() -> str:
    pattern = r'(<section class="hero[^"]*"[^>]*>.*?</section>)'
    match = re.search(pattern, _INDEX_HTML, re.DOTALL | re.IGNORECASE)
    if not match:
        raise ValueError("Hero section not found in index.html")
    return match.group(1)


def html_block(eid: str, html: str, label: str) -> dict:
    return el(eid, "html", 0, [], {"html": html}, label)


def build_batch2_sections() -> list[dict]:
    out: list[dict] = []
    for eid, sid in zip(_ELEMENT_IDS, SECTION_IDS):
        out.append(html_block(eid, extract_section(sid), sid))
    return out
