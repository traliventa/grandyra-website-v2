/* Grandyra — interaction layer. Depends on gsap, ScrollTrigger, Lenis (vendored). */
(function () {
  "use strict";
  var d = document, html = d.documentElement, body = d.body;
  var reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  var fine = matchMedia("(hover: hover) and (pointer: fine)").matches;
  var desktop = function () { return innerWidth > 900; };
  var hasGsap = !!(window.gsap && window.ScrollTrigger);
  html.classList.add("js");
  if (hasGsap) gsap.registerPlugin(ScrollTrigger);

  function store(k, v) { try { if (v === undefined) return sessionStorage.getItem(k); sessionStorage.setItem(k, v); } catch (e) { return null; } }

  /* ---------- Smooth scroll ---------- */
  var lenis = null;
  if (!reduce && window.Lenis && hasGsap) {
    lenis = new Lenis({ lerp: 0.09, smoothWheel: true });
    lenis.on("scroll", ScrollTrigger.update);
    gsap.ticker.add(function (t) { lenis.raf(t * 1000); });
    gsap.ticker.lagSmoothing(0);
  }

  /* ---------- Dhaka clock ---------- */
  function tick() {
    var s;
    try { s = new Intl.DateTimeFormat("en-GB", { timeZone: "Asia/Dhaka", hour: "2-digit", minute: "2-digit", hourCycle: "h23" }).format(new Date()); }
    catch (e) { var t = new Date(Date.now() + (new Date().getTimezoneOffset() + 360) * 60000); s = ("0" + t.getHours()).slice(-2) + ":" + ("0" + t.getMinutes()).slice(-2); }
    d.querySelectorAll("[data-clock]").forEach(function (el) { el.textContent = s; });
    html.classList.add("clock-ready");
  }
  tick(); setInterval(tick, 20000);
  d.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* ---------- Split words ---------- */
  function split(el) {
    if (el.dataset.done) return; el.dataset.done = 1;
    var walk = function (node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (n) {
        if (n.nodeType === 3) {
          var frag = d.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(function (part) {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(d.createTextNode(" ")); return; }
            var w = d.createElement("span"); w.className = "w";
            var i = d.createElement("span"); i.textContent = part; w.appendChild(i); frag.appendChild(w);
          });
          n.parentNode.replaceChild(frag, n);
        } else if (n.nodeType === 1 && !n.classList.contains("w") && !n.classList.contains("ph-text")) {
          walk(n);
        }
      });
    };
    walk(el);
  }

  /* ---------- Preloader ---------- */
  var loader = d.querySelector(".loader");
  var firstVisit = !store("gy-seen");
  function startPage() {
    body.classList.add("ready");
    if (!hasGsap || reduce) {
      d.querySelectorAll(".split .w > span, .fade").forEach(function (el) { el.style.transform = "none"; el.style.opacity = 1; });
      return;
    }
    revealIn();
  }
  if (loader && firstVisit && hasGsap && !reduce) {
    store("gy-seen", "1");
    var count = loader.querySelector(".count"), word = loader.querySelector(".word"), bar = loader.querySelector(".bar");
    var o = { v: 0 }, words = ["noise", "noise", "signal", "clarity", "greatness"];
    if (lenis) lenis.stop();
    var skipLoader = function () { if (tl) tl.progress(1); };
    ["pointerdown", "keydown"].forEach(function (ev) { d.addEventListener(ev, skipLoader, { once: true }); });
    var tl = gsap.to(o, {
      v: 100, duration: 1.0, ease: "power2.inOut",
      onUpdate: function () {
        var v = Math.round(o.v); count.textContent = ("00" + v).slice(-3);
        word.textContent = words[Math.min(words.length - 1, Math.floor(v / 21))];
        bar.style.transform = "scaleX(" + o.v / 100 + ")";
      },
      onComplete: function () {
        gsap.to(loader, { clipPath: "inset(0 0 100% 0)", duration: .8, ease: "expo.inOut", onComplete: function () { loader.remove(); if (lenis) lenis.start(); } });
        setTimeout(startPage, 250);
      }
    });
    loader.style.clipPath = "inset(0 0 0% 0)";
  } else {
    html.classList.add("no-loader");
    if (loader) loader.remove();
    enterCurtain();
  }

  /* ---------- Page transitions ---------- */
  var curtain = d.querySelector(".curtain");
  function enterCurtain() {
    if (!curtain || !hasGsap || reduce || !store("gy-leaving")) { startPage(); return; }
    store("gy-leaving", "");
    var bars = curtain.querySelectorAll("i");
    gsap.set(bars, { scaleY: 1, transformOrigin: "top" });
    gsap.to(bars, { scaleY: 0, duration: .75, ease: "expo.inOut", stagger: .05, onComplete: function () {} });
    setTimeout(startPage, 300);
  }
  if (curtain && hasGsap && !reduce) {
    d.addEventListener("click", function (e) {
      var a = e.target.closest("a"); if (!a) return;
      var href = a.getAttribute("href") || "";
      if (!/\.html(#.*)?$/.test(href) || a.target || e.metaKey || e.ctrlKey || e.shiftKey) return;
      e.preventDefault();
      store("gy-leaving", "1");
      var bars = curtain.querySelectorAll("i");
      gsap.set(bars, { transformOrigin: "bottom" });
      gsap.to(bars, { scaleY: 1, duration: .45, ease: "expo.inOut", stagger: .04, onComplete: function () { location.href = href; } });
    });
    addEventListener("pageshow", function (ev) { if (ev.persisted) gsap.set(curtain.querySelectorAll("i"), { scaleY: 0 }); });
  }

  /* ---------- Reveal-in on load + scroll ---------- */
  function revealIn() {
    d.querySelectorAll("[data-split]").forEach(function (el) {
      split(el); el.classList.add("split");
      var inner = el.querySelectorAll(".w > span");
      var trig = el.closest(".hero, .phero") ? null : { trigger: el, start: "top 88%" };
      gsap.to(inner, { y: 0, duration: 1.2, ease: "expo.out", stagger: 0.035, delay: trig ? 0 : 0.1, scrollTrigger: trig });
    });
    d.querySelectorAll(".fade").forEach(function (el) {
      gsap.to(el, { opacity: 1, y: 0, duration: 1.1, ease: "expo.out", scrollTrigger: el.closest(".hero, .phero") ? null : { trigger: el, start: "top 90%" }, delay: el.closest(".hero, .phero") ? .5 : 0 });
    });
    d.querySelectorAll(".imgr[data-reveal]").forEach(function (el) {
      var img = el.querySelector("img");
      var tl = gsap.timeline({ scrollTrigger: { trigger: el, start: "top 85%" } });
      tl.to(el, { clipPath: "inset(0% 0 0 0)", duration: 1.4, ease: "expo.inOut" })
        .to(img, { scale: 1, duration: 1.8, ease: "expo.out" }, "<.1");
      if (el.hasAttribute("data-parallax")) {
        gsap.fromTo(img, { yPercent: -6 }, { yPercent: 6, ease: "none", scrollTrigger: { trigger: el, scrub: true } });
      }
    });
    initScrub();
  }
  // safety: never leave content hidden
  setTimeout(function () { if (!body.classList.contains("ready")) startPage(); }, 4000);

  /* ---------- Manifesto word scrub ---------- */
  function initScrub() {
    var el = d.querySelector("[data-scrub]"); if (!el) return;
    var walk = function (node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (n) {
        if (n.nodeType === 3) {
          var frag = d.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(function (p) {
            if (!p) return;
            if (/^\s+$/.test(p)) { frag.appendChild(d.createTextNode(" ")); return; }
            var s = d.createElement("span"); s.className = "mw"; s.textContent = p; frag.appendChild(s);
          });
          n.parentNode.replaceChild(frag, n);
        } else if (n.nodeType === 1) walk(n);
      });
    };
    walk(el);
    var sec = el.closest(".manifesto") || el;
    // Dim the words only from 60% of a screen before the section appears until it has gone by.
    ScrollTrigger.create({ trigger: sec, start: "top bottom+=60%", end: "bottom top-=20%", toggleClass: { targets: sec, className: "dim" } });
    gsap.fromTo(el.querySelectorAll(".mw"), { opacity: 0.14 }, { opacity: 1, stagger: 0.08, ease: "none", immediateRender: false, scrollTrigger: { trigger: el, start: "top 78%", end: "bottom 45%", scrub: 0.6 } });
  }

  /* ---------- Menu ---------- */
  var menu = d.querySelector(".menu"), mbtn = d.querySelector(".menu-btn");
  if (menu && mbtn) {
    var open = false, pic = menu.querySelector(".pic img");
    var toggle = function () {
      open = !open; body.classList.toggle("menu-open", open);
      mbtn.setAttribute("aria-expanded", open); mbtn.querySelector(".lbl").textContent = open ? "Close" : "Menu";
      menu.setAttribute("aria-hidden", !open);
      if (open) setTimeout(function () { var f = menu.querySelector("nav a"); if (f) f.focus({ preventScroll: true }); }, 400); else mbtn.focus({ preventScroll: true });
      if (hasGsap && !reduce) {
        if (open) {
          gsap.set(menu, { visibility: "visible" });
          gsap.to(menu, { clipPath: "inset(0 0 0% 0)", duration: .9, ease: "expo.inOut" });
          gsap.fromTo(menu.querySelectorAll("nav .d"), { yPercent: 110 }, { yPercent: 0, duration: 1, ease: "expo.out", stagger: .06, delay: .35 });
          if (lenis) lenis.stop();
        } else {
          gsap.to(menu, { clipPath: "inset(0 0 100% 0)", duration: .8, ease: "expo.inOut", onComplete: function () { gsap.set(menu, { visibility: "hidden" }); } });
          if (lenis) lenis.start();
        }
      } else {
        menu.style.visibility = open ? "visible" : "hidden"; menu.style.clipPath = open ? "none" : "inset(0 0 100% 0)";
      }
    };
    mbtn.addEventListener("click", toggle);
    d.addEventListener("keydown", function (e) { if (e.key === "Escape" && open) toggle(); });
    menu.querySelectorAll("nav a").forEach(function (a) {
      a.addEventListener("mouseenter", function () { if (pic && a.dataset.img) pic.src = a.dataset.img; });
    });
  }

  /* ---------- Cursor ---------- */
  if (fine && !reduce) {
    var cur = d.createElement("div"); cur.className = "cur"; cur.innerHTML = '<div class="dot"><span></span></div>'; cur.setAttribute("aria-hidden", "true");
    body.appendChild(cur);
    var label = cur.querySelector("span"), cx = innerWidth / 2, cy = innerHeight / 2, tx = cx, ty = cy;
    var curRun = false;
    function curLoop() {
      cx += (tx - cx) * .2; cy += (ty - cy) * .2; cur.style.transform = "translate(" + cx + "px," + cy + "px)";
      if (Math.abs(tx - cx) > .1 || Math.abs(ty - cy) > .1) requestAnimationFrame(curLoop); else curRun = false; // idle: stop the loop
    }
    addEventListener("mousemove", function (e) { tx = e.clientX; ty = e.clientY; if (!curRun) { curRun = true; requestAnimationFrame(curLoop); } }, { passive: true });
    d.addEventListener("mouseover", function (e) {
      var t = e.target.closest("[data-cursor]");
      if (t) { label.textContent = t.dataset.cursor; cur.classList.add("big"); }
      else cur.classList.remove("big");
    });
  }

  /* ---------- Magnetic ---------- */
  if (fine && !reduce && hasGsap) {
    d.querySelectorAll("[data-magnetic]").forEach(function (el) {
      el.addEventListener("mousemove", function (e) {
        var r = el.getBoundingClientRect();
        gsap.to(el, { x: (e.clientX - r.left - r.width / 2) * .35, y: (e.clientY - r.top - r.height / 2) * .35, duration: .6, ease: "power3.out" });
      });
      el.addEventListener("mouseleave", function () { gsap.to(el, { x: 0, y: 0, duration: .9, ease: "elastic.out(1,.4)" }); });
    });
  }

  /* ---------- Hero: noise → GRANDYRA ---------- */
  var cv = d.getElementById("noise");
  if (cv) {
    var ctx = cv.getContext("2d"), W, H, dpr = Math.min(devicePixelRatio || 1, 1.5), parts = [], progress = reduce ? 1 : 0, mouse = { x: -9999, y: -9999 };
    var COLS = ["#FF4F2B", "#19B5BC", "#C5A880", "#EEE9DF", "#0C7D84", "#8A6CF0"];
    var meter = d.querySelector(".hero .meter i"), stateEl = d.querySelector(".hero .state span");
    function targets() {
      var SC = 0.25, o = d.createElement("canvas"), oc = o.getContext("2d", { willReadFrequently: true });
      var tw = Math.min(W * (W < 700 ? 0.92 : 0.78), 1250), fs = tw / 4.1;
      o.width = Math.ceil(W * SC); o.height = Math.ceil(H * SC); oc.scale(SC, SC);
      oc.fillStyle = "#fff"; oc.textAlign = "center"; oc.textBaseline = "middle";
      oc.font = "condensed 800 " + fs + "px Archivo";
      try { oc.fontStretch = "extra-condensed"; } catch (e) {}
      oc.font = "800 " + fs + "px Archivo"; try { oc.fontStretch = "condensed"; } catch (e) {}
      var cyT = W < 700 ? H * 0.36 : H * 0.36;
      oc.fillText("GRANDYRA", W / 2, cyT);
      var ow = o.width, data = oc.getImageData(0, 0, ow, o.height).data, pts = [];
      for (var y = 0; y < o.height; y++) for (var x = 0; x < ow; x++) if (data[(y * ow + x) * 4 + 3] > 110) pts.push([x / SC + Math.random() * 3, y / SC + Math.random() * 3]);
      return pts;
    }
    function build() {
      W = cv.clientWidth; H = cv.clientHeight;
      if (!W || !H) { parts = []; setTimeout(build, 400); return; } // not laid out yet (hidden tab, resize): try again
      cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var weak = W < 700 || (navigator.hardwareConcurrency || 4) <= 4;
      var pts = targets(), max = weak ? 2200 : 4200;
      for (var i = pts.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = pts[i]; pts[i] = pts[j]; pts[j] = t; }
      pts = pts.slice(0, max);
      parts = pts.map(function (p, i) {
        return { tx: p[0], ty: p[1], x: Math.random() * W, y: Math.random() * H, ox: Math.random() * W, oy: Math.random() * H,
          s: Math.random() * 2.2 + 1.4, c: COLS[i % COLS.length], ph: Math.random() * 6.28, sp: .3 + Math.random() * .7, gold: Math.random() < .12, vx: 0, vy: 0 };
      });
    }
    function ease(t) { return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }
    var time = 0;
    function frame() {
      time += 0.008;
      ctx.clearRect(0, 0, W, H);
      var e = ease(Math.min(1, Math.max(0, progress)));
      for (var i = 0; i < parts.length; i++) {
        var p = parts[i];
        var nx = p.ox + Math.sin(time * p.sp + p.ph) * 60 + Math.cos(time * .7 + p.ph * 2) * 40;
        var ny = p.oy + Math.cos(time * p.sp + p.ph) * 60 + Math.sin(time * .5 + p.ph) * 40;
        var gx = nx + (p.tx - nx) * e, gy = ny + (p.ty - ny) * e;
        var dx = gx - mouse.x, dy = gy - mouse.y, dist = dx * dx + dy * dy;
        if (dist < 14000) { var f = (14000 - dist) / 14000 * 2.2; p.vx += dx * f * .02; p.vy += dy * f * .02; }
        p.vx *= .86; p.vy *= .86;
        p.x += (gx - p.x) * .12 + p.vx; p.y += (gy - p.y) * .12 + p.vy;
        var col = e > .6 ? (p.gold ? "#C5A880" : "#EEE9DF") : p.c;
        ctx.globalAlpha = .8 + .2 * e;
        ctx.fillStyle = col;
        var s = p.s * (1 - e * .25);
        ctx.fillRect(p.x, p.y, s, s);
      }
      ctx.globalAlpha = 1;
      if (meter) meter.style.transform = "scaleX(" + Math.min(1, progress) + ")";
      if (stateEl) stateEl.textContent = progress < .15 ? "Noise" : progress < .85 ? "Finding the signal" : "Clarity";
      if (!reduce && heroVisible) requestAnimationFrame(frame); else running = false;
    }
    var heroVisible = true, running = false;
    function startFrames() { if (!running) { running = true; frame(); } }
    if ("IntersectionObserver" in window) new IntersectionObserver(function (en) { heroVisible = en[0].isIntersecting; if (heroVisible) startFrames(); }).observe(cv.parentElement);
    d.addEventListener("visibilitychange", function () { heroVisible = !d.hidden && heroVisible; if (!d.hidden) { heroVisible = true; startFrames(); } });
    var ready = d.fonts && d.fonts.load ? d.fonts.load("800 100px Archivo") : Promise.resolve();
    var idle = window.requestIdleCallback || function (f) { return setTimeout(f, 200); };
    ready.then(function () { return new Promise(function (r) { idle(r, { timeout: 1200 }); }); }).then(function () {
      build(); startFrames();
      if (hasGsap && !reduce) {
        var st = ScrollTrigger.create({ trigger: ".hero", start: "top top", end: "+=" + (innerHeight * 1.1), pin: true, scrub: true,
          refreshPriority: 10, onUpdate: function (s) { progress = s.progress * 1.15; } });
        ScrollTrigger.sort(); ScrollTrigger.refresh();
        // auto-tease: if user doesn't scroll in 2.5s, briefly hint the formation
        setTimeout(function () { if (scrollY < 10 && progress < .05) { var o = { p: 0 }; gsap.to(o, { p: .35, duration: 1.4, yoyo: true, repeat: 1, ease: "sine.inOut", onUpdate: function () { if (scrollY < 10) progress = o.p; } }); } }, 3200);
      }
    });
    var rt; addEventListener("resize", function () { clearTimeout(rt); rt = setTimeout(build, 250); });
    cv.parentElement.addEventListener("mousemove", function (e) { var r = cv.getBoundingClientRect(); mouse.x = e.clientX - r.left; mouse.y = e.clientY - r.top; });
    cv.parentElement.addEventListener("mouseleave", function () { mouse.x = mouse.y = -9999; });
  }

  /* ---------- Horizontal work ---------- */
  var hw = d.querySelector(".hwork");
  if (hw && hasGsap && !reduce) {
    var mm = gsap.matchMedia();
    mm.add("(min-width: 901px)", function () {
      var track = hw.querySelector(".track"), countEl = hw.querySelector("[data-count]"), cards = hw.querySelectorAll(".card");
      var dist = function () { return track.scrollWidth - innerWidth; };
      var tw = gsap.to(track, { x: function () { return -dist(); }, ease: "none",
        scrollTrigger: { trigger: hw, start: "top top", end: function () { return "+=" + dist(); }, pin: true, scrub: 1, invalidateOnRefresh: true,
          onUpdate: function (s) { var i = Math.min(cards.length, Math.max(1, Math.round(s.progress * (cards.length - 1)) + 1)); if (countEl) countEl.textContent = ("0" + i).slice(-2); } } });
      cards.forEach(function (c) {
        var img = c.querySelector("img");
        if (!img) return;
        gsap.fromTo(img, { xPercent: -8, scale: 1.15 }, { xPercent: 8, ease: "none", scrollTrigger: { trigger: c, containerAnimation: tw, start: "left right", end: "right left", scrub: true } });
      });
    });
  }

  /* ---------- Needs: hover image follow ---------- */
  var fl = d.querySelector(".float-img");
  if (fl && fine && hasGsap && !reduce) {
    var flimg = fl.querySelector("img"), xTo = gsap.quickTo(fl, "x", { duration: .6, ease: "power3" }), yTo = gsap.quickTo(fl, "y", { duration: .6, ease: "power3" });
    d.querySelectorAll(".need").forEach(function (n) {
      n.addEventListener("mouseenter", function (e) { flimg.src = n.dataset.img; gsap.set(fl, { x: e.clientX + 170, y: e.clientY }); gsap.to(fl, { opacity: 1, scale: 1, rotate: 0, duration: .6, ease: "expo.out" }); });
      n.addEventListener("mouseleave", function () { gsap.to(fl, { opacity: 0, scale: .6, rotate: -6, duration: .4 }); });
      n.addEventListener("mousemove", function (e) { xTo(e.clientX + 170); yTo(e.clientY); });
    });
  }

  if (fl) addEventListener("scroll", function () { gsap && gsap.to(fl, { opacity: 0, scale: .6, duration: .3 }); }, { passive: true });

  /* ---------- Marquee (velocity reactive) ---------- */
  d.querySelectorAll(".marquee .row").forEach(function (row) {
    if (!hasGsap || reduce) return;
    var dir = row.classList.contains("alt") ? 1 : -1;
    var w = row.scrollWidth / 2;
    var tween = gsap.fromTo(row, { x: dir < 0 ? 0 : -w }, { x: dir < 0 ? -w : 0, duration: 38, ease: "none", repeat: -1 });
    if (lenis) lenis.on("scroll", function (e) { var v = Math.min(4, Math.abs(e.velocity) / 6 + 1); gsap.to(tween, { timeScale: v, duration: .3, overwrite: true, onComplete: function () { gsap.to(tween, { timeScale: 1, duration: 1.2 }); } }); });
  });

  /* ---------- Journal cover tilt ---------- */
  if (fine && !reduce) {
    d.querySelectorAll(".cover").forEach(function (c) {
      c.addEventListener("mousemove", function (e) { var r = c.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5; c.style.transform = "rotateY(" + x * 12 + "deg) rotateX(" + -y * 12 + "deg) translateZ(10px)"; });
      c.addEventListener("mouseleave", function () { c.style.transform = ""; });
    });
  }

  /* ---------- Work filters ---------- */
  var fbtns = d.querySelectorAll(".filters button");
  fbtns.forEach(function (b) {
    b.addEventListener("click", function () {
      fbtns.forEach(function (x) { x.setAttribute("aria-pressed", x === b); });
      var f = b.dataset.f;
      d.querySelectorAll(".wgrid .wc").forEach(function (c) { c.classList.toggle("off", f !== "all" && c.dataset.cat !== f); });
    });
  });

  /* ---------- Reading progress ---------- */
  var prog = d.querySelector(".progress");
  if (prog) addEventListener("scroll", function () { var h = d.documentElement.scrollHeight - innerHeight; prog.style.transform = "scaleX(" + (h > 0 ? scrollY / h : 0) + ")"; }, { passive: true });

  /* ---------- Copy email ---------- */
  d.querySelectorAll("[data-copy]").forEach(function (b) {
    b.addEventListener("click", function () {
      var hint = b.querySelector(".hint") || b;
      var done = function (ok) { hint.textContent = ok ? "Copied" : "Select to copy"; setTimeout(function () { hint.textContent = "Copy"; }, 1800); };
      try { navigator.clipboard.writeText(b.dataset.copy).then(function () { done(true); }, function () { done(false); }); } catch (e) { done(false); }
    });
  });

  /* ---------- Inquiry form ---------- */
  // No server here: the form opens the visitor's email app with the message ready,
  // addressed to data-to. If you add an inbox service later, set data-endpoint and it will POST instead.
  var form = d.querySelector("form[data-inquiry]");
  if (form) {
    var status = form.querySelector(".status");
    var say = function (msg, bad) { status.textContent = msg; status.classList.add("on"); status.classList.toggle("err-state", !!bad); };
    var msgs = { name: "Enter your name.", email: "Enter an email address we can reply to, like name@company.com.", message: "Tell us a little about what you're building." };
    var check = function (f) {
      var err = d.getElementById(f.getAttribute("aria-describedby")); if (!err) return true;
      var ok = f.checkValidity();
      f.setAttribute("aria-invalid", ok ? "false" : "true");
      err.textContent = ok ? "" : (f.validity.typeMismatch && f.value ? "That email address doesn't look right. Check it and try again." : msgs[f.name] || "This field is required.");
      return ok;
    };
    form.querySelectorAll("[required]").forEach(function (f) { f.addEventListener("blur", function () { check(f); }); f.addEventListener("input", function () { if (f.getAttribute("aria-invalid") === "true") check(f); }); });
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var bad = null;
      form.querySelectorAll("[required]").forEach(function (f) { if (!check(f) && !bad) bad = f; });
      if (bad) { bad.focus(); return; }
      var fd = new FormData(form), ep = form.getAttribute("data-endpoint"), to = form.getAttribute("data-to");
      if (fd.get("_gotcha")) return; // honeypot: bots fill the hidden field
      var services = fd.getAll("services").join(", ");
      if (ep) {
        fetch(ep, { method: "POST", body: fd, headers: { Accept: "application/json" } })
          .then(function (r) { if (!r.ok) throw 0; say("Message sent. We'll reply to " + fd.get("email") + " personally."); form.reset(); })
          .catch(function () { say("The message didn't send. Email us at " + to + " and we'll pick it up from there.", true); });
        return;
      }
      var body = "Name: " + fd.get("name") + "\nCompany: " + (fd.get("company") || "-") + "\nEmail: " + fd.get("email") + "\nNeeds: " + (services || "-") + "\n\n" + fd.get("message");
      location.href = "mailto:" + to + "?subject=" + encodeURIComponent("New project enquiry from " + fd.get("name")) + "&body=" + encodeURIComponent(body);
      say("Your email app should open with this message ready to send. If it doesn't, write to " + to + " and paste it in.");
    });
  }

  /* ---------- Text scramble on hover ---------- */
  if (fine && !reduce) {
    var CH = "GRANDYR*#/<>+=01";
    d.querySelectorAll(".hdr .label, .pill").forEach(function (el) {
      var tn = Array.prototype.find.call(el.childNodes, function (n) { return n.nodeType === 3 && n.textContent.trim(); });
      if (!tn) return;
      var orig = tn.textContent, busy = false;
      el.addEventListener("mouseenter", function () {
        if (busy) return; busy = true; var f = 0, total = 14;
        (function step() {
          tn.textContent = orig.replace(/\S/g, function (c, i) { return i < (f / total) * orig.length ? c : CH[Math.floor(Math.random() * CH.length)]; });
          if (++f <= total) requestAnimationFrame(step); else { tn.textContent = orig; busy = false; }
        })();
      });
    });
  }

  /* ---------- Velocity skew on imagery ---------- */
  if (lenis && hasGsap) {
    var skewEls = d.querySelectorAll(".hwork .card .imgr, .wgrid .wc .imgr, .cover-band .imgr");
    var setters = Array.prototype.map.call(skewEls, function (el) { return gsap.quickTo(el, "skewY", { duration: .6, ease: "power3" }); });
    lenis.on("scroll", function (e) { var s = Math.max(-2, Math.min(2, e.velocity * 0.07)); setters.forEach(function (f) { f(s); }); });
  }

  addEventListener("load", function () {
    if (hasGsap) ScrollTrigger.refresh();
    // The menu picture and the hover preview are not needed to paint the page: fetch them once everything else is done.
    (window.requestIdleCallback || function (f) { setTimeout(f, 300); })(function () {
      d.querySelectorAll("img[data-src]").forEach(function (im) { im.src = im.getAttribute("data-src"); });
    });
  });
})();
