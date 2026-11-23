#!/usr/bin/env python3
"""Generates the Grandyra static site into ./site from content below."""
import json, os, shutil, html

BASE = "https://grandyra.com"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")


def P(text):
    """Visible placeholder the Grandyra team must replace."""
    return f'<span class="ph-text">[{text}]</span>'


def fig(caption, tone="tone-teal", ratio="", extra=""):
    light = " light" if tone in ("tone-paper", "tone-gold") else ""
    return (f'<figure class="ph {ratio}{light} {extra}"><div class="ph-art {tone}"></div>'
            f'<figcaption>Replace: {html.escape(caption)}</figcaption></figure>')


FONTS = ("https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,300..600,0..100;"
         "1,9..144,300..600,0..100&family=Geist:wght@300..600&family=Hind+Siliguri:wght@400;500;600&display=swap")

NAV = [("work.html", "Work"), ("services.html", "Services"), ("journal.html", "Journal"),
       ("about.html", "About")]


def header(current):
    links = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if h == current else ""}>{t}</a>' for h, t in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap">
  <a class="wordmark" href="index.html" aria-label="Grandyra — home">Grandyra<span>.</span></a>
  <button class="nav-toggle" aria-expanded="false" aria-controls="nav"><span class="lbl">Menu</span><span class="bars" aria-hidden="true"></span></button>
  <nav class="nav" id="nav" aria-label="Main">{links}<a class="btn" href="contact.html">Start a project <span class="arr" aria-hidden="true">→</span></a></nav>
</div></header>'''


def footer():
    svc = "".join(f'<li><a href="{s["slug"]}.html">{s["name"]}</a></li>' for s in SERVICES[:6])
    return f'''<section class="dark cta" aria-labelledby="cta-h">
  <div class="wrap">
    <p class="eyebrow"><span class="num">Next</span> Have something in mind?</p>
    <h2 id="cta-h" class="sr-only">Start a project with Grandyra</h2>
    <a class="big-link" href="contact.html">Let’s talk <em>it through</em> <span class="arr" aria-hidden="true">↗</span></a>
  </div>
</section>
<footer class="site-footer"><div class="wrap">
  <div class="cols">
    <div><p class="tag">Building brands worthy of tomorrow.</p>
      <p class="mt-2">Grandyra Limited<br>Dhaka, Bangladesh<br>{P("Street address")}</p></div>
    <div><h4>Services</h4><ul>{svc}<li><a href="services.html">All services</a></li></ul></div>
    <div><h4>Studio</h4><ul><li><a href="work.html">Work</a></li><li><a href="journal.html">Journal</a></li><li><a href="about.html">About</a></li><li><a href="contact.html">Contact</a></li></ul></div>
    <div><h4>Say hello</h4><ul><li>{P("hello@grandyra.com")}</li><li>{P("+880 phone")}</li><li>{P("LinkedIn")}</li><li>{P("Instagram")}</li></ul></div>
  </div>
  <div class="legal"><span>© <span data-year>2026</span> Grandyra Limited. All rights reserved.</span><span>Strategy before decoration.</span></div>
</div></footer>'''


def crumbs(items):
    parts = ['<a href="index.html">Home</a>']
    for href, label in items[:-1]:
        parts.append(f'<a href="{href}">{label}</a>')
    parts.append(f'<span aria-current="page" style="margin:0">{items[-1][1]}</span>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<span aria-hidden="true">/</span>'.join(parts) + '</nav>'


def crumb_schema(items):
    lst = [{"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"}]
    for i, (href, label) in enumerate(items, start=2):
        lst.append({"@type": "ListItem", "position": i, "name": label, "item": f"{BASE}/{href.replace('.html', '')}"})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": lst}


ORG = {
    "@context": "https://schema.org",
    "@type": "ProfessionalService",
    "@id": BASE + "/#org",
    "name": "Grandyra",
    "legalName": "Grandyra Limited",
    "url": BASE + "/",
    "slogan": "Building brands worthy of tomorrow.",
    "description": "Grandyra is a branding and creative house in Dhaka, Bangladesh, working across brand strategy, identity, packaging, advertising, PR, events and training.",
    "areaServed": {"@type": "Country", "name": "Bangladesh"},
    "address": {"@type": "PostalAddress", "addressLocality": "Dhaka", "addressCountry": "BD"},
    # TODO(Grandyra): add streetAddress, postalCode, telephone, email, geo, openingHours, logo, sameAs.
}


def page(path, title, desc, body, current="", lang="en", schema=None, og_type="website"):
    canonical = BASE + "/" + ("" if path == "index.html" else path.replace(".html", ""))
    schemas = "".join(
        f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in (schema or []))
    hreflang = ""
    doc = f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canonical}">{hreflang}
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#F3EFE7">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Grandyra">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{BASE}/og/{path.replace('.html', '')}.jpg">
<meta property="og:locale" content="{'bn_BD' if lang == 'bn' else 'en_BD'}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="assets/site.css">
{schemas}
</head>
<body>
{header(current)}
<main id="main">
{body}
</main>
{footer()}
<script src="assets/site.js" defer></script>
</body>
</html>
'''
    with open(os.path.join(OUT, path), "w", encoding="utf-8") as f:
        f.write(doc)
    PAGES.append(path)


PAGES = []

