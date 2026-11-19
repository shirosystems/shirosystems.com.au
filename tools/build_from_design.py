#!/usr/bin/env python3
"""Turn the Claude Design export (Main.dc.html) into the static index.html for GitHub Pages.

Usage: python3 tools/build_from_design.py <path/to/Main.dc.html>

Strips the design runtime, maps the theme tokens to CSS variables with light and dark
following the system setting, swaps Google Fonts for the self-hosted files in fonts/,
and fills in the head (SEO, Open Graph, favicons, Organization schema).
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = Path(sys.argv[1])
s = SRC.read_text(encoding="utf-8")

# Theme tokens from the design's renderVals()
LIGHT = dict(bg="#FFFFFF", surface="#F5F5F2", ink="#111111", muted="#5E616A", rule="#E6E6E2",
             accent="#B7282E", accentHover="#93202A", btnHover="#2B2B2B")
DARK = dict(bg="#16181D", surface="#1E2128", ink="#F5F5F2", muted="#A0A3AB", rule="#2C2F37",
            accent="#E5615B", accentHover="#F08A85", btnHover="#FFFFFF")
VAR = dict(bg="--bg", surface="--surface", ink="--ink", muted="--muted", rule="--rule",
           accent="--accent", accentHover="--accent-hover", btnHover="--btn-hover")

def tokens(t):
    return "".join(f"{VAR[k]}:{v};" for k, v in t.items())

# Body: everything inside <x-dc>, minus <helmet>
body = re.search(r"<x-dc>(.*)</x-dc>", s, re.S).group(1)
helmet_css = re.search(r"<helmet>.*?<style>(.*?)</style>.*?</helmet>", body, re.S).group(1)
body = re.sub(r"<helmet>.*?</helmet>", "", body, flags=re.S).strip()

# Root div: drop the {{t.*}} custom properties (now defined on :root)
body = re.sub(r"--[a-z-]+: \{\{t\.\w+\}\}; ", "", body)
assert "{{" not in body, "unresolved template hole"

# Content fixes
body = body.replace("[alex@shirosystems.com.au]", "alex@shirosystems.com.au")
body = re.sub(r"<span>\[PO Box[^]<]*\]</span>",
              "<span>Suite 246, 793 Burke Road, Camberwell VIC 3124</span>", body)
assert "[" not in re.sub(r"<[^>]+>", "", body), "placeholder left in copy"

# Each certification links to its Microsoft Learn credential page, which verifies it
CREDS = {
    "Azure DevOps Engineer Expert": "3C20A9052E043AB2",
    "Power Platform Solution Architect Expert": "3C4D5C6EC7FE4AC",
    "Dynamics 365 Business Central Developer Associate": "12F862A67BEF1910",
    "Azure Administrator Associate": "D4B9386BCE958AB9",
    "Azure Developer Associate": "C528CF04ECC7DDC8",
    "Power Platform Developer Associate": "BFB2EA4AED6D3F53",
}
LINK = ('<a href="https://learn.microsoft.com/api/credentials/share/en-us/alex-shirokikh/{id}'
        '?sharingId=7F5744789344AFC9" class="ul" style="color: var(--ink); text-decoration: underline; '
        'text-decoration-color: var(--accent); text-decoration-thickness: 1px; '
        'text-underline-offset: 3px">{name}</a>')
for name, cid in CREDS.items():
    li = f'border-bottom: 1px solid var(--rule)">{name}</li>'
    assert body.count(li) == 1, f"certification not found once: {name}"
    body = body.replace(li, f'border-bottom: 1px solid var(--rule)">{LINK.format(id=cid, name=name)}</li>')

FONT = "/fonts/"
css = f"""
@font-face{{font-family:'IBM Plex Sans';font-style:normal;font-weight:400;font-display:swap;src:url({FONT}ibm-plex-sans-latin-400-normal.woff2) format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}}
@font-face{{font-family:'IBM Plex Sans';font-style:normal;font-weight:400;font-display:swap;src:url({FONT}ibm-plex-sans-cyrillic-400-normal.woff2) format('woff2');unicode-range:U+0301,U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116}}
@font-face{{font-family:'IBM Plex Sans';font-style:normal;font-weight:600;font-display:swap;src:url({FONT}ibm-plex-sans-latin-600-normal.woff2) format('woff2')}}
@font-face{{font-family:'IBM Plex Mono';font-style:normal;font-weight:400;font-display:swap;src:url({FONT}ibm-plex-mono-latin-400-normal.woff2) format('woff2')}}
:root{{color-scheme:light dark;{tokens(LIGHT)}}}
@media (prefers-color-scheme: dark){{:root{{{tokens(DARK)}}}}}
body{{background:var(--bg)}}
{helmet_css.strip()}
""".strip()

TITLE = "Shiro Systems | Business Central and Azure architecture, Melbourne"
DESC = ("Business Central architecture, built hands-on. Alex Shirokikh designs Business Central "
        "solutions and builds them: architecture, AL code, pipelines and the Azure services underneath.")
URL = "https://shirosystems.com.au/"
SCHEMA = """{"@context":"https://schema.org","@type":"Organization","name":"Shiro Systems Pty Ltd","alternateName":"Shiro Systems","url":"https://shirosystems.com.au/","logo":"https://shirosystems.com.au/logo.png","email":"alex@shirosystems.com.au","sameAs":["https://www.linkedin.com/in/alexshirokikh"]}"""

html = f"""<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<link rel="canonical" href="{URL}">
<meta name="theme-color" content="#FFFFFF" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#16181D" media="(prefers-color-scheme: dark)">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Shiro Systems">
<meta property="og:title" content="Shiro Systems: Business Central architecture, built hands-on">
<meta property="og:description" content="{DESC}">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="{URL}og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="The Shiro Systems seal and name">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" href="{FONT}ibm-plex-sans-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{FONT}ibm-plex-sans-latin-600-normal.woff2" as="font" type="font/woff2" crossorigin>
<script type="application/ld+json">{SCHEMA}</script>
<style>
{css}
</style>
</head>
<body>
{body}
</body>
</html>
"""
(ROOT / "index.html").write_text(html, encoding="utf-8")
print(f"index.html written ({len(html.encode())} bytes)")
