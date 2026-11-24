#!/usr/bin/env python3
"""Grandyra site generator — 'Noise → Greatness' direction."""
import json, os, re, sys, html, shutil, datetime

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools"))
import legacy_data as old  # reuse verified copy: SERVICES, WORK, ISSUES, P()

P = old.P
# Production URL. Override for staging: SITE_URL=https://staging.example.com python3 build.py
BASE = os.environ.get("SITE_URL", "https://grandyra.com").rstrip("/")
# PREVIEW=1 builds a private review copy that search engines are told to ignore.
PREVIEW = os.environ.get("PREVIEW") == "1"
ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "site")
PAGES = []

SERVICES = old.SERVICES
# Services that do not appear in Grandyra's own documents yet. HOLD_UNVERIFIED=1 python3 build.py leaves them out
# (pages, menu, footer, form options, sitemap) until the company confirms them. See docs/CONTENT-VERIFICATION.md.
UNVERIFIED = {"packaging-design", "brand-launch", "rebranding", "retainer-partnership"}
if os.environ.get("HOLD_UNVERIFIED") == "1":
    SERVICES = [s for s in SERVICES if s["slug"] not in UNVERIFIED]
SVC = {s["slug"]: s for s in SERVICES}
NWORD = {10: "Ten", 6: "Six"}.get(len(SERVICES), str(len(SERVICES)))
NEED = {
    "brand-identity-design": ("Start something new", "#FF4F2B"),
    "rebranding": ("Outgrow your brand", "#19B5BC"),
    "brand-launch": ("Make an entrance", "#C5A880"),
    "packaging-design": ("Win the shelf", "#FF4F2B"),
    "advertising-agency": ("Be remembered", "#19B5BC"),
    "brand-marketing": ("Stay consistent", "#C5A880"),
    "pr-agency": ("Be trusted", "#FF4F2B"),
    "event-management": ("Bring people together", "#19B5BC"),
    "corporate-training": ("Build from within", "#C5A880"),
    "retainer-partnership": ("Go the distance", "#FF4F2B"),
}
THEME = {"brand-identity-design": "t-ink", "rebranding": "t-deep", "brand-launch": "t-verm", "packaging-design": "t-gold",
         "advertising-agency": "t-ink", "brand-marketing": "t-teal", "pr-agency": "t-ink", "event-management": "t-plum",
         "corporate-training": "t-deep", "retainer-partnership": "t-ink"}

EMAIL = "info@grandyra.com"
# Set to a form service URL (Formspree, Basin, Web3Forms...) to turn the contact form into a real online form.
FORM_ENDPOINT = ""
ADDRESS = "House 7, Road 4, Gulshan-1, Dhaka, Bangladesh"

# Real projects. Every fact below is taken from Grandyra's own profile, master presentation and Futsal deck.
# Items marked CONFIRM are listed in LAUNCH-CHECKLIST.md for company sign-off.
WORK = [
    dict(no="01", href="work-real-estate-futsal-2026.html", title="Real Estate Futsal 2026", tagline="Official creative partner for a 16-team tournament at ISD, Dhaka",
         disc="Identity, trophies, venue and campaign", year="2026", cat="events", img="futsal-hero", real=True),
    dict(no="02", href="work-souk-taban.html", title="Souk Taban", tagline="A brand and spatial identity for a three-day marketplace at SC Club, Banani",
         disc="Brand identity, environmental graphics, spatial typography, event collateral, digital assets", year="2026", cat="brand",
         stat="2,000+", statlabel="visitors over three days", theme="t-teal",
         photo=("souk-hero", 1330, 650, "Souk Taban brand sign on a patterned dark ground, reading SC Club, Banani, 30 April to 2 May 2026"),
         stats=[("2,000+", "visitors over three days")],
         gallery=[("souk-stall", 1000, 964, "A Motka Painting stall at Souk Taban, with a printed banner and hand-painted pots", "A Motka Painting stall at the market")],
         lede="A unified brand and spatial identity that turned a marketplace into a memorable cultural destination.",
         body=["Souk Taban ran for three days at SC Club, Banani. Grandyra was asked for a complete branding and experiential vision, from the brand guide and visual language to the spatial strategy of the venue.",
               "Signage, typography and wayfinding were designed as one system, so visitors moved through the venue inside a single, consistent identity."],
         did=["Brand identity", "Environmental graphics", "Spatial typography", "Event collateral", "Digital brand assets"],
         facts=[("Role", "Brand and experience design"), ("Venue", "SC Club, Banani"), ("When", "30 April – 2 May 2026"), ("Result", "2,000+ visitors")],
         result=""),
    dict(no="03", href="work-seheri-nights.html", title="Seheri Nights", tagline="A Ramadan night market at ICCB, Dhaka, running from Iftaar to Seheri",
         disc="Brand identity, vendor communication system, promotional campaign", year="", cat="events",
         stat="10,000+", statlabel="attendees over two nights, with 40+ food vendors", theme="t-plum",
         photo=("seheri-crowd", 961, 471, "A crowd filling the market hall during Seheri Nights, seen from above"),
         stats=[("10,000+", "attendees over two nights"), ("40+", "culinary vendors")], note="Record nightly attendance.", hero_max=1000,
         gallery=[("seheri-team", 631, 770, "Four people posing together at the Seheri Nights market", "")],
         lede="A night market built around Ramadan evenings, held together by one identity from Iftaar to Seheri.",
         body=["Seheri Nights brought food, culture and community together in a lively open-air experience at ICCB, Dhaka.",
               "The market was shaped around Ramadan nights: lighting zones, vendor guidelines, signage and small spaces to gather in. Every touchpoint was designed to encourage connection and celebration."],
         did=["Brand identity", "Vendor communication system", "Promotional campaign"],
         facts=[("Role", "Brand and communication design"), ("Venue", "ICCB, Dhaka"), ("Format", "Open-air night market"), ("Result", "10,000+ attendees")],
         result=""),
    dict(no="04", href="work-the-audio-expo.html", title="The Audio Expo", tagline="A listening experience for audiophiles, made with Gears For Ears",
         disc="Creative direction, identity, environmental design, experience planning", year="2025", cat="events",
         stat="First", statlabel="ever audiophile meetup", theme="t-verm",
         photo=("audio-booth", 1800, 868, "The Audio Expo backdrop above a row of headphones and listening gear"),
         stats=[("First", "ever audiophile meetup")],
         gallery=[("audio-table", 1008, 1231, "A display table of audio products at The Audio Expo, with banners behind", "")],
         lede="A high-end listening experience that brought sound, technology and design together under one roof.",
         body=["Inspired by leading international audio exhibitions, The Audio Expo gave music enthusiasts and industry-leading brands an immersive place to meet.",
               "The floor was laid out in layers, with loudspeakers, IEMs, headphones and DAC/amps, so every visitor could move from one way of listening to the next. The experience was benchmarked to CanJam."],
         did=["Creative direction", "Brand identity", "Environmental design", "Experience planning"],
         facts=[("Role", "Creative direction and identity"), ("With", "Gears For Ears"), ("Year", "2025"), ("Result", "First audiophile meetup")],
         result="Strong engagement from the industry."),
    dict(no="05", href="work-first-momentum.html", title="First Momentum", tagline="Electromechanical Expo Dhaka, organised by Grandyra at Aloki, Dhaka",
         disc="Expo organised by Grandyra", year="Upcoming", cat="events",
         stat="26–28 Jan", statlabel="2027, at Aloki, Dhaka", theme="t-gold", img="first-momentum", poster=True,
         lede="An expo that Grandyra is organising, bringing the people who build with the brands that equip them.",
         body=["First Momentum is the Electromechanical Expo Dhaka. It is a platform that brings developers, architects, MEP consultants, regulators and students together with elevator, HVAC, generator and solar brands.",
               "Unlike our other projects, this one is organised by Grandyra itself."],
         did=[],
         facts=[("Role", "Organiser"), ("Venue", "Aloki, Dhaka"), ("When", "26–28 January 2027"), ("Status", "Upcoming")],
         result=""),
]

