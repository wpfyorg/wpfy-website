"""Batch 2 page sections — native Bricks elements; html only for decorations + subscribe form."""
from __future__ import annotations

from bricks_builders import (
    code_well,
    compare_card,
    deco_html,
    eco_box,
    feature_card,
    reveal_attr,
    section_head,
    wpfy_tag,
    _kid,
)
from decorations import (
    CTA_DECO,
    FEATURES_DECO,
    PROBLEM_DECO,
    SUBSCRIBE_DECO,
    USE_CASES_DECO,
    WHO_CARDS_DOODLES,
    WHO_DECO_BOTTOM,
    WHO_DECO_TOP,
)
from icon_paths import icon
from bricks_common import el

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

OLD_WAY_ROWS = [
    ("wpfy-li-x", "x", "Shared host packages", "One PHP upgrade or package conflict can affect every site on the server."),
    ("wpfy-li-x", "x", "Multi-site sprawl", "Sites share processes, users, and config; cleanly removing one site is harder than it should be."),
    ("wpfy-li-x", "x", "Ad-hoc workflows", "SSL, backups, restore, diagnostics, and SFTP end up as one-off scripts and tribal knowledge."),
    ("wpfy-li-x", "x", "Hand-built stacks", "Compose files, proxies, and certificates assembled by hand for every site."),
]

WPFY_WAY_ROWS = [
    ("wpfy-li-check", "✓", "Docker-first", "No host-level Nginx, PHP, MariaDB, or Redis. The host stays clean."),
    ("wpfy-li-check", "✓", "Per-site isolation", "Sites never share PHP, database, cache, writable volumes, or networks."),
    ("wpfy-li-check", "✓", "CLI-driven workflows", "Create, SSL, backup, restore, diagnostics, and SFTP are retry-safe commands."),
    ("wpfy-li-check", "✓", "Safer SSL", "Certificates issue only after a DNS/IP preflight confirms the domain points at your server."),
]

FEATURES = [
    ("Installer", "yellow", "Ubuntu installer", "One scripted install on a fresh VPS: Docker Engine, the wpfy CLI, and the shared runtime, with staged steps and dry-run support.", "install.sh"),
    ("Isolation", "teal", "Per-site Compose stacks", "Every site is its own Docker Compose project with a private network, volumes, and database. Nothing is shared.", "wpfy site create"),
    ("Routing", "blue", "Traefik edge proxy", "A single shared Traefik instance routes traffic to each site's containers, with no broad write access to site data.", "wpfy stack install"),
    ("SSL", "yellow", "SSL DNS/IP preflight", "Let's Encrypt issuance is opt-in and gated: wpfy verifies DNS resolution and public IP match before requesting a certificate.", "wpfy site ssl"),
    ("WordPress", "blue", "WordPress provisioning", "Full WordPress setup per site, with wp-cli available inside each site's container for plugin, theme, and content work.", "wpfy site wp"),
    ("Safety", "teal", "Backup & restore", "Create per-site backup archives and restore them with a command. Backups are kept private, never world-readable.", "wpfy site backup"),
    ("Health", "yellow", "Diagnostics", "Structured checks across Docker, Traefik, and every managed site, plus per-site status, info, and log inspection.", "wpfy debug"),
    ("Access", "blue", "SFTP lifecycle", "Enable, inspect, and manage per-site SFTP access so each site gets its own scoped file transfer entry point.", "wpfy sftp"),
]

STEPS = [
    ("1", "Install WPFY", "Run the installer on a fresh Ubuntu VPS. It sets up Docker and the wpfy CLI, then verify with:", "$ wpfy --help"),
    ("2", "Create a site", "Provision an isolated WordPress stack (Compose project, network, database, and volumes) in one command:", "$ wpfy site create example.com --wp\n# add -le for SSL with DNS/IP preflight"),
    ("3", "Manage from the CLI", "SSL, backups, restore, diagnostics, and SFTP are all first-class commands:", "$ wpfy site status example.com\n$ wpfy site backup example.com\n$ wpfy debug"),
]

WHO_CARDS = [
    ("yellow", "Agencies & studios", "Run every client on one VPS. One site's plugin meltdown never touches the others.", 0),
    ("teal", "Freelance developers", "Provision a client site in minutes, hand over scoped SFTP, and keep root to yourself.", 1),
    ("blue", "Self-hosters", "Leave managed-WordPress pricing behind without giving up sane, retry-safe workflows.", 2),
]

