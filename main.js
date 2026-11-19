(function () {
  var KEY = "amrinawork-lang";
  var current = document.body.dataset.lang;

  function store(lang) { try { localStorage.setItem(KEY, lang); } catch (e) {} }
  function stored() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }

  // Mobile menu
  var btn = document.querySelector(".menu-btn"), nav = document.getElementById("nav");
  btn.addEventListener("click", function () {
    var open = nav.classList.toggle("open");
    btn.setAttribute("aria-expanded", open);
  });
  nav.addEventListener("click", function (e) {
    if (e.target.tagName === "A") { nav.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); }
  });

  // Header language links remember the choice
  document.querySelectorAll(".switch a").forEach(function (a) {
    a.addEventListener("click", function () { store(a.dataset.lang); });
  });

  // Services tabs (ARIA tabs pattern) with autoplay and replayed mock-up animations
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var bench = document.querySelector(".bench");
  var tabs = Array.prototype.slice.call(document.querySelectorAll('[role="tab"]'));
  function countUp(panel) {
    panel.querySelectorAll(".count").forEach(function (el) {
      var target = el.dataset.to, m = target.match(/-?\d+/);
      if (!m || reduceMotion) { el.textContent = target; return; }
      var end = parseInt(m[0], 10), t0 = null;
      function step(ts) {
        if (!t0) t0 = ts;
        var k = Math.min(1, (ts - t0) / 1200), val = Math.round(end * (1 - Math.pow(1 - k, 3)));
        el.textContent = target.replace(m[0], val);
        if (k < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    });
  }
  function select(tab, byUser) {
    tabs.forEach(function (t) {
      var on = t === tab, panel = document.getElementById(t.getAttribute("aria-controls"));
      t.setAttribute("aria-selected", on);
      t.tabIndex = on ? 0 : -1;
      panel.hidden = !on;
      panel.classList.remove("run");
      if (on) { void panel.offsetWidth; panel.classList.add("run"); countUp(panel); }
    });
    if (byUser && bench) { bench.classList.remove("auto"); bench.dataset.touched = "1"; }
  }
  tabs.forEach(function (t, i) {
    t.addEventListener("click", function () { select(t, true); t.scrollIntoView({ block: "nearest", inline: "nearest" }); });
    t.addEventListener("keydown", function (e) {
      var j = e.key === "ArrowDown" || e.key === "ArrowRight" ? i + 1 : e.key === "ArrowUp" || e.key === "ArrowLeft" ? i - 1 : null;
      if (j === null) return;
      e.preventDefault();
      var next = tabs[(j + tabs.length) % tabs.length];
      select(next, true); next.focus();
    });
    t.querySelector(".prog").addEventListener("animationend", function () {
      if (!bench.classList.contains("auto")) return;
      select(tabs[(i + 1) % tabs.length], false);
    });
  });
  if (bench && !reduceMotion && "IntersectionObserver" in window) {
    var started = false;
    new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting && !started) {
          started = true;
          if (!bench.dataset.touched) { bench.classList.add("auto"); select(tabs[0], false); }
        }
        bench.classList.toggle("paused", !en.isIntersecting);
      });
    }, { threshold: 0.35 }).observe(bench);
    bench.addEventListener("mouseenter", function () { bench.classList.add("paused"); });
    bench.addEventListener("mouseleave", function () { bench.classList.remove("paused"); });
  }

  // Work filter
  var fbtns = Array.prototype.slice.call(document.querySelectorAll(".filters button"));
  var cases = Array.prototype.slice.call(document.querySelectorAll(".case"));
  fbtns.forEach(function (b) {
    b.addEventListener("click", function () {
      var cat = b.dataset.cat;
      fbtns.forEach(function (o) { o.setAttribute("aria-pressed", o === b); });
      document.querySelector(".cases").classList.toggle("filtered", cat !== "all");
      cases.forEach(function (c) {
        var show = cat === "all" || c.dataset.cats.split(" ").indexOf(cat) > -1;
        c.hidden = !show;
        c.classList.remove("enter");
        if (show) { void c.offsetWidth; c.classList.add("enter"); }
      });
    });
  });

  // Hero chat plays once
  var chat = document.querySelector(".chat");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  function play() { if (!reduce) chat.classList.add("play"); }

  // First visit: ask for a language before continuing
  var dlg = document.getElementById("lang-dialog");
  var saved = stored();
  if (!saved && dlg && typeof dlg.showModal === "function") {
    if (!reduce) chat.classList.add("wait");
    var guess = (navigator.language || "en").slice(0, 2).toLowerCase();
    var pick = dlg.querySelector('[data-lang="' + guess + '"]') || dlg.querySelector('[data-lang="en"]');
    dlg.addEventListener("cancel", function (e) { e.preventDefault(); });
    dlg.querySelectorAll(".dlg-lang").forEach(function (a) {
      a.addEventListener("click", function (e) {
        store(a.dataset.lang);
        if (a.dataset.lang === current) {
          e.preventDefault();
          dlg.close();
          chat.classList.remove("wait");
          play();
        }
      });
    });
    dlg.showModal();
    pick.focus();
  } else {
    play();
  }
})();
