#!/usr/bin/env python3
"""Generate flat illustrated celebrity avatars (SVG) for the Celebrity Invite site.
All avatars share one face geometry; hair / outfit / accessories vary per person.
Canvas: 240x240, full-bleed circle background with a brand gradient.
"""
import math, os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "assets", "avatars")
INK = "#2B1B2E"

# ---------------------------------------------------------------- primitives

def grad(gid, a, b):
    return (f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>')

def sparkles():
    pts = [(40, 56, 4, .5), (196, 42, 3, .45), (208, 148, 4.5, .3),
           (26, 148, 3, .38), (168, 24, 3.5, .5), (66, 26, 2.5, .4)]
    return "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFFFFF" opacity="{o}"/>' for x, y, r, o in pts)

SHOULDERS = "M40,246 C40,198 75,168 120,168 C165,168 200,198 200,246 L200,252 L40,252 Z"

def neck(skin):
    return f'<rect x="106" y="132" width="28" height="44" rx="9" fill="{skin}"/>'

def head(skin):
    return f'<ellipse cx="120" cy="112" rx="46" ry="50" fill="{skin}"/>'

def ears(skin):
    return (f'<circle cx="73" cy="115" r="9" fill="{skin}"/>'
            f'<circle cx="167" cy="115" r="9" fill="{skin}"/>')

def blush(strong=False):
    o = .45 if strong else .3
    return (f'<ellipse cx="93" cy="128" rx="7.5" ry="4.5" fill="#FF7BAC" opacity="{o}"/>'
            f'<ellipse cx="147" cy="128" rx="7.5" ry="4.5" fill="#FF7BAC" opacity="{o}"/>')

def eyes():
    return (f'<circle cx="102" cy="114" r="5.2" fill="{INK}"/>'
            f'<circle cx="138" cy="114" r="5.2" fill="{INK}"/>'
            f'<circle cx="100.2" cy="112.2" r="1.7" fill="#FFFFFF"/>'
            f'<circle cx="136.2" cy="112.2" r="1.7" fill="#FFFFFF"/>')

def brows(color, raised_right=False):
    left = f'<path d="M90,100 Q100,92 112,96" stroke="{color}" stroke-width="5" stroke-linecap="round" fill="none"/>'
    if raised_right:
        right = f'<path d="M128,92 Q140,84 151,90" stroke="{color}" stroke-width="5" stroke-linecap="round" fill="none"/>'
    else:
        right = f'<path d="M128,96 Q140,92 150,100" stroke="{color}" stroke-width="5" stroke-linecap="round" fill="none"/>'
    return left + right

def mouth_smile():
    return f'<path d="M103,133 Q120,149 137,133" stroke="{INK}" stroke-width="5.5" stroke-linecap="round" fill="none"/>'

def mouth_grin():
    return (f'<path d="M101,131 C107,150 133,150 139,131 C127,137 113,137 101,131 Z" fill="#8C3A46"/>'
            f'<path d="M105,132 C112,138 128,138 135,132 C125,135.5 115,135.5 105,132 Z" fill="#FFFFFF"/>')

def mouth_lips():
    return (f'<path d="M104,133 Q120,147 136,133 Q120,153 104,133 Z" fill="#E0284F"/>'
            f'<path d="M104,133 Q120,141 136,133" stroke="#B01C3E" stroke-width="1.5" fill="none" opacity=".6"/>')

def mouth_beard():  # subtle lip line for bearded faces
    return f'<path d="M110,143 Q120,150 130,143" stroke="#2B1B2E" stroke-width="4" stroke-linecap="round" fill="none" opacity=".55"/>'

def beard_full(color):
    return ('<path d="M76,104 C76,152 94,174 120,174 C146,174 164,152 164,104 '
            'C164,118 160,138 150,150 C140,160 130,163 120,163 C110,163 100,160 90,150 '
            f'C80,138 76,118 76,104 Z" fill="{color}"/>')

def mustache(color):
    return ('<path d="M103,128 C108,121 116,124 120,128 C124,124 132,121 137,128 '
            f'C133,134 125,135 120,131 C115,135 107,134 103,128 Z" fill="{color}"/>')

def goatee(color):
    return (f'<ellipse cx="120" cy="158" rx="13" ry="8" fill="{color}"/>' + mustache(color))

def sunglasses():
    return ('<path d="M84,104 L74,109" stroke="#241239" stroke-width="4" stroke-linecap="round"/>'
            '<path d="M156,104 L166,109" stroke="#241239" stroke-width="4" stroke-linecap="round"/>'
            '<rect x="84" y="101" width="30" height="21" rx="8" fill="#241239"/>'
            '<rect x="126" y="101" width="30" height="21" rx="8" fill="#241239"/>'
            '<path d="M114,108 Q120,104 126,108" stroke="#241239" stroke-width="4" fill="none"/>'
            '<rect x="88" y="105" width="10" height="4" rx="2" fill="#FFFFFF" opacity=".35"/>'
            '<rect x="130" y="105" width="10" height="4" rx="2" fill="#FFFFFF" opacity=".35"/>')

def tintglasses():
    return ('<path d="M84,104 L74,109" stroke="#C2186B" stroke-width="3.5" stroke-linecap="round"/>'
            '<path d="M156,104 L166,109" stroke="#C2186B" stroke-width="3.5" stroke-linecap="round"/>'
            '<rect x="83" y="99" width="32" height="25" rx="10" fill="#FF5FA2" opacity=".55"/>'
            '<rect x="125" y="99" width="32" height="25" rx="10" fill="#FF5FA2" opacity=".55"/>'
            '<rect x="83" y="99" width="32" height="25" rx="10" fill="none" stroke="#C2186B" stroke-width="3.5"/>'
            '<rect x="125" y="99" width="32" height="25" rx="10" fill="none" stroke="#C2186B" stroke-width="3.5"/>'
            '<path d="M115,109 Q120,105 125,109" stroke="#C2186B" stroke-width="3.5" fill="none"/>')

def earrings(kind="stud"):
    if kind == "hoop":
        return ('<circle cx="72" cy="133" r="7" fill="none" stroke="#FFC53D" stroke-width="3.5"/>'
                '<circle cx="168" cy="133" r="7" fill="none" stroke="#FFC53D" stroke-width="3.5"/>')
    return ('<circle cx="72" cy="128" r="4.5" fill="#FFC53D" stroke="#E8A21C" stroke-width="1.5"/>'
            '<circle cx="168" cy="128" r="4.5" fill="#FFC53D" stroke="#E8A21C" stroke-width="1.5"/>')

# ---------------------------------------------------------------- hair styles

def hair_short(c):
    return ('<path d="M75,108 C71,68 92,50 120,50 C148,50 169,68 165,108 '
            f'C163,84 146,71 120,71 C94,71 77,84 75,108 Z" fill="{c}"/>')

def hair_buzz(c):
    return ('<path d="M75,106 C71,68 92,50 120,50 C148,50 169,68 165,106 '
            f'C162,82 146,64 120,64 C94,64 78,82 75,106 Z" fill="{c}"/>')

def hair_quiff(c):
    return ('<path d="M75,108 C71,68 86,44 116,47 C136,36 166,52 166,102 '
            f'C164,76 150,62 122,61 C96,61 80,84 75,108 Z" fill="{c}"/>')

def hair_part(c):  # short with a middle part notch
    return ('<path d="M75,106 C71,66 94,48 120,48 C146,48 169,66 165,106 '
            'C160,80 144,68 124,66 L120,75 L116,66 '
            f'C96,68 80,82 75,106 Z" fill="{c}"/>')

def hair_bob_back(c):
    return ('<path d="M68,114 C62,50 96,40 120,40 C144,40 178,50 172,114 '
            f'C172,150 160,168 148,168 L92,168 C80,168 68,150 68,114 Z" fill="{c}"/>')

def hair_bob_bangs(c):
    return ('<path d="M78,104 C76,60 96,50 120,50 C144,50 164,60 162,104 '
            f'C150,82 138,79 120,79 C102,79 90,82 78,104 Z" fill="{c}"/>')

def hair_long_back(c):
    return ('<path d="M70,116 C64,48 100,36 120,36 C140,36 176,48 170,116 '
            'C173,150 173,172 167,190 C162,200 153,203 147,197 L93,197 '
            f'C87,203 78,200 73,190 C67,172 67,150 70,116 Z" fill="{c}"/>')

def hair_waves_extra(c):
    return "".join(f'<circle cx="{x}" cy="{y}" r="16" fill="{c}"/>'
                   for x, y in [(76, 184), (104, 194), (136, 194), (164, 184)])

def hair_curls(c, big=False):
    circles = [(86, 72, 20), (108, 57, 22), (132, 57, 22), (154, 72, 20),
               (72, 92, 17), (168, 92, 17), (66, 114, 15), (174, 114, 15)]
    if big:
        circles += [(68, 138, 14), (172, 138, 14)]
    s = f'<ellipse cx="120" cy="72" rx="46" ry="22" fill="{c}"/>'
    return s + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>' for x, y, r in circles)

def hair_afro_ring(c):  # short gray curls (crown ring)
    out = []
    for ang in (150, 122.5, 95, 67.5, 40):
        a = math.radians(ang)
        x = 120 + 47 * math.cos(a)
        y = 106 - 52 * math.sin(a)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="12" fill="{c}"/>')
    return "".join(out)

def hair_ponytail(c, tie):
    tail = ('<path d="M150,48 C196,44 214,84 206,128 C201,158 186,176 172,170 '
            'C164,166 164,156 170,150 C184,136 186,108 172,86 C164,74 154,66 142,62 Z" '
            f'fill="{c}"/>')
    cap = hair_short(c)
    tieel = f'<circle cx="149" cy="55" r="7" fill="{tie}"/>'
    return tail + cap + tieel

def hair_braids_back(c):
    caps = []
    for x, y0, y1 in [(66, 96, 176), (82, 106, 190), (158, 106, 190), (174, 96, 176)]:
        caps.append(f'<rect x="{x-6}" y="{y0}" width="12" height="{y1-y0}" rx="6" fill="{c}"/>')
        caps.append(f'<circle cx="{x}" cy="{y1}" r="4.5" fill="#FFC53D"/>')
    return "".join(caps)

def hair_bun(c, tie):
    return (f'<circle cx="120" cy="40" r="16" fill="{c}"/>'
            f'<ellipse cx="120" cy="55" rx="11" ry="4.5" fill="{tie}"/>' + hair_short(c))

# ---------------------------------------------------------------- outfits

def outfit(kind, slug, c1, c2="#FFFFFF", accent="#FF3D8F"):
    base = f'<path d="{SHOULDERS}" fill="{c1}"/>'
    if kind == "tux":
        v = f'<path d="M97,171 C105,180 135,180 143,171 L124,212 C121,217 119,217 116,212 Z" fill="#FFFFFF"/>'
        bow = ('<path d="M117,176 C107,168 99,168 99,176 C99,184 107,184 117,176 Z" fill="#14091F"/>'
               '<path d="M123,176 C133,168 141,168 141,176 C141,184 133,184 123,176 Z" fill="#14091F"/>'
               '<circle cx="120" cy="176" r="4.5" fill="#14091F"/>')
        return base + v + bow
    if kind == "suit":
        v = f'<path d="M99,171 C106,179 134,179 141,171 L124,206 C121,211 119,211 116,206 Z" fill="{c2}"/>'
        tie = (f'<path d="M116,174 L120,206 L124,174 Z" fill="{accent}"/>'
               f'<rect x="114.5" y="170" width="11" height="7" rx="2.5" fill="{accent}"/>')
        return base + v + tie
    if kind == "blazer":
        v = f'<path d="M99,171 C106,180 134,180 141,171 L126,204 C122,210 118,210 114,204 Z" fill="{c2}"/>'
        lap = (f'<path d="M97,170 L114,204 L104,172 Z" fill="#00000022"/>'
               f'<path d="M143,170 L126,204 L136,172 Z" fill="#00000022"/>')
        return base + v + lap
    if kind == "tee":
        neck_line = '<path d="M104,172 C110,180 130,180 136,172" stroke="#00000030" stroke-width="4" fill="none" stroke-linecap="round"/>'
        return base + neck_line
    if kind == "hoodie":
        strings = ('<path d="M112,178 L110,198" stroke="#FFFFFF" stroke-width="3.5" stroke-linecap="round"/>'
                   '<path d="M128,178 L130,198" stroke="#FFFFFF" stroke-width="3.5" stroke-linecap="round"/>'
                   '<path d="M100,174 C106,182 134,182 140,174" stroke="#00000028" stroke-width="4" fill="none" stroke-linecap="round"/>')
        return base + strings
    if kind == "cardigan":
        v = f'<path d="M100,171 C107,179 133,179 140,171 L125,208 C122,213 118,213 115,208 Z" fill="{c2}"/>'
        btn = '<circle cx="120" cy="212" r="2.4" fill="#00000045"/><circle cx="120" cy="222" r="2.4" fill="#00000045"/>'
        return base + v + btn
    if kind == "sparkle":
        stars = "".join(star(x, y, s) for x, y, s in [(96, 198, 1.0), (140, 190, .8), (118, 224, 1.1), (158, 218, .7), (82, 224, .7)])
        return base + stars
    if kind == "stripes":
        clip = f'<clipPath id="sh-{slug}"><path d="{SHOULDERS}"/></clipPath>'
        bands = "".join(f'<rect x="{x}" y="164" width="16" height="92" fill="{c2}" clip-path="url(#sh-{slug})"/>'
                        for x in (88, 112, 136))
        return clip + base + bands
    return base

def star(x, y, s=1.0):
    p = (f"M{x},{y - 6*s} L{x + 1.8*s},{y - 1.8*s} L{x + 6*s},{y} L{x + 1.8*s},{y + 1.8*s} "
         f"L{x},{y + 6*s} L{x - 1.8*s},{y + 1.8*s} L{x - 6*s},{y} L{x - 1.8*s},{y - 1.8*s} Z")
    return f'<path d="{p}" fill="#FFFFFF" opacity=".85"/>'

def chain_gold():
    return '<path d="M94,178 C104,196 136,196 146,178" stroke="#FFC53D" stroke-width="5" fill="none" stroke-linecap="round"/>'

def necklace_dots():
    pts = []
    for i in range(7):
        t = i / 6
        x = (1-t)**2 * 96 + 2*(1-t)*t * 120 + t**2 * 144
        y = (1-t)**2 * 178 + 2*(1-t)*t * 198 + t**2 * 178
        pts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.2" fill="#FFC53D"/>')
    return "".join(pts)

# ---------------------------------------------------------------- roster

C = dict  # shorthand

CELEBS = [
    C(slug="george-clooney", name="George Clooney", bg=("#8C4DFF", "#FF3D8F"), skin="#EFB98D",
      hair=("part", "#8E939B"), brow="#6E7076", outfit=("tux", "#2B1B45"), mouth="smile", show_ears=True),
    C(slug="taylor-swift", name="Taylor Swift", bg=("#FF3D8F", "#FF8A3D"), skin="#F9D2A6",
      hair=("bob", "#F5D76E"), brow="#C9A24B", outfit=("sparkle", "#7EA8FF"), mouth="lips"),
    C(slug="dwayne-johnson", name="Dwayne Johnson", bg=("#12C2B9", "#3D7BFF"), skin="#B07B4F",
      hair=None, brow="#2B1B12", outfit=("tee", "#241239"), mouth="grin", raised=True,
      facial=("goatee", "#2B1B12"), extra="chain", show_ears=True),
    C(slug="beyonce", name="Beyoncé", bg=("#FFC53D", "#FF3D8F"), skin="#A9713F",
      hair=("waves", "#C98A3D"), brow="#6B4423", outfit=("sparkle", "#FFD75E"), mouth="grin", ear="hoop"),
    C(slug="keanu-reeves", name="Keanu Reeves", bg=("#3D7BFF", "#8C4DFF"), skin="#EFB98D",
      hair=("long", "#26201A"), brow="#26201A", outfit=("tee", "#1E1A2E"), mouth="beard",
      facial=("beard", "#3F332A"), tuck=True),
    C(slug="zendaya", name="Zendaya", bg=("#FF8A3D", "#FF3D8F"), skin="#A9713F",
      hair=("curls", "#3B2A20"), brow="#3B2A20", outfit=("blazer", "#E8323C"), mouth="smile", ear="stud"),
    C(slug="barack-obama", name="Barack Obama", bg=("#3D7BFF", "#12C2B9"), skin="#8D5B34",
      hair=("buzz", "#57606B"), brow="#3A3F46", outfit=("suit", "#24345C", "#FFFFFF", "#E0506B"),
      mouth="grin", show_ears=True),
    C(slug="oprah-winfrey", name="Oprah Winfrey", bg=("#8C4DFF", "#FF8A3D"), skin="#8D5B34",
      hair=("curlsbig", "#3B2A20"), brow="#3B2A20", outfit=("blazer", "#7C3AED"), mouth="grin", ear="stud"),
    C(slug="lionel-messi", name="Lionel Messi", bg=("#FF3D8F", "#8C4DFF"), skin="#EFB98D",
      hair=("short", "#6E4B2A"), brow="#6E4B2A", outfit=("stripes", "#FFFFFF", "#86CDEB"),
      mouth="beard", facial=("beard", "#6E4B2A"), show_ears=True),
    C(slug="serena-williams", name="Serena Williams", bg=("#12C2B9", "#FFC53D"), skin="#8D5B34",
      hair=("bun", "#241A12", "#FF3D8F"), brow="#241A12", outfit=("tee", "#FF6F61"), mouth="grin", ear="stud"),
    C(slug="tom-hanks", name="Tom Hanks", bg=("#FF8A3D", "#FFC53D"), skin="#F7C9A3",
      hair=("short", "#9AA0A8"), brow="#7B818A", outfit=("cardigan", "#8A6D5C"), mouth="smile", show_ears=True),
    C(slug="lady-gaga", name="Lady Gaga", bg=("#FF3D8F", "#8C4DFF"), skin="#F9D2A6",
      hair=("long", "#F3E9CF"), brow="#C9A24B", outfit=("sparkle", "#C0C6FF"), mouth="lips", glasses="tint"),
    C(slug="ryan-reynolds", name="Ryan Reynolds", bg=("#12C2B9", "#8C4DFF"), skin="#F1BE93",
      hair=("quiff", "#6E4B2A"), brow="#5A3D22", outfit=("suit", "#55617A", "#FFFFFF", "#241239"),
      mouth="smile", raised=True, show_ears=True),
    C(slug="snoop-dogg", name="Snoop Dogg", bg=("#FFC53D", "#12C2B9"), skin="#6F4326",
      hair=("braids", "#1E1A16"), brow="#1E1A16", outfit=("hoodie", "#3D7BFF"), mouth="smile", glasses="sun"),
    C(slug="ariana-grande", name="Ariana Grande", bg=("#FF7BAC", "#8C4DFF"), skin="#F1BE93",
      hair=("ponytail", "#4A2F1D", "#FF3D8F"), brow="#4A2F1D", outfit=("tee", "#B79CFF"),
      mouth="smile", ear="stud", strongblush=True),
    C(slug="morgan-freeman", name="Morgan Freeman", bg=("#3D7BFF", "#FFC53D"), skin="#6F4326",
      hair=("afro", "#B9BDC4"), brow="#9DA2AB", outfit=("blazer", "#24345C"), mouth="beard",
      facial=("beard", "#B9BDC4"), ear="stud"),
    C(slug="michelle-obama", name="Michelle Obama", bg=("#FF8A3D", "#8C4DFF"), skin="#8D5B34",
      hair=("bob", "#241A12"), brow="#241A12", outfit=("blazer", "#0FA3A3"), mouth="grin", ear="stud"),
    C(slug="elton-john", name="Elton John", bg=("#FF3D8F", "#FFC53D"), skin="#F7C9A3",
      hair=("short", "#B07A45"), brow="#8A5C30", outfit=("sparkle", "#8C4DFF"), mouth="grin",
      glasses="tint", show_ears=True),
]

# ---------------------------------------------------------------- assembly

def render(c):
    slug = c["slug"]
    skin = c["skin"]
    hb, ht = "", ""  # hair back, hair top
    if c.get("hair"):
        style, col, *rest = c["hair"]
        tie = rest[0] if rest else "#FF3D8F"
        if style == "short":     ht = hair_short(col)
        elif style == "buzz":    ht = hair_buzz(col)
        elif style == "quiff":   ht = hair_quiff(col)
        elif style == "part":    ht = hair_part(col)
        elif style == "bob":     hb, ht = hair_bob_back(col), hair_bob_bangs(col)
        elif style == "long":
            hb = hair_long_back(col)
            ht = hair_buzz(col) if c.get("tuck") else hair_part(col)
        elif style == "waves":   hb, ht = hair_long_back(col) + hair_waves_extra(col), hair_part(col)
        elif style == "curls":   ht = hair_curls(col)
        elif style == "curlsbig": ht = hair_curls(col, big=True)
        elif style == "afro":    ht = hair_afro_ring(col)
        elif style == "ponytail": ht = hair_ponytail(col, tie)
        elif style == "braids":  hb, ht = hair_braids_back(col), hair_buzz(col)
        elif style == "bun":     ht = hair_bun(col, tie)

    ok = c["outfit"]
    kind, c1 = ok[0], ok[1]
    c2 = ok[2] if len(ok) > 2 else "#FFFFFF"
    accent = ok[3] if len(ok) > 3 else "#FF3D8F"
    body = outfit(kind, slug, c1, c2, accent)
    if c.get("extra") == "chain":
        body += chain_gold()
    if c.get("extra") == "necklace":
        body += necklace_dots()

    face = blush(c.get("strongblush", False)) + brows(c["brow"], c.get("raised", False)) + eyes()

    facial = ""
    m = c.get("mouth", "smile")
    if c.get("facial"):
        fk, fc = c["facial"]
        facial = beard_full(fc) if fk == "beard" else goatee(fc)
        if fk == "beard":
            facial += mustache(fc)
    if m == "smile":   mouth = mouth_smile()
    elif m == "grin":  mouth = mouth_grin()
    elif m == "lips":  mouth = mouth_lips()
    else:              mouth = mouth_beard()

    glasses = ""
    if c.get("glasses") == "sun":
        glasses = sunglasses()
    elif c.get("glasses") == "tint":
        glasses = tintglasses()

    ear_svg = earrings(c["ear"]) if c.get("ear") else ""
    ears_svg = ears(skin) if c.get("show_ears") else ""

    parts = [
        f'<circle cx="120" cy="120" r="120" fill="url(#bg-{slug})"/>',
        sparkles(),
        hb,
        neck(skin),
        body,
        head(skin),
        ears_svg,
        face,
        facial,
        mouth,
        ht,
        glasses,
        ear_svg,
    ]
    inner = "".join(p for p in parts if p)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240" role="img" '
            f'aria-label="Illustrated avatar of {c["name"]}">'
            f'<title>{c["name"]}</title>'
            f'<defs>{grad("bg-" + slug, *c["bg"])}'
            f'<clipPath id="clip-{slug}"><circle cx="120" cy="120" r="120"/></clipPath></defs>'
            f'<g clip-path="url(#clip-{slug})">{inner}</g></svg>')


