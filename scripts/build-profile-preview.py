#!/usr/bin/env python3
"""Build a self-contained local preview; never publishes or calls GitHub."""
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "docs/preview/assets"
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)


def hero(theme, moving):
    dark = theme == "dark"
    ink, muted = ("#f5f5f7", "#a9aabd") if dark else ("#22222a", "#6c6c7c")
    bg, line = ("#16161e", "#30303e") if dark else ("#f8f8fd", "#e5e5ef")
    colors = ["#8b86ff", "#60c6b2", "#ffad72", "#d790ee"]
    motion = """.ribbon{stroke-dasharray:120 42;animation:flow 8s linear infinite}
    .ribbon.alt{animation-direction:reverse;animation-duration:11s}
    .spark{transform-box:fill-box;transform-origin:center;animation:spin 9s linear infinite}
    .underline{transform-origin:48px 177px;animation:stretch 4s ease-in-out infinite}
    @keyframes flow{to{stroke-dashoffset:-648}}
    @keyframes spin{to{transform:rotate(360deg)}}
    @keyframes stretch{0%,100%{transform:scaleX(.65)}50%{transform:scaleX(1)}}
    @media(prefers-reduced-motion:reduce){.ribbon,.spark,.underline{animation:none}}
    """ if moving else ""
    art = f'''<g fill="none" stroke-width="24" stroke-linecap="round">
        <path class="ribbon" d="M552 40C680 40 620 218 776 218S910 24 940 36" stroke="{colors[0]}"/>
        <path class="ribbon alt" d="M520 97C645 -10 705 293 872 113" stroke="{colors[1]}"/>
        <path class="ribbon" d="M562 202C605 272 738 12 868 63" stroke="{colors[2]}" stroke-width="15"/>
        </g>'''
    return f'''<svg xmlns="{NS}" viewBox="0 0 880 270" role="img" aria-labelledby="title desc">
    <title id="title">Rui Cao.</title><desc id="desc">Rui Cao, @rucNick, with flowing Waves artwork.</desc>
    <defs><clipPath id="clip"><rect x="1" y="1" width="878" height="268" rx="20"/></clipPath>
    <linearGradient id="accent"><stop stop-color="#8b86ff"/><stop offset=".5" stop-color="#60c6b2"/><stop offset="1" stop-color="#ffad72"/></linearGradient></defs>
    <style>text{{font-family:Arial,Helvetica,sans-serif}}{motion}</style>
    <rect x="1" y="1" width="878" height="268" rx="20" fill="{bg}" stroke="{line}"/>
    <g clip-path="url(#clip)">{art}</g>
    <text x="47" y="151" font-size="84" font-weight="700" letter-spacing="-4" fill="{ink}">Rui Cao.</text>
    <rect class="underline" x="50" y="175" width="265" height="5" rx="2.5" fill="url(#accent)"/>
    <text x="52" y="215" font-size="17" letter-spacing="1.5" fill="{muted}">@rucNick</text>
    <g class="spark" stroke="{colors[2]}" stroke-width="3" stroke-linecap="round"><path d="M425 66V88M414 77H436"/></g>
    </svg>'''


def stack(name):
    if name == "ai":
        badges = [
            (1, 1, 120, "Claude Code", "#efb69b"),
            (129, 1, 90, "Codex", "#b5d8fa"),
            (227, 1, 112, "Unsloth", "#a8f0c6"),
            (1, 47, 102, "PyTorch", "#ffb293"),
            (111, 47, 140, "Transformers", "#efdc94"),
            (259, 47, 80, "MCP", "#c8b8ff"),
        ]
        art = [f'<svg xmlns="{NS}" viewBox="0 0 340 88" role="img" aria-labelledby="title">',
               '<title id="title">Claude Code, Codex, Unsloth, PyTorch, Transformers and MCP</title>']
        for x, y, width, label, color in badges:
            art.append(f'<rect x="{x}" y="{y}" width="{width}" height="40" rx="9" fill="#152332" stroke="#334a5e"/>')
            art.append(f'<text x="{x+width/2:g}" y="{y+25}" fill="{color}" font-family="Arial,Helvetica,sans-serif" font-size="14" font-weight="600" text-anchor="middle">{label}</text>')
        art.append('</svg>')
        (DEST / "ai-static.svg").write_text("\n".join(art))
        return
    (DEST / f"{name}-static.svg").write_bytes((ROOT / "assets" / f"{name}.svg").read_bytes())


def snake(theme):
    file = "github-snake-dark.svg" if theme == "dark" else "github-snake.svg"
    data = subprocess.check_output(["git", "show", f"origin/output:{file}"], cwd=ROOT, text=True)
    tree = ET.fromstring(data)
    # Keep the upstream animation; add an accessible reduced-motion fallback.
    css = ET.SubElement(tree, f"{{{NS}}}style")
    css.text = "@media(prefers-reduced-motion:reduce){*{animation:none!important}}"
    ET.ElementTree(tree).write(DEST / f"snake-{theme}-animated.svg", encoding="unicode")
    css.text = "*{animation:none!important}"
    ET.ElementTree(tree).write(DEST / f"snake-{theme}-still.svg", encoding="unicode")


if __name__ == "__main__":
    DEST.mkdir(parents=True, exist_ok=True)
    for theme in ("light", "dark"):
        for moving in (True, False):
            suffix = "animated" if moving else "still"
            (DEST / f"hero-waves-{theme}-{suffix}.svg").write_text(hero(theme, moving))
    for name in ("frontend", "backend", "ai", "cloud"):
        stack(name)
    for theme in ("light", "dark"):
        snake(theme)
    print(f"Built Waves, static stack icons and snake preview assets in {DEST}")
