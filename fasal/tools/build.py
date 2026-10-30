#!/usr/bin/env python3
"""Fasal static site builder. Pure stdlib. Reads data/crops.json, writes the site."""
import json, os, shutil, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = json.load(open(os.path.join(ROOT, 'data', 'crops.json'), encoding='utf-8'))
CATS = DATA['categories']
CROPS = DATA['crops']
SITE = DATA['site']
CAT = {c['slug']: c for c in CATS}
BYCAT = {}
for c in CROPS:
    BYCAT.setdefault(c['cat'], []).append(c)

def E(s): return html.escape(s or '')

# ---------- Original duotone botanical motifs (Python mirror of app.js) ----------
def motif(motif_name, hue, size=96):
    P = f'hsl({hue},48%,52%)'; T = f'hsl({hue},38%,86%)'; D = f'hsl({hue},45%,34%)'
    shapes = {
    'grain': f'<path d="M50 92V38" stroke="{D}" stroke-width="4" stroke-linecap="round"/><path d="M50 30c-9-2-15-10-15-20 10 0 15 8 15 20zm0 0c9-2 15-10 15-20-10 0-15 8-15 20z" fill="{P}"/><path d="M50 52c-8-2-13-8-13-17 9 0 13 7 13 17zm0 0c8-2 13-8 13-17-9 0-13 7-13 17z" fill="{T}" stroke="{D}" stroke-width="2"/><path d="M50 74c-8-2-13-8-13-17 9 0 13 7 13 17zm0 0c8-2 13-8 13-17-9 0-13 7-13 17z" fill="{P}" opacity=".8"/><path d="M50 92c-6 0-12-3-16-8M50 92c6 0 12-3 16-8" stroke="{D}" stroke-width="3" stroke-linecap="round"/>',
    'pod': f'<path d="M28 70C28 44 44 30 74 26c2 0 3 2 2 4C70 58 54 72 30 74c-1 0-2-2-2-4z" fill="{T}" stroke="{D}" stroke-width="3"/><circle cx="42" cy="58" r="5" fill="{P}"/><circle cx="54" cy="50" r="5" fill="{P}"/><circle cx="64" cy="42" r="5" fill="{P}"/><path d="M74 26c8-6 16-6 20-2-4 6-12 6-20 2z" fill="{P}"/>',
    'flower': f'<g fill="{P}"><ellipse cx="50" cy="28" rx="10" ry="14"/><ellipse cx="50" cy="72" rx="10" ry="14"/><ellipse cx="28" cy="50" rx="14" ry="10"/><ellipse cx="72" cy="50" rx="14" ry="10"/><ellipse cx="34" cy="34" rx="10" ry="12" transform="rotate(-45 34 34)"/><ellipse cx="66" cy="34" rx="10" ry="12" transform="rotate(45 66 34)"/><ellipse cx="34" cy="66" rx="10" ry="12" transform="rotate(45 34 66)"/><ellipse cx="66" cy="66" rx="10" ry="12" transform="rotate(-45 66 66)"/></g><circle cx="50" cy="50" r="9" fill="{D}"/><circle cx="50" cy="50" r="5" fill="{T}"/>',
    'fruit': f'<circle cx="50" cy="58" r="26" fill="{P}"/><path d="M50 58c-8-8-8-20 0-26 8 6 8 18 0 26z" fill="{T}" opacity=".55"/><path d="M50 32c0-8 4-12 10-14" stroke="{D}" stroke-width="4" stroke-linecap="round"/><path d="M60 20c8-4 16-2 20 4-6 4-14 4-20-4z" fill="{D}"/>',
    'leaf': f'<path d="M50 88C30 70 26 44 34 18c26 4 40 24 34 52-4 12-10 16-18 18z" fill="{P}"/><path d="M50 88C48 64 44 40 34 18" stroke="{D}" stroke-width="3" stroke-linecap="round"/><path d="M48 66l-12-6M47 54l-10-8M46 42l-8-8M52 66l12-6M53 54l10-8" stroke="{D}" stroke-width="2" stroke-linecap="round"/>',
    'root': f'<path d="M50 12c10 0 16 6 16 14 0 14-8 26-12 44-2 10-6 18-8 18s-4-8-5-16c-3-18-9-32-9-46 0-8 8-14 18-14z" fill="{P}"/><path d="M50 12c-4-6-12-8-18-6M50 12c4-6 12-8 18-6" stroke="{D}" stroke-width="3" stroke-linecap="round"/><path d="M38 40h24M40 54h20" stroke="{D}" stroke-width="2" opacity=".5"/>',
    'grass': f'<g stroke="{P}" stroke-width="5" stroke-linecap="round"><path d="M50 90C50 70 46 50 34 34"/><path d="M50 90c0-22 4-42 16-58"/><path d="M50 90c-8-14-20-22-32-26"/><path d="M50 90c8-14 20-22 32-26"/><path d="M50 90V60"/></g><path d="M30 90h40" stroke="{D}" stroke-width="5" stroke-linecap="round"/>',
    'tree': f'<circle cx="50" cy="36" r="22" fill="{P}"/><circle cx="34" cy="46" r="12" fill="{T}"/><path d="M50 58v32M50 70l-14-8M50 70l14-8" stroke="{D}" stroke-width="5" stroke-linecap="round"/><path d="M38 90h24" stroke="{D}" stroke-width="5" stroke-linecap="round"/>',
    'bulb': f'<path d="M50 88c-14-8-20-20-20-34 0-16 10-28 20-34 10 6 20 18 20 34 0 14-6 26-20 34z" fill="{T}" stroke="{D}" stroke-width="3"/><path d="M50 20c-6 12-8 26-6 44M50 20c6 12 8 26 6 44" stroke="{P}" stroke-width="3"/><path d="M50 20c0-6 2-10 6-12" stroke="{D}" stroke-width="3" stroke-linecap="round"/>',
    }
    return f'<svg viewBox="0 0 100 100" width="{size}" height="{size}" fill="none" aria-hidden="true">{shapes.get(motif_name, shapes["leaf"])}</svg>'

