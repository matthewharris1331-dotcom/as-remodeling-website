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
import json, os, pathlib, shutil

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
<a class="brand" href="index.html"><img class="logo" src="as-remodeling-logo-horizontal.svg" alt="A.S. Remodeling LLC" width="189" height="46"></a>
<nav>{links}</nav>
<a class="call" href="tel:{PHONE_TEL}">Call {PHONE}</a>
</div></header>"""

FOOTER = f"""<footer><div class="wrap footgrid">
<div>
<p class="footbrand">A.S. Remodeling LLC</p>
<p>Licensed, bonded and insured AZ tile specialty contractor, {ROC}. Serving {AREAS}.</p>
<p>Hours: Monday to Friday, 8am to 5pm</p>
</div>
<div>
<p class="foothead">Services</p>
<p><a href="shower-tile-installation.html">Shower tile</a><br><a href="kitchen-tile-backsplash.html">Kitchen tile and backsplash</a><br><a href="bathroom-tile-remodeling.html">Bathroom remodeling</a><br><a href="tile-flooring.html">Tile flooring</a></p>
</div>
<div>
<p class="foothead">Get started</p>
<p>Phone: <a href="tel:{PHONE_TEL}">{PHONE}</a><br>Email: <a href="mailto:{EMAIL}">{EMAIL}</a><br><a href="contact.html">Get a Free Estimate</a></p>
</div>
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

def page(slug, title, desc, body, active, extra_schema=None):
    extra = f'<script type="application/ld+json">{extra_schema}</script>' if extra_schema else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="style.css">
<link rel="icon" type="image/svg+xml" href="as-remodeling-logo.svg">
<script type="application/ld+json">{SCHEMA}</script>
{extra}
</head>
<body>
{header(active)}
<main>
{body}
<section class="cta"><div class="wrap cta-inner">
<div>
<h2>Get a Free Estimate</h2>
<p>{PITCH}</p>
</div>
<p class="cta-btns"><a class="btn" href="contact.html">Get a Free Estimate</a> <a class="btn secondary" href="tel:{PHONE_TEL}">Call {PHONE}</a></p>
</div></section>
</main>
{FOOTER}
</body>
</html>
"""

def photo(caption):
    return f'<div class="photo" role="img" aria-label="Photo placeholder"><span class="photo-tile"></span><span class="photo-label">{caption}<small>Replace with an approved finished-job photo before going live.</small></span></div>'

def service_body(intro, items):
    lis = "".join(f"<li>{i}</li>" for i in items)
    return f"<p class=\"lede\">{intro}</p><h2>What is included</h2><ul class=\"checklist\">{lis}</ul><p>{PITCH}</p>"


def faq_schema(faqs):
    import json as _json
    return _json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faqs
        ],
    })

def city_body(city, intro, sections, faqs, others):
    secs = "".join(f"<h2>{h}</h2><p>{t}</p>" for h, t in sections)
    faq_html = "".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in faqs)
    other_links = " ".join(f'<a href="{href}">{label}</a>' for label, href in others)
    return (
        f'<main class="wrap page-head"><h1>Tile Installation in {city}, AZ</h1>'
        f'<p class="lede">{intro}</p>'
        + photo(f"Photo: finished tile work in {city}")
        + secs
        + '<h2>What we review before tile work in ' + city + '</h2>'
        + '<ul class="checklist"><li>The room, the material, and what you want changed</li>'
        + '<li>The existing surface, and the waterproofing and prep it needs</li>'
        + '<li>Layout, grout lines, and transitions to adjoining floors</li>'
        + '<li>Scheduling, access, and how the work fits around your home</li></ul>'
        + '<h2>Questions about tile work in ' + city + '</h2>' + faq_html
        + '<p>Also serving: ' + other_links + '. See all <a href="service-areas.html">service areas</a>.</p>'
        + ('<p>Tile work in ' + city + ': <a href="shower-tile-' + city.lower().replace(' ', '-') + '-az.html">Shower tile</a>, <a href="bathroom-tile-' + city.lower().replace(' ', '-') + '-az.html">Bathroom tile</a>, <a href="kitchen-backsplash-' + city.lower().replace(' ', '-') + '-az.html">Kitchen backsplash</a>.</p>' if city in ('Scottsdale', 'Phoenix') else '')
        + '<p>Call <a href="tel:+16028841904">(602) 884-1904</a> to talk through your project and set up a free estimate.</p></main>'
    )


def service_city_body(service, city, intro, sections, faqs, city_href, service_href):
    secs = "".join(f"<h2>{h}</h2><p>{t}</p>" for h, t in sections)
    faq_html = "".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in faqs)
    return (
        f'<main class="wrap page-head"><h1>{service} in {city}, AZ</h1>'
        f'<p class="lede">{intro}</p>'
        + photo(f"Photo: finished {service.lower()} in {city}")
        + secs
        + '<h2>What we review before ' + service.lower() + ' in ' + city + '</h2>'
        + '<ul class="checklist"><li>The room, the material, and what you want changed</li>'
        + '<li>The existing surface, and the waterproofing and prep it needs</li>'
        + '<li>Layout, grout lines, and the details around fixtures and edges</li>'
        + '<li>Scheduling, access, and how the work fits around your home</li></ul>'
        + '<h2>Questions about ' + service.lower() + ' in ' + city + '</h2>' + faq_html
        + f'<p>More: <a href="{city_href}">Tile installation in {city}</a> and <a href="{service_href}">{service}</a>. See all <a href="service-areas.html">service areas</a>.</p>'
        + '<p>Call <a href="tel:+16028841904">(602) 884-1904</a> to talk through your project and set up a free estimate.</p></main>'
    )

PAGES = {
 "index.html": (
  "Tile Installation & Remodeling | Phoenix, AZ | A.S. Remodeling",
  "High-end tile installation in Phoenix, AZ. Family-owned, one craftsman on every job. Free estimates.",
  f"""<section class="hero"><div class="wrap hero-inner">