# --------------------------------------------------------------------------
# SERVICES — one primary keyword per page (see Stage 1 keyword map)
# --------------------------------------------------------------------------
SERVICES = [
    dict(
        slug="brand-identity-design", name="Brand Creation", tone="tone-teal",
        title="Brand Identity Design & Logo Design in Bangladesh | Grandyra",
        desc="Brand identity design for new companies in Bangladesh: strategy, naming review, logo, visual identity and guidelines from Grandyra, a Dhaka creative house.",
        h1="Brand <em>creation</em>", kw="Brand identity design in Bangladesh",
        lede="A new company has no history to lean on. Its name, its mark and the way it speaks have to earn trust before anyone has a reason to give it. We build that from the ground up — the thinking first, then the identity that carries it.",
        problem=["Most new brands start with a logo and work backwards. It looks fine on a business card and falls apart everywhere else: on a pack, on a billboard, in front of an investor.",
                 "A logo is not a brand. It's the signature at the bottom of one. What matters is what the signature stands for — and whether anyone can tell after a three-second glance."],
        steps=[("Listen", "Conversations with founders, a look at the market and the competitors, and honest questions about where the business is going."),
               ("Position", "Who the brand is for, what it promises, and what it will never be. Written down in plain words everyone can agree on."),
               ("Express", "Logo, typography, colour, imagery and voice — designed as one system, tested on real applications, not mock-ups alone."),
               ("Equip", "Guidelines and files your team, printers and agencies can actually use, so the brand stays itself after we leave.")],
        deliver=["Brand strategy and positioning", "Logo and visual identity system", "Typography, colour and imagery direction", "Tone of voice", "Brand guidelines", "Core applications: stationery, social templates, signage direction"],
        faq=[("How long does brand identity design take?", "It depends on scope. After a first conversation we give you a clear timeline in the proposal, from first workshop to final guidelines."),
             ("Do you only design logos?", "We do design logos, but we rarely design only a logo. A mark without strategy, typography and rules around it tends to get used inconsistently, and an inconsistent brand is expensive to fix later."),
             ("What does a brand identity cost in Bangladesh?", "Every project is scoped individually, so we don't publish a rate card. After a first conversation you get a clear proposal with the scope and the cost.")],
        related=["rebranding", "packaging-design", "brand-launch"],
    ),
    dict(
        slug="rebranding", name="Brand Refresh", tone="tone-deep",
        title="Rebranding Agency in Bangladesh — Brand Refresh | Grandyra",
        desc="Rebranding done carefully: we keep what your customers already trust and change what's holding you back. Brand refresh and rebranding in Dhaka, Bangladesh.",
        h1="Brand <em>refresh</em>", kw="Rebranding in Bangladesh",
        lede="Some brands outgrow their clothes. The business has moved on — new markets, new products, new ambition — and the brand still looks like the company it was ten years ago.",
        problem=["Rebranding is risky because brands carry memory. Change too little and nobody notices; change too much and loyal customers feel like strangers.",
                 "Our job is to tell the difference between what's holding you back and what people already love — then keep the second and fix the first."],
        steps=[("Audit", "We look at everything the brand currently touches and talk to the people who use it, sell it and buy it."),
               ("Decide", "Evolution or revolution? We recommend how far to go, and why, before anything is designed."),
               ("Redesign", "A refreshed identity that feels like a confident next chapter, not a different company."),
               ("Roll out", "A practical transition plan, so signage, packaging and digital change in a sensible order and budget.")],
        deliver=["Brand audit and recommendations", "Refined positioning", "Updated identity system", "Transition and rollout plan", "Updated guidelines"],
        faq=[("How do we know if we need a rebrand?", "Usually the signs are practical: the brand no longer fits what you sell, you're entering a new market, you've merged, or your team keeps making exceptions to the old guidelines. Our Journal has a longer piece on this."),
             ("Will we lose recognition?", "Not if it's done carefully. Most refreshes keep at least one strong existing asset — a colour, a shape, a name — so customers can follow you to the new version."),
             ("Can you rebrand in phases?", "Yes. Many clients roll out digital first and physical assets as stock runs out. We plan it that way from the start.")],
        related=["brand-identity-design", "brand-launch", "corporate-training"],
        journal="journal-when-to-rebrand.html",
    ),
    dict(
        slug="brand-launch", name="Brand Launch", tone="tone-clay",
        title="Brand Launch Campaigns in Bangladesh | Grandyra",
        desc="Launching a new brand or product in Bangladesh? Grandyra plans and creates brand launches: the story, the campaign, the launch event and the first months after.",
        h1="Brand <em>launch</em>", kw="Brand launch in Bangladesh",
        lede="A launch is the one moment everyone is paying attention. It's also the moment most brands spend shouting instead of saying something worth hearing.",
        problem=["A good launch answers one question for the audience: why should I care about this, today? Everything — the campaign, the event, the press, the first social posts — should point at the same answer.",
                 "We plan launches as a sequence, not a single day: what people should hear before, on and after the moment you go live."],
        steps=[("Story", "Finding the one idea the launch is built around."),
               ("Plan", "Channels, timing, budget and the order things happen in."),
               ("Make", "Campaign creative, launch event, PR material and content."),
               ("Sustain", "The first 90 days after launch, so momentum doesn't end with the ribbon-cutting.")],
        deliver=["Launch strategy and timeline", "Campaign concept and creative", "Launch event concept and production", "Press kit and media outreach", "Social launch content"],
        faq=[("How early should we start planning a launch?", "As early as you can. Ideally before the brand is finished, so the identity, the campaign and the event are designed together."),
             ("Can you launch a brand you didn't design?", "Yes. We'll start by understanding the brand you have and build the launch around it."),
             ("Do you handle the event as well?", "Yes — our event production team works alongside the campaign team, so the stage and the advertising tell the same story.")],
        related=["advertising-agency", "event-management", "pr-agency"],
    ),
    dict(
        slug="packaging-design", name="Packaging Design", tone="tone-gold",
        title="Packaging Design Agency in Bangladesh | Grandyra",
        desc="Packaging design in Bangladesh that works on the shelf and in the hand: structure, graphics and print-ready artwork from Grandyra, a Dhaka branding house.",
        h1="Packaging <em>design</em>", kw="Packaging design in Bangladesh",
        lede="On a crowded shelf, your pack has about three seconds to be noticed and understood. Then it has to survive printing, shipping and a customer's kitchen.",
        problem=["Packaging is where brand meets reality. It has to be beautiful, legible, legally compliant, affordable to print and recognisable from two metres away — at the same time.",
                 "We design packaging with the production realities of Bangladesh in mind, so what you approve on screen is what you'll actually see on the shelf."],
        steps=[("Shelf study", "We look at the category as a shopper does — what blends in, what stands out, what's expected."),
               ("Concept", "Two or three distinct directions, shown on realistic mock-ups."),
               ("Refine", "Hierarchy, mandatory information, variants and flavours worked out properly."),
               ("Production", "Print-ready artwork and close work with your printer through the first run.")],
        deliver=["Category and shelf analysis", "Packaging concepts", "Range architecture for variants", "Print-ready artwork", "Printer liaison and press checks"],
        faq=[("Can you work with our existing printer?", "Yes. We prefer to involve your printer early so finishes, materials and colours are realistic from the start."),
             ("Do you design the structure or only the graphics?", "Mainly graphics and brand systems. If a pack needs a new structure, we involve your printer or a structural specialist early."),
             ("How many variants can you handle?", "From a single product to large ranges. We design a system first, so adding a new flavour or size later is simple.")],
        related=["brand-identity-design", "brand-launch", "rebranding"],
    ),
    dict(
        slug="advertising-agency", name="Advertising & Campaigns", tone="tone-ink",
        title="Advertising Agency in Bangladesh — Campaigns | Grandyra",
        desc="Grandyra is an advertising agency in Dhaka creating campaigns people remember: strategy, big ideas, TVC and OVC, print, outdoor and digital across Bangladesh.",
        h1="Advertising <em>&amp; campaigns</em>", kw="Advertising agency in Bangladesh",
        lede="Most advertising is ignored. The rest is remembered for the wrong reasons. We aim for the small, valuable space in between: work people notice, understand and act on.",
        problem=["A campaign starts with a business problem, not a format. Sometimes the answer is a TVC. Sometimes it's a billboard, a stunt or a sentence on a pack.",
                 "We begin with what needs to change — awareness, preference, trial, reputation — and only then decide what to make."],
        steps=[("Brief", "Getting the real problem down on one page, with a clear measure of success."),
               ("Idea", "One strong creative idea that can live across channels."),
               ("Craft", "Scripts, design, production and post — done properly."),
               ("Learn", "Measuring what worked, so the next campaign starts smarter.")],
        deliver=["Communication strategy", "Campaign concept", "TVC / OVC scripts and production", "Print, outdoor and digital creative", "Media recommendations"],
        faq=[("Do you produce video in-house?", "We direct the production and work with trusted production partners, so the finished film matches the idea."),
             ("Do you buy media?", "We recommend where to spend, and we can work with your media agency or ours to buy it."),
             ("What size of campaigns do you take on?", "Everything from focused single-channel campaigns to integrated national work. What matters is a clear problem worth solving.")],
        related=["brand-marketing", "brand-launch", "pr-agency"],
    ),
    dict(
        slug="brand-marketing", name="Brand Marketing", tone="tone-teal",
        title="Brand Marketing Agency in Dhaka | Grandyra",
        desc="Brand marketing that keeps your brand consistent and growing: content, social, digital and always-on communication from Grandyra in Dhaka, Bangladesh.",
        h1="Brand <em>marketing</em>", kw="Brand marketing in Bangladesh",
        lede="A brand is built in the long stretches between campaigns — in the posts, the emails, the brochures and the small decisions nobody notices until they're wrong.",
        problem=["Most brands are disciplined during a launch and drift afterwards. Every new post looks slightly different; every new brochure has a new tone.",
                 "Brand marketing is the steady work of keeping the brand itself, everywhere, every week — while still giving people something worth paying attention to."],
        steps=[("Plan", "A clear yearly plan built around moments that matter to your audience."),
               ("Create", "Content and materials made to the brand's standard, not just the deadline."),
               ("Publish", "Social, digital and offline channels managed consistently."),
               ("Review", "Monthly reporting that focuses on what changed, not vanity numbers.")],
        deliver=["Annual brand marketing plan", "Social media strategy and content", "Digital and print collateral", "Content calendar", "Monthly reporting"],
        faq=[("Is this the same as digital marketing?", "It includes digital, but it's broader: the aim is a stronger brand, not only more clicks. We'll always tell you which channels are worth your money."),
             ("Can you work with our in-house team?", "Yes, and we often do. We can lead, support, or set the standard for your team to follow."),
             ("How do you measure success?", "We agree on a few meaningful measures at the start — enquiries, recall, sales support, sentiment — and report against them.")],
        related=["advertising-agency", "retainer-partnership", "pr-agency"],
    ),
    dict(
        slug="pr-agency", name="Public Relations", tone="tone-deep",
        title="PR Agency in Bangladesh — Public Relations | Grandyra",
        desc="Public relations in Bangladesh: media relations, reputation, press releases and corporate communication from Grandyra, a Dhaka-based creative house.",
        h1="Public <em>relations</em>", kw="PR agency in Bangladesh",
        lede="What other people say about you matters more than anything you say about yourself. PR is the work of earning that — honestly, and over time.",
        problem=["Good PR isn't about volume. A single well-placed story in the right publication often does more than fifty press releases nobody reads.",
                 "We help you find the stories that are genuinely newsworthy, tell them clearly, and be ready for the questions that come back."],
        steps=[("Map", "Who needs to hear from you: media, partners, regulators, communities."),
               ("Shape", "Key messages and stories worth telling."),
               ("Place", "Media relations, interviews, features and events."),
               ("Protect", "Preparation for difficult moments, so you're never writing a statement at midnight from scratch.")],
        deliver=["PR strategy and messaging", "Press releases and media kits", "Media relations", "Spokesperson preparation", "Issues and crisis communication planning"],
        faq=[("Do you guarantee media coverage?", "No honest PR agency can. We do promise stories that are genuinely worth covering, pitched to the right people."),
             ("Can you help during a crisis?", "Yes. Write to us as early as possible and we will tell you honestly how we can help.")],
        related=["brand-launch", "event-management", "advertising-agency"],
    ),
    dict(
        slug="event-management", name="Event Production & Experiences", tone="tone-clay",
        title="Event Management Company in Bangladesh | Grandyra",
        desc="Event management and brand experiences in Dhaka: concept, design, production and on-site management for launches, tournaments, markets and expos.",
        h1="Events <em>&amp; experiences</em>", kw="Event management company in Bangladesh",
        lede="An event is a brand you can walk into. People remember how it felt long after they forget what was said on stage.",
        problem=["Many events are well organised and instantly forgettable — the same stage, the same backdrop, the same running order.",
                 "We design events as brand experiences: one idea carried through the invitation, the space, the programme and what guests take home."],
        steps=[("Concept", "The idea and the feeling the event should leave behind."),
               ("Design", "Space, stage, signage and every touchpoint guests see."),
               ("Produce", "Vendors, logistics, technical production and rehearsals."),
               ("Run", "On-site management, so you can be a host, not a project manager.")],
        deliver=["Event concept and creative", "Venue, stage and spatial design", "Production and vendor management", "On-site event management", "Photo and video coverage"],
        faq=[("What kinds of events do you produce?", "Brand and product launches, tournaments, markets, expos and brand activations. See Real Estate Futsal 2026 and Seheri Nights in our work."),
             ("Do you work outside Dhaka?", "Our studio is in Dhaka, and we are happy to travel for the right project. Tell us where it is and we will plan around it."),
             ("How far in advance should we book?", "The earlier the better. Larger events need a few months. Smaller activations can move faster.")],
        related=["brand-launch", "pr-agency", "advertising-agency"],
        work="work-real-estate-futsal-2026.html",
    ),
    dict(
        slug="corporate-training", name="Corporate Training", tone="tone-gold",
        title="Corporate Training in Bangladesh | Grandyra",
        desc="Corporate training in Bangladesh on brand, communication and creative thinking, so your team can protect and grow the brand from the inside.",
        h1="Corporate <em>training</em>", kw="Corporate training in Bangladesh",
        lede="Your brand is only as strong as the people who represent it every day. Training is how the thinking behind a brand travels from a document into behaviour.",
        problem=["Brand guidelines often end up in a drawer. Teams improvise, and the brand slowly becomes inconsistent — not through bad intent, but because nobody explained the why.",
                 "Our sessions are practical and specific to your business, built on real examples from your own brand."],
        steps=[("Assess", "Understanding where your team is today and what they need."),
               ("Design", "A programme built around your brand, not a generic slide deck."),
               ("Deliver", "Interactive workshops, in person or online."),
               ("Embed", "Tools and follow-ups that keep the learning in daily work.")],
        deliver=["Brand immersion workshops", "Communication and presentation training", "Creative thinking sessions", "Training materials and toolkits"],
        faq=[("Who are the sessions for?", "Leadership teams, marketing and sales teams, and anyone who speaks for the brand."),
             ("How long is a typical programme?", "It depends on your team. Some need a single workshop, others a short series. We agree the format with you first.")],
        related=["rebranding", "brand-identity-design", "retainer-partnership"],
    ),
    dict(
        slug="retainer-partnership", name="Retainer Partnership", tone="tone-ink",
        title="Branding Retainer in Bangladesh | Grandyra",
        desc="A Grandyra retainer gives you a senior creative team on call every month: strategy, design, campaigns and brand guardianship for growing brands in Bangladesh.",
        h1="Retainer <em>partnership</em>", kw="Creative retainer in Bangladesh",
        lede="The best work usually comes from long relationships. A retainer means we know your business well enough to say no to a bad idea — and to bring you good ones before you ask.",
        problem=["Briefing a new agency for every project costs time and money, and you lose the knowledge built up last time.",
                 "A retainer puts a dedicated team on your brand month after month, with clear scope and a single point of contact."],
        steps=[("Scope", "We agree on the work, the team and the monthly rhythm."),
               ("Plan", "A quarterly plan aligned with your business calendar."),
               ("Deliver", "Ongoing creative, strategy and brand guardianship."),
               ("Review", "Regular check-ins on what's working and what to change.")],
        deliver=["Dedicated team and point of contact", "Monthly creative and design support", "Campaign and content planning", "Brand guardianship and quality control", "Quarterly strategy reviews"],
        faq=[("What's included in a retainer?", "Each retainer is shaped around your needs: design, campaigns, content and brand guardianship, with a clear monthly rhythm."),
             ("What's the minimum commitment?", "We agree the term together. A retainer works best over several months, because the value comes from knowing your business well."),
             ("Can the scope change over time?", "Yes. We review scope regularly and adjust as your priorities change.")],
        related=["brand-marketing", "advertising-agency", "corporate-training"],
    ),
]
SVC = {s["slug"]: s for s in SERVICES}

