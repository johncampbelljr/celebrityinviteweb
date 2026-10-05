# Celebrity Invite — iOS app handoff brief

This document is a self-contained brief for building the **Celebrity Invite** iOS app. It was written from the finished marketing site in this repo (`../index.html`), which is the source of truth for the game rules, copy voice, and visual identity.

**How to use this:** start a new Claude Code session in the *app* repo (not this one), and open with something like:

> I'm building the Celebrity Invite iOS app. Read the brief at
> `~/git/celebrityinviteweb/handoff/APP_BRIEF.md` and the roster at
> `~/git/celebrityinviteweb/handoff/celebrities.json`. Let's start with the project scaffold.

---

## 1. What the app is

A **social party game for two or more people sharing one iPhone.** The app deals famous people one at a time; the players decide together who earns one of ten seats at an imaginary party.

It is deliberately *not* a solo swiping game. The phone is a prop for a conversation — the fun is people arguing out loud about whether Snoop Dogg deserves a seat more than Morgan Freeman.

## 2. The rules (authoritative — the site copy was corrected twice to get these right)

There are two roles:

- **The Dealer** holds the phone for the entire game. They deal one celebrity at a time and tap in every verdict. The phone never leaves their hands.
- **The Host** (one person, or a whole room) **never touches the phone.** They rule on each celebrity out loud — in or out — and must give a reason. *"He'd bring the espresso"* counts; silence doesn't.

The loop:

1. Dealer reveals a celebrity.
2. Host rules invite-or-pass, out loud, with a stated reason. Group play: the room debates, Host has the final call.
3. Dealer taps the verdict in. Invites decrement from ten.
4. At the tenth invite, a **Party Page** reveals the full guest list with a celebratory moment.
5. Next round, the players **swap roles.**

Design consequences worth respecting in the UI:

- The screen is read by the Dealer but **seen by the room** — favor large type and a card that's legible at arm's length across a table.
- The reason-giving is the heart of the game. The app should *prompt* for it (a "now say why" beat) without trying to capture or validate it — no text entry, no scoring. Don't let the phone do the talking.
- Ten seats is the tension. Keep the remaining-invite count visible at all times.

## 3. Screen flow (minimum viable)

| Screen | Purpose |
|---|---|
| Start | Explain roles briefly, pick number of celebrities/categories if desired, "Deal the first star" |
| Game | The card (avatar, name, category, one-line tagline), remaining-invite counter, filled-seat row, invite/pass controls, a "say why" prompt beat |
| Party Page | All ten guests, a personalized "vibe" summary line, share, play again (with a swap-roles nudge) |

The website's demo section implements this exact loop in JavaScript — read `../index.html` (the `<script>` block, functions `choose`, `renderStack`, `finishParty`, `vibeLine`) for working reference logic, including two behaviors worth keeping:

- **Deck exhaustion:** if the Host passes so many people that the deck runs out before ten seats fill, previously-passed celebrities are reshuffled back in ("Word got out — everyone you passed is back in line 👀").
- **The vibe line:** the Party Page composes a sentence from the category mix, e.g. *"4 movie stars, 3 chart-toppers, 2 world leaders and 1 TV icon — Range. Your party has range."* Four or more categories represented gets the "Range." closer; otherwise it uses a per-category closer.

## 4. Content

`celebrities.json` (next to this file) holds the full roster, ready to drop into the app bundle:

```json
{
  "categories": { "movies": { "emoji": "🎬", "label": "Movies" }, ... },
  "celebrities": [
    {
      "slug": "george-clooney",
      "name": "George Clooney",
      "first": "George",
      "cat": "movies",
      "tag": "Oscar winner. Eternal best-man energy."
    }
  ]
}
```

18 celebrities across five categories: `movies`, `music`, `sports`, `politics`, `tv`. The `first` field is the short name used in toast copy ("George is IN!"). The `tag` is the one-line card description — comic, affectionate, never mean. Match that voice when adding more.

**18 is a starter roster, not a shipping one.** A real game needs enough that repeats are rare across a session — plan for a few hundred, and treat the roster as data you can grow without code changes.

## 5. Visual identity

Pulled verbatim from the site's CSS.

**Palette**

| Token | Hex | Use |
|---|---|---|
| ink | `#241239` | Primary text, phone chrome, footer |
| ink-soft | `#5F4B78` | Secondary text |
| paper | `#FFF7EF` | Page background (warm cream) |
| card | `#FFFFFF` | Card surfaces |
| pink | `#FF3D8F` | Primary accent |
| pink-deep | `#D91C77` | Accent text on light pink |
| orange | `#FF8A3D` | Gradient partner |
| yellow | `#FFC53D` | Confetti, gold details |
| purple | `#8C4DFF` | Secondary accent |
| teal | `#12C2B9` | Confetti, accents |
| blue | `#3D7BFF` | Confetti, accents |

