/**
 * Compare static site (local) vs Bricks WP staging.
 * Usage: node compare_sites.mjs [localUrl] [wpUrl]
 */
import { chromium } from "playwright";
import { writeFileSync } from "fs";

const LOCAL = process.argv[2] || "http://127.0.0.1:8766/";
const WP = process.argv[3] || "https://wpfy.dev.wpfy.org/";

const SELECTORS = [
  { key: "announce", sel: ".announce" },
  { key: "header", sel: ".site-header" },
  { key: "hero", sel: ".hero" },
  { key: "tech", sel: "#tech" },
  { key: "whyDocker", sel: "#why-docker" },
  { key: "architecture", sel: "#architecture" },
  { key: "commands", sel: "#commands" },
  { key: "capabilities", sel: "#capabilities" },
  { key: "quickStart", sel: "#quick-start" },
  { key: "users", sel: "#users" },
  { key: "boundaries", sel: "#boundaries" },
  { key: "cta", sel: "#cta" },
  { key: "updates", sel: "#updates" },
  { key: "footer", sel: ".site-footer" },
];

const STYLE_PROBES = [
  { key: "bodyBg", sel: "body", prop: "backgroundColor" },
  { key: "bodyFont", sel: "body", prop: "fontFamily" },
  { key: "h1Size", sel: "#hero-title", prop: "fontSize" },
  { key: "h1Family", sel: "#hero-title", prop: "fontFamily" },
  { key: "btnPrimaryBg", sel: ".btn-primary, .btn-blue", prop: "backgroundColor" },
  { key: "announceBg", sel: ".announce", prop: "backgroundColor" },
  { key: "sectionStone", sel: "#why-docker, .section-stone", prop: "backgroundColor" },
  { key: "sectionNavy", sel: "#architecture, .section-navy", prop: "backgroundColor" },
  { key: "sectionGreen", sel: "#capabilities, .section-green", prop: "backgroundColor" },
  { key: "ctaBg", sel: "#cta, .cta-band", prop: "backgroundColor" },
  { key: "wrapMax", sel: ".wrap", prop: "maxWidth" },
  { key: "codeBlockBg", sel: ".code-block", prop: "backgroundColor" },
  { key: "footerBg", sel: ".site-footer", prop: "backgroundColor" },
];

const TEXT_CHECKS = [
  { key: "heroTitle", sel: "#hero-title" },
  { key: "whyTitle", sel: "#why-title" },
  { key: "archTitle", sel: "#arch-title" },
  { key: "commandsTitle", sel: "#commands-title" },
  { key: "boundariesTitle", sel: "#boundaries-title" },
  { key: "ctaTitle", sel: "#cta-title" },
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
        compareCards: document.querySelectorAll(".compare-card").length,
        whoCards: document.querySelectorAll(".who-card").length,
        stepCards: document.querySelectorAll(".step-card").length,
        capBands: document.querySelectorAll(".cap-band").length,
        cmdTabs: document.querySelectorAll(".cmd-tab").length,
        archSites: document.querySelectorAll(".arch-site").length,
        boundaryRows: document.querySelectorAll(".boundaries-table tbody tr").length,
        navLinks: document.querySelectorAll(".nav-links a").length,
        footerCols: document.querySelectorAll(".site-footer .footer-grid > div").length,
        marquee: document.querySelectorAll(".marquee").length,
        doodles: document.querySelectorAll(".doodle, .edge-doodle, .drift").length,
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
      window.scrollTo(0, document.body.scrollHeight);
      await new Promise((r) => setTimeout(r, 400));
      window.scrollTo(0, 0);
    });
  };
  await primePage(localPage);
  await primePage(wpPage);

  const localAudit = await audit(localPage, "local");
  const wpAudit = await audit(wpPage, "wp");
  const diffs = diffObjects(localAudit, wpAudit);

  await localPage.screenshot({ path: `/tmp/compare-${vp.name}-local.png`, fullPage: true });
  await wpPage.screenshot({ path: `/tmp/compare-${vp.name}-wp.png`, fullPage: true });

  report.viewports[vp.name] = { local: localAudit, wp: wpAudit, diffs };
  console.log(`\n=== ${vp.name} (${vp.width}x${vp.height}) ===`);
  console.log(`Diffs: ${diffs.length}`);
  diffs.slice(0, 30).forEach((d) => console.log(JSON.stringify(d)));

  await localPage.close();
  await wpPage.close();
}

writeFileSync("/tmp/compare-report.json", JSON.stringify(report, null, 2));
console.log("\nReport: /tmp/compare-report.json");
await browser.close();
