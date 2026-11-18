#!/usr/bin/env python3
"""Build index.html from projects.json. Standard library only.

    python3 art.py     # (re)draw banners and card images into images/
    python3 build.py   # write index.html

Tabs are plain sections; a small script turns them into tabs and opens each
card's detail panel. Links like /#research open that tab directly. Without
JavaScript every section shows, one after another.
"""
import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
GH = "https://github.com/maxsancheez/"

ACCENT = {"about": "#f2a65a", "experience": "#7ad3c0", "research": "#e07a5f",
          "tools": "#8ab4f8", "contact": "#c9a7f5"}

CSS = """
:root{--bg:#fbfaf7;--fg:#1b1d21;--muted:#5d6370;--card:#fff;--line:#e6e3dc;--chip:#efece6;--accent:#c4572a;--shadow:0 1px 2px rgba(0,0,0,.04),0 8px 24px rgba(0,0,0,.06)}
@media (prefers-color-scheme:dark){:root{--bg:#0f1114;--fg:#ecebe7;--muted:#a3a8b2;--card:#171a1f;--line:#262a31;--chip:#22262d;--accent:#f2a65a;--shadow:none}}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 system-ui,-apple-system,"Segoe UI",sans-serif}
a{color:inherit}
.wrap{max-width:1040px;margin:0 auto;padding:0 16px}
.hero{display:flex;gap:32px;align-items:center;padding:56px 0 32px}
.hero img{width:132px;height:132px;border-radius:50%;object-fit:cover;flex:none;box-shadow:var(--shadow)}
.hero h1{font-size:2.6rem;line-height:1.05;margin:0 0 8px;letter-spacing:-.02em}
.headline{font-weight:600;color:var(--accent);margin:0 0 10px}
.pitch{color:var(--muted);font-size:1.08rem;max-width:620px;margin:0 0 18px}
.cta{display:flex;flex-wrap:wrap;gap:10px}
.btn{display:inline-block;padding:9px 18px;border-radius:999px;border:1px solid var(--line);text-decoration:none;font-weight:600;font-size:.95rem;background:var(--card)}
.btn.primary{background:var(--fg);color:var(--bg);border-color:var(--fg)}
.btn:hover{border-color:var(--accent)}
nav[role=tablist]{position:sticky;top:0;z-index:5;background:var(--bg);border-bottom:1px solid var(--line);display:flex;gap:4px;overflow-x:auto;scrollbar-width:none}
nav[role=tablist]::-webkit-scrollbar{display:none}
[role=tab]{appearance:none;background:none;border:0;border-bottom:3px solid transparent;color:var(--muted);font:600 .98rem system-ui,sans-serif;padding:14px 14px 11px;cursor:pointer;white-space:nowrap}
[role=tab][aria-selected=true]{color:var(--fg);border-bottom-color:var(--tab)}
[role=tab]:focus-visible{outline:2px solid var(--accent);outline-offset:-4px}
.panel{padding:28px 0 56px}
.js .panel[hidden]{display:none}
.banner{width:100%;aspect-ratio:10/3;object-fit:cover;border-radius:16px;display:block;margin-bottom:24px;border-bottom:4px solid var(--tab)}
.panel h2{font-size:1.7rem;margin:0 0 6px;letter-spacing:-.01em}
.intro{color:var(--muted);margin:0 0 22px;max-width:680px}
.panel p{max-width:700px}
.skills{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px;margin:24px 0 0;padding:0;list-style:none}
.skills li{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px;box-shadow:var(--shadow)}
.skills strong{display:block}
.skills span{color:var(--muted);font-size:.9rem}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:18px}
.card{display:flex;flex-direction:column;text-align:left;width:100%;padding:0;background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:hidden;color:inherit;font:inherit;cursor:pointer;box-shadow:var(--shadow);transition:border-color .15s,transform .15s}
.card:hover{border-color:var(--tab);transform:translateY(-2px)}
.card:focus-visible{outline:2px solid var(--tab);outline-offset:2px}
.card img,.tile{width:100%;aspect-ratio:2/1;object-fit:cover;display:block;background:#101418}
.tile{display:flex;align-items:center;padding:0 22px;color:#f4f1ec;font-weight:800;font-size:1.3rem;line-height:1.2;border-bottom:4px solid var(--tab)}
.cbody{padding:14px 16px 16px;display:flex;flex-direction:column;gap:8px;flex:1}
.cbody h3{margin:0;font-size:1.06rem}
.cbody p{margin:0;font-size:.93rem;color:var(--muted)}
.meta{color:var(--muted);font-size:.88rem}
.more{margin-top:auto;font-size:.88rem;font-weight:600;color:var(--tab)}
.tags{display:flex;flex-wrap:wrap;gap:6px}
.tags span{font-size:.75rem;padding:2px 9px;border-radius:999px;background:var(--chip)}
dialog{border:0;padding:0;border-radius:18px;max-width:720px;width:calc(100% - 32px);background:var(--card);color:var(--fg);box-shadow:0 20px 60px rgba(0,0,0,.35)}
dialog::backdrop{background:rgba(10,12,15,.6)}
dialog img,dialog .tile{border-radius:0}
.dbody{padding:22px 24px 26px}
.dbody h3{font-size:1.4rem;margin:0 0 4px}
.dbody h4{margin:18px 0 6px;font-size:.95rem;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}
.dbody ul{margin:0;padding-left:20px}
.dclose{position:absolute;top:10px;right:10px;width:38px;height:38px;border-radius:50%;border:0;background:rgba(16,20,24,.75);color:#fff;font-size:1.3rem;cursor:pointer}
.dactions{display:flex;flex-wrap:wrap;gap:10px;margin-top:20px}
.contact{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:14px}
.contact a{display:block;padding:18px;border:1px solid var(--line);border-radius:14px;background:var(--card);text-decoration:none;box-shadow:var(--shadow)}
.contact a:hover{border-color:var(--tab)}
.contact strong{display:block;font-size:1.05rem}
.contact span{color:var(--muted);font-size:.9rem;word-break:break-all}
footer{border-top:1px solid var(--line);padding:22px 0 40px;color:var(--muted);font-size:.85rem}
@media (max-width:640px){.hero{flex-direction:column;align-items:flex-start;gap:18px;padding-top:36px}.hero img{width:96px;height:96px}.hero h1{font-size:2.1rem}.banner{aspect-ratio:2/1;object-position:100% 50%}[role=tab]{padding:14px 10px 11px;font-size:.93rem}nav[role=tablist]{-webkit-mask-image:linear-gradient(90deg,#000 85%,transparent);mask-image:linear-gradient(90deg,#000 85%,transparent)}}
"""