ISSUES = [
    dict(no="01", slug="journal-strategy-before-decoration.html", title="Strategy before decoration", topic="Brand creation", theme="t-ink", img="svc-retainer-partnership"),
    dict(no="02", slug="journal-when-to-rebrand.html", title="When should a company rebrand?", topic="Brand refresh", theme="t-deep", img="svc-rebranding"),
]

PHOTOS = {
    "festival": ("photo-1767330855011-fc628d33caea", "Samiul Haque Bhuyan", "samiulhaquebhuyan", "Pohela Boishakh procession in Dhaka with colourful masks"),
    "dhaka": ("photo-1748353671829-f64d0aa1bc51", "Serzill Hasan", "serzill", "Aerial view of Uttara, Dhaka, at sunset"),
    "buriganga": ("photo-1788888106259-270e33a79d02", "Anik Roy", "anik_roy", "Wooden boats crossing the Buriganga river in Dhaka"),
    "rickshaw": ("photo-1695374345839-a6869ae9d6c1", "Sadnan Bashar", "sadnanbashar", "A rickshaw puller resting between rides on a Dhaka street"),
    "swatches": ("photo-1716471330463-f475b00f0506", "Andy Brown", "basallt", "Colour swatch cards on a designer's desk"),
    "sketches": ("photo-1629752187687-3d3c7ea3a21b", "Hal Gatewood", "halacious", "Hand-drawn layout sketches"),
    "pantone": ("photo-1581079289196-67865ea83118", "Mika Baumeister", "kommumikation", "A fan deck of printed colour swatches"),
    "stage": ("photo-1470229722913-7c0e2dbbafd3", "Yvette de Wit", "yvettedewit", "Stage lights over an audience at a live event"),
    "press": ("photo-1503694978374-8a2fa686963a", "Bank Phrom", "bank_phrom", "An offset printing press in motion"),
}
UTM = "?utm_source=grandyra&utm_medium=referral"


def photo(key, fallback, cls="", reveal=True, parallax=False, sizes="(max-width: 900px) 100vw, 60vw", eager=False):
    pid, name, user, alt = PHOTOS[key]
    base = f"assets/img/photo-{key}"
    r = " data-reveal" if reveal else ""
    p = " data-parallax" if parallax else ""
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    credit = (f'<span class="tag credit">Photo: <a href="https://unsplash.com/@{user}{UTM}" rel="noopener">{name}</a> / '
              f'<a href="https://unsplash.com/{UTM}" rel="noopener">Unsplash</a></span>')
    return (f'<div class="imgr {cls}"{r}{p}>{credit}<img src="{base}.webp" srcset="{base}-sm.webp 800w, {base}.webp 1600w" '
            f'sizes="{sizes}" width="1600" height="1067" alt="{html.escape(alt)}" {load}></div>')

SVC_PHOTO = {"brand-identity-design": "swatches", "rebranding": "sketches", "brand-launch": "festival", "packaging-design": "pantone",
             "advertising-agency": "press", "brand-marketing": "dhaka", "event-management": "stage"}
SHOW_DRAFT = False  # True shows sections still waiting for real Grandyra content


def icon(name, cls="ic"):
    svg = open(os.path.join(ROOT, "node_modules/lucide-static/icons", name + ".svg")).read()
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S).strip()
    svg = re.sub(r'\s(class|width|height)="[^"]*"', "", svg)
    svg = svg.replace("<svg", f'<svg class="{cls}" aria-hidden="true" focusable="false"', 1).replace('stroke-width="2"', 'stroke-width="1.5"')
    return svg


ICON = {"brand-identity-design": "sparkles", "rebranding": "refresh-cw", "brand-launch": "rocket", "packaging-design": "package",
        "advertising-agency": "megaphone", "brand-marketing": "trending-up", "pr-agency": "mic", "event-management": "calendar-heart",
        "corporate-training": "graduation-cap", "retainer-partnership": "handshake"}

STAR = '<svg class="star" viewBox="0 0 100 100" aria-hidden="true"><path fill="currentColor" d="M50 0l7 36 36-14-29 25 36 14-37-4 9 37-22-31-22 31 9-37-37 4 36-14L7 22l36 14z"/></svg>'


def img(name, alt, cls="", reveal=True, parallax=False, tag=True, sizes="(max-width: 900px) 100vw, 60vw", eager=False):
    r = " data-reveal" if reveal else ""
    p = " data-parallax" if parallax else ""
    t = '<span class="tag">Studio artwork</span>' if tag else ""
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<div class="imgr {cls}"{r}{p}>{t}<img src="assets/img/{name}.webp" '
            f'srcset="assets/img/{name}-sm.webp 800w, assets/img/{name}.webp 1600w" sizes="{sizes}" '
            f'width="1600" height="1200" alt="{html.escape(alt)}" {load}></div>')


