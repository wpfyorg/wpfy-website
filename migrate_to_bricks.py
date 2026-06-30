#!/usr/bin/env python3
"""Push WPFY design framework to Bricks staging via Novamira MCP."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.request
import base64
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MCP_CONFIG = ROOT.parent / ".cursor" / "mcp.json"


def load_creds() -> tuple[str, str, str]:
    cfg = json.loads(MCP_CONFIG.read_text())
    env = cfg["mcpServers"]["novamira-wpfy-dev-wpfy-or"]["env"]
    return env["WP_API_URL"], env["WP_API_USERNAME"], env["WP_API_PASSWORD"]


class McpClient:
    def __init__(self) -> None:
        self.url, user, password = load_creds()
        auth = base64.b64encode(f"{user}:{password}".encode()).decode()
        self.auth = auth
        self.session = self._init()

    def _init(self) -> str:
        req = urllib.request.Request(
            self.url,
            data=json.dumps({
                "jsonrpc": "2.0", "id": 1, "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "wpfy-migrate", "version": "1.0"},
                },
            }).encode(),
            method="POST",
        )
        req.add_header("Content-Type", "application/json")
        req.add_header("Accept", "application/json, text/event-stream")
        req.add_header("Authorization", f"Basic {self.auth}")
        resp = urllib.request.urlopen(req)
        sid = resp.headers.get("Mcp-Session-Id") or resp.headers.get("mcp-session-id")
        if not sid:
            raise RuntimeError("No MCP session id")
        return sid

    def ability(self, name: str, parameters: dict | None = None) -> dict:
        payload = {
            "jsonrpc": "2.0", "id": 2, "method": "tools/call",
            "params": {
                "name": "mcp-adapter-execute-ability",
                "arguments": {"ability_name": name, "parameters": parameters or {}},
            },
        }
        req = urllib.request.Request(self.url, data=json.dumps(payload).encode(), method="POST")
        req.add_header("Content-Type", "application/json")
        req.add_header("Authorization", f"Basic {self.auth}")
        req.add_header("Mcp-Session-Id", self.session)
        raw = json.loads(urllib.request.urlopen(req).read())
        sc = raw.get("result", {}).get("structuredContent", {})
        if sc.get("success") is False:
            raise RuntimeError(f"{name} failed: {sc.get('error', sc)}")
        if sc.get("success"):
            return sc.get("data", sc)
        content = raw.get("result", {}).get("content", [])
        if content:
            try:
                return json.loads(content[0]["text"])
            except json.JSONDecodeError:
                pass
        if raw.get("result", {}).get("isError"):
            raise RuntimeError(content[0]["text"] if content else str(raw))
        return raw


COLORS = [
    ("cream", "#f4efea"),
    ("paper", "#ffffff"),
    ("ink", "#383838"),
    ("ink-soft", "#5c5c5c"),
    ("blue", "#97d4ff"),
    ("blue-deep", "#6fc2ff"),
    ("yellow", "#ffde00"),
    ("teal", "#53dbc9"),
    ("teal-deep", "#16aa98"),
    ("red", "#f2655a"),
    ("green", "#1fa04c"),
]

from bricks_common import MONO_TYPO, el, marquee_track_html
from bricks_global_classes import CLASS_IDS, GLOBAL_CLASSES
from bricks_global_variables import VARIABLES


def push_tokens(client: McpClient) -> None:
    print("→ Color palette")
    for name, hex_val in COLORS:
        try:
            client.ability("novamira/bricks-add-color-palette-entry", {"name": name, "raw": hex_val})
            print(f"  + {name}")
        except RuntimeError as e:
            if "exists" in str(e).lower():
                print(f"  ~ {name} (exists)")
            else:
                raise

    print("→ CSS variables")
    for name, value, cat in VARIABLES:
        try:
            client.ability("novamira/bricks-create-variable", {"name": name, "value": value, "category": cat})
            print(f"  + {name}")
        except RuntimeError as e:
            if "exists" in str(e).lower():
                print(f"  ~ {name} (exists)")
            else:
                raise

    print("→ Global classes")
    for name, category, settings in GLOBAL_CLASSES:
        try:
            client.ability("novamira/bricks-create-global-class", {
                "name": name, "category": category, "settings": settings,
            })
            print(f"  + {name}")
        except RuntimeError as e:
            if "exists" in str(e).lower():
                print(f"  ~ {name} (exists)")
            else:
                raise

    print("→ Theme style")
    try:
        client.ability("novamira/bricks-create-theme-style", {
            "label": "WPFY Main",
            "conditions": [{"main": "any"}],
            "settings": {
                "general": {"containerWidth": "1200px", "sectionVerticalPadding": "96px"},
                "colors": {
                    "primary": {"raw": "var(--wpfy-blue-deep)"},
                    "secondary": {"raw": "var(--wpfy-ink)"},
                    "light": {"raw": "var(--wpfy-cream)"},
                    "dark": {"raw": "var(--wpfy-ink)"},
                },
                "typography": {
                    "fontFamily": "Inter",
                    "bodyTypography": {
                        "font-size": "16px",
                        "line-height": "1.6",
                        "color": {"raw": "var(--wpfy-ink)"},
                    },
                    "h1Typography": {
                        "font-family": "IBM Plex Mono",
                        "font-size": "clamp(2rem, 1rem + 4.6vw, 3.6rem)",
                        "font-weight": "500",
                        "text-transform": "uppercase",
                        "letter-spacing": "0.02em",
                        "line-height": "1.15",
                    },
                    "h2Typography": {
                        "font-family": "IBM Plex Mono",
                        "font-size": "clamp(1.5rem, 1rem + 2.4vw, 2.4rem)",
                        "font-weight": "500",
                        "text-transform": "uppercase",
                        "letter-spacing": "0.02em",
                        "line-height": "1.15",
                    },
                    "h3Typography": {
                        "font-family": "IBM Plex Mono",
                        "font-size": "0.92rem",
                        "font-weight": "500",
                        "text-transform": "uppercase",
                        "letter-spacing": "0.02em",
                    },
                    "linkColor": {"raw": "var(--wpfy-ink)"},
                },
                "button": {
                    "backgroundColor": {"raw": "var(--wpfy-cream)"},
                    "border": {
                        "width": {"top": "2px", "right": "2px", "bottom": "2px", "left": "2px"},
                        "style": "solid",
                        "color": {"raw": "var(--wpfy-ink)"},
                        "radius": {"top": "2px", "right": "2px", "bottom": "2px", "left": "2px"},
                    },
                },
            },
        })
        print("  + WPFY Main")
    except RuntimeError as e:
        if "exists" in str(e).lower():
            print("  ~ WPFY Main (exists)")
        else:
            raise


def push_child_assets(client: McpClient) -> None:
    print("→ Child theme assets")
    assets_dir = ROOT / "bricks-child-assets"
    for fname in ("wpfy.css", "wpfy.js"):
        content = (assets_dir / fname).read_text()
        path = f"wp-content/themes/bricks-child/assets/{fname}"
        try:
            client.ability("novamira/write-file", {"path": path, "content": content})
            print(f"  + {path}")
        except RuntimeError:
            client.ability("novamira/edit-file", {
                "path": path,
                "old_string": client.ability("novamira/read-file", {"path": path})["content"],
                "new_string": content,
            })
            print(f"  ~ {path} (updated)")

    icons_dir = assets_dir / "icons"
    if icons_dir.is_dir():
        for icon_path in sorted(icons_dir.glob("*.svg")):
            path = f"wp-content/themes/bricks-child/assets/icons/{icon_path.name}"
            content = icon_path.read_text()
            try:
                client.ability("novamira/write-file", {"path": path, "content": content})
                print(f"  + {path}")
            except RuntimeError:
                client.ability("novamira/edit-file", {
                    "path": path,
                    "old_string": client.ability("novamira/read-file", {"path": path})["content"],
                    "new_string": content,
                })
                print(f"  ~ {path} (updated)")

    sandbox_php = (assets_dir / "wpfy-assets.php").read_text()
    client.ability("novamira/write-file", {
        "path": "wp-content/novamira-sandbox/wpfy-assets.php",
        "content": sandbox_php,
    })
    print("  + wp-content/novamira-sandbox/wpfy-assets.php (asset loader)")


def sftp_put(local: Path, remote: str) -> bool:
    """Upload via SFTP when MCP/execute-php cannot persist theme files."""
    cfg = json.loads(MCP_CONFIG.read_text())
    ssh = cfg["mcpServers"].get("ssh-mcp-server", {}).get("args", [])
    host = user = password = None
    for i, arg in enumerate(ssh):
        if arg.startswith("--host="):
            host = arg.split("=", 1)[1]
        elif arg.startswith("--user="):
            user = arg.split("=", 1)[1]
        elif arg.startswith("--password="):
            password = arg.split("=", 1)[1]
    if not (host and user and password):
        return False
    env = os.environ.copy()
    env["SSHPASS"] = password
    proc = subprocess.run(
        ["sshpass", "-e", "sftp", "-o", "StrictHostKeyChecking=no", f"{user}@{host}:{remote}", str(local)],
        env=env,
        capture_output=True,
        text=True,
    )
    return proc.returncode == 0


def push_marketing_hooks(client: McpClient) -> None:
    """Patch functions.php with body class + front-page title (theme dir not always writable)."""
    hooks = """