# --------------------------------------------------------------------------
# WORK — only verified projects. Fill details from Grandyra's own records.
# --------------------------------------------------------------------------
WORK = [
    dict(no="01", slug="work-real-estate-futsal-2026.html", title="Real Estate Futsal 2026", client="Real Estate Futsal 2026",
         disc="Event creative partner", year="2026", tone="tone-teal", caption="Tournament key visual"),
    dict(no="02", slug=None, title=P("Project name"), client=P("Client"), disc="Brand creation", year=P("Year"), tone="tone-clay", caption="Identity system"),
    dict(no="03", slug=None, title=P("Project name"), client=P("Client"), disc="Packaging design", year=P("Year"), tone="tone-gold", caption="Pack range"),
    dict(no="04", slug=None, title=P("Project name"), client=P("Client"), disc="Advertising campaign", year=P("Year"), tone="tone-ink", caption="Campaign key visual"),
    dict(no="05", slug=None, title=P("Project name"), client=P("Client"), disc="Brand refresh", year=P("Year"), tone="tone-deep", caption="Before / after"),
]


def work_rows(limit=None):
    out = []
    for w in WORK[:limit]:
        href = w["slug"] or "work.html"
        out.append(f'''<li class="work-row"><a href="{href}" data-tone="{w["tone"]}" data-caption="Replace: {w["caption"]}">
  <span class="no">{w["no"]}</span><span class="title">{w["title"]}</span>
  <span class="meta">{w["disc"]}</span><span class="meta">{w["year"]}</span><span class="go" aria-hidden="true">→</span></a></li>''')
    return '<ul class="work-list">' + "".join(out) + '</ul><div class="preview" aria-hidden="true"><div class="inner"></div></div>'


