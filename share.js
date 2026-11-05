/* Share menu for all pages. One file, no third-party scripts, no tracking.
   - window.shareMenu(button, url, title): phones open the system share sheet; other screens open a small menu
     with Copy link, LinkedIn, X, Facebook and WhatsApp.
   - On Teams and Clubs pages, adds a Share button to the tab bar; on Teams, a small share icon on each team that has a roster. */
(function () {
  var css = ".shm{position:absolute;z-index:50;min-width:176px;background:var(--surface,#fff);color:var(--fg,#13202f);border:1px solid var(--line,#d3dae3);border-radius:6px;box-shadow:0 6px 22px rgba(0,0,0,.18);padding:4px;display:flex;flex-direction:column}" +
    ".shm a,.shm button{font:500 14px var(--sans,inherit);color:inherit;text-decoration:none;text-align:left;background:none;border:0;border-radius:4px;padding:9px 12px;cursor:pointer}" +
    ".shm a:hover,.shm button:hover,.shm a:focus-visible,.shm button:focus-visible{background:var(--chip,#e3e9f1);outline:none}" +
    ".tabs .wrap .shb{margin-left:auto;font:500 13px var(--mono,inherit);letter-spacing:.08em;text-transform:uppercase;color:var(--accent,#1b3a63);background:transparent;border:1px solid var(--accent,#1b3a63);border-radius:3px;padding:7px 14px;cursor:pointer}" +
    ".tabs .wrap .shb:hover{background:var(--accent,#1b3a63);color:var(--bg,#fff)}" +
    ".soc button.si{display:inline-flex;align-items:center;justify-content:center;width:30px;height:30px;padding:0;border:1px solid var(--line,#d3dae3);border-radius:50%;color:var(--accent,#1b3a63);background:transparent;cursor:pointer}" +
    ".soc button.si:hover,.soc button.si:focus-visible{background:var(--chip,#e3e9f1)}";
  var st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);

  var openMenu = null;
  function closeMenu() { if (openMenu) { openMenu.remove(); openMenu = null; } }
  document.addEventListener("click", function (e) { if (openMenu && !openMenu.contains(e.target) && !e.target.closest("[data-share]")) closeMenu(); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeMenu(); });

  function copy(text) {
    return (navigator.clipboard && navigator.clipboard.writeText ? navigator.clipboard.writeText(text) : Promise.reject())
      .then(function () { return true; }, function () {
        var ta = document.createElement("textarea"); ta.value = text; document.body.appendChild(ta); ta.select();
        var ok = false; try { ok = document.execCommand("copy"); } catch (_) {}
        ta.remove(); return ok;
      });
  }

  window.shareMenu = function (btn, url, title) {
    var touch = window.matchMedia && matchMedia("(pointer:coarse)").matches;
    if (touch && navigator.share) {
      navigator.share({ title: title, url: url }).catch(function () {});
      return;
    }
    if (openMenu && openMenu.__for === btn) { closeMenu(); return; }
    closeMenu();
    var u = encodeURIComponent(url), t = encodeURIComponent(title);
    var m = document.createElement("div"); m.className = "shm"; m.setAttribute("role", "menu"); m.__for = btn;
    var c = document.createElement("button"); c.type = "button"; c.textContent = "Copy link"; c.setAttribute("role", "menuitem");
    c.addEventListener("click", function () {
      copy(url).then(function (ok) { c.textContent = ok ? "Link copied" : "Copy: " + url; setTimeout(closeMenu, ok ? 900 : 5000); });
    });
    m.appendChild(c);
    [["LinkedIn", "https://www.linkedin.com/sharing/share-offsite/?url=" + u],
     ["X", "https://twitter.com/intent/tweet?url=" + u + "&text=" + t],
     ["Facebook", "https://www.facebook.com/sharer/sharer.php?u=" + u],
     ["WhatsApp", "https://wa.me/?text=" + t + "%20" + u]].forEach(function (p) {
      var a = document.createElement("a"); a.href = p[1]; a.target = "_blank"; a.rel = "noopener"; a.textContent = p[0]; a.setAttribute("role", "menuitem");
      a.addEventListener("click", function () { setTimeout(closeMenu, 50); });
      m.appendChild(a);
    });
    document.body.appendChild(m);
    var r = btn.getBoundingClientRect(), w = m.offsetWidth;
    var left = Math.min(Math.max(8, r.left + window.scrollX), window.scrollX + document.documentElement.clientWidth - w - 8);
    m.style.left = left + "px"; m.style.top = (r.bottom + window.scrollY + 6) + "px";
    openMenu = m;
    var first = m.querySelector("button,a"); if (first) first.focus();
  };

  function bind(btn, urlFn, titleFn) {
    btn.setAttribute("data-share", ""); btn.setAttribute("aria-haspopup", "menu");
    btn.addEventListener("click", function () { window.shareMenu(btn, urlFn(), titleFn()); });
  }

  document.addEventListener("DOMContentLoaded", function () {
    var site = "Canadian University Baseball Database";
    // Tab-bar Share button on Teams and Clubs (the Players page keeps its own button in the filter bar).
    var wrap = document.querySelector(".tabs .wrap");
    if (wrap && !document.getElementById("share")) {
      var b = document.createElement("button"); b.type = "button"; b.className = "shb"; b.textContent = "Share";
      var page = document.title.replace(/^Canadian University Baseball\s*/, "") || "";
      bind(b, function () { return location.origin + location.pathname; }, function () { return site + (page ? " - " + page : ""); });
      wrap.appendChild(b);
    }
    // Teams page: a small share icon on every team that has a roster.
    if (/teams\.html$/.test(location.pathname)) document.querySelectorAll(".tc").forEach(function (card) {
      var pl = card.querySelector("a.pl"); if (!pl) return;
      var name = (card.querySelector("h3") || {}).textContent || "";
      var lk = card.querySelector(".lk"); if (!lk) return;
      var soc = lk.querySelector(".soc");
      if (!soc) { soc = document.createElement("span"); soc.className = "soc"; lk.appendChild(soc); }
      var s = document.createElement("button"); s.type = "button"; s.className = "si";
      s.setAttribute("aria-label", "Share the " + name + " roster"); s.title = "Share this roster";
      s.innerHTML = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="M8.6 10.5l6.8-4M8.6 13.5l6.8 4"/></svg>';
      bind(s, function () { return new URL(pl.getAttribute("href"), location.href).href; }, function () { return name + " baseball roster - " + site; });
      soc.appendChild(s);
    });
  });
})();