// WPFY marketing site: body class + front-page document title (parity with static site).
if ( ! function_exists( 'wpfy_marketing_body_class' ) ) {
	function wpfy_marketing_body_class( $classes ) {
		if ( is_admin() ) {
			return $classes;
		}
		if ( ! in_array( 'wpfy-gutenberg-shell', $classes, true ) && ! in_array( 'wpfy-site', $classes, true ) ) {
			$classes[] = 'wpfy-site';
		}
		return $classes;
	}
	add_filter( 'body_class', 'wpfy_marketing_body_class', 20 );
}
if ( ! function_exists( 'wpfy_marketing_document_title' ) ) {
	function wpfy_marketing_document_title( $title ) {
		if ( is_front_page() ) {
			return 'WPFY · Docker-first WordPress server management for Ubuntu VPS';
		}
		return $title;
	}
	add_filter( 'pre_get_document_title', 'wpfy_marketing_document_title', 20 );
	function wpfy_marketing_document_title_parts( $parts ) {
		if ( is_front_page() ) {
			$parts['title'] = 'WPFY · Docker-first WordPress server management for Ubuntu VPS';
			unset( $parts['tagline'], $parts['site'] );
		}
		return $parts;
	}
	add_filter( 'document_title_parts', 'wpfy_marketing_document_title_parts', 20 );
}
"""
    b64 = base64.b64encode(hooks.encode()).decode()
    result = client.ability("novamira/execute-php", {
        "code": f"""
