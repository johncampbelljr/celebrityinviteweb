# Celebrity Invite — marketing site

Single-page marketing site for **Celebrity Invite**, an iOS party game for two or more
people sharing one phone: the *Dealer* deals famous people one at a time, the *Host*
rules each one in or out — out loud, with a reason — until ten party seats are full.

The site is a hand-written static page with no build step and no dependencies.

## Structure

| Path | What it is |
|---|---|
| `index.html` | The entire site — markup, styles, and the playable demo game |
| `assets/avatars/` | 18 illustrated celebrity avatars (SVG) |
| `assets/favicon.svg` | Site icon |
| `tools/gen_avatars.py` | Parametric generator that renders every avatar; no dependencies |
| `roster/celebrities.json` | Celebrity roster with avatar parameters (schema-versioned) |
| `handoff/` | Brief and app-ready roster for building the iOS app |

## Local preview

```bash
python3 -m http.server 4173
```

Then open <http://localhost:4173>.

## Regenerating avatars

Avatars are generated, not hand-drawn. Add a celebrity to the spec table in
`tools/gen_avatars.py`, then:

```bash
python3 tools/gen_avatars.py
```

This rewrites `assets/avatars/*.svg` and `assets/favicon.svg`. To show a new celebrity
in the site's demo game, also add a matching entry to the `CELEBS` array in `index.html`.

## Note on likenesses

Celebrity avatars are stylized illustrations, not photographs. The site carries a
disclaimer that no affiliation with or endorsement by any person depicted is implied.
