#!/usr/bin/env python3
"""Build the profile's SVG assets in the same cold-glass style as
https://younesberiane.github.io (ice-blue / indigo on near-black glass,
JetBrains Mono, the pixel "Y.B." mark).

Writes:
    assets/card-dark.svg, assets/card-light.svg        hero card, desktop
    assets/card-dark-m.svg, assets/card-light-m.svg    hero card, narrow (mobile)
    assets/terminal.svg, assets/terminal-m.svg         terminal bio (dark on both schemes, like the site)

The counts (merged PRs, projects) are written from data/fixes.json / the
README table so they start out right, and scripts/refresh.py rewrites them in
place afterwards (see the regexes there: "N open-source fixes merged into M
projects", "M projects (N PRs)", class="n-prs">N< and class="n-projects">M<).

JetBrains Mono is embedded as a subset (assets/fonts/*.woff2, glyphs listed in
assets/fonts/subset-chars.txt) because SVGs shown through <img> cannot load
external fonts.

Usage: python3 scripts/build_assets.py
"""
import base64
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
FONTS = ASSETS / "fonts"
README = ROOT / "README.md"

# ---------------------------------------------------------------- palette
DARK = dict(
    bg="#06090f", text="#e5edf7", muted="#97a5ba", faint="#76849c",
    accent="#8fd3ff", accent2="#c2e9ff", g1="#7dd3fc", g2="#818cf8",
    border="rgba(148,163,184,.16)", border2="rgba(148,163,184,.36)",
    surface="rgba(255,255,255,.035)", surface2="rgba(255,255,255,.07)",
    glow1="rgba(56,189,248,.18)", glow2="rgba(129,140,248,.16)",
    dot="rgba(148,163,184,.13)", hl1="rgba(255,255,255,.08)", hl2="rgba(255,255,255,.04)",
    shimmer="rgba(255,255,255,.07)",
)
LIGHT = dict(
    bg="#f3f6fb", text="#0f1a2b", muted="#4b5a70", faint="#66758c",
    accent="#0b63a8", accent2="#084c85", g1="#0ea5e9", g2="#4f46e5",
    border="#d3dbe7", border2="#aab7cb",
    surface="rgba(255,255,255,.72)", surface2="#ffffff",
    glow1="rgba(14,165,233,.18)", glow2="rgba(79,70,229,.12)",
    dot="rgba(15,26,43,.09)", hl1="rgba(255,255,255,.9)", hl2="rgba(255,255,255,.5)",
    shimmer="rgba(255,255,255,.55)",
)
TERM = dict(bg="#0a1019", border="rgba(148,163,184,.2)", text="#dbe7f5", muted="#8aa0b8",
            prompt="#7dd3fc", hi="#c2e9ff", d1="#4b5d75", d2="#3b4f68", d3="#7dd3fc",
            bar="rgba(255,255,255,.03)")

MONO = "'JetBrains Mono', ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', 'DejaVu Sans Mono', monospace"
CH = 0.6  # JetBrains Mono advance width in em


def font_face():
    faces = []
    for file, weight, style in (
        ("JetBrainsMono-Regular.woff2", 400, "normal"),
        ("JetBrainsMono-Bold.woff2", 700, "normal"),
        ("JetBrainsMono-Italic.woff2", 400, "italic"),
    ):
        b64 = base64.b64encode((FONTS / file).read_bytes()).decode("ascii")
        faces.append(
            f"@font-face{{font-family:'JetBrains Mono';font-weight:{weight};font-style:{style};"
            f"src:url(data:font/woff2;base64,{b64}) format('woff2');}}"
        )
    return "".join(faces)


# ---------------------------------------------------------------- pixel mark (same grid and rules as the site)
ART = [
    "██╗   ██╗   ██████╗    ",
    "╚██╗ ██╔╝   ██╔══██╗   ",
    " ╚████╔╝    ██████╔╝   ",
    "  ╚██╔╝     ██╔══██╗   ",
    "   ██║   ██╗██████╔╝██╗",
    "   ╚═╝   ╚═╝╚═════╝ ╚═╝",
]
ART_W, ART_H = 23 * 15, 6 * 28


