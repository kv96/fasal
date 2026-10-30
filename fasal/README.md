# Fasal — Field notes on the crops behind everyday life

An **original** crop-library demo website: 39 hand-written crop field notes across
13 crop groups, with live search, an A–Z explorer, tabbed crop detail pages
(info / structure diagram / compare tool / print-to-PDF), an English↔Hindi
interface toggle, a dark-themed discovery challenge page, and a mobile bottom
tab bar. Inspired by the *structure* of crop-library sites, but every word,
illustration and design token here is original.

## Quick start

No dependencies — pure Python 3 standard library for the build, plain
HTML/CSS/JS output.

```bash
# 1. Build the site (reads data/crops.json, writes 57 pages)
python3 tools/build.py

# 2. Serve it locally
python3 -m http.server 8000

# 3. Open http://localhost:8000/
```

Any static file server works (nginx, `npx serve`, GitHub Pages, Netlify Drop).
You can also just double-click `index.html` — all links and assets use relative
paths, so the site works straight from the file system too.

## Project structure

```
fasal/
├── data/crops.json        # All content: 13 categories + 39 crops (edit, then rebuild)
├── tools/build.py         # Static-site generator (stdlib only)
├── src/
│   ├── css/style.css      # Design system + all component styles
│   └── js/app.js          # Search, tabs, carousel, i18n toggle, accordion, modal, compare
├── assets/
│   ├── img/               # Original AI-generated photography (hero, about, challenge, cta)
│   └── fonts/             # Self-hosted variable fonts (Fraunces + Inter, OFL license)
├── index.html             # Generated: homepage
├── learn/                 # Generated: A–Z explorer with live filter
├── category/<slug>/       # Generated: 13 group pages
├── crop/<slug>/           # Generated: 39 detail pages
├── about/  challenge/  login/
├── sitemap.xml  robots.txt
└── qa/                    # Build verification screenshots (not part of the site)
```

## Design tokens

| Token | Value |
|---|---|
| Brand (terracotta) | `#B5542C` / hover `#8F3F1F` |
| Ink (bark) | `#3E2F23` |
| Leaf accent | `#6A994E` |
| Gold accent | `#E9A426` |
| Background (cream) | `#FAF5EA` |
| Display type | Fraunces (self-hosted) |
| Body type | Inter (self-hosted) |

Crop and category artwork is an original duotone SVG botanical system
(`motif()` in `build.py` / `motifSVG()` in `app.js`) — nine motifs
(grain, pod, flower, fruit, leaf, root, grass, tree, bulb), hue-parameterised
per crop. No stock imagery on cards.

## Features

- Live search with dropdown results (homepage + Learn page)
- Crop detail: tabbed Info / Structure (labelled SVG diagram) / Compare
  (side-by-side vs another crop in the group) / PDF (print-to-PDF)
- Photo-style carousel per crop (3 botanical plates, arrows + dots + counter)
- EN ⇄ HI toggle: full UI chrome + crop names/taglines switch to Hindi
  (persisted in localStorage)
- Challenge sub-site: dark theme, how-it-works, points gate, leaderboard,
  rules, FAQ accordion, sign-in modal
- Demo sign-in (front-end only, localStorage — no backend)
- Responsive: 4→2→1 column grids, mobile bottom tab bar under 760px,
  `prefers-reduced-motion` respected

## Honest limitations

- **39 crops, not 400+.** The dataset is a hand-written sample; extend
  `data/crops.json` and rebuild to grow it.
- **Hindi is partial.** UI chrome, crop names, taglines and headings are
  translated; long-form descriptions remain English.
- **Auth is a demo.** Sign-in stores a name in localStorage only.
- **PDF = browser print.** The PDF tab triggers `window.print()`; use
  “Save as PDF” in the print dialog.
- **Leaderboard is illustrative** sample data.
- Fonts are self-hosted OFL-licensed files from Google Fonts; photographic
  assets were generated for this project.

## Rebuilding

Edit `data/crops.json`, `src/css/style.css` or `src/js/app.js`, then run
`python3 tools/build.py` again. Generated HTML is committed alongside source
so the site works straight from the folder.
