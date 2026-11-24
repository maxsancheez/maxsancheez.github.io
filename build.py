#!/usr/bin/env python3
"""Build index.html from projects.json. Standard library only.

    python3 art.py     # (re)draw banners and experience images into images/
    python3 build.py   # write index.html

Tabs are plain sections; a small script turns them into tabs and opens each
card's detail panel. Links like /#research open that tab directly. Without
JavaScript every section shows, one after another. Mark one project per
section with "featured": true to show it as the wide card at the top.
"""
import hashlib
import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
GH = "https://github.com/maxsancheez/"

CSS = """
/* Layout: bone page, ink type, one orange. Hero with a facts strip, sticky tabs,
   featured work as a wide split card above the grid. */
:root{
  --bg:#F5EFE3; --surface:#FFFBF4; --ink:#1F1A14; --muted:#6A5F53; --line:#E3D8C6;
  --accent:#E8620C; --accent-soft:#F8CFAE; --accent-ink:#B04A07; --art-bg:#EDE3D1;
  --shadow:0 1px 2px rgba(60,40,20,.05),0 10px 30px rgba(60,40,20,.07);
  --display:"Bricolage Grotesque","Inter",system-ui,sans-serif;
  --body:"Inter",system-ui,-apple-system,"Segoe UI",sans-serif;
  color-scheme:light;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --bg:#16120E; --surface:#1F1A15; --ink:#F2EBDF; --muted:#B5A999; --line:#33291F;
  --accent:#FF8A3D; --accent-soft:#5A3218; --accent-ink:#FFA066; --art-bg:#221B15;
  --shadow:none; color-scheme:dark}}
:root[data-theme="dark"]{
  --bg:#16120E; --surface:#1F1A15; --ink:#F2EBDF; --muted:#B5A999; --line:#33291F;
  --accent:#FF8A3D; --accent-soft:#5A3218; --accent-ink:#FFA066; --art-bg:#221B15;
  --shadow:none; color-scheme:dark}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{transition:none!important}}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.65 var(--body)}
a{color:inherit}
h1,h2,h3{font-family:var(--display);text-wrap:balance;letter-spacing:-.02em}
.wrap{max-width:1080px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}

/* hero */
.hero{display:grid;grid-template-columns:auto 1fr;gap:36px;align-items:start;padding-block:64px 28px}
.mono{width:128px;height:128px;border-radius:50%;background:var(--accent);color:var(--ink);display:grid;place-items:center;font:800 2.9rem/1 var(--display);letter-spacing:-.04em;overflow:hidden}
.mono img{width:100%;height:100%;object-fit:cover}
.hero h1{font-size:clamp(2.2rem,5vw,3.6rem);line-height:1.02;margin:0 0 10px;font-weight:800}
.hero h1 .nick{color:var(--accent-ink)}
.headline{font:600 1.15rem/1.4 var(--display);margin:0 0 12px}
.pitch{color:var(--muted);font-size:1.06rem;max-width:62ch;margin:0 0 18px}
.open{display:inline-block;background:var(--accent-soft);border-radius:10px;padding:8px 14px;font-weight:600;font-size:.95rem;margin:0 0 20px;max-width:100%}
.cta{display:flex;flex-wrap:wrap;gap:10px}
.btn{display:inline-flex;align-items:center;gap:8px;padding:10px 18px;border-radius:10px;border:1.5px solid var(--ink);text-decoration:none;font-weight:700;font-size:.95rem;background:transparent;color:var(--ink);font-family:var(--body);cursor:pointer}
.btn.primary{background:var(--accent);border-color:var(--accent);color:#1F1A14}
.btn:hover{transform:translateY(-1px)}
.btn:focus-visible,.card:focus-visible,.row:focus-visible,[role=tab]:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
.facts{display:grid;grid-template-columns:repeat(4,1fr);border-top:1.5px solid var(--ink);border-bottom:1px solid var(--line);margin:8px 0 0;padding:0}
.facts div{padding:12px 14px 12px 0}
.facts dt{font-size:.72rem;text-transform:uppercase;letter-spacing:.09em;color:var(--muted);margin:0}
.facts dd{margin:2px 0 0;font:700 1.05rem/1.3 var(--display)}

/* tabs */
nav[role=tablist]{position:sticky;top:0;z-index:5;background:var(--bg);display:flex;gap:2px;overflow-x:auto;scrollbar-width:none;border-bottom:1px solid var(--line);margin-top:28px}
nav[role=tablist]::-webkit-scrollbar{display:none}
[role=tab]{appearance:none;background:none;border:0;border-bottom:3px solid transparent;color:var(--muted);font:600 1rem var(--body);padding:15px 14px 12px;cursor:pointer;white-space:nowrap}
[role=tab]:hover{color:var(--ink)}
[role=tab][aria-selected=true]{color:var(--ink);border-bottom-color:var(--accent)}
.panel{padding-block:30px 64px}
.js .panel[hidden]{display:none}
.banner{border-radius:18px;overflow:hidden;aspect-ratio:10/3;margin-bottom:26px;background:var(--art-bg)}
.banner svg,.thumb svg,.dart svg{display:block;width:100%;height:100%}
.panel h2{font-size:clamp(1.6rem,3vw,2.1rem);margin:0 0 6px;font-weight:800}
.intro{color:var(--muted);margin:0 0 24px;max-width:62ch}
.panel p{max-width:66ch}

/* about */
.about{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(0,1fr);gap:40px}
.label{font-size:.75rem;text-transform:uppercase;letter-spacing:.09em;color:var(--muted);margin:0 0 10px;font-weight:600}
.route{list-style:none;margin:0 0 28px;padding:0;display:flex;flex-wrap:wrap;gap:8px}
.route li{padding:5px 12px;border-radius:999px;border:1.5px solid var(--line);font-weight:600;font-size:.9rem}
.route li:first-child{background:var(--accent);border-color:var(--accent);color:#1F1A14}
.skills{margin:0;display:grid;gap:14px}
.skills div{border-left:3px solid var(--accent);padding-left:12px}
.skills dt{font-weight:700}
.skills dd{margin:0;color:var(--muted);font-size:.95rem}

/* experience rows */
.rows{display:grid;gap:12px}
.row{display:grid;grid-template-columns:150px minmax(0,1fr) auto;gap:20px;align-items:center;width:100%;text-align:left;padding:12px;border:1px solid var(--line);border-radius:14px;background:var(--surface);color:inherit;font:inherit;cursor:pointer;transition:border-color .15s,transform .15s}
.row:hover{border-color:var(--accent);transform:translateY(-1px)}
.thumb{border-radius:10px;overflow:hidden;aspect-ratio:4/3;background:var(--art-bg)}
.ttl{display:block;font:700 1.1rem/1.3 var(--display);letter-spacing:-.01em}
.row .role{display:block;font-weight:600}
.sum{display:block;color:var(--muted);font-size:.93rem}
.row .sum{margin-top:4px}
.when{color:var(--muted);font-size:.88rem;white-space:nowrap;font-variant-numeric:tabular-nums}
.chev{color:var(--accent-ink);font-weight:700;font-size:.9rem;white-space:nowrap}

/* project cards */
.grid{display:grid;grid-template-columns:repeat(var(--cols,3),minmax(0,1fr));gap:18px}
.card{display:flex;flex-direction:column;text-align:left;width:100%;padding:0;background:var(--surface);border:1px solid var(--line);border-radius:16px;overflow:hidden;color:inherit;font:inherit;cursor:pointer;transition:border-color .15s,transform .15s}
.card:hover{border-color:var(--accent);transform:translateY(-2px)}
.card img,.tile{width:100%;aspect-ratio:2/1;object-fit:cover;display:block}
.tile{display:flex;align-items:center;padding:0 22px;background:var(--accent-soft);color:var(--ink);font:800 1.3rem/1.2 var(--display)}
.cbody{padding:14px 16px 16px;display:flex;flex-direction:column;gap:8px;flex:1}
.more{margin-top:auto;font-size:.88rem;font-weight:700;color:var(--accent-ink)}
.tags{display:flex;flex-wrap:wrap;gap:6px}
.tags>span{font-size:.75rem;padding:2px 9px;border-radius:999px;background:var(--bg);border:1px solid var(--line)}
.feature{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);border:2px solid var(--accent);box-shadow:var(--shadow);margin-bottom:18px}
.feature img,.feature .tile{aspect-ratio:auto;height:100%;min-height:260px}
.feature .cbody{padding:24px 26px;gap:12px;justify-content:center}
.feature .ttl{font-size:1.65rem;line-height:1.15}
.feature .sum{font-size:1rem}
.badge{align-self:flex-start;background:var(--accent);color:#1F1A14;font-size:.72rem;font-weight:800;text-transform:uppercase;letter-spacing:.09em;padding:4px 10px;border-radius:6px}

/* dialogs */
dialog{border:0;padding:0;border-radius:18px;max-width:720px;width:calc(100% - 32px);max-height:calc(100% - 32px);background:var(--surface);color:var(--ink);box-shadow:0 24px 70px rgba(0,0,0,.35)}
dialog::backdrop{background:rgba(22,18,14,.62)}
dialog img,dialog .tile{display:block;width:100%;aspect-ratio:2/1;object-fit:cover}
.dart{aspect-ratio:2/1;background:var(--art-bg)}
.dbody{padding:22px 26px 28px}
.dbody h3{font-size:1.5rem;margin:0 0 6px}
.dbody h4{margin:20px 0 6px;font-size:.78rem;text-transform:uppercase;letter-spacing:.09em;color:var(--muted)}
.dbody ul{margin:0;padding-left:20px}
.dclose{position:absolute;top:12px;right:12px;width:40px;height:40px;border-radius:50%;border:0;background:var(--ink);color:var(--bg);font-size:1.3rem;line-height:1;cursor:pointer}
.dactions{display:flex;flex-wrap:wrap;gap:10px;margin-top:22px}

/* contact */
.mail{display:flex;flex-wrap:wrap;align-items:center;gap:12px 16px;padding:22px 24px;border:2px solid var(--accent);border-radius:16px;background:var(--surface);margin-bottom:16px}
.mlabel{display:block;font:600 .72rem/1.4 var(--body);text-transform:uppercase;letter-spacing:.09em;color:var(--muted);user-select:none}
.mail .addr{font:800 clamp(1.15rem,3.2vw,1.6rem)/1.2 var(--display);user-select:all;word-break:break-all;margin-right:auto}
.copied{font-size:.88rem;color:var(--accent-ink);font-weight:600}
.others{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px}
.thumb img,.dart img{display:block;width:100%;height:100%;object-fit:cover}
.gallery{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:10px;margin-top:18px}
.gallery img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:10px;display:block}
.others a{display:block;padding:16px 18px;border:1px solid var(--line);border-radius:14px;background:var(--surface);text-decoration:none}
.others a:hover{border-color:var(--accent)}
.others strong{display:block}
.others span{color:var(--muted);font-size:.9rem;word-break:break-all}
footer{border-top:1px solid var(--line);padding-block:22px 44px;color:var(--muted);font-size:.85rem}

@media (max-width:860px){.grid{--cols:2!important}.about{grid-template-columns:1fr;gap:8px}.feature{grid-template-columns:1fr}.feature img,.feature .tile{min-height:0;aspect-ratio:2/1}}
@media (max-width:600px){
  .hero{grid-template-columns:1fr;gap:18px;padding-block:36px 20px}.mono{width:88px;height:88px;font-size:2rem}
  .facts{grid-template-columns:repeat(2,1fr)}
  .grid{--cols:1!important}
  .banner{aspect-ratio:2/1}
  .row{grid-template-columns:96px minmax(0,1fr);gap:14px}.row .when,.row .chev{grid-column:2}
  [role=tab]{padding:14px 10px 11px;font-size:.94rem}
  nav[role=tablist]{-webkit-mask-image:linear-gradient(90deg,#000 85%,transparent);mask-image:linear-gradient(90deg,#000 85%,transparent)}
  .others{grid-template-columns:1fr}
}
"""

