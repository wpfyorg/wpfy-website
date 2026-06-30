"""Self-hosted Simple Icons — local SVG paths for WP theme and static site."""
from __future__ import annotations

WP_ICON_BASE = "/wp-content/themes/bricks-child/assets/icons"
STATIC_ICON_BASE = "assets/icons"

ICONS = (
    "docker",
    "traefikproxy",
    "letsencrypt",
    "wordpress",
    "nginx",
    "php",
    "mariadb",
    "redis",
    "ubuntu",
)


def icon(slug: str, *, static: bool = False) -> str:
    """Return URL path to a self-hosted icon SVG."""
    if slug not in ICONS:
        raise ValueError(f"Unknown icon slug: {slug!r}")
    base = STATIC_ICON_BASE if static else WP_ICON_BASE
    return f"{base}/{slug}.svg"