# ---------- Shared chrome ----------
NAV = [('home','/index.html','Home'),('learn','/learn/index.html','Learn'),('about','/about/index.html','About'),('challenge','/challenge/index.html','Challenge')]
ICONS = {'home':'⌂','learn':'❦','about':'✿','challenge':'🏆'}

def head(title, desc):
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)} | Fasal</title><meta name="description" content="{E(desc)}">
<meta property="og:title" content="{E(title)} | Fasal"><meta property="og:description" content="{E(desc)}">
<link rel="stylesheet" href="/assets/css/style.css"></head>"""

def header(active):
    links = ''.join(f'<a href="{u}" class="{"active" if k==active else ""}" data-i18n="{k}">{label}</a>' for k,u,label in NAV)
    return f"""<header class="site-header"><div class="wrap header-inner">
<a class="brand" href="/index.html"><span class="brand-mark">🌱</span><span>Fasal<small>FIELD NOTES</small></span></a>
<nav class="main-nav">{links}</nav>
<div class="lang-toggle"><button data-lang="en" class="on">English</button><button data-lang="hi">अ</button></div>
<a class="btn btn-primary header-cta" href="#" data-open-modal="joinModal" style="padding:10px 22px;font-size:.9rem"><span data-user-greet data-i18n="signin">Sign in</span></a>
</div></header>"""

def tabbar(active):
    items = ''.join(f'<a href="{u}" class="{"active" if k==active else ""}"><span class="ti">{ICONS[k]}</span><span data-i18n="{k}">{label}</span></a>' for k,u,label in NAV)
    return f'<nav class="tab-bar">{items}</nav>'

def footer():
    catlinks = ''.join(f'<a href="/category/{c["slug"]}/index.html">{E(c["name"])}</a>' for c in CATS[:7])
    return f"""<footer class="site-footer"><div class="wrap">
<div class="footer-grid">
<div><div class="footer-brand">🌱 Fasal</div><p class="footer-note">Original field notes on the crops behind everyday life. Built as a learning demo — all text and artwork are original.</p></div>
<div><h4>Explore</h4><a href="/index.html" data-i18n="home">Home</a><a href="/learn/index.html" data-i18n="learn">Learn</a><a href="/about/index.html" data-i18n="about">About</a><a href="/challenge/index.html" data-i18n="challenge">Challenge</a></div>
<div><h4>Groups</h4>{catlinks}</div>
<div><h4>Project</h4><a href="/about/index.html">About Fasal</a><a href="/login/index.html">Sign in</a><a href="/challenge/index.html#faq">FAQ</a></div>
</div>
<div class="footer-bottom"><span>© <span data-year></span> Fasal field notes. An original demo project.</span><span>Made with soil under the nails.</span></div>
</div></footer>"""

def join_modal():
    return """<div class="modal-back" id="joinModal"><div class="modal" role="dialog" aria-modal="true">