JS = """
document.documentElement.classList.add('js');
(function(){
  var tabs=[].slice.call(document.querySelectorAll('[role=tab]'));
  var panels=tabs.map(function(t){return document.getElementById(t.getAttribute('aria-controls'));});
  function show(id,focus){
    if(!tabs.some(function(t){return t.dataset.tab===id;}))id=tabs[0].dataset.tab;
    tabs.forEach(function(t,i){var on=t.dataset.tab===id;t.setAttribute('aria-selected',on);t.tabIndex=on?0:-1;panels[i].hidden=!on;if(on&&focus)t.focus();});
  }
  function go(id){history.replaceState(null,'','#'+id);show(id);}
  tabs.forEach(function(t,i){
    t.addEventListener('click',function(){go(t.dataset.tab);});
    t.addEventListener('keydown',function(e){
      var k=e.key==='ArrowRight'?1:e.key==='ArrowLeft'?-1:0;if(!k)return;e.preventDefault();
      var n=tabs[(i+k+tabs.length)%tabs.length];history.replaceState(null,'','#'+n.dataset.tab);show(n.dataset.tab,true);
    });
  });
  document.querySelectorAll('[data-goto]').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();go(a.dataset.goto);document.querySelector('nav[role=tablist]').scrollIntoView({behavior:'smooth'});});});
  document.querySelectorAll('[data-open]').forEach(function(b){b.addEventListener('click',function(){var d=document.getElementById(b.dataset.open);if(d&&d.showModal)d.showModal();});});
  document.querySelectorAll('dialog').forEach(function(d){
    d.addEventListener('click',function(e){if(e.target===d)d.close();});
    d.querySelector('.dclose').addEventListener('click',function(){d.close();});
  });
  document.querySelectorAll('[data-copy]').forEach(function(b){b.addEventListener('click',function(){
    var t=b.dataset.copy,note=document.getElementById(b.dataset.note);
    function done(msg){if(note)note.textContent=msg;}
    if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(function(){done('Copied');},function(){done('Select the address to copy it');});}
    else done('Select the address to copy it');
  });});
  window.addEventListener('hashchange',function(){show(location.hash.slice(1));});
  show((location.hash||'').slice(1));
})();
"""


