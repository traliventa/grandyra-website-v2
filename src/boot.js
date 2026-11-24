/* Runs before the first paint (loaded in <head>, tiny). It marks the page as JavaScript-enabled and flags a
   first visit, so the loading screen only ever appears once per session and never flashes on later pages.
   If main.js does not start, the page falls back to plain visible content after six seconds. */
(function () {
  var h = document.documentElement;
  h.classList.add("js");
  try { if (!sessionStorage.getItem("gy-seen")) h.classList.add("gy-first"); } catch (e) {}
  setTimeout(function () {
    if (!document.body || !document.body.classList.contains("ready")) h.classList.remove("js", "gy-first");
  }, 6000);
})();