$path = get_stylesheet_directory() . '/functions.php';
$functions = file_get_contents($path);
$marker = 'wpfy_marketing_body_class';
$block = base64_decode({json.dumps(b64)});
if (strpos($functions, $marker) === false) {{
    $functions = rtrim($functions) . "\\n" . $block . "\\n";
    if (file_put_contents($path, $functions) === false) {{
        return 'write failed';
    }}
    return 'patched';
}}
return 'already patched';
""",
    })
    print(f"  ~ functions.php marketing hooks ({result.get('return_value', result)})")


def push_theme_php(client: McpClient) -> None:
    """Push Gutenberg template + theme hooks into bricks-child."""
    print("→ Child theme PHP (Gutenberg templates)")
    assets_dir = ROOT / "bricks-child-assets"
    theme_files = {
        "wpfy-theme.php": assets_dir / "wpfy-theme.php",
        "template-wpfy-content.php": assets_dir / "template-wpfy-content.php",
        "single.php": assets_dir / "single.php",
    }
    for fname, local_path in theme_files.items():
        content = local_path.read_text()
        remote = f"wp-content/themes/bricks-child/{fname}"
        b64 = base64.b64encode(content.encode()).decode()
        result = client.ability("novamira/execute-php", {
            "code": f"""
$path = get_stylesheet_directory() . '/' . {json.dumps(fname)};
$content = base64_decode({json.dumps(b64)});
if ($content === false || file_put_contents($path, $content) === false) {{
    return 'write failed: ' . $path;
}}
return 'ok: ' . $path . ' (' . strlen($content) . ' bytes)';
""",
        })
        print(f"  + themes/bricks-child/{fname} ({result.get('return_value', result)})")

    client.ability("novamira/execute-php", {
        "code": r"""