def e(s):
    return html.escape(s, quote=True)


def art(path):
    return open(os.path.join(HERE, path), encoding="utf-8").read()


def picture(path, alt=""):
    """Drawn SVGs are inlined so they follow the theme; photos load as <img>."""
    if path.endswith(".svg"):
        return art(path)
    return f'<img src="{e(path)}" alt="{e(alt)}" loading="lazy">'


def top_image(p):
    if p.get("repo") and os.path.exists(os.path.join(HERE, "covers", p["repo"] + ".svg")):
        return f'<img src="covers/{e(p["repo"])}.svg" alt="">'
    return f'<span class="tile" aria-hidden="true">{e(p["title"])}</span>'


def tags(ts):
    return '<span class="tags">' + "".join(f"<span>{e(t)}</span>" for t in ts) + "</span>"


def slug(p):
    return "d-" + (p.get("repo") or p["title"].lower().replace(" ", "-"))


def project(p):
    did = slug(p)
    feat = p.get("featured")
    badge = '<span class="badge">Featured project</span>' if feat else ""
    card = (f'<button class="card{" feature" if feat else ""}" type="button" data-open="{did}" aria-haspopup="dialog">'
            f'{top_image(p)}<span class="cbody">{badge}<span class="ttl">{e(p["title"])}</span>'
            f'<span class="sum">{e(p["detail"] if feat else p["summary"])}</span>{tags(p.get("tags", []))}'
            f'<span class="more">Read more →</span></span></button>')
    built = "".join(f"<li>{e(b)}</li>" for b in p.get("built", []))
    link = (f'<div class="dactions"><a class="btn primary" href="{GH}{e(p["repo"])}">Read the full case study</a></div>'
            if p.get("repo") else "")
    dialog = (f'<dialog id="{did}" aria-labelledby="{did}-t"><button class="dclose" type="button" aria-label="Close">×</button>'
              f'{top_image(p)}<div class="dbody">{badge}<h3 id="{did}-t">{e(p["title"])}</h3>'
              f'{tags(p.get("tags", []))}<p>{e(p["detail"])}</p>'
              + (f"<h4>What I did</h4><ul>{built}</ul>" if built else "") + link + "</div></dialog>")
    return card, dialog


