# Profile maintenance

GitHub renders the root `README.md` of the public `rucNick/rucNick` repository on
[the profile](https://github.com/rucNick).

- Keep the name `Rui Cao.`, English-only text, and the approved Waves design.
- The header and contribution snake animate. Technology stack panels stay static.
- Desktop stack panels use two columns; mobile panels use one. `README.md` selects
  the appropriate SVG using picture sources, including light and dark variants.
- Edit technology labels in `scripts/build-profile-assets.py` and regenerate with
  `python3 scripts/build-profile-assets.py`. Header artwork is shared with the
  approved local preview via `scripts/build-profile-preview.py`.
- `assets/frontend.svg`, `backend.svg`, and `cloud.svg` are vendored Skill Icons.
  See `assets/THIRD_PARTY.md` for attribution and the included license.
- `assets/ai.svg` shows Claude Code, Codex, Unsloth, PyTorch, Transformers and MCP.
- The snake workflow refreshes the `output` branch daily at 08:23 UTC. It can also
  be run manually under Actions. It uses GitHub's repository token, not a personal
  access token. Both animation types respect reduced-motion preferences.

All artwork is served from this repository. The controls in `docs/preview/` are
local review tools and are not included in the profile README.