<button class="x" aria-label="Close">×</button>
<div id="joinModalLoggedOut">
<h2 data-i18n="joinTitle">Welcome to Fasal</h2>
<p>Demo sign-in — your name is stored only in this browser.</p>
<form id="joinForm"><div class="field"><label data-i18n="name">Your name</label><input name="name" required maxlength="40" placeholder="Asha"></div>
<div class="field"><label data-i18n="email">Email address</label><input name="email" type="email" required placeholder="asha@example.org"></div>
<button class="btn btn-primary" style="width:100%;justify-content:center" data-i18n="create">Create profile</button></form>
</div>
<div id="joinModalLoggedIn" style="display:none">
<h2>Welcome back, <span class="user-name-display"></span>!</h2>
<p style="margin:14px 0 24px">You are currently signed in as <strong class="user-name-display"></strong>.</p>
<div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap">
<button class="btn btn-ghost" id="modalSignoutBtn">Sign out</button>
<button class="btn btn-primary" onclick="this.closest('.modal-back').classList.remove('open')">Close</button>
</div>
</div>
</div></div>"""

def scripts(extra='', base='.'):
    crops_json = json.dumps([{'slug':c['slug'],'name':c['name'],'hindi':c['hindi'],'binomial':c['binomial'],'hue':c['hue'],'motif':c['motif'],'cat':c['cat'],'uses':c['uses'],'grows':c['grows'],'care':c['care'],'tags':' '.join([c.get('tagline',''), c.get('desc','')] + c.get('uses',[]) + c.get('facts',[]))} for c in CROPS], ensure_ascii=False)
    return ('<script>window.FASAL_CROPS=' + crops_json + ';</script>'
            + f'<script>window.FASAL_BASE="{base}";</script>'
            + (('<script>window.FASAL_CURRENT='+extra+';</script>') if extra else '')
            + '<script src="/assets/js/app.js"></script>')

DEPTH_BASE = {0:'.', 1:'..', 2:'../..'}
def page(title, desc, active, body, extra='', depth=0):
    P = DEPTH_BASE[depth]
    h = head(title,desc)+'<body>'+header(active)+'<main>'+body+'</main>'+footer()+tabbar(active)+join_modal()+scripts(extra, P)+'</body></html>'
    # Relative URLs so the site works via file:// as well as any static server
    h = h.replace('href="/', f'href="{P}/').replace('src="/', f'src="{P}/')
    return h

def crop_card(c):
    return f"""<a class="crop-card" href="/crop/{c['slug']}/index.html">
<div class="crop-art" style="background:hsl({c['hue']},42%,90%)">{motif(c['motif'],c['hue'],104)}</div>
<div class="crop-body"><span class="pill-cat">{E(CAT[c['cat']]['name'])}</span>
<h3 data-name-en="{E(c['name'])}" data-name-hi="{E(c['hindi'])}">{E(c['name'])}</h3>
<div class="binomial">{E(c['binomial'])}</div><p>{E(c['tagline'])}</p></div></a>"""

def cat_card(c):
    n = len(BYCAT.get(c['slug'],[]))
    return f"""<a class="cat-card" href="/category/{c['slug']}/index.html">
<div class="cat-art" style="background:hsl({c['hue']},42%,90%)">{motif(c['motif'],c['hue'],88)}<span class="count-chip">{n} crops</span></div>
<div class="cat-body"><h3 data-name-en="{E(c['name'])}" data-name-hi="{E(c['hindi'])}">{E(c['name'])}</h3><p>{E(c['blurb'])}</p><span class="cat-link">Open group →</span></div></a>"""

def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full,'w',encoding='utf-8').write(content)
    print('wrote', path)

# ---------- Homepage ----------
def build_index():
    featured = [CROPS[i] for i in (0, 13, 21, 27, 33, 36)]  # wheat, tomato, mango, turmeric, marigold, neem
    body = f"""<section class="hero"><div class="wrap hero-grid">