Two gradients carry most of the brand: **hot** = `#FF3D8F → #FF8A3D` at 120° (primary buttons, invite action), **cool** = `#8C4DFF → #FF3D8F` at 120° (the download panel).

**Category chips**

| Category | Background | Text | Emoji |
|---|---|---|---|
| movies | `#FFE3EF` | `#C2186B` | 🎬 |
| music | `#EFE5FF` | `#7C3AED` | 🎤 |
| sports | `#DCF6EE` | `#0E8F77` | 🏆 |
| politics | `#E3ECFF` | `#2957D0` | 🏛️ |
| tv | `#FFF1D6` | `#B45309` | ✨ |

**Type** — display face is **Fredoka** (600 weight, tight tracking) for headings, counters, and buttons; body is **Inter**. Fredoka is on Google Fonts under the SIL Open Font License, so it can ship in the app bundle. The iOS fallback for the rounded display face is `.system(.rounded)`, which is close in spirit if you'd rather not bundle a font.

**Feel** — vibrant party: warm cream ground, saturated confetti accents, generous rounding (24px cards, fully-round pills), soft long shadows, playful but not childish. Motion is a real part of it: cards spring and fling, seats pop as they fill, confetti falls at the tenth invite.

## 6. The avatars — read this before you plan assets

The 18 celebrity avatars in `../assets/avatars/*.svg` are **not hand-drawn.** They're generated by `../tools/gen_avatars.py`, a dependency-free Python script where each celebrity is a row of parameters — skin tone, hair style, hair color, outfit, facial hair, glasses, earrings, background gradient — assembled from shared primitive shapes on one common face geometry.

That matters for iOS, because SVG is not a native asset format — Xcode asset catalogs want PDF (vector) or PNG. Three paths, in order of preference:

1. **Port the generator to SwiftUI `Shape`/`Path` code (recommended).** The avatars are only circles, ellipses, and bezier paths. As native drawing code they'd be resolution-independent, animatable, tintable, weigh nothing in the bundle, and — most importantly — stay *parametric*, so adding a celebrity remains a data change rather than an asset-pipeline errand. This is the option that matches how the roster wants to grow.
2. **Convert to PDF for the asset catalog.** Quickest path to pixels on screen. No converter is currently installed on this machine; `brew install librsvg` then `rsvg-convert -f pdf -o out.pdf in.svg` over the folder does it. Fine for prototyping, but each new celebrity means re-running a pipeline.
3. **Render SVG at runtime** via a third-party package (e.g. SVGKit). Adds a dependency for something the app can draw itself; not recommended.

If you take path 1, `gen_avatars.py` is the spec — it's readable, ~350 lines, and the drawing functions map almost one-to-one onto SwiftUI `Path` calls.

**Legal note:** these are stylized cartoon illustrations, deliberately not photographs, and the site carries a disclaimer that no affiliation or endorsement is implied. Keep an equivalent line in the app's About screen. Real celebrity photos would be a licensing problem; the illustrated approach exists specifically to avoid it.

## 7. Decisions already made

- **iOS only.** No Android. (Decided after the site was built — the site now shows a single App Store badge.)
- **Illustrated avatars, not photos.** See above.
- **Vibrant party** visual direction, chosen over a red-carpet-dark and a minimal-light alternative.
- **Ten seats**, one celebrity at a time, reason required out loud.
- Role names **Dealer** and **Host** were invented for the website copy. If you name them differently in the app, tell me and I'll update the site to match.

## 8. Open questions for the app

Things the website didn't have to answer:

- Does the app **prompt** for the reason (a timed beat, a "now say why" card) or stay silent and trust the players?
- Is there any **scoring or judging** across rounds, or is the Party Page the only payoff?
- **Categories as a filter** — let players deal only from Music, or always mix?
- Does the Party Page **persist** (a history of past parties) or evaporate on restart?
- **Share format** — the site copies a text list; the app could render a shareable image of the Party Page, which is a much stronger growth loop.
- How does the roster **update** — bundled and shipped with app updates, or fetched so new celebrities can arrive without a release?

## 9. Related files

| Path | What it is |
|---|---|
| `../index.html` | The finished marketing site — game rules in copy, plus a working JS implementation of the game loop in the demo section |
| `../tools/gen_avatars.py` | Parametric avatar generator; the spec for a SwiftUI port |
| `../assets/avatars/*.svg` | 18 rendered avatars |
| `./celebrities.json` | The roster, app-ready |

The site is also published as a shareable page: https://claude.ai/code/artifact/1a7b8239-d8ef-44e2-b0cc-35d8a2f0495e