def favicon():
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
            '<defs><linearGradient id="f" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="#FF3D8F"/><stop offset="1" stop-color="#FF8A3D"/></linearGradient></defs>'
            '<rect width="64" height="64" rx="15" fill="url(#f)"/>'
            '<path d="M32,14 L36.6,25.4 L48.9,26.3 L39.5,34.3 L42.4,46.3 L32,39.8 L21.6,46.3 L24.5,34.3 L15.1,26.3 L27.4,25.4 Z" fill="#FFFFFF"/>'
            '<circle cx="14" cy="14" r="3" fill="#FFE08A"/>'
            '<circle cx="51" cy="12" r="2.5" fill="#B9F5EF"/>'
            '<circle cx="53" cy="52" r="3" fill="#FFD2E4"/>'
            '<circle cx="12" cy="50" r="2.5" fill="#D8C6FF"/>'
            '</svg>')


def main():
    os.makedirs(OUT, exist_ok=True)
    for c in CELEBS:
        path = os.path.join(OUT, c["slug"] + ".svg")
        with open(path, "w") as f:
            f.write(render(c))
    with open(os.path.join(REPO, "assets", "favicon.svg"), "w") as f:
        f.write(favicon())
    print(f"wrote {len(CELEBS)} avatars + favicon")

if __name__ == "__main__":
    main()