<p class="eyebrow">Phoenix, Cave Creek, Anthem, and Scottsdale</p>
<h1>High-End Tile Installation in Phoenix, AZ</h1>
<p class="hero-pitch">{PITCH}</p>
<p class="hero-btns"><a class="btn" href="contact.html">Get a Free Estimate</a> <a class="btn light" href="tel:{PHONE_TEL}">Call {PHONE}</a></p>
<p class="hero-trust">Licensed, Bonded and Insured, {ROC} &nbsp;|&nbsp; 5.0 stars on Google &nbsp;|&nbsp; One craftsman on every job</p>
</div></section>
<section class="trust"><div class="wrap trust-row">
<span><strong>Licensed, Bonded and Insured</strong> {ROC}</span>
<span><strong>5.0 stars</strong> on Google</span>
<span><strong>Family-owned</strong> and local</span>
<span><strong>Free</strong> estimates</span>
</div></section>
<main class="wrap">
{photo("Hero photo: finished tile work")}
<h2>We specialize in</h2>
<div class="cards">
<div class="card"><h3>Shower Tile</h3><p>Full shower tile from the pan up, waterproofed to spec, finished ready for glass.</p><p><a href="shower-tile-installation.html">Shower tile installation</a></p></div>
<div class="card"><h3>Kitchen Tile and Backsplash</h3><p>Backsplash tile with tight lines and clean edges, matched to your cabinets and counters.</p><p><a href="kitchen-tile-backsplash.html">Kitchen tile and backsplash</a></p></div>
<div class="card"><h3>Bathroom Remodeling</h3><p>Full bathroom remodels with tile as the centerpiece, floors, walls, showers, and tub surrounds.</p><p><a href="bathroom-tile-remodeling.html">Bathroom tile and remodeling</a></p></div>
<div class="card"><h3>Tile Flooring</h3><p>Ceramic, porcelain, and stone floors that sit flat and hold up for decades.</p><p><a href="tile-flooring.html">Tile flooring installation</a></p></div>
</div>
<h2>How it works</h2>
<ol class="steps">
<li><strong>1. Call or send a request</strong><span>Tell us about the room and what you want changed.</span></li>
<li><strong>2. Free estimate</strong><span>We look at the space, talk through tile and layout, and give you a clear estimate.</span></li>
<li><strong>3. One craftsman, start to finish</strong><span>Your installer is the person you talked to, not a rotating crew.</span></li>
</ol>
<h2>Why homeowners choose A.S. Remodeling</h2>
<ul class="checklist">
<li>One craftsman on every job, so nothing gets lost between people</li>
<li>Waterproofing and prep done right, the parts you never see but depend on</li>
<li>Straight lines, clean cuts, and grout color matched to the tile</li>
<li>Serving Phoenix, Cave Creek, Anthem, and Scottsdale</li>
</ul>
<p><a href="services.html">See all services</a> in {AREAS}.</p>
<h2>Tile installation across the Valley</h2>
<p>We serve homeowners in <a href="tile-installation-phoenix-az.html">Phoenix</a>, <a href="tile-installation-scottsdale-az.html">Scottsdale</a>, <a href="tile-installation-cave-creek-az.html">Cave Creek</a>, and <a href="tile-installation-anthem-az.html">Anthem</a>. See all <a href="service-areas.html">service areas</a>.</p>
</main>""",
  "index.html"),
 "services.html": (
  "Our Services | Tile, Bathroom & Kitchen Remodeling in Phoenix, AZ | A.S. Remodeling",
  "Shower tile, kitchen tile and backsplash, bathroom remodeling, and tile flooring in Phoenix, Cave Creek, Anthem, and Scottsdale.",
  """<main class="wrap page-head"><h1>Our Services</h1>
<p class="lede">Tile work by one craftsman, from a single backsplash to a full bathroom. Every job starts with a free estimate.</p>
<div class="cards">
<div class="card"><h3>Shower Tile Installation</h3><p>Full shower remodels and retiles, walk-in showers, tub surrounds, shower pans, and waterproofing done to spec.</p><p><a href="shower-tile-installation.html">Shower tile installation</a></p></div>
<div class="card"><h3>Kitchen Tile and Backsplash</h3><p>Backsplash tile in subway, mosaic, stone, and large format, plus kitchen floor tile with clean cuts around outlets and cabinets.</p><p><a href="kitchen-tile-backsplash.html">Kitchen tile and backsplash</a></p></div>
<div class="card"><h3>Bathroom Tile and Remodeling</h3><p>Full bathroom remodels with tile as the centerpiece, including floors, walls, showers, and tub surrounds.</p><p><a href="bathroom-tile-remodeling.html">Bathroom tile and remodeling</a></p></div>
<div class="card"><h3>Tile Flooring Installation</h3><p>Ceramic, porcelain, and stone tile floors, with subfloor prep and leveling so tiles do not crack later.</p><p><a href="tile-flooring.html">Tile flooring installation</a></p></div>
</div>
<p>Not sure which service fits your project? Call <a href="tel:+16028841904">(602) 884-1904</a> and describe the room.</p>
</main>""",
  "services.html"),
 "shower-tile-installation.html": (
  "Shower Tile Installation in Phoenix, AZ | A.S. Remodeling",
  "Full shower tile installation in Phoenix, AZ: waterproofing, wall tile, floor tile, niches, and finishes ready for glass.",
  "<main class=\"wrap page-head\"><h1>Shower Tile Installation in Phoenix, AZ</h1>" + photo("Photo: finished shower tile") + service_body(
   "A shower gets used every day, so the tile work has to be right the first time. I handle full shower tile installation from the pan up: waterproofing, wall tile, floor tile, niches, and finishes ready for glass.",
   ["Full shower remodels and retiles", "Walk-in showers, tub surrounds, and shower pans", "Waterproofing done to spec, the part that keeps a shower from leaking into your walls", "Wall and floor tile, niches, benches, and trim", "Glass enclosure ready finishes"]) + "</main>",
  "services.html"),
 "kitchen-tile-backsplash.html": (
  "Kitchen Tile & Backsplash Installation in Phoenix, AZ | A.S. Remodeling",
  "Kitchen backsplash and floor tile in Phoenix, AZ, with tight lines and clean edges matched to your cabinets and counters.",
  "<main class=\"wrap page-head\"><h1>Kitchen Tile &amp; Backsplash Installation in Phoenix, AZ</h1>" + photo("Photo: finished kitchen backsplash") + service_body(
   "The backsplash is the part of the kitchen everyone looks at. I install backsplash tile with tight lines and clean edges, matched to your cabinets and counters. Kitchen floors too, from a single room to the whole downstairs.",
   ["Kitchen backsplash tile: subway, mosaic, stone, and large format", "Kitchen floor tile", "Clean cuts around outlets, cabinets, and windows", "Grout color matched to the tile", "Caulked edges where the tile meets the counter"]) + "</main>",
  "services.html"),
 "bathroom-tile-remodeling.html": (
  "Bathroom Tile & Remodeling in Phoenix, AZ | A.S. Remodeling",
  "Full bathroom remodels in Phoenix, AZ with tile as the centerpiece: floors, walls, showers, and tub surrounds.",
  "<main class=\"wrap page-head\"><h1>Bathroom Tile &amp; Remodeling in Phoenix, AZ</h1>" + photo("Photo: finished bathroom tile") + service_body(
   "Full bathroom remodels with tile as the centerpiece. Floors, walls, showers, and tub surrounds, handled start to finish by one craftsman who has done hundreds of bathrooms.",
   ["Full bathroom remodels", "Bathroom floor and wall tile", "Shower and tub surround tile", "Shower pans, niches, benches, and trim", "Old tile removal and surface prep"]) + "</main>",
  "services.html"),
 "tile-flooring.html": (
  "Tile Flooring Installation in Phoenix, AZ | A.S. Remodeling",
  "Tile flooring installation in Phoenix, AZ: ceramic, porcelain, and stone tile floors that sit flat and hold up for decades.",
  "<main class=\"wrap page-head\"><h1>Tile Flooring Installation in Phoenix, AZ</h1>" + photo("Photo: finished tile floor") + service_body(
   "Tile floors that sit flat, look straight, and hold up for decades. I install ceramic, porcelain, and stone tile floors across the Phoenix area, with the subfloor prep that keeps tiles from cracking later.",
   ["Ceramic, porcelain, and stone tile floors", "Kitchens, bathrooms, entryways, and whole-home tile", "Subfloor prep and leveling", "Straight grout lines, sealed where it counts", "Transitions finished clean where tile meets other floors"]) + "</main>",
  "services.html"),
 "gallery.html": (
  "Project Gallery | Tile Work in Phoenix, AZ | A.S. Remodeling",
  "Finished tile work by A.S. Remodeling in Phoenix, Cave Creek, Anthem, and Scottsdale.",
  "<main class=\"wrap page-head\"><h1>Project Gallery</h1><p class=\"lede\">Photos below are placeholders. Replace each one with an approved finished-job photo before going live.</p>"
  + '<div class="gallery">' + photo("Photo: bathroom tile") + photo("Photo: shower tile") + photo("Photo: kitchen backsplash") + photo("Photo: tile flooring") + "</div></main>",
  "gallery.html"),
 "about.html": (
  "About A.S. Remodeling | Tile Installer in Phoenix, AZ",
  "A.S. Remodeling is a family-owned tile installer serving Phoenix, Cave Creek, Anthem, and Scottsdale, AZ.",
  f"""<main class="wrap page-head"><h1>About A.S. Remodeling</h1><p class="lede">{PITCH}</p>
