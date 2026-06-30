/* WPFY launch site: reveals, hero terminal loop, copy, mobile nav.
   All animation is transform/opacity; everything degrades statically
   under prefers-reduced-motion or without JS. */
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
  }

  /* ---------- copy buttons ---------- */
  document.querySelectorAll(".copy-btn").forEach(function (btn) {
    var label = btn.querySelector("span");
    btn.addEventListener("click", function () {
      if (!navigator.clipboard || !btn.dataset.copy) { return; }
      navigator.clipboard.writeText(btn.dataset.copy).then(function () {
        if (label) { label.textContent = "copied"; }
        setTimeout(function () { if (label) { label.textContent = "copy"; } }, 1600);
      }).catch(function () {
        if (label) { label.textContent = "failed"; }
        setTimeout(function () { if (label) { label.textContent = "copy"; } }, 1600);
      });
    });
  });

  /* ---------- command chips: click to copy ---------- */
  var CHIP_ICO = '<svg class="cmd-chip-ico" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><g class="ico-copy"><rect x="5" y="5" width="8" height="9" rx="1"/><path d="M11 5V3.5A1.5 1.5 0 0 0 9.5 2h-5A1.5 1.5 0 0 0 3 3.5v7A1.5 1.5 0 0 0 4.5 12H5"/></g><path class="ico-check" d="M3.5 8.4l3 3 6-6.6"/></svg>';
  document.querySelectorAll(".cmd-chip[data-copy]").forEach(function (chip) {
    chip.insertAdjacentHTML("beforeend", CHIP_ICO);
    var baseLabel = "Copy command: " + chip.dataset.copy;
    chip.setAttribute("aria-label", baseLabel);
    chip.setAttribute("title", "Copy to clipboard");
    var timer;
    // success/failure changes the visual state AND the accessible name, so
    // screen-reader users get the same confirmation; both restore the label.
    var restore = function () {
      chip.classList.remove("copied");
      chip.setAttribute("aria-label", baseLabel);
    };
    chip.addEventListener("click", function () {
      if (!navigator.clipboard) { return; }
      navigator.clipboard.writeText(chip.dataset.copy).then(function () {
        chip.classList.add("copied");
        chip.setAttribute("aria-label", "Copied: " + chip.dataset.copy);
        clearTimeout(timer);
        timer = setTimeout(restore, 1500);
      }).catch(function () {
        chip.classList.remove("copied");
        chip.setAttribute("aria-label", "Copy failed");
        clearTimeout(timer);
        timer = setTimeout(restore, 1500);
      });
    });
  });

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
  }

  /* ---------- ecosystem pipes ---------- */
  // Colored pipes snaking from each box into the center node. Drawn from the
  // measured layout so they hold at any width; the stacked (<=1024px) layout
  // hides them. Coordinates are relative to .eco-diagram, so the reveal
  // translate doesn't skew them.
  var ecoDiagram = document.querySelector(".eco-diagram");
  var ecoPipesSvg = document.querySelector(".eco-pipes");
  var ecoNode = document.querySelector(".eco-node");
  if (ecoDiagram && ecoPipesSvg && ecoNode) {
    var SVG_NS = "http://www.w3.org/2000/svg";
    var PIPE_COLORS = {
      "box-blue": "#6fc2ff",
      "box-teal": "#53dbc9",
      "box-yellow": "#ffde00",
      "box-red": "#f2655a",
      "box-cream": "#c9c2ba"
    };
    var stackedQuery = window.matchMedia("(max-width: 1024px)");
    var pipeByBox = new Map();

    var pipeColor = function (box) {
      for (var key in PIPE_COLORS) {
        if (box.classList.contains(key)) { return PIPE_COLORS[key]; }
      }
      return PIPE_COLORS["box-cream"];
    };

    // orthogonal polyline -> path with rounded corners
    var roundedPath = function (pts, radius) {
      var d = "M" + pts[0][0] + " " + pts[0][1];
      for (var i = 1; i < pts.length - 1; i++) {
        var prev = pts[i - 1], cur = pts[i], next = pts[i + 1];
        var inLen = Math.hypot(cur[0] - prev[0], cur[1] - prev[1]);
        var outLen = Math.hypot(next[0] - cur[0], next[1] - cur[1]);
        var r = Math.min(radius, inLen / 2, outLen / 2);
        if (r < 1) { d += " L" + cur[0] + " " + cur[1]; continue; }
        d += " L" + (cur[0] - ((cur[0] - prev[0]) / inLen) * r) +
             " " + (cur[1] - ((cur[1] - prev[1]) / inLen) * r) +
             " Q" + cur[0] + " " + cur[1] +
             " " + (cur[0] + ((next[0] - cur[0]) / outLen) * r) +
             " " + (cur[1] + ((next[1] - cur[1]) / outLen) * r);
      }
      d += " L" + pts[pts.length - 1][0] + " " + pts[pts.length - 1][1];
      return d;
    };

    var drawEcoPipes = function () {
      ecoPipesSvg.textContent = "";
      pipeByBox.clear();
      if (stackedQuery.matches) { return; }
      var base = ecoDiagram.getBoundingClientRect();
      var node = ecoNode.getBoundingClientRect();
      var nodeL = node.left - base.left;
      var nodeR = node.right - base.left;
      var nodeT = node.top - base.top;

      [{ sel: ".eco-col-l .eco-box", dir: 1 }, { sel: ".eco-col-r .eco-box", dir: -1 }]
        .forEach(function (side) {
          var boxes = ecoDiagram.querySelectorAll(side.sel);
          Array.prototype.forEach.call(boxes, function (box, i) {
            var b = box.getBoundingClientRect();
            var sx = (side.dir === 1 ? b.right : b.left) - base.left;
            var sy = b.top - base.top + b.height / 2;
            var ex = side.dir === 1 ? nodeL : nodeR;
            // bundle entries on the node edge: top box high, bottom box low
            var ey = nodeT + node.height * (0.3 + 0.2 * i);
            // parallel vertical corridors in the column gap
            var cx = sx + side.dir * (i === 0 ? 22 : i === 1 ? 30 : 40);
            var path = document.createElementNS(SVG_NS, "path");
            path.setAttribute("class", "eco-pipe");
            path.setAttribute("stroke", pipeColor(box));
            path.setAttribute("d", roundedPath([[sx, sy], [cx, sy], [cx, ey], [ex, ey]], 14));
            ecoPipesSvg.appendChild(path);
            pipeByBox.set(box, path);
          });
        });
    };

    Array.prototype.forEach.call(ecoDiagram.querySelectorAll(".eco-box"), function (box) {
      box.addEventListener("mouseenter", function () {
        var p = pipeByBox.get(box);
        if (p) { p.classList.add("hot"); }
      });
      box.addEventListener("mouseleave", function () {
        var p = pipeByBox.get(box);
        if (p) { p.classList.remove("hot"); }
      });
    });

    var pipeTimer;
    window.addEventListener("resize", function () {
      clearTimeout(pipeTimer);
      pipeTimer = setTimeout(drawEcoPipes, 150);
    });
    window.addEventListener("load", drawEcoPipes);
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(drawEcoPipes);
    }
    drawEcoPipes();
  }

  /* ---------- subscribe ribbon (placeholder: no backend wired yet) ---------- */
  var subForm = document.querySelector(".sub-form[data-placeholder]");
  var subStatus = document.querySelector(".sub-status");
  var subPrivacy = document.getElementById("sub-privacy");
  if (subForm && subStatus) {
    subForm.addEventListener("submit", function (e) {
      e.preventDefault();
      if (subPrivacy && !subPrivacy.checked) {
        subPrivacy.focus();
        return;
      }
      if (!subForm.checkValidity()) {
        if (subForm.reportValidity) { subForm.reportValidity(); }
        return;
      }
      subForm.hidden = true;
      subStatus.hidden = false;
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
    if (choice.analytics) {
      /* Load analytics only after consent — wire provider here when enabled. */
      document.dispatchEvent(new CustomEvent("wpfy:consent-analytics", { detail: choice }));
    }
    if (choice.marketing) {
      document.dispatchEvent(new CustomEvent("wpfy:consent-marketing", { detail: choice }));
    }
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
          '<button type="button" class="btn btn-ink" data-cookie-save style="margin-top:8px">Save preferences</button>' +
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
  // Two scenes: the installer run, then a site-create with SSL preflight.
  // Static markup stays in place for reduced-motion / no-JS readers.
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
      cmd: "wpfy site create example.com --wp -le",
      lines: [
        '<span class="t-out"><span class="t-ok">✓</span> scaffold rendered        <span class="t-dim">compose.yaml · .env · isolated network</span></span>',
        '<span class="t-out"><span class="t-ok">✓</span> ssl preflight passed     <span class="t-dim">DNS A → matches server public IP</span></span>',
        '<span class="t-out"><span class="t-ok">✓</span> certificate issued       <span class="t-dim">Let’s Encrypt (ACME)</span></span>',
        '<span class="t-out"><span class="t-ok">✓</span> wordpress provisioned    <span class="t-dim">https://example.com is live</span></span>'
      ]
    }
  ];

  var TYPE_MS = 26;        // per character
  var LINE_MS = 340;       // between output lines
  var SCENE_HOLD_MS = 4200;

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
        setTimeout(typeChar, TYPE_MS + Math.random() * 24);
      } else {
        setTimeout(function () { printLine(0); }, 420);
      }
    }

    function printLine(n) {
      if (n < scene.lines.length) {
        term.insertBefore(el(scene.lines[n]), caretHolder());
        setTimeout(function () { printLine(n + 1); }, LINE_MS);
      } else {
        setTimeout(function () { playScene(i + 1); }, SCENE_HOLD_MS);
      }
    }

    // keep the caret parked on its own trailing line while output prints
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

    typeChar();
  }

  // hand off from the static markup once the terminal scrolls into view
  var started = false;
  var startIO = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting && !started) {
        started = true;
        startIO.disconnect();
        setTimeout(function () { playScene(0); }, 500);
      }
    });
  }, { threshold: 0.4 });
  startIO.observe(term);
})();
