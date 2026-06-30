"""Native Bricks element tree helpers — prefer layout/content elements over html."""
from __future__ import annotations

from bricks_common import MONO_TYPO, el


def _anchor_id(li_id: str) -> str:
    return f"{li_id[:3]}a{li_id[-2:]}"


def _kid(base: str, suffix: str) -> str:
    """Derive a unique 6-char child id from a 6-char parent id."""
    return f"{base[:3]}{suffix}{base[-2:]}"


def reveal_attr(d: int) -> list[dict]:
    if d <= 0:
        return []
    return [{"id": f"rv{d:04d}", "name": "style", "value": f"--d:{d}"}]


def deco_html(eid: str, parent: str, html: str, label: str = "Decorations") -> dict:
    """Absolute-positioned ornaments — no Bricks equivalent."""
    return el(eid, "html", parent, [], {"html": html}, label)


def section_head(
    head_id: str,
    parent: str,
    title: str,
    *,
    title_tag: str = "h2",
    title_css_id: str | None = None,
    lede: str | None = None,
    subtitle: str | None = None,
    reveal: bool = True,
    head_classes: str = "",
) -> list[dict]:
    """Eyebrow-free section header: heading + optional subtitle + lede."""
    title_id = _kid(head_id, "t")
    kids: list[str] = [title_id]
    global_cls = ["wpfy-section-head"]
    if reveal:
        global_cls.append("wpfy-reveal")
    if head_classes:
        global_cls.extend(c for c in head_classes.split() if c)
    out: list[dict] = [
        el(
            head_id,
            "block",
            parent,
            kids,
            {
                "_cssGlobalClasses": global_cls,
                "_width": "100%",
                "_rowGap": "12px",
                "_margin": {"bottom": "48px"},
                "_typography": {"text-align": "center"},
            },
            "Section head",
        ),
    ]
    h_settings: dict = {
        "text": title,
        "tag": title_tag,
        "_cssGlobalClasses": ["wpfy-heading-mono"],
        "_typography": {"text-align": "center"},
    }
    if title_css_id:
        h_settings["_cssId"] = title_css_id
    out.append(el(title_id, "heading", head_id, [], h_settings, title))
    if subtitle:
        sid = _kid(head_id, "s")
        out[0]["children"].append(sid)
        out.append(el(sid, "text-basic", head_id, [], {
            "text": subtitle,
            "tag": "p",
            "_cssGlobalClasses": ["wpfy-eco-sub"],
        }))
    if lede:
        lid = _kid(head_id, "l")
        out[0]["children"].append(lid)
        out.append(el(lid, "text-basic", head_id, [], {
            "text": lede,
            "tag": "p",
            "_cssGlobalClasses": ["wpfy-lede"],
            "_typography": {"text-align": "center"},
            "_margin": {"top": "18px", "left": "auto", "right": "auto"},
        }))
    return out


def wpfy_tag(eid: str, parent: str, text: str, variant: str) -> dict:
    return el(eid, "text-basic", parent, [], {
        "text": text,
        "tag": "span",
        "_cssGlobalClasses": ["wpfy-tag", f"wpfy-tag-{variant}"],
    })


def anchor(eid: str, parent: str, text: str, url: str, *, new_tab: bool = False, classes: str = "") -> dict:
    settings: dict = {
        "text": text,
        "tag": "a",
        "link": {"type": "external", "url": url},
    }
    if new_tab:
        settings["link"]["newTab"] = True
    if classes:
        settings["_cssClasses"] = classes
    return el(eid, "text-basic", parent, [], settings)


