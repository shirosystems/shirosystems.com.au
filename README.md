# shirosystems.com.au

The Shiro Systems website. One static page, no framework, no analytics, no cookies, no form.
Hosted on GitHub Pages with the custom domain in `CNAME`.

## Update the page

The design lives in Claude Design ("Shiro Systems website"). After changing it:

1. Save the design's `project/Main.dc.html` over `design/Main.dc.html`.
2. Run `python3 tools/build_from_design.py design/Main.dc.html` to regenerate `index.html`.
3. Commit and push. Pages deploys from `main`.

The build strips the design runtime, maps the theme to CSS variables (light and dark follow the
system setting), uses the self-hosted IBM Plex fonts in `fonts/` (SIL OFL, see `fonts/OFL.txt`)
and fills in the SEO, Open Graph and Organization schema.

`og.png` (the link preview) is rendered from `tools/og.html` with headless Chrome.