<div>
<span class="kicker">A field notebook · {len(CROPS)} crops</span>
<h1>Know the crops <em>behind</em> everyday life.</h1>
<p class="lede">Fasal is a friendly visual library for the curious. Start with the food on your plate, then follow its story back to seed, soil and season.</p>
<div class="search-block"><label data-i18n="searchLabel">What are you curious about?</label>
<div class="search-row"><input id="q" data-i18n-ph="searchPh" placeholder="Search for a crop, plant, or fun fact..." autocomplete="off"><button class="btn btn-primary" data-i18n="searchBtn">Search</button></div>
<div class="search-results" id="sr"></div></div>
</div>
<div class="hero-img"><img src="/assets/img/hero.jpg" alt="Sunlit crop field at dawn">
<div class="hero-stat"><div><b>{len(CROPS)}</b><span>field notes</span></div><div><b>13</b><span>crop groups</span></div><div><b>2</b><span>languages</span></div></div></div>
</div></section>
<section><div class="wrap">
<span class="kicker" data-i18n="explore">Explore crop groups</span>
<h2>Thirteen ways to sort a harvest</h2>
<p class="lede">From cereals to ornamentals — pick a group and wander.</p>
<div class="cat-grid">{''.join(cat_card(c) for c in CATS)}</div>
</div></section>
<section><div class="wrap">
<div class="more-row"><div><span class="kicker">Editor's picks</span><h2>Start with these</h2></div>
<a class="btn btn-ghost" href="/learn/index.html" data-i18n="allCrops">Browse all crops</a></div>
<div class="crop-grid">{''.join(crop_card(c) for c in featured)}</div>
<div class="cta-band"><img src="/assets/img/cta.jpg" alt="">
<div class="cta-inner"><h2 data-i18n="ctaH">Start exploring nature today.</h2>
<p data-i18n="ctaP">From seed to plate — field notes and counting.</p>
<a class="btn btn-leaf" href="/learn/index.html" data-i18n="ctaBtn">Open the field notebook</a></div></div>
</div></section>"""
    return page('Grow with nature', SITE['tagline'], 'home', body)

# ---------- Learn ----------
def build_learn():
    letters = ['ALL'] + [chr(a) for a in range(65,91)]
    bar = ''.join(f'<button data-letter="{L}" class="{"on" if L=="ALL" else ""}">{L}</button>' for L in letters)
    cards = []
    for c in sorted(CROPS, key=lambda x: x['name']):
        tag_str = E(f"{c['hindi']} {c['binomial']} {c.get('tagline','')} {' '.join(c.get('uses',[]))}")
        cards.append(f"""<div class="crop-card" data-name="{E(c['name'])}" data-tags="{tag_str}">
<a href="/crop/{c['slug']}/index.html" style="color:inherit"><div class="crop-art" style="background:hsl({c['hue']},42%,90%)">{motif(c['motif'],c['hue'],80)}</div>
<div class="crop-body"><span class="pill-cat">{E(CAT[c['cat']]['name'])}</span>
<h3 data-name-en="{E(c['name'])}" data-name-hi="{E(c['hindi'])}">{E(c['name'])}</h3>
<div class="binomial">{E(c['binomial'])}</div></div></a></div>""")
    body = f"""<section><div class="wrap">
<span class="kicker">The library</span><h1>Learn the crops</h1>
<p class="lede">Every field note in one place. Filter by letter or search as you type.</p>
<div class="search-block" style="margin-top:24px"><div class="search-row"><input id="q2" placeholder="Filter crops..." autocomplete="off"><button class="btn btn-primary">Filter</button></div></div>
<div class="az-bar" id="azBar">{bar}</div>
<p class="learn-count" id="azCount"></p>
<div class="crop-grid" id="azGrid">{''.join(cards)}</div>
</div></section>"""
    return page('Learn about crops', 'Browse all field notes A to Z.', 'learn', body, depth=1)

# ---------- Category ----------
def build_category(cat):
    crops = BYCAT.get(cat['slug'], [])
    body = f"""<section style="padding-bottom:0"><div class="wrap cat-hero">
