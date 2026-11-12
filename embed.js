/* Embed mode for sites that show a page of this database inside their own page.
   Only active when the address carries ?embed=cbn. Adds the credit line under the sponsor strip,
   and keeps ?embed=cbn on links inside the site so the credit stays as a visitor moves between pages.
   Normal visits are unaffected. No third-party scripts, no tracking. */
(function () {
  var P;
  try { P = new URLSearchParams(location.search); } catch (e) { return; }
  if (P.get("embed") !== "cbn") return;

  var rs = history.replaceState;
  history.replaceState = function (s, t, u) {
    try {
      if (typeof u === "string") {
        var x = new URL(u, location.href);
        x.searchParams.set("embed", "cbn");
        u = x.pathname + x.search + x.hash;
      }
    } catch (e) {}
    return rs.call(history, s, t, u);
  };

  function ready(f) {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", f); else f();
  }
  ready(function () {
    var d = document.createElement("div");
    d.className = "cbn-credit";
    d.setAttribute("role", "note");
    d.textContent = "Compiled for Canadian Baseball Network by Wayne E. Yang";
    d.style.cssText = "background:var(--chip,#eef2f7);border-bottom:1px solid var(--line,#d3dae3);color:var(--fg,#13202f);font:500 13px var(--mono,monospace);letter-spacing:.06em;padding:8px 20px;text-align:center";
    var spon = document.querySelector(".spon");
    if (spon && spon.parentNode) spon.parentNode.insertBefore(d, spon.nextSibling);
    else document.body.insertBefore(d, document.body.firstChild);
  });

  document.addEventListener("click", function (e) {
    var a = e.target && e.target.closest ? e.target.closest("a[href]") : null;
    if (!a) return;
    var h = a.getAttribute("href");
    if (!h || /^(mailto:|tel:|javascript:|#)/i.test(h)) return;
    try {
      var u = new URL(h, location.href);
      if (u.origin !== location.origin) return;
      u.searchParams.set("embed", "cbn");
      a.setAttribute("href", u.pathname + u.search + u.hash);
    } catch (err) {}
  }, true);
})();