def experience_row(x):
    did = "d-exp-" + x["id"]
    thumb = picture(x["image"])
    when = f'<span class="when">{e(x["when"])}</span>' if x.get("when") else ""
    row = (f'<button class="row" type="button" data-open="{did}" aria-haspopup="dialog">'
           f'<span class="thumb">{thumb}</span><span><span class="ttl">{e(x["org"])}</span>'
           f'<span class="role">{e(x["role"])}</span><span class="sum">{e(x["summary"])}</span></span>'
           f'<span>{when}<br><span class="chev">Details →</span></span></button>')
    paras = "".join(f"<p>{e(p)}</p>" for p in x.get("detail", []))
    bl = "".join(f"<li>{e(b)}</li>" for b in x.get("bullets", []))
    dialog = (f'<dialog id="{did}" aria-labelledby="{did}-t"><button class="dclose" type="button" aria-label="Close">×</button>'
              f'<div class="dart">{thumb}</div><div class="dbody"><h3 id="{did}-t">{e(x["org"])}</h3>'
              f'<strong>{e(x["role"])}</strong>' + (f' · <span class="when">{e(x["when"])}</span>' if x.get("when") else "")
              + paras + (f"<ul>{bl}</ul>" if bl else "")
              + ('<div class="gallery">' + "".join(picture(g, x["org"]) for g in x.get("gallery", [])) + "</div>"
                 if x.get("gallery") else "") + "</div></dialog>")
    return row, dialog