def crumbs(items):
    out = ['<a class="label" href="index.html">Home</a>']
    for h, l in items[:-1]:
        out.append(f'<a class="label" href="{h}">{l}</a>')
    out.append(f'<span class="label muted" aria-current="page">{items[-1][1]}</span>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<span class="label muted">/</span>'.join(out) + '</nav>'


def crumb_ld(items):
    lst = [{"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"}]
    for i, (h, l) in enumerate(items, 2):
        lst.append({"@type": "ListItem", "position": i, "name": re.sub("<[^>]+>", "", l), "item": f"{BASE}/{h.replace('.html', '')}"})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": lst}


SOCIAL = [
    ("LinkedIn", "https://www.linkedin.com/company/grandyra/"),
    ("Instagram", "https://www.instagram.com/grandyra"),
    ("Facebook", "https://www.facebook.com/share/1PpPFbYfxY/"),
    ("X", "https://x.com/grandyra"),
    ("Threads", "https://www.threads.com/@grandyra"),
]


def social_links():
    return "".join(f'<li><a href="{u}" target="_blank" rel="noopener me">{n}</a></li>' for n, u in SOCIAL)


def logo(kind="mark", cls="gy-logo"):
    """Inline the official Grandyra logo (src/brand/*.svg), coloured by currentColor."""
    svg = open(os.path.join(ROOT, "src/brand", f"grandyra-{kind}.svg"), encoding="utf-8").read()
    return svg.replace("<svg", f'<svg class="{cls}" role="img" aria-label="Grandyra"', 1)


ORG = dict(old.ORG)
ORG["sameAs"] = [u for _, u in SOCIAL]
ORG["@id"] = BASE + "/#org"
ORG["url"] = BASE + "/"
ORG["email"] = EMAIL
ORG["logo"] = BASE + "/assets/favicon.svg"
ORG["address"] = {"@type": "PostalAddress", "streetAddress": "House 7, Road 4, Gulshan-1", "addressLocality": "Dhaka", "addressCountry": "BD"}


def mail_row():
    return (f'<span class="mailrow"><a class="mail" href="mailto:{EMAIL}">{EMAIL}</a>'
            f'<button type="button" class="copy" data-copy="{EMAIL}" aria-label="Copy email address">Copy</button></span>')


def chrome_top(current=""):
    links = [("index.html", "Home", "work-04"), ("work.html", "Work", "work-02"), ("services.html", "Services", "svc-brand-launch"),
             ("journal.html", "Journal", "svc-pr-agency"), ("about.html", "About", "studio-01"), ("contact.html", "Contact", "svc-rebranding")]
    nav = "".join(f'<a href="{h}" data-img="assets/img/{im}-sm.webp"><span class="n label">0{i}</span><span class="d">{t}</span></a>'
                  for i, (h, t, im) in enumerate(links, 1))
    groups = {"work.html": lambda c: c.startswith("work"), "services.html": lambda c: c == "services.html" or c[:-5] in SVC,
              "journal.html": lambda c: c.startswith("journal"), "about.html": lambda c: c == "about.html"}
    inline_nav = "".join(f'<a href="{h}"{" aria-current=\"page\"" if groups[h](current) else ""}>{n}</a>'
                         for h, n in (("work.html", "Work"), ("services.html", "Services"), ("journal.html", "Journal"), ("about.html", "About")))
    return f'''<a class="skip" href="#main">Skip to content</a>
<div class="loader" aria-hidden="true">
  <div class="row"><span class="label">Grandyra — Dhaka</span><span class="label">Greatness over noise</span></div>
  {logo("mark", "gy-logo loader-logo")}
  <span class="word d">noise</span>
  <div class="row"><span class="label">Loading the signal</span><span class="count d">000</span></div>
  <i class="bar"></i>
</div>
<div class="curtain" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div>
<header class="hdr">
  <a class="wm" href="index.html" aria-label="Grandyra home">{logo("mark", "gy-logo wm-mark")}<span class="wm-txt">Grandyra</span></a>
  <span class="clock label clk">Dhaka <span data-clock>--:--</span> GMT+6</span>
  <nav class="hdr-nav label" aria-label="Primary">{inline_nav}</nav>
  <div class="right"><a class="cta-link label" href="contact.html">Start a project</a>
  <button class="menu-btn label" aria-expanded="false" aria-controls="menu"><span class="lbl">Menu</span><span class="dots" aria-hidden="true"></span></button></div>
</header>
<div class="menu" id="menu" aria-hidden="true">
  <nav aria-label="Main">{nav}</nav>
  <aside>
    <div class="pic"><img src="assets/img/work-04-sm.webp" alt="" width="800" height="600"></div>
    <div><p class="label muted">Say hello</p><ul><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li class="muted">{ADDRESS}</li></ul>
    <p class="label muted" style="margin-top:2rem">Elsewhere</p><ul>{social_links()}</ul></div>
  </aside>
</div>'''


def chrome_bottom():
    svc = "".join(f'<li><a href="{s["slug"]}.html">{s["name"]}</a></li>' for s in SERVICES[:6])
    return f'''<footer class="t-ink">
<section class="foot-cta wrap" aria-labelledby="fc">
  <p class="label muted fade">Got something in mind?</p>
  <div class="big">
    <h2 id="fc" class="d d-xxl" data-split>Let’s make<br><span class="it">something</span> great</h2>
    <a class="orb" href="contact.html" data-magnetic data-cursor="Hello">Start a<br>project</a>
  </div>
  <div class="foot-grid">
    <div>
      {mail_row()}
      <address class="muted" style="margin-top:1.5rem;font-style:normal">Grandyra Limited<br>{ADDRESS}<br><span class="clk">It’s <span data-clock>--:--</span> in Dhaka right now.</span></address>
    </div>
    <div><h3 class="label">Services</h3><ul>{svc}<li><a href="services.html">All services</a></li></ul></div>
    <div><h3 class="label">Studio</h3><ul><li><a href="work.html">Work</a></li><li><a href="journal.html">Journal</a></li><li><a href="about.html">About</a></li><li><a href="contact.html">Contact</a></li></ul></div>
    <div><h3 class="label">Follow</h3><ul>{social_links()}</ul></div>
  </div>
  <a class="foot-logo" href="index.html" aria-label="Grandyra home">{logo("logo", "gy-logo foot-logo-svg")}</a>
  <div class="legal"><span>© <span data-year>2026</span> Grandyra Limited</span><span>Building brands worthy of tomorrow.</span></div>
</section>
</footer>'''


def page(path, title, desc, body, lang="en", schema=None, og="website", robots=None, extra_head="", og_image="og-default.jpg", og_alt="Grandyra, a branding and communications house in Dhaka"):
    if robots is None:
        robots = "noindex, nofollow" if PREVIEW else "index, follow, max-image-preview:large"
    canonical = BASE + "/" + ("" if path == "index.html" else path.replace(".html", ""))
    ld = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in (schema or []))
    doc = f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#0D0D0B">
<meta property="og:type" content="{og}"><meta property="og:site_name" content="Grandyra">
<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canonical}"><meta property="og:image" content="{BASE}/assets/img/{og_image}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{html.escape(og_alt)}">
<meta property="og:locale" content="en_BD"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{html.escape(title)}"><meta name="twitter:description" content="{html.escape(desc)}"><meta name="twitter:image" content="{BASE}/assets/img/{og_image}">
<link rel="preload" href="assets/fonts/archivo-wdth.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/bodoni-italic.woff2" as="font" type="font/woff2" crossorigin>
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="assets/apple-touch-icon.png"><link rel="manifest" href="assets/site.webmanifest">
<script src="assets/boot.js"></script>
<link rel="stylesheet" href="assets/site.css">{extra_head}
{ld}
</head>
<body>
{chrome_top(path)}
<main id="main">
{body}
</main>
{chrome_bottom()}
<script src="assets/vendor/gsap.min.js" defer></script>
<script src="assets/vendor/ScrollTrigger.min.js" defer></script>
<script src="assets/vendor/lenis.min.js" defer></script>
<script src="assets/main.js" defer></script>
</body>
</html>'''
    with open(os.path.join(OUT, path), "w", encoding="utf-8") as f:
        f.write(doc)
    PAGES.append(path)


def needs_rows(theme_dark=False):
    out = []
    for i, s in enumerate(SERVICES, 1):
        q, c = NEED[s["slug"]]
        out.append(f'''<a class="need" href="{s["slug"]}.html" style="--c:{c}" data-img="assets/img/svc-{s["slug"]}-sm.webp" data-cursor="Explore">
<span class="n">{icon(ICON[s["slug"]])}</span><span class="q d">{q}</span><span class="s">{s["name"]} <span class="arr" aria-hidden="true">→</span></span></a>''')
    return "".join(out) + '<div class="float-img" aria-hidden="true"><img src="assets/img/svc-brand-identity-design-sm.webp" alt="" width="800" height="600"></div>'


def covers(items):
    out = []
    for i in items:
        bn = ""
        inner = f'''<div class="page {i["theme"]}"><img src="assets/img/{i["img"]}-sm.webp" alt="" loading="lazy" width="800" height="600">
