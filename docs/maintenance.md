# Profile maintenance

GitHub renders the root `README.md` of the public `rucNick/rucNick` repository on
[the profile](https://github.com/rucNick).

- Edit the introduction, technology labels and project links in `README.md`.
- `assets/hero.svg` and `assets/wave.svg` are original, script-free SVG animations.
  They respect the visitor's reduced-motion preference.
- `assets/frontend.svg`, `backend.svg`, and `cloud.svg` are vendored Skill Icons.
  See `assets/THIRD_PARTY.md` for attribution and the included license.
- The contribution snake has light and dark variants. The pinned
  [Platane/snk](https://github.com/Platane/snk) action reads the contribution graph
  and publishes generated assets to `output` daily at 08:23 UTC. The main branch
  stays free of daily asset commits. GitHub may delay scheduled jobs; a manual
  run is available in Actions → Refresh contribution snake → Run workflow.
- The workflow uses only GitHub's built-in repository token, with repository
  contents write access for publishing. No personal access token is required.
- GitHub can pause scheduled workflows after 60 days of repository inactivity.
  Re-enable or manually run the workflow if the animation stops refreshing.
- The snake is an animation of the contribution calendar, not a live widget or a
  count of all work. Its available data depends on GitHub's contribution visibility.

All profile artwork and technology icons are served from this repository. The
README does not depend on a third-party stats-card or typing-banner service.
