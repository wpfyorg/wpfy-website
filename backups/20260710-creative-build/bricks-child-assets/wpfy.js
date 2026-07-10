/* WPFY marketing site — reveals, copy, command tabs, mobile nav, terminal loop */
(function () {
  "use strict";

  document.documentElement.classList.add("js");

  var reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- scroll reveals ---------- */
  var revealEls = document.querySelectorAll(".reveal");
  if (reducedMotion || !("IntersectionObserver" in window)) {
    revealEls.forEach(function (el) { el.classList.add("in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("in");
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    revealEls.forEach(function (el) { io.observe(el); });
    document.querySelectorAll(".hero .reveal, .announce + header + main .reveal").forEach(function (el) {
      el.classList.add("in");
    });
  }

  /* ---------- copy buttons ---------- */
  var live = document.createElement("div");
  live.setAttribute("aria-live", "polite");
  live.className = "sr-only";
  document.body.appendChild(live);

  document.querySelectorAll(".copy-btn").forEach(function (btn) {
    var label = btn.querySelector("span");
    btn.addEventListener("click", function () {
      if (!navigator.clipboard || !btn.dataset.copy) { return; }
      navigator.clipboard.writeText(btn.dataset.copy).then(function () {
        if (label) { label.textContent = "copied"; }
        live.textContent = "Command copied to clipboard";
        setTimeout(function () {
          if (label) { label.textContent = "copy"; }
          live.textContent = "";
        }, 1600);
      }).catch(function () {
        if (label) { label.textContent = "failed"; }
        live.textContent = "Copy failed";
        setTimeout(function () {
          if (label) { label.textContent = "copy"; }
          live.textContent = "";
        }, 1600);
      });
    });
  });

  /* ---------- command tabs ---------- */
  var tablist = document.querySelector(".cmd-tabs");
  if (tablist) {
    var tabs = tablist.querySelectorAll('[role="tab"]');
    var panels = document.querySelectorAll(".cmd-panel[role='tabpanel']");

    function activateTab(tab) {
      tabs.forEach(function (t) {
        var selected = t === tab;
        t.setAttribute("aria-selected", selected ? "true" : "false");
        t.tabIndex = selected ? 0 : -1;
      });
      panels.forEach(function (panel) {
        var active = panel.id === tab.getAttribute("aria-controls");
        panel.classList.toggle("is-active", active);
        panel.hidden = !active;
      });
    }

    tabs.forEach(function (tab, index) {
      tab.tabIndex = tab.getAttribute("aria-selected") === "true" ? 0 : -1;
      tab.addEventListener("click", function () { activateTab(tab); });
      tab.addEventListener("keydown", function (e) {
        var next = index;
        if (e.key === "ArrowRight") { next = (index + 1) % tabs.length; }
        else if (e.key === "ArrowLeft") { next = (index - 1 + tabs.length) % tabs.length; }
        else if (e.key === "Home") { next = 0; }
        else if (e.key === "End") { next = tabs.length - 1; }
        else { return; }
        e.preventDefault();
        activateTab(tabs[next]);
        tabs[next].focus();
      });
    });
  }

  /* ---------- mobile nav ---------- */
  var menuBtn = document.querySelector(".menu-btn");
  var navLinks = document.getElementById("nav-links");
  if (menuBtn && navLinks) {
    menuBtn.addEventListener("click", function () {
      var open = navLinks.classList.toggle("open");
      menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
    });
    navLinks.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        navLinks.classList.remove("open");
        menuBtn.setAttribute("aria-expanded", "false");
      });
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && navLinks.classList.contains("open")) {
        navLinks.classList.remove("open");
        menuBtn.setAttribute("aria-expanded", "false");
        menuBtn.focus();
      }
    });
  }

  /* ---------- cookie consent ---------- */
  var CONSENT_KEY = "wpfy_cookie_consent";
  var consentRaw = null;
  try { consentRaw = localStorage.getItem(CONSENT_KEY); } catch (e) { /* private mode */ }

  function parseConsent(raw) {
    if (!raw) { return null; }
    try { return JSON.parse(raw); } catch (e) { return null; }
  }

  function saveConsent(choice) {
    try { localStorage.setItem(CONSENT_KEY, JSON.stringify(choice)); } catch (e) { /* noop */ }
    applyConsent(choice);
    hideCookieBanner();
  }

  function applyConsent(choice) {
    document.documentElement.dataset.cookieAnalytics = choice.analytics ? "1" : "0";
    document.documentElement.dataset.cookieMarketing = choice.marketing ? "1" : "0";
  }

  var existingConsent = parseConsent(consentRaw);
  if (existingConsent) { applyConsent(existingConsent); }

  function hideCookieBanner() {
    var banner = document.getElementById("cookie-banner");
    if (banner) { banner.classList.remove("is-visible"); }
  }

  function buildCookieBanner() {
    if (document.getElementById("cookie-banner")) { return; }
    if (existingConsent) { return; }
    var banner = document.createElement("div");
    banner.id = "cookie-banner";
    banner.className = "cookie-banner";
    banner.setAttribute("role", "dialog");
    banner.setAttribute("aria-label", "Cookie consent");
    banner.innerHTML =
      '<div class="cookie-banner-inner">' +
        '<p>We use necessary cookies to run the site. With your consent, we may use analytics and affiliate tracking cookies. See our <a href="/legal/cookies">Cookie Policy</a> and <a href="/legal/privacy">Privacy Policy</a>.</p>' +
        '<div class="cookie-banner-actions">' +
          '<button type="button" class="btn" data-cookie-reject>Reject non-essential</button>' +
          '<button type="button" class="btn" data-cookie-customize>Customize</button>' +
          '<button type="button" class="btn btn-blue" data-cookie-accept>Accept all</button>' +
        '</div>' +
        '<div class="cookie-panel" id="cookie-panel">' +
          '<label><input type="checkbox" checked disabled> Strictly necessary (always on)</label>' +
          '<label><input type="checkbox" id="cookie-analytics"> Analytics</label>' +
          '<label><input type="checkbox" id="cookie-marketing"> Marketing &amp; affiliate</label>' +
          '<button type="button" class="btn btn-primary" data-cookie-save style="margin-top:8px">Save preferences</button>' +
        '</div>' +
      '</div>';
    document.body.appendChild(banner);
    requestAnimationFrame(function () { banner.classList.add("is-visible"); });

    banner.querySelector("[data-cookie-accept]").addEventListener("click", function () {
      saveConsent({ necessary: true, analytics: true, marketing: true, ts: Date.now() });
    });
    banner.querySelector("[data-cookie-reject]").addEventListener("click", function () {
      saveConsent({ necessary: true, analytics: false, marketing: false, ts: Date.now() });
    });
    banner.querySelector("[data-cookie-customize]").addEventListener("click", function () {
      document.getElementById("cookie-panel").classList.toggle("is-open");
    });
    banner.querySelector("[data-cookie-save]").addEventListener("click", function () {
      saveConsent({
        necessary: true,
        analytics: !!document.getElementById("cookie-analytics").checked,
        marketing: !!document.getElementById("cookie-marketing").checked,
        ts: Date.now()
      });
    });
  }

  buildCookieBanner();

  document.querySelectorAll("[data-cookie-settings]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      existingConsent = null;
      try { localStorage.removeItem(CONSENT_KEY); } catch (e) { /* noop */ }
      var old = document.getElementById("cookie-banner");
      if (old) { old.remove(); }
      buildCookieBanner();
      var fresh = document.getElementById("cookie-banner");
      if (fresh) { fresh.classList.add("is-visible"); }
    });
  });

  /* ---------- hero terminal loop ---------- */
  var term = document.getElementById("hero-term");
  if (!term || reducedMotion || !("IntersectionObserver" in window)) { return; }

  var SCENES = [
    {
      cmd: "curl -fsSL https://raw.githubusercontent.com/wpfyorg/wpfy/main/install.sh | sudo bash",
      lines: [
        '<span class="t-out">[ 1/16] Checking Ubuntu release ............ <span class="t-ok">OK</span></span>',
        '<span class="t-out">[ 2/16] Verifying source checksum .......... <span class="t-ok">OK</span></span>',
        '<span class="t-out">[ 3/16] Installing Docker Engine ........... <span class="t-ok">OK</span></span>',
        '<span class="t-out">        ...</span>',
        '<span class="t-out">[16/16] wpfy installed. Run: <span class="t-dim">wpfy --help</span></span>'
      ]
    },
    {
      cmd: "wpfy run example.com --wp",
      lines: [
        '<span class="t-out"><span class="t-ok">✓</span> scaffold rendered        <span class="t-dim">compose.yaml · private network</span></span>',
        '<span class="t-out"><span class="t-ok">✓</span> wordpress provisioned    <span class="t-dim">site runtime started</span></span>',
        '<span class="t-out"><span class="t-ok">✓</span> status                   <span class="t-dim">wpfy site status example.com</span></span>'
      ]
    },
    {
      cmd: "wpfy site ssl example.com --letsencrypt",
      lines: [
        '<span class="t-out"><span class="t-ok">✓</span> ssl preflight passed     <span class="t-dim">DNS A → matches server public IP</span></span>',
        '<span class="t-out"><span class="t-ok">✓</span> certificate issued       <span class="t-dim">Let\'s Encrypt (ACME)</span></span>'
      ]
    }
  ];

  var TYPE_MS = 22;
  var LINE_MS = 320;
  var SCENE_HOLD_MS = 3800;

  function el(html) {
    var span = document.createElement("span");
    span.className = "t-line t-in";
    span.innerHTML = html;
    return span;
  }

  function playScene(i) {
    var scene = SCENES[i % SCENES.length];
    term.textContent = "";

    var cmdLine = el('<span class="t-prompt">$</span> <span class="t-cmd"></span><span class="t-caret"></span>');
    term.appendChild(cmdLine);
    var cmdSpan = cmdLine.querySelector(".t-cmd");
    var caret = cmdLine.querySelector(".t-caret");

    var pos = 0;
    function typeChar() {
      if (pos < scene.cmd.length) {
        pos += 1;
        cmdSpan.textContent = scene.cmd.slice(0, pos);
        setTimeout(typeChar, TYPE_MS + Math.random() * 20);
      } else {
        setTimeout(function () { printLine(0); }, 400);
      }
    }

    var parked = null;
    function caretHolder() {
      if (!parked) {
        cmdLine.removeChild(caret);
        parked = el("");
        parked.appendChild(caret);
        term.appendChild(parked);
      }
      return parked;
    }

    function printLine(n) {
      if (n < scene.lines.length) {
        term.insertBefore(el(scene.lines[n]), caretHolder());
        setTimeout(function () { printLine(n + 1); }, LINE_MS);
      } else {
        setTimeout(function () { playScene(i + 1); }, SCENE_HOLD_MS);
      }
    }

    typeChar();
  }

  var started = false;
  var startIO = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting && !started) {
        started = true;
        startIO.disconnect();
        setTimeout(function () { playScene(0); }, 500);
      }
    });
  }, { threshold: 0.35 });
  startIO.observe(term);
})();