$path = get_stylesheet_directory() . '/functions.php';
$functions = file_get_contents($path);
$require_line = "require_once __DIR__ . '/wpfy-theme.php';";
// Repair a prior bad patch that inserted literal \n tokens.
$functions = str_replace('\\n', "\n", $functions);
if (strpos($functions, $require_line) === false) {
    $functions = rtrim($functions) . "\n\n/**\n * WPFY Gutenberg content shell.\n */\n" . $require_line . "\n";
}
if (file_put_contents($path, $functions) === false) {
    return 'write failed';
}
return 'ok';
""",
    })
    print("  ~ themes/bricks-child/functions.php (require wpfy-theme.php)")
    push_marketing_hooks(client)


def get_global_class_map(client: McpClient) -> dict[str, str]:
    """Resolve Bricks global class names to stored IDs (required for frontend output)."""
    result = client.ability("novamira/bricks-list-global-classes", {})
    payload = result.get("data", result)
    classes = payload if isinstance(payload, list) else payload.get("classes", [])
    return {c["name"]: c["id"] for c in classes if c.get("name") and c.get("id")}


def apply_global_class_ids(elements: list[dict], class_map: dict[str, str]) -> list[dict]:
    out: list[dict] = []
    for node in elements:
        node = dict(node)
        settings = dict(node.get("settings") or {})
        names = settings.get("_cssGlobalClasses")
        if names:
            resolved = []
            for name in names:
                gid = class_map.get(name)
                if not gid:
                    raise RuntimeError(f"Global class not found: {name}")
                resolved.append(gid)
            settings["_cssGlobalClasses"] = resolved
        node["settings"] = settings
        out.append(node)
    return out


def push_content(client: McpClient, post_id: int, elements: list[dict], *, area: str = "content") -> None:
    class_map = get_global_class_map(client)
    client.ability("novamira/bricks-set-content", {
        "post_id": post_id,
        "area": area,
        "elements": apply_global_class_ids(elements, class_map),
    })


from bricks_builders import deco_html, footer_col_title, link_list, nav_ul, reveal_attr


def build_header_elements() -> list[dict]:
    """Announce bar + sticky header with logo, nav, CTA."""
    nav_links = [
        ("Stack", "#stack"),
        ("Features", "#features"),
        ("How it Works", "#how-it-works"),
        ("Forum", "https://forum.wpfy.org"),
        ("Docs", "https://docs.wpfy.org"),
        ("GitHub", "https://github.com/wpfyorg/wpfy"),
    ]
    out = [
        el("an0001", "section", 0, ["an0002"], {"tag": "div", "_cssGlobalClasses": ["wpfy-announce"]}, "Announce"),
        el("an0002", "container", "an0001", ["an0003"], {"_direction": "row", "_justifyContent": "center", "_alignItems": "center"}, "Announce inner"),
        el("an0003", "text-basic", "an0002", [], {
            "text": 'WPFY is in beta · test on a fresh Ubuntu VPS first — <a href="https://github.com/wpfyorg/wpfy">Read the notes →</a>',
        }),
        el("hd0001", "section", 0, ["hd0002"], {"tag": "header", "_cssGlobalClasses": ["wpfy-site-header"]}, "Site header"),
        el("hd0002", "container", "hd0001", ["hd0003", "hd0004", "hd0005", "hd0006"], {
            "_cssGlobalClasses": ["wpfy-wrap"],
            "_direction": "row",
            "_alignItems": "center",
            "_columnGap": "28px",
            "_heightMin": "64px",
        }, "Nav row"),
        el("hd0003", "text-basic", "hd0002", [], {
            "text": 'wpfy<span style="color:var(--wpfy-teal-deep)">_</span>',
            "tag": "a",
            "link": {"type": "external", "url": "/"},
            "_cssGlobalClasses": ["wpfy-logo"],
        }, "Logo"),
        el("hd0005", "button", "hd0002", [], {
            "text": "Star on GitHub",
            "link": {"type": "external", "url": "https://github.com/wpfyorg/wpfy", "newTab": True},
            "_cssGlobalClasses": ["wpfy-btn", "wpfy-btn-blue"],
        }, "GitHub CTA"),
        el("hd0006", "button", "hd0002", [], {
            "text": "☰",
            "_cssClasses": "wpfy-menu-btn",
            "_attributes": [
                {"id": "mb0002", "name": "aria-label", "value": "Toggle navigation"},
                {"id": "mb0003", "name": "aria-expanded", "value": "false"},
                {"id": "mb0004", "name": "aria-controls", "value": "wpfy-nav-links"},
            ],
            "_display:mobile_landscape": "inline-flex",
            "_display": "none",
            "_cssCustom": "%root% { border: var(--wpfy-border); border-radius: 2px; background: var(--wpfy-paper); padding: 9px; min-height: auto; }",
        }, "Mobile menu"),
    ]
    out += nav_ul("hd0004", "hd0002", nav_links)
    return out


PRODUCT_LINKS = [
    ("GitHub", "https://github.com/wpfyorg/wpfy"),
    ("Forum", "https://forum.wpfy.org"),
    ("Docs", "https://docs.wpfy.org"),
    ("Security", "https://github.com/wpfyorg/wpfy/blob/main/docs/SECURITY.md"),
    ("License (AGPL-3.0)", "https://github.com/wpfyorg/wpfy/blob/main/LICENSE"),
]

LEGAL_LINKS = [
    ("Privacy", "/legal/privacy"),
    ("Terms", "/legal/terms"),
    ("Cookies", "/legal/cookies"),
    ("Affiliate", "/legal/affiliate-disclosure"),
    ("Disclaimer", "/legal/disclaimer"),
    ("Refund", "/legal/refund"),
    ("Community", "/legal/community"),
]


def build_footer_elements() -> list[dict]:
    grid_id = "ft0003"
    c1, c2, c3, c4 = "ftc001", "ftc002", "ftc003", "ftc004"
    out = [
        el("ft0001", "section", 0, ["ft0002"], {"tag": "footer", "_cssGlobalClasses": ["wpfy-site-footer"]}, "Site footer"),
        el("ft0002", "container", "ft0001", [grid_id, "ft0004"], {
            "_cssGlobalClasses": ["wpfy-wrap"],
            "_cssClasses": "wpfy-footer-inner",
        }),
        el(grid_id, "block", "ft0002", [c1, c2, c3, c4], {
            "_cssClasses": "wpfy-footer-grid",
            "_display": "grid",
            "_gridTemplateColumns": "repeat(4, minmax(0, 1fr))",
            "_gridGap": "32px 40px",
            "_padding": {"bottom": "48px"},
            "_gridTemplateColumns:tablet_portrait": "1fr 1fr",
            "_gridTemplateColumns:mobile_portrait": "1fr",
        }, "Footer grid"),
        el(c1, "block", grid_id, ["ftl001", "ftm001"], {"_cssClasses": "wpfy-footer-col", "_rowGap": "14px"}),
        el("ftl001", "text-basic", c1, [], {
            "text": 'wpfy<span class="mark">_</span>',
            "tag": "a",
            "link": {"type": "external", "url": "/"},
            "_cssGlobalClasses": ["wpfy-logo"],
        }, "Logo"),
        el("ftm001", "text-basic", c1, [], {
            "text": (
                "Docker-first WordPress server management for Ubuntu VPS.<br>"
                "Beta software, test on a fresh VPS first.<br>"
                "Licensed under AGPL-3.0."
            ),
            "tag": "p",
            "_cssClasses": "wpfy-footer-meta",
        }),
        el(c2, "block", grid_id, ["ftp001", "ftpl01"], {"_cssClasses": "wpfy-footer-col", "_rowGap": "14px"}),
        footer_col_title("ftp001", c2, "Product"),
        el(c3, "block", grid_id, ["ftl201", "ftll01"], {"_cssClasses": "wpfy-footer-col", "_rowGap": "14px"}),
        footer_col_title("ftl201", c3, "Legal"),
        el(c4, "block", grid_id, ["fts001", "ftcs01"], {"_cssClasses": "wpfy-footer-col", "_rowGap": "14px"}),
        footer_col_title("fts001", c4, "Settings"),
        el("ftcs01", "button", c4, [], {
            "text": "Cookie settings",
            "tag": "button",
            "_cssClasses": "wpfy-cookie-settings",
            "_attributes": [{"id": "ftcsk", "name": "data-cookie-settings", "value": ""}],
        }),
        el("ft0004", "text", "ft0002", [], {
            "text": (
                "Developed by folks behind "
                '<a href="https://bricksgenius.com" target="_blank" rel="noopener">BricksGenius</a>, Hosted on '
                '<a href="https://www.vultr.com" target="_blank" rel="noopener">Vultr</a> using '
                '<a href="https://wpfy.org">wpfy</a>, built with '
                '<a href="https://bricksbuilder.io" target="_blank" rel="noopener">Bricks Builder</a> and Optimised by '
                '<a href="https://flyingpress.com" target="_blank" rel="noopener">FlyingPress</a>.'
            ),
            "_cssClasses": "wpfy-footer-bar",
        }, "Footer bar"),
    ]
    out += link_list("ftpl01", c2, PRODUCT_LINKS, new_tab=True, item_ids=["ftpr01", "ftpr02", "ftpr03", "ftpr04", "ftpr05"])
    out += link_list("ftll01", c3, LEGAL_LINKS, item_ids=["ftlg01", "ftlg02", "ftlg03", "ftlg04", "ftlg05", "ftlg06", "ftlg07"])
    return out


def build_hero_section() -> list[dict]:
    from decorations import HERO_DOODLES

    copy_cmd = "curl -fsSL https://raw.githubusercontent.com/wpfyorg/wpfy/main/install.sh | sudo bash"
    term_id, term_wrap, doodle_id = "hr0012", "hr0010", "hr0011"
    bar_id, pre_id = "hrbar1", "hrpre1"
    dot_ids = ["hrdot1", "hrdot2", "hrdot3"]
    return [
        el("hr0001", "section", 0, ["hr0002"], {
            "tag": "section",
            "_cssGlobalClasses": ["wpfy-hero"],
            "_attributes": [{"id": "hrattr", "name": "aria-labelledby", "value": "hero-title"}],
        }, "Hero"),
        el("hr0002", "container", "hr0001", ["hr0003", "hr0004", "hr0005", "hr0006", "hr0007"], {
            "_cssGlobalClasses": ["wpfy-wrap"],
            "_direction": "column",
            "_alignItems": "center",
        }),
        el("hr0003", "heading", "hr0002", [], {
            "text": "Infrastructure for WordPress",
            "tag": "h1",
            "_cssId": "hero-title",
            "_cssClasses": "wpfy-reveal",
            "_cssGlobalClasses": ["wpfy-heading-mono"],
            "_widthMax": "1080px",
            "_typography": {"font-size": "clamp(2rem, 1rem + 4.6vw, 3.6rem)", "text-align": "center"},
        }),
        el("hr0004", "text-basic", "hr0002", [], {
            "text": "Docker-first server management for Ubuntu VPS. Install, provision, secure, back up, restore, and manage isolated WordPress sites from one CLI.",
            "_cssClasses": "wpfy-reveal",
            "_attributes": reveal_attr(1),
            "_typography": {"font-size": "1.1rem", "color": {"raw": "var(--wpfy-ink-soft)"}, "text-align": "center"},
            "_widthMax": "700px",
            "_margin": {"top": "24px", "bottom": "36px"},
        }),
        el("hr0005", "block", "hr0002", ["hr0008", "hr0009"], {
            "_cssClasses": "wpfy-reveal wpfy-hero-ctas",
            "_attributes": reveal_attr(2),
            "_direction": "row",
            "_justifyContent": "center",
            "_columnGap": "16px",
            "_flexWrap": "wrap",
        }),
        el("hr0008", "button", "hr0005", [], {
            "text": "View on GitHub",
            "link": {"type": "external", "url": "https://github.com/wpfyorg/wpfy", "newTab": True},
            "_cssGlobalClasses": ["wpfy-btn", "wpfy-btn-blue"],
        }),
        el("hr0009", "button", "hr0005", [], {
            "text": "Installation Guide",
            "link": {"type": "external", "url": "https://github.com/wpfyorg/wpfy/blob/main/docs/INSTALLER.md", "newTab": True},
            "_cssGlobalClasses": ["wpfy-btn"],
        }),
        el("hr0006", "text-basic", "hr0002", [], {
            "text": "<strong>Beta software.</strong> Test on a fresh VPS before important production sites.",
            "_cssClasses": "wpfy-reveal",
            "_attributes": reveal_attr(3),
            "_typography": {**MONO_TYPO, "font-size": "0.75rem", "text-align": "center", "color": {"raw": "var(--wpfy-ink-soft)"}},
            "_margin": {"top": "28px"},
        }),
        el("hr0007", "div", "hr0002", [doodle_id, term_wrap], {
            "_cssClasses": "wpfy-reveal wpfy-term-stage",
            "_attributes": reveal_attr(4),
            "_widthMax": "860px",
            "_margin": {"top": "64px", "left": "auto", "right": "auto"},
        }),
        deco_html(doodle_id, "hr0007", HERO_DOODLES, "Hero doodles"),
        el(term_wrap, "block", "hr0007", [bar_id, pre_id], {"_cssClasses": "wpfy-terminal"}, "Terminal"),
        el(bar_id, "block", term_wrap, [*dot_ids, "hrttt1", "hrcopy"], {
            "_cssClasses": "wpfy-term-bar",
            "_direction": "row",
            "_alignItems": "center",
            "_columnGap": "8px",
        }),
        el(dot_ids[0], "div", bar_id, [], {"_cssClasses": "wpfy-term-dot d1", "_width": "11px", "_height": "11px"}),
        el(dot_ids[1], "div", bar_id, [], {"_cssClasses": "wpfy-term-dot d2", "_width": "11px", "_height": "11px"}),
        el(dot_ids[2], "div", bar_id, [], {"_cssClasses": "wpfy-term-dot d3", "_width": "11px", "_height": "11px"}),
        el("hrttt1", "text-basic", bar_id, [], {
            "text": "root@vps:~",
            "tag": "span",
            "_cssClasses": "wpfy-term-title",
            "_margin": {"left": "8px"},
        }),
        el("hrcopy", "html", bar_id, [], {
            "html": (
                f'<button type="button" class="wpfy-copy-btn" data-copy="{copy_cmd}">'
                "<span>copy</span></button>"
            ),
            "_margin": {"left": "auto"},
        }, "Copy install cmd"),
        el(pre_id, "html", term_wrap, [], {
            "html": '<pre class="wpfy-term-body" id="wpfy-hero-term" aria-hidden="true"></pre>',
        }, "Terminal output"),
    ]


def build_marquee() -> list[dict]:
    """Marquee band — single html track with duplicated inline spans for seamless loop."""
    return [
        el("mq0001", "section", 0, ["mq0002"], {
            "tag": "div",
            "_cssGlobalClasses": ["wpfy-marquee", "wpfy-marquee-yellow"],
            "_attributes": [{"id": "mqattr", "name": "aria-hidden", "value": "true"}],
        }, "Marquee"),
        el("mq0002", "html", "mq0001", [], {
            "html": marquee_track_html(),
        }, "Marquee track"),
    ]


def push_templates_and_page(client: McpClient) -> None:
    class_map = get_global_class_map(client)
    header_els = apply_global_class_ids(build_header_elements(), class_map)

    print("→ Header template")
    header = client.ability("novamira/bricks-create-template", {
        "title": "WPFY Header",
        "type": "header",
        "elements": header_els,
        "template_settings": {"headerSticky": True},
    })
    header_id = header.get("template_id") or header.get("id")
    client.ability("novamira/bricks-set-template-conditions", {
        "template_id": header_id,
        "conditions": [{"main": "any"}],
    })
    print(f"  + header template #{header_id}")

    print("→ Footer template")
    footer_els = apply_global_class_ids(build_footer_elements(), class_map)
    footer = client.ability("novamira/bricks-create-template", {
        "title": "WPFY Footer",
        "type": "footer",
        "elements": footer_els,
    })
    footer_id = footer.get("template_id") or footer.get("id")
    client.ability("novamira/bricks-set-template-conditions", {
        "template_id": footer_id,
        "conditions": [{"main": "any"}],
    })
    print(f"  + footer template #{footer_id}")

    print("→ Home page")
    pages = client.ability("novamira/create-post", {
        "title": "WPFY — Docker-first WordPress server management",
        "slug": "home",
        "status": "publish",
        "post_type": "page",
    })
    page_id = pages.get("post_id") or pages.get("id")
    print(f"  + page #{page_id}")

    hero = build_hero_section()
    marquee = build_marquee()
    push_content(client, page_id, hero + marquee)
    client.ability("novamira/bricks-set-settings", {
        "post_id": page_id,
        "settings": {
            "pageTitle": "hide",
            "contentWidth": "full_width",
        },
    })
    client.ability("novamira/update-post", {
        "post_id": page_id,
        "meta": {"_wp_page_template": "page"},
    })
    print(f"  + hero + marquee content on page #{page_id}")

    try:
        client.ability("novamira/run-wp-cli", {
            "args": ["option", "update", "show_on_front", "page"],
        })
        client.ability("novamira/run-wp-cli", {
            "args": ["option", "update", "page_on_front", str(page_id)],
        })
        print("  + set as front page")
    except RuntimeError as e:
        print(f"  ! front page setting skipped: {e}")


def resolve_home_page_id(client: McpClient) -> int:
    result = client.ability("novamira/execute-php", {
        "code": (
            "$front = (int) get_option('page_on_front');"
            "if ($front) return $front;"
            "$p = get_page_by_path('home');"
            "return $p ? (int) $p->ID : 0;"
        ),
    })
    page_id = int(result.get("return_value") or 0)
    if not page_id:
        raise RuntimeError("Home page not found — run migrate_to_bricks.py templates first")
    return page_id


def push_templates_refresh(client: McpClient) -> None:
    """Re-push header/footer templates with resolved global class IDs."""
    class_map = get_global_class_map(client)
    for template_id, builder, label, area in (
        (9, build_header_elements, "header", "header"),
        (10, build_footer_elements, "footer", "footer"),
    ):
        print(f"→ Refresh {label} template #{template_id}")
        els = apply_global_class_ids(builder(), class_map)
        client.ability("novamira/bricks-set-content", {
            "post_id": template_id,
            "area": area,
            "elements": els,
        })
        print(f"  ~ template #{template_id} ({area})")


HOME_PAGE_TITLE = "WPFY · Docker-first WordPress server management for Ubuntu VPS"


def push_batch2(client: McpClient, page_id: int | None = None) -> None:
    from batch2_sections import build_batch2_sections

    if page_id is None:
        page_id = resolve_home_page_id(client)
    print(f"→ Batch 2 sections on page #{page_id}")
    hero = build_hero_section()
    marquee = build_marquee()
    batch2 = build_batch2_sections()
    push_content(client, page_id, hero + marquee + batch2)
    client.ability("novamira/update-post", {
        "post_id": page_id,
        "title": HOME_PAGE_TITLE,
    })
    print(f"  + {len(batch2)} section elements ({len(hero + marquee + batch2)} total nodes)")
    print(f"  + page title → {HOME_PAGE_TITLE!r}")


def legal_nav_html(current_slug: str) -> str:
    from generate_legal_pages import LEGAL_NAV

    lines = []
    for label, slug in LEGAL_NAV:
        cur = ' aria-current="page"' if slug == current_slug else ""
        lines.append(f'        <li><a href="/legal/{slug}"{cur}>{label}</a></li>')
    return "\n".join(lines)


def legal_main_html(slug: str, title: str, body: str) -> str:
    from generate_legal_pages import LAST_UPDATED, legal_breadcrumbs_html

    display_title = title.replace("&amp;", "&")
    return (
        f'<div class="legal-doc">\n'
        f'  <div class="wpfy-wrap" style="padding-top:24px;padding-bottom:0">\n'
        f'    <a class="wpfy-btn legal-back" href="/">← Back to home</a>\n'
        f"  </div>\n"
        f'  <div class="wpfy-wrap legal-layout">\n'
        f'    <article class="legal-article">\n'
        f"      {legal_breadcrumbs_html(display_title)}\n"
        f'      <h1 class="wpfy-heading-mono">{display_title}</h1>\n'
        f'      <p class="legal-meta">Last updated: {LAST_UPDATED}</p>\n'
        f"{body}\n"
        f"    </article>\n"
        f'    <nav class="legal-nav" aria-label="Legal pages">\n'
        f'      <p class="legal-nav-title">Legal</p>\n'
        f"      <ul>\n"
        f"{legal_nav_html(slug)}\n"
        f"      </ul>\n"
        f"    </nav>\n"
        f"  </div>\n"
        f"</div>"
    )


def build_legal_page_elements(slug: str, title: str, body: str) -> list[dict]:
    import re

    html = legal_main_html(slug, title, body)
    sid = re.sub(r"[^a-z0-9]", "", slug)[:6].ljust(6, "0")
    return [
        el(f"{sid}a1", "section", 0, [f"{sid}a2"], {
            "_cssGlobalClasses": ["wpfy-section-pad"],
            "_padding": {"top": "0", "bottom": "0"},
        }, f"Legal: {title}"),
        el(f"{sid}a2", "html", f"{sid}a1", [], {"html": html}, "Legal body HTML"),
    ]


def ensure_legal_parent_id(client: McpClient) -> int:
    result = client.ability("novamira/execute-php", {
        "code": r"""
