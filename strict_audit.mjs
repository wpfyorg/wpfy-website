/**
 * Strict section-by-section parity audit (local static vs Bricks WP).
 * Usage: node strict_audit.mjs [localUrl] [wpUrl]
 */
import { chromium } from "playwright";
import { writeFileSync } from "fs";

const LOCAL = process.argv[2] || "http://127.0.0.1:8766/";
const WP = process.argv[3] || "https://wpfy.dev.wpfy.org/";

const SECTION_IDS = [
  "tech",
  "why-docker",
  "architecture",
  "commands",
  "capabilities",
  "quick-start",
  "users",
  "boundaries",
  "cta",
  "updates",
];

const CHROME = [
  { key: "announce", sel: ".announce, .wpfy-announce" },
  { key: "header", sel: ".site-header, .wpfy-site-header" },
  { key: "hero", sel: ".hero, .wpfy-hero" },
  { key: "footer", sel: ".site-footer, .wpfy-site-footer" },
];

function pctMatch(local, wp) {
  if (local == null || wp == null) return local === wp ? 100 : 0;
  if (typeof local === "number" && typeof wp === "number") {
    if (local === 0 && wp === 0) return 100;
    const base = Math.max(Math.abs(local), Math.abs(wp), 1);
    return Math.max(0, 100 - (100 * Math.abs(local - wp)) / base);
  }
  return local === wp ? 100 : 0;
}

async function strictAudit(page) {
  await page.evaluate(async () => {
    document.body.classList.add("js");
    document.querySelectorAll(".bricks-lazy-hidden").forEach((el) => {
      el.classList.remove("bricks-lazy-hidden");
    });
    for (let y = 0; y < document.body.scrollHeight; y += 400) {
      window.scrollTo(0, y);
      await new Promise((r) => setTimeout(r, 60));
    }
    window.scrollTo(0, 0);
  });
  await page.waitForTimeout(400);

  return page.evaluate(
    ({ SECTION_IDS, CHROME }) => {
      const probe = (el) => {
        if (!el) return null;
        const r = el.getBoundingClientRect();
        const c = getComputedStyle(el);
        return {
          h: Math.round(r.height),
          w: Math.round(r.width),
          padT: Math.round(parseFloat(c.paddingTop) || 0),
          padB: Math.round(parseFloat(c.paddingBottom) || 0),
          bg: c.backgroundColor,
          fs: c.fontSize,
          ta: c.textAlign,
          disp: c.display,
        };
      };

      const sections = {};
      for (const id of SECTION_IDS) {
        const el = document.getElementById(id);
        sections[id] = probe(el);
      }

      const chrome = {};
      for (const { key, sel } of CHROME) {
        const el = document.querySelector(sel);
        chrome[key] = probe(el);
      }

      const heroH1 = document.querySelector("#hero-title");
      const counts = {
        marquee: document.querySelectorAll(".marquee, .wpfy-marquee").length,
        doodles: document.querySelectorAll(".doodle, .edge-doodle, .drift, .wpfy-doodle").length,
        cmdTabs: document.querySelectorAll(".cmd-tab").length,
        boundaryRows: document.querySelectorAll(".boundaries-table tbody tr").length,
      };

      return {
        sections,
        chrome,
        heroTitle: heroH1 ? heroH1.textContent.trim() : null,
        pageH: document.documentElement.scrollHeight,
        counts,
      };
    },
    { SECTION_IDS, CHROME }
  );
}

function scoreSection(local, wp) {
  if (!local && !wp) return 100;
  if (!local || !wp) return 0;
  const keys = ["h", "w", "padT", "padB"];
  const scores = keys.map((k) => pctMatch(local[k], wp[k]));
  return Math.round(scores.reduce((a, b) => a + b, 0) / scores.length);
}

const browser = await chromium.launch();
const viewports = [
  { name: "desktop", width: 1440, height: 900 },
  { name: "tablet", width: 768, height: 1024 },
  { name: "mobile", width: 390, height: 844 },
];

const report = { local: LOCAL, wp: WP, results: {} };

for (const vp of viewports) {
  const localPage = await browser.newPage({ viewport: { width: vp.width, height: vp.height } });
  const wpPage = await browser.newPage({ viewport: { width: vp.width, height: vp.height } });
  await localPage.goto(LOCAL, { waitUntil: "networkidle", timeout: 60000 });
  await wpPage.goto(WP, { waitUntil: "networkidle", timeout: 60000 });

  const local = await strictAudit(localPage);
  const wp = await strictAudit(wpPage);

  const sectionScores = {};
  for (const id of SECTION_IDS) {
    sectionScores[id] = scoreSection(local.sections[id], wp.sections[id]);
  }

  report.results[vp.name] = {
    local,
    wp,
    sectionScores,
    avgScore: Math.round(
      Object.values(sectionScores).reduce((a, b) => a + b, 0) / SECTION_IDS.length
    ),
  };

  console.log(`\n=== ${vp.name} strict audit ===`);
  console.log("Avg section score:", report.results[vp.name].avgScore);
  console.log("Local page height:", local.pageH, "WP:", wp.pageH);
  console.log("Local hero:", local.heroTitle, "| WP:", wp.heroTitle);
  console.log("Marquee count local/wp:", local.counts.marquee, wp.counts.marquee);

  await localPage.close();
  await wpPage.close();
}

writeFileSync("/tmp/strict-audit-report.json", JSON.stringify(report, null, 2));
console.log("\nReport: /tmp/strict-audit-report.json");
await browser.close();