def link_list(
    list_id: str,
    parent: str,
    links: list[tuple[str, str]],
    *,
    list_class: str = "wpfy-footer-links",
    new_tab: bool = False,
    item_ids: list[str] | None = None,
) -> list[dict]:
    """ul > li > a list using div semantic tags."""
    if item_ids is None:
        item_ids = [f"{list_id[:3]}{i:02d}" for i in range(len(links))]
    out: list[dict] = [
        el(list_id, "div", parent, item_ids, {
            "tag": "ul",
            "_cssClasses": list_class,
            "_display": "grid",
            "_rowGap": "10px",
        }, "Link list"),
    ]
    for i, (label, url) in enumerate(links):
        li_id = item_ids[i]
        a_id = _anchor_id(li_id)
        out.append(el(li_id, "div", list_id, [a_id], {"tag": "li"}))
        out.append(anchor(a_id, li_id, label, url, new_tab=new_tab))
    return out


def footer_col_title(eid: str, parent: str, text: str) -> dict:
    return el(eid, "text-basic", parent, [], {
        "text": text,
        "tag": "p",
        "_cssClasses": "wpfy-footer-col-title",
    })


def compare_row(
    row_id: str,
    parent: str,
    marker_class: str,
    marker: str,
    title: str,
    body: str,
) -> list[dict]:
    mark_id, body_id = _kid(row_id, "m"), _kid(row_id, "b")
    return [
        el(row_id, "div", parent, [mark_id, body_id], {
            "tag": "li",
            "_display": "flex",
            "_columnGap": "12px",
            "_alignItems": "flex-start",
        }),
        el(mark_id, "text-basic", row_id, [], {
            "text": marker,
            "tag": "span",
            "_cssClasses": marker_class,
        }),
        el(body_id, "text", row_id, [], {
            "text": f"<strong>{title}</strong>{body}",
        }),
    ]


def compare_card(
    card_id: str,
    parent: str,
    tag_text: str,
    tag_variant: str,
    rows: list[tuple[str, str, str, str]],
    *,
    reveal_d: int = 0,
) -> list[dict]:
    """Compare card with tag + list of x/check rows."""
    tag_wrap_id = _kid(card_id, "g")
    tag_id = _kid(card_id, "t")
    list_id = _kid(card_id, "l")
    row_ids = [f"r{card_id[-4:]}{i}" for i in range(len(rows))]
    attrs = reveal_attr(reveal_d)
    card_settings: dict = {
        "_cssGlobalClasses": ["wpfy-compare-card"],
        "_cssClasses": "wpfy-reveal",
    }
    if attrs:
        card_settings["_attributes"] = attrs
    out: list[dict] = [
        el(card_id, "block", parent, [tag_wrap_id, list_id], card_settings, tag_text),
        el(tag_wrap_id, "block", card_id, [tag_id], {"_margin": {"bottom": "20px"}}),
        wpfy_tag(tag_id, tag_wrap_id, tag_text, tag_variant),
        el(list_id, "div", card_id, row_ids, {
            "tag": "ul",
            "_display": "grid",
            "_rowGap": "14px",
        }),
    ]
    for i, (mcls, mark, title, body) in enumerate(rows):
        out.extend(compare_row(row_ids[i], list_id, mcls, mark, title, body))
    return out


def feature_card(
    card_id: str,
    parent: str,
    tag: str,
    tag_variant: str,
    title: str,
    body: str,
    cmd: str,
    *,
    reveal_d: int = 0,
) -> list[dict]:
    top_id = _kid(card_id, "a")
    tag_id = _kid(card_id, "b")
    h_id = _kid(card_id, "c")
    p_id = _kid(card_id, "d")
    btn_id = _kid(card_id, "e")
    attrs = reveal_attr(reveal_d)
    settings: dict = {
        "tag": "article",
        "_cssGlobalClasses": ["wpfy-card"],
        "_cssClasses": "wpfy-reveal",
        "_rowGap": "12px",
    }
    if attrs:
        settings["_attributes"] = attrs
    return [
        el(card_id, "block", parent, [top_id, h_id, p_id, btn_id], settings, title),
        el(top_id, "block", card_id, [tag_id], {"_cssClasses": "wpfy-card-top"}),
        wpfy_tag(tag_id, top_id, tag, tag_variant),
        el(h_id, "heading", card_id, [], {"text": title, "tag": "h3"}),
        el(p_id, "text-basic", card_id, [], {"text": body, "tag": "p"}),
        el(btn_id, "button", card_id, [], {
            "text": cmd,
            "tag": "button",
            "_cssClasses": "wpfy-cmd-chip",
            "_attributes": [{"id": f"cp{btn_id[-4:]}", "name": "data-copy", "value": cmd}],
        }),
    ]