$legal = get_page_by_path('legal');
if ($legal) {
    return (int) $legal->ID;
}
$id = wp_insert_post([
    'post_title' => 'Legal',
    'post_name' => 'legal',
    'post_type' => 'page',
    'post_status' => 'publish',
    'post_content' => '',
]);
return (int) $id;
""",
    })
    parent_id = int(result.get("return_value") or 0)
    if not parent_id:
        raise RuntimeError("Failed to create legal parent page")
    return parent_id


def find_legal_child_id(client: McpClient, parent_id: int, slug: str) -> int:
    result = client.ability("novamira/execute-php", {
        "code": f"""
$parent = {parent_id};
$slug = {json.dumps(slug)};
$pages = get_posts([
    'post_type' => 'page',
    'post_status' => ['publish', 'draft', 'private'],
    'post_parent' => $parent,
    'name' => $slug,
    'numberposts' => 1,
]);
return $pages ? (int) $pages[0]->ID : 0;
""",
    })
    return int(result.get("return_value") or 0)


def enable_gutenberg_shell(client: McpClient, page_id: int) -> None:
    """Switch a page/post from Bricks canvas to native block editor shell."""
    client.ability("novamira/execute-php", {
        "code": f"""
$id = {page_id};
delete_post_meta($id, '_bricks_page_content_2');
delete_post_meta($id, '_bricks_page_settings');
update_post_meta($id, '_bricks_editor_mode', 'wordpress');
update_post_meta($id, '_wp_page_template', 'template-wpfy-content.php');
return true;
""",
    })


def push_legal_pages(client: McpClient) -> None:
    from generate_legal_pages import PAGES

    print("→ Legal parent page")
    parent_id = ensure_legal_parent_id(client)
    print(f"  + legal parent #{parent_id}")
    enable_gutenberg_shell(client, parent_id)

    for slug, (title, body) in PAGES.items():
        print(f"→ Legal page: {slug}")
        page_id = find_legal_child_id(client, parent_id, slug)
        display_title = title.replace("&amp;", "&")
        # Body only: shell template adds title, nav, and header offset.
        content = "\n".join(line.strip() for line in body.strip().splitlines())

        if page_id:
            client.ability("novamira/update-post", {
                "post_id": page_id,
                "title": display_title,
                "status": "publish",
                "content": content,
            })
            print(f"  ~ updated page #{page_id}")
        else:
            created = client.ability("novamira/create-post", {
                "title": display_title,
                "slug": slug,
                "status": "publish",
                "post_type": "page",
                "parent": parent_id,
                "content": content,
            })
            page_id = int(created.get("post_id") or created.get("id") or 0)
            if not page_id:
                raise RuntimeError(f"Failed to create legal page: {slug}")
            print(f"  + created page #{page_id}")

        enable_gutenberg_shell(client, page_id)
        print(f"  + gutenberg content on #{page_id} (/legal/{slug})")

    try:
        client.ability("novamira/run-wp-cli", {
            "args": ["rewrite", "flush"],
        })
        print("  + flushed rewrite rules")
    except RuntimeError as e:
        print(f"  ! rewrite flush skipped: {e}")


def push_gutenberg(client: McpClient) -> None:
    """Push Gutenberg templates, assets, footer, and legal pages."""
    push_child_assets(client)
    push_theme_php(client)
    push_templates_refresh(client)
    push_legal_pages(client)


def main() -> int:
    step = sys.argv[1] if len(sys.argv) > 1 else "all"
    client = McpClient()
    if step in ("tokens", "all"):
        push_tokens(client)
    if step in ("assets", "all"):
        push_child_assets(client)
        push_theme_php(client)
    if step in ("templates", "all"):
        push_templates_and_page(client)
    if step in ("republish", "all"):
        push_templates_refresh(client)
    if step in ("batch2", "all", "republish"):
        push_batch2(client)
    if step in ("legal", "gutenberg"):
        push_gutenberg(client)
    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
