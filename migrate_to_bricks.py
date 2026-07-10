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
MCP_CANDIDATES = [
    ROOT.parent / "wpfy-pvt" / ".cursor" / "mcp.json",
    ROOT.parent / ".cursor" / "mcp.json",
    Path.home() / "Desktop" / "_Projects" / "wpfy-pvt" / ".cursor" / "mcp.json",
]


def _mcp_config_path() -> Path:
    for path in MCP_CANDIDATES:
        if path.is_file():
            return path
    raise FileNotFoundError(f"No MCP config found; tried: {MCP_CANDIDATES}")


MCP_CONFIG = _mcp_config_path()


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
    ("near-black", "#17171c"),
    ("canvas", "#ffffff"),
    ("ink", "#212121"),
    ("deep-green", "#003c33"),
    ("dark-navy", "#071829"),
    ("soft-stone", "#eeece7"),
    ("pale-green", "#edfce9"),
    ("pale-blue", "#f1f5ff"),
    ("hairline", "#d9d9dd"),
    ("muted", "#93939f"),
    ("body-muted", "#616161"),
    ("action-blue", "#1863dc"),
    ("focus-blue", "#4c6ee6"),
    ("coral", "#ff7759"),
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
			return 'WPFY · Docker-first WordPress infrastructure CLI for Ubuntu VPS';
		}
		return $title;
	}
	add_filter( 'pre_get_document_title', 'wpfy_marketing_document_title', 20 );
	function wpfy_marketing_document_title_parts( $parts ) {
		if ( is_front_page() ) {
			$parts['title'] = 'WPFY · Docker-first WordPress infrastructure CLI for Ubuntu VPS';
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
        ("Product", "#why-docker"),
        ("Architecture", "#architecture"),
        ("Commands", "#commands"),
        ("Docs", "https://docs.wpfy.org"),
        ("Forum", "https://forum.wpfy.org"),
        ("GitHub", "https://github.com/wpfyorg/wpfy"),
    ]
    out = [
        el("an0001", "section", 0, ["an0002"], {"tag": "div", "_cssClasses": "announce"}, "Announce"),
        el("an0002", "container", "an0001", ["an0003"], {"_direction": "row", "_justifyContent": "center", "_alignItems": "center"}, "Announce inner"),
        el("an0003", "text-basic", "an0002", [], {
            "text": (
                'WPFY is currently beta/RC software. Test it on a fresh or disposable Ubuntu VPS first. '
                '<a href="https://docs.wpfy.org/releases/v1.0.0-rc1">Read the release notes</a>'
            ),
        }),
        el("hd0001", "section", 0, ["hd0002"], {"tag": "header", "_cssClasses": "site-header"}, "Site header"),
        el("hd0002", "container", "hd0001", ["hd0003", "hd0004", "hd0005", "hd0006"], {
            "_cssClasses": "wrap nav",
            "_direction": "row",
            "_alignItems": "center",
            "_columnGap": "28px",
            "_heightMin": "64px",
        }, "Nav row"),
        el("hd0003", "text-basic", "hd0002", [], {
            "text": 'wpfy<span class="mark">_</span>',
            "tag": "a",
            "link": {"type": "external", "url": "/"},
            "_cssGlobalClasses": ["wpfy-logo"],
        }, "Logo"),
        el("hd0005", "button", "hd0002", [], {
            "text": "Install WPFY",
            "link": {"type": "external", "url": "https://docs.wpfy.org/runbooks/fresh-install", "newTab": True},
            "_cssClasses": "btn btn-primary",
        }, "Install CTA"),
        el("hd0006", "html", "hd0002", [], {
            "html": (
                '<button type="button" class="menu-btn" aria-label="Toggle navigation" aria-expanded="false" aria-controls="nav-links">'
                '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">'
                '<path d="M2 4.5h12M2 8h12M2 11.5h12"/></svg></button>'
            ),
        }, "Mobile menu"),
    ]
    out += nav_ul("hd0004", "hd0002", nav_links, css_id="nav-links")
    return out


PRODUCT_LINKS = [
    ("GitHub", "https://github.com/wpfyorg/wpfy"),
    ("Docs", "https://docs.wpfy.org"),
    ("Forum", "https://forum.wpfy.org"),
    ("Security", "https://docs.wpfy.org/reference/security"),
    ("Releases", "https://docs.wpfy.org/releases/v1.0.0-rc1"),
    ("License", "https://github.com/wpfyorg/wpfy/blob/main/LICENSE"),
]

RESOURCE_LINKS = [
    ("Installation", "https://docs.wpfy.org/runbooks/fresh-install"),
    ("Commands", "https://docs.wpfy.org/commands/run"),
    ("Architecture", "https://docs.wpfy.org/reference/architecture"),
    ("Backup guide", "https://docs.wpfy.org/commands/backup"),
    ("SSL guide", "https://docs.wpfy.org/runbooks/enable-ssl"),
    ("Roadmap", "https://github.com/wpfyorg/wpfy/blob/main/ROADMAP.md"),
]

LEGAL_LINKS = [
    ("Privacy", "/legal/privacy"),
    ("Terms", "/legal/terms"),
    ("Cookies", "/legal/cookies"),
    ("Disclaimer", "/legal/disclaimer"),
    ("Affiliate disclosure", "/legal/affiliate-disclosure"),
    ("Refund / cancellation", "/legal/refund"),
    ("Community terms", "/legal/community"),
    ("Comparison methodology", "/legal/comparison-methodology"),
]


def build_footer_elements() -> list[dict]:
    grid_id = "ft0003"
    c1, c2, c3, c4 = "ftc001", "ftc002", "ftc003", "ftc004"
    out = [
        el("ft0001", "section", 0, ["ft0002"], {"tag": "footer", "_cssClasses": "site-footer"}, "Site footer"),
        el("ft0002", "container", "ft0001", [grid_id, "ft0004"], {
            "_cssClasses": "wrap footer-grid",
        }),
        el(grid_id, "block", "ft0002", [c1, c2, c3, c4], {
            "_cssClasses": "footer-grid",
            "_display": "grid",
            "_gridTemplateColumns": "repeat(4, minmax(0, 1fr))",
            "_gridGap": "32px 40px",
            "_padding": {"bottom": "48px"},
            "_gridTemplateColumns:tablet_portrait": "1fr 1fr",
            "_gridTemplateColumns:mobile_portrait": "1fr",
        }, "Footer grid"),
        el(c1, "block", grid_id, ["ftl001", "ftm001"], {"_rowGap": "14px"}),
        el("ftl001", "text-basic", c1, [], {
            "text": 'wpfy<span class="mark">_</span>',
            "tag": "a",
            "link": {"type": "external", "url": "/"},
            "_cssGlobalClasses": ["wpfy-logo"],
        }, "Logo"),
        el("ftm001", "text-basic", c1, [], {
            "text": (
                "Docker-first WordPress infrastructure CLI for Ubuntu VPS.<br>"
                "Beta / RC software — test on a disposable VPS first.<br>"
                "Open source under AGPL-3.0."
            ),
            "tag": "p",
            "_cssClasses": "footer-meta",
        }),
        el(c2, "block", grid_id, ["ftp001", "ftpl01"], {"_rowGap": "14px"}),
        footer_col_title("ftp001", c2, "Product"),
        el(c3, "block", grid_id, ["ftr001", "ftrl01"], {"_rowGap": "14px"}),
        footer_col_title("ftr001", c3, "Resources"),
        el(c4, "block", grid_id, ["ftl201", "ftll01", "ftcs01"], {"_rowGap": "14px"}),
        footer_col_title("ftl201", c4, "Legal"),
        el("ftcs01", "button", c4, [], {
            "text": "Cookie settings",
            "tag": "button",
            "_cssClasses": "cookie-settings-link",
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
            "_cssClasses": "footer-bar",
        }, "Footer bar"),
    ]
    out += link_list("ftpl01", c2, PRODUCT_LINKS, new_tab=True, item_ids=["ftpr01", "ftpr02", "ftpr03", "ftpr04", "ftpr05", "ftpr06"])
    out += link_list("ftrl01", c3, RESOURCE_LINKS, new_tab=True, item_ids=["ftrs01", "ftrs02", "ftrs03", "ftrs04", "ftrs05", "ftrs06"])
    out += link_list("ftll01", c4, LEGAL_LINKS, item_ids=["ftlg01", "ftlg02", "ftlg03", "ftlg04", "ftlg05", "ftlg06", "ftlg07", "ftlg08"])
    return out


def build_hero_section() -> list[dict]:
    from batch2_sections import extract_hero_section

    return [el("hr0001", "html", 0, [], {"html": extract_hero_section()}, "Hero")]


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


HOME_PAGE_TITLE = "WPFY · Docker-first WordPress infrastructure CLI for Ubuntu VPS"


def push_batch2(client: McpClient, page_id: int | None = None) -> None:
    from batch2_sections import build_batch2_sections

    if page_id is None:
        page_id = resolve_home_page_id(client)
    print(f"→ Redesign sections on page #{page_id}")
    hero = build_hero_section()
    batch2 = build_batch2_sections()
    push_content(client, page_id, hero + batch2)
    client.ability("novamira/update-post", {
        "post_id": page_id,
        "title": HOME_PAGE_TITLE,
    })
    print(f"  + {len(batch2)} section elements ({len(hero + batch2)} total nodes)")
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