JS = """
document.documentElement.classList.add('js');
(function(){
  var tabs=[].slice.call(document.querySelectorAll('[role=tab]'));
  var panels=tabs.map(function(t){return document.getElementById(t.getAttribute('aria-controls'));});
  function show(id,focus){
    var found=false;
    tabs.forEach(function(t,i){var on=t.dataset.tab===id;found=found||on;t.setAttribute('aria-selected',on);t.tabIndex=on?0:-1;panels[i].hidden=!on;if(on&&focus)t.focus();});
    if(!found)show(tabs[0].dataset.tab,focus);
  }
  tabs.forEach(function(t,i){
    t.addEventListener('click',function(){history.replaceState(null,'','#'+t.dataset.tab);show(t.dataset.tab);});
    t.addEventListener('keydown',function(e){
      var k=e.key==='ArrowRight'?1:e.key==='ArrowLeft'?-1:0;if(!k)return;e.preventDefault();
      var n=tabs[(i+k+tabs.length)%tabs.length];history.replaceState(null,'','#'+n.dataset.tab);show(n.dataset.tab,true);
    });
  });
  document.querySelectorAll('[data-goto]').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();var id=a.dataset.goto;history.replaceState(null,'','#'+id);show(id);document.querySelector('nav[role=tablist]').scrollIntoView({behavior:'smooth'});});});
  document.querySelectorAll('[data-open]').forEach(function(b){b.addEventListener('click',function(){var d=document.getElementById(b.dataset.open);if(d&&d.showModal)d.showModal();});});
  document.querySelectorAll('dialog').forEach(function(d){
    d.addEventListener('click',function(e){if(e.target===d)d.close();});
    d.querySelector('.dclose').addEventListener('click',function(){d.close();});
  });
  window.addEventListener('hashchange',function(){show(location.hash.slice(1));});
  show((location.hash||'').slice(1));
})();
"""


def e(s):
    return html.escape(s, quote=True)


def top_image(repo, title):
    if os.path.exists(os.path.join(HERE, "covers", repo + ".svg")):
        return f'<img src="covers/{e(repo)}.svg" alt="">'
    return f'<div class="tile" aria-hidden="true">{e(title)}</div>'


def tags(ts):
    return '<div class="tags">' + "".join(f"<span>{e(t)}</span>" for t in ts) + "</div>"


def project_card(p):
    did = "d-" + p["repo"]
    card = (f'<button class="card" type="button" data-open="{did}" aria-haspopup="dialog">'
            f'{top_image(p["repo"], p["title"])}<div class="cbody"><h3>{e(p["title"])}</h3>'
            f'<p>{e(p["summary"])}</p>{tags(p.get("tags", []))}<span class="more">Read more →</span></div></button>')
    built = "".join(f"<li>{e(b)}</li>" for b in p.get("built", []))
    dialog = (f'<dialog id="{did}" aria-labelledby="{did}-t"><button class="dclose" type="button" aria-label="Close">×</button>'
              f'{top_image(p["repo"], p["title"])}<div class="dbody"><h3 id="{did}-t">{e(p["title"])}</h3>'
              f'{tags(p.get("tags", []))}<p>{e(p["detail"])}</p>'
              + (f"<h4>What I did</h4><ul>{built}</ul>" if built else "")
              + f'<div class="dactions"><a class="btn primary" href="{GH}{e(p["repo"])}">Full write-up &amp; code</a></div></div></dialog>')
    return card, dialog


