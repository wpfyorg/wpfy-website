/**
 * Compare static site (local) vs Bricks WP staging.
 * Usage: node compare_sites.mjs [localUrl] [wpUrl]
 */
import { chromium } from "playwright";
import { writeFileSync } from "fs";

const LOCAL = process.argv[2] || "http://127.0.0.1:8765/";
const WP = process.argv[3] || "https://wpfy.dev.wpfy.org/";

const SELECTORS = [
  { key: "announce", sel: ".announce, .wpfy-announce" },
  { key: "header", sel: ".site-header, .wpfy-site-header" },
  { key: "hero", sel: ".hero, .wpfy-hero" },
  { key: "marquee", sel: ".marquee, .wpfy-marquee" },
  { key: "problem", sel: "#problem" },
  { key: "stack", sel: "#stack" },
  { key: "features", sel: "#features" },
  { key: "how", sel: "#how-it-works" },
  { key: "who", sel: "#who" },
  { key: "useCases", sel: "#use-cases" },
  { key: "beta", sel: "#beta" },
  { key: "subscribe", sel: "#subscribe" },
  { key: "footer", sel: ".site-footer, .wpfy-site-footer" },
];

const STYLE_PROBES = [
  { key: "bodyBg", sel: "body", prop: "backgroundColor" },
  { key: "bodyFont", sel: "body", prop: "fontFamily" },
  { key: "bodySize", sel: "body", prop: "fontSize" },
  { key: "h1Size", sel: "#hero-title", prop: "fontSize" },
  { key: "h1Family", sel: "#hero-title", prop: "fontFamily" },
  { key: "btnBg", sel: ".btn-blue, .wpfy-btn-blue", prop: "backgroundColor" },
  { key: "marqueeBg", sel: ".marquee-yellow, .wpfy-marquee-yellow", prop: "backgroundColor" },
  { key: "marqueeBorder", sel: ".marquee, .wpfy-marquee", prop: "borderTopWidth" },
  { key: "sectionSky", sel: "#problem, #features, #who, .wpfy-section-sky", prop: "backgroundColor" },
  { key: "ctaBg", sel: "#beta, .wpfy-cta-band", prop: "backgroundColor" },
  { key: "subBg", sel: "#subscribe, .wpfy-subscribe-band", prop: "backgroundColor" },
  { key: "wrapMax", sel: ".wrap, .wpfy-wrap", prop: "maxWidth" },
  { key: "headerH", sel: ".nav, .wpfy-nav, .wpfy-site-header .wpfy-wrap", prop: "height" },
  { key: "cardBorder", sel: ".card, .wpfy-card", prop: "borderWidth" },
  { key: "tagBg", sel: ".tag-yellow, .wpfy-tag-yellow", prop: "backgroundColor" },
  { key: "codeWellBg", sel: ".code-well, .wpfy-code-well", prop: "backgroundColor" },
  { key: "footerBg", sel: ".site-footer, .wpfy-site-footer", prop: "backgroundColor" },
  { key: "gridCols", sel: ".grid-4, .wpfy-grid-4", prop: "gridTemplateColumns" },
];

const TEXT_CHECKS = [
  { key: "heroTitle", sel: "#hero-title" },
  { key: "problemH2", sel: "#problem-title" },
  { key: "stackH2", sel: "#stack-title, #stack h2" },
  { key: "featuresH2", sel: "#features-title, #features h2" },
  { key: "betaH2", sel: "#beta-title" },
  { key: "subH2", sel: "#sub-title" },
];