USE_CASES = [
    (
        False,
        "Host a fleet of client sites",
        "Each site is its own Compose stack with a private network, database, and volumes. Hand every client scoped SFTP access and keep the server yours.",
        "#how-it-works",
        "How it works",
        "$ wpfy site create client-a.com --wp -le\n$ wpfy site create client-b.com --wp --php 8.3\n$ wpfy sftp --enable client-a.com",
    ),
    (
        True,
        "Migrate and recover without fear",
        "Archive any site to a private backup and bring it back with one command. SSL only issues after DNS provably points at your server.",
        "https://github.com/wpfyorg/wpfy/blob/main/docs/SECURITY.md",
        "Security model",
        "$ wpfy site backup example.com\n$ wpfy site restore example.com example-backup.tar.gz\n$ wpfy site ssl example.com",
    ),
]


def _section_shell(
    sid: str,
    inner_id: str,
    inner_children: list[str],
    *,
    css_id: str | None = None,
    global_classes: list[str] | None = None,
    extra_classes: str = "",
    deco_id: str | None = None,
    deco_html_str: str = "",
    label: str = "",
) -> list[dict]:
    section_kids = []
    if deco_id and deco_html_str:
        section_kids.append(deco_id)
    section_kids.append(inner_id)
    settings: dict = {"tag": "section", "_position": "relative", "_overflow": "visible"}
    if css_id:
        settings["_cssId"] = css_id
    if extra_classes:
        settings["_cssClasses"] = extra_classes
    if global_classes:
        settings["_cssGlobalClasses"] = global_classes
    out = [el(sid, "section", 0, section_kids, settings, label or css_id or sid)]
    if deco_id and deco_html_str:
        out.append(deco_html(deco_id, sid, deco_html_str))
    out.append(el(inner_id, "container", sid, inner_children, {"_cssGlobalClasses": ["wpfy-wrap"]}, "Inner"))
    return out


def build_problem_section() -> list[dict]:
    sid, wrap, head, grid = "pb0001", "pb0002", "pb0003", "pb0004"
    c1, c2 = "pb0005", "pb0006"
    out = _section_shell(
        sid, wrap, [head, grid],
        css_id="problem",
        global_classes=["wpfy-section-sky", "wpfy-section-pad"],
        deco_id="pbdeco",
        deco_html_str=PROBLEM_DECO,
        label="Problem vs solution",
    )
    out += section_head(
        head, wrap,
        "Host-level WordPress stacks get messy fast",
        title_css_id="problem-title",
        lede="Traditional server tooling installs Nginx, PHP, MariaDB, and Redis directly on the host. That works, until it doesn't. WPFY replaces all of it with one isolated Docker Compose stack per site.",
    )
    out.append(el(grid, "block", wrap, [c1, c2], {
        "_cssClasses": "wpfy-compare",
        "_display": "grid",
        "_gridTemplateColumns": "1fr 1fr",
        "_gridGap": "32px",
        "_margin": {"top": "48px"},
        "_gridTemplateColumns:mobile_landscape": "1fr",
    }))
    out += compare_card(c1, grid, "The old way", "red", OLD_WAY_ROWS, reveal_d=1)
    out += compare_card(c2, grid, "The WPFY way", "teal", WPFY_WAY_ROWS, reveal_d=2)
    return out