<p>A.S. Remodeling LLC is a licensed, bonded and insured AZ tile specialty contractor, {ROC}, serving {AREAS}.</p>
<p>Copy on this staging page is carried over from the current site and the drafted service pages. Aleks must confirm the history and project claims before this page goes live.</p>
<ul class="checklist">
<li>Family-owned, one craftsman on every job</li>
<li>Licensed, bonded and insured, {ROC}</li>
<li>Serving Phoenix, Cave Creek, Anthem, and Scottsdale</li>
</ul></main>""",
  "about.html"),
 "contact.html": (
  "Contact for a Free Estimate | A.S. Remodeling, Phoenix AZ",
  "Contact A.S. Remodeling for a free tile estimate in Phoenix, Cave Creek, Anthem, or Scottsdale.",
  f"""<main class="wrap page-head"><h1>Contact for a Free Estimate</h1>
<p class="lede">Call <a href="tel:{PHONE_TEL}">{PHONE}</a> or email <a href="mailto:{EMAIL}">{EMAIL}</a>. Hours: Monday to Friday, 8am to 5pm.</p>
<div class="form-card">
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
<p><small>Staging note: do not publish this form until a form endpoint (for example a free form service or email handler) is chosen and approved. No submission is sent from this staging build.</small></p>
</div></main>""",
  "contact.html"),
 "tile-installation-phoenix-az.html": (
  "Tile Installation in Phoenix, AZ | A.S. Remodeling",
  "Tile installation in Phoenix, AZ: showers, bathroom tile, kitchen backsplash, and tile floors, from historic homes to North Central ranches.",
  city_body(
   "Phoenix",
   "Phoenix covers a lot of ground, from 1950s ranches in North Central and the Biltmore area to 1980s custom homes, Moon Valley, and historic districts like Willo, Encanto-Palmcroft, Roosevelt, and F.Q. Story. Tile work here has to fit the house it goes into, not the other way around.",
   [
    ("Older homes, new tile that fits the house",
     "Many Phoenix homes were built in the 1930s through the 1980s, and their bathrooms and kitchens carry the character of their era. A 1930s Tudor or Spanish Colonial home may still have its original pink-tiled bathroom, plaster walls, and coved ceilings. New tile in a house like that works best when it respects the period, with subway tile, handpainted Mexican tile, or a patterned floor that suits the room, while the waterproofing and setting materials underneath are modern and built to last."),
    ("Showers and bathrooms in older Phoenix homes",
     "Bathrooms in older homes are often smaller than the ones built today, and the layout needs rethinking before tile goes in. We look at the existing shower pan and walls, the plumbing, and where a niche, bench, or larger shower would actually fit. Waterproofing comes first, then the tile layout, so the finished shower holds up and the grout lines stay straight."),
    ("Kitchens and floors across Phoenix",
     "Kitchen tile in Phoenix runs from a simple backsplash to a full floor through the kitchen and living areas. Backsplash tile is cut around outlets, windows, and cabinets, with clean edges where tile meets the counter. Tile floors need subfloor prep and leveling first, so tiles sit flat and do not crack later, and transitions are finished clean where tile meets wood or carpet in the next room."),
   ],
   [
    ("Do you work in Phoenix historic districts?",
     "Yes, for interior tile work. Interior work generally proceeds with a normal permit. Exterior changes in a designated historic district usually need historic preservation review first, so tell us if your home is in one and we will talk through what applies."),
    ("Can you match old tile in my bathroom?",
     "Sometimes. It depends on whether spare tile is available, or a suitable replacement in the same size, thickness, and shade. Even the same product can vary between batches. Send photos and we will tell you plainly whether a match is likely, or whether a wider replacement makes more sense."),
    ("How long does a shower retile take?",
     "It depends on the size and condition of the shower, and what we find once the old tile comes off. Ask at the estimate and we will give you a timeline for your specific shower, not a generic one."),
   ],
   [("Scottsdale", "tile-installation-scottsdale-az.html"), ("Cave Creek", "tile-installation-cave-creek-az.html"), ("Anthem", "tile-installation-anthem-az.html")]),
  "services.html",
  faq_schema([
    ("Do you work in Phoenix historic districts?", "Yes, for interior tile work. Interior work generally proceeds with a normal permit. Exterior changes in a designated historic district usually need historic preservation review first, so tell us if your home is in one and we will talk through what applies."),
    ("Can you match old tile in my bathroom?", "Sometimes. It depends on whether spare tile is available, or a suitable replacement in the same size, thickness, and shade. Even the same product can vary between batches. Send photos and we will tell you plainly whether a match is likely, or whether a wider replacement makes more sense."),
    ("How long does a shower retile take?", "It depends on the size and condition of the shower, and what we find once the old tile comes off. Ask at the estimate and we will give you a timeline for your specific shower, not a generic one."),
  ])),
 "tile-installation-scottsdale-az.html": (
  "Tile Installation in Scottsdale, AZ | A.S. Remodeling",
  "Tile installation in Scottsdale, AZ: large format tile, marble, and high-end showers and bathrooms, installed with careful prep.",
  city_body(
   "Scottsdale",
   "Scottsdale is where large format tile and natural stone show up most. Primary bathrooms here often ask for large format porcelain or marble walls, a frameless glass enclosure, and a freestanding soaking tub, with fewer grout lines and a clean, open feel. That look only works if the prep underneath is right.",
   [
    ("Large format tile needs a flat floor and a careful layout",
     "Large format tile is a dominant look in Scottsdale luxury bathrooms, and it is also the least forgiving. A large tile shows every dip in the floor or wall, so we check slab and wall flatness first, plan movement joints, and lay out full and cut pieces before setting anything. In Arizona heat, with wide temperature swings between seasons, the setting material and the substrate preparation matter as much as the tile itself."),
    ("Marble and natural stone in showers",
     "Natural stone, marble, and travertine are common requests in Scottsdale, and they behave differently in a shower than in a dry room. Marble and travertine need sealing suited to the specific stone and to wet use, and the maintenance is different from porcelain. We talk through that before you commit to the material, so you know what the tile will need after it is installed."),
    ("Primary bathrooms and slab-on-grade homes",
     "Many Scottsdale homes are single-story and slab-on-grade, which means moving plumbing for a larger shower or a new layout can require cutting concrete. That is a decision to make before ordering tile, not after. We look at the existing layout, the slab, and the fixtures, and plan the tile around what the room can actually support."),
   ],
   [
    ("Should I order large format tile before the floor is reviewed?",
     "No. A sample and the product details help us discuss the layout, but have the existing surface, finished heights, and preparation needs reviewed before committing to the full order. Tile size alone does not tell us whether a floor is suitable."),
    ("Can marble go in a shower?",
     "Yes, with the right stone, the right sealing, and the right maintenance. Marble in a wet area needs more care than porcelain. We will tell you what that care looks like for the specific stone you choose."),
    ("What grout works with large format tile?",
     "It depends on the tile, the joint width, and the room. Large format work often uses narrow joints, and the grout color is matched to the tile so the lines do not fight the pattern. We go over that at the estimate."),
   ],
   [("Phoenix", "tile-installation-phoenix-az.html"), ("Cave Creek", "tile-installation-cave-creek-az.html"), ("Anthem", "tile-installation-anthem-az.html")]),
  "services.html",
  faq_schema([
    ("Should I order large format tile before the floor is reviewed?", "No. A sample and the product details help us discuss the layout, but have the existing surface, finished heights, and preparation needs reviewed before committing to the full order. Tile size alone does not tell us whether a floor is suitable."),
    ("Can marble go in a shower?", "Yes, with the right stone, the right sealing, and the right maintenance. Marble in a wet area needs more care than porcelain. We will tell you what that care looks like for the specific stone you choose."),
    ("What grout works with large format tile?", "It depends on the tile, the joint width, and the room. Large format work often uses narrow joints, and the grout color is matched to the tile so the lines do not fight the pattern. We go over that at the estimate."),
  ])),
 "tile-installation-cave-creek-az.html": (
  "Tile Installation in Cave Creek, AZ | A.S. Remodeling",
  "Tile installation in Cave Creek, AZ: indoor-outdoor tile, patios, showers, and bathroom tile for desert homes.",
  city_body(
   "Cave Creek",
   "Cave Creek is desert living, with covered patios, pools, and homes that open to the outdoors. Many homes here, including the Tatum Ranch homes built in the 1990s, have tile floors through the main living areas, a covered patio off the kitchen, and a primary bath designed to feel like a spa. Tile work here has to handle sun, water, and the step between inside and outside.",
   [
    ("Indoor-outdoor tile, done as one decision",
     "A lot of Cave Creek homes have an accordion glass wall or a wide sliding door between the kitchen and the patio, so the tile inside and outside is really one surface. The same tile can work in both places, but only if it is rated for outdoor use, and only if the doorway, floor heights, and drainage are planned first. We check those before deciding how the two areas should meet."),
    ("Patios, pools, and outdoor living",
     "Covered patios, outdoor kitchens, fireplaces, and pools are part of everyday life in Cave Creek. Outdoor tile needs to suit the sun and the water it will see, and the joints need room for movement. New tile will not fix a drainage problem underneath it, so we look at where water collects after rain, and at the thresholds and steps, before setting anything."),
    ("Bathrooms and floors in Cave Creek homes",
     "Inside, tile floors are common through the whole home, often in a travertine Versailles pattern or a large format porcelain. Primary baths often have dual vanities, a deep soaking tub, and a separate tiled shower. We install the tile, the shower walls and floors, and the backsplashes that tie the kitchen and bath together, with the same prep and waterproofing we use everywhere else."),
   ],
   [
    ("Can I use the same tile inside and outside?",
     "Sometimes, but the tile must be rated for both uses. We also need to check the doorway, floor heights, and outdoor drainage before deciding how the two areas should meet."),
    ("Will patio tile hold up in the Cave Creek sun?",
     "It can, if the tile is rated for outdoor use and the installation allows for movement and drainage. Dark tile and direct sun need extra care in the layout, and we will talk through that for your specific patio."),
    ("Do you install pool tile?",
     "We install tile around pools and in pool areas as part of a tile project. Tell us about the pool, the existing surface, and what needs work, and we will tell you what we can take on."),
   ],
   [("Phoenix", "tile-installation-phoenix-az.html"), ("Scottsdale", "tile-installation-scottsdale-az.html"), ("Anthem", "tile-installation-anthem-az.html")]),
  "services.html",
  faq_schema([
    ("Can I use the same tile inside and outside?", "Sometimes, but the tile must be rated for both uses. We also need to check the doorway, floor heights, and outdoor drainage before deciding how the two areas should meet."),
    ("Will patio tile hold up in the Cave Creek sun?", "It can, if the tile is rated for outdoor use and the installation allows for movement and drainage. Dark tile and direct sun need extra care in the layout, and we will talk through that for your specific patio."),
    ("Do you install pool tile?", "We install tile around pools and in pool areas as part of a tile project. Tell us about the pool, the existing surface, and what needs work, and we will tell you what we can take on."),
  ])),
 "tile-installation-anthem-az.html": (
  "Tile Installation in Anthem, AZ | A.S. Remodeling",
  "Tile installation in Anthem, AZ: updating 1990s and 2000s bathrooms, kitchens, and floors in Parkside and Anthem Country Club.",
  city_body(
   "Anthem",
   "Anthem is a master-planned community built mostly from the late 1990s through the 2000s, split between Anthem Parkside and the gated Anthem Country Club, built between 1999 and 2006. Those homes are now at the age where kitchens, baths, flooring, and windows need attention, and homes with original 2000s finishes sell for less than comparable homes that have been updated.",
   [
    ("Updating 2000s bathrooms and kitchens",
     "The most common Anthem ask is a bathroom or kitchen that finally matches the house. Larger primary showers, a tiled shower with a niche and bench, a new backsplash, and tile floors through the main living areas are the usual starting points. We look at the existing layout first, then talk through tile, grout, and layout before anything is ordered."),
    ("Floors through the house",
     "Many Anthem homes still have their original flooring in the main living areas, with carpet in the bedrooms and tile in the baths. Replacing it with tile through the kitchen, living room, and hallways makes the house feel bigger and easier to keep clean, but the transitions to the bedrooms, the door clearances, and the finished heights all need planning first."),
    ("Permits and design review in Anthem",
     "Anthem is unincorporated, so building permits come from Maricopa County, while exterior changes typically go through the community design review before work starts. Interior tile work is different from an exterior change, but tell us if your project touches the outside of the home, or if your HOA asks for a submittal, and we will talk through what applies before we start."),
   ],
   [
    ("Do I need HOA approval for interior tile work?",
     "Interior tile work usually does not need the same approval as an exterior change, but every community is different. If your HOA asks for a submittal, tell us and we will help you work out what it needs."),
    ("Can you work in the gated Anthem Country Club?",
     "Yes. Tell us which gate and what access your home needs, and we will plan the visit around it."),
    ("How long does a bathroom retile take in Anthem?",
     "It depends on the size and condition of the bathroom, and what we find once the old tile comes off. Ask at the estimate and we will give you a timeline for your specific bathroom."),
   ],
   [("Phoenix", "tile-installation-phoenix-az.html"), ("Scottsdale", "tile-installation-scottsdale-az.html"), ("Cave Creek", "tile-installation-cave-creek-az.html")]),
  "services.html",
  faq_schema([
    ("Do I need HOA approval for interior tile work?", "Interior tile work usually does not need the same approval as an exterior change, but every community is different. If your HOA asks for a submittal, tell us and we will help you work out what it needs."),
    ("Can you work in the gated Anthem Country Club?", "Yes. Tell us which gate and what access your home needs, and we will plan the visit around it."),
    ("How long does a bathroom retile take in Anthem?", "It depends on the size and condition of the bathroom, and what we find once the old tile comes off. Ask at the estimate and we will give you a timeline for your specific bathroom."),
  ])),
 "service-areas.html": (
  "Service Areas | Tile Installation in Phoenix, Scottsdale, Cave Creek & Anthem | A.S. Remodeling",
  "A.S. Remodeling installs tile in Phoenix, Scottsdale, Cave Creek, and Anthem, AZ: showers, bathroom tile, kitchen backsplash, and tile floors.",
  """<main class="wrap page-head"><h1>Service Areas</h1>