def art(grid=ART):
    """Return (list of fill rects (x, y, w, h), stroke path d, stroke length)."""
    CW, CHh, D = 15, 28, 2.6
    B = "█"

    def f(v):
        return f"{round(v * 10) / 10:g}"

    shapes = {
        "═": lambda x0, y0, x1, y1, cx, cy: [[x0, cy - D, x1, cy - D], [x0, cy + D, x1, cy + D]],
        "║": lambda x0, y0, x1, y1, cx, cy: [[cx - D, y0, cx - D, y1], [cx + D, y0, cx + D, y1]],
        "╗": lambda x0, y0, x1, y1, cx, cy: [[x0, cy - D, cx + D, cy - D, cx + D, y1], [x0, cy + D, cx - D, cy + D, cx - D, y1]],
        "╔": lambda x0, y0, x1, y1, cx, cy: [[x1, cy - D, cx - D, cy - D, cx - D, y1], [x1, cy + D, cx + D, cy + D, cx + D, y1]],
        "╝": lambda x0, y0, x1, y1, cx, cy: [[x0, cy + D, cx + D, cy + D, cx + D, y0], [x0, cy - D, cx - D, cy - D, cx - D, y0]],
        "╚": lambda x0, y0, x1, y1, cx, cy: [[x1, cy + D, cx - D, cy + D, cx - D, y0], [x1, cy - D, cx + D, cy - D, cx + D, y0]],
    }
    rects, stroke, length = [], "", 0.0
    for r, line in enumerate(grid):
        c = 0
        while c < len(line):
            if line[c] != B:
                c += 1
                continue
            s = c
            while c < len(line) and line[c] == B:
                c += 1
            rects.append((s * CW, r * CHh, (c - s) * CW, CHh))
        for k, ch in enumerate(line):
            fn = shapes.get(ch)
            if not fn:
                continue
            x0, y0 = k * CW, r * CHh
            for p in fn(x0, y0, x0 + CW, y0 + CHh, x0 + CW / 2, y0 + CHh / 2):
                stroke += f"M{f(p[0])} {f(p[1])}"
                for i in range(2, len(p), 2):
                    stroke += f"L{f(p[i])} {f(p[i + 1])}"
                    length += math.hypot(p[i] - p[i - 2], p[i + 1] - p[i - 1])
    return rects, stroke, length


def mark_svg(x, y, scale, pal, uid="m"):
    """The Y.B. mark: blocks fade in one by one, the outline draws itself once."""
    rects, stroke, length = art()
    out = [f'<g transform="translate({x} {y}) scale({scale})">']
    for i, (rx, ry, rw, rh) in enumerate(rects):
        out.append(
            f'<rect class="px" style="animation-delay:{0.35 + i * 0.07:.2f}s" x="{rx}" y="{ry}" '
            f'width="{rw}" height="{rh}" fill="url(#{uid}g)" shape-rendering="crispEdges"/>'
        )
    out.append(
        f'<path class="ln" style="stroke-dasharray:{math.ceil(length)};stroke-dashoffset:{math.ceil(length)}" '
        f'fill="none" stroke="url(#{uid}g)" stroke-opacity=".75" stroke-width="1.4" d="{stroke}"/>'
    )
    out.append("</g>")
    grad = (
        f'<linearGradient id="{uid}g" gradientUnits="userSpaceOnUse" x1="{x}" y1="{y}" '
        f'x2="{x + ART_W * scale}" y2="{y + ART_H * scale}">'
        f'<stop offset="0" stop-color="{pal["g1"]}"/><stop offset="1" stop-color="{pal["g2"]}"/></linearGradient>'
    )
    return grad, "\n".join(out)


