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

  // Savings calculator: hours = questions/day x minutes x share x 22 days / 60
  var cq = document.getElementById("c-q");
  if (cq) {
    var cm = document.getElementById("c-m"), cs = document.getElementById("c-s"), cc = document.getElementById("c-c");
    var cur = cc.dataset.cur, lang = document.documentElement.lang;
    var fmt = new Intl.NumberFormat(lang === "id" ? "id-ID" : lang === "de" ? "de-DE" : "en-GB", { maximumFractionDigits: 0 });
    function calc() {
      var hours = cq.value * cm.value * (cs.value / 100) * 22 / 60;
      var step = cur === "Rp" ? 1000 : 10, money = Math.round(hours * cc.value / step) * step;
      document.getElementById("o-q").textContent = cq.value;
      document.getElementById("o-m").textContent = cm.value;
      document.getElementById("o-s").textContent = cs.value + "%";
      document.getElementById("o-c").textContent = cur + " " + fmt.format(cc.value);
      document.getElementById("r-h").textContent = fmt.format(hours);
      document.getElementById("r-v").textContent = cur + " " + fmt.format(money);
      document.getElementById("r-bar").style.width = Math.min(100, hours / 160 * 100) + "%";
    }
    [cq, cm, cs, cc].forEach(function (el) { el.addEventListener("input", calc); });
    calc();
  }

  // Adoption curve draws once when visible
  var curve = document.querySelector(".curve");
  if (curve && "IntersectionObserver" in window && !reduceMotion) {
    new IntersectionObserver(function (en, obs) {
      if (en[0].isIntersecting) { curve.classList.add("draw"); obs.disconnect(); }
    }, { threshold: 0.4 }).observe(curve);
  }

  // On-page assistant: answers only from this page's text, shows the source, hands over when nothing matches
  var abtn = document.querySelector(".asst-btn"), asst = document.getElementById("asst");
  if (abtn && asst) {
    var kb = JSON.parse(document.getElementById("kb").textContent);
    var cfg = JSON.parse(document.getElementById("asst-cfg").textContent);
    var log = asst.querySelector(".asst-log"), form = asst.querySelector(".asst-form"), input = document.getElementById("asst-in");
    var STOP = ("the and for you your are can could would will with what how does this that from have about our is do me my we us need want please help build make create get " +
      "ist und der die das ein eine einen sie ich wie was mit fur auf von zu den dem des bei sind wir uns wird werden kann konnen bauen machen brauchen mochte bitte mein meine " +
      "apa dan yang untuk dari dengan ini itu saya anda kami bisa ada atau di ke ya tidak buat bikin mau ingin perlu butuh tolong bagaimana gimana").split(" ");
    function toks(s) {
      return (s || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/ß/g, "ss")
        .split(/[^a-z0-9]+/).filter(function (w) { return w.length > 2 && STOP.indexOf(w) < 0; });
    }
    var df = {};
    kb.forEach(function (e) {
      e.kw = toks(e.q + " " + e.k); e.tx = toks(e.a);
      var seen = {};
      e.kw.concat(e.tx).forEach(function (w) { if (!seen[w]) { seen[w] = 1; df[w] = (df[w] || 0) + 1; } });
    });
    function idf(w) { return Math.log(1 + kb.length / (df[w] || 1)); }
    function hit(w, list) {
      for (var i = 0; i < list.length; i++) {
        var o = list[i];
        if (o === w) return 1;
        if (w.length >= 4 && o.length >= 4 && (o.indexOf(w) === 0 || w.indexOf(o) === 0)) return 0.7;
      }
      return 0;
    }
    function best(q) {
      var qt = toks(q), top = null, topScore = 0, topHits = 0;
      if (!qt.length) return null;
      kb.forEach(function (e) {
        var s = 0, n = 0;
        qt.forEach(function (w) { var h = Math.max(2 * hit(w, e.kw), hit(w, e.tx)); if (h) n++; s += idf(w) * h; });
        if (s > topScore) { topScore = s; top = e; topHits = n; }
      });
      // most of the meaningful words must match, otherwise hand over instead of guessing
      return topScore >= 2 && topHits * 2 > qt.length ? top : null;
    }
    function add(cls, html) {
      var d = document.createElement("div"); d.className = "m " + cls; d.innerHTML = html;
      log.appendChild(d); log.scrollTop = log.scrollHeight; return d;
    }
    function esc(s) { var d = document.createElement("div"); d.textContent = s; return d.innerHTML; }
    function answer(q) {
      add("m-user", esc(q));
      var t = add("m-ai", '<span class="typing-m"><i></i><i></i><i></i></span>');
      setTimeout(function () {
        var e = best(q);
        if (e) {
          t.innerHTML = esc(e.a) + (e.src ? '<br><a class="m-src" href="' + e.href + '">' + esc(cfg.src) + ": " + esc(e.src) + "</a>" : "");
          var link = t.querySelector(".m-src");
          if (link && window.innerWidth < 640) link.addEventListener("click", close);
        } else {
          t.innerHTML = esc(cfg.none) + '<div class="m-act"><a href="' + cfg.waHref + encodeURIComponent(cfg.waText + q) +
            '" target="_blank" rel="noopener">' + esc(cfg.wa) + '</a><a href="' + cfg.bookHref + '" target="_blank" rel="noopener">' + esc(cfg.book) + "</a></div>";
        }
        log.scrollTop = log.scrollHeight;
      }, reduceMotion ? 0 : 650);
    }
    function open() { asst.hidden = false; abtn.setAttribute("aria-expanded", "true"); input.focus(); }
    function close() { asst.hidden = true; abtn.setAttribute("aria-expanded", "false"); abtn.focus(); }
    abtn.addEventListener("click", open);
    asst.querySelector(".asst-x").addEventListener("click", close);
    asst.addEventListener("keydown", function (e) { if (e.key === "Escape") close(); });
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var q = input.value.trim(); if (!q) return;
      input.value = ""; answer(q);
    });
    asst.querySelectorAll(".chip").forEach(function (c) { c.addEventListener("click", function () { answer(c.textContent); }); });
  }

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
