#!/usr/bin/env python3
"""Render the approved Waves artwork and static, responsive GitHub stack panels."""
from copy import deepcopy
import importlib.util
from pathlib import Path
import re
import textwrap
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)
spec = importlib.util.spec_from_file_location("preview_art", ROOT / "scripts/build-profile-preview.py")
preview = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preview)

GROUPS = [
    ("frontend", "Frontend & mobile", "React · Next.js · TypeScript · Tailwind CSS · Flutter · Dart"),
    ("backend", "Backend & data", "Java · Spring Boot · Python · PostgreSQL · Redis · Kafka"),
    ("ai", "AI engineering", "Claude Code · Codex · Unsloth · PyTorch · Transformers · MCP"),
    ("cloud", "Cloud & workflow", "Google Cloud · Docker · GitHub Actions · Linux"),
]


def text(parent, x, y, label, color, size, weight="400"):
    node = ET.SubElement(parent, f"{{{NS}}}text", {
        "x": str(x), "y": str(y), "fill": color, "font-size": str(size),
        "font-weight": weight, "font-family": "Arial,Helvetica,sans-serif",
    })
    node.text = label


def icon_strip(name, x, y):
    source = deepcopy(ET.parse(ASSETS / f"{name}.svg").getroot())
    ids = {node.get("id"): f"{name}-{node.get('id')}" for node in source.iter() if node.get("id")}
    for node in source.iter():
        for key, value in list(node.attrib.items()):
            if key == "id":
                value = ids[value]
            elif key == "aria-labelledby":
                value = " ".join(ids.get(part, part) for part in value.split())
            else:
                value = re.sub(r"url\(#([^)]*)\)", lambda match: f"url(#{ids[match[1]]})", value)
                if key.endswith("href") and value.startswith("#"):
                    value = "#" + ids[value[1:]]
            node.set(key, value)
    _, _, width, height = map(float, source.get("viewBox").split())
    rendered_width = 198 if name == "cloud" else 300
    source.set("x", str(x))
    source.set("y", str(y))
    source.set("width", str(rendered_width))
    source.set("height", str(rendered_width * height / width))
    return source


def panel(theme, mobile):
    dark = theme == "dark"
    ink, muted = ("#eeedf4", "#9897a6") if dark else ("#23232e", "#71717e")
    root = ET.Element(f"{{{NS}}}svg", {
        "viewBox": "0 0 320 650" if mobile else "0 0 880 318",
        "role": "img", "aria-labelledby": "title description",
    })
    ET.SubElement(root, f"{{{NS}}}title", {"id": "title"}).text = "Rui Cao. — Tech stack"
    ET.SubElement(root, f"{{{NS}}}desc", {"id": "description"}).text = "; ".join(f"{title}: {labels}" for _, title, labels in GROUPS)
    for index, (name, title, labels) in enumerate(GROUPS):
        x = 0 if mobile else (index % 2) * 460
        y = [0, 155, 310, 495][index] if mobile else (index // 2) * 158
        text(root, x, y + 19, title, ink, 16 if mobile else 14, "600")
        lines = textwrap.wrap(labels, width=45 if mobile else 67, break_long_words=False)
        for line_no, line in enumerate(lines):
            text(root, x, y + 45 + line_no * 20, line, muted, 13 if mobile else 12)
        root.append(icon_strip(name, x, y + (80 if mobile else 66)))
    return root


if __name__ == "__main__":
    for theme in ("light", "dark"):
        (ASSETS / f"hero-waves-{theme}.svg").write_text(preview.hero(theme, True))
        for mobile in (False, True):
            kind = "mobile" if mobile else "desktop"
            ET.ElementTree(panel(theme, mobile)).write(ASSETS / f"stack-{kind}-{theme}.svg", encoding="unicode")
    print("Built approved Waves headers and four static responsive stack panels.")