<div class="mast"><span class="label">The Grandyra Journal</span><span class="label">No. {i["no"]}</span></div>
<span class="no it">{i["no"]}</span><span class="ttl d"{bn}>{i["title"]}</span></div>
<div class="cap"><span class="label"{bn}>{i["topic"]}</span><span class="label muted">{"Read →" if i["slug"] else "Soon"}</span></div>'''
        if i["slug"]:
            out.append(f'<a class="cover fade" href="{i["slug"]}" data-cursor="Read">{inner}</a>')
        else:
            out.append(f'<div class="cover soon fade" aria-label="Coming soon: {html.escape(i["title"])}">{inner}</div>')
    return '<div class="covers">' + "".join(out) + "</div>"


SVC_WORK = {"event-management": ["work-real-estate-futsal-2026", "work-seheri-nights", "work-the-audio-expo", "work-first-momentum"],
            "brand-identity-design": ["work-souk-taban", "work-seheri-nights"],
            "advertising-agency": ["work-real-estate-futsal-2026"]}


def next_card(i):
    n = WORK[(i + 1) % len(WORK)]
    return (f'<section class="nextp t-ink"><a class="wrap" href="{n["href"]}" data-cursor="Next"><span class="label muted">Next project</span>'
            f'<span class="d d-xl">{n["title"]}</span><span class="nxt-tl">{n["tagline"]}</span></a></section>')


def build():
    if os.path.exists(OUT):
        for f in os.listdir(OUT):
            if f.endswith(".html") or f in ("sitemap.xml", "robots.txt"):
                os.remove(os.path.join(OUT, f))
    shutil.copy(os.path.join(ROOT, "src/site.css"), os.path.join(OUT, "assets/site.css"))
    shutil.copy(os.path.join(ROOT, "src/main.js"), os.path.join(OUT, "assets/main.js"))
    shutil.copy(os.path.join(ROOT, "src/boot.js"), os.path.join(OUT, "assets/boot.js"))
    import subprocess
    for f in ("assets/site.css", "assets/main.js", "assets/boot.js"):
        p = os.path.join(OUT, f)
        try:
            subprocess.run(["npx", "esbuild", p, "--minify", "--allow-overwrite", "--outfile=" + p, "--log-level=error"], cwd=ROOT, check=True)
        except (FileNotFoundError, subprocess.CalledProcessError):
            print(f"warning: esbuild not available, {f} was copied without minifying (run `npm install` first)")
    deploy = os.path.join(ROOT, "src", "deploy")  # host config (_headers, .htaccess) and icons
    if os.path.isdir(deploy):
        for name in os.listdir(deploy):
            dest = os.path.join(OUT, name) if name in ("_headers", ".htaccess") else os.path.join(OUT, "assets", name)
            shutil.copy(os.path.join(deploy, name), dest)

    # ============================ HOME ============================
    def work_visual(w, sizes):
        if w.get("real"):
            n = w["img"]
            return (f'<div class="imgr"><img src="assets/img/{n}.webp" srcset="assets/img/{n}-sm.webp 800w, assets/img/{n}.webp 1400w" sizes="{sizes}" '
                    f'width="1400" height="1867" alt="{html.escape(w["title"])}: venue, trophy and branding assembled into one hexagon collage" loading="lazy" decoding="async"></div>')
        if w.get("photo"):
            n, wd, ht, alt = w["photo"]
            return (f'<div class="imgr photo"><img src="assets/img/{n}.webp" srcset="assets/img/{n}-sm.webp {min(700, wd)}w, assets/img/{n}.webp {wd}w" sizes="{sizes}" '
                    f'width="{wd}" height="{ht}" alt="{html.escape(alt)}" loading="lazy" decoding="async"></div>')
        return (f'<div class="imgr typo {w["theme"]}"><span class="label typo-top">{w["disc"].split(",")[0]}</span>'
                f'<b class="d typo-stat">{w["stat"]}</b><span class="typo-lbl">{w["statlabel"]}</span></div>')

    def work_meta(w):
        yr = f'<span class="label muted">{w["year"]}</span>' if w["year"] else ""
        fact = f'<p class="label gold factline">{w["stats"][0][0]} {w["stats"][0][1]}</p>' if w.get("stats") and w.get("photo") else ""
        return (f'<div class="meta"><div><h3 class="d d-s">{w["title"]}</h3><p class="muted tl">{w["tagline"]}</p>{fact}</div>{yr}</div>')

    def work_card(w, sizes="56vw"):
        inner = work_visual(w, sizes) + work_meta(w)
        if w["href"]:
            return f'<a class="card" href="{w["href"]}" data-cursor="View" aria-label="{html.escape(w["title"])}: view case study">{inner}</a>'
        return f'<div class="card">{inner}</div>'

    cards = "".join(work_card(w) for w in WORK)

    marquee_items = "".join(f'<span class="item d">{a} <span class="it">over</span> {b} {STAR}</span>' for a, b in
                            [("Greatness", "noise"), ("Clarity", "complexity"), ("Timeless", "temporary")]) + \
        f'<span class="item d">Strategy <span class="it">before</span> decoration {STAR}</span>'

    home = f'''
<section class="hero t-ink" aria-label="Introduction">
  <canvas id="noise" aria-hidden="true"></canvas>
  <div class="top"><span class="label">Branding &amp; communications house</span><span class="label">Dhaka, Bangladesh</span></div>
  <h1 class="d">We turn noise<br>into <span class="it">greatness.</span></h1>
  <div class="foot"><span class="label state"><b></b><span>Noise</span></span><span class="meter" aria-hidden="true"><i></i></span><span class="label">Scroll to find the signal ↓</span></div>
</section>

<section class="manifesto t-bone wrap" aria-labelledby="mf">
  <h2 id="mf" class="sr-only">About Grandyra</h2>
  <div class="grid">
    <div><div class="badge" aria-hidden="true"><svg viewBox="0 0 200 200"><defs><path id="c" d="M100,100 m-78,0 a78,78 0 1,1 156,0 a78,78 0 1,1 -156,0"/></defs><text font-size="15.5" font-weight="600" letter-spacing="4.2" fill="currentColor" font-family="Archivo"><textPath href="#c">GREATNESS OVER NOISE • CLARITY OVER COMPLEXITY •</textPath></text></svg><span class="core"></span></div></div>
    <div>
      <p class="txt" data-scrub>Grandyra is a branding and communications house in Dhaka. We start by asking why: why this business, why now, why would anyone choose it. Then we build the <a href="brand-identity-design.html">brand</a>, the <a href="advertising-agency.html">campaign</a> and the <a href="event-management.html">experience</a> that answer it. Strategy first. Then the <span class="it">beautiful</span> part.</p>
      <div class="cta-row fade"><a class="pill solid" href="work.html" data-magnetic>See our work</a><a class="pill" href="contact.html">Start a project</a></div>
    </div>
  </div>
</section>

<section class="band t-bone" aria-label="Dhaka, in colour">
  <div class="band-grid wrap">
    {photo("festival", "svc-event-management", cls="tall", parallax=True)}
    <div class="band-txt"><p class="label muted">Where we work</p>
    <p class="big-text fade" style="margin-top:1rem">Dhaka is loud, colourful and never still. In a city like this, the brands people remember are the clear ones.</p>
    {photo("rickshaw", "studio-01", cls="small")}</div>
  </div>
</section>
<section class="hwork t-ink" aria-labelledby="sw">
  <div class="track">
    <div class="intro">
      <div><p class="label muted">Recent work</p><h2 id="sw" class="d d-xl" style="margin-top:1rem">The work<br><span class="it gold">talks</span></h2></div>
      <div><span class="count d" aria-hidden="true"><span data-count>01</span><span class="of"> /0{len(WORK)}</span></span>
      <p class="muted" style="max-width:30ch">Tournaments, night markets and expos. Each one started with a business problem.</p>
      <a class="pill" href="work.html" style="margin-top:1rem">All projects</a></div>
    </div>
    {cards}
  </div>
</section>

<section class="needs t-bone" aria-labelledby="nd">
  <div class="head wrap"><h2 id="nd" class="d d-l" data-split>What do<br>you <span class="it">need?</span></h2>
  <p class="lede fade">Most people don’t arrive asking for a “brand identity system”. They arrive with a problem. Start there.</p></div>
  {needs_rows()}
</section>

<section class="why t-ink wrap" aria-labelledby="wy">
  <div class="why-head"><p class="label muted">How we think</p><h2 id="wy" class="d d-l" data-split style="margin-top:1rem">Four rules<br>we work <span class="it gold">by</span></h2></div>
  <div class="why-grid">
    <article class="fade"><span class="why-ic">{icon("lightbulb")}</span><h3 class="d d-s">Strategy before aesthetics</h3><p class="muted">We work out the business problem before we shape anything visual. Design should be an answer, not a guess.</p></article>
    <article class="fade"><span class="why-ic">{icon("volume-x")}</span><h3 class="d d-s">Substance over noise</h3><p class="muted">In a cluttered market we practise restraint. Every element has to earn its place.</p></article>
    <article class="fade"><span class="why-ic">{icon("hourglass")}</span><h3 class="d d-s">Longevity over trends</h3><p class="muted">Trends expire. We build visual systems meant to hold their value for years, not seasons.</p></article>
    <article class="fade"><span class="why-ic">{icon("pen-tool")}</span><h3 class="d d-s">Craft over convenience</h3><p class="muted">From type scales to venue signage, the details get the time they need.</p></article>
  </div>
</section>
<section class="marquee t-verm" aria-label="Our principles">
  <div class="row">{marquee_items}{marquee_items}</div>
  <div class="row alt" aria-hidden="true">{marquee_items}{marquee_items}</div>
</section>

