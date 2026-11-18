#!/usr/bin/env python3
"""Draw the site's banner and card images into images/. Standard library only.

    python3 art.py

Same look as the research covers: dark background, one accent per tab,
a simple motif, no text (titles live in the HTML).
"""
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "images")
BG = "#101418"


def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">'
            f'<rect width="{w}" height="{h}" fill="{BG}"/>{body}</svg>\n')


def dots(w, h, color, step=40):
    out = []
    for x in range(step // 2, w, step):
        for y in range(step // 2, h, step):
            out.append(f'<circle cx="{x}" cy="{y}" r="1.5" fill="{color}" opacity="0.12"/>')
    return "".join(out)


def about(a):
    w, h = 1200, 360
    b = dots(w, h, a)
    b += f'<circle cx="840" cy="180" r="110" fill="none" stroke="{a}" stroke-width="6"/>'
    b += f'<circle cx="840" cy="140" r="34" fill="{a}" opacity="0.9"/>'
    b += f'<path d="M772 262 C772 212 804 188 840 188 C876 188 908 212 908 262 Z" fill="{a}" opacity="0.9"/>'
    for i, (x, y) in enumerate([(1010, 90), (1060, 200), (1000, 290), (680, 80), (640, 260)]):
        b += f'<line x1="840" y1="180" x2="{x}" y2="{y}" stroke="{a}" stroke-width="3" opacity="0.5"/>'
        b += f'<circle cx="{x}" cy="{y}" r="{14 if i % 2 else 10}" fill="{a}" opacity="{0.9 if i % 2 else 0.5}"/>'
    return svg(w, h, b)


def experience(a):
    w, h = 1200, 360
    b = dots(w, h, a)
    cx, cy, r = 820, 180, 120
    b += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{a}" stroke-width="6"/>'
    for k in (0.45, 0.85):
        b += f'<ellipse cx="{cx}" cy="{cy}" rx="{r*k:.0f}" ry="{r}" fill="none" stroke="{a}" stroke-width="3" opacity="0.6"/>'
    for dy in (-60, 0, 60):
        hw = math.sqrt(r * r - dy * dy)
        b += f'<line x1="{cx-hw:.0f}" y1="{cy+dy}" x2="{cx+hw:.0f}" y2="{cy+dy}" stroke="{a}" stroke-width="3" opacity="0.6"/>'
    b += f'<path d="M560 300 C620 200 700 120 770 110" fill="none" stroke="{a}" stroke-width="4" stroke-dasharray="10 10"/>'
    b += f'<circle cx="560" cy="300" r="12" fill="{a}"/>'
    b += f'<path d="M770 70 a22 22 0 0 1 22 22 c0 18 -22 40 -22 40 s-22 -22 -22 -40 a22 22 0 0 1 22 -22z" fill="{a}"/>'
    b += f'<circle cx="770" cy="92" r="8" fill="{BG}"/>'
    return svg(w, h, b)


def research(a):
    w, h = 1200, 360
    b = dots(w, h, a)
    for i, bh in enumerate([90, 150, 120, 200, 170, 240]):
        x = 640 + i * 52
        b += f'<rect x="{x}" y="{300-bh}" width="34" height="{bh}" rx="4" fill="{a}" opacity="{0.35 + 0.1*i:.2f}"/>'
    b += f'<circle cx="930" cy="150" r="78" fill="{BG}" fill-opacity="0.6" stroke="{a}" stroke-width="10"/>'
    b += f'<line x1="986" y1="206" x2="1060" y2="280" stroke="{a}" stroke-width="18" stroke-linecap="round"/>'
    b += f'<path d="M890 160 L915 135 L940 155 L970 120" fill="none" stroke="{a}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>'
    return svg(w, h, b)


def tools(a):
    w, h = 1200, 360
    b = dots(w, h, a)
    xs = [600, 790, 980]
    for i, x in enumerate(xs):
        b += f'<rect x="{x}" y="130" width="120" height="100" rx="16" fill="none" stroke="{a}" stroke-width="6"/>'
        if i < 2:
            b += f'<path d="M{x+132} 180 L{x+176} 180" stroke="{a}" stroke-width="6" stroke-linecap="round"/>'
            b += f'<path d="M{x+164} 168 L{x+178} 180 L{x+164} 192" fill="none" stroke="{a}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>'
    b += f'<path d="M630 200 L650 160 L670 190 L690 150" fill="none" stroke="{a}" stroke-width="5" stroke-linecap="round"/>'
    b += f'<circle cx="850" cy="180" r="24" fill="{a}" opacity="0.85"/>'
    for k in range(3):
        b += f'<rect x="1005" y="{152+k*22}" width="{70-k*14}" height="10" rx="5" fill="{a}" opacity="0.8"/>'
    return svg(w, h, b)


def contact(a):
    w, h = 1200, 360
    b = dots(w, h, a)
    b += f'<rect x="700" y="100" width="260" height="170" rx="18" fill="none" stroke="{a}" stroke-width="7"/>'
    b += f'<path d="M712 112 L830 200 L948 112" fill="none" stroke="{a}" stroke-width="7" stroke-linejoin="round"/>'
    b += f'<rect x="900" y="60" width="150" height="90" rx="18" fill="{a}" opacity="0.9"/>'
    b += f'<path d="M930 150 L922 178 L956 150" fill="{a}" opacity="0.9"/>'
    for k in range(3):
        b += f'<circle cx="{945+k*30}" cy="105" r="8" fill="{BG}"/>'
    return svg(w, h, b)


def exp_card(a, kind):
    w, h = 1200, 600
    b = dots(w, h, a)
    if kind == "teach":
        b += f'<rect x="300" y="140" width="600" height="300" rx="12" fill="none" stroke="{a}" stroke-width="8"/>'
        b += f'<line x1="300" y1="470" x2="900" y2="470" stroke="{a}" stroke-width="8" stroke-linecap="round"/>'
        b += f'<path d="M360 360 C420 240 480 380 540 260 S660 300 700 220" fill="none" stroke="{a}" stroke-width="7" stroke-linecap="round"/>'
        b += f'<circle cx="790" cy="230" r="44" fill="none" stroke="{a}" stroke-width="6"/>'
        b += f'<ellipse cx="790" cy="230" rx="18" ry="44" fill="none" stroke="{a}" stroke-width="4" opacity="0.7"/>'
        b += f'<line x1="746" y1="230" x2="834" y2="230" stroke="{a}" stroke-width="4" opacity="0.7"/>'
    else:
        b += f'<rect x="380" y="220" width="440" height="260" rx="22" fill="none" stroke="{a}" stroke-width="8"/>'
        b += f'<path d="M530 220 V180 a20 20 0 0 1 20 -20 h100 a20 20 0 0 1 20 20 V220" fill="none" stroke="{a}" stroke-width="8"/>'
        b += f'<line x1="380" y1="320" x2="820" y2="320" stroke="{a}" stroke-width="6" opacity="0.7"/>'
        b += f'<rect x="575" y="302" width="50" height="36" rx="6" fill="{a}"/>'
        for i, bh in enumerate([40, 70, 55, 95]):
            b += f'<rect x="{880+i*36}" y="{460-bh}" width="24" height="{bh}" rx="3" fill="{a}" opacity="0.6"/>'
    return svg(w, h, b)


def avatar(a):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400">'
            f'<rect width="400" height="400" fill="{BG}"/>'
            f'<circle cx="200" cy="200" r="170" fill="none" stroke="{a}" stroke-width="10"/>'
            f'<text x="200" y="240" text-anchor="middle" font-family="system-ui,-apple-system,sans-serif" '
            f'font-size="130" font-weight="800" fill="#f4f1ec">MS</text></svg>\n')


TABS = {
    "about": ("#f2a65a", about),
    "experience": ("#7ad3c0", experience),
    "research": ("#e07a5f", research),
    "tools": ("#8ab4f8", tools),
    "contact": ("#c9a7f5", contact),
}


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, (a, fn) in TABS.items():
        open(os.path.join(OUT, f"tab-{name}.svg"), "w").write(fn(a))
    open(os.path.join(OUT, "exp-aiesec.svg"), "w").write(exp_card("#7ad3c0", "teach"))
    open(os.path.join(OUT, "exp-capa.svg"), "w").write(exp_card("#7ad3c0", "work"))
    open(os.path.join(OUT, "avatar.svg"), "w").write(avatar("#f2a65a"))
    print("wrote", len(os.listdir(OUT)), "images")


if __name__ == "__main__":
    main()
