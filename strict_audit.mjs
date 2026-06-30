/**
 * Strict section-by-section parity audit (local static vs Bricks WP).
 * Usage: node strict_audit.mjs [localUrl] [wpUrl]
 */
import { chromium } from "playwright";
import { writeFileSync } from "fs";

const LOCAL = process.argv[2] || "http://127.0.0.1:18875/";
const WP = process.argv[3] || "https://wpfy.dev.wpfy.org/";

const SECTION_IDS = [
  "problem",
  "stack",
  "features",
  "how-it-works",
  "who",
  "use-cases",
  "beta",
  "subscribe",
];

const CHROME = [
  { key: "announce", sel: ".announce, .wpfy-announce" },
  { key: "header", sel: ".site-header, .wpfy-site-header" },
  { key: "hero", sel: ".hero, .wpfy-hero, #brxe-hr0001" },
  { key: "marquee", sel: ".marquee, .wpfy-marquee" },
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
        chrome[key] = probe(document.querySelector(sel));
      }

      const heroH1 = document.querySelector("#hero-title");
      const heroCtas = document.querySelector(".hero-ctas, .wpfy-hero-ctas");
      const nav = document.querySelector(".nav, #brxe-hd0002");
      const menuBtn = document.querySelector(".menu-btn, .wpfy-menu-btn");

      const grids = {
        featuresGrid: probe(document.querySelector("#features .grid-4, #features .wpfy-grid-4")),
        whoGrid: probe(document.querySelector("#who .grid-3, #who .wpfy-grid-3")),
        compare: probe(document.querySelector("#problem .compare, #problem .wpfy-compare")),
      };

      return {
        body: probe(document.body),
        hero: probe(document.querySelector(".hero, .wpfy-hero, #brxe-hr0001")),
        heroH1: heroH1
          ? { fs: getComputedStyle(heroH1).fontSize, ta: getComputedStyle(heroH1).textAlign }
          : null,
        heroCtas: heroCtas
          ? { jc: getComputedStyle(heroCtas).justifyContent, disp: getComputedStyle(heroCtas).display }
          : null,
        navH: nav ? Math.round(nav.getBoundingClientRect().height) : null,
        menuBtnVisible: menuBtn ? getComputedStyle(menuBtn).display !== "none" : null,
        navLinksVisible: (() => {
          const nl = document.querySelector(".nav-links, .wpfy-nav-links");
          return nl ? getComputedStyle(nl).display !== "none" : null;
        })(),
        sections,
        chrome,
        grids,
        counts: {
          featureCards: document.querySelectorAll("#features .card, #features .wpfy-card").length,
          ecoBoxes: document.querySelectorAll("#stack .eco-box, #stack .wpfy-eco-box").length,
          ucRows: document.querySelectorAll("#use-cases .uc-row, #use-cases .wpfy-uc-row").length,
        },
        totalH: Math.round(document.body.scrollHeight),
      };
    },
    { SECTION_IDS, CHROME }
  );
}

const viewports = [
  { name: "desktop", width: 1440, height: 900 },
  { name: "tablet", width: 768, height: 1024 },
  { name: "mobile", width: 390, height: 844 },
];

const browser = await chromium.launch();
const report = { local: LOCAL, wp: WP, results: {} };

for (const vp of viewports) {
  const localPage = await browser.newPage({ viewport: { width: vp.width, height: vp.height } });
  const wpPage = await browser.newPage({ viewport: { width: vp.width, height: vp.height } });
  await localPage.goto(LOCAL, { waitUntil: "networkidle", timeout: 60000 });
  await wpPage.goto(WP, { waitUntil: "networkidle", timeout: 60000 });

  const local = await strictAudit(localPage);
  const wp = await strictAudit(wpPage);

  const sectionScores = [];
  const issues = [];

  for (const id of SECTION_IDS) {
    const l = local.sections[id];
    const w = wp.sections[id];
    if (!l || !w) {
      issues.push({ vp: vp.name, section: id, type: "missing", local: !!l, wp: !!w });
      sectionScores.push(0);
      continue;
    }
    const hMatch = pctMatch(l.h, w.h);
    const padMatch = (pctMatch(l.padT, w.padT) + pctMatch(l.padB, w.padB)) / 2;
    const bgMatch = l.bg === w.bg ? 100 : 0;
    const score = hMatch * 0.55 + padMatch * 0.25 + bgMatch * 0.2;
    sectionScores.push(score);
    if (score < 95 || Math.abs(l.h - w.h) > 24) {
      issues.push({
        vp: vp.name,
        section: id,
        type: "layout",
        score: +score.toFixed(1),
        local: l,
        wp: w,
        dH: w.h - l.h,
      });
    }
  }

  // Chrome / hero checks
  if (local.heroH1 && wp.heroH1 && local.heroH1.ta !== wp.heroH1.ta) {
    issues.push({ vp: vp.name, section: "hero", type: "textAlign", local: local.heroH1.ta, wp: wp.heroH1.ta });
  }
  if (local.menuBtnVisible !== wp.menuBtnVisible) {
    issues.push({ vp: vp.name, section: "header", type: "menuBtn", local: local.menuBtnVisible, wp: wp.menuBtnVisible });
  }
  if (local.navLinksVisible !== wp.navLinksVisible) {
    issues.push({ vp: vp.name, section: "header", type: "navLinks", local: local.navLinksVisible, wp: wp.navLinksVisible });
  }
  if (local.heroCtas && wp.heroCtas && local.heroCtas.jc !== wp.heroCtas.jc) {
    issues.push({ vp: vp.name, section: "hero-ctas", type: "justify", local: local.heroCtas.jc, wp: wp.heroCtas.jc });
  }

  const totalMatch = pctMatch(local.totalH, wp.totalH);
  const avgSection = sectionScores.length
    ? sectionScores.reduce((a, b) => a + b, 0) / sectionScores.length
    : 0;

  report.results[vp.name] = { local, wp, avgSection: +avgSection.toFixed(2), totalMatch: +totalMatch.toFixed(2), issues };

  await localPage.screenshot({ path: `/tmp/strict-${vp.name}-local.png`, fullPage: true });
  await wpPage.screenshot({ path: `/tmp/strict-${vp.name}-wp.png`, fullPage: true });
  await localPage.close();
  await wpPage.close();
}

await browser.close();
writeFileSync("/tmp/strict-audit.json", JSON.stringify(report, null, 2));

console.log("\n=== STRICT PARITY SUMMARY ===");
for (const [vp, data] of Object.entries(report.results)) {
  console.log(`${vp}: sections ${data.avgSection}% | page height ${data.totalMatch}% | issues ${data.issues.length}`);
}

console.log("\n=== ISSUES (score < 95 or |dH| > 24) ===");
for (const data of Object.values(report.results)) {
  for (const i of data.issues) {
    if (i.type === "layout") {
      console.log(
        `[${i.vp}] ${i.section}: score=${i.score}% local.h=${i.local.h} wp.h=${i.wp.h} (d=${i.dH}) pad ${i.local.padT}/${i.local.padB} vs ${i.wp.padT}/${i.wp.padB} bg ${i.local.bg === i.wp.bg ? "ok" : "MISMATCH"}`
      );
    } else {
      console.log(`[${i.vp}] ${i.section} ${i.type}:`, JSON.stringify(i));
    }
  }
}
