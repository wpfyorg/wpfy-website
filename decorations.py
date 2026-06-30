"""Decorative doodles, edge ornaments, and drift elements (from static site)."""

from icon_paths import icon

CLOUD_SVG = (
    '<svg viewBox="0 0 150 70" fill="#fff" stroke="#383838" stroke-width="2.5">'
    '<path d="M28 58c-12 0-22-7-22-17 0-9 8-15 16-15 2-9 11-16 22-16 10 0 18 5 21 13 2-1 5-2 8-2 10 0 18 7 18 16 0 11-10 21-24 21H28Z"/>'
    "</svg>"
)
CLOUD_SVG_LG = (
    '<svg viewBox="0 0 170 80" fill="#fff" stroke="#383838" stroke-width="2.5">'
    '<path d="M34 66c-14 0-26-8-26-19 0-10 9-17 18-17 3-11 13-19 26-19 11 0 21 6 24 15 3-2 6-3 10-3 11 0 20 8 20 18 0 13-11 25-27 25H34Z"/>'
    "</svg>"
)
LOCK_SVG = (
    '<svg viewBox="0 0 24 24" fill="#ffde00" stroke="#383838" stroke-width="2">'
    '<rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3" fill="none"/>'
    "</svg>"
)
SPARK_STAR = (
    '<svg viewBox="0 0 24 24" fill="#53dbc9" stroke="#383838" stroke-width="2">'
    '<path d="M12 2l2.6 7.4L22 12l-7.4 2.6L12 22l-2.6-7.4L2 12l7.4-2.6L12 2Z"/>'
    "</svg>"
)
SPARK_DIAMOND = (
    '<svg viewBox="0 0 20 20" fill="#f2655a" stroke="#383838" stroke-width="2">'
    '<rect x="4" y="4" width="12" height="12" transform="rotate(45 10 10)"/>'
    "</svg>"
)
WHO_BUILDING = (
    '<svg viewBox="0 0 24 24" fill="#ffde00" stroke="#383838" stroke-width="2" stroke-linejoin="round">'
    '<rect x="3" y="8" width="8" height="13"/><rect x="11" y="3" width="10" height="18"/>'
    '<path d="M14 8h4M14 12.5h4M14 17h4" fill="none" stroke-width="1.5" stroke-linecap="round"/>'
    "</svg>"
)
WHO_PERSON = (
    '<svg viewBox="0 0 24 24" fill="#53dbc9" stroke="#383838" stroke-width="2" stroke-linejoin="round">'
    '<circle cx="12" cy="8" r="4"/><path d="M5 20a7 7 0 0 1 14 0Z"/>'
    "</svg>"
)
WHO_SERVER = (
    '<svg viewBox="0 0 24 24" fill="#97d4ff" stroke="#383838" stroke-width="2" stroke-linejoin="round">'
    '<rect x="3" y="4" width="18" height="7" rx="1.5"/><rect x="3" y="13" width="18" height="7" rx="1.5"/>'
    '<path d="M7 7.5h.01M7 16.5h.01" fill="none" stroke-width="2.6" stroke-linecap="round"/>'
    "</svg>"
)


def edge_cloud(left: str | None = None, right: str | None = None, width: str = "130px") -> str:
    parts = []
    if left:
        parts.append(
            f'<span class="wpfy-edge-doodle" style="left:{left};width:{width}" aria-hidden="true">{CLOUD_SVG}</span>'
        )
    if right:
        parts.append(
            f'<span class="wpfy-edge-doodle" style="right:{right};width:{width}" aria-hidden="true">{CLOUD_SVG_LG if width > "140" else CLOUD_SVG}</span>'
        )
    return "".join(parts)


def edge_icon(href: str, *, left: str | None = None, right: str | None = None, width: str = "44px", bottom: bool = False) -> str:
    cls = "wpfy-edge-doodle wpfy-edge-icon"
    if bottom:
        cls += " wpfy-edge-doodle-b"
    style = f"left:{left};" if left else f"right:{right};"
    style += f"width:{width}"
    return (
        f'<span class="{cls}" style="{style}" aria-hidden="true">'
        f'<img src="{href}" alt="" width="{width.replace("px","")}" height="{width.replace("px","")}" loading="lazy">'
        f"</span>"
    )


def edge_svg(svg: str, *, left: str | None = None, right: str | None = None, width: str = "44px", bottom: bool = False) -> str:
    cls = "wpfy-edge-doodle wpfy-edge-icon"
    if bottom:
        cls += " wpfy-edge-doodle-b"
    style = f"left:{left};" if left else f"right:{right};"
    style += f"width:{width}"
    return f'<span class="{cls}" style="{style}" aria-hidden="true">{svg}</span>'