def build_eco_section() -> list[dict]:
    sid = "ec0001"
    sky, wrap, head, diagram = "ecsky1", "ec0002", "ec0003", "ec0004"
    pipes_id = "ecpipe"
    col_l, col_c, col_r = "eclcol", "eccctr", "ecrcol"
    out = [
        el(sid, "section", 0, [sky, wrap], {
            "tag": "section",
            "_cssId": "stack",
            "_cssClasses": "wpfy-eco-section",
            "_position": "relative",
        }, "Ecosystem"),
        el(sky, "block", sid, ["ecsk1", "ecsk2"], {
            "_cssClasses": "wpfy-eco-sky",
            "_attributes": [{"id": "ecskat", "name": "aria-hidden", "value": "true"}],
        }, "Sky"),
        el("ecsk1", "html", sky, [], {
            "html": f'<span class="wpfy-eco-sky-cloud c1">{CLOUD_SVG}</span>',
        }),
        el("ecsk2", "html", sky, [], {
            "html": f'<span class="wpfy-eco-sky-cloud c2">{CLOUD_SVG_LG}</span>',
        }),
        el(wrap, "container", sid, [head, diagram], {"_cssGlobalClasses": ["wpfy-wrap"]}),
    ]
    out += section_head(
        head, wrap, "Ecosystem",
        title_css_id="eco-title",
        subtitle="Modern WordPress stack",
        lede="Traefik is the only shared component; every site runs its own isolated services, all orchestrated from a single CLI.",
        head_classes="wpfy-eco-head",
    )
    out.append(el(diagram, "block", wrap, [pipes_id, col_l, col_c, col_r], {
        "_cssClasses": "wpfy-eco-diagram wpfy-reveal",
        "_attributes": reveal_attr(1),
        "_display": "grid",
        "_gridTemplateColumns": "minmax(0, 1fr) 200px minmax(0, 1fr)",
        "_gridGap": "32px 56px",
        "_alignItems": "center",
        "_margin": {"top": "56px"},
        "_gridTemplateColumns:tablet_portrait": "1fr",
    }))
    out.append(el(pipes_id, "html", diagram, [], {
        "html": '<svg class="wpfy-eco-pipes" aria-hidden="true" focusable="false"></svg>',
    }, "Eco pipes SVG"))
    out.append(el(col_l, "block", diagram, ["eclb01", "eclb02", "eclb03"], {
        "_cssClasses": "wpfy-eco-col wpfy-eco-col-l", "_display": "grid", "_rowGap": "28px",
    }))
    out.append(el(col_r, "block", diagram, ["ecrb01", "ecrb02", "ecrb03"], {
        "_cssClasses": "wpfy-eco-col wpfy-eco-col-r", "_display": "grid", "_rowGap": "28px",
    }))
    out += eco_box("eclb01", col_l, "Shared edge", "wpfy-box-blue", [("traefikproxy", "Traefik"), ("letsencrypt", "Let's Encrypt")])
    out += eco_box("eclb02", col_l, "Site runtime", "wpfy-box-teal", [("wordpress", "WordPress"), ("nginx", "Nginx"), ("php", "PHP-FPM")])
    out += eco_box("eclb03", col_l, "Data & cache", "wpfy-box-yellow", [("mariadb", "MariaDB"), ("redis", "Redis")])
    out += eco_box("ecrb01", col_r, "Host", "wpfy-box-cream", [("ubuntu", "Ubuntu"), ("docker", "Docker Engine"), ("docker", "Compose")])
    out += eco_box("ecrb02", col_r, "Access", "wpfy-box-red", [(None, "SFTP"), (None, "WP-CLI")])
    out += eco_box("ecrb03", col_r, "Safety nets", "wpfy-box-blue", [(None, "Backups"), (None, "Restore"), (None, "Diagnostics")])
    # Center CLI node
    out.append(el(col_c, "block", diagram, ["ecc1", "ecc2", "ecc3"], {
        "_cssClasses": "wpfy-eco-center",
        "_direction": "column",
        "_alignItems": "center",
        "_rowGap": "14px",
        "_typography": {"text-align": "center"},
        "_order:tablet_portrait": "-1",
    }))
    out.append(el("ecc1", "text-basic", col_c, [], {
        "text": "Your Ubuntu VPS",
        "tag": "span",
        "_cssClasses": "wpfy-eco-center-label",
        "_typography": {**{"font-family": "IBM Plex Mono"}, "font-size": "0.72rem", "text-transform": "uppercase"},
    }))
    node_id, bar_id, body_id = "ecc2", "ecc2b", "ecc2d"
    out.append(el(node_id, "block", col_c, [bar_id, body_id], {
        "_cssClasses": "wpfy-eco-node",
        "_attributes": [{"id": "ecnhd", "name": "aria-hidden", "value": "true"}],
    }))
    out.append(el(bar_id, "block", node_id, ["ecd1", "ecd2", "ecd3"], {"_cssClasses": "wpfy-term-bar", "_direction": "row", "_columnGap": "8px"}))
    for dot_id, cls in [("ecd1", "d1"), ("ecd2", "d2"), ("ecd3", "d3")]:
        out.append(el(dot_id, "div", bar_id, [], {"_cssClasses": f"wpfy-term-dot {cls}", "_width": "11px", "_height": "11px"}))
    out.append(el(body_id, "text-basic", node_id, [], {
        "text": '<span class="wpfy-t-prompt">$</span> wpfy<span class="wpfy-t-caret"></span>',
        "_cssClasses": "wpfy-eco-node-body",
        "_typography": {"font-family": "IBM Plex Mono", "font-size": "0.82rem"},
    }))
    out.append(el("ecc3", "text-basic", col_c, [], {
        "text": "One CLI runs it all",
        "tag": "span",
        "_cssClasses": "wpfy-eco-center-sub",
        "_typography": {**{"font-family": "IBM Plex Mono"}, "font-size": "0.72rem", "text-transform": "uppercase"},
    }))
    return out