# --------------------------------------------------------------------------
# JOURNAL
# --------------------------------------------------------------------------
ISSUES = [
    dict(no="01", slug="journal-strategy-before-decoration.html", title="Strategy before decoration", sub="Why we start every project with a question, not a sketch.", tone="tone-ink", topic="Brand Creation"),
    dict(no="02", slug="journal-when-to-rebrand.html", title="When should a company rebrand?", sub="And, just as important, when it shouldn't.", tone="tone-teal", topic="Brand Refresh"),
    dict(no="03", slug="journal-logo-design-bangla.html", title="লোগো ডিজাইন: একটি লোগো আসলে কী করে", sub="বাংলায় — ভালো লোগো চেনার সহজ উপায়।", tone="tone-clay", topic="Logo Design", bn=True),
    dict(no="04", slug=None, title="What a pack says in three seconds", sub="Coming soon", tone="tone-gold", topic="Packaging"),
    dict(no="05", slug=None, title="The campaign nobody skipped", sub="Coming soon", tone="tone-deep", topic="Advertising"),
    dict(no="06", slug=None, title="Events people talk about on Monday", sub="Coming soon", tone="tone-paper", topic="Experiences"),
]


def issue_cards(items):
    out = []
    for i in items:
        cls = "issue" + ("" if i["slug"] else " soon")
        paper = " paper" if i["tone"] in ("tone-paper", "tone-gold") else ""
        bn = ' lang="bn"' if i.get("bn") else ""
        inner = f'''<div class="cover {i["tone"]}{paper}"><div class="top"><span>The Grandyra Journal</span><span>No. {i["no"]}</span></div>
<div class="big" aria-hidden="true">{i["no"]}</div><div class="ttl"{bn}>{i["title"]}</div></div>
<p class="cap"><span>{i["topic"]}</span> — <span{bn}>{i["sub"]}</span></p>'''
        if i["slug"]:
            out.append(f'<a class="{cls} reveal" href="{i["slug"]}">{inner}</a>')
        else:
            out.append(f'<div class="{cls} reveal" aria-label="Coming soon: {i["title"]}">{inner}</div>')
    return '<div class="issues">' + "".join(out) + '</div>'


