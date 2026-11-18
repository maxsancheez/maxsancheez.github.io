#!/usr/bin/env python3
"""Build index.html from projects.json. Standard library only.

    python3 build.py

Covers live in covers/<repo>.svg. A project without one gets a text tile.
"""
import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
GH = "https://github.com/maxsancheez/"

CSS = """
:root{--bg:#fbfaf7;--fg:#1b1d21;--muted:#5d6370;--card:#fff;--line:#e6e3dc;--accent:#c4572a;--tile:#101418;--tilefg:#f4f1ec}
@media (prefers-color-scheme:dark){:root{--bg:#121417;--fg:#ecebe7;--muted:#a3a8b2;--card:#1a1d22;--line:#2b2f36;--accent:#f2a65a}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 system-ui,-apple-system,"Segoe UI",sans-serif}
main{max-width:960px;margin:0 auto;padding:56px 16px 40px}
h1{font-size:2.4rem;line-height:1.1;margin:0 0 12px;letter-spacing:-.02em}
.tagline{font-size:1.15rem;color:var(--muted);max-width:640px;margin:0 0 20px}
.links{display:flex;flex-wrap:wrap;gap:10px;margin:0 0 8px;padding:0;list-style:none}
.links a{display:inline-block;padding:6px 14px;border:1px solid var(--line);border-radius:999px;color:var(--fg);text-decoration:none;font-size:.95rem}
.links a:hover{border-color:var(--accent);color:var(--accent)}
h2{font-size:1.25rem;margin:48px 0 16px;padding-bottom:8px;border-bottom:1px solid var(--line)}
p{margin:0 0 12px;max-width:680px}
.exp{list-style:none;margin:0;padding:0}
.exp li{display:flex;justify-content:space-between;gap:16px;padding:10px 0;border-bottom:1px solid var(--line)}
.exp .when{color:var(--muted);white-space:nowrap}
.exp .detail{display:block;color:var(--muted);font-size:.95rem}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:18px}
.card{display:flex;flex-direction:column;background:var(--card);border:1px solid var(--line);border-radius:12px;overflow:hidden;color:inherit;text-decoration:none;transition:border-color .15s,transform .15s}
.card:hover{border-color:var(--accent);transform:translateY(-2px)}
.card img,.tile{width:100%;aspect-ratio:2/1;object-fit:cover;display:block;background:var(--tile)}
.tile{display:flex;align-items:center;padding:0 22px;color:var(--tilefg);font-weight:800;font-size:1.3rem;line-height:1.2;border-bottom:4px solid var(--accent)}
.body{padding:14px 16px 16px}
.body h3{margin:0 0 6px;font-size:1.05rem}
.body p{font-size:.93rem;color:var(--muted);margin:0 0 10px}
.tags{display:flex;flex-wrap:wrap;gap:6px}
.tags span{font-size:.75rem;padding:2px 8px;border-radius:999px;background:var(--line);color:var(--fg)}
footer{margin-top:56px;color:var(--muted);font-size:.85rem}
@media (max-width:600px){h1{font-size:2rem}main{padding-top:36px}.exp li{flex-direction:column;gap:2px}}
"""


def e(s):
    return html.escape(s, quote=True)


def card(p):
    cover = os.path.join(HERE, "covers", p["repo"] + ".svg")
    if os.path.exists(cover):
        top = f'<img src="covers/{e(p["repo"])}.svg" alt="">'
    else:
        top = f'<div class="tile" aria-hidden="true">{e(p["title"])}</div>'
    tags = "".join(f"<span>{e(t)}</span>" for t in p.get("tags", []))
    return (f'<a class="card" href="{GH}{e(p["repo"])}">{top}<div class="body">'
            f'<h3>{e(p["title"])}</h3><p>{e(p["summary"])}</p><div class="tags">{tags}</div></div></a>')


def main():
    d = json.load(open(os.path.join(HERE, "projects.json"), encoding="utf-8"))
    links = "".join(f'<li><a href="{e(l["url"])}">{e(l["label"])}</a></li>' for l in d["links"])
    about = "".join(f"<p>{e(p)}</p>" for p in d["about"])
    exp = ""
    if d.get("experience"):
        items = "".join(
            f'<li><div><strong>{e(x["org"])}</strong> · {e(x["role"])}'
            + (f'<span class="detail">{e(x["detail"])}</span>' if x.get("detail") else "")
            + f'</div><span class="when">{e(x["when"])}</span></li>'
            for x in d["experience"])
        exp = f'<h2>Experience</h2><ul class="exp">{items}</ul>'
    sections = "".join(
        f'<h2>{e(s["title"])}</h2><div class="grid">{"".join(card(p) for p in s["projects"])}</div>'
        for s in d["sections"])
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(d["name"])}</title>
<meta name="description" content="{e(d["tagline"])}">
<meta property="og:title" content="{e(d["name"])}">
<meta property="og:description" content="{e(d["tagline"])}">
<style>{CSS}</style>
</head>
<body>
<main>
<header>
<h1>{e(d["name"])}</h1>
<p class="tagline">{e(d["tagline"])}</p>
<ul class="links">{links}</ul>
</header>
<h2>About</h2>
{about}
{exp}
{sections}
<footer>Every project links to its full write-up, code and sources on GitHub.</footer>
</main>
</body>
</html>
"""
    open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(page)
    print("wrote index.html")


if __name__ == "__main__":
    main()