def build_features_section() -> list[dict]:
    sid, wrap, head, grid = "fe0001", "fe0002", "fe0003", "fe0004"
    out = _section_shell(
        sid, wrap, [head, grid],
        css_id="features",
        global_classes=["wpfy-section-sky", "wpfy-section-pad"],
        deco_id="fedeco",
        deco_html_str=FEATURES_DECO,
        label="Features",
    )
    out += section_head(
        head, wrap,
        "Everything a WordPress VPS needs, as commands",
        title_css_id="features-title",
        lede="WordOps/Webinoly-style convenience, rebuilt around Docker isolation.",
    )
    card_ids = [f"fc00{i:02d}" for i in range(1, len(FEATURES) + 1)]
    out.append(el(grid, "block", wrap, card_ids, {
        "_cssClasses": "wpfy-grid wpfy-grid-4",
        "_display": "grid",
        "_gridTemplateColumns": "repeat(4, minmax(0, 1fr))",
        "_gridGap": "24px",
        "_gridTemplateColumns:tablet_portrait": "repeat(2, minmax(0, 1fr))",
        "_gridTemplateColumns:mobile_portrait": "1fr",
    }))
    for i, (tag, variant, title, body, cmd) in enumerate(FEATURES):
        out += feature_card(card_ids[i], grid, tag, variant, title, body, cmd, reveal_d=i % 4)
    return out


def build_how_section() -> list[dict]:
    sid, wrap, head, grid = "hw0001", "hw0002", "hw0003", "hw0004"
    out = _section_shell(
        sid, wrap, [head, grid],
        css_id="how-it-works",
        global_classes=["wpfy-section-pad"],
        label="How it works",
    )
    out += section_head(head, wrap, "From fresh VPS to managed WordPress in three steps", title_css_id="how-title")
    card_ids = ["hwc001", "hwc002", "hwc003"]
    out.append(el(grid, "block", wrap, card_ids, {
        "_cssClasses": "wpfy-grid wpfy-grid-3",
        "_display": "grid",
        "_gridTemplateColumns": "repeat(3, minmax(0, 1fr))",
        "_gridGap": "24px",
        "_gridTemplateColumns:mobile_portrait": "1fr",
    }))
    for i, (num, title, body, code) in enumerate(STEPS):
        cid = card_ids[i]
        num_id, h_id, p_id, w_id = _kid(cid, "n"), _kid(cid, "h"), _kid(cid, "p"), _kid(cid, "w")
        attrs = reveal_attr(i)
        card_settings: dict = {
            "tag": "article",
            "_cssGlobalClasses": ["wpfy-card"],
            "_cssClasses": "wpfy-reveal wpfy-step-card",
            "_rowGap": "12px",
        }
        if attrs:
            card_settings["_attributes"] = attrs
        out.append(el(cid, "block", grid, [num_id, h_id, p_id, w_id], card_settings, title))
        out.append(el(num_id, "text-basic", cid, [], {
            "text": num,
            "tag": "span",
            "_cssClasses": "wpfy-step-num",
            "_attributes": [{"id": f"{num_id}a", "name": "aria-hidden", "value": "true"}],
        }))
        out.append(el(h_id, "heading", cid, [], {"text": title, "tag": "h3"}))
        out.append(el(p_id, "text-basic", cid, [], {"text": body, "tag": "p"}))
        out.append(code_well(w_id, cid, code))
    return out