<section class="process t-bone wrap" aria-labelledby="pr">
  <div class="grid">
    <div class="sticky"><p class="label muted">How we work</p><h2 id="pr" class="d d-l" data-split style="margin-top:1rem">No shortcuts<br>through the<br><span class="it">first step.</span></h2>
    <p class="lede fade" style="margin-top:2rem">Five stages, one team, from the first conversation to long after launch.</p></div>
    <div>
      <article class="pcard t-ink"><div class="hd"><span class="num d">01</span><h3 class="d d-m">Discover</h3></div><span class="big d it" data-n="01" aria-hidden="true"></span><p class="muted">We listen, research and question until the real problem is clear.</p></article>
      <article class="pcard t-deep"><div class="hd"><span class="num d">02</span><h3 class="d d-m">Define</h3></div><span class="big d it" data-n="02" aria-hidden="true"></span><p class="muted">We set the strategy and the direction before any design begins.</p></article>
      <article class="pcard t-verm"><div class="hd"><span class="num d">03</span><h3 class="d d-m">Create</h3></div><span class="big d it" data-n="03" aria-hidden="true"></span><p>Ideas are invented first, then crafted across every touchpoint.</p></article>
      <article class="pcard t-gold"><div class="hd"><span class="num d">04</span><h3 class="d d-m">Refine</h3></div><span class="big d it" data-n="04" aria-hidden="true"></span><p>We iterate and polish until every detail earns its place.</p></article>
      <article class="pcard t-teal"><div class="hd"><span class="num d">05</span><h3 class="d d-m">Endure</h3></div><span class="big d it" data-n="05" aria-hidden="true"></span><p>We build systems that keep the brand relevant long after launch.</p></article>
    </div>
  </div>
</section>

<section class="journal t-ink" aria-labelledby="jn">
  <div class="wrap">
    <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:2rem;flex-wrap:wrap;margin-bottom:3rem">
      <h2 id="jn" class="d d-l" data-split>The Grandyra<br><span class="it gold">Journal</span></h2>
      <p class="lede muted fade">Short reads on brands and the craft of making them.</p>
    </div>
    {covers(ISSUES)}
  </div>
</section>

<section class="voices t-bone wrap" aria-labelledby="vc">
  <p id="vc" class="label muted">From our founder</p>
  <blockquote class="fade" style="margin-top:2rem">I don’t want Grandyra to create brands that are simply noticed. I want us to create brands that are remembered.</blockquote>
  <p class="label" style="margin-top:2rem">Arman Hossain, Founder &amp; Managing Director</p>
</section>

<section class="studio t-bone wrap" aria-labelledby="st" style="padding-top:0">
  <div class="grid">
    <div class="dhaka">{photo("dhaka", "studio-01", reveal=False, parallax=True)}<span class="coords label">Dhaka, Bangladesh</span></div>
    <div>
      <p class="label muted">The studio</p>
      <h2 id="st" class="d d-l" data-split style="margin-top:1rem">Made in<br><span class="it">Dhaka.</span></h2>
      <p class="lede fade" style="margin-top:1.5rem">We work with businesses, institutions and founders who have something worth building. Our studio is a small team of strategists, designers and makers who care a slightly unreasonable amount about getting it right.</p>
      <div class="facts fade"><div><b>Gulshan-1</b><span class="label muted">House 7, Road 4, Dhaka</span></div><div class="clk"><b><span data-clock>--:--</span></b><span class="label muted">Dhaka time</span></div><div><b><a href="mailto:{EMAIL}" class="ulink">Email us</a></b><span class="label muted">{EMAIL}</span></div></div>
      <a class="pill solid" href="about.html" style="margin-top:2rem" data-magnetic>About Grandyra</a>
    </div>
  </div>
</section>
'''
    page("index.html", "Grandyra — Branding Agency in Dhaka, Bangladesh",
         "Grandyra is a branding and communications house in Dhaka. Brand identity, packaging, advertising, PR and events. We turn noise into greatness.",
         home, schema=[ORG, {"@context": "https://schema.org", "@type": "WebSite", "name": "Grandyra", "url": BASE + "/"}])

    # ============================ WORK ============================
    def wc_card(w):
        inner = work_visual(w, "(max-width:800px) 100vw, 55vw") + (
            f'<div class="meta"><div><span class="label gold">{w["no"]}</span><h2 class="d d-s" style="margin:.4rem 0 0">{w["title"]}</h2>'
            f'<p class="muted" style="margin:.4rem 0 0;max-width:46ch">{w["tagline"]}</p></div>'
            f'<span class="label muted">{w["year"]}</span></div>'
            f'<p class="label muted scope">{w["disc"]}</p>')
        if w["href"]:
            return f'<a class="wc fade" href="{w["href"]}" data-cat="{w["cat"]}" data-cursor="View">{inner}</a>'
        return f'<div class="wc fade" data-cat="{w["cat"]}">{inner}</div>'

    wc = "".join(wc_card(w) for w in WORK)
    work = f'''
<section class="phero t-ink wrap">
  {crumbs([("work.html", "Work")])}
  <h1 class="d d-xxl" data-split>Recent <span class="it gold">work</span></h1>
  <div class="row"><p class="lede fade">A few of the projects we’ve made so far. The Real Estate Futsal 2026 case study is open to read. More will follow.</p><span></span></div>
</section>
<section class="t-ink wrap" style="padding-bottom:8rem"><div class="wgrid">{wc}</div></section>
<section class="t-verm wrap cta-band"><p class="d d-m">Have a project<br>in mind?</p><a class="pill solid" href="contact.html" data-magnetic>Start a conversation</a></section>
'''
    page("work.html", "Our Work — Branding & Event Projects | Grandyra",
         "Recent projects by Grandyra, a branding and communications house in Dhaka: Real Estate Futsal 2026, Souk Taban, Seheri Nights and The Audio Expo.",
         work, schema=[crumb_ld([("work.html", "Work")])])

    # ============================ CASE STUDY ============================
    def board(name, alt):
        return (f'<div class="imgr board" data-reveal><img src="assets/img/{name}.webp" srcset="assets/img/{name}-sm.webp 800w, assets/img/{name}.webp 1100w" '
                f'sizes="(max-width: 900px) 100vw, 46vw" width="1100" height="1467" alt="{html.escape(alt)}" loading="lazy" decoding="async"></div>')

    def cs_block(label, title, text, name, alt, theme="t-bone"):
        return (f'<section class="sec {theme} wrap"><div class="split2"><div class="side"><p class="label muted">{label}</p>'
                f'<h2 class="d d-m" style="margin-top:1rem">{title}</h2><p class="cs-text fade">{text}</p></div><div>{board(name, alt)}</div></div></section>')

    cs = f'''
<section class="phero t-ink wrap">
  {crumbs([("work.html", "Work"), ("work-real-estate-futsal-2026.html", "Real Estate Futsal 2026")])}
  <p class="label gold fade">Case study</p>
  <h1 class="d d-xxl" data-split style="margin-top:1rem">Real Estate<br><span class="it">Futsal</span> 2026</h1>
  <div class="row"><p class="lede fade">Grandyra was the official creative partner for the tournament, shaping how it looked, from the trophy to the court.</p><span></span></div>
  <dl class="facts-bar fade"><div><dt class="label">Role</dt><dd>Official creative partner</dd></div><div><dt class="label">Venue</dt><dd>ISD, Dhaka</dd></div><div><dt class="label">When</dt><dd>October 2026</dd></div><div><dt class="label">Scope</dt><dd>Identity, trophies, venue, campaign</dd></div></dl>
