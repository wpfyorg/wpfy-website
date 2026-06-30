#!/usr/bin/env python3
"""Generate static legal pages under website/legal/ with shared chrome."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent
LEGAL_DIR = ROOT / "legal"
LAST_UPDATED = "June 22, 2026"
CSS_V = "8"
JS_V = "7"

LEGAL_NAV = [
    ("Privacy Policy", "privacy"),
    ("Terms of Service", "terms"),
    ("Cookie Policy", "cookies"),
    ("Affiliate Disclosure", "affiliate-disclosure"),
    ("Disclaimer", "disclaimer"),
    ("Services Terms", "services-terms"),
    ("Refund Policy", "refund"),
    ("Comparison Methodology", "comparison-methodology"),
    ("Community Guidelines", "community"),
    ("DMCA Policy", "dmca"),
]

FOOTER_LINKS = """
    <ul class="footer-links">
      <li><a href="https://github.com/wpfyorg/wpfy">GitHub</a></li>
      <li><a href="https://forum.wpfy.org">Forum</a></li>
      <li><a href="https://docs.wpfy.org">Docs</a></li>
      <li><a href="https://github.com/wpfyorg/wpfy/blob/main/docs/SECURITY.md">Security</a></li>
      <li><a href="https://github.com/wpfyorg/wpfy/blob/main/LICENSE">License (AGPL-3.0)</a></li>
    </ul>
    <ul class="footer-links footer-legal">
      <li><a href="/legal/privacy">Privacy</a></li>
      <li><a href="/legal/terms">Terms</a></li>
      <li><a href="/legal/cookies">Cookies</a></li>
      <li><a href="/legal/affiliate-disclosure">Affiliate</a></li>
      <li><a href="/legal/disclaimer">Disclaimer</a></li>
      <li><a href="/legal/refund">Refund</a></li>
      <li><a href="/legal/community">Community</a></li>
    </ul>"""


def legal_breadcrumbs_html(title: str) -> str:
    return (
        '<nav class="legal-breadcrumbs" aria-label="Breadcrumb">'
        '<a href="/">Home</a>'
        '<span class="legal-breadcrumbs-sep" aria-hidden="true">/</span>'
        '<a href="/legal/privacy/">Legal</a>'
        f'<span class="legal-breadcrumbs-sep" aria-hidden="true">/</span>'
        f'<span aria-current="page">{title}</span>'
        "</nav>"
    )


def shell(title: str, slug: str, body: str) -> str:
    nav_items = "\n".join(
        f'      <li><a href="/legal/{s}"{" aria-current=\"page\"" if s == slug else ""}>{label}</a></li>'
        for label, s in LEGAL_NAV
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} · WPFY</title>
<meta name="description" content="{title} for wpfy.org. Docker-first WordPress server management.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/styles.css?v={CSS_V}">
</head>
<body>

<header class="site-header legal-header">
  <div class="wrap nav">
    <a class="logo" href="/" aria-label="WPFY home">wpfy<span class="mark">_</span></a>
    <a class="btn legal-back" href="/">← Back to home</a>
  </div>
</header>

<main class="legal-doc">
  <div class="wrap legal-layout">
    <article class="legal-article">
      {legal_breadcrumbs_html(title)}
      <h1>{title}</h1>
      <p class="legal-meta">Last updated: {LAST_UPDATED}</p>
{body}
    </article>
    <nav class="legal-nav" aria-label="Legal pages">
      <p class="legal-nav-title">Legal</p>
      <ul>
{nav_items}
      </ul>
    </nav>
  </div>
</main>

<footer class="site-footer">
  <div class="wrap footer-inner">
    <div>
      <a class="logo" href="/" aria-label="WPFY home">wpfy<span class="mark">_</span></a>
      <p class="footer-meta">Docker-first WordPress server management for Ubuntu VPS.<br>Beta software, test on a fresh VPS first.<br>Licensed under AGPL-3.0.</p>
    </div>
    <div class="footer-link-groups">
{FOOTER_LINKS}
    </div>
  </div>
</footer>

<script src="/assets/main.js?v={JS_V}" defer></script>
</body>
</html>
"""