# ---------------------------------------------------------------- counts
def counts():
    """Merged PR count and project count from the README table (the source refresh.py maintains)."""
    text = README.read_text()
    m = re.search(r"<!-- merged:start -->(.*?)<!-- merged:end -->", text, re.S)
    rows = re.findall(r"^\| \[([^/\]]+/[^\]#]+?) #\d+\]", m.group(1), re.M) if m else []
    if not rows:
        raise SystemExit("no merged table in README.md")
    return len(rows), len(set(rows))


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---------------------------------------------------------------- card
def card(pal, prs, projects, mobile=False):
    W, H = (480, 640) if mobile else (960, 324)
    title = (
        f"Y.B. (drakeo338). {prs} open-source fixes merged into {projects} projects, "
        "including LangChain OpenWiki, MapLibre GL JS, Tencent BrowserSkill, Bazel rules_rust, "
        "Pake, VoiceStudio, Hindsight and DB-GPT. In memory of Drakeo the Ruler (1993-2021)."
    )
    if mobile:
        px, py, pw, ph = 24, 24, 432, 236
        scale = 1.0
    else:
        px, py, pw, ph = 36, 36, 316, 248
        scale = 0.74
    mw, mh = ART_W * scale, ART_H * scale
    mx, my = px + (pw - mw) / 2, py + (ph - mh) / 2 - 8
    grad, mark = mark_svg(mx, my, scale, pal)

    css = font_face() + (
        f"text{{font-family:{MONO};}}"
        f".px{{opacity:0;animation:pop .5s ease-out both;}}"
        f".ln{{animation:draw 2.2s cubic-bezier(.4,0,.2,1) .2s forwards;}}"
        f".sh{{animation:shimmer 9s linear 2.5s infinite;}}"
        f".halo{{animation:halo 2.6s ease-out infinite;transform-box:fill-box;transform-origin:center;}}"
        f"@keyframes pop{{from{{opacity:0;}}to{{opacity:1;}}}}"
        f"@keyframes draw{{to{{stroke-dashoffset:0;}}}}"
        f"@keyframes shimmer{{0%{{transform:translateX(-{pw + 120}px);}}18%{{transform:translateX({pw + 120}px);}}100%{{transform:translateX({pw + 120}px);}}}}"
        f"@keyframes halo{{0%{{transform:scale(1);opacity:.55;}}100%{{transform:scale(2.6);opacity:0;}}}}"
        f".name{{font-size:{34 if mobile else 40}px;font-weight:700;letter-spacing:-.03em;}}"
        f".kick{{font-size:{12.5 if mobile else 13}px;fill:{pal['muted']};}}"
        f".line{{font-size:15px;fill:{pal['text']};}}"
        f".num{{font-size:26px;font-weight:700;fill:{pal['text']};}}"
        f".lbl{{font-size:10.5px;fill:{pal['muted']};letter-spacing:.08em;}}"
        f".fact{{font-size:14px;font-weight:700;fill:{pal['text']};}}"
        f".tag{{font-size:11px;fill:{pal['faint']};letter-spacing:.06em;}}"
        f".foot{{font-size:12px;fill:{pal['faint']};}}"
        f".memo{{font-size:12px;font-style:italic;fill:{pal['faint']};}}"
    )

    o = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">',
        f"<title id=\"t\">{esc(title)}</title>",
        "<defs>",
        f"<style>{css}</style>",
        grad,
        f'<radialGradient id="glow1" gradientUnits="userSpaceOnUse" cx="{px + pw * 0.4}" cy="{py + 20}" r="{380 if mobile else 340}">'
        f'<stop offset="0" stop-color="{pal["glow1"]}"/><stop offset="1" stop-color="{pal["glow1"]}" stop-opacity="0"/></radialGradient>',
        f'<radialGradient id="glow2" gradientUnits="userSpaceOnUse" cx="{W - 60}" cy="{H - 20}" r="{360 if mobile else 380}">'
        f'<stop offset="0" stop-color="{pal["glow2"]}"/><stop offset="1" stop-color="{pal["glow2"]}" stop-opacity="0"/></radialGradient>',
        f'<linearGradient id="hl" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{pal["hl1"]}"/>'
        f'<stop offset=".4" stop-color="{pal["hl1"]}" stop-opacity="0"/><stop offset=".6" stop-color="{pal["hl2"]}" stop-opacity="0"/>'
        f'<stop offset="1" stop-color="{pal["hl2"]}"/></linearGradient>',
        f'<linearGradient id="shg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{pal["shimmer"]}" stop-opacity="0"/>'
        f'<stop offset=".5" stop-color="{pal["shimmer"]}"/><stop offset="1" stop-color="{pal["shimmer"]}" stop-opacity="0"/></linearGradient>',
        f'<linearGradient id="tg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{pal["text"]}"/>'
        f'<stop offset=".55" stop-color="{pal["text"]}"/><stop offset="1" stop-color="{pal["accent"]}"/></linearGradient>',
        f'<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="{pal["dot"]}"/></pattern>',
        f'<clipPath id="card"><rect x="0" y="0" width="{W}" height="{H}" rx="16"/></clipPath>',
        f'<clipPath id="panel"><rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="16"/></clipPath>',
        "</defs>",
        f'<g clip-path="url(#card)">',
        f'<rect width="{W}" height="{H}" fill="{pal["bg"]}"/>',
        f'<rect width="{W}" height="{H}" fill="url(#dots)"/>',
        f'<rect width="{W}" height="{H}" fill="url(#glow1)"/>',
        f'<rect width="{W}" height="{H}" fill="url(#glow2)"/>',
        "</g>",
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="none" stroke="{pal["border"]}"/>',
        # glass panel
        f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="16" fill="{pal["surface"]}" stroke="{pal["border"]}"/>',
        f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="16" fill="url(#hl)"/>',
        mark,
        f'<g clip-path="url(#panel)"><rect class="sh" x="{px + pw / 2 - 60}" y="{py - 20}" width="120" height="{ph + 40}" '
        f'fill="url(#shg)" transform="skewX(-18)"/></g>',
        f'<text class="tag" x="{px + 14}" y="{py + ph - 12}">Y.B. / 2026</text>',
    ]

    if mobile:
        cx = 24
        ky = 300
        o += [
            f'<circle class="halo" cx="{cx + 4}" cy="{ky - 4}" r="4" fill="{pal["accent"]}"/>',
            f'<circle cx="{cx + 4}" cy="{ky - 4}" r="4" fill="{pal["accent"]}"/>',
            f'<text class="kick" x="{cx + 16}" y="{ky}">open-source contributor · Rennes SB</text>',
            f'<text class="name" x="{cx}" y="{ky + 44}" fill="url(#tg)">Younes Beriane</text>',
            f'<text class="line" x="{cx}" y="{ky + 76}">I find real bugs in other people\'s</text>',
            f'<text class="line" x="{cx}" y="{ky + 98}">projects and send small, tested fixes.</text>',
        ]
        ty = ky + 122
        tiles = [(cx, 206, "n-prs", prs, "MERGED PRS"), (cx + 226, 206, "n-projects", projects, "PROJECTS")]
        for tx, tw, cls, n, lbl in tiles:
            o += [
                f'<rect x="{tx}" y="{ty}" width="{tw}" height="66" rx="12" fill="{pal["surface"]}" stroke="{pal["border"]}"/>',
                f'<text class="num" x="{tx + 16}" y="{ty + 34}"><tspan class="{cls}">{n}</tspan></text>',
                f'<text class="lbl" x="{tx + 16}" y="{ty + 53}">{lbl}</text>',
            ]
        fy = ty + 82
        o += [
            f'<rect x="{cx}" y="{fy}" width="432" height="44" rx="12" fill="{pal["surface"]}" stroke="{pal["border"]}"/>',
            f'<text class="fact" x="{cx + 16}" y="{fy + 28}">CompTIA Security+</text>',
            f'<text class="foot" x="{cx}" y="{H - 40}">yb@drakeo338 · younesberiane.github.io</text>',
            f'<text class="memo" x="{cx}" y="{H - 20}">In memory of Drakeo the Ruler (1993-2021)</text>',
        ]
    else:
        cx = 396
        ky = 76
        o += [
            f'<circle class="halo" cx="{cx + 4}" cy="{ky - 4}" r="4" fill="{pal["accent"]}"/>',
            f'<circle cx="{cx + 4}" cy="{ky - 4}" r="4" fill="{pal["accent"]}"/>',
            f'<text class="kick" x="{cx + 16}" y="{ky}">open-source contributor · Rennes School of Business</text>',
            f'<text class="name" x="{cx}" y="{ky + 48}" fill="url(#tg)">Younes Beriane</text>',
            f'<text class="line" x="{cx}" y="{ky + 82}">I find real bugs in other people\'s projects</text>',
            f'<text class="line" x="{cx}" y="{ky + 104}">and send small, tested fixes.</text>',
        ]
        ty = ky + 126
        tiles = [(cx, 150, "MERGED PRS", "n-prs", prs), (cx + 162, 150, "PROJECTS", "n-projects", projects)]
        for tx, tw, lbl, cls, n in tiles:
            o += [
                f'<rect x="{tx}" y="{ty}" width="{tw}" height="64" rx="12" fill="{pal["surface"]}" stroke="{pal["border"]}"/>',
                f'<text class="num" x="{tx + 16}" y="{ty + 33}"><tspan class="{cls}">{n}</tspan></text>',
                f'<text class="lbl" x="{tx + 16}" y="{ty + 51}">{lbl}</text>',
            ]
        tx = cx + 324
        o += [
            f'<rect x="{tx}" y="{ty}" width="{W - 36 - tx}" height="64" rx="12" fill="{pal["surface"]}" stroke="{pal["border"]}"/>',
            f'<text class="fact" x="{tx + 16}" y="{ty + 33}">CompTIA Security+</text>',
            f'<text class="lbl" x="{tx + 16}" y="{ty + 51}">CERTIFICATION</text>',
            f'<text class="foot" x="36" y="{H - 16}">yb@drakeo338 · younesberiane.github.io</text>',
            f'<text class="memo" x="{W - 36}" y="{H - 16}" text-anchor="end">In memory of Drakeo the Ruler (1993-2021)</text>',
        ]
    o.append("</svg>")
    return "\n".join(o) + "\n"


