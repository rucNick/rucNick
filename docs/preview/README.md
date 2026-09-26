# Local animation preview

From the repository root, generate the preview assets first:

```bash
python3 scripts/build-profile-preview.py
```

Then open `index.html` directly, or serve this directory with:

```bash
python3 -m http.server 18765 --bind 127.0.0.1 --directory docs/preview
```

The preview uses the selected Waves artwork and contribution snake, with light
and dark themes and a motion toggle. All technology icons stay static. AI
engineering lists Claude Code, Codex, Unsloth, PyTorch, Transformers and MCP.
Text is English-only; the name is `Rui Cao.`. The original circuit banner,
waving hand, introductory slogans and project showcase remain absent.

The snake is copied from the previously generated `origin/output` contribution
snapshot. It represents actual historical GitHub contribution data, not new or
live activity. The other animations are original SVG artwork. Technology icons
derive from [Skill Icons](https://github.com/tandpfun/skill-icons); their license
and attribution remain in `../../assets/`.

Regenerate the preview artwork from the repository root with:

```bash
python3 scripts/build-profile-preview.py
```

This command reads local files and Git objects only. It does not update the root
README, create a workflow, push commits or change GitHub settings. The Waves and
static-stack design has been approved. Preview buttons are local tools and are
not part of the published GitHub README.
