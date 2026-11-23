# Testing guide

Run these on the staging address before launch. Nothing here needs special software beyond a browser and a phone.

## Automated checks (needs a computer with Node and Chrome)
```
npm install
python3 build.py
npm run serve               # http://localhost:8000
npm run lighthouse          # opens a report
```
Targets: Performance, Accessibility, Best Practices and SEO all 90 or higher on mobile. Test the home page, a service page, a case study and the contact page. Free alternatives: PageSpeed Insights on the live staging URL, and the axe DevTools browser extension.

## Accessibility (about 20 minutes)
- [ ] **Keyboard only**: press Tab from the top. Every link and button gets a visible outline, in a sensible order. Enter opens the menu, Escape closes it and focus returns to the Menu button
- [ ] **Skip link**: the first Tab stop is "Skip to content"
- [ ] **Screen reader** (VoiceOver on Mac/iPhone, NVDA on Windows, TalkBack on Android): the headings read in order, images read their descriptions, the form fields announce their labels and errors
- [ ] **Reduced motion**: turn on "Reduce motion" in the operating system. The preloader, particle hero, page transitions and parallax stop, and all text stays visible
- [ ] **Zoom**: 200% and text-only enlargement. Nothing is cut off or overlaps
- [ ] **JavaScript off**: all text and links remain readable

## Mobile devices
Test on a real iPhone (Safari) and a mid-range Android phone (Chrome). A hosted device lab such as BrowserStack works if you do not have both.
- [ ] Home hero loads and the noise forms the word GRANDYRA while scrolling. It should stay smooth
- [ ] Menu opens and closes. Contact details and social links are tappable
- [ ] Work cards stack. Case-study photos do not overflow
- [ ] Contact form: wrong entries show a clear message under the field. A valid entry opens the email app
- [ ] No sideways scrolling on any page
- [ ] Landscape and small phones (iPhone SE size, 375 px wide)

## Browsers
Latest Chrome, Safari, Firefox, Edge. Check the loading screen, page transitions and the horizontal "Recent work" scroll on the home page.

## Security and performance
- [ ] Response headers show the policy from `_headers` (check with securityheaders.com or the browser's Network tab)
- [ ] HTTPS everywhere. Both `http://` and the other host variant redirect with a 301
- [ ] `/assets/` files return cache headers
- [ ] A missing address shows the 404 page
- [ ] After connecting the form service, a real submission arrives in the info@grandyra.com inbox, not in spam

## What was checked already (local, desktop browser)
Heading order and a single h1 on every page; alt text on every image; no empty links; no duplicate ids; all internal links and assets exist; no console errors on the pages loaded; no sideways scroll at 375 px on 15 pages; colour contrast of the main text pairs (calculated, see `src/site.css`, section "contrast fixes").
Not checked: a real Lighthouse run, screen readers, real phones.
