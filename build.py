#!/usr/bin/env python3
"""Build the A.S. Remodeling staging site.

Stack: plain static HTML + CSS, no framework, no database, no build
dependencies beyond Python 3. Edit the PAGES data below, run
    python3 build.py
and the deployable site appears in dist/.

Why this stack: Squarespace's visual editor is the blocker - Muse
could not reliably create pages, set SEO titles, or add a sticky
Call Now button there. Here every page is a file Muse can read,
edit, diff, and search directly. Deploy dist/ to any static host
(Netlify, Cloudflare Pages, GitHub Pages, Vercel static).
DO NOT point asremodelingllc.com at this build until Aleks approves
it. This is staging only.
"""
import json, os, pathlib

OUT = pathlib.Path(__file__).parent / "dist"
PHONE = "(602) 884-1904"
PHONE_TEL = "+16028841904"
EMAIL = "Ascremodel@gmail.com"
ROC = "AZ ROC 361142"
AREAS = "Phoenix, Cave Creek, Anthem, and Scottsdale, AZ"
PITCH = "Family-owned. One craftsman on every job. No crews, no shortcuts. Free estimates."

NAV = [
    ("Home", "index.html"),
    ("Services", "services.html"),
    ("Gallery", "gallery.html"),
    ("About", "about.html"),
    ("Contact", "contact.html"),
]

def header(active):
    links = "".join(
        f'<a href="{href}"{" class=\"active\"" if href == active else ""}>{label}</a>'
        for label, href in NAV
    )
    return f"""<header><div class="wrap bar">
<a class="brand" href="index.html">A.S. Remodeling</a>
<nav>{links}</nav>
<a class="call" href="tel:{PHONE_TEL}">Call {PHONE}</a>
</div></header>"""

FOOTER = f"""<footer><div class="wrap">
<p>A.S. Remodeling LLC. Licensed AZ tile specialty contractor, {ROC}. Serving {AREAS}.</p>
<p>Phone: <a href="tel:{PHONE_TEL}">{PHONE}</a> | Email: <a href="mailto:{EMAIL}">{EMAIL}</a> | Hours: Monday to Friday, 8am to 5pm</p>
<p><a href="contact.html">Get a Free Estimate</a></p>
</div></footer>"""

SCHEMA = json.dumps({
    "@context": "https://schema.org",
    "@type": "HomeAndGardenBusiness",
    "name": "A.S. Remodeling, LLC",
    "telephone": PHONE,
    "email": EMAIL,
    "url": "https://www.asremodelingllc.com",
    "areaServed": ["Phoenix, AZ", "Cave Creek, AZ", "Anthem, AZ", "Scottsdale, AZ"],
    "openingHours": "Mo-Fr 08:00-17:00",
}, indent=2)

def page(slug, title, desc, body, active):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="style.css">
<script type="application/ld+json">{SCHEMA}</script>
</head>
<body>
{header(active)}
<main class="wrap">
{body}
<section class="cta">
<h2>Get a Free Estimate</h2>
<p>{PITCH}</p>
<p><a class="btn" href="contact.html">Get a Free Estimate</a> <a class="btn secondary" href="tel:{PHONE_TEL}">Call {PHONE}</a></p>
</section>
</main>
{FOOTER}
</body>
</html>
"""

def photo(caption):
    return f'<div class="photo" role="img" aria-label="Photo placeholder">{caption}<br><small>Replace with an approved finished-job photo before going live.</small></div>'

def service_body(intro, items):
    lis = "".join(f"<li>{i}</li>" for i in items)
    return f"<p>{intro}</p><h2>What is included</h2><ul>{lis}</ul><p>{PITCH}</p>"

PAGES = {
 "index.html": (
  "Tile Installation & Remodeling | Phoenix, AZ | A.S. Remodeling",
  "High-end tile installation in Phoenix, AZ. Family-owned, one craftsman on every job. Free estimates.",
  f"""<section class="hero"><h1>High-End Tile Installation in Phoenix, AZ</h1>
<p>{PITCH}</p>
<p><a class="btn" href="contact.html">Get a Free Estimate</a> <a class="btn secondary" href="tel:{PHONE_TEL}">Call {PHONE}</a></p></section>
{photo("Hero photo: finished tile work")}
<h2>We specialize in:</h2>
<ul><li>Tile installation</li><li>Full Bathroom Remodels</li><li>Kitchen Remodels</li></ul>
<p><a href="services.html">See all services</a> in {AREAS}.</p>""",
  "index.html"),
 "services.html": (
  "Our Services | Tile, Bathroom & Kitchen Remodeling in Phoenix, AZ | A.S. Remodeling",
  "Shower tile, kitchen tile and backsplash, bathroom remodeling, and tile flooring in Phoenix, Cave Creek, Anthem, and Scottsdale.",
  """<h1>Our Services</h1><ul>