PAGES: dict[str, tuple[str, str]] = {
    "privacy": (
        "Privacy Policy",
        """
      <p class="legal-lede">This policy explains how WPFY (“we”, “us”) collects, uses, and shares personal data when you use wpfy.org, docs.wpfy.org, forum.wpfy.org, our open-source software, email list, support channels, and paid services.</p>
      <p class="legal-note"><strong>Not legal advice.</strong> Update the legal entity name and registered address below before monetization launch.</p>

      <h2>1. Who we are</h2>
      <p>Data controller: <strong>WPFY</strong> (operating wpfy.org). Contact: <a href="mailto:privacy@wpfy.org">privacy@wpfy.org</a>.</p>
      <p>Registered address: <em>[Add legal entity name and registered address before launch]</em></p>

      <h2>2. Data we collect</h2>
      <ul>
        <li><strong>Account and contact data</strong>: name, email, billing contact details when you subscribe, buy support, or open a ticket.</li>
        <li><strong>Technical data</strong>: IP address, browser type, device identifiers, pages visited, referral URLs, and server logs.</li>
        <li><strong>Cookie and analytics data</strong>: see our <a href="/legal/cookies">Cookie Policy</a>.</li>
        <li><strong>Payment metadata</strong>: transaction IDs and billing status from our payment processor (we do not store full card numbers).</li>
        <li><strong>Support data</strong>: messages, screenshots, SSH session notes, and logs you share for premium support (may include server configuration and site content).</li>
        <li><strong>Forum data</strong>: posts, profile information, and moderation records on forum.wpfy.org.</li>
      </ul>
      <p>We do not intentionally collect data from children under 16.</p>

      <h2>3. How we use data</h2>
      <ul>
        <li>Provide, operate, and improve the website, documentation, forum, and software.</li>
        <li>Send release notes and marketing emails when you opt in (you may unsubscribe anytime).</li>
        <li>Deliver paid support and respond to inquiries.</li>
        <li>Process payments and prevent fraud.</li>
        <li>Measure traffic and site performance (with consent where required).</li>
        <li>Comply with law and enforce our <a href="/legal/terms">Terms of Service</a>.</li>
      </ul>

      <h2>4. Legal bases (EEA/UK)</h2>
      <p>Where GDPR applies, we rely on: <strong>contract</strong> (support and purchases), <strong>consent</strong> (non-essential cookies, marketing email), <strong>legitimate interests</strong> (security, analytics, product improvement), and <strong>legal obligation</strong>.</p>

      <h2>5. Sharing and subprocessors</h2>
      <p>We use service providers who process data on our behalf, such as:</p>
      <ul>
        <li>Hosting and CDN providers</li>
        <li>Email delivery (newsletter and transactional)</li>
        <li>Payment processors (e.g. Stripe or PayPal; update when selected)</li>
        <li>Analytics (only after cookie consent where required)</li>
        <li>Forum platform hosting</li>
      </ul>
      <p>We may disclose data if required by law or to protect rights, safety, and security. We do not sell personal data.</p>

      <h2>6. International transfers</h2>
      <p>We may process data in countries outside your own. Where required, we use appropriate safeguards such as Standard Contractual Clauses.</p>

      <h2>7. Retention</h2>
      <p>We keep data only as long as needed for the purposes above: active accounts and support records while the relationship continues; marketing data until you unsubscribe; logs and analytics per provider defaults; legal records as required by tax and compliance rules.</p>

      <h2>8. Your rights</h2>
      <p>Depending on your location, you may have rights to access, correct, delete, restrict, object, or port your data, and to withdraw consent. California residents may have rights under CCPA/CPRA including opt-out of certain sharing (we do not sell personal information).</p>
      <p>Contact <a href="mailto:privacy@wpfy.org">privacy@wpfy.org</a>. You may lodge a complaint with your local data protection authority.</p>

      <h2>9. Security</h2>
      <p>We use reasonable technical and organizational measures. No method of transmission or storage is 100% secure. See our <a href="https://github.com/wpfyorg/wpfy/blob/main/docs/SECURITY.md">security documentation</a>.</p>

      <h2>10. Changes</h2>
      <p>We may update this policy. Material changes will be posted here with a new “Last updated” date.</p>
""",
    ),
    "cookies": (
        "Cookie Policy",
        """
      <p class="legal-lede">This policy describes how wpfy.org uses cookies and similar technologies. It should be read with our <a href="/legal/privacy">Privacy Policy</a>.</p>

      <h2>1. What are cookies?</h2>
      <p>Cookies are small text files stored on your device. Similar technologies include local storage and pixels.</p>

      <h2>2. Categories we use</h2>
      <h3>Strictly necessary</h3>
      <p>Required for basic site function, security, and remembering your cookie consent choice. These do not require consent in the EU.</p>
      <h3>Analytics (optional)</h3>
      <p>Help us understand traffic and improve the site (e.g. privacy-focused analytics). Loaded only if you accept analytics cookies.</p>
      <h3>Marketing and affiliate (optional)</h3>
      <p>May be set by affiliate partners or advertising tools to attribute referrals. Loaded only if you accept marketing cookies.</p>

      <h2>3. Cookie consent</h2>
      <p>On your first visit, we show a banner letting you accept all, reject non-essential, or customize choices. Non-essential scripts are blocked until you consent. You can change your choice anytime by clearing site data or using the “Cookie settings” control in the site footer (when available).</p>

      <h2>4. Third-party cookies</h2>
      <p>Third parties may set cookies when you follow affiliate links or use embedded content. Their use is governed by their own policies. We document major tools here as we adopt them:</p>
      <ul>
        <li><strong>wpfy_cookie_consent</strong>: stores your banner choice (necessary, first-party)</li>
        <li><em>[Analytics provider: add name and policy URL when enabled]</em></li>
        <li><em>[Affiliate networks: add when partnerships are live]</em></li>
      </ul>

      <h2>5. Browser controls</h2>
      <p>You can block or delete cookies in your browser settings. Blocking necessary cookies may affect site functionality.</p>

      <h2>6. Contact</h2>
      <p>Questions: <a href="mailto:privacy@wpfy.org">privacy@wpfy.org</a>.</p>
""",
    ),
    "terms": (
        "Terms of Service",
        """
      <p class="legal-lede">These Terms govern your use of wpfy.org, related subdomains, the WPFY open-source software, the community forum, and any services we offer. By using our properties, you agree to these Terms.</p>

      <h2>1. Beta software</h2>
      <p>WPFY is <strong>beta software</strong>. Test on a fresh Ubuntu VPS before production use. The CLI is provided under the <a href="https://github.com/wpfyorg/wpfy/blob/main/LICENSE">AGPL-3.0 license</a> without warranty. Paid support is governed separately by our <a href="/legal/services-terms">Services Terms</a>.</p>

      <h2>2. Eligibility</h2>
      <p>You must be able to form a binding contract and comply with applicable laws. You are responsible for your account credentials and activity under your account.</p>

      <h2>3. Acceptable use</h2>
      <p>You may not use our services to:</p>
      <ul>
        <li>Violate laws or third-party rights</li>
        <li>Distribute malware, spam, or abusive content</li>
        <li>Probe or attack systems without authorization</li>
        <li>Share others’ credentials or private server data without permission</li>
        <li>Misrepresent affiliation with WPFY or impersonate others</li>
      </ul>
      <p>Forum-specific rules are in our <a href="/legal/community">Community Guidelines</a>.</p>

      <h2>4. Intellectual property</h2>
      <p>Site content, branding, and documentation are owned by WPFY or licensors. Open-source code is licensed under AGPL-3.0. You retain ownership of content you submit; you grant us a license to host and display it on our platforms.</p>

      <h2>5. Third-party services and links</h2>
      <p>We link to VPS providers, GitHub, and other third parties. We are not responsible for their services. Affiliate relationships are disclosed in our <a href="/legal/affiliate-disclosure">Affiliate Disclosure</a>.</p>

      <h2>6. Disclaimers</h2>
      <p>Services and content are provided <strong>“as is”</strong> without warranties of any kind, including merchantability, fitness for a particular purpose, or non-infringement. See also our <a href="/legal/disclaimer">Disclaimer</a>.</p>

      <h2>7. Limitation of liability</h2>
      <p>To the maximum extent permitted by law, WPFY and its contributors are not liable for indirect, incidental, special, consequential, or punitive damages, or for loss of data, revenue, or profits arising from use of the software or site. Our total liability for paid services is limited to the amount you paid for the specific service giving rise to the claim in the twelve months before the event.</p>

      <h2>8. Indemnification</h2>
      <p>You agree to indemnify WPFY against claims arising from your misuse of the services, your content, or violation of these Terms.</p>

      <h2>9. Termination</h2>
      <p>We may suspend or terminate access for violation of these Terms or for operational reasons. You may stop using our services at any time.</p>

      <h2>10. Governing law</h2>
      <p><em>[Specify governing law and venue before launch (e.g. laws of [jurisdiction], courts of [venue]).]</em></p>

      <h2>11. Changes</h2>
      <p>We may update these Terms. Continued use after the effective date constitutes acceptance of material changes.</p>

      <h2>12. Contact</h2>
      <p><a href="mailto:legal@wpfy.org">legal@wpfy.org</a></p>
""",
    ),
    "affiliate-disclosure": (
        "Affiliate Disclosure",
        """
      <p class="legal-lede">WPFY is reader-supported. Some pages on wpfy.org, especially VPS comparisons and hosting recommendations, may include affiliate links.</p>

      <h2>What this means</h2>
      <ul>
        <li>If you click a link and sign up or purchase, we may earn a commission.</li>
        <li>This does not increase the price you pay.</li>
        <li>Commissions help fund documentation, development, and site operations.</li>
      </ul>

      <h2>Editorial independence</h2>
      <p>Affiliate relationships do not dictate our rankings or opinions. We document how we evaluate providers in our <a href="/legal/comparison-methodology">Comparison Methodology</a>. Where a link is affiliate, we label it on the page.</p>

      <h2>FTC disclosure</h2>
      <p>We comply with applicable endorsement and affiliate disclosure rules, including clear and conspicuous disclosure near affiliate content, not only in this footer policy.</p>

      <h2>Questions</h2>
      <p><a href="mailto:legal@wpfy.org">legal@wpfy.org</a></p>
""",
    ),
    "disclaimer": (
        "Disclaimer",
        """
      <p class="legal-lede">Information on wpfy.org is for general informational purposes. It is not professional advice.</p>

      <h2>Software and infrastructure</h2>
      <p>WPFY is beta open-source software for Docker-based WordPress hosting on Ubuntu VPS. You are responsible for backups, security hardening, compliance, and production readiness. We do not guarantee uptime, security, or fitness for any particular workload.</p>

      <h2>Comparisons and reviews</h2>
      <p>VPS comparisons reflect our research and opinion at the time of writing. Pricing, features, and availability change. We do not warrant accuracy or completeness. See <a href="/legal/comparison-methodology">Comparison Methodology</a>.</p>

      <h2>No endorsement</h2>
      <p>References to third-party products (WordPress, Docker, hosting providers, etc.) do not imply endorsement. Trademarks belong to their respective owners.</p>

      <h2>Professional advice</h2>
      <p>Nothing here is legal, tax, security audit, or financial advice. Consult qualified professionals for decisions affecting your business or compliance obligations.</p>

      <h2>Contact</h2>
      <p><a href="mailto:legal@wpfy.org">legal@wpfy.org</a></p>
""",
    ),
    "services-terms": (
        "Services &amp; Support Terms",
        """
      <p class="legal-lede">These terms apply to one-time and project-based premium support, consulting, and related paid services sold by WPFY. They supplement our <a href="/legal/terms">Terms of Service</a>. The open-source WPFY CLI remains under AGPL-3.0; these terms govern the <strong>service relationship</strong>, not the software license.</p>

      <h2>1. Scope of services</h2>
      <p>Each engagement is defined in a written quote, invoice, or statement of work (SOW) specifying deliverables, estimated hours, and price. Services may include installation help, migration assistance, debugging, configuration review, and training, only as explicitly listed.</p>

      <h2>2. What is not included</h2>
      <ul>
        <li>24/7 monitoring or guaranteed uptime unless explicitly agreed in writing</li>
        <li>Unlimited future support after the engagement ends</li>
        <li>Third-party hosting, domain, or license fees</li>
        <li>Custom feature development unless scoped in the SOW</li>
        <li>Warranty of production readiness for beta software beyond agreed deliverables</li>
      </ul>

      <h2>3. Customer responsibilities</h2>
      <ul>
        <li>Provide timely SSH, DNS, or panel access as needed</li>
        <li>Maintain backups before destructive changes</li>
        <li>Disclose relevant production constraints and compliance requirements</li>
        <li>Not share credentials in public forum posts</li>
      </ul>

      <h2>4. Response times</h2>
      <p>We target reasonable response times during business hours unless a binding SLA is purchased separately. Response targets are goals, not guarantees, unless stated in your SOW.</p>

      <h2>5. Confidentiality</h2>
      <p>We treat non-public server details and business information as confidential. You should not share secrets in plaintext email; use secure channels when offered.</p>

      <h2>6. Data processing</h2>
      <p>Support may require access to systems containing personal data. EU/UK business customers may request a Data Processing Agreement (DPA). Contact <a href="mailto:privacy@wpfy.org">privacy@wpfy.org</a>.</p>

      <h2>7. Limitation of liability</h2>
      <p>Our liability for paid services is limited as described in the <a href="/legal/terms">Terms of Service</a>. You acknowledge infrastructure work carries inherent risk; maintain backups and rollback plans.</p>

      <h2>8. Force majeure</h2>
      <p>We are not liable for delays caused by events outside reasonable control (provider outages, network failures, natural disasters, etc.).</p>

      <h2>9. Contact</h2>
      <p><a href="mailto:support@wpfy.org">support@wpfy.org</a></p>
""",
    ),
    "refund": (
        "Refund &amp; Cancellation Policy",
        """
      <p class="legal-lede">This policy applies to one-time invoices and project-based premium support purchased from WPFY. Subscription products, if introduced later, will have separate terms.</p>

      <h2>1. Before work begins</h2>
      <p>If you cancel before we start billable work, you may receive a full refund minus payment processor fees, at our discretion.</p>

      <h2>2. After work begins</h2>
      <p>Refunds are generally <strong>not available</strong> for completed deliverables or hours already worked. For partial engagements, unused prepaid hours may be refunded within <strong>14 days</strong> of payment if no substantial work has been performed.</p>

      <h2>3. Non-refundable items</h2>
      <ul>
        <li>Third-party costs (hosting, domains, licenses) already incurred on your behalf</li>
        <li>Completed milestones defined in your SOW</li>
        <li>Chargebacks filed without contacting us first</li>
      </ul>

      <h2>4. How to request a refund</h2>
      <p>Email <a href="mailto:support@wpfy.org">support@wpfy.org</a> with your invoice number and reason. We respond within 5 business days. Approved refunds return to the original payment method within 10 business days.</p>

      <h2>5. Disputes</h2>
      <p>Contact us before initiating a payment dispute so we can resolve the issue directly.</p>
""",
    ),
    "comparison-methodology": (
        "Comparison Methodology",
        """
      <aside class="wpfy-affiliate-banner" role="note" aria-label="Affiliate disclosure">
        <p><strong>Disclosure:</strong> Comparison pages may include affiliate links. WPFY may earn a commission at no extra cost to you. <a href="/legal/affiliate-disclosure">Full affiliate disclosure</a></p>
      </aside>

      <p class="legal-lede">How we research, rank, and update VPS and hosting comparisons on wpfy.org.</p>

      <h2>1. Goals</h2>
      <p>Help WordPress operators on Ubuntu VPS choose infrastructure that fits isolation, performance, and budget needs, especially when using WPFY’s Docker-first stack.</p>

      <h2>2. Providers we include</h2>
      <p>We prioritize providers that support Ubuntu VPS, reasonable pricing for solo developers and agencies, clear networking (IPv4/IPv6), and reputations for reliability. We may exclude providers with repeated billing or support complaints unless reviewing them specifically.</p>

      <h2>3. Criteria</h2>
      <ul>
        <li><strong>Pricing</strong>: entry plans, renewal pricing, bandwidth and snapshot costs</li>
        <li><strong>Performance</strong>: CPU/RAM tiers, storage type, geographic regions</li>
        <li><strong>WordPress fit</strong>: Docker compatibility, firewall control, backup options</li>
        <li><strong>Support &amp; docs</strong>: quality of provider documentation and ticket response</li>
        <li><strong>Policy</strong>: acceptable use, outbound mail, and resource limits</li>
      </ul>

      <h2>4. Affiliate relationships</h2>
      <p>Some listed providers have affiliate programs. Affiliate status does not guarantee placement or a higher score. We label affiliate links and publish our <a href="/legal/affiliate-disclosure">Affiliate Disclosure</a>.</p>

      <h2>5. Updates</h2>
      <p>We review comparisons periodically and after major provider changes. Each page shows a “Last reviewed” date when published on the marketing site.</p>

      <h2>6. Corrections</h2>
      <p>Found outdated pricing or specs? Email <a href="mailto:legal@wpfy.org">legal@wpfy.org</a> or open a thread on <a href="https://forum.wpfy.org">forum.wpfy.org</a>.</p>
""",
    ),
    "community": (
        "Community Guidelines",
        """
      <p class="legal-lede">These guidelines apply to forum.wpfy.org and other WPFY community spaces. They supplement our <a href="/legal/terms">Terms of Service</a>.</p>

      <h2>1. Be respectful</h2>
      <p>Debate ideas, not people. No harassment, hate speech, slurs, or personal attacks.</p>

      <h2>2. Stay on topic</h2>
      <p>Post in the right category. WordPress, Docker, Ubuntu VPS, and WPFY operations are welcome. Pure spam or unrelated ads are not.</p>

      <h2>3. No secrets in public</h2>
      <p>Never post passwords, API keys, private keys, or full <code>.env</code> files. Redact domains and IPs when possible in public threads.</p>

      <h2>4. No malicious content</h2>
      <p>Do not share exploits, pirated software, or instructions for unauthorized access.</p>

      <h2>5. Commercial posts</h2>
      <p>Disclose affiliation when recommending products. Excessive self-promotion may be removed. Affiliate links must follow our <a href="/legal/affiliate-disclosure">Affiliate Disclosure</a> spirit. Be transparent.</p>

      <h2>6. Moderation</h2>
      <p>Moderators may edit, lock, or remove posts and suspend accounts that violate these rules. Appeals: <a href="mailto:legal@wpfy.org">legal@wpfy.org</a>.</p>

      <h2>7. Acceptable use</h2>
      <p>Prohibited uses of community and support channels include scanning third-party servers without permission, distributing malware, and using the forum to coordinate abuse. See also our <a href="/legal/terms">Terms of Service</a> acceptable use section.</p>
""",
    ),
    "dmca": (
        "DMCA &amp; Copyright Policy",
        """
      <p class="legal-lede">WPFY respects intellectual property rights. This policy describes how copyright holders can request removal of infringing material on properties we operate, including forum.wpfy.org.</p>

      <h2>1. Designated agent</h2>
      <p><em>[Add DMCA agent name and postal address before US launch if required.]</em><br>Email: <a href="mailto:legal@wpfy.org">legal@wpfy.org</a></p>

      <h2>2. Takedown notice</h2>
      <p>Send a notice including:</p>
      <ul>
        <li>Identification of the copyrighted work</li>
        <li>URL or location of the allegedly infringing material</li>
        <li>Your contact information</li>
        <li>A statement of good-faith belief that use is not authorized</li>
        <li>A statement, under penalty of perjury, that the information is accurate and you are authorized to act</li>
        <li>Your physical or electronic signature</li>
      </ul>

      <h2>3. Counter-notification</h2>
      <p>If you believe content was removed in error, you may submit a counter-notification with the information required under 17 U.S.C. § 512(g). We may restore material after the statutory period unless the complainant files suit.</p>

      <h2>4. Repeat infringers</h2>
      <p>We may terminate accounts of repeat infringers in appropriate circumstances.</p>
""",
    ),
}


def main() -> None:
    LEGAL_DIR.mkdir(parents=True, exist_ok=True)
    for slug, (title, body) in PAGES.items():
        page_dir = LEGAL_DIR / slug
        page_dir.mkdir(parents=True, exist_ok=True)
        path = page_dir / "index.html"
        path.write_text(shell(title, slug, body), encoding="utf-8")
        print(f"  wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