def panel(tab, title, body, intro=""):
    return (f'<section class="panel" id="p-{tab}" role="tabpanel" aria-labelledby="t-{tab}">'
            f'<div class="banner">{art(f"images/tab-{tab}.svg")}</div><h2>{e(title)}</h2>'
            + (f'<p class="intro">{e(intro)}</p>' if intro else "") + body + "</section>")


def cols_for(n):
    if n % 3 == 0 or n >= 5:
        return 3
    return 2


def main():
    d = json.load(open(os.path.join(HERE, "projects.json"), encoding="utf-8"))
    dialogs, panels = [], []

    paras = "".join(f"<p>{e(p)}</p>" for p in d["about"])
    route = '<ul class="route">' + "".join(f"<li>{e(p)}</li>" for p in d["places"]) + "</ul>"
    skills = '<dl class="skills">' + "".join(
        f'<div><dt>{e(s["name"])}</dt><dd>{e(s["detail"])}</dd></div>' for s in d["skills"]) + "</dl>"
    about = (f'<div class="about"><div>{paras}</div><div><p class="label">Where I\'ve lived and worked</p>{route}'
             f'<p class="label">Skills</p>{skills}</div></div>')
    panels.append(("about", "About", panel("about", "About me", about)))

    rows = []
    for x in d["experience"]:
        r, dl = experience_row(x)
        rows.append(r)
        dialogs.append(dl)
    panels.append(("experience", "Experience", panel("experience", "Experience", f'<div class="rows">{"".join(rows)}</div>')))

    for s in d["sections"]:
        feat = [p for p in s["projects"] if p.get("featured")][:1]
        rest = [p for p in s["projects"] if p not in feat]
        body = ""
        for p in feat:
            c, dl = project(p)
            body += c
            dialogs.append(dl)
        cards = []
        for p in rest:
            c, dl = project(p)
            cards.append(c)
            dialogs.append(dl)
        body += f'<div class="grid" style="--cols:{cols_for(len(cards))}">{"".join(cards)}</div>'
        panels.append((s["tab"], s["title"], panel(s["tab"], s["title"], body, s.get("intro", ""))))

    mails = ""
    for i, m in enumerate(d["emails"]):
        user, domain = m["address"].split("@")
        mails += (f'<div class="mail"><span class="addr"><span class="mlabel">{e(m["label"])}</span>{e(user)}&#64;{e(domain)}</span>'
                  f'<a class="btn primary" href="mailto:{e(user)}&#64;{e(domain)}">Email me</a>'
                  f'<button class="btn" type="button" data-copy="{e(m["address"])}" data-note="copy-note-{i}">Copy address</button>'
                  f'<span class="copied" id="copy-note-{i}" aria-live="polite"></span></div>')
    # Resume PDFs keep fixed file names (replace the file, never rename it); the ?v= hash
    # changes with the file's contents so browsers don't serve an old copy.
    here = os.path.dirname(os.path.abspath(__file__))
    resumes = []
    for r in d.get("resumes", []):
        with open(os.path.join(here, r["file"]), "rb") as f:
            v = hashlib.sha1(f.read()).hexdigest()[:8]
        resumes.append({**r, "href": f'{r["file"]}?v={v}'})
    contact = (mails + '<div class="others">' + "".join(
                   f'<a href="{e(l["url"])}"><strong>{e(l["label"])}</strong><span>{e(l["url"].split("://")[1])}</span></a>'
                   for l in d["links"]) + "".join(
                   f'<a href="{e(r["href"])}" target="_blank" rel="noopener"><strong>{e(r["label"])}</strong><span>{e(r["note"])}</span></a>'
                   for r in resumes) + "</div>")
    # Resumes open in a new tab, in the browser's PDF viewer, which has its own download button.
    resume_btn = f'<a class="btn" href="{e(resumes[0]["href"])}" target="_blank" rel="noopener">Resume</a>' if resumes else ""
    panels.append(("contact", "Contact", panel("contact", "Get in touch", contact, "Email is the best way to reach me. Either address works.")))

    tabs = "".join(f'<button role="tab" id="t-{t}" data-tab="{t}" aria-controls="p-{t}" aria-selected="false">{e(l)}</button>'
                   for t, l, _ in panels)
    import re
    m = re.match(r"(.*?)\s*(\([^)]*\))\s*(.*)", d["name"])
    name_html = (f'{e(m.group(1))} <span class="nick">{e(m.group(2))}</span> {e(m.group(3))}' if m else e(d["name"]))
    first = d["name"].split()[0]
    mono = f'<img src="{e(d["photo"])}" alt="">' if d.get("photo") else "MS"
    facts = '<dl class="facts">' + "".join(
        f'<div><dt>{e(f["label"])}</dt><dd>{e(f["value"])}</dd></div>' for f in d["facts"]) + "</dl>"

    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(d["short_name"])}</title>