def build_who_section() -> list[dict]:
    sid, wrap, head, grid = "wh0001", "wh0002", "wh0003", "wh0004"
    out = _section_shell(
        sid, wrap, [head, grid],
        css_id="who",
        global_classes=["wpfy-section-sky", "wpfy-section-pad"],
        deco_id="whdeco",
        deco_html_str=WHO_DECO_TOP,
        label="Who is it for",
    )
    out += section_head(
        head, wrap, "Who is it for?",
        title_css_id="who-title",
        lede="Docker-grade isolation for everyone who runs WordPress on their own servers.",
    )
    card_ids = ["whc001", "whc002", "whc003"]
    out.append(el(grid, "block", wrap, card_ids, {
        "_cssClasses": "wpfy-grid wpfy-grid-3 wpfy-who-grid",
        "_display": "grid",
        "_gridTemplateColumns": "repeat(3, minmax(0, 1fr))",
        "_gridGap": "24px",
        "_gridTemplateColumns:mobile_portrait": "1fr",
    }))
    for i, (variant, title, body, doodle_idx) in enumerate(WHO_CARDS):
        cid = card_ids[i]
        deco_id, tag_id, p_id = _kid(cid, "d"), _kid(cid, "t"), _kid(cid, "p")
        attrs = reveal_attr(i)
        settings: dict = {"_cssClasses": "wpfy-who-card wpfy-reveal", "_rowGap": "12px"}
        if attrs:
            settings["_attributes"] = attrs
        out.append(el(cid, "block", grid, [deco_id, tag_id, p_id], settings, title))
        out.append(deco_html(deco_id, cid, WHO_CARDS_DOODLES[doodle_idx]))
        out.append(wpfy_tag(tag_id, cid, title, variant))
        out.append(el(p_id, "text-basic", cid, [], {"text": body, "tag": "p"}))
    out.append(deco_html("whdeco2", sid, WHO_DECO_BOTTOM))
    out[0]["children"].append("whdeco2")
    return out


def build_use_cases_section() -> list[dict]:
    sid, wrap, head = "uc0001", "uc0002", "uc0003"
    row_ids = ["ucr001", "ucr002"]
    out = _section_shell(
        sid, wrap, [head, *row_ids],
        css_id="use-cases",
        global_classes=["wpfy-section-pad"],
        deco_id="ucdeco",
        deco_html_str=USE_CASES_DECO,
        label="Use cases",
    )
    out += section_head(head, wrap, "Use cases", title_css_id="uc-title")
    for i, (flip, title, body, btn_url, btn_text, code) in enumerate(USE_CASES):
        rid = row_ids[i]
        copy_id, well_id, btn_id = _kid(rid, "c"), _kid(rid, "w"), _kid(rid, "b")
        h_id, p_id = _kid(copy_id, "h"), _kid(copy_id, "p")
        classes = "wpfy-uc-row wpfy-reveal"
        if flip:
            classes += " wpfy-uc-flip"
        out.append(el(rid, "block", wrap, [copy_id, well_id], {
            "_cssClasses": classes,
            "_display": "grid",
            "_gridTemplateColumns": "1fr 1fr",
            "_columnGap": "40px",
            "_alignItems": "center",
            "_gridTemplateColumns:mobile_landscape": "1fr",
        }))
        out.append(el(copy_id, "block", rid, [h_id, p_id, btn_id], {"_cssClasses": "wpfy-uc-copy", "_rowGap": "16px"}))
        out.append(el(h_id, "heading", copy_id, [], {"text": title, "tag": "h3"}))
        out.append(el(p_id, "text-basic", copy_id, [], {"text": body, "tag": "p"}))
        out.append(el(btn_id, "button", copy_id, [], {
            "text": btn_text,
            "link": {"type": "external", "url": btn_url, "newTab": btn_url.startswith("http")},
            "_cssGlobalClasses": ["wpfy-btn"],
        }))
        out.append(code_well(well_id, rid, code, extra_class="wpfy-uc-well"))
    return out