<div><a href="/learn/index.html" style="font-weight:700">← <span data-i18n="back">Back to groups</span></a>
<h1 style="margin:14px 0" data-name-en="{E(cat['name'])}" data-name-hi="{E(cat['hindi'])}">{E(cat['name'])}</h1>
<p class="lede">{E(cat['blurb'])}</p>
<p style="margin-top:16px"><span class="count-chip" style="position:static">{len(crops)} <span data-i18n="crops">crops</span></span></p></div>
<div class="cat-hero-art" style="background:hsl({cat['hue']},42%,90%)">{motif(cat['motif'],cat['hue'],150)}</div>
</div></section>
<section><div class="wrap"><div class="crop-grid">{''.join(crop_card(c) for c in crops)}</div></div></section>"""
    return page(cat['name'], cat['blurb'], 'learn', body, depth=2)

# ---------- Crop detail ----------
STRUCT_LABELS = {
 'grain':[('Head','where the grains ripen'),('Leaf','catches the sunlight'),('Stem','holds the plant tall'),('Roots','drink from the soil')],
 'pod':[('Pod','the protective case'),('Seeds','the harvest inside'),('Leaf','feeds the plant'),('Stem','carries nutrients')],
 'flower':[('Petals','advertise to pollinators'),('Stamen','makes the pollen'),('Leaf','the food factory'),('Stem','the support')],
 'fruit':[('Fruit','protects the seeds'),('Leaf','photosynthesis'),('Branch','bears the weight'),('Roots','anchor and absorb')],
 'leaf':[('Blade','the flat green surface'),('Veins','plumbing of the leaf'),('Petiole','the leaf stalk'),('Stem','main axis')],
 'root':[('Shoot','the green top'),('Storage root','the edible swelling'),('Lateral roots','spread wide'),('Root tip','grows downward')],
 'grass':[('Blade','long narrow leaf'),('Culm','the hollow stem'),('Node','where leaves join'),('Roots','fibrous mat')],
 'tree':[('Canopy','the leafy crown'),('Trunk','the woody column'),('Branches','reach for light'),('Roots','deep anchors')],
 'bulb':[('Leaves','green and upright'),('Tunic','papery coat'),('Basal plate','the growing base'),('Roots','fine feeders')],
}
def struct_diagram(c):
    labels = STRUCT_LABELS.get(c['motif'], STRUCT_LABELS['leaf'])
    hue = c['hue']; P=f'hsl({hue},48%,52%)'; D=f'hsl({hue},45%,34%)'; T=f'hsl({hue},38%,86%)'
    svg = f"""<svg viewBox="0 0 200 260" aria-hidden="true">
<circle cx="100" cy="52" r="10" fill="{P}"/><circle cx="100" cy="112" r="10" fill="{P}"/>
<circle cx="100" cy="168" r="10" fill="{P}"/><circle cx="100" cy="222" r="10" fill="{P}"/>
<text x="100" y="57" text-anchor="middle" font-size="12" fill="#fff" font-weight="bold">1</text>
<text x="100" y="117" text-anchor="middle" font-size="12" fill="#fff" font-weight="bold">2</text>
<text x="100" y="173" text-anchor="middle" font-size="12" fill="#fff" font-weight="bold">3</text>
<text x="100" y="227" text-anchor="middle" font-size="12" fill="#fff" font-weight="bold">4</text>
<path d="M100 20v220" stroke="{D}" stroke-width="4"/>
<path d="M100 90c-24-6-36-20-40-38M100 140c24-6 36-20 40-38" stroke="{D}" stroke-width="3" fill="none"/>
<path d="M100 240c-10 8-14 14-16 18M100 240c10 8 14 14 16 18" stroke="{D}" stroke-width="3" fill="none"/></svg>"""
    items = ''.join(f'<li><b>{E(a)}</b><span>{E(b)}</span></li>' for a,b in labels)
    return f'<div class="struct-diagram">{svg}<ul class="struct-labels">{items}</ul></div>'

def build_crop(c):
    cat = CAT[c['cat']]
    others = [x for x in BYCAT[c['cat']] if x['slug']!=c['slug']]
    more = others[:3]
    def lis(items): return ''.join(f'<li>{E(i)}</li>' for i in items)
    slides = [
        (f'hsl({c["hue"]},42%,90%)','Botanical portrait'),
        (f'hsl({c["hue"]},30%,78%)','Field sketch'),
        ('var(--cream-deep)','Pattern study'),
    ]
    car = ''.join(f'<div class="car-slide" style="position:absolute;inset:0;display:grid;place-items:center;background:{bg}">{motif(c["motif"],c["hue"],200)}<span class="car-cap">{cap}</span></div>' for bg,cap in slides)
    dots = ''.join('<i></i>' for _ in slides)
    opts = ''.join(f'<option value="{x["slug"]}">{E(x["name"])}</option>' for x in others)
    body = f"""<div class="wrap" data-tabs>
