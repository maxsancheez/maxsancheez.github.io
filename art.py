#!/usr/bin/env python3
"""Draw the site's banner and card images into images/. Standard library only.

    python3 art.py

The SVGs paint with the page's CSS variables (with fallbacks), and build.py
inlines them, so they follow the light/dark theme. No text in the art: titles
live in the HTML.
"""
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "images")

BG = "var(--art-bg,#EFE6D6)"
A = "var(--accent,#E8620C)"
INK = "var(--ink,#1F1A14)"
SOFT = "var(--accent-soft,#F6C9A6)"


def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'preserveAspectRatio="xMidYMid slice" aria-hidden="true">'
            f'<rect width="{w}" height="{h}" fill="{BG}"/>{body}</svg>\n')


def grid(w, h, step=48):
    out = []
    for x in range(step, w, step):
        out.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{h}" stroke="{INK}" stroke-opacity="0.05"/>')
    for y in range(step, h, step):
        out.append(f'<line x1="0" y1="{y}" x2="{w}" y2="{y}" stroke="{INK}" stroke-opacity="0.05"/>')
    return "".join(out)


def about():
    # A route through places (dots), ending in a filled "home" circle.
    w, h = 1200, 360
    b = grid(w, h)
    pts = [(560, 250), (680, 150), (800, 220), (930, 110), (1060, 200)]
    d = "M" + " L".join(f"{x} {y}" for x, y in pts)
    b += f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="3" stroke-dasharray="2 10" stroke-linecap="round"/>'
    for i, (x, y) in enumerate(pts):
        r = 30 if i == 0 else 14
        fill = A if i == 0 else SOFT
        b += f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"/>'
    b += f'<circle cx="560" cy="250" r="52" fill="none" stroke="{A}" stroke-width="3"/>'
    return svg(w, h, b)


def experience():
    w, h = 1200, 360
    b = grid(w, h)
    cx, cy, r = 900, 180, 120
    b += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{SOFT}"/>'
    for k in (0.4, 0.8):
        b += f'<ellipse cx="{cx}" cy="{cy}" rx="{r*k:.0f}" ry="{r}" fill="none" stroke="{INK}" stroke-width="3" stroke-opacity="0.5"/>'
    for dy in (-60, 0, 60):
        hw = math.sqrt(r * r - dy * dy)
        b += f'<line x1="{cx-hw:.0f}" y1="{cy+dy}" x2="{cx+hw:.0f}" y2="{cy+dy}" stroke="{INK}" stroke-width="3" stroke-opacity="0.5"/>'
    b += f'<rect x="560" y="170" width="190" height="130" rx="18" fill="{A}"/>'
    b += f'<path d="M620 170 V146 a14 14 0 0 1 14 -14 h42 a14 14 0 0 1 14 14 V170" fill="none" stroke="{A}" stroke-width="10"/>'
    b += f'<line x1="560" y1="226" x2="750" y2="226" stroke="{BG}" stroke-width="6"/>'
    return svg(w, h, b)


def research():
    w, h = 1200, 360
    b = grid(w, h)
    for i, bh in enumerate([80, 140, 110, 190, 160, 230]):
        x = 600 + i * 56
        b += f'<rect x="{x}" y="{310-bh}" width="38" height="{bh}" rx="4" fill="{A if i == 5 else SOFT}"/>'
    b += f'<circle cx="980" cy="140" r="74" fill="{BG}" fill-opacity="0.7" stroke="{INK}" stroke-width="10"/>'
    b += f'<line x1="1033" y1="193" x2="1100" y2="262" stroke="{INK}" stroke-width="18" stroke-linecap="round"/>'
    b += f'<path d="M942 160 L965 132 L990 150 L1018 112" fill="none" stroke="{A}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
    return svg(w, h, b)


def tools():
    w, h = 1200, 360
    b = grid(w, h)
    for i, x in enumerate([580, 780, 980]):
        fill = A if i == 1 else SOFT
        b += f'<rect x="{x}" y="125" width="130" height="110" rx="18" fill="{fill}"/>'
        if i < 2:
            b += f'<path d="M{x+142} 180 L{x+186} 180" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
            b += f'<path d="M{x+174} 168 L{x+188} 180 L{x+174} 192" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>'
    b += f'<path d="M608 200 L628 160 L648 190 L668 150 L688 175" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
    b += f'<circle cx="845" cy="180" r="26" fill="{BG}"/>'
    for k in range(3):
        b += f'<rect x="1006" y="{152+k*22}" width="{78-k*16}" height="10" rx="5" fill="{INK}"/>'
    return svg(w, h, b)


def contact():
    w, h = 1200, 360
    b = grid(w, h)
    b += f'<rect x="680" y="100" width="280" height="180" rx="18" fill="{SOFT}"/>'
    b += f'<path d="M692 114 L820 206 L948 114" fill="none" stroke="{INK}" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/>'
    b += f'<rect x="910" y="56" width="160" height="94" rx="20" fill="{A}"/>'
    b += f'<path d="M944 150 L934 180 L972 150 Z" fill="{A}"/>'
    for k in range(3):
        b += f'<circle cx="{955+k*35}" cy="103" r="9" fill="{BG}"/>'
    return svg(w, h, b)