def build_cta_section() -> list[dict]:
    return [
        el("ct0001", "section", 0, ["ctdeco", "ct0002"], {
            "tag": "section",
            "_cssId": "beta",
            "_cssGlobalClasses": ["wpfy-cta-band"],
            "_position": "relative",
            "_overflow": "visible",
            "_attributes": [{"id": "ctattr", "name": "aria-labelledby", "value": "beta-title"}],
        }, "CTA band"),
        deco_html("ctdeco", "ct0001", CTA_DECO),
        el("ct0002", "container", "ct0001", ["ct0003", "ct0004", "ct0005"], {
            "_cssGlobalClasses": ["wpfy-wrap"],
            "_direction": "column",
            "_alignItems": "center",
        }),
        el("ct0003", "heading", "ct0002", [], {
            "text": "Try the WPFY beta",
            "tag": "h2",
            "_cssId": "beta-title",
            "_cssClasses": "wpfy-reveal",
            "_cssGlobalClasses": ["wpfy-heading-mono"],
            "_typography": {"font-size": "clamp(1.7rem, 1rem + 3vw, 2.8rem)", "text-align": "center"},
        }),
        el("ct0004", "text-basic", "ct0002", [], {
            "text": "Spin up a fresh Ubuntu VPS, run the installer, and create your first isolated WordPress site in minutes. Feedback from real deployments moves the beta forward.",
            "_cssClasses": "wpfy-reveal",
            "_attributes": reveal_attr(1),
            "_typography": {"text-align": "center"},
            "_widthMax": "560px",
            "_margin": {"bottom": "36px"},
        }),
        el("ct0005", "block", "ct0002", ["ct0006", "ct0007", "ct0008"], {
            "_cssClasses": "wpfy-reveal wpfy-cta-actions",
            "_attributes": reveal_attr(2),
            "_direction": "row",
            "_justifyContent": "center",
            "_columnGap": "16px",
            "_flexWrap": "wrap",
        }),
        el("ct0006", "button", "ct0005", [], {
            "text": "View on GitHub",
            "link": {"type": "external", "url": "https://github.com/wpfyorg/wpfy", "newTab": True},
            "_cssGlobalClasses": ["wpfy-btn", "wpfy-btn-ink"],
        }),
        el("ct0007", "button", "ct0005", [], {
            "text": "Join the forum",
            "link": {"type": "external", "url": "https://forum.wpfy.org", "newTab": True},
            "_cssGlobalClasses": ["wpfy-btn", "wpfy-btn-blue"],
        }),
        el("ct0008", "button", "ct0005", [], {
            "text": "Report issues & feedback",
            "link": {"type": "external", "url": "https://github.com/wpfyorg/wpfy/issues", "newTab": True},
            "_cssGlobalClasses": ["wpfy-btn"],
        }),
    ]


def build_subscribe_section() -> list[dict]:
    """Subscribe band — html only for form inputs (no native input element)."""
    sid, wrap = "sb0001", "sb0002"
    copy_id, form_id, status_id = "sb0003", "sb0004", "sb0005"
    form_html = (
        '<form class="wpfy-sub-form wpfy-reveal" style="--d:1" action="#" method="post" data-placeholder>'
        '<div class="wpfy-sub-fields">'
        '<label class="wpfy-sr-only" for="sub-email">Email address</label>'
        '<input id="sub-email" name="email" type="email" required placeholder="you@yourserver.com" autocomplete="email">'
        '<button class="wpfy-btn wpfy-btn-ink" type="submit">Subscribe</button>'
        '</div>'
        '<p class="wpfy-sub-privacy">'
        '<label for="wpfy-sub-privacy">'
        '<input id="wpfy-sub-privacy" name="privacy" type="checkbox" required value="1">'
        ' I agree to the <a href="/legal/privacy">Privacy Policy</a>.'
        '</label></p>'
        "</form>"
    )
    return [
        el(sid, "section", 0, ["sbdeco", wrap], {
            "tag": "section",
            "_cssId": "subscribe",
            "_cssGlobalClasses": ["wpfy-subscribe-band"],
            "_attributes": [{"id": "sbattr", "name": "aria-labelledby", "value": "sub-title"}],
        }, "Subscribe"),
        deco_html("sbdeco", sid, SUBSCRIBE_DECO),
        el(wrap, "container", sid, [copy_id, form_id, status_id], {
            "_cssGlobalClasses": ["wpfy-wrap", "wpfy-sub-inner"],
        }),
        el(copy_id, "block", wrap, ["sbh", "sbp"], {
            "_cssGlobalClasses": ["wpfy-sub-copy", "wpfy-reveal"],
            "_rowGap": "8px",
        }),
        el("sbh", "heading", copy_id, [], {
            "text": "Stay in the loop",
            "tag": "h2",
            "_cssId": "sub-title",
            "_cssGlobalClasses": ["wpfy-heading-mono"],
        }),
        el("sbp", "text-basic", copy_id, [], {
            "text": "Release notes, new guides, and beta milestones. No spam, unsubscribe anytime.",
            "tag": "p",
        }),
        el(form_id, "html", wrap, [], {"html": form_html}, "Subscribe form"),
        el(status_id, "text-basic", wrap, [], {
            "text": "Thanks! You're on the list.",
            "tag": "p",
            "_cssGlobalClasses": ["wpfy-sub-status"],
            "_visibility": "hidden",
            "_attributes": [{"id": "sbattr2", "name": "aria-live", "value": "polite"}],
        }),
    ]


def build_batch2_sections() -> list[dict]:
    """All sections after marquee."""
    out: list[dict] = []
    out += build_problem_section()
    out += build_eco_section()
    out += build_features_section()
    out += build_how_section()
    out += build_who_section()
    out += build_use_cases_section()
    out += build_cta_section()
    out += build_subscribe_section()
    return out