<li><a href="shower-tile-installation.html">Shower Tile Installation</a></li>
<li><a href="kitchen-tile-backsplash.html">Kitchen Tile &amp; Backsplash</a></li>
<li><a href="bathroom-tile-remodeling.html">Bathroom Tile &amp; Remodeling</a></li>
<li><a href="tile-flooring.html">Tile Flooring Installation</a></li>
</ul>""",
  "services.html"),
 "shower-tile-installation.html": (
  "Shower Tile Installation in Phoenix, AZ | A.S. Remodeling",
  "Full shower tile installation in Phoenix, AZ: waterproofing, wall tile, floor tile, niches, and finishes ready for glass.",
  "<h1>Shower Tile Installation in Phoenix, AZ</h1>" + photo("Photo: finished shower tile") + service_body(
   "A shower gets used every day, so the tile work has to be right the first time. I handle full shower tile installation from the pan up: waterproofing, wall tile, floor tile, niches, and finishes ready for glass.",
   ["Full shower remodels and retiles", "Walk-in showers, tub surrounds, and shower pans", "Waterproofing done to spec, the part that keeps a shower from leaking into your walls", "Wall and floor tile, niches, benches, and trim", "Glass enclosure ready finishes"]),
  "services.html"),
 "kitchen-tile-backsplash.html": (
  "Kitchen Tile & Backsplash Installation in Phoenix, AZ | A.S. Remodeling",
  "Kitchen backsplash and floor tile in Phoenix, AZ, with tight lines and clean edges matched to your cabinets and counters.",
  "<h1>Kitchen Tile &amp; Backsplash Installation in Phoenix, AZ</h1>" + photo("Photo: finished kitchen backsplash") + service_body(
   "The backsplash is the part of the kitchen everyone looks at. I install backsplash tile with tight lines and clean edges, matched to your cabinets and counters. Kitchen floors too, from a single room to the whole downstairs.",
   ["Kitchen backsplash tile: subway, mosaic, stone, and large format", "Kitchen floor tile", "Clean cuts around outlets, cabinets, and windows", "Grout color matched to the tile", "Caulked edges where the tile meets the counter"]),
  "services.html"),
 "bathroom-tile-remodeling.html": (
  "Bathroom Tile & Remodeling in Phoenix, AZ | A.S. Remodeling",
  "Full bathroom remodels in Phoenix, AZ with tile as the centerpiece: floors, walls, showers, and tub surrounds.",
  "<h1>Bathroom Tile &amp; Remodeling in Phoenix, AZ</h1>" + photo("Photo: finished bathroom tile") + service_body(
   "Full bathroom remodels with tile as the centerpiece. Floors, walls, showers, and tub surrounds, handled start to finish by one craftsman who has done hundreds of bathrooms.",
   ["Full bathroom remodels", "Bathroom floor and wall tile", "Shower and tub surround tile", "Shower pans, niches, benches, and trim", "Old tile removal and surface prep"]),
  "services.html"),
 "tile-flooring.html": (
  "Tile Flooring Installation in Phoenix, AZ | A.S. Remodeling",
  "Tile flooring installation in Phoenix, AZ: ceramic, porcelain, and stone tile floors that sit flat and hold up for decades.",
  "<h1>Tile Flooring Installation in Phoenix, AZ</h1>" + photo("Photo: finished tile floor") + service_body(
   "Tile floors that sit flat, look straight, and hold up for decades. I install ceramic, porcelain, and stone tile floors across the Phoenix area, with the subfloor prep that keeps tiles from cracking later.",
   ["Ceramic, porcelain, and stone tile floors", "Kitchens, bathrooms, entryways, and whole-home tile", "Subfloor prep and leveling", "Straight grout lines, sealed where it counts", "Transitions finished clean where tile meets other floors"]),
  "services.html"),
 "gallery.html": (
  "Project Gallery | Tile Work in Phoenix, AZ | A.S. Remodeling",
  "Finished tile work by A.S. Remodeling in Phoenix, Cave Creek, Anthem, and Scottsdale.",
  "<h1>Project Gallery</h1><p>Photos below are placeholders. Replace each one with an approved finished-job photo before going live.</p>"
  + photo("Photo: bathroom tile") + photo("Photo: shower tile") + photo("Photo: kitchen backsplash") + photo("Photo: tile flooring"),
  "gallery.html"),
 "about.html": (
  "About A.S. Remodeling | Tile Installer in Phoenix, AZ",
  "A.S. Remodeling is a family-owned tile installer serving Phoenix, Cave Creek, Anthem, and Scottsdale, AZ.",
  f"""<h1>About A.S. Remodeling</h1><p>{PITCH}</p>
