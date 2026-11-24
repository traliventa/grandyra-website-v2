# Lighthouse comparison

Lighthouse 13.6.0, Chrome 158, headless, default simulated throttling (mobile: slow 4G and 4x CPU slowdown; desktop preset). Same machine and a local server with gzip and a 10-minute cache (like GitHub Pages), run one after the other. **Before** = commit `4158825` (previous polish pass). **After** = this branch. Scores are performance / accessibility / best practices / SEO.

Mobile and desktop numbers vary by 1-3 points between runs. Where three runs were made, the median is shown.


## Mobile

| Page | Device | Before | After | FCP | LCP | TBT | CLS |
|---|---|---|---|---|---|---|---|
| Home | mobile | 93 / 96 / 100 / 69 | **94** / **100** / 100 / 69 | 1.4 s | 2.9 s | 110 ms | 0.002 |
| Services hub | mobile | 99 / 96 / 100 / 66 | **100** / **96** / 100 / 66 | 0.9 s | 0.9 s | 0 ms | 0.002 |
| Service page | mobile | 95 / 100 / 100 / 69 | **100** / **100** / 100 / 69 | 0.9 s | 0.9 s | 0 ms | 0.002 |
| Work index | mobile | 100 / 100 / 100 / 69 | **100** / **100** / 100 / 69 | 1.4 s | 1.4 s | 24 ms | 0.001 |
| Case study | mobile | 95 / 100 / 100 / 69 | **96** / **100** / 100 / 69 | 0.9 s | 2.7 s | 66 ms | 0.002 |
| Journal index | mobile | 95 / 100 / 100 / 69 | **97** / **100** / 100 / 69 | 0.9 s | 2.6 s | 0 ms | 0.001 |
| Journal article | mobile | 99 / 100 / 100 / 69 | **100** / **100** / 100 / 69 | 0.9 s | 0.9 s | 0 ms | 0.002 |
| About | mobile | 100 / 100 / 100 / 69 | **100** / **100** / 100 / 69 | 0.9 s | 0.9 s | 32 ms | 0.001 |
| Contact | mobile | 100 / 100 / 100 / 66 | **100** / **100** / 100 / 66 | 1.4 s | 1.4 s | 39 ms | 0.002 |

## Desktop

| Page | Device | Before | After | FCP | LCP | TBT | CLS |
|---|---|---|---|---|---|---|---|
| Home | desktop | 99 / 96 / 100 / 69 | **100** / **100** / 100 / 69 | 0.4 s | 0.4 s | 12 ms | 0.006 |
| Services hub | desktop | 100 / 96 / 100 / 66 | **100** / **96** / 100 / 66 | 0.3 s | 0.3 s | 0 ms | 0.010 |
| Service page | desktop | 99 / 100 / 100 / 69 | **99** / **100** / 100 / 69 | 0.4 s | 0.4 s | 0 ms | 0.010 |
| Work index | desktop | 100 / 100 / 100 / 69 | **100** / **100** / 100 / 69 | 0.4 s | 0.4 s | 0 ms | 0.013 |
| Case study | desktop | 100 / 100 / 100 / 69 | **100** / **100** / 100 / 69 | 0.4 s | 0.4 s | 0 ms | 0.013 |
| Journal index | desktop | 100 / 100 / 100 / 69 | **100** / **100** / 100 / 69 | 0.4 s | 0.4 s | 0 ms | 0.012 |
| Journal article | desktop | 99 / 100 / 100 / 69 | **99** / **100** / 100 / 69 | 0.4 s | 0.4 s | 0 ms | 0.013 |
| About | desktop | 100 / 100 / 100 / 69 | **100** / **100** / 100 / 69 | 0.4 s | 0.4 s | 0 ms | 0.012 |
| Contact | desktop | 100 / 100 / 100 / 66 | **100** / **100** / 100 / 66 | 0.4 s | 0.4 s | 0 ms | 0.010 |

Three-run pages: home (mobile) before 93/93/93, after 94/94/95; case study (mobile) after 96/96/96; service page (mobile) after 100/99/100.

## Remaining warnings

- **SEO 69 (66 on the contact page and services hub):** the only failing audit is `is-crawlable`, the intentional `noindex` on the review copy. It clears with a live build (`python3 build.py`).
- **Services hub accessibility 96:** the header uses `mix-blend-mode: difference`, which the audit cannot evaluate; it assumes white text on the pale background (1.2:1). The rendered text is `#111620` on `#EEE9DF`, measured at 15:1. Left as is, because changing it would change the design.
- **Case study and journal index, mobile, LCP about 2.6-2.7 s:** the largest element is the intro paragraph (case study) or the first issue cover (journal index). Both fade in as part of the page entrance animation, so the simulated LCP waits for the scripts. Making the cover load eagerly was tried and changed nothing, so it was reverted. Left as is (animation timing).
- **Home, mobile, LCP 2.9 s:** the hero heading is split into words and revealed by the entrance animation, so the simulated LCP waits for the scripts. Real (unthrottled) Chrome measures 0.37 s. Left as is (animation).
- **Cache lifetimes, render-blocking CSS, forced reflow, network chain:** the cache result reflects the 10-minute test server; the supplied `_headers` / `.htaccess` set long cache lifetimes on a real host. The stylesheet (8.7 KB compressed) has to block rendering. Forced reflow comes from GSAP/ScrollTrigger internals.
- **Image delivery (about 28 KiB, 5 pages):** two work-card images are slightly larger than needed. Not changed.
