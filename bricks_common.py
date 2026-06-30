"""Shared Bricks migration primitives (no circular imports)."""
from __future__ import annotations


MONO_TYPO = {
    "font-family": "IBM Plex Mono",
    "text-transform": "uppercase",
    "letter-spacing": "0.04em",
}

MARQUEE_KEYWORDS = [
    "WORDPRESS",
    "DOCKER-FIRST",
    "UBUNTU VPS",
    "DOCKER COMPOSE",
    "PER-SITE STACKS",
    "SITE ISOLATION",
    "WP-CLI",
    "TRAEFIK",
    "LET'S ENCRYPT",
    "SSL AUTOMATION",
    "NGINX",
    "PHP-FPM",
    "MARIADB",
    "REDIS CACHE",
    "SFTP ACCESS",
    "BACKUPS",
    "RESTORE",
    "SERVER HEALTH",
    "LOGS",
    "DIAGNOSTICS",
    "MULTI-SITE VPS",
    "PRODUCTION STACKS",
    "SECURE ACCESS",
    "STACK AUTOMATION",
    "CLI WORKFLOWS",
    "CONTAINERIZED HOSTING",
    "DEVOPS FOR WORDPRESS",
]


def marquee_track_html(*, css_class: str = "wpfy-marquee-track") -> str:
    """Two identical span sequences for seamless -50% CSS loop."""
    parts: list[str] = []
    for kw in MARQUEE_KEYWORDS:
        parts.append(f"<span>{kw}</span><span>+</span>")
    seq = "".join(parts)
    return f'<div class="{css_class}">{seq}{seq}</div>'


def el(
    eid: str,
    name: str,
    parent: str | int,
    children: list[str],
    settings: dict | None = None,
    label: str | None = None,
) -> dict:
    node = {"id": eid, "name": name, "parent": parent, "children": children, "settings": settings or {}}
    if label:
        node["label"] = label
    return node
