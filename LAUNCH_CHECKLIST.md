# Go-live checklist (search engines and sharing)

The review copy on GitHub Pages is built **with `--preview`**, so every page says `noindex, nofollow` and `robots.txt` blocks crawling. Going live is one rebuild, not a series of edits. Nothing is removed from the code.

## The one switch

| Build | Command | Result |
|---|---|---|
| Review / staging copy (now) | `python3 build.py --preview` (or `npm run build:preview`) | `noindex, nofollow` on every page, `robots.txt` = `Disallow: /`, canonicals point at `https://grandyra.com` |
| Live site | `python3 build.py` (or `npm run build`) | `index, follow, max-image-preview:large`, `robots.txt` allows everything and lists the sitemap |
| Live site on another address (for example `www`) | `python3 build.py --site-url https://www.grandyra.com` | Every canonical, Open Graph URL, sitemap entry and structured-data URL uses that address |
| Try a build without touching `site/` | `python3 build.py --out ../site-live-test` | Writes a full copy (static assets copied across) to another folder |

The environment variables `PREVIEW=1`, `SITE_URL=...` and `HOLD_UNVERIFIED=1` still work. `--hold-unverified` leaves out the four services that are not confirmed yet. Run `npm install` first so CSS and JS are minified with esbuild.

Both configurations were audited automatically: 24 pages, one h1 each, titles of 60 characters or fewer, unique titles and descriptions, a self-referencing canonical, complete Open Graph and Twitter tags with a 1200x630 image that exists, valid structured data (organisation, breadcrumbs, services, FAQ, articles), 23 sitemap URLs that match the canonicals, and the expected `robots` meta on every page.

## Every place `noindex` comes from

| Where | Line | What |
|---|---|---|
| `build.py` | 281 | `robots = "noindex, nofollow" if PREVIEW else "index, follow, max-image-preview:large"` (the switch) |
| `build.py` | 24 | `PREVIEW = _args.preview or os.environ.get("PREVIEW") == "1"` |
| `build.py` | 819 | the 404 page always uses `robots="noindex"`. **Keep this at launch** |
| `build.py` | 832 | `robots.txt`: `Disallow: /` when previewing, otherwise `Allow: /` plus the sitemap line |
| `site/*.html` (24 files) | 9 | `<meta name="robots" content="noindex, nofollow">` (built output, generated from line 281) |
| `site/robots.txt` | 2 | `Disallow: /` (built output) |

Do not edit the built files by hand. Rebuild instead.

## Every place the live address `grandyra.com` appears

| Where | Line | What | Changes with |
|---|---|---|---|
| `build.py` | 23 | `BASE = ... "https://grandyra.com"` (the default) | `--site-url` |
| `build.py` | 282, 291 | canonical URL, built from `BASE` | `--site-url` |
| `build.py` | 296-297 | `og:url`, `og:image`, `twitter:image` | `--site-url` |
| `build.py` | 207-211 | organisation data: `@id`, `url`, `logo` (PNG), `sameAs` | `--site-url` |
| `build.py` | 823-831 | `sitemap.xml` (23 URLs) | `--site-url` |
| `build.py` | 832 | `Sitemap:` line in `robots.txt` (live build only) | `--site-url` |
| `build.py` | 55 | `EMAIL = "info@grandyra.com"` (contact address, not a URL) | stays |
| `site/*.html` | 8 | `<link rel="canonical">` | rebuild |
| `site/*.html` | 13-14 | `og:url`, `og:image`, `twitter:image` | rebuild |
| `site/*.html` | inside `<script type="application/ld+json">` | structured data URLs | rebuild |
| `site/sitemap.xml` | every `<loc>` | 23 URLs | rebuild |
| `src/deploy/.htaccess` | 14, 17 | commented `www` redirect for Apache | edit if you use Apache |

Canonicals use clean URLs (`/about`, not `/about.html`). The host must serve both, or redirect `.html` to the clean address (see `docs/DEPLOY.md`).

## What to do on launch day

1. Confirm the address: `grandyra.com` or `www.grandyra.com`. Use `--site-url` if it is `www`.
2. Build the live copy: `python3 build.py`. Check that `site/robots.txt` says `Allow: /` and that `site/index.html` no longer contains `noindex`.
3. Deploy `site/` to the production host (see `docs/DEPLOY.md`). The GitHub Pages workflow publishes whatever is committed in `site/`, so **do not commit the live build to the review repository** unless you want the review link indexed.
4. Make sure the old review address still says `noindex`, or take it down.
5. Check `https://<domain>/robots.txt`, `/sitemap.xml` and view-source on three pages for `index, follow` and a self-referencing canonical.
6. Open Graph and Twitter previews: test the home page, one service, one case study with the LinkedIn Post Inspector, the Facebook Sharing Debugger and a WhatsApp message. Share images are cached, so test again after a change.
7. Submit `https://<domain>/sitemap.xml` in Google Search Console and Bing Webmaster Tools, then request indexing for the home page.
8. Re-run Lighthouse on the live address. SEO should reach 100 once `noindex` is gone.

## Known gaps in structured data
The journal articles have a headline, image and publisher, but **no author or publication date**, because none has been provided. Add `author` and `datePublished` to the article schema when you have them. They are not invented.