</section>
<section class="t-ink" style="padding-bottom:5rem"><div class="cover-band cs-hero">{img("futsal-hero", "Real Estate Futsal 2026 venue, trophy and branding in a hexagon collage", parallax=True, eager=True, tag=False, sizes="(max-width: 900px) 100vw, 50vw")}</div></section>
{cs_block("The identity", "A tournament with its own mark", "The official emblem captures the drive of the industry and the heart of futsal. Its line, “Built from the skyline, forged for the game.”, gave sixteen teams a tournament with an identity of its own.", "futsal-identity", "Real Estate Futsal 2026 identity board with the trophy emblem and tagline")}
{cs_block("Kits, passes and awards", "One system, down to the lanyard", "Accreditation, player kits and awards all carried the same identity, so the tournament looked like one thing from the lanyard to the crystal award.", "futsal-kits", "Accreditation lanyard, player jerseys and a crystal award for Real Estate Futsal 2026")}
{cs_block("Custom trophies and hardware", "Made for the final moment", "The champions’ trophy was designed with the event branding around it, so the winning photograph carries the identity.", "futsal-trophy", "Champions trophy and branded backdrops for Real Estate Futsal 2026")}
{cs_block("Venue branding", "Branding the court", "Court-side banners and wall graphics at ISD carried the identity into the space, for the players and the crowd.", "futsal-venue", "Branded banners and wall graphics at the ISD venue")}
{cs_block("Digital and social campaign", "Built for the feed and the big screen", "Social creatives and live-screening graphics shared the same look as everything on the court.", "futsal-social", "Social campaign creatives and live screening graphics")}
{cs_block("On the turf", "Unforgettable moments", "The branding at work with teams, organisers and the crowd, and the Grandyra team on the day.", "futsal-moments", "Photographs from the tournament court and crowd")}
{next_card(0)}
<section class="sec t-ink wrap"><div class="split2"><div class="side"><p class="label muted">Next</p><h2 class="d d-m" style="margin-top:1rem">Planning an event?</h2></div>
<div><p class="big-text fade">We design the brand, the space and the story as one piece, so the event feels like itself.</p>
<div style="display:flex;gap:.6rem;flex-wrap:wrap;margin-top:2rem"><a class="pill" href="event-management.html">Event production</a><a class="pill solid" href="contact.html">Start a conversation</a></div></div></div></section>
'''
    page("work-real-estate-futsal-2026.html", "Real Estate Futsal 2026 — Case Study | Grandyra",
         "How Grandyra worked as official creative partner for Real Estate Futsal 2026 at ISD, Dhaka: identity, kits, trophy, venue branding and campaign.",
         cs, og="article", og_image="og-work-real-estate-futsal-2026.jpg", og_alt="Real Estate Futsal 2026 branding assembled in a hexagon collage",
         schema=[crumb_ld([("work.html", "Work"), ("work-real-estate-futsal-2026.html", "Real Estate Futsal 2026")]),
                                   {"@context": "https://schema.org", "@type": "CreativeWork", "name": "Real Estate Futsal 2026", "creator": {"@id": BASE + "/#org"}}])

    # ============================ PROJECT CASE STUDIES ============================
    def pimg(n, wd, ht, alt, sizes, eager=False, cls="", parallax=False):
        sm = min(700, wd)
        load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
        par = " data-parallax" if parallax else ""
        return (f'<div class="imgr {cls}" data-reveal{par}><img src="assets/img/{n}.webp" srcset="assets/img/{n}-sm.webp {sm}w, assets/img/{n}.webp {wd}w" '
                f'sizes="{sizes}" width="{wd}" height="{ht}" alt="{html.escape(alt)}" {load}></div>')

    for i, w in enumerate(WORK):
        if w.get("real"):
            continue
        facts = "".join(f'<div><dt class="label">{k}</dt><dd>{v}</dd></div>' for k, v in w["facts"])
        body = "".join(f'<p class="big-text fade"{" style=margin-top:2rem" if n else ""}>{p}</p>' for n, p in enumerate(w["body"]))
        body = body.replace("style=margin-top:2rem", 'style="margin-top:2rem"')
        if w.get("poster"):
            n = w["img"]
            hero = (f'<section class="t-ink" style="padding-bottom:5rem"><div class="cover-band cs-poster"><div class="imgr board poster" data-reveal><img src="assets/img/{n}.webp" '
                    f'srcset="assets/img/{n}-sm.webp 540w, assets/img/{n}.webp 900w" sizes="(max-width: 700px) 90vw, 420px" width="900" height="2250" '
                    f'alt="Teaser artwork for First Momentum 2027, the Electromechanical Expo Dhaka: Coming soon, where great things begin" fetchpriority="high"></div></div></section>')
        else:
            pn, pw, ph, palt = w["photo"]
            mx = f' style="max-width:{w["hero_max"]}px;margin-inline:auto"' if w.get("hero_max") else ""
            hero = (f'<section class="t-ink" style="padding-bottom:0"><div class="cover-band pcover"{mx}>'
                    f'{pimg(pn, pw, ph, palt, "(max-width: 900px) 100vw, 90vw", eager=True, cls="pwide")}</div></section>')
        stats = ""
        if w.get("stats"):
            cells = "".join(f'<div><b class="d">{a}</b><span>{b}</span></div>' for a, b in w["stats"])
            note = f'<p class="statnote">{w["note"]}</p>' if w.get("note") else ""
            stats = f'<section class="statband {w["theme"]}"><div class="wrap"><div class="stats">{cells}</div>{note}</div></section>'
        did = ""
        if w["did"]:
            did = (f'<section class="sec t-ink wrap"><div class="split2"><div class="side"><p class="label muted">What we did</p><h2 class="d d-m" style="margin-top:1rem">Our <span class="it gold">part</span></h2></div>'
                   f'<div><ul class="deliv" style="color:var(--bone)">{"".join(f"<li>{x}</li>" for x in w["did"])}</ul></div></div></section>')
        gal = ""
        if w.get("gallery"):
            items = "".join(
                f'<figure class="pfig">{pimg(n, wd, ht, alt, "(max-width: 900px) 100vw, 45vw", cls="ptall")}' + (f"<figcaption class=\"label muted\">{cap}</figcaption>" if cap else "") + "</figure>"
                for n, wd, ht, alt, cap in w["gallery"])
            gal = f'<section class="t-bone pgal"><div class="wrap">{items}</div></section>'
        result = ""
        if w["result"]:
            result = (f'<section class="sec t-bone wrap" style="padding-top:0"><div class="split2"><div class="side"><p class="label muted">The result</p></div>'
                      f'<div><p class="big-text fade">{w["result"]}</p></div></div></section>')
        year = f' ({w["year"]})' if w["year"] and w["year"] != "Upcoming" else ""
        cs2 = f'''
<section class="phero t-ink wrap">
  {crumbs([("work.html", "Work"), (w["href"], w["title"])])}
  <p class="label gold fade">Case study</p>
  <h1 class="d d-xxl" data-split style="margin-top:1rem">{w["title"]}</h1>
  <div class="row"><p class="lede fade">{w["lede"]}</p><span></span></div>
  <dl class="facts-bar fade">{facts}</dl>
</section>
{hero}
{stats}
<section class="sec t-bone wrap"><div class="split2"><div class="side"><p class="label muted">The project</p></div><div>{body}</div></div></section>
{gal}
{did}
{result}
{next_card(i)}
<section class="t-verm wrap cta-band"><p class="d d-m">Planning something<br>similar?</p><a class="pill solid" href="contact.html" data-magnetic>Start a conversation</a></section>
'''
        page(w["href"], f'{w["title"]}{year} — Case Study | Grandyra',
             f'{w["lede"]} {w["tagline"]}.'[:158],
             cs2, og="article", og_image=f'og-{w["href"][:-5]}.jpg', og_alt=f'{w["title"]}: Grandyra case study',
             schema=[crumb_ld([("work.html", "Work"), (w["href"], w["title"])]),
                     {"@context": "https://schema.org", "@type": "CreativeWork", "name": w["title"], "description": w["lede"], "creator": {"@id": BASE + "/#org"}}])

    # ============================ SERVICES HUB ============================
    hub = f'''
<section class="phero t-bone wrap">
  {crumbs([("services.html", "Services")])}
  <h1 class="d d-xxl" data-split>What do you <span class="it">need?</span></h1>
  <div class="row"><p class="lede fade">{NWORD} disciplines, one way of thinking. Pick the problem — we’ll connect the rest.</p><span></span></div>