<meta name="description" content="{e(d["headline"])}. {e(d["pitch"])}">
<meta property="og:title" content="{e(d["short_name"])} · {e(d["headline"])}">
<meta property="og:description" content="{e(d["pitch"])}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=Inter:wght@400;600;700&display=swap">
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<header class="hero">
<div class="mono" aria-hidden="true">{mono}</div>
<div>
<h1>{name_html}</h1>
<p class="headline">{e(d["headline"])}</p>
<p class="pitch">{e(d["pitch"])}</p>
<p class="open">{e(d["open_to"])}</p>
<div class="cta"><a class="btn primary" href="#research" data-goto="research">See my work</a><a class="btn" href="#contact" data-goto="contact">Contact me</a><a class="btn" href="{e(d["links"][0]["url"])}">LinkedIn</a>{resume_btn}</div>
</div>
</header>
{facts}
<nav role="tablist" aria-label="Sections">{tabs}</nav>
<main>{"".join(p for _, _, p in panels)}</main>
<footer>© 2026 {e(d["short_name"])}</footer>
</div>
{"".join(dialogs)}
<script>{JS}</script>
</body>
</html>
"""
    open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(page)
    print(f"wrote index.html ({len(panels)} tabs, {len(dialogs)} detail panels)")


if __name__ == "__main__":
    main()