<p>A.S. Remodeling LLC is a licensed AZ tile specialty contractor, {ROC}, serving {AREAS}.</p>
<p>Copy on this staging page is carried over from the current site and the drafted service pages. Aleks must confirm the history and project claims before this page goes live.</p>""",
  "about.html"),
 "contact.html": (
  "Contact for a Free Estimate | A.S. Remodeling, Phoenix AZ",
  "Contact A.S. Remodeling for a free tile estimate in Phoenix, Cave Creek, Anthem, or Scottsdale.",
  f"""<h1>Contact for a Free Estimate</h1>
<p>Call <a href="tel:{PHONE_TEL}">{PHONE}</a> or email <a href="mailto:{EMAIL}">{EMAIL}</a>. Hours: Monday to Friday, 8am to 5pm.</p>
<form id="estimate-form">
<label>First Name <input name="first_name" required></label>
<label>Phone (required) <input name="phone" type="tel" required></label>
<label>Email <input name="email" type="email"></label>
<label>Project Type <select name="project_type"><option>Shower tile</option><option>Kitchen tile and backsplash</option><option>Bathroom tile and remodeling</option><option>Tile flooring</option><option>Other</option></select></label>
<label>Project Details <textarea name="details" rows="5"></textarea></label>
<button type="submit">Send Estimate Request</button>
<p id="form-note"></p>
</form>
<script>
document.getElementById('estimate-form').addEventListener('submit', function(e) {{
  e.preventDefault();
  document.getElementById('form-note').textContent = 'Staging form: no form endpoint is connected yet. In the live version this will send to Aleks, and you will see: Thanks! We will call you within one business day.';
}});
</script>
<p><small>Staging note: do not publish this form until a form endpoint (for example a free form service or email handler) is chosen and approved. No submission is sent from this staging build.</small></p>""",
  "contact.html"),
}

CSS = """body{font-family:system-ui,Arial,sans-serif;margin:0;color:#222;line-height:1.6}
.wrap{max-width:820px;margin:0 auto;padding:0 20px}
header{border-bottom:1px solid #ddd;position:sticky;top:0;background:#fff}
.bar{display:flex;gap:16px;align-items:center;flex-wrap:wrap;padding:12px 20px}
.brand{font-weight:700;text-decoration:none;color:#111;font-size:20px}
nav a{margin-right:12px;text-decoration:none;color:#333}
nav a.active{font-weight:700}
.call{margin-left:auto;background:#111;color:#fff;padding:8px 14px;border-radius:6px;text-decoration:none}
.hero{padding:48px 0 24px}
.btn{display:inline-block;background:#111;color:#fff;padding:10px 18px;border-radius:6px;text-decoration:none;margin-right:10px}
.btn.secondary{background:#fff;color:#111;border:1px solid #111}
.cta{border-top:1px solid #ddd;margin-top:40px;padding:24px 0}
.photo{background:#eee;border:1px dashed #999;padding:48px 20px;text-align:center;margin:20px 0}
form label{display:block;margin:12px 0}
form input,form select,form textarea{width:100%;padding:10px;margin-top:4px;box-sizing:border-box}
form button{background:#111;color:#fff;padding:12px 20px;border:0;border-radius:6px}
footer{border-top:1px solid #ddd;padding:24px 0;color:#555}
"""

def main():
    OUT.mkdir(exist_ok=True)
    for slug, (title, desc, body, active) in PAGES.items():
        (OUT / slug).write_text(page(slug, title, desc, body, active), encoding="utf-8")
    (OUT / "style.css").write_text(CSS, encoding="utf-8")
    urls = "".join(f"<url><loc>https://www.asremodelingllc.com/{s if s != 'index.html' else ''}</loc></url>\n" for s in PAGES)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n', encoding="utf-8")
    (OUT / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: https://www.asremodelingllc.com/sitemap.xml\n", encoding="utf-8")
    print(f"Built {len(PAGES)} pages in {OUT}")

if __name__ == "__main__":
    main()
