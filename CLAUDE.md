# Grandyra website — "Noise → Greatness"

Static multi-page site for Grandyra Limited (branding and creative house, Dhaka). Goal: Awwwards-level quality, strong SEO for "branding agency Bangladesh / Dhaka".

## Layout
- `site/` — the built, deployable website (plain HTML/CSS/JS). This is what gets hosted.
- `src/site.css`, `src/main.js` — source styles and scripts (copied and minified into `site/assets/` on build).
- `build.py` — generates every page in `site/` (content, SEO tags, JSON-LD, sitemap, robots).
- `tools/legacy_data.py` — services, work and journal data that `build.py` imports.
- `tools/journal-src/` — journal article bodies.
- `tools/art/` — canvas artwork (`art.html`) and `render.py` (Playwright) that renders the concept art in `site/assets/img/`.
- `tools/shoot.py` — Playwright screenshot checker (edit the port inside).

## Commands
- Install: `npm install` (fonts, GSAP, Lenis, lucide icons, esbuild) and `pip install playwright pillow` for tools.
- Build: `python3 build.py` (live, indexable) or `python3 build.py --preview` (review copy: noindex). Needs `npx esbuild` from node_modules for minifying. Other flags: `--site-url`, `--hold-unverified`, `--out`. See `LAUNCH_CHECKLIST.md`.
- Preview: `cd site && python3 -m http.server 8000`.

## Brand and content sources
- Logo: `src/brand/grandyra-mark.svg` and `grandyra-logo.svg` (from the official logo files), inlined by `logo()` in `build.py`. Favicon is `site/assets/favicon.svg`.
- Official details: email info@grandyra.com, address House 7, Road 4, Gulshan-1, Dhaka (constants `EMAIL`, `ADDRESS` in `build.py`). No phone number is published on the site.
- Real project facts (Souk Taban, Seheri Nights, The Audio Expo, First Momentum, Real Estate Futsal 2026) and the "Grand + Era / Y = Why" story come from the Grandyra profile, brand guideline and master presentation in `D:\GRANDYRA`. Real Futsal artwork is in `site/assets/img/futsal-*.webp`.
- The site is English only. Contact form opens the visitor's email app (mailto); set `data-endpoint` on the form if an inbox service is added.
- Without Node, build with a wrapper that stubs `subprocess.run` (skips esbuild minify). Lucide icons must exist in `node_modules/lucide-static/icons/`.

## Rules
- Edit `build.py` / `src/` and rebuild; don't hand-edit `site/*.html` (it is regenerated).
- Never invent client projects, awards, stats, testimonials or company history.
- Concept art is labelled "Concept art — replace with project imagery"; swap in real project photos when available.
- Keep canonical URLs on https://grandyra.com/<slug>, and keep sitemap.xml in sync.