# ---------------------------------------------------------------- terminal
def terminal(prs, projects, mobile=False):
    W = 480 if mobile else 960
    fs = 13.5 if mobile else 15.5
    lh = 22 if mobile else 25
    pad_x = 16 if mobile else 20
    bar_h = 40
    if mobile:
        lines = [
            ("cmd", "cat role.txt"),
            ("out", "MSc Digital Marketing Management student"),
            ("hi", "Rennes School of Business"),
            ("cmd", "cat status.txt"),
            ("out", "Looking for a work-study position or an"),
            ("out", "internship in digital marketing."),
            ("cmd", "ls certs/"),
            ("hi", "CompTIA Security+"),
            ("cmd", "cat open-source.txt"),
            ("out", f"{projects} projects ({prs} PRs), every one merged"),
            ("out", "into someone else's repository. Small PRs,"),
            ("out", "real fixes, tests included. Sorted by"),
            ("out", "stars below."),
            ("caret", ""),
        ]
    else:
        lines = [
            ("cmd", "cat role.txt"),
            ("out", "MSc Digital Marketing Management student"),
            ("hi", "Rennes School of Business"),
            ("cmd", "cat status.txt"),
            ("out", "Looking for a work-study position or an internship in digital marketing."),
            ("cmd", "ls certs/"),
            ("hi", "CompTIA Security+"),
            ("cmd", "cat open-source.txt"),
            ("out", f"{projects} projects ({prs} PRs), every one merged into someone else's repository."),
            ("out", "Small PRs, real fixes, tests included. Sorted by stars below."),
            ("caret", ""),
        ]
    body_top = bar_h + 16
    H = body_top + len(lines) * lh + 10
    title = "Terminal: " + " ".join(t for k, t in lines if t)

    css = font_face() + (
        f"text{{font-family:{MONO};font-size:{fs}px;}}"
        f".cmd{{fill:{TERM['muted']};}}.out{{fill:{TERM['text']};}}.hi{{fill:{TERM['hi']};}}"
        f".pr{{fill:{TERM['prompt']};font-weight:700;}}.ttl{{fill:{TERM['muted']};font-size:11.5px;letter-spacing:.02em;}}"
        f".ap{{opacity:0;animation:appear .01s linear forwards;}}"
        f".caret{{fill:{TERM['prompt']};animation:blink 1s steps(1) infinite;}}"
        "@keyframes appear{to{opacity:1;}}@keyframes blink{50%{opacity:0;}}"
    )
    o = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">',
        f"<title id=\"t\">{esc(title)}</title>",
        f"<defs><style>{css}</style>",
        f'<clipPath id="r"><rect x="0" y="0" width="{W}" height="{H}" rx="12"/></clipPath>',
    ]
    body = [
        f'<g clip-path="url(#r)"><rect width="{W}" height="{H}" fill="{TERM["bg"]}"/>',
        f'<rect width="{W}" height="{bar_h}" fill="{TERM["bar"]}"/>',
        f'<line x1="0" y1="{bar_h + .5}" x2="{W}" y2="{bar_h + .5}" stroke="{TERM["border"]}"/></g>',
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="none" stroke="{TERM["border"]}"/>',
        f'<circle cx="{pad_x + 5}" cy="{bar_h / 2}" r="5" fill="{TERM["d1"]}"/>',
        f'<circle cx="{pad_x + 21}" cy="{bar_h / 2}" r="5" fill="{TERM["d2"]}"/>',
        f'<circle cx="{pad_x + 37}" cy="{bar_h / 2}" r="5" fill="{TERM["d3"]}"/>',
        f'<text class="ttl" x="{W - pad_x}" y="{bar_h / 2 + 4}" text-anchor="end">drakeo338@github — ~</text>',
    ]
    t = 0.5  # timeline in seconds
    per_char = 0.045
    out_x = pad_x + round(fs * CH * 2.2)
    for i, (kind, text) in enumerate(lines):
        y = body_top + i * lh + fs * 0.8
        if kind == "cmd":
            # Slack: a scaled-down <img> snaps glyph advances to whole pixels, so the drawn
            # text runs up to ~10% wider than the nominal advance; nothing follows a command,
            # so a wider clip is invisible.
            w = len(text) * fs * CH * 1.12 + fs
            o.append(
                f'<clipPath id="c{i}"><rect x="{out_x}" y="{y - fs}" width="0" height="{lh}">'
                f'<animate attributeName="width" from="0" to="{w:.0f}" begin="{t:.2f}s" dur="{len(text) * per_char:.2f}s" fill="freeze"/></rect></clipPath>'
            )
            body.append(f'<text class="pr ap" style="animation-delay:{t:.2f}s" x="{pad_x}" y="{y}">❯</text>')
            body.append(f'<text class="cmd" clip-path="url(#c{i})" x="{out_x}" y="{y}">{esc(text)}</text>')
            t += len(text) * per_char + 0.3
        elif kind == "caret":
            body.append(f'<text class="pr ap" style="animation-delay:{t:.2f}s" x="{pad_x}" y="{y}">❯</text>')
            body.append(
                f'<rect class="caret ap" style="animation:appear .01s linear {t:.2f}s forwards,blink 1s steps(1) {t:.2f}s infinite" '
                f'x="{out_x}" y="{y - fs * 0.85}" width="{fs * 0.55:.1f}" height="{fs * 1.1:.1f}"/>'
            )
        else:
            body.append(f'<text class="{kind} ap" style="animation-delay:{t:.2f}s" x="{out_x}" y="{y}">{esc(text)}</text>')
            t += 0.12
            if i + 1 < len(lines) and lines[i + 1][0] in ("cmd", "caret"):
                t += 0.35
    o.append("</defs>")
    o += body
    o.append("</svg>")
    return "\n".join(o) + "\n"


def main():
    prs, projects = counts()
    (ASSETS / "card-dark.svg").write_text(card(DARK, prs, projects))
    (ASSETS / "card-light.svg").write_text(card(LIGHT, prs, projects))
    (ASSETS / "card-dark-m.svg").write_text(card(DARK, prs, projects, mobile=True))
    (ASSETS / "card-light-m.svg").write_text(card(LIGHT, prs, projects, mobile=True))
    (ASSETS / "terminal.svg").write_text(terminal(prs, projects))
    (ASSETS / "terminal-m.svg").write_text(terminal(prs, projects, mobile=True))
    print(f"built assets for {projects} projects ({prs} PRs)")


if __name__ == "__main__":
    main()