<section class="crop-hero" style="padding-bottom:0"><div class="crop-titleblock">
<a href="/category/{cat['slug']}/index.html" style="font-weight:700">← FIELD NOTE ON: {E(cat['name']).upper()}</a>
<div class="lang-toggle"><button data-lang="en" class="on">English</button><button data-lang="hi">अ</button></div>
<div class="binomial">{E(c['binomial'])}</div>
<h1 data-name-en="{E(c['name'])}" data-name-hi="{E(c['hindi'])}">{E(c['name'])}</h1>
<p class="lede" data-tag-en="{E(c['tagline'])}" data-tag-hi="{E(c['tagline_hi'])}">{E(c['tagline'])}</p>
</div>
<aside class="fact-rail"><h4>Quick facts</h4>
<div class="fact-row"><span>Group</span><b>{E(cat['name'])}</b></div>
<div class="fact-row"><span>Botanical name</span><b style="font-style:italic">{E(c['binomial'])}</b></div>
<div class="fact-row"><span>Hindi</span><b>{E(c['hindi'])}</b></div>
<div class="fact-row"><span>Field note</span><b>#{CROPS.index(c)+1:02d}</b></div></aside>
</section>
<div class="tabs">
<button class="tab on" data-tab="info" data-i18n="info">Info</button>
<button class="tab" data-tab="structure" data-i18n="structure">Structure</button>
<button class="tab" data-tab="compare" data-i18n="compare">Compare</button>
<button class="tab" data-tab="pdf" data-i18n="pdf">PDF</button></div>
<div class="tabpane on" id="pane-info">
<div class="carousel"><div class="car-view" style="position:relative">{car}</div>
<div class="car-nav"><div class="car-btns"><button class="car-btn car-prev" aria-label="Previous">‹</button><button class="car-btn car-next" aria-label="Next">›</button></div><span class="car-count"></span><div class="car-dots">{dots}</div></div></div>
<div class="info-section"><h3><span class="info-num">01</span><span data-i18n="aboutPlant">About this plant</span></h3><p>{E(c['desc'])}</p></div>
<div class="info-section"><h3><span class="info-num">02</span><span data-i18n="uses">Uses</span></h3><ul class="tick-list">{lis(c['uses'])}</ul></div>
<div class="info-section"><h3><span class="info-num">03</span><span data-i18n="grows">Where it grows</span></h3><ul class="tick-list">{lis(c['grows'])}</ul></div>
<div class="info-section"><h3><span class="info-num">04</span><span data-i18n="care">Plant care</span></h3><ul class="tick-list">{lis(c['care'])}</ul></div>
<div class="info-section"><h3><span class="info-num">05</span><span data-i18n="facts">Interesting facts</span></h3><ul class="tick-list">{lis(c['facts'])}</ul></div>
</div>
<div class="tabpane" id="pane-structure"><div class="info-section"><h3><span class="info-num">✿</span><span data-i18n="structure">Structure</span></h3><p class="lede">Anatomy of the plant, labelled.</p>{struct_diagram(c)}</div></div>
<div class="tabpane" id="pane-compare"><div class="info-section"><h3><span class="info-num">⇄</span><span data-i18n="compare">Compare</span></h3>
<p class="lede" data-i18n="pickCompare">Pick a crop to compare with</p>
<select class="compare-select"><option value="">— {E(cat['name'])} —</option>{opts}</select>
<div id="compareOut"></div></div></div>
<div class="tabpane" id="pane-pdf"><div class="info-section"><h3><span class="info-num">⤓</span><span data-i18n="pdf">PDF</span></h3>
<p class="lede">Print this field note to PDF for your classroom wall.</p>
<p style="margin:18px 0"><button class="btn btn-primary" onclick="window.print()">Print / Save as PDF</button></p>
<p style="color:var(--muted);font-size:.9rem">Tip: choose “Save as PDF” in your browser's print dialog.</p></div></div>
</div>
<section><div class="wrap">
<div class="more-row"><h2><span data-i18n="moreIn">More in</span> {E(cat['name'])}</h2><a class="btn btn-ghost" href="/learn/index.html" data-i18n="allCrops">Browse all crops</a></div>
<div class="crop-grid">{''.join(crop_card(x) for x in more)}</div>
</div></section>"""
    cur = json.dumps({'slug':c['slug'],'name':c['name'],'hindi':c['hindi'],'binomial':c['binomial'],'hue':c['hue'],'motif':c['motif'],'uses':c['uses'],'grows':c['grows'],'care':c['care']}, ensure_ascii=False)
    return page(f"{c['name']} ({c['binomial']})", c['tagline'], 'learn', body, cur, depth=2)

# ---------- About ----------
def build_about():
    stats = [('39','field notes'),('13','crop groups'),('2','languages'),('9','art motifs')]
    powers = [('📝','Field notes','Concise, classroom-ready notes: uses, growing needs, care and curious facts.'),
              ('🎨','Visual system','Nine original botanical motifs, one warm palette, zero stock photos on crop cards.'),
              ('🌐','Bilingual','Interface and crop names in English and Hindi, with a one-tap toggle.'),
              ('🏆','Challenge','A photo challenge with points, leaderboard and rules to keep exploring.')]
    body = f"""<section><div class="wrap">
