# WPFY Product-Truth Audit

**Date:** 2026-07-10  
**Sources:** `wpfy-pvt`, `wpfy-docs`, `wpfy-website`  
**Backup:** `backups/20260710-creative-build/`

## Release status

| Field | Value |
|-------|-------|
| Marketing string | Beta / RC — v1.0.0-rc1 (planned). Validate on disposable Ubuntu VPS before production. |
| Package version | `1.0.0` in `wpfy-pvt/pyproject.toml` (no `-rc1` suffix) |
| Docs label | Planned release candidate |

## Truth sheet (summary)

| Claim | Category |
|-------|----------|
| Docker-first WordPress VPS CLI | Implemented |
| Open-source AGPL-3.0 | Implemented |
| Per-site Docker Compose stacks | Implemented |
| No host Nginx/PHP/MariaDB/Redis packages | Implemented |
| Per-site PHP 7.4–8.4 (default 8.4) | Implemented |
| Isolation reduces cross-site blast radius | Implemented (qualified) |
| Absolute isolation guarantee | Unsafe claim |
| Independent security audit | Deferred |
| Shared Traefik + Let's Encrypt | Implemented |
| SSL DNS/IP preflight | Implemented |
| Wildcard SSL | Limited — Cloudflare DNS only |
| Flat CLI primary (`run`, `backup`, `restore`, …) | Implemented |
| `wpfy stack install` before sites | Implemented |
| Backups files + verified SQL | Implemented |
| S3-compatible remote backup | Implemented |
| Scheduled backup timer | Implemented |
| Edge/ACME backup + restore | Implemented |
| `restore --latest` only when explicit | Implemented |
| Provider bucket lifecycle APIs | Deferred |
| `wpfy debug` / healthcheck / motd / utility | Implemented |
| `wpfy stack migrate` | Deferred |
| phpMyAdmin/Adminer/Composer helpers | Limited — pull-only |
| MySQLTuner | Deferred |
| Host hardening (ufw/fail2ban/netdata) | Deferred |
| Panel / API / UI | Deferred |
| Ubuntu-first 22.04/24.04 | Limited |
| Multi-tenant untrusted hosting | Out of scope |
| Mutable `main` install | Limited — prefer pin |

## Verified command surface (homepage-safe)

```bash
curl -fsSL https://raw.githubusercontent.com/wpfyorg/wpfy/main/install.sh | sudo bash
# Prefer: review install.sh; pin WPFY_REF + WPFY_SOURCE_SHA256

wpfy stack install --nginx --php --mysql
wpfy run example.com --wp
wpfy run example.com --wp -le
wpfy site ssl example.com --letsencrypt
wpfy site status example.com
wpfy debug

wpfy backup example.com
wpfy backup prune example.com --keep 7
wpfy backup schedule daily --time 02:30 --s3
wpfy restore example.com --latest
wpfy backup edge

wpfy healthcheck all
wpfy debug example.com
wpfy log show example.com --nginx -f
wpfy secure example.com

printf '%s\n' '<token>' | wpfy dns cloudflare set --token-stdin
wpfy site ssl example.com --letsencrypt wildcard --dns cloudflare
```

## Hard boundaries (must publish)

1. Beta/RC — disposable Ubuntu VPS first
2. No independent security audit
3. Multi-tenant untrusted hosting out of scope
4. Ubuntu-first; other distros untested
5. Mutable `main` install — review or pin
6. `wpfy stack migrate` not implemented
7. Wildcard SSL = Cloudflare DNS only
8. Helper images pull-only (no public dashboards)
9. MySQLTuner unavailable
10. Remote prune = WPFY-managed, not provider lifecycle APIs
11. `restore --latest` only when requested
12. Destructive commands: non-interactive `rm`/`site delete` skip prompts; `stack purge` has no confirmation
13. Host hardening is operator responsibility
14. Keep off-server backup copies
15. AGPL-3.0 network-service source obligations

## File ownership

| Role | Path |
|------|------|
| Static source | `index.html`, `assets/styles.css`, `assets/main.js` |
| Child theme | `bricks-child-assets/` |
| Generators | `migrate_to_bricks.py`, `batch2_sections.py`, `bricks_*.py` |
| QA | `compare_sites.mjs`, `strict_audit.mjs` |
| Bricks IDs | Header 9, Footer 10, Home 11 |

## Image API

| Item | Status |
|------|--------|
| Key in `.env` | Present (not committed) |
| Model in `.env` | Present |
| Decision | Prefer CSS/SVG stack graphics; generate only if concept needs atmosphere |
