# Deploying the Grandyra website

The site is static. `site/` is the finished website. Everything below prepares it for production. Nothing here needs an account until you choose a host.

## 1. Build

```
npm install            # fonts, GSAP, Lenis, lucide icons, esbuild
python3 build.py       # production build into site/
```

Options (command-line flags; the matching environment variables still work):
| Flag | Effect |
|---|---|
| `--site-url https://staging.example.com` | Changes every canonical, Open Graph URL and sitemap entry (default `https://grandyra.com`) |
| `--preview` | Marks the copy `noindex, nofollow` and writes `robots.txt` as `Disallow: /`. Use for review links (`npm run build:preview`) |
| `--hold-unverified` | Leaves out the four service pages that are not yet confirmed |
| `--out DIR` | Writes the site to another folder instead of `site/` |

Without Node, the build still runs but CSS and JS are not minified (a warning is printed). Always build with `npm install` first for production.

## 2. Host

Any static host works. `site/` contains host files that the build copies in from `src/deploy/`:
- `_headers`: security and cache headers for **Netlify** and **Cloudflare Pages**
- `.htaccess`: the same for **Apache / cPanel** (clean URLs, HTTPS, www redirect). Untested on your host, so try it on a staging address first
- GitHub Pages ignores both files. Use it for review links only

## 3. Domain

1. Choose one address, `grandyra.com` or `www.grandyra.com`, and redirect the other to it (301). The canonical tags use `https://grandyra.com`. If you choose `www`, build with `python3 build.py --site-url https://www.grandyra.com`.
2. Add the domain in your host's dashboard and create the DNS records it shows. Those values are specific to the host, so they are not listed here.
3. Turn on HTTPS and "force HTTPS". The `.htaccess` and `_headers` files send an HSTS header, so only do this once HTTPS works.
4. Pages are linked as `about.html`, while canonicals use `/about`. Netlify and Cloudflare Pages serve both. On Apache the `.htaccess` rewrite does it. Check that `/about` and `/about.html` both load.

## 4. Contact form

Today the form opens the visitor's email app with the message ready (button: "Write in your email app"). It does not send from the page.

To make it a real online form:
1. Pick a form service. Recommended: **Formspree** or **Basin** for the quickest start, or a small serverless function (Cloudflare Pages Function, Netlify Function) with Cloudflare Turnstile and Resend or Postmark if you want full control.
2. Create a form that delivers to info@grandyra.com and copy its endpoint URL.
3. In `build.py` set `FORM_ENDPOINT = "<that URL>"` and rebuild. The button becomes "Send message", and the form posts the data. A hidden honeypot field is already included.
4. Add the service's domain to `connect-src` and `form-action` in `src/deploy/_headers` (and `.htaccess`), otherwise the security policy will block it.
5. Set up SPF, DKIM and DMARC for grandyra.com so the notification emails are not filtered.
6. Add a one-line privacy note under the button and test a real submission end to end.

## 5. Search and sharing
- Submit `https://<domain>/sitemap.xml` in Google Search Console and Bing Webmaster Tools. The sitemap date is the build date.
- Share previews: every page has Open Graph and Twitter tags. Case studies have their own 1200x630 image. Check them with the LinkedIn Post Inspector and the Facebook Sharing Debugger after launch (they cache).
- Organization data (name, address, email, social profiles) is in the page source. Check it with Google's Rich Results Test.

## 6. Before you go live
See `docs/TESTING.md` and resolve `docs/CONTENT-VERIFICATION.md`.