</section>
<section class="needs t-bone" style="padding-top:0">{needs_rows()}</section>
'''
    page("services.html", "Services — Branding, Advertising & Events | Grandyra",
         "Brand identity, rebranding, packaging, advertising, brand marketing, PR, events, corporate training and retainers — Grandyra's services in Dhaka, Bangladesh.",
         hub, schema=[crumb_ld([("services.html", "Services")])])

    # ============================ SERVICE PAGES ============================
    for s in SERVICES:
        q, c = NEED[s["slug"]]
        th = THEME[s["slug"]]
        title_words = s["h1"]  # e.g. Brand <em>creation</em>
        h1 = re.sub(r"<em>(.*?)</em>", r'<span class="it">\1</span>', title_words)
        steps = "".join(f'<li class="fade"><span class="k d">0{i}</span><h3 class="d">{t}</h3><p>{dsc}</p></li>' for i, (t, dsc) in enumerate(s["steps"], 1))
        deliv = "".join(f"<li>{x}</li>" for x in s["deliver"])
        faqs = "".join(f'<details><summary>{qq}<span class="pm" aria-hidden="true">+</span></summary><div class="a"><p>{a}</p></div></details>' for qq, a in s["faq"])
        rel = "".join(f'<a href="{r}.html" data-cursor="Go"><span class="d d-m">{NEED[r][0]}</span><span class="label">{SVC[r]["name"]} →</span></a>' for r in s["related"] if r in SVC)
        extra = ""
        if s.get("journal"):
            extra = '<a class="pill" href="journal-when-to-rebrand.html" style="margin-top:2rem">Read: When should a company rebrand? ↗</a>'
        proj = [w for w in WORK if w["href"][:-5] in SVC_WORK.get(s["slug"], [])]
        if proj:
            extra += '<p class="label muted" style="margin-top:2.5rem">Related work</p><div style="display:flex;gap:.6rem;flex-wrap:wrap;margin-top:.8rem">' + "".join(
                f'<a class="pill" href="{w["href"]}">{w["title"]}</a>' for w in proj) + "</div>"
        body = f'''
<section class="phero {th} wrap">
  {crumbs([("services.html", "Services"), (s["slug"] + ".html", s["name"])])}
  <p class="label ask fade">{q} — {s["kw"]}</p>
  <h1 class="d d-xxl" data-split style="margin-top:1rem">{h1}</h1>
  <div class="row"><p class="lede fade">{s["lede"]}</p><a class="orb" href="contact.html" data-magnetic data-cursor="Hello" style="justify-self:end">Talk to<br>us ↗</a></div>
</section>
<section class="{th}" style="padding-bottom:5rem"><div class="cover-band">{photo(SVC_PHOTO[s["slug"]], "svc-" + s["slug"], parallax=True, eager=True) if s["slug"] in SVC_PHOTO else img("svc-" + s["slug"], s["name"] + " — studio artwork", parallax=True, eager=True)}</div></section>
<section class="sec t-bone wrap"><div class="split2"><div class="side"><p class="label muted">01 — The problem</p></div>
<div>{"".join(f'<p class="big-text fade">{p}</p>' for p in s["problem"])}</div></div></section>
<section class="sec t-bone wrap" style="padding-top:0"><h2 class="label muted" style="margin:0 0 2rem;font-weight:400">02 — How we approach it</h2><ol class="steps4" style="padding:0;margin:0">{steps}</ol></section>
<section class="sec t-ink wrap"><div class="split2"><div class="side"><p class="label muted">03 — What you receive</p><h2 class="d d-m" style="margin-top:1rem">Scoped to you,<br><span class="it gold">not a menu.</span></h2></div>
<div><ul class="deliv" style="color:var(--bone)">{deliv}</ul>{extra}</div></div></section>
<section class="sec t-bone wrap"><div class="split2"><div class="side"><p class="label muted">04 — Questions</p><h2 class="d d-m" style="margin-top:1rem">Asked <span class="it">often</span></h2></div>
<div class="faq">{faqs}</div></div></section>
<section class="sec t-bone wrap" style="padding-top:0"><p class="label muted" style="margin-bottom:1.5rem">05 — You might also need</p><div class="rel">{rel}</div></section>
'''
        faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": qq, "acceptedAnswer": {"@type": "Answer", "text": html.unescape(re.sub("<[^>]+>", "", a))}}
            for qq, a in s["faq"] if "ph-text" not in a]}
        ld = [crumb_ld([("services.html", "Services"), (s["slug"] + ".html", s["name"])]),
              {"@context": "https://schema.org", "@type": "Service", "name": s["name"], "serviceType": s["kw"], "provider": {"@id": BASE + "/#org"},
               "areaServed": {"@type": "Country", "name": "Bangladesh"}, "description": s["desc"]}]
        if faq_ld["mainEntity"]:
            ld.append(faq_ld)
        page(s["slug"] + ".html", s["title"], s["desc"], body, schema=ld)

    # ============================ JOURNAL ============================
    jh = f'''
<section class="phero t-ink wrap">
  {crumbs([("journal.html", "Journal")])}
  <h1 class="d d-xxl" data-split>The <span class="it gold">Journal</span></h1>
  <div class="row"><p class="lede fade">A slow publication about brands, ideas and the craft of making them. Numbered issues.</p><span></span></div>
</section>
<section class="t-ink wrap" style="padding-bottom:8rem">{covers(ISSUES)}</section>
'''
    page("journal.html", "The Grandyra Journal — Ideas on Branding & Creativity",
         "The Grandyra Journal: numbered issues on branding, rebranding, logo design, packaging and advertising, from a creative house in Dhaka.",
         jh, schema=[crumb_ld([("journal.html", "Journal")])])

    def prose_from_old(fname):
        t = open(os.path.join(ROOT, "tools", "journal-src", fname), encoding="utf-8").read()
        m = re.search(r'<div class="span-8 start-5 prose">(.*?)<div class="mt-3">', t, re.S)
        p = m.group(1)
        return p.replace('class="link"', "")

    arts = [
        ("journal-strategy-before-decoration.html", "01", 'Strategy<br>before <span class="it">decoration</span>', "Strategy before decoration",
         "Strategy Before Decoration | Grandyra Journal",
         "Why every Grandyra project starts with a question, not a sketch — and what that means for the brands we build in Bangladesh.",
         "Brand creation", "t-ink", "svc-retainer-partnership", "en", ["brand-identity-design", "rebranding"]),
        ("journal-when-to-rebrand.html", "02", 'When should<br>a company <span class="it">rebrand?</span>', "When should a company rebrand?",
         "When Should a Company Rebrand? | Grandyra Journal",
         "How to tell whether your company needs a rebrand, a refresh, or neither — practical signs, common mistakes and how to decide, from a Dhaka branding agency.",
         "Brand refresh", "t-deep", "svc-rebranding", "en", ["rebranding", "brand-identity-design", "brand-launch"]),
    ]
    for path, no, h1, plain, st, desc, topic, th, im, lang, rel in arts:
        relh = "".join(f'<a href="{r}.html"><span class="d d-m">{NEED[r][0]}</span><span class="label">{SVC[r]["name"]} →</span></a>' for r in rel if r in SVC)
        h1cls = "d d-xl"
        h1style = ""
        body = f'''<div class="progress" aria-hidden="true"></div>
<article>
<section class="phero {th} wrap">
  {crumbs([("journal.html", "Journal"), (path, "No. " + no)])}
  <p class="label fade">The Grandyra Journal — No. {no} — {topic}</p>
  <h1 class="{h1cls}"{h1style} data-split>{h1}</h1>
</section>
<section class="{th}" style="padding-bottom:5rem"><div class="cover-band">{img(im, "Issue " + no + " cover art", parallax=True, eager=True)}</div></section>
<section class="sec t-bone wrap"><div class="split2"><div class="side"><span class="d it issue-no" data-n="{no}" aria-hidden="true" style="font-size:clamp(6rem,12vw,12rem);color:var(--verm)"></span></div>
<div class="prose">{prose_from_old(path)}</div></div></section>
<section class="sec t-bone wrap" style="padding-top:0"><p class="label muted" style="margin-bottom:1.5rem">Related</p><div class="rel">{relh}<a href="journal.html"><span class="d d-m">More issues</span><span class="label">Journal →</span></a></div></section>
</article>'''
        page(path, st, desc, body, lang=lang, og="article",
             schema=[crumb_ld([("journal.html", "Journal"), (path, "No. " + no)]),
                     {"@context": "https://schema.org", "@type": "Article", "headline": plain, "inLanguage": lang,
                      "image": f"{BASE}/assets/img/{im}.webp", "publisher": {"@id": BASE + "/#org"}, "mainEntityOfPage": BASE + "/" + path.replace(".html", "")}])

    # ============================ ABOUT ============================
    about = f'''
