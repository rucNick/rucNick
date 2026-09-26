#!/usr/bin/env python3
"""Vendor pinned MIT-licensed Skill Icons using gh and the Python standard library."""
import base64
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET

REVISION = "7f7e691e71aec64e8354bf697835e009d1ad80f8"
ASSETS = Path(__file__).resolve().parents[1] / "assets"
GROUPS = {
    "frontend": ["React-Dark", "NextJS-Dark", "TypeScript", "TailwindCSS-Dark", "Flutter-Dark", "Dart-Dark"],
    "backend": ["Java-Dark", "Spring-Dark", "Python-Dark", "PostgreSQL-Dark", "Redis-Dark", "Kafka"],
    "cloud": ["GCP-Dark", "Docker", "GithubActions-Dark", "Linux-Dark"],
}
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)


def fetch(path):
    encoded = subprocess.check_output([
        "gh", "api", f"repos/tandpfun/skill-icons/contents/{path}?ref={REVISION}",
        "--jq", ".content",
    ], text=True)
    return base64.b64decode(encoded)


def build(group):
    name, icons = group
    root = ET.Element(f"{{{NS}}}svg", {
        "viewBox": f"0 0 {len(icons) * 58 - 6} 52", "role": "img", "aria-labelledby": "title",
    })
    ET.SubElement(root, f"{{{NS}}}title", {"id": "title"}).text = ", ".join(icons).replace("-Dark", "")
    for index, icon in enumerate(icons):
        source = ET.fromstring(fetch(f"icons/{icon}.svg"))
        ids = {element.get("id"): f"i{index}-{element.get('id')}" for element in source.iter() if element.get("id")}
        for element in source.iter():
            for key, value in list(element.attrib.items()):
                if key == "id":
                    element.set(key, ids[value])
                else:
                    value = re.sub(r"url\(#([^)]*)\)", lambda m: f"url(#{ids[m[1]]})", value)
                    if key.endswith("href") and value.startswith("#"):
                        value = "#" + ids[value[1:]]
                    element.set(key, value)
        source.set("x", str(index * 58))
        source.set("y", "0")
        source.set("width", "52")
        source.set("height", "52")
        root.append(source)
    ET.ElementTree(root).write(ASSETS / f"{name}.svg", encoding="unicode")
    return f"Built {name}.svg ({len(icons)} icons)"


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    with ThreadPoolExecutor(max_workers=3) as pool:
        for result in pool.map(build, GROUPS.items()):
            print(result)
    (ASSETS / "SKILL_ICONS_LICENSE").write_bytes(fetch("LICENSE"))