<p class="lede">We install tile in Phoenix, Scottsdale, Cave Creek, and Anthem. Each city has its own page, with what tile work there usually involves and what to check before you start.</p>
<div class="cards">
<div class="card"><h3>Phoenix</h3><p>From 1950s ranches in North Central to historic homes in Willo and Roosevelt, tile that fits the house it goes into.</p><p><a href="tile-installation-phoenix-az.html">Tile installation in Phoenix</a></p></div>
<div class="card"><h3>Scottsdale</h3><p>Large format tile, marble, and high-end primary bathrooms, with careful prep for desert heat and slab-on-grade homes.</p><p><a href="tile-installation-scottsdale-az.html">Tile installation in Scottsdale</a></p></div>
<div class="card"><h3>Cave Creek</h3><p>Indoor-outdoor tile, patios, pools, and spa-inspired baths for desert homes that open to the outdoors.</p><p><a href="tile-installation-cave-creek-az.html">Tile installation in Cave Creek</a></p></div>
<div class="card"><h3>Anthem</h3><p>Updating 1990s and 2000s bathrooms, kitchens, and floors in Parkside and Anthem Country Club.</p><p><a href="tile-installation-anthem-az.html">Tile installation in Anthem</a></p></div>
</div>
<p>Call <a href="tel:+16028841904">(602) 884-1904</a> to talk through your project and set up a free estimate.</p></main>""",
  "service-areas.html"),
 "shower-tile-scottsdale-az.html": (
  "Shower Tile Installation in Scottsdale, AZ | A.S. Remodeling",
  "Shower tile installation in Scottsdale, AZ: curbless and walk-in showers, large format tile and marble, with full waterproofing first.",
  service_city_body(
   "Shower Tile Installation",
   "Scottsdale",
   "Scottsdale showers range from compact layouts in mid-century ranch homes near Old Town to larger primary suites in custom builds in Gainey Ranch and DC Ranch. The larger suites have room for a curbless shower, a freestanding tub, and separate vanities, while the smaller homes need the layout planned carefully before tile goes in.",
   [
    ("Curbless and walk-in showers",
     "A curbless shower has no step or curb at the entry, so the tile floor runs unbroken into the shower with a linear drain and frameless glass. It reads larger and calmer, and it needs precise waterproofing and drainage planning to work. We install a full waterproofing membrane on the walls and pan before tile goes on, because Scottsdale dry air does not remove the moisture risk inside a shower. Daily use creates localized humidity that can wear down a poorly waterproofed shower over time."),
    ("Large format tile and marble shower walls",
     "Large format porcelain or stone tile on shower walls, in 24 by 48 inch formats and larger, gives fewer grout lines and a clean, open feel, but only on a flat substrate with tight tolerances. Marble and honed natural stone give a depth that printed tile cannot match, and they need sealing suited to wet use and more care after installation. Marble-look porcelain is the lower-care alternative when you want the look without the maintenance."),
    ("Tub-to-shower conversions",
     "Replacing a tub-shower combo with a walk-in shower is a common ask in Scottsdale, especially in homes where the original tub is rarely used. We look at the existing plumbing, the drain, and the slab before planning the new shower, because moving plumbing in a slab-on-grade home can require cutting concrete. The shower footprint, the niche and bench, and the glass are planned before demolition, so the tile layout is settled before anything is ordered."),
   ],
   [
    ("Can I replace my shower without moving the plumbing?",
     "Often, yes, if the new shower fits the existing drain and layout. If you want a larger shower or a different layout, the plumbing may need to move, and that is a decision to make before ordering tile."),
    ("Does a curbless shower need special waterproofing?",
     "Yes. A curbless shower needs a full waterproofing membrane, a correctly sloped floor, and a drain planned for the whole shower, not just the center. We go over that at the estimate for your specific shower."),
    ("Marble or porcelain for shower walls?",
     "Marble is beautiful and needs sealing and more care in a wet area. Porcelain, including marble-look porcelain, is more forgiving and easier to maintain. We will talk through the care each one needs before you choose."),
   ],
   "tile-installation-scottsdale-az.html", "shower-tile-installation.html"),
  "services.html",
  faq_schema([
    ("Can I replace my shower without moving the plumbing?", "Often, yes, if the new shower fits the existing drain and layout. If you want a larger shower or a different layout, the plumbing may need to move, and that is a decision to make before ordering tile."),
    ("Does a curbless shower need special waterproofing?", "Yes. A curbless shower needs a full waterproofing membrane, a correctly sloped floor, and a drain planned for the whole shower, not just the center. We go over that at the estimate for your specific shower."),
    ("Marble or porcelain for shower walls?", "Marble is beautiful and needs sealing and more care in a wet area. Porcelain, including marble-look porcelain, is more forgiving and easier to maintain. We will talk through the care each one needs before you choose."),
  ])),
 "shower-tile-phoenix-az.html": (
  "Shower Tile Installation in Phoenix, AZ | A.S. Remodeling",
  "Shower tile installation in Phoenix, AZ: showers in older homes, tub-to-shower conversions, and tile that fits the house.",
  service_city_body(
   "Shower Tile Installation",
   "Phoenix",
   "Phoenix showers are often in smaller bathrooms than the ones built today, in homes from the 1930s through the 1980s. Plumbing is often stacked close together, which limits how much a layout can shift, and the tile has to work with the room it is in, not against it.",
   [
    ("Small bathrooms, planned layouts",
     "Bathrooms in older Phoenix homes are often smaller footprints, so the shower layout needs rethinking before tile goes in. Accent walls, borders, and niches can add detail without overwhelming the room, and the tile layout is planned around the existing plumbing and the size of the shower. We look at the shower pan and walls first, then talk through what fits, so the finished shower feels bigger than it is."),
    ("Tub-to-shower conversions in older homes",
     "Replacing a tub with a walk-in shower is a common ask in Phoenix, and what we find once the old tile comes off matters. Old shower pans, walls, and waterproofing are often past their best, so we plan the new pan, the membrane, and the drain before setting tile. A curbless entry or a low threshold is possible in many homes, but it depends on the floor and the drain, and we will tell you plainly what your shower can support."),
    ("Tile choices that fit the house",
     "A shower in a historic home in Willo or Encanto-Palmcroft does not need the same tile as a new build. Subway, hexagon, mosaic, and glass accents suit period bathrooms, and a patterned floor can carry the character of the house without making the room feel busy. We help you choose tile that fits the home, then install it with the modern waterproofing underneath that keeps it looking right for years."),
   ],
   [
    ("Can you match the old tile in my shower?",
     "Sometimes. It depends on whether spare tile is available, or a suitable replacement in the same size, thickness, and shade. Even the same product can vary between batches. Send photos and we will tell you plainly whether a match is likely."),
    ("Do you work in Phoenix historic districts?",
     "Yes, for interior tile work. Interior work generally proceeds with a normal permit. Exterior changes in a designated historic district usually need historic preservation review first, so tell us if your home is in one."),
    ("Can I keep my tub and just retile the surround?",
     "Often, yes, if the tub and the walls behind the tile are in good condition. We check the existing surface first, then talk through whether a retile or a wider replacement makes more sense."),
   ],
   "tile-installation-phoenix-az.html", "shower-tile-installation.html"),
  "services.html",
  faq_schema([
    ("Can you match the old tile in my shower?", "Sometimes. It depends on whether spare tile is available, or a suitable replacement in the same size, thickness, and shade. Even the same product can vary between batches. Send photos and we will tell you plainly whether a match is likely."),
    ("Do you work in Phoenix historic districts?", "Yes, for interior tile work. Interior work generally proceeds with a normal permit. Exterior changes in a designated historic district usually need historic preservation review first, so tell us if your home is in one."),
    ("Can I keep my tub and just retile the surround?", "Often, yes, if the tub and the walls behind the tile are in good condition. We check the existing surface first, then talk through whether a retile or a wider replacement makes more sense."),
  ])),
 "bathroom-tile-scottsdale-az.html": (
  "Bathroom Tile Installation in Scottsdale, AZ | A.S. Remodeling",
  "Bathroom tile installation in Scottsdale, AZ: large format floors, marble walls, and primary and guest bathrooms, installed with careful prep.",
  service_city_body(
   "Bathroom Tile Installation",
   "Scottsdale",
   "Scottsdale bathrooms span a wide range of home styles and sizes, from compact layouts in mid-century ranch homes near Old Town to larger primary suites in custom builds in Gainey Ranch and DC Ranch. The tile work is different in each, and the prep underneath matters more than the tile on top.",
   [
    ("Bathroom floors that sit flat",
     "Large format porcelain or stone tile on bathroom floors needs a flat substrate first, with movement joints planned and the layout settled before setting. In Arizona heat, with wide temperature swings between seasons, the setting material and the substrate preparation matter as much as the tile itself. Epoxy grout is available for homeowners who want the most stain-resistant and moisture-resistant grout, especially where water contact with the floor tile is constant."),
    ("Primary bathrooms, walls and vanities",
     "A primary bathroom in Scottsdale often asks for large format tile on the walls, a freestanding tub, and separate vanities, with a curbless shower and frameless glass. We plan the wall tile, the niche and bench, and the transitions to the floor as one layout, so the grout lines stay straight and the room reads calm. Marble and natural stone need sealing suited to wet use, and we talk through that care before you commit."),
    ("Guest baths and powder rooms",
     "Guest baths and powder rooms are smaller, and the tile can carry more personality there without overwhelming the room. A patterned floor, a mosaic accent, or a bold wall tile works in a small room when the layout is planned around the vanity, the mirror, and the door swing. We keep the details in proportion to the room, so the finished bath feels intentional, not busy."),
   ],
   [
    ("Is epoxy grout worth it in a bathroom?",
     "It can be, especially in a shower or on a floor that sees a lot of water. Epoxy grout is more stain-resistant and moisture-resistant than standard grout, and it costs more to install. We will talk through whether it fits your bathroom."),
    ("Can tile run from the bathroom floor into the shower?",
     "Yes, in many bathrooms, and it makes the room feel larger. It needs the right tile for wet use, a correctly sloped shower floor, and a drain planned for the whole area."),
    ("Large format tile on a bathroom floor, is the slab flat enough?",
     "That depends on your floor, and we check it before ordering tile. Large format tile shows every dip, so flatness is checked first, and leveling is planned before setting anything."),
   ],
   "tile-installation-scottsdale-az.html", "bathroom-tile-remodeling.html"),
  "services.html",
  faq_schema([
    ("Is epoxy grout worth it in a bathroom?", "It can be, especially in a shower or on a floor that sees a lot of water. Epoxy grout is more stain-resistant and moisture-resistant than standard grout, and it costs more to install. We will talk through whether it fits your bathroom."),
    ("Can tile run from the bathroom floor into the shower?", "Yes, in many bathrooms, and it makes the room feel larger. It needs the right tile for wet use, a correctly sloped shower floor, and a drain planned for the whole area."),
    ("Large format tile on a bathroom floor, is the slab flat enough?", "That depends on your floor, and we check it before ordering tile. Large format tile shows every dip, so flatness is checked first, and leveling is planned before setting anything."),
  ])),
 "bathroom-tile-phoenix-az.html": (
  "Bathroom Tile Installation in Phoenix, AZ | A.S. Remodeling",
  "Bathroom tile installation in Phoenix, AZ: floors, walls, and shower surrounds in older homes, with tile that fits the house.",
  service_city_body(
   "Bathroom Tile Installation",
   "Phoenix",
   "Bathrooms in older Phoenix homes are often smaller footprints, and the tile has to be planned around the room, not just the pattern. Porcelain and ceramic floors are selected for moisture exposure, and accent walls, borders, and niches add detail without overwhelming a small room.",
   [
    ("Floors and walls in small baths",
     "A small bathroom needs the tile layout planned first, so the cuts fall where they should and the grout lines stay straight. We look at the existing floor, the walls, and the transitions to the hallway, then plan the tile around the vanity, the tub or shower, and the door. Tile floors need subfloor prep and leveling first, so tiles sit flat and do not crack later."),
    ("Period bathrooms, kept in character",
     "Many Phoenix bathrooms still carry the character of their era, from a 1930s pink-tiled bathroom to black-and-white floors and handpainted Mexican tile. New tile in a house like that works best when it respects the period, with subway tile, a patterned floor, or a mosaic that suits the room, while the waterproofing and setting materials underneath are modern and built to last."),
    ("Shower and tub surrounds",
     "The shower and tub surround is where waterproofing matters most. We check the existing pan and walls, plan the membrane and the drain, then set the tile with niches, benches, and trim planned before anything goes up. The finished surround should look clean and hold up, with grout lines that stay straight and edges finished where tile meets the tub or the wall."),
   ],
   [
    ("Can you tile over my existing bathroom floor?",
     "It depends on the condition of the existing floor and what is underneath it. Sometimes it works, and sometimes removal is the right call. We check the surface first, then tell you plainly which way makes sense for your bathroom."),
    ("How do I choose tile for a small bathroom?",
     "Start with the size of the room and the light it gets, then the tile size and pattern. Large tile can make a small room feel bigger, and a patterned floor can carry the room, but the layout has to be planned around the fixtures. Bring photos and we will talk through it at the estimate."),
    ("Do you handle the whole bathroom remodel?",
     "We lead with the tile and work with licensed trades for the rest. Ask us about your specific project and we will tell you plainly what we do ourselves and what we bring in help for."),
   ],
   "tile-installation-phoenix-az.html", "bathroom-tile-remodeling.html"),
  "services.html",
  faq_schema([
    ("Can you tile over my existing bathroom floor?", "It depends on the condition of the existing floor and what is underneath it. Sometimes it works, and sometimes removal is the right call. We check the surface first, then tell you plainly which way makes sense for your bathroom."),
    ("How do I choose tile for a small bathroom?", "Start with the size of the room and the light it gets, then the tile size and pattern. Large tile can make a small room feel bigger, and a patterned floor can carry the room, but the layout has to be planned around the fixtures. Bring photos and we will talk through it at the estimate."),
    ("Do you handle the whole bathroom remodel?", "We lead with the tile and work with licensed trades for the rest. Ask us about your specific project and we will tell you plainly what we do ourselves and what we bring in help for."),
  ])),
 "kitchen-backsplash-scottsdale-az.html": (
  "Kitchen Tile Backsplash Installation in Scottsdale, AZ | A.S. Remodeling",
  "Kitchen backsplash installation in Scottsdale, AZ: marble, zellige, and large format backsplashes, set around cabinets, counters, and hoods.",
  service_city_body(
   "Kitchen Tile Backsplash Installation",
   "Scottsdale",
   "Scottsdale kitchens often pair quartz counters with a marble backsplash, or warm wood cabinets with zellige tile and brass details. The backsplash is where most of the kitchen personality lives, and it is the surface homeowners rethink first in a renovation.",
   [
    ("Marble and stone backsplashes",
     "A marble subway tile backsplash adds subtle texture and a timeless look behind the range and along the walls, and stone like Taj Mahal quartzite can carry the veining from the countertop up the wall and across the hood for one continuous look. Natural stone needs sealing suited to kitchen use, and we talk through that care before you choose, so you know what the tile will need after it is installed."),
    ("Zellige and handmade-look tile",
     "Handmade-looking ceramics and zellige tile have settled in as a staple in Scottsdale kitchens, prized for the organic variation and warmth they bring. The fresh part is how restrained the applications have become, with straight stacks and clean grids letting the natural variation in the glaze do the work. A half offset is the forgiving default for handmade tile, because it hides small variations in tile length, and we plan the pattern, the waste, and the order before setting anything."),
    ("Full-height and slab-look backsplashes",
     "Running the backsplash all the way to the ceiling, or using large format porcelain in 24 by 48 inch formats, gives fewer grout lines and a clean, open look. The layout is planned around the outlets, windows, hood, and cabinet lines, so cuts and grout joints look intentional. A standard field is 18 inches from counter to upper cabinet, and a vertical stack can read taller in a short field, but it needs a dead-level first course or the whole field leans."),
   ],
   [
    ("Does a marble backsplash need sealing?",
     "Yes, marble in a kitchen needs sealing suited to the stone and to kitchen use, and it needs more care than porcelain. We will talk through what that care looks like for the specific stone you choose."),
    ("Will zellige tile look uneven?",
     "Zellige tile is made to vary, in color, thickness, and glaze, and that variation is the point. Set in a straight stack or a running bond, it catches light and gives a custom, lived-in feel, and we plan the layout so the variation reads as warmth, not as a mistake."),
    ("Should the backsplash run to the ceiling?",
     "It can, and it often looks best when it does, especially behind the range. Stopping halfway can read unfinished. We will show you how it would look in your kitchen at the estimate."),
   ],
   "tile-installation-scottsdale-az.html", "kitchen-tile-backsplash.html"),
  "services.html",
  faq_schema([
    ("Does a marble backsplash need sealing?", "Yes, marble in a kitchen needs sealing suited to the stone and to kitchen use, and it needs more care than porcelain. We will talk through what that care looks like for the specific stone you choose."),
    ("Will zellige tile look uneven?", "Zellige tile is made to vary, in color, thickness, and glaze, and that variation is the point. Set in a straight stack or a running bond, it catches light and gives a custom, lived-in feel, and we plan the layout so the variation reads as warmth, not as a mistake."),
    ("Should the backsplash run to the ceiling?", "It can, and it often looks best when it does, especially behind the range. Stopping halfway can read unfinished. We will show you how it would look in your kitchen at the estimate."),
  ])),
 "kitchen-backsplash-phoenix-az.html": (
  "Kitchen Tile Backsplash Installation in Phoenix, AZ | A.S. Remodeling",
  "Kitchen backsplash installation in Phoenix, AZ: subway, hexagon, and mosaic backsplashes in historic and mid-century kitchens.",
  service_city_body(
   "Kitchen Tile Backsplash Installation",
   "Phoenix",
   "Phoenix kitchens run from galley kitchens in historic bungalows in Willo and Encanto-Palmcroft to mid-century homes in Ahwatukee and the Biltmore corridor. The backsplash has to work with the cabinets and counters already there, and with the character of the house.",
   [
    ("Subway and hexagon in historic kitchens",
     "Subway tile is the timeless choice in a historic Phoenix kitchen, and it suits the cabinets and counters without fighting them. Backsplash layouts are aligned with countertop edges and cabinet lines so cuts and grout joints look intentional, and the grout lines come out symmetrical instead of looking squeezed in. Hexagon tile gives a structured pattern with the same period feel, and we plan the cuts around outlets, windows, and the range hood before setting anything."),
    ("Mosaic, glass, and natural stone",
     "Mosaic, glass, and natural stone tile can add color and texture to a Phoenix kitchen without overwhelming it, coordinated with the room finishes. A colorful tiled backsplash suits a historic Coronado kitchen, and a quiet stone backsplash suits a mid-century home. We help you choose tile that fits the kitchen, then set it with clean edges where tile meets the counter and the cabinets."),
    ("Backsplashes as part of a tile-led remodel",
     "A backsplash is often the first tile in a wider kitchen update, and we lead with the tile and work with licensed trades for the rest. Tell us about the kitchen, the counters, and what you want changed, and we will tell you plainly what we do ourselves and what we bring in help for, so the finished kitchen feels like one project, not a set of separate jobs."),
   ],
   [
    ("Can a backsplash match my countertop?",
     "It should coordinate with the countertop, not match it exactly. Bring a sample of the countertop, or photos of the kitchen, and we will talk through tile colors and patterns that work with it."),
    ("What grout color works with subway tile?",
     "It depends on the tile and the look you want. A grout close to the tile color gives a calm, continuous look, and a contrasting grout makes the pattern stand out. We go over that at the estimate."),
    ("Can you install a backsplash over my old tile?",
     "It depends on the condition of the existing tile and what is underneath it. Sometimes it works, and sometimes removal is the right call. We check the surface first, then tell you plainly which way makes sense for your kitchen."),
   ],
   "tile-installation-phoenix-az.html", "kitchen-tile-backsplash.html"),
  "services.html",
  faq_schema([
    ("Can a backsplash match my countertop?", "It should coordinate with the countertop, not match it exactly. Bring a sample of the countertop, or photos of the kitchen, and we will talk through tile colors and patterns that work with it."),
    ("What grout color works with subway tile?", "It depends on the tile and the look you want. A grout close to the tile color gives a calm, continuous look, and a contrasting grout makes the pattern stand out. We go over that at the estimate."),
    ("Can you install a backsplash over my old tile?", "It depends on the condition of the existing tile and what is underneath it. Sometimes it works, and sometimes removal is the right call. We check the surface first, then tell you plainly which way makes sense for your kitchen."),
  ])),
}

CSS = """
:root{--ink:#22302e;--ink-soft:#4a5a57;--cream:#f7f2e9;--paper:#fffdf8;--terra:#b4552d;--terra-dark:#8f3f1f;--teal:#1e4a48;--gold:#c9a86a;--line:#e5ddd0;--card:#ffffff}
*{box-sizing:border-box}
body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;margin:0;color:var(--ink);line-height:1.65;background:var(--paper)}
h1,h2,h3{font-family:Georgia,'Times New Roman',serif;line-height:1.15;color:var(--ink);letter-spacing:-.01em}
h1{font-size:clamp(2rem,5vw,3.1rem);margin:.2em 0 .4em}
h2{font-size:1.65rem;margin:2.2em 0 .6em}
h3{font-size:1.2rem;margin:0 0 .4em}
p{margin:.5em 0 .9em}
a{color:var(--terra-dark)}
.wrap{max-width:1060px;margin:0 auto;padding:0 24px}
.lede{font-size:1.15rem;color:var(--ink-soft);max-width:62ch}
.page-head{padding:44px 24px 8px}
/* header */
header{border-bottom:1px solid var(--line);position:sticky;top:0;background:rgba(255,253,248,.97);z-index:10;backdrop-filter:blur(6px)}
.bar{display:flex;gap:18px;align-items:center;flex-wrap:wrap;padding:14px 24px}
.brand{font-family:Georgia,serif;font-weight:700;text-decoration:none;color:var(--ink);font-size:1.25rem;display:flex;align-items:center;gap:10px}
.brand img.logo{height:46px;width:auto;display:block}
.mark{display:inline-grid;place-items:center;width:38px;height:38px;border-radius:9px;background:var(--teal);color:#fff;font-family:system-ui,sans-serif;font-weight:800;font-size:.85rem;letter-spacing:.04em}
nav a{margin-right:16px;text-decoration:none;color:var(--ink-soft);font-weight:600;font-size:.95rem}
nav a:hover{color:var(--terra-dark)}
nav a.active{color:var(--terra-dark);border-bottom:2px solid var(--terra)}
.call{margin-left:auto;background:var(--terra);color:#fff;padding:10px 16px;border-radius:999px;text-decoration:none;font-weight:700;white-space:nowrap;box-shadow:0 2px 10px rgba(180,85,45,.3)}
.call:hover{background:var(--terra-dark)}
/* hero */
.hero{background:var(--teal);color:#fff;background-image:linear-gradient(rgba(255,255,255,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.07) 1px,transparent 1px);background-size:56px 56px}
.hero-inner{padding:64px 24px 58px}
.eyebrow{text-transform:uppercase;letter-spacing:.14em;font-size:.8rem;font-weight:700;color:var(--gold);margin:0 0 12px}
.hero h1{color:#fff;margin:0 0 14px;max-width:16ch}
.hero-pitch{font-size:1.2rem;color:#e8efec;max-width:56ch}
.hero-btns{margin:22px 0 14px}
.hero-trust{color:#cfe0dc;font-size:.95rem;margin:18px 0 0}
.btn{display:inline-block;background:var(--terra);color:#fff;padding:12px 22px;border-radius:999px;text-decoration:none;font-weight:700;margin:0 10px 10px 0;box-shadow:0 4px 14px rgba(0,0,0,.18)}
.btn:hover{background:var(--terra-dark)}
.btn.secondary{background:#fff;color:var(--ink);border:1px solid var(--line);box-shadow:none}
.btn.light{background:#fff;color:var(--teal);box-shadow:none}
/* trust bar */
.trust{background:var(--cream);border-bottom:1px solid var(--line)}
.trust-row{display:flex;flex-wrap:wrap;gap:10px 32px;padding:16px 24px;font-size:.98rem;color:var(--ink-soft)}
.trust-row strong{color:var(--ink)}
/* cards */
.cards{display:grid;grid-template-columns:repeat(2,1fr);gap:18px;margin:18px 0 8px}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:22px;box-shadow:0 6px 22px rgba(34,48,46,.07)}
.card p{color:var(--ink-soft)}
.card a{font-weight:700}
/* steps */
.steps{list-style:none;padding:0;display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin:16px 0}
.steps li{background:var(--cream);border:1px solid var(--line);border-radius:16px;padding:20px}
.steps strong{display:block;font-family:Georgia,serif;font-size:1.1rem;margin-bottom:6px}
.steps span{color:var(--ink-soft)}
/* checklist */
.checklist{list-style:none;padding:0}
.checklist li{padding:8px 0 8px 34px;position:relative}
.checklist li:before{content:"✓";position:absolute;left:0;top:8px;width:24px;height:24px;border-radius:50%;background:var(--teal);color:#fff;display:grid;place-items:center;font-size:.85rem}
/* photo placeholders: styled tile blocks, still clearly placeholders */
.photo{position:relative;border-radius:16px;overflow:hidden;margin:22px 0;min-height:260px;background:#dfe8e4;background-image:linear-gradient(rgba(30,74,72,.18) 1px,transparent 1px),linear-gradient(90deg,rgba(30,74,72,.18) 1px,transparent 1px),linear-gradient(135deg,#e9e2d2 0%,#d7e0da 55%,#c9d6cf 100%);background-size:72px 72px,72px 72px,100% 100%;border:1px solid var(--line);display:grid;place-items:center;text-align:center}
.photo-label{background:rgba(255,253,248,.94);border:1px solid var(--line);border-radius:12px;padding:16px 20px;font-family:Georgia,serif;font-size:1.15rem;font-weight:700;max-width:82%}
.photo-label small{display:block;font-family:system-ui,sans-serif;font-weight:400;font-size:.85rem;color:var(--ink-soft);margin-top:6px}
.gallery{display:grid;grid-template-columns:repeat(2,1fr);gap:18px}
.gallery .photo{min-height:220px;margin:0}
/* CTA + footer */
.cta{background:var(--teal);color:#fff;margin-top:56px}
.cta-inner{display:flex;gap:24px;align-items:center;justify-content:space-between;flex-wrap:wrap;padding:40px 24px}
.cta h2{color:#fff;margin:0 0 6px}
.cta p{color:#dce9e5;margin:0}
.cta-btns{margin:0}
footer{background:#182624;color:#c8d6d2}
.footgrid{display:grid;grid-template-columns:2fr 1fr 1fr;gap:28px;padding:44px 24px}
.footbrand{font-family:Georgia,serif;font-size:1.2rem;color:#fff;font-weight:700;margin:0 0 8px}
.foothead{font-weight:700;color:#fff;margin:0 0 8px}
footer a{color:#f0d9c8}
footer p{margin:.4em 0}
/* form */
.form-card{background:#fff;border:1px solid var(--line);border-radius:16px;padding:26px;box-shadow:0 6px 22px rgba(34,48,46,.07);max-width:640px;margin:20px 0 32px}
form label{display:block;margin:14px 0;font-weight:600}
form input,form select,form textarea{width:100%;padding:12px;margin-top:6px;box-sizing:border-box;border:1px solid #cbd5d1;border-radius:10px;font:inherit}
form input:focus,form select:focus,form textarea:focus{outline:2px solid var(--terra);outline-offset:1px}
form button{background:var(--terra);color:#fff;padding:13px 22px;border:0;border-radius:999px;font-weight:700;cursor:pointer;margin-top:8px}
form button:hover{background:var(--terra-dark)}
#form-note{color:var(--ink-soft)}
@media (max-width:720px){
.cards,.steps,.gallery,.footgrid{grid-template-columns:1fr}
.hero-inner{padding:44px 24px 40px}
.bar{padding:12px 16px}
.call{margin-left:0;width:100%;text-align:center}
nav{order:3;width:100%}
nav a{margin-right:14px}
.cta-inner{padding:32px 24px}
}
"""

def main():
    OUT.mkdir(exist_ok=True)
    # Aleks's real logo (SVG traced 2026-11-07 from his low-res JPEG).
    # Copy it into dist/ so the header and favicon can use it.
    shutil.copyfile(pathlib.Path(__file__).parent / "as-remodeling-logo.svg", OUT / "as-remodeling-logo.svg")
    shutil.copyfile(pathlib.Path(__file__).parent / "as-remodeling-logo-horizontal.svg", OUT / "as-remodeling-logo-horizontal.svg")
    for slug, entry in PAGES.items():
        title, desc, body, active = entry[:4]
        extra = entry[4] if len(entry) > 4 else None
        (OUT / slug).write_text(page(slug, title, desc, body, active, extra), encoding="utf-8")
    (OUT / "style.css").write_text(CSS, encoding="utf-8")
    urls = "".join(f"<url><loc>https://www.asremodelingllc.com/{s if s != 'index.html' else ''}</loc></url>\n" for s in PAGES)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n', encoding="utf-8")
    (OUT / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: https://www.asremodelingllc.com/sitemap.xml\n", encoding="utf-8")
    print(f"Built {len(PAGES)} pages in {OUT}")

if __name__ == "__main__":
    main()