<section class="phero t-ink wrap">
  {crumbs([("about.html", "About")])}
  <h1 class="d d-xxl" data-split>A creative house<br>with a <span class="it gold">point of view</span></h1>
  <div class="row"><p class="lede fade">Grandyra Limited is a branding and communications house in Dhaka. Too many good businesses in Bangladesh are represented by brands that undersell them. We’re here to change that.</p><span></span></div>
</section>
<section class="t-ink" style="padding-bottom:5rem"><div class="cover-band">{photo("buriganga", "studio-01", parallax=True, eager=True)}</div></section>
<section class="sec t-bone wrap"><div class="split2"><div class="side"><p class="label muted">The name</p></div>
<div><p class="big-text fade">Grandyra joins <span class="it">Grand</span> and <span class="it">Era</span>: a grand era for brands built in Bangladesh, made to last.</p>
<p class="big-text fade" style="margin-top:2rem">At the centre of our mark is the Y. It stands for <span class="it">Why.</span> We ask why before we ask how, because every great brand starts with a question.</p></div></div></section>
<section class="marquee t-verm" aria-label="Our principles"><div class="row">{marquee_items}{marquee_items}</div></section>
<section class="sec t-ink wrap"><div class="split2"><div class="side"><p class="label muted">How we work</p><h2 class="d d-m" style="margin-top:1rem">One roof,<br>one <span class="it gold">story</span></h2></div>
<div><p class="big-text fade">Strategy, branding, communication and events sit under one roof. The people who ask the hard questions work next to the people who answer them visually.</p>
<p class="big-text fade muted" style="margin-top:2rem">It means every touchpoint tells the same story, from the first meeting to the last banner.</p>
<div style="display:flex;gap:.6rem;flex-wrap:wrap;margin-top:2.5rem"><a class="pill" href="services.html">What we do</a><a class="pill" href="work.html">Recent work</a></div></div></div></section>
<section class="sec t-bone wrap"><div class="split2"><div class="side"><p class="label muted">Where we’re headed</p></div>
<div><p class="big-text fade">We want to elevate Bangladesh through world-class branding, and to see Bangladeshi creativity recognised around the world.</p></div></div></section>
<section class="voices t-ink wrap" aria-labelledby="fm">
  <p id="fm" class="label muted">Founder’s message</p>
  <blockquote class="fade" style="margin-top:2rem">Greatness is never an accident. It is imagined with vision, built with purpose and refined with intention.</blockquote>
  <p class="label" style="margin-top:2rem">Arman Hossain, Founder &amp; Managing Director</p>
</section>
<section class="t-verm wrap cta-band"><p class="d d-m">Let’s talk about<br>what you’re building.</p><a class="pill solid" href="contact.html" data-magnetic>Start a conversation</a></section>
'''
    page("about.html", "About Grandyra — Branding & Communications House in Dhaka",
         "Grandyra Limited is a branding and communications house in Dhaka, Bangladesh. Learn where the name comes from, how we think and what we believe.",
         about, schema=[ORG, crumb_ld([("about.html", "About")])])

    # ============================ CONTACT ============================
    maps = "https://www.google.com/maps/search/?api=1&query=House+7+Road+4+Gulshan+1+Dhaka+Bangladesh"
    chips = "".join(f'<input type="checkbox" id="s-{s["slug"]}" name="services" value="{s["name"]}"><label for="s-{s["slug"]}">{s["name"]}</label>' for s in SERVICES)
    contact = f'''
<section class="phero t-ink wrap">
  {crumbs([("contact.html", "Contact")])}
  <h1 class="d d-xxl" data-split>Tell us what<br>you’re <span class="it" style="color:var(--verm)">building</span></h1>
</section>
<section class="t-ink wrap" style="padding-bottom:8rem"><div class="split2">
  <div class="side">
    <p class="lede">A few questions help us make the first conversation a useful one. We read every message and reply personally.</p>
    <div style="margin-top:2.5rem"><p class="label muted">Or write to us directly</p>
    <div style="margin-top:.6rem">{mail_row()}</div>
    <p class="label muted" style="margin-top:2rem">Studio</p>
    <address style="font-style:normal;margin-top:.5rem">Grandyra Limited<br>{ADDRESS}<br><a class="ulink" href="{maps}" target="_blank" rel="noopener">Open in Maps</a></address>
    <p class="muted clk" style="margin-top:1.5rem">It’s <span data-clock>--:--</span> in Dhaka right now.</p></div>
  </div>
  <form class="form" data-inquiry data-to="{EMAIL}" data-endpoint="{FORM_ENDPOINT}" novalidate>
    <div class="hp" aria-hidden="true"><label>Leave this field empty<input name="_gotcha" tabindex="-1" autocomplete="off"></label></div>
    <div class="two"><div class="field"><label class="label" for="f1">Your name <span aria-hidden="true">*</span></label><input id="f1" name="name" autocomplete="name" required aria-describedby="e1"><p class="err" id="e1" role="alert"></p></div>
    <div class="field"><label class="label" for="f2">Company</label><input id="f2" name="company" autocomplete="organization"></div></div>
    <div class="field"><label class="label" for="f3">Email address <span aria-hidden="true">*</span></label><input id="f3" type="email" name="email" autocomplete="email" required aria-describedby="e3"><p class="err" id="e3" role="alert"></p></div>
    <fieldset style="border:0;padding:0;margin:0;min-width:0"><legend class="label muted" style="margin-bottom:1rem">What do you need? Pick any that fit</legend><div class="chips">{chips}</div></fieldset>
    <div class="field"><label class="label" for="f6">What are you building? <span aria-hidden="true">*</span></label><textarea id="f6" name="message" required aria-describedby="e6"></textarea><p class="err" id="e6" role="alert"></p></div>
    <div><button class="pill solid" type="submit" data-magnetic>{"Send message" if FORM_ENDPOINT else "Write in your email app"}</button></div>
    {"" if FORM_ENDPOINT else '<p class="form-note">This opens your email app with the message ready to send. Nothing is sent from this page until you press send there.</p>'}
    <p class="status" role="status" aria-live="polite"></p>
  </form>
</div></section>
'''
    page("contact.html", "Contact Grandyra — Start a Branding Project in Dhaka",
         "Start a project with Grandyra, a branding and communications house in Gulshan-1, Dhaka. Tell us what you're building and we'll reply personally.",
         contact, schema=[ORG, crumb_ld([("contact.html", "Contact")])])

    # ============================ 404 ============================
    nf = '''<section class="phero t-ink wrap" style="min-height:80vh"><p class="label gold">404 — Signal lost</p>
<h1 class="d d-xxl" data-split>Just <span class="it">noise</span> here</h1>
<div class="row"><p class="lede fade">This page doesn’t exist, or it moved when we rebuilt the site. Here’s where to go next.</p><span></span></div>
<div style="display:flex;gap:.6rem;flex-wrap:wrap;margin-top:2.5rem"><a class="pill" href="index.html">Home</a><a class="pill" href="work.html">Work</a><a class="pill" href="services.html">Services</a><a class="pill" href="contact.html">Contact</a></div></section>'''
    page("404.html", "Page not found | Grandyra", "This page doesn't exist. Find your way back to Grandyra.", nf, robots="noindex")

    # ============================ sitemap / robots ============================
    svc_pages = [s["slug"] + ".html" for s in SERVICES]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in PAGES:
        if p == "404.html":
            continue
        loc = BASE + "/" + ("" if p == "index.html" else p.replace(".html", ""))
        pr = "1.0" if p == "index.html" else "0.9" if p in svc_pages else "0.7"
        sm.append(f"  <url><loc>{loc}</loc><lastmod>{datetime.date.today().isoformat()}</lastmod><priority>{pr}</priority></url>")
    sm.append("</urlset>")
    open(os.path.join(OUT, "sitemap.xml"), "w").write("\n".join(sm) + "\n")
    robots_txt = "User-agent: *\nDisallow: /\n" if PREVIEW else f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n"
    open(os.path.join(OUT, "robots.txt"), "w").write(robots_txt)
    print("built", len(PAGES), "pages")


if __name__ == "__main__":
    build()