def code_well(well_id: str, parent: str, code: str, *, extra_class: str = "") -> dict:
    classes = extra_class.strip()
    return el(well_id, "text-basic", parent, [], {
        "text": code,
        "tag": "pre",
        "_cssGlobalClasses": ["wpfy-code-well"],
        "_cssClasses": classes,
    })


def nav_ul(nav_id: str, parent: str, links: list[tuple[str, str]], *, css_id: str = "wpfy-nav-links") -> list[dict]:
    """Header nav: ul#wpfy-nav-links with anchor hash + external links."""
    li_ids = [f"hdnv{i:02d}" for i in range(1, len(links) + 1)]
    out: list[dict] = [
        el(nav_id, "div", parent, li_ids, {
            "tag": "ul",
            "_cssId": css_id,
            "_cssGlobalClasses": ["wpfy-nav-links"],
        }, "Nav links"),
    ]
    for i, (label, url) in enumerate(links):
        li_id = li_ids[i]
        a_id = _anchor_id(li_id)
        out.append(el(li_id, "div", nav_id, [a_id], {"tag": "li"}))
        out.append(anchor(a_id, li_id, label, url, new_tab=url.startswith("http")))
    return out


def eco_item(item_id: str, parent: str, label: str, icon_url: str | None = None) -> list[dict]:
    kids: list[str] = []
    out: list[dict] = [
        el(item_id, "div", parent, kids, {
            "_cssClasses": "wpfy-eco-item",
            "_display": "inline-flex",
            "_alignItems": "center",
            "_columnGap": "7px",
        }),
    ]
    if icon_url:
        img_id = _kid(item_id, "i")
        kids.append(img_id)
        out.append(el(img_id, "image", item_id, [], {
            "image": {"url": icon_url, "external": True},
            "altText": "",
            "loading": "lazy",
            "_width": "18px",
            "_height": "18px",
        }))
    text_id = _kid(item_id, "t")
    kids.append(text_id)
    out.append(el(text_id, "text-basic", item_id, [], {
        "text": label,
        "tag": "span",
        "_typography": {**MONO_TYPO, "font-size": "0.7rem", "font-weight": "600"},
    }))
    return out


def eco_box(
    box_id: str,
    parent: str,
    title: str,
    box_class: str,
    items: list[tuple[str | None, str]],
    *,
    item_ids: list[str] | None = None,
) -> list[dict]:
    """Eco diagram box: heading + chip row."""
    heading_id = _kid(box_id, "h")
    items_wrap_id = _kid(box_id, "w")
    if item_ids is None:
        item_ids = [f"ei{box_id[-4:]}{chr(ord('a') + n)}" for n in range(len(items))]
    out: list[dict] = [
        el(box_id, "block", parent, [heading_id, items_wrap_id], {
            "_cssClasses": f"wpfy-eco-box {box_class}",
        }, title),
        el(heading_id, "heading", box_id, [], {"text": title, "tag": "h3"}),
        el(items_wrap_id, "block", box_id, item_ids, {
            "_cssClasses": "wpfy-eco-items",
            "_display": "flex",
            "_flexWrap": "wrap",
            "_justifyContent": "center",
            "_columnGap": "10px",
            "_rowGap": "8px",
        }),
    ]
    for n, (icon_key, label) in enumerate(items):
        from icon_paths import icon as icon_url

        url = icon_url(icon_key) if icon_key else None
        out.extend(eco_item(item_ids[n], items_wrap_id, label, url))
    return out