def thumb(kind):
    w, h = 480, 360
    b = grid(w, h, 40)
    if kind == "tapreview":
        b += f'<rect x="100" y="70" width="170" height="230" rx="24" fill="{INK}"/>'
        b += f'<rect x="114" y="88" width="142" height="178" rx="10" fill="{BG}"/>'
        for i in range(5):
            cx, cy, ro, ri = 130 + i * 27, 177, 12, 5
            pts = []
            for k in range(10):
                r = ro if k % 2 == 0 else ri
                ang = -math.pi / 2 + k * math.pi / 5
                pts.append(f"{cx + r*math.cos(ang):.1f},{cy + r*math.sin(ang):.1f}")
            b += f'<polygon points="{" ".join(pts)}" fill="{A}"/>'
        for r in (34, 58, 82):
            b += f'<path d="M{300} {185 - r} a{r} {r} 0 0 1 0 {2*r}" fill="none" stroke="{A}" stroke-width="8" stroke-linecap="round"/>'
    elif kind == "nutripeludos":
        b += f'<path d="M120 220 h240 l-28 70 h-184 z" fill="{A}"/>'
        b += f'<ellipse cx="240" cy="220" rx="120" ry="18" fill="{SOFT}"/>'
        b += f'<ellipse cx="240" cy="130" rx="34" ry="30" fill="{INK}"/>'
        for x, y in [(190, 88), (225, 70), (262, 72), (294, 92)]:
            b += f'<ellipse cx="{x}" cy="{y}" rx="13" ry="16" fill="{INK}"/>'
    elif kind == "aiesec":
        b += f'<rect x="110" y="120" width="260" height="130" rx="46" fill="{INK}"/>'
        b += f'<circle cx="190" cy="185" r="38" fill="{A}"/>'
        b += f'<circle cx="290" cy="185" r="38" fill="{A}"/>'
        b += f'<path d="M224 250 q16 -26 32 0" fill="{BG}"/>'
        b += f'<path d="M110 160 q-40 0 -40 -40" fill="none" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>'
        b += f'<path d="M370 160 q40 0 40 -40" fill="none" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>'
        b += f'<rect x="200" y="60" width="80" height="22" rx="11" fill="{SOFT}"/>'
    elif kind == "ahk":
        b += f'<path d="M110 130 L240 70 L370 130 Z" fill="{A}"/>'
        for x in (130, 190, 250, 310):
            b += f'<rect x="{x}" y="145" width="36" height="120" rx="4" fill="{SOFT}"/>'
        b += f'<rect x="104" y="270" width="272" height="22" rx="4" fill="{INK}"/>'
    elif kind == "danone":
        b += f'<rect x="100" y="70" width="280" height="220" rx="16" fill="{SOFT}"/>'
        for i, bh in enumerate([50, 90, 70, 130]):
            b += f'<rect x="{135+i*60}" y="{260-bh}" width="38" height="{bh}" rx="4" fill="{A if i == 3 else INK}"/>'
        b += f'<path d="M135 150 L195 120 L255 135 L330 90" fill="none" stroke="{A}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>'
    elif kind == "dakora":
        # a gear beside a three-step workflow
        cx, cy = 150, 180
        for k in range(8):
            ang = k * math.pi / 4
            x, y = cx + 72 * math.cos(ang), cy + 72 * math.sin(ang)
            b += f'<rect x="{x-14:.1f}" y="{y-14:.1f}" width="28" height="28" rx="4" fill="{INK}" transform="rotate({k*45} {x:.1f} {y:.1f})"/>'
        b += f'<circle cx="{cx}" cy="{cy}" r="66" fill="{INK}"/>'
        b += f'<circle cx="{cx}" cy="{cy}" r="26" fill="{BG}"/>'
        for i, y in enumerate((90, 165, 240)):
            b += f'<rect x="270" y="{y}" width="120" height="44" rx="10" fill="{A if i == 2 else SOFT}"/>'
        for y in (134, 209):
            b += f'<path d="M330 {y+4} v22" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
    return svg(w, h, b)


def main():
    os.makedirs(OUT, exist_ok=True)
    # only clear drawn SVGs; photos (headshot, galleries) live in images/ too
    for old in os.listdir(OUT):
        if old.endswith(".svg"):
            os.remove(os.path.join(OUT, old))
    for name, fn in {"about": about, "experience": experience, "research": research,
                     "tools": tools, "contact": contact}.items():
        open(os.path.join(OUT, f"tab-{name}.svg"), "w").write(fn())
    for k in ("tapreview", "nutripeludos", "aiesec", "ahk", "danone", "dakora"):
        open(os.path.join(OUT, f"exp-{k}.svg"), "w").write(thumb(k))
    print("wrote", len(os.listdir(OUT)), "images")


if __name__ == "__main__":
    main()