# ==========================================================================
# BUILD
# ==========================================================================
def build():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "assets"))
    shutil.copy(os.path.join(SRC, "site.css"), os.path.join(OUT, "assets", "site.css"))
    shutil.copy(os.path.join(SRC, "site.js"), os.path.join(OUT, "assets", "site.js"))

    # ---------------- HOME ----------------
    caps = "".join(
        f'<li><a href="{s["slug"]}.html"><span class="n">{i:02d}</span><span class="t">{s["name"]}</span><span aria-hidden="true">→</span></a></li>'
        for i, s in enumerate(SERVICES, 1))
    home = f'''
<section class="hero"><div class="wrap">
  <p class="eyebrow reveal in"><span class="num">Grandyra</span> A branding &amp; creative house in Dhaka</p>
  <h1>Good brands are built on better <span class="strike">decoration</span> <em class="fix">thinking.</em></h1>
  <div class="hero-foot">
    <p class="lede">We’re a branding agency in Bangladesh that starts with the business problem — then turns it into brands, campaigns and experiences people remember.</p>
    <p class="note">Strategy first. Then the beautiful part.</p>
    <a class="scroll" href="#work">Selected work ↓</a>
  </div>
</div></section>

<section class="wrap reveal" aria-label="Featured project">
  {fig("hero image from Grandyra's strongest project — real photography, no stock", "tone-teal", "ratio-pano")}
</section>

<section class="section" id="work" aria-labelledby="work-h"><div class="wrap">
  <div class="flex-between mb-3">
    <div><p class="eyebrow"><span class="num">01</span> Selected work</p>
    <h2 id="work-h" class="reveal">The work does <em>the talking.</em></h2></div>
    <a class="link" href="work.html">All projects →</a>
  </div>
  {work_rows(5)}
</div></section>

<section class="section dark" aria-labelledby="phil-h"><div class="wrap">
  <div class="grid">
    <div class="span-5"><p class="eyebrow"><span class="num">02</span> What we believe</p>
      <h2 id="phil-h" class="reveal">A few things we <em>won’t</em> compromise on.</h2>
      <p class="mt-2 reveal">These aren’t slogans on a wall. They’re the questions we ask in every review — and the reasons we sometimes push back on a brief.</p></div>
    <div class="span-7"><ul class="principles">
      <li class="reveal"><span>Greatness</span><span>noise</span></li>
      <li class="reveal"><span>Clarity</span><span>complexity</span></li>
      <li class="reveal"><span>Timeless</span><span>temporary</span></li>
      <li class="reveal no-over"><span>Strategy</span><span>decoration</span></li>
    </ul></div>
  </div>
</div></section>

<section class="section" aria-labelledby="cap-h"><div class="wrap">
  <div class="grid">
    <div class="span-4"><p class="eyebrow"><span class="num">03</span> What we do</p>
      <h2 id="cap-h" class="reveal">Connected <em>disciplines.</em></h2>
      <p class="mt-2 muted reveal">Most clients come to us for one thing and stay for the way it connects to everything else. A brand, its launch, its campaigns and its events should feel like one voice.</p>
      <p class="note mt-2">Every service starts in the same place: what needs to change for the business.</p></div>
    <div class="span-8"><ul class="cap-list">{caps}</ul></div>
  </div>
</div></section>

<section class="section rule" aria-labelledby="how-h"><div class="wrap">
  <p class="eyebrow"><span class="num">04</span> How we think</p>
  <h2 id="how-h" class="reveal mb-3" style="max-width:18ch">Four steps. <em>No shortcuts</em> through the first one.</h2>
  <ol class="steps">
    <li class="reveal"><h3>Understand</h3><p>The business, the market and the people you need to reach — before a single idea.</p></li>
    <li class="reveal reveal-d1"><h3>Define</h3><p>One clear problem and one clear promise, written in plain words.</p></li>
    <li class="reveal reveal-d2"><h3>Create</h3><p>Ideas with a reason behind them, crafted until they’re right.</p></li>
    <li class="reveal reveal-d3"><h3>Deliver</h3><p>From the first conversation to the final experience, with the same team.</p></li>
  </ol>
</div></section>

<section class="section" style="background:var(--paper-2)" aria-labelledby="j-h"><div class="wrap">
  <div class="flex-between mb-3">
    <div><p class="eyebrow"><span class="num">05</span> The Grandyra Journal</p>
    <h2 id="j-h" class="reveal">Ideas we’d rather <em>show</em> than sell.</h2></div>
    <a class="link" href="journal.html">Read the Journal →</a>
  </div>
  {issue_cards(ISSUES[:3])}
</div></section>

<section class="section" aria-labelledby="t-h"><div class="wrap">
  <div class="grid">
    <div class="span-4"><p class="eyebrow"><span class="num">06</span> In their words</p>
      <h2 id="t-h" class="reveal">Clients, <em>unfiltered.</em></h2></div>
    <div class="span-8">
      <blockquote class="reveal" style="margin:0;font-family:var(--serif);font-size:clamp(1.6rem,3vw,2.6rem);line-height:1.2;letter-spacing:-.02em">
        “{P("Real client testimonial — verbatim, with permission")}”
      </blockquote>
      <p class="mt-2 muted">— {P("Name, title, company")}</p>
      <p class="dev-note">Only real, approved testimonials go here. Client logos too: add them only with written permission.</p>
    </div>
  </div>
</div></section>

<section class="section rule" aria-labelledby="h-h"><div class="wrap">
  <div class="grid">
    <div class="span-5"><p class="eyebrow"><span class="num">07</span> The studio</p>
      <h2 id="h-h" class="reveal">Real people. <em>Real arguments</em> about kerning.</h2>
      <p class="mt-2 muted reveal">Behind every project is a small team that cares a slightly unreasonable amount about getting it right.</p>
      <a class="link mt-2" style="display:inline-block" href="about.html">Meet the studio →</a></div>
    <div class="span-7 grid" style="grid-template-columns:1fr 1fr;gap:1rem">
      <div style="grid-column:span 1">{fig("team at work — candid, natural light", "tone-paper", "ratio-tall")}</div>
      <div style="grid-column:span 1;margin-top:4rem">{fig("a review session / sketches on the wall", "tone-gold", "ratio-tall")}</div>
    </div>
  </div>
</div></section>
'''
    page("index.html", "Grandyra — Branding Agency in Bangladesh | Creative House, Dhaka",
         "Grandyra is a branding and creative house in Dhaka, Bangladesh. Brand identity, rebranding, packaging, advertising, PR and events — built on better thinking.",
         home, "", schema=[ORG, {"@context": "https://schema.org", "@type": "WebSite", "name": "Grandyra", "url": BASE + "/"}])

    # ---------------- WORK ----------------
    work = f'''
<section class="page-head"><div class="wrap">
  {crumbs([("work.html", "Work")])}
  <h1>Selected <em>work.</em></h1>
  <p class="lede">Brands, campaigns and experiences — and the thinking behind each one.</p>
</div></section>
<section class="section tight"><div class="wrap">
  {work_rows()}
  <p class="dev-note">Grandyra team: add 4–6 verified projects. Each needs a client, discipline, year, the brief, the thinking, the work (real images) and any verified results. Placeholder rows link back here until their case studies exist.</p>
</div></section>
'''
    page("work.html", "Our Work — Branding & Creative Projects in Bangladesh | Grandyra",
         "Selected branding, packaging, advertising and event projects by Grandyra, a creative house in Dhaka — with the thinking behind each one.",
         work, "work.html", schema=[crumb_schema([("work.html", "Work")])])

    # ---------------- CASE STUDY ----------------
    cs = f'''
<section class="page-head"><div class="wrap">
  {crumbs([("work.html", "Work"), ("work-real-estate-futsal-2026.html", "Real Estate Futsal 2026")])}
  <p class="eyebrow"><span class="num">01</span> Case study</p>
  <h1>Real Estate <em>Futsal</em> 2026</h1>
  <p class="lede">{P("One-sentence summary of the project and Grandyra's role as creative partner")}</p>
</div></section>
<section class="wrap">
  <dl class="facts">
    <div><dt>Client</dt><dd>{P("Organiser")}</dd></div>
    <div><dt>Role</dt><dd>Creative partner</dd></div>
    <div><dt>Venue</dt><dd>{P("Venue, e.g. ISD")}</dd></div>
    <div><dt>Year</dt><dd>2026</dd></div>
  </dl>
</section>
<section class="wrap mt-3 reveal">{fig("hero photograph from the tournament", "tone-teal", "ratio-pano")}</section>
<section class="section"><div class="wrap grid">
  <div class="span-4"><p class="eyebrow"><span class="num">A</span> The challenge</p></div>
  <div class="span-7 start-6 prose"><p>{P("What the organisers needed and why it was hard. 2–3 sentences in plain language.")}</p></div>
</div></section>
<section class="section rule"><div class="wrap grid">
  <div class="span-4"><p class="eyebrow"><span class="num">B</span> The thinking</p><p class="note">The insight that shaped everything else.</p></div>
  <div class="span-7 start-6 prose"><p>{P("The strategic idea behind the creative work.")}</p></div>
</div></section>
<section class="wrap grid reveal" style="gap:1rem">
  <div class="span-7">{fig("key visual / identity", "tone-ink", "ratio-sq")}</div>
  <div class="span-5" style="display:grid;gap:1rem">{fig("jersey or merchandise", "tone-gold", "ratio-wide")}{fig("venue branding", "tone-clay", "ratio-wide")}</div>
</section>
<section class="section"><div class="wrap grid">
  <div class="span-4"><p class="eyebrow"><span class="num">C</span> Execution</p></div>
  <div class="span-7 start-6 prose"><p>{P("What was made: key visual, venue branding, digital, merchandise, event-day materials.")}</p></div>
</div></section>
<section class="section rule"><div class="wrap grid">
  <div class="span-4"><p class="eyebrow"><span class="num">D</span> Outcome</p></div>
  <div class="span-7 start-6 prose"><p>{P("Verified results only — attendance, coverage, client feedback. Leave out if not available.")}</p>
  <div class="related mt-2"><a class="chip" href="event-management.html">Event production</a><a class="chip" href="brand-launch.html">Brand launch</a><a class="chip" href="work.html">All work</a></div></div>
</div></section>
'''
    page("work-real-estate-futsal-2026.html", "Real Estate Futsal 2026 — Event Creative Case Study | Grandyra",
         "How Grandyra worked as creative partner for Real Estate Futsal 2026 in Dhaka: the challenge, the thinking and the event creative.",
         cs, "work.html", og_type="article",
         schema=[crumb_schema([("work.html", "Work"), ("work-real-estate-futsal-2026.html", "Real Estate Futsal 2026")]),
                 {"@context": "https://schema.org", "@type": "CreativeWork", "name": "Real Estate Futsal 2026", "creator": {"@id": BASE + "/#org"}, "dateCreated": "2026"}])

    # ---------------- SERVICES HUB ----------------
    rows = ""
    for i, s in enumerate(SERVICES, 1):
        rows += f'''<a class="work-row-svc" href="{s["slug"]}.html" style="display:grid;grid-template-columns:4rem 1fr 1fr 2rem;gap:1.5rem;align-items:baseline;padding:1.8rem 0;border-bottom:1px solid var(--line);text-decoration:none">
<span class="note" style="max-width:none">{i:02d}</span><span class="t" style="font-family:var(--serif);font-size:clamp(1.6rem,3vw,2.6rem);letter-spacing:-.02em;line-height:1.05">{s["name"]}</span>
<span class="muted" style="font-size:.95rem">{s["problem"][0].split(". ")[0]}.</span><span aria-hidden="true">→</span></a>'''
    hub = f'''
<section class="page-head"><div class="wrap">
  {crumbs([("services.html", "Services")])}
  <h1>What we <em>do.</em></h1>
  <p class="lede">Ten disciplines, one way of thinking. Start wherever your problem is — we’ll connect the rest.</p>
</div></section>
<section class="section tight"><div class="wrap">
  <div style="border-top:1px solid var(--line-strong)" class="svc-list">{rows}</div>
</div></section>
<style>.svc-list a:hover .t{{color:var(--teal);font-style:italic}} @media(max-width:800px){{.svc-list a{{grid-template-columns:2.5rem 1fr !important}} .svc-list a > :nth-child(3), .svc-list a > :nth-child(4){{display:none}}}}</style>
'''
    page("services.html", "Branding, Advertising & Event Services in Bangladesh | Grandyra",
         "Brand identity, rebranding, packaging, advertising, brand marketing, PR, events, corporate training and retainers — Grandyra's services in Dhaka, Bangladesh.",
         hub, "services.html", schema=[crumb_schema([("services.html", "Services")])])

    # ---------------- SERVICE PAGES ----------------
    for s in SERVICES:
        steps = "".join(f'<li class="reveal"><h3>{t}</h3><p>{d}</p></li>' for t, d in s["steps"])
        deliv = "".join(f"<li>{d}</li>" for d in s["deliver"])
        faqs = "".join(f'<details><summary>{q}</summary><div class="a"><p>{a}</p></div></details>' for q, a in s["faq"])
        rel = "".join(f'<a class="chip" href="{r}.html">{SVC[r]["name"]}</a>' for r in s["related"])
        extra = ""
        if s.get("journal"):
            extra += f'<p class="mt-2"><a class="link" href="{s["journal"]}">Read: When should a company rebrand? →</a></p>'
        if s.get("work"):
            extra += f'<p class="mt-2"><a class="link" href="{s["work"]}">See: Real Estate Futsal 2026 →</a></p>'
        body = f'''
<section class="page-head"><div class="wrap">
  {crumbs([("services.html", "Services"), (s["slug"] + ".html", s["name"])])}
  <p class="eyebrow"><span class="num">Service</span> {s["kw"]}</p>
  <h1>{s["h1"]}</h1>
  <p class="lede">{s["lede"]}</p>
</div></section>
<section class="wrap reveal">{fig(f'{s["name"].lower()} work from a real Grandyra project', s["tone"], "ratio-pano")}</section>
<section class="section"><div class="wrap grid">
  <div class="span-4"><p class="eyebrow"><span class="num">01</span> The problem</p></div>
  <div class="span-7 start-6 prose">{"".join(f"<p>{p}</p>" for p in s["problem"])}</div>
</div></section>
<section class="section rule"><div class="wrap">
  <p class="eyebrow"><span class="num">02</span> How we approach it</p>
  <ol class="steps mt-2">{steps}</ol>
</div></section>
<section class="section rule"><div class="wrap grid">
  <div class="span-4"><p class="eyebrow"><span class="num">03</span> What you receive</p>
    <p class="note">Scoped to your needs — this is the usual shape, not a fixed menu.</p></div>
  <div class="span-7 start-6"><ul class="deliver">{deliv}</ul>{extra}</div>
</div></section>
<section class="section rule"><div class="wrap grid">
  <div class="span-4"><p class="eyebrow"><span class="num">04</span> Questions</p>
    <h2 class="reveal" style="font-size:clamp(1.8rem,3vw,2.6rem)">Asked <em>often.</em></h2></div>
  <div class="span-7 start-6 faq">{faqs}</div>
</div></section>
<section class="section tight rule"><div class="wrap flex-between">
  <div><p class="eyebrow" style="margin-bottom:1rem"><span class="num">05</span> Related</p><div class="related">{rel}</div></div>
  <a class="btn" href="contact.html">Talk to us about {s["name"].lower()} <span class="arr" aria-hidden="true">→</span></a>
</div></section>
'''
        faq_schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": html.unescape(
                __import__("re").sub(r"<[^>]+>", "", a))}} for q, a in s["faq"] if "ph-text" not in a]}
        schemas = [crumb_schema([("services.html", "Services"), (s["slug"] + ".html", s["name"])]),
                   {"@context": "https://schema.org", "@type": "Service", "name": s["name"], "serviceType": s["kw"],
                    "provider": {"@id": BASE + "/#org"}, "areaServed": {"@type": "Country", "name": "Bangladesh"},
                    "description": s["desc"]}]
        if faq_schema["mainEntity"]:
            schemas.append(faq_schema)
        page(s["slug"] + ".html", s["title"], s["desc"], body, "services.html", schema=schemas)

    # ---------------- JOURNAL HUB ----------------
    jh = f'''
<section class="page-head"><div class="wrap">
  {crumbs([("journal.html", "Journal")])}
  <h1>The Grandyra <em>Journal.</em></h1>
  <p class="lede">A slow publication about brands, ideas and the craft of making them. Numbered issues, in English and বাংলা.</p>
</div></section>
<section class="section tight"><div class="wrap">{issue_cards(ISSUES)}</div></section>
'''
    page("journal.html", "The Grandyra Journal — Ideas on Branding & Creativity",
         "The Grandyra Journal: numbered issues on branding, rebranding, logo design, packaging and advertising, from a creative house in Dhaka. In English and Bangla.",
         jh, "journal.html", schema=[crumb_schema([("journal.html", "Journal")])])

    def article(path, no, title_html, title_plain, seo_title, desc, topic, tone, prose, lang="en", related=None, kicker="Issue"):
        rel = "".join(f'<a class="chip" href="{r}.html">{SVC[r]["name"]}</a>' for r in (related or []))
        body = f'''
<article>
<section class="page-head"><div class="wrap">
  {crumbs([("journal.html", "Journal"), (path, f"No. {no}")])}
  <p class="eyebrow"><span class="num">No. {no}</span> {topic}</p>
  <h1 style="max-width:18ch">{title_html}</h1>
  <p class="mt-2 muted">{P("Author name")} · {P("Publish date")} · {P("Reading time")}</p>
</div></section>
<section class="wrap"><div class="ph ratio-pano {tone}" role="img" aria-label="Issue {no} cover"><div class="ph-art {tone}"></div>
  <div style="position:absolute;inset:0;display:flex;align-items:flex-end;justify-content:space-between;padding:clamp(1rem,3vw,2.5rem);color:var(--paper);z-index:2">
  <span style="font-family:var(--serif);font-style:italic;font-size:clamp(5rem,14vw,13rem);line-height:.8">{no}</span>
  <span style="font-size:.75rem;letter-spacing:.14em;text-transform:uppercase">The Grandyra Journal</span></div></div></section>
<section class="section"><div class="wrap grid">
  <aside class="span-3"><p class="note">{kicker} {no} of the Grandyra Journal.</p></aside>
  <div class="span-8 start-5 prose">{prose}
    <div class="mt-3"><p class="eyebrow" style="margin-bottom:1rem"><span class="num">→</span> Related</p><div class="related">{rel}<a class="chip" href="journal.html">All issues</a></div></div>
  </div>
</div></section>
</article>'''
        page(path, seo_title, desc, body, "journal.html", lang=lang, og_type="article",
             schema=[crumb_schema([("journal.html", "Journal"), (path, f"No. {no}")]),
                     {"@context": "https://schema.org", "@type": "Article", "headline": title_plain, "inLanguage": "bn" if lang == "bn" else "en",
                      "publisher": {"@id": BASE + "/#org"}, "mainEntityOfPage": BASE + "/" + path.replace(".html", "")}])

    article("journal-strategy-before-decoration.html", "01", "Strategy before <em>decoration.</em>", "Strategy before decoration",
            "Strategy Before Decoration — Why Brands Start With Thinking | Grandyra Journal",
            "Why every Grandyra project starts with a question, not a sketch — and what that means for the brands we build in Bangladesh.",
            "Brand Creation", "tone-ink", """
<p>Every designer knows the temptation. A brief arrives, and before the meeting is over there are already sketches in the margin of the notebook. A colour. A shape. A typeface that would look good on the sign.</p>
<p>We try hard to resist it. Not because sketches are bad, but because a sketch made too early answers a question nobody has asked yet.</p>
<h2>Decoration is easy to agree on</h2>
<p>It's much easier to have an opinion about a logo than about a positioning statement. Logos are visible; strategy is a paragraph in a document. So meetings drift towards what people can see, and the hard decisions get made quietly by accident.</p>
<p>That's how a company ends up with a beautiful identity that says the wrong thing — premium when the business is built on value, playful when the customers want reassurance.</p>
<blockquote>The work becomes beautiful once it becomes clear.</blockquote>
<h2>What we ask first</h2>
<ul>
<li>What has to change for this business in the next three years?</li>
<li>Who are we trying to convince, and what do they believe today?</li>
<li>What can this brand say that its competitors can't?</li>
<li>What would we be embarrassed to promise?</li>
</ul>
<p>The answers are rarely glamorous. But they turn creative work from a matter of taste into a matter of judgement — and judgement is something a client and an agency can actually discuss.</p>
<h2>Then the beautiful part</h2>
<p>Strategy before decoration doesn't mean strategy instead of decoration. Craft matters enormously. People feel the difference between a typeface chosen with care and one chosen in a hurry, even if they can't name it.</p>
<p>It just means the craft has a job to do. When it does, it lasts.</p>
""", related=["brand-identity-design", "rebranding"])

    article("journal-when-to-rebrand.html", "02", "When should a company <em>rebrand?</em>", "When should a company rebrand?",
            "When Should a Company Rebrand? Signs, Risks & How to Decide | Grandyra",
            "How to tell whether your company needs a rebrand, a refresh, or neither — practical signs, common mistakes and how to decide, from a Dhaka branding agency.",
            "Brand Refresh", "tone-teal", """
<p>Rebranding is one of the most expensive decisions a company can make, and one of the easiest to make for the wrong reasons. A new CEO wants a fresh start. Someone saw a competitor's new logo. The office is being renovated anyway.</p>
<p>None of those are good reasons on their own. Here's how we think about it.</p>
<h2>Good reasons to rebrand</h2>
<ul>
<li><strong>The business has changed.</strong> You started as a trading company and now you manufacture. You sold one product; now you sell twenty. The brand still describes the old company.</li>
<li><strong>You're entering a new market.</strong> A brand that works in Dhaka may not travel to Dubai or to a younger audience at home.</li>
<li><strong>A merger or acquisition.</strong> Two brands, one company — something has to give.</li>
<li><strong>Your reputation is holding you back.</strong> Rarely solved by design alone, but a rebrand can mark a genuine change in behaviour.</li>
<li><strong>Nobody can use the brand properly.</strong> If every new brochure needs an exception to the guidelines, the system is broken.</li>
</ul>
<h2>Reasons that usually aren't enough</h2>
<ul>
<li>The team is bored of the logo. (Customers are usually not.)</li>
<li>A competitor rebranded.</li>
<li>It's been a while.</li>
</ul>
<blockquote>Your team sees the brand every day. Your customers see it for a few seconds. Fatigue is felt inside long before it's felt outside.</blockquote>
<h2>Refresh or rebrand?</h2>
<p>Most companies don't need a revolution. A <a class="link" href="rebranding.html">brand refresh</a> keeps what people already recognise — a colour, a symbol, a name — and fixes what's holding the brand back: dated typography, a messy system, an unclear message.</p>
<p>A full rebrand makes sense when the old brand is actively working against where the business is going.</p>
<h2>How to decide</h2>
<p>Start with an honest audit. Gather everything the brand touches, talk to customers and staff, and ask one question: does this still describe who we are and where we're going? The answer usually makes the scale of the change obvious.</p>
""", related=["rebranding", "brand-identity-design", "brand-launch"])

    article("journal-logo-design-bangla.html", "03", "লোগো ডিজাইন: একটি লোগো আসলে <em>কী করে?</em>", "লোগো ডিজাইন: একটি লোগো আসলে কী করে?",
            "লোগো ডিজাইন: ভালো লোগো কী এবং কীভাবে বানাবেন | Grandyra Journal",
            "লোগো ডিজাইন নিয়ে সহজ বাংলায় একটি গাইড: ভালো লোগোর বৈশিষ্ট্য, সাধারণ ভুল, এবং আপনার ব্যবসার জন্য লোগো বানানোর আগে কী ভাববেন।",
            "লোগো ডিজাইন", "tone-clay", """
<p>লোগো নিয়ে আমরা সবাই কথা বলতে পছন্দ করি। রং ভালো লাগলো কি না, আকারটা সুন্দর কি না — এসব নিয়ে মতামত দেওয়া সহজ। কিন্তু একটা লোগো আসলে কী কাজ করে, সেই প্রশ্নটা খুব কম জনই করেন।</p>
<h2>লোগো ব্র্যান্ড নয়</h2>
<p>লোগো হলো ব্র্যান্ডের স্বাক্ষর। স্বাক্ষর গুরুত্বপূর্ণ, কিন্তু স্বাক্ষরের পেছনে যে মানুষটা আছে, তার পরিচয়টাই আসল। তেমনি একটা প্রতিষ্ঠান কী বিশ্বাস করে, কাদের জন্য কাজ করে, এবং কেন তাকে বেছে নেওয়া উচিত — এই উত্তরগুলোই ব্র্যান্ড। লোগো সেই উত্তরগুলোকে এক নজরে মনে করিয়ে দেয়।</p>
<h2>একটি ভালো লোগোর পাঁচটি গুণ</h2>
<ul>
<li><strong>সরল:</strong> এক নজরে চেনা যায়, মনে রাখা যায়।</li>
<li><strong>ছোট-বড় সব মাপে কাজ করে:</strong> মোবাইলের ছোট আইকন থেকে বিলবোর্ড পর্যন্ত।</li>
<li><strong>এক রঙেও টিকে থাকে:</strong> সাদা-কালোয় ছাপালেও চেনা যায়।</li>
<li><strong>প্রতিষ্ঠানের চরিত্রের সাথে মেলে:</strong> একটি হাসপাতাল আর একটি খেলনার দোকানের লোগো একরকম হবে না।</li>
<li><strong>সময়ের পরীক্ষায় টেকে:</strong> আজকের ট্রেন্ড অনুসরণ করা লোগো দুই বছর পর পুরোনো লাগে।</li>
</ul>
<blockquote>ভালো লোগো চিৎকার করে না। সে শুধু মনে থেকে যায়।</blockquote>
<h2>সাধারণ কিছু ভুল</h2>
<ul>
<li>লোগোতে সব কিছু বলার চেষ্টা করা — পণ্য, সেবা, শহর, মূল্যবোধ।</li>
<li>অন্য কোনো পরিচিত ব্র্যান্ডের মতো দেখতে বানানো।</li>
<li>শুধু স্ক্রিনে দেখে অনুমোদন দেওয়া, বাস্তব ব্যবহারে পরীক্ষা না করা।</li>
<li>লোগো তৈরির পর ব্যবহারের নিয়ম (গাইডলাইন) না রাখা।</li>
</ul>
<h2>লোগো বানানোর আগে নিজেকে তিনটি প্রশ্ন করুন</h2>
<p>আমাদের গ্রাহক কারা? আমরা তাদের কাছে কী প্রতিশ্রুতি দিই? আর আমাদের প্রতিযোগীদের থেকে আমরা কোথায় আলাদা? এই উত্তরগুলো পরিষ্কার থাকলে লোগো ডিজাইন অনেক সহজ এবং অর্থবহ হয়।</p>
<p>আপনার প্রতিষ্ঠানের জন্য নতুন পরিচিতি তৈরি করতে চাইলে আমাদের <a class="link" href="brand-identity-design.html">ব্র্যান্ড আইডেন্টিটি ডিজাইন</a> সেবা সম্পর্কে জানুন।</p>
""", lang="bn", related=["brand-identity-design", "rebranding"], kicker="সংখ্যা")

    # ---------------- ABOUT ----------------
    about = f'''
<section class="page-head"><div class="wrap">
  {crumbs([("about.html", "About")])}
  <h1>A creative house with a <em>point of view.</em></h1>
  <p class="lede">Grandyra Limited is a branding and creative house in Dhaka. We exist for one reason: too many good businesses in Bangladesh are represented by brands that undersell them.</p>
</div></section>
<section class="wrap reveal">{fig("studio photograph — the real space, real people", "tone-paper", "ratio-pano")}</section>
<section class="section"><div class="wrap grid">
  <div class="span-4"><p class="eyebrow"><span class="num">01</span> Why we exist</p></div>
  <div class="span-7 start-6 prose">
    <p>{P("Grandyra's real founding story, in the founder's words: when, why, and what you saw missing. Do not invent.")}</p>
    <p>What we believe is simple: brands are built on thinking, not decoration. A brand that knows what it stands for can be bold, quiet, playful or serious — and still be unmistakably itself.</p>
  </div>
</div></section>
<section class="section dark"><div class="wrap grid">
  <div class="span-5"><p class="eyebrow"><span class="num">02</span> How we work</p>
    <h2 class="reveal">Strategy and creativity in <em>the same room.</em></h2></div>
  <div class="span-6 start-7 prose">
    <p>In many agencies, strategists hand a document to designers and leave. We don't separate them. The people who ask the hard questions sit next to the people who answer them visually — from the first meeting to the final file.</p>
    <p>It's slower at the start and much faster at the end. Fewer surprises, fewer rounds of revisions, and work that holds together.</p>
  </div>
</div></section>
<section class="section"><div class="wrap">
  <p class="eyebrow"><span class="num">03</span> The people</p>
  <h2 class="reveal mb-3">The team behind <em>the work.</em></h2>
  <div class="grid" style="grid-template-columns:repeat(4,1fr)">
    {"".join(f'<div class="reveal">{fig("team portrait", t, "ratio-tall")}<p class="mt-1" style="font-family:var(--serif);font-size:1.2rem;margin-bottom:0">{P("Name")}</p><p class="muted" style="font-size:.9rem">{P("Role")}</p></div>' for t in ("tone-paper", "tone-gold", "tone-paper", "tone-gold"))}
  </div>
  <p class="dev-note">Real team only: names, roles and photographs supplied by Grandyra. Remove this grid if you prefer to show the studio rather than individuals.</p>
</div></section>
<section class="section rule"><div class="wrap grid">
  <div class="span-4"><p class="eyebrow"><span class="num">04</span> Principles</p></div>
  <div class="span-7 start-6"><ul class="deliver">
    <li>Greatness over noise.</li><li>Clarity over complexity.</li><li>Timeless over temporary.</li>
    <li>Strategy before decoration.</li><li>Creativity with a reason.</li><li>Ideas that change something in the real world.</li>
  </ul></div>
</div></section>
'''
    page("about.html", "About Grandyra — Branding & Creative House in Dhaka",
         "Grandyra Limited is a branding and creative house in Dhaka, Bangladesh, where strategy and creativity work in the same room. Meet the studio and what we believe.",
         about, "about.html", schema=[ORG, crumb_schema([("about.html", "About")])])

    # ---------------- CONTACT ----------------
    opts = "".join(
        f'<input type="checkbox" id="s-{s["slug"]}" name="services" value="{s["name"]}"><label for="s-{s["slug"]}">{s["name"]}</label>'
        for s in SERVICES)
    contact = f'''
<section class="page-head"><div class="wrap">
  {crumbs([("contact.html", "Contact")])}
  <h1>Tell us what <em>you’re building.</em></h1>
  <p class="lede">No forms of the soul-destroying kind. A few questions so the first conversation is a useful one.</p>
</div></section>
<section class="section tight"><div class="wrap grid">
  <div class="span-7">
    <form class="form" data-inquiry data-endpoint="" novalidate>
      <div class="grid" style="grid-template-columns:1fr 1fr;gap:1.75rem">
        <div class="field" style="grid-column:span 1"><label for="f-name">Your name <span class="req">*</span></label><input id="f-name" name="name" autocomplete="name" required></div>
        <div class="field" style="grid-column:span 1"><label for="f-co">Company</label><input id="f-co" name="company" autocomplete="organization"></div>
        <div class="field" style="grid-column:span 1"><label for="f-email">Email <span class="req">*</span></label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
        <div class="field" style="grid-column:span 1"><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>
      </div>
      <fieldset class="field" style="border:0;padding:0;margin:0"><legend style="font-size:.78rem;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin-bottom:.8rem">What can we help with?</legend><div class="pills">{opts}</div></fieldset>
      <div class="field"><label for="f-budget">Approximate budget</label>
        <select id="f-budget" name="budget"><option value="">Prefer to discuss</option><option>{html.unescape("Under BDT [X]")}</option><option>BDT [X] – [Y]</option><option>Above BDT [Y]</option></select></div>
      <div class="field"><label for="f-msg">Tell us about the project <span class="req">*</span></label><textarea id="f-msg" name="message" required placeholder="What's happening in the business, and what needs to change?"></textarea></div>
      <div><button class="btn" type="submit">Send <span class="arr" aria-hidden="true">→</span></button></div>
      <p class="form-status" role="status" aria-live="polite"></p>
      <p class="dev-note">Integration required: connect the form to an inbox (e.g. Formspree, Basin, or Grandyra's own API) by setting <code>data-endpoint</code>. Replace budget bands [X]/[Y] with real figures or remove the field.</p>
    </form>
  </div>
  <aside class="span-4 start-9">
    <p class="eyebrow"><span class="num">Or</span> the old-fashioned way</p>
    <p style="font-family:var(--serif);font-size:1.5rem;line-height:1.3">{P("hello@grandyra.com")}<br>{P("+880 phone")}</p>
    <p class="mt-2 muted">Grandyra Limited<br>{P("Street address")}<br>Dhaka, Bangladesh</p>
    <div class="mt-2">{fig("map or photo of the studio entrance", "tone-paper", "ratio-sq")}</div>
    <p class="note mt-2">We reply to every message ourselves, usually within {P("response time")}.</p>
  </aside>
</div></section>
<style>@media(max-width:700px){{.form .grid{{grid-template-columns:1fr !important}}}}</style>
'''
    page("contact.html", "Contact Grandyra — Start a Branding Project in Dhaka",
         "Start a project with Grandyra, a branding and creative house in Dhaka, Bangladesh. Tell us what you're building and we'll reply personally.",
         contact, "contact.html", schema=[ORG, crumb_schema([("contact.html", "Contact")])])

    # ---------------- 404 ----------------
    nf = '''
<section class="hero"><div class="wrap">
  <p class="eyebrow"><span class="num">404</span> Page not found</p>
  <h1>This page took a <em>creative detour.</em></h1>
  <div class="hero-foot"><p class="lede">It may have moved when we rebuilt the site. Try the work, the services or the Journal — or just say hello.</p></div>
  <div class="related mt-3"><a class="chip" href="index.html">Home</a><a class="chip" href="work.html">Work</a><a class="chip" href="services.html">Services</a><a class="chip" href="journal.html">Journal</a><a class="chip" href="contact.html">Contact</a></div>
</div></section>'''
    page("404.html", "Page not found | Grandyra", "This page doesn't exist. Find your way back to Grandyra's work, services or Journal.", nf)
    # 404 must not be indexed
    p404 = os.path.join(OUT, "404.html")
    with open(p404, encoding="utf-8") as f:
        t = f.read().replace('content="index, follow, max-image-preview:large"', 'content="noindex"')
    with open(p404, "w", encoding="utf-8") as f:
        f.write(t)

    # ---------------- sitemap + robots ----------------
    urls = [p for p in PAGES if p != "404.html"]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in urls:
        loc = BASE + "/" + ("" if p == "index.html" else p.replace(".html", ""))
        pri = "1.0" if p == "index.html" else ("0.9" if p in [s["slug"] + ".html" for s in SERVICES] else "0.7")
        sm.append(f"  <url><loc>{loc}</loc><lastmod>2026-11-22</lastmod><priority>{pri}</priority></url>")
    sm.append("</urlset>")
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write("\n".join(sm) + "\n")
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
    print(f"Built {len(PAGES)} pages into {OUT}")


if __name__ == "__main__":
    build()
