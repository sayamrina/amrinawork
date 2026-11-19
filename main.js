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

  // Services tabs (ARIA tabs pattern)
  var tabs = Array.prototype.slice.call(document.querySelectorAll('[role="tab"]'));
  function select(tab) {
    tabs.forEach(function (t) {
      var on = t === tab;
      t.setAttribute("aria-selected", on);
      t.tabIndex = on ? 0 : -1;
      document.getElementById(t.getAttribute("aria-controls")).hidden = !on;
    });
  }
  tabs.forEach(function (t, i) {
    t.addEventListener("click", function () { select(t); t.scrollIntoView({ block: "nearest", inline: "nearest" }); });
    t.addEventListener("keydown", function (e) {
      var j = e.key === "ArrowDown" || e.key === "ArrowRight" ? i + 1 : e.key === "ArrowUp" || e.key === "ArrowLeft" ? i - 1 : null;
      if (j === null) return;
      e.preventDefault();
      var next = tabs[(j + tabs.length) % tabs.length];
      select(next); next.focus();
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