<span class="kicker">About Fasal</span>
<h1>Growing curiosity about the plants that feed us.</h1>
<p class="lede" style="margin-top:16px">Fasal is an original demo project: a small, hand-built library of crop field notes. Every word and illustration here was made for this site — nothing copied, nothing scraped.</p>
<div class="stat-grid">{''.join(f'<div class="stat"><b>{n}</b><span>{l}</span></div>' for n,l in stats)}</div>
</div></section>
<section><div class="wrap split">
<img src="/assets/img/about.jpg" alt="Hands holding a young seedling">
<div><span class="kicker">Why it exists</span><h2>From plate back to seed</h2>
<p class="lede">Most of us meet crops as groceries. Fasal traces them backwards — the flower before the fruit, the field before the flower, the seed before the field — so everyday food becomes a story worth knowing.</p></div>
</div></section>
<section><div class="wrap">
<span class="kicker">Under the hood</span><h2>What powers the notebook</h2>
<div class="power-grid">{''.join(f'<div class="power-card"><div class="pi">{i}</div><h3>{t}</h3><p>{d}</p></div>' for i,t,d in powers)}</div>
<div class="band"><h2>Open learning, by design</h2><p>Static files, no tracking, no accounts that matter. Copy the field notes for your classroom — that is what they are for.</p></div>
</div></section>"""
    return page('About', 'Why Fasal exists and how it is built.', 'about', body, depth=1)

# ---------- Challenge (dark sub-site) ----------
def build_challenge():
    how = [('01','Wander','Walk fields, gardens and markets with your eyes open.'),
           ('02','Photograph','Capture ten different photos of the same crop.'),
           ('03','Get recognised','Climb the leaderboard and earn your explorer badge.')]
    leaders = [('Asha V.',128),('Rohan K.',114),('Meera S.',97),('Arjun P.',82),('Kavya R.',66),('Dev M.',51)]
    rules = [('R-01','Photos must be your own, taken during the challenge.'),
             ('R-02','Ten different photos of the same crop earn one point.'),
             ('R-03','No two photos may show the same individual plant.'),
             ('R-04','Cultivated and wild plants both count.'),
             ('R-05','Do not trespass or damage crops while photographing.'),
             ('R-06','The jury’s identification is final.')]
    faqs = [('Q-01','Do I need a fancy camera?','No. Any phone camera works — observation matters more than megapixels.'),
            ('Q-02','Can children take part?','Yes, with a guardian. There is a separate junior leaderboard.'),
            ('Q-03','When does the challenge run?','Dates are announced on this page. The demo leaderboard below is illustrative.'),
            ('Q-04','What counts as “the same crop”?','Same species — ten mango photos from ten trees, for example.'),
            ('Q-05','Is there a prize?','Recognition, a printed field certificate, and serious bragging rights.'),
            ('Q-06','Where do I submit photos?','Submissions open when the challenge goes live. This demo build does not collect photos.')]
    lb = ''.join(f'<tr><td>#{i+1}</td><td>{E(n)}</td><td>{p} pts</td></tr>' for i,(n,p) in enumerate(leaders))
    body = f"""<section class="challenge-hero"><div class="wrap">