def drift_icon(href: str, *, top: str | None = None, bottom: str | None = None,
               left: str | None = None, right: str | None = None, width: str = "56px") -> str:
    style = f"width:{width};"
    if top:
        style += f"top:{top};"
    if bottom:
        style += f"bottom:{bottom};"
    if left:
        style += f"left:{left};"
    if right:
        style += f"right:{right};"
    return (
        f'<span class="wpfy-drift d-icon" style="{style}" aria-hidden="true">'
        f'<img src="{href}" alt="" width="{width.replace("px","")}" height="{width.replace("px","")}" loading="lazy">'
        f"</span>"
    )


def drift_cloud(*, top: str | None = None, bottom: str | None = None,
                left: str | None = None, right: str | None = None, width: str = "120px", large: bool = False) -> str:
    style = f"width:{width};"
    if top:
        style += f"top:{top};"
    if bottom:
        style += f"bottom:{bottom};"
    if left:
        style += f"left:{left};"
    if right:
        style += f"right:{right};"
    svg = CLOUD_SVG_LG if large else CLOUD_SVG
    return f'<span class="wpfy-drift d-cloud" style="{style}" aria-hidden="true">{svg}</span>'


def drift_lock(*, bottom: str, right: str, width: str = "44px") -> str:
    return (
        f'<span class="wpfy-drift d-lock" style="bottom:{bottom};right:{right};width:{width}" aria-hidden="true">'
        f"{LOCK_SVG}</span>"
    )


HERO_DOODLES = f"""
<span class="wpfy-doodle wpfy-doodle-cloud-l" aria-hidden="true">{CLOUD_SVG}</span>
<span class="wpfy-doodle wpfy-doodle-cloud-r" aria-hidden="true">{CLOUD_SVG_LG}</span>
<span class="wpfy-doodle wpfy-doodle-spark-1" aria-hidden="true">{SPARK_STAR}</span>
<span class="wpfy-doodle wpfy-doodle-spark-2" aria-hidden="true">{SPARK_DIAMOND}</span>
<span class="wpfy-bubble" aria-hidden="true">Fresh VPS to WordPress in minutes!</span>
"""

PROBLEM_DECO = (
    edge_cloud(left="7%", width="130px")
    + edge_svg(LOCK_SVG, right="9%", width="44px")
    + drift_icon(icon("docker"), top="12%", right="4%", width="64px")
    + drift_cloud(bottom="10%", left="2%", width="110px")
)

FEATURES_DECO = (
    f'<span class="wpfy-edge-doodle" style="right:6%;width:150px" aria-hidden="true">{CLOUD_SVG_LG}</span>'
    + edge_icon(icon("docker"), left="8%", width="46px")
    + drift_icon(icon("wordpress"), top="6%", left="3%", width="56px")
    + drift_lock(bottom="8%", right="3%")
    + f'<span class="wpfy-edge-doodle wpfy-edge-doodle-b" style="left:8%;width:140px" aria-hidden="true">{CLOUD_SVG}</span>'
    + edge_icon(icon("nginx"), right="14%", width="44px", bottom=True)
)

WHO_DECO_TOP = (
    edge_cloud(left="6%", width="140px")
    + edge_icon(icon("wordpress"), right="7%", width="44px")
    + drift_cloud(top="8%", left="3%", width="120px")
    + drift_cloud(bottom="6%", right="5%", width="150px", large=True)
)

WHO_DECO_BOTTOM = (
    edge_svg(WHO_SERVER, left="9%", width="44px", bottom=True)
    + f'<span class="wpfy-edge-doodle wpfy-edge-doodle-b" style="right:7%;width:150px" aria-hidden="true">{CLOUD_SVG_LG}</span>'
)

USE_CASES_DECO = (
    drift_icon(icon("letsencrypt"), top="10%", right="4%", width="54px")
    + drift_icon(icon("docker"), bottom="12%", left="3%", width="60px")
)

CTA_DECO = (
    f'<span class="wpfy-cta-cloud" style="left:6%;width:130px" aria-hidden="true">{CLOUD_SVG}</span>'
    + f'<span class="wpfy-cta-cloud" style="right:7%;width:160px" aria-hidden="true">{CLOUD_SVG_LG}</span>'
)

SUBSCRIBE_DECO = (
    edge_cloud(left="5%", width="120px")
    + edge_icon(icon("letsencrypt"), right="7%", width="44px")
)

WHO_CARDS_DOODLES = (
    f'<span class="wpfy-who-doodle" aria-hidden="true">{WHO_BUILDING}</span>',
    f'<span class="wpfy-who-doodle" aria-hidden="true">{WHO_PERSON}</span>',
    f'<span class="wpfy-who-doodle" aria-hidden="true">{WHO_SERVER}</span>',
)
