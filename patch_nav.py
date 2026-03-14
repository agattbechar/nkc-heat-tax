"""
patch_nav.py — inject mobile hamburger nav into all 14 pages.
Run from project root: python patch_nav.py
"""

import os, re

FR_LINKS = [
    ("La Courbe",   "curve.html"),
    ("Compression", "compression.html"),
    ("Prime AC",    "premium.html"),
    ("Production",  "shadow.html"),
    ("Methode",     "methodology.html"),
    ("Donnees",     "data.html"),
]

EN_LINKS = [
    ("The Curve",   "curve.html"),
    ("Compression", "compression.html"),
    ("AC Premium",  "premium.html"),
    ("Output",      "shadow.html"),
    ("Method",      "methodology.html"),
    ("Data",        "data.html"),
]

ALL_PAGES = {
    "site/index.html":          {"active": None,          "lang_href": "en/index.html",       "lang": "EN", "links": FR_LINKS},
    "site/curve.html":          {"active": "La Courbe",   "lang_href": "en/curve.html",       "lang": "EN", "links": FR_LINKS},
    "site/compression.html":    {"active": "Compression", "lang_href": "en/compression.html", "lang": "EN", "links": FR_LINKS},
    "site/premium.html":        {"active": "Prime AC",    "lang_href": "en/premium.html",     "lang": "EN", "links": FR_LINKS},
    "site/shadow.html":         {"active": "Production",  "lang_href": "en/shadow.html",      "lang": "EN", "links": FR_LINKS},
    "site/methodology.html":    {"active": "Methode",     "lang_href": "en/methodology.html", "lang": "EN", "links": FR_LINKS},
    "site/data.html":           {"active": "Donnees",     "lang_href": "en/data.html",        "lang": "EN", "links": FR_LINKS},
    "site/en/index.html":       {"active": None,          "lang_href": "../index.html",       "lang": "FR", "links": EN_LINKS},
    "site/en/curve.html":       {"active": "The Curve",   "lang_href": "../curve.html",       "lang": "FR", "links": EN_LINKS},
    "site/en/compression.html": {"active": "Compression", "lang_href": "../compression.html", "lang": "FR", "links": EN_LINKS},
    "site/en/premium.html":     {"active": "AC Premium",  "lang_href": "../premium.html",     "lang": "FR", "links": EN_LINKS},
    "site/en/shadow.html":      {"active": "Output",      "lang_href": "../shadow.html",      "lang": "FR", "links": EN_LINKS},
    "site/en/methodology.html": {"active": "Method",      "lang_href": "../methodology.html", "lang": "FR", "links": EN_LINKS},
    "site/en/data.html":        {"active": "Data",        "lang_href": "../data.html",        "lang": "FR", "links": EN_LINKS},
}

BURGER_CSS = """
    .nav-burger {
      display: none; flex-direction: column; justify-content: center;
      gap: 5px; width: 32px; height: 32px;
      background: none; border: none; cursor: pointer; padding: 4px;
      z-index: 201; flex-shrink: 0;
    }
    .nav-burger span {
      display: block; width: 100%; height: 1px;
      background: var(--text-mid);
      transition: all .25s cubic-bezier(.16,1,.3,1);
      transform-origin: center;
    }
    .nav-burger.open span:nth-child(1) { transform: translateY(6px) rotate(45deg); background: var(--amber); }
    .nav-burger.open span:nth-child(2) { opacity: 0; transform: scaleX(0); }
    .nav-burger.open span:nth-child(3) { transform: translateY(-6px) rotate(-45deg); background: var(--amber); }
    .nav-drawer {
      display: none; position: fixed;
      top: 52px; left: 0; right: 0;
      background: rgba(10,13,20,0.98);
      backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--border);
      z-index: 199; padding: 1.5rem;
      opacity: 0; transform: translateY(-8px);
      transition: all .25s cubic-bezier(.16,1,.3,1);
      pointer-events: none;
    }
    .nav-drawer.open { opacity: 1; transform: translateY(0); pointer-events: all; }
    .nav-drawer ul { list-style: none; margin-bottom: 1.2rem; }
    .nav-drawer ul li { border-bottom: 1px solid var(--border); }
    .nav-drawer ul li:last-child { border-bottom: none; }
    .nav-drawer ul a {
      font-family: 'DM Mono', monospace;
      font-size: 11px; letter-spacing: .12em; text-transform: uppercase;
      color: var(--text-mid); text-decoration: none;
      display: block; padding: 1rem 0; transition: color .2s;
    }
    .nav-drawer ul a:hover, .nav-drawer ul a.active { color: var(--amber); }
    .nav-drawer-lang {
      font-family: 'DM Mono', monospace;
      font-size: 10px; letter-spacing: .12em; text-transform: uppercase;
      color: var(--text-dim); text-decoration: none;
      border: 1px solid var(--border); padding: 6px 14px;
      display: inline-block; transition: all .2s;
    }
    .nav-drawer-lang:hover { color: var(--amber); border-color: var(--amber-muted); }
    @media (max-width: 640px) {
      .nav-burger { display: flex !important; }
      .nav-drawer { display: block !important; }
      .nav-lang   { display: none !important; }
      .nav-links  { display: none !important; }
    }
"""

BURGER_BTN = '<button class="nav-burger" id="nav-burger" aria-label="Menu"><span></span><span></span><span></span></button>'

BURGER_JS = """<script>
(function(){
  var b=document.getElementById('nav-burger');
  var d=document.getElementById('nav-drawer');
  if(!b||!d)return;
  b.addEventListener('click',function(){b.classList.toggle('open');d.classList.toggle('open');});
  d.querySelectorAll('a').forEach(function(a){
    a.addEventListener('click',function(){b.classList.remove('open');d.classList.remove('open');});
  });
})();
</script>"""

def make_drawer(links, active, lang_href, lang):
    items = ""
    for label, href in links:
        cls = ' class="active"' if label == active else ""
        items += f'  <li><a href="{href}"{cls}>{label}</a></li>\n'
    return (
        f'\n<div class="nav-drawer" id="nav-drawer">\n'
        f'<ul>\n{items}</ul>\n'
        f'<a class="nav-drawer-lang" href="{lang_href}">{lang} &rarr;</a>\n'
        f'</div>\n'
    )

def patch(path, active, lang_href, lang, links):
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # Check if already patched (look for the specific button ID)
    if 'id="nav-burger"' in html:
        print(f"SKIP {path} (already patched)")
        return

    # 1. inject CSS
    if ".nav-burger {" not in html:
        html = html.replace("</style>", BURGER_CSS + "\n  </style>", 1)

    # 2. add burger button inside nav (before </nav>)
    html = html.replace("</nav>", BURGER_BTN + "\n</nav>", 1)

    # 3. add drawer div right after </nav>
    drawer = make_drawer(links, active, lang_href, lang)
    html = html.replace("</nav>", "</nav>" + drawer, 1)

    # 4. inject JS before </body>
    if 'id="nav-burger"' not in html or BURGER_JS not in html:
        html = html.replace("</body>", BURGER_JS + "\n</body>")

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"OK  {path}")

base = os.path.dirname(os.path.abspath(__file__))
for rel, cfg in ALL_PAGES.items():
    patch(os.path.join(base, rel), cfg["active"], cfg["lang_href"], cfg["lang"], cfg["links"])

print("\nDone. git add site/ && git commit -m 'mobile nav' && git push")