<div><span class="ch-pill">FASAL · PLANT DISCOVERY CHALLENGE</span><span class="ch-pill">● DATES TO BE ANNOUNCED</span></div>
<h1 style="margin-top:20px">Discover plants.<br>Explore nature.<br><em style="color:var(--gold)">Earn recognition.</em></h1>
<p class="lede">Ten different photos of the same crop earn one point. How many crops can you document?</p>
<p style="margin-top:28px"><button class="btn btn-primary" data-open-modal="joinModal" style="background:var(--gold);color:#241a10;box-shadow:0 8px 20px rgba(233,164,38,.35)">Join the challenge</button>
<a class="btn btn-ghost" href="#leaderboard" style="color:#fff;border-color:rgba(255,255,255,.3);margin-left:10px">View leaderboard</a></p>
<img class="orb" src="/assets/img/challenge.jpg" alt="Greenhouse at night">
</div></section>
<section><div class="wrap"><span class="kicker" style="background:rgba(233,164,38,.15);color:var(--gold)" data-i18n="howH">How it works</span>
<div class="how-grid">{''.join(f'<div class="how-card"><div class="hn">{n}</div><h3>{t}</h3><p>{d}</p></div>' for n,t,d in how)}</div></div></section>
<section><div class="wrap"><h2 data-i18n="pointsH">Your explorer points</h2><p class="lede" data-points-note></p></div></section>
<section id="leaderboard"><div class="wrap"><h2 data-i18n="lbH">Top explorers</h2>
<table class="lb-table"><tr><th>Rank</th><th>Explorer</th><th>Points</th></tr>{lb}</table></div></section>
<section><div class="wrap"><h2 data-i18n="rulesH">Challenge rules</h2>
<div style="margin-top:20px">{''.join(f'<div class="rule"><b>{r}</b><span>{d}</span></div>' for r,d in rules)}</div></div></section>
<section id="faq"><div class="wrap"><h2 data-i18n="faqH">Questions, answered</h2>
<div class="faq">{''.join(f'<div class="faq-item"><button class="faq-q">{q}<span class="chev">▾</span></button><div class="faq-a">{a}</div></div>' for q,_,a in faqs)}</div></div></section>
<section><div class="wrap" style="text-align:center;padding-bottom:40px">
<h2>Your next discovery awaits.</h2>
<p><button class="btn btn-primary" data-open-modal="joinModal" style="background:var(--gold);color:#241a10;margin-top:20px">Join the challenge</button></p></div></section>"""
    html_out = page('Plant discovery challenge', 'Photograph crops, earn points, climb the leaderboard.', 'challenge', body, depth=1)
    return html_out.replace('<body>', '<body class="challenge">', 1)

# ---------- Login ----------
def build_login():
    body = """<div class="login-wrap"><div class="login-card">
<div class="brand" style="justify-content:center;margin-bottom:18px"><span class="brand-mark">🌱</span><span>Fasal</span></div>
<div id="loginLoggedOut">
<h2>Welcome back</h2><p style="color:var(--muted);margin:8px 0 24px">Demo sign-in — stored only in this browser.</p>
<form id="loginPageForm"><div class="field"><label data-i18n="name">Your name</label><input name="name" required maxlength="40" placeholder="Asha"></div>
<div class="field"><label data-i18n="email">Email address</label><input name="email" type="email" required placeholder="asha@example.org"></div>
<button class="btn btn-primary" style="width:100%;justify-content:center" data-i18n="signin">Sign in</button></form>
<p style="margin-top:18px;font-size:.85rem;color:var(--muted)">No password, no server, no tracking. This is a front-end demo.</p>
</div>
<div id="loginLoggedIn" style="display:none">
<h2>Welcome back, <span class="user-name-display"></span>!</h2>
<p style="color:var(--muted);margin:12px 0 24px">You are currently signed in as <strong class="user-name-display"></strong>.</p>
<div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap">
<a class="btn btn-primary" href="/index.html">Go to Home</a>
<a class="btn btn-ghost" href="/challenge/index.html">View Challenge</a>
<button class="btn btn-ghost" id="pageSignoutBtn">Sign out</button>
</div>
</div>
</div></div>"""
    return page('Sign in', 'Demo sign-in for Fasal.', 'login', body, depth=1)

# ---------- Sitemap / robots ----------
def build_sitemap():
    urls = ['/', '/learn/', '/about/', '/challenge/', '/login/']
    urls += [f"/category/{c['slug']}/" for c in CATS]
    urls += [f"/crop/{c['slug']}/" for c in CROPS]
    items = ''.join(f'<url><loc>https://example.org{u}</loc></url>' for u in urls)
    write('sitemap.xml', f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{items}</urlset>')
    write('robots.txt', 'User-agent: *\nAllow: /\nSitemap: https://example.org/sitemap.xml\n')

# ---------- Main ----------
def main():
    for src, dst in [('src/css/style.css','assets/css/style.css'),('src/js/app.js','assets/js/app.js')]:
        os.makedirs(os.path.join(ROOT, os.path.dirname(dst)), exist_ok=True)
        shutil.copy(os.path.join(ROOT, src), os.path.join(ROOT, dst))
        print('copied', dst)
    write('index.html', build_index())
    write('learn/index.html', build_learn())
    write('about/index.html', build_about())
    write('challenge/index.html', build_challenge())
    write('login/index.html', build_login())
    for c in CATS:
        write(f"category/{c['slug']}/index.html", build_category(c))
    for c in CROPS:
        write(f"crop/{c['slug']}/index.html", build_crop(c))
    build_sitemap()
    print(f'DONE: {2+3+len(CATS)+len(CROPS)} pages')

if __name__ == '__main__':
    main()