def exp_card(x):
    has = bool(x.get("detail") or x.get("bullets"))
    inner = (f'<img src="{e(x["image"])}" alt=""><div class="cbody"><h3>{e(x["org"])}</h3>'
             f'<p>{e(x["role"])}</p><span class="meta">{e(x["when"])}</span>'
             + ('<span class="more">Read more →</span>' if has else "") + "</div>")
    if not has:
        return f'<div class="card" style="cursor:default">{inner}</div>', ""
    did = "d-exp-" + x["id"]
    paras = "".join(f"<p>{e(p)}</p>" for p in x.get("detail", []))
    bl = "".join(f"<li>{e(b)}</li>" for b in x.get("bullets", []))
    dialog = (f'<dialog id="{did}" aria-labelledby="{did}-t"><button class="dclose" type="button" aria-label="Close">×</button>'
              f'<img src="{e(x["image"])}" alt=""><div class="dbody"><h3 id="{did}-t">{e(x["org"])} · {e(x["role"])}</h3>'
              f'<span class="meta">{e(x["when"])}</span>{paras}' + (f"<ul>{bl}</ul>" if bl else "") + "</div></dialog>")
    return f'<button class="card" type="button" data-open="{did}" aria-haspopup="dialog">{inner}</button>', dialog


def panel(tab, title, body, intro=""):
    return (f'<section class="panel" id="p-{tab}" role="tabpanel" aria-labelledby="t-{tab}" style="--tab:{ACCENT[tab]}">'
            f'<img class="banner" src="images/tab-{tab}.svg" alt=""><h2>{e(title)}</h2>'
            + (f'<p class="intro">{e(intro)}</p>' if intro else "") + body + "</section>")


def main():
    d = json.load(open(os.path.join(HERE, "projects.json"), encoding="utf-8"))
    dialogs, panels, tabs = [], [], []

    about = "".join(f"<p>{e(p)}</p>" for p in d["about"])
    about += '<ul class="skills">' + "".join(
        f'<li><strong>{e(s["name"])}</strong><span>{e(s["detail"])}</span></li>' for s in d["skills"]) + "</ul>"
    panels.append(("about", "About", panel("about", "About", about)))

    cards = []
    for x in d["experience"]:
        c, dl = exp_card(x)
        cards.append(c)
        if dl:
            dialogs.append(dl)
    panels.append(("experience", "Experience", panel("experience", "Experience", f'<div class="grid">{"".join(cards)}</div>')))

    for s in d["sections"]:
        cards = []
        for p in s["projects"]:
            c, dl = project_card(p)
            cards.append(c)
            dialogs.append(dl)
        panels.append((s["tab"], s["title"], panel(s["tab"], s["title"], f'<div class="grid">{"".join(cards)}</div>', s.get("intro", ""))))

    contact = '<div class="contact">' + "".join(
        f'<a href="{e(l["url"])}"><strong>{e(l["label"])}</strong><span>{e(l["url"].split("://")[1])}</span></a>'
        for l in d["links"]) + "</div>"
    panels.append(("contact", "Contact", panel("contact", "Get in touch", contact,
                                               "The best way to reach me is a message on LinkedIn.")))

    for tab, label, _ in panels:
        tabs.append(f'<button role="tab" id="t-{tab}" data-tab="{tab}" aria-controls="p-{tab}" '
                    f'aria-selected="false" style="--tab:{ACCENT[tab]}">{e(label)}</button>')

    photo = d.get("photo") or "images/avatar.svg"
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(d["name"])}</title>
<meta name="description" content="{e(d["pitch"])}">
<meta property="og:title" content="{e(d["name"])} · {e(d["headline"])}">
<meta property="og:description" content="{e(d["pitch"])}">
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<header class="hero">
<img src="{e(photo)}" alt="{e(d["name"])}">
<div>
<h1>{e(d["name"])}</h1>
<p class="headline">{e(d["headline"])}</p>
<p class="pitch">{e(d["pitch"])}</p>
<div class="cta"><a class="btn primary" href="#research" data-goto="research">See my work</a><a class="btn" href="#contact" data-goto="contact">Contact</a><a class="btn" href="{e(d["links"][0]["url"])}">LinkedIn</a></div>
</div>
</header>
<nav role="tablist" aria-label="Sections">{"".join(tabs)}</nav>
<main>{"".join(p for _, _, p in panels)}</main>
<footer>Every project links to its full write-up, code and sources on GitHub.</footer>
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
