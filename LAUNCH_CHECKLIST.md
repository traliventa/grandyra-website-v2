# Go-live checklist (search engines and sharing)

The review copy on GitHub Pages is built **with `PREVIEW=1`**, so every page says `noindex, nofollow` and `robots.txt` blocks crawling. Going live is one rebuild, not a series of edits. Nothing is removed from the code.

## The one switch

| Build | Command | Result |
|---|---|---|
| Review copy (now) | `PREVIEW=1 python3 build.py` | `noindex, nofollow` on every page, `robots.txt` = `Disallow: /`, canonicals point at `https://grandyra.com` |
| Live site | `python3 build.py` | `index, follow, max-image-preview:large`, `robots.txt` allows everything and lists the sitemap |
| Live site on another address (for example `www`) | `SITE_URL=https://www.grandyra.com python3 build.py` | Every canonical, Open Graph URL, sitemap entry and structured-data URL uses that address |

`SITE_URL` defaults to `https://grandyra.com`, so for the plain domain no variable is needed. Run `npm install` first so CSS and JS are minified with esbuild.

Windows PowerShell: `$env:PREVIEW='1'; python build.py` (remove it with `Remove-Item Env:PREVIEW`).

## Every place `noindex` comes from

| Where | Line | What |
|---|---|---|
| `build.py` | 267 | `robots = "noindex, nofollow" if PREVIEW else "index, follow, max-image-preview:large"` (the switch) |
| `build.py` | 802 | the 404 page always uses `robots="noindex"`. **Keep this at launch** |
| `build.py` | 815 | `robots.txt`: `Disallow: /` when `PREVIEW`, otherwise `Allow: /` plus the sitemap line |
| `site/*.html` (24 files) | 9 | `<meta name="robots" content="noindex, nofollow">` (built output, generated from the line above) |
| `site/robots.txt` | 2 | `Disallow: /` (built output) |

Do not edit the built files by hand. Rebuild instead.

## Every place the live address `grandyra.com` appears

| Where | Line | What | Changes with |
|---|---|---|---|
| `build.py` | 10 | `BASE = ... "https://grandyra.com"` | `SITE_URL` |
| `build.py` | 268, 277 | canonical URL, built from `BASE` | `SITE_URL` |
| `build.py` | 282 | `og:url` and `og:image` | `SITE_URL` |
| `build.py` | 283 | `twitter:image` and related tags | `SITE_URL` |
| `build.py` | 193-197 | organisation data: `@id`, `url`, `logo`, `sameAs` | `SITE_URL` |
| `build.py` | 806-814 | `sitemap.xml` (23 URLs) | `SITE_URL` |
| `build.py` | 815 | `Sitemap:` line in `robots.txt` (live build only) | `SITE_URL` |
| `build.py` | 41 | `EMAIL = "info@grandyra.com"` (contact address, not a URL) | stays |
| `site/*.html` | 8 | `<link rel="canonical">` | rebuild |
| `site/*.html` | 13 | `og:url`, `og:image` | rebuild |
| `site/*.html` | 14 | `twitter:image` | rebuild |
| `site/*.html` | in `<script type="application/ld+json">` | 16 mentions on the home page | rebuild |
| `site/sitemap.xml` | every `<loc>` | 23 URLs | rebuild |
| `src/deploy/.htaccess` | 14, 17 | commented `www` redirect for Apache | edit if you use Apache |

Canonicals use clean URLs (`/about`, not `/about.html`). The host must serve both, or redirect `.html` to the clean address (see `docs/DEPLOY.md`).

## What to do on launch day

1. Confirm the address: `grandyra.com` or `www.grandyra.com`. Use `SITE_URL` if it is `www`.
2. Build the live copy: `python3 build.py`. Check that `site/robots.txt` says `Allow: /` and that `site/index.html` no longer contains `noindex`.
3. Deploy `site/` to the production host (see `docs/DEPLOY.md`). The GitHub Pages workflow publishes whatever is committed in `site/`, so **do not commit the live build to the review repository** unless you want the review link indexed.
4. Make sure the old review address still says `noindex`, or take it down.
5. Check `https://<domain>/robots.txt`, `/sitemap.xml` and view-source on three pages for `index, follow` and a self-referencing canonical.
6. Open Graph and Twitter previews: test the home page, one service, one case study with the LinkedIn Post Inspector, the Facebook Sharing Debugger and a WhatsApp message. Each page has its own title and description. Case studies have their own 1200x630 image. Share images are cached, so test again after a change.
7. Submit `https://<domain>/sitemap.xml` in Google Search Console and Bing Webmaster Tools, then request indexing for the home page.
8. Re-run Lighthouse on the live address. SEO should reach 100 once `noindex` is gone.