async function audit(page, label) {
  return page.evaluate(
    ({ SELECTORS, STYLE_PROBES, TEXT_CHECKS }) => {
      const norm = (s) => (s || "").replace(/\s+/g, " ").trim();
      const first = (sel) => {
        for (const part of sel.split(",")) {
          const el = document.querySelector(part.trim());
          if (el) return el;
        }
        return null;
      };

      const sections = {};
      for (const { key, sel } of SELECTORS) {
        const el = document.querySelector(sel);
        sections[key] = {
          found: !!el,
          textLen: el ? norm(el.innerText).length : 0,
          childCount: el ? el.children.length : 0,
        };
      }

      const styles = {};
      for (const { key, sel, prop } of STYLE_PROBES) {
        const el = first(sel);
        styles[key] = el ? getComputedStyle(el)[prop] : null;
      }

      const texts = {};
      for (const { key, sel } of TEXT_CHECKS) {
        const el = document.querySelector(sel);
        texts[key] = el ? norm(el.textContent) : null;
      }

      const counts = {
        featureCards: document.querySelectorAll("#features .wpfy-card, #features .card").length,
        compareCards: document.querySelectorAll(".compare-card, .wpfy-compare-card").length,
        whoCards: document.querySelectorAll(".who-card, .wpfy-who-card").length,
        stepCards: document.querySelectorAll(".step-card, .wpfy-step-card").length,
        ecoBoxes: document.querySelectorAll(".eco-box, .wpfy-eco-box").length,
        edgeDoodles: document.querySelectorAll(".edge-doodle, .wpfy-edge-doodle").length,
        drifts: document.querySelectorAll(".drift, .wpfy-drift").length,
        heroDoodles: document.querySelectorAll(".doodle, .wpfy-doodle, .bubble, .wpfy-bubble").length,
        navLinks: document.querySelectorAll(".nav-links a, .wpfy-nav-links a").length,
        footerCols: document.querySelectorAll(
          ".site-footer .col, .site-footer .wpfy-footer-col, .wpfy-site-footer .wpfy-footer-col"
        ).length,
      };

      return { sections, styles, texts, counts, title: document.title };
    },
    { SELECTORS, STYLE_PROBES, TEXT_CHECKS }
  );
}

function diffObjects(a, b, path = "") {
  const diffs = [];
  const keys = new Set([...Object.keys(a || {}), ...Object.keys(b || {})]);
  for (const k of keys) {
    const p = path ? `${path}.${k}` : k;
    const va = a?.[k];
    const vb = b?.[k];
    if (va && typeof va === "object" && !Array.isArray(va) && vb && typeof vb === "object") {
      diffs.push(...diffObjects(va, vb, p));
    } else if (JSON.stringify(va) !== JSON.stringify(vb)) {
      diffs.push({ path: p, local: va, wp: vb });
    }
  }
  return diffs;
}

const browser = await chromium.launch();
const viewports = [
  { name: "desktop", width: 1440, height: 900 },
  { name: "tablet", width: 768, height: 1024 },
  { name: "mobile", width: 390, height: 844 },
];

const report = { local: LOCAL, wp: WP, viewports: {} };

for (const vp of viewports) {
  const localPage = await browser.newPage({ viewport: { width: vp.width, height: vp.height } });
  const wpPage = await browser.newPage({ viewport: { width: vp.width, height: vp.height } });
  await localPage.goto(LOCAL, { waitUntil: "networkidle", timeout: 60000 });
  await wpPage.goto(WP, { waitUntil: "networkidle", timeout: 60000 });
  await localPage.waitForTimeout(1500);
  await wpPage.waitForTimeout(1500);

  const primePage = async (page) => {
    await page.evaluate(async () => {
      document.querySelectorAll(".bricks-lazy-hidden").forEach((el) => {
        el.classList.remove("bricks-lazy-hidden");
        el.classList.add("bricks-lazy-loaded");
      });
      document.querySelectorAll(".wpfy-reveal").forEach((el) => el.classList.add("in"));
      const step = window.innerHeight * 0.85;
      let y = 0;
      while (y < document.body.scrollHeight) {
        window.scrollTo(0, y);
        y += step;
        await new Promise((r) => setTimeout(r, 80));
      }
      window.scrollTo(0, 0);
    });
    await page.waitForTimeout(800);
  };

  await primePage(localPage);
  await primePage(wpPage);

  const localData = await audit(localPage, "local");
  const wpData = await audit(wpPage, "wp");
  const diffs = diffObjects(localData, wpData);

  await localPage.screenshot({ path: `/tmp/compare-${vp.name}-local.png`, fullPage: true });
  await wpPage.screenshot({ path: `/tmp/compare-${vp.name}-wp.png`, fullPage: true });

  report.viewports[vp.name] = { local: localData, wp: wpData, diffs };
  await localPage.close();
  await wpPage.close();
}

await browser.close();

writeFileSync("/tmp/compare-report.json", JSON.stringify(report, null, 2));

const desktopDiffs = report.viewports.desktop.diffs;
console.log(`\n=== DESKTOP DIFFS (${desktopDiffs.length}) ===`);
for (const d of desktopDiffs.slice(0, 80)) {
  console.log(`${d.path}: LOCAL=${JSON.stringify(d.local)} | WP=${JSON.stringify(d.wp)}`);
}
if (desktopDiffs.length > 80) console.log(`... +${desktopDiffs.length - 80} more`);
