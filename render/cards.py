"""REMAX Surfside brochure card templates (1080x1350, Facebook 4:5).

Seven formats (f1-f7) x four color schemes. Each template takes a card dict
(see SPEC.md) and returns the card's HTML body. The same templates serve sale
listings (agent block) and vacation rentals (booking block).

Compliance, every card: REMAX Surfside lighthouse logo, office name and address,
"Each Office Independently Owned and Operated", and the office phone, which is
always the largest phone number on the card (OFFICE_PHONE_PX vs AGENT_PHONE_PX).
"""
from html import escape

OFFICE_NAME = "REMAX Surfside"
OFFICE_ADDR = "315 Ocean Street, Suite 24, Cape May, NJ 08204"
OFFICE_PHONE = "609-884-4242"
OFFICE_PHONE_PX = 42
AGENT_PHONE_PX = 28          # hard ceiling for any agent phone; render.py checks it
LOGO = "https://d2td4dobkk213c.cloudfront.net/remaxsurfside9221/profiles/9221_101895927_OfficeLogo_cropped.jpg"

SCHEMES = {
    "classic":  "--red:#FF1200;--blue:#0043FF;--navy:#06205C;--deep:#031338",
    "reverse":  "--red:#0043FF;--blue:#FF1200;--navy:#0B0B0F;--deep:#0B0B0F",
    "midnight": "--red:#FF1200;--blue:#0B0B0F;--navy:#0B0B0F;--deep:#0B0B0F",
    "harbor":   "--red:#FF1200;--blue:#06205C;--navy:#0043FF;--deep:#06205C",
}

FONTS_URL = ("https://fonts.googleapis.com/css2?family=Anton&family=Bebas+Neue&family=Kaushan+Script"
             "&family=DM+Serif+Display:ital@0;1&family=Montserrat:ital,wght@0,400;0,500;0,600;0,700;0,800;0,900;1,500"
             "&family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Oswald:wght@400;500;600;700"
             "&family=Barlow+Condensed:wght@500;600;700;800&display=block")

# Short family names used in the templates -> Google family names.
FAMILY_ALIASES = {"Bebas": "Bebas Neue", "Kaushan": "Kaushan Script", "DMSerif": "DM Serif Display",
                  "Playfair": "Playfair Display", "Barlow": "Barlow Condensed"}

BASE_CSS = """
:root{--red:#FF1200;--blue:#0043FF;--cream:#F7F5EE;--ink:#0B0B0F;--navy:#06205C;--deep:#031338}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1350px;overflow:hidden;background:#fff}
body{font-family:Montserrat,sans-serif;color:var(--ink);-webkit-font-smoothing:antialiased}
.card{position:relative;width:1080px;height:1350px;overflow:hidden}
.ph{background-size:cover;background-position:center;background-repeat:no-repeat;background-color:#c9ccd3}
.logo{background:url('%LOGO%') center/contain no-repeat;mix-blend-mode:multiply}
.hs{border-radius:50%%;background-size:cover;background-position:center 20%%;flex:none}
.fit{white-space:nowrap;overflow:hidden}
span.fit{display:inline-block;vertical-align:bottom}
.fit2{overflow:hidden}
""".replace("%LOGO%", LOGO).replace("%%", "%")


def e(s):
    return escape(str(s)) if s is not None else ""


def ml(s):
    """Escape and turn newlines into <br>."""
    return "<br>".join(e(x) for x in str(s or "").split("\n"))


def bg(url, pos=None):
    p = f";background-position:{pos}" if pos else ""
    return f"background-image:url('{e(url)}'){p}" if url else ""


def photo(c, i):
    p = c.get("photos") or []
    return p[i] if i < len(p) else None


def label(c, i):
    lb = c.get("photo_labels") or []
    return lb[i] if i < len(lb) else ""


def foot(h=124, logo=True, rule="var(--red)"):
    lg = '<div class="logo" style="width:190px;height:84px;flex:none"></div>' if logo else ""
    return f'''<div class="office" style="position:absolute;inset:auto 0 0 0;height:{h}px;background:#fff;border-top:6px solid {rule};display:flex;align-items:center;gap:26px;padding:0 44px">
  {lg}<div style="flex:1;min-width:0;font:500 16px/1.35 Montserrat;color:#3d4048"><div style="font:800 21px/1.2 Montserrat;color:#0B0B0F">{OFFICE_NAME}</div>{OFFICE_ADDR}<div style="font:500 13px/1.4 Montserrat;color:#6b6f78">Each Office Independently Owned and Operated</div></div>
  <div style="text-align:right;flex:none"><div style="font:700 14px/1 Montserrat;letter-spacing:4px;color:#6b6f78">OFFICE</div><div class="office-phone" style="font:800 {OFFICE_PHONE_PX}px/1.1 Montserrat;color:#0B0B0F">{OFFICE_PHONE}</div></div></div>'''


# ---------------------------------------------------------------- contact helpers
def agents(c):
    return [a for a in (c.get("agents") or []) if a.get("name")]


def agent_names(c):
    a = agents(c)
    return " & ".join(x["name"] for x in a)


def agent_phone(c):
    a = agents(c)
    return a[0].get("phone", "") if a else ""


def heads(c, size, ring, overlap=0.2):
    """Headshot circles for every agent that has one. ring = CSS box-shadow/border."""
    out, first = [], True
    for a in agents(c):
        if not a.get("headshot"):
            continue
        ml_ = "" if first else f"margin-left:-{int(size * overlap)}px;"
        out.append(f'<div class="hs" style="width:{size}px;height:{size}px;{ml_}{bg(a["headshot"])};{ring}"></div>')
        first = False
    return f'<div style="display:flex;flex:none">{"".join(out)}</div>' if out else ""


def booking(c):
    b = c.get("booking") or {}
    return {"label": b.get("label", "BOOK YOUR STAY"), "site": b.get("site", "SurfsideCapeMay.com"),
            "note": b.get("note", "Photos, rates & live calendar")}


def is_rental(c):
    return c.get("kind") == "rental" or not agents(c)


def stats_text(c, sep=" &nbsp; "):
    return sep.join(f"{e(b)} {e(s)}" for b, s in (c.get("stats") or []))


STAR = ("polygon(50% 0%,61% 12%,76% 6%,79% 22%,95% 25%,89% 40%,100% 50%,89% 60%,95% 75%,79% 78%,76% 94%,"
        "61% 88%,50% 100%,39% 88%,24% 94%,21% 78%,5% 75%,11% 60%,0% 50%,11% 40%,5% 25%,21% 22%,24% 6%,39% 12%)")


# ---------------------------------------------------------------- F1 BOLD BANNER
def f1(c):
    insets = [(photo(c, i), label(c, i)) for i in (1, 2, 3) if photo(c, i)]
    cols = max(1, len(insets))
    pol = "".join(
        f'''<div style="background:#fff;padding:8px 8px {0 if lb else 8}px;box-shadow:0 16px 30px rgba(0,0,0,.30);transform:rotate({r}deg)">
      <div class="ph" style="height:196px;{bg(u)}"></div>
      {f'<div class="fit" style="background:var(--navy);color:#fff;font:600 23px/1 Oswald;letter-spacing:1px;text-align:center;padding:11px 6px 10px;margin:0 -8px">{e(lb)}</div>' if lb else ''}</div>'''
        for (u, lb), r in zip(insets, (-1.5, 0, 1.5)))
    bullets = c.get("bullets") or [f"{b} {s.lower()}" for b, s in (c.get("stats") or [])]
    lis = "".join(f'<li style="font:700 28px/1.15 Montserrat;color:var(--ink);display:flex;gap:14px"><span style="color:var(--red)">&#9733;</span><span class="fit" style="max-width:520px">{e(t)}</span></li>' for t in bullets[:5])
    star = (f'''<div style="position:absolute;right:42px;top:330px;width:230px;height:230px;clip-path:{STAR};background:var(--red);display:flex;align-items:center;justify-content:center;transform:rotate(8deg)">
    <div class="fit2" style="font:400 44px/0.95 Anton;color:#fff;text-align:center;width:170px;max-height:140px">{ml(c["star"])}</div></div>''' if c.get("star") else "")
    price = (f'''<div style="position:absolute;left:40px;top:196px;transform:rotate(-4deg);background:var(--blue);padding:10px 34px 8px 34px;box-shadow:0 12px 26px rgba(0,0,0,.35);display:flex;align-items:baseline;gap:18px">
    {f'<span style="font:600 40px/1 Oswald;color:#fff;letter-spacing:1px">{e(c.get("price_label"))}</span>' if c.get("price_label") else ''}
    <span style="font:400 84px/1 Anton;color:var(--cream)">{e(c["price"])}</span></div>''' if c.get("price") else "")
    if is_rental(c):
        b = booking(c)
        contact = f'''<div style="font:400 40px/1 Kaushan;color:var(--red)">Book online</div>
    <div class="fit" style="font:800 34px/1.15 Montserrat;color:var(--navy);margin-top:10px;width:390px">{e(b["site"])}</div>
    <div style="font:600 22px/1.35 Montserrat;color:#4a5165;margin-top:8px">{e(b["note"])}</div>'''
    else:
        h = heads(c, 170 if len(agents(c)) == 1 else 140, "border:7px solid #fff;box-shadow:0 0 0 5px var(--blue),0 14px 30px rgba(0,0,0,.25)", 0.15)
        contact = f'''<div style="display:flex;justify-content:center">{h}</div>
    <div style="font:400 40px/1 Kaushan;color:var(--red);margin-top:16px">Call</div>
    <div class="fit2" style="font:700 30px/1.15 Montserrat;color:var(--navy);max-height:72px">{e(agent_names(c))}</div>
    <div class="agent-phone" style="font:800 {AGENT_PHONE_PX}px/1.2 Montserrat;color:var(--ink);margin-top:4px">{e(agent_phone(c))}</div>'''
    return f"""<div class="card" style="background:#fff">
  <div class="ph" style="position:absolute;inset:0 0 auto 0;height:700px;{bg(photo(c, 0), c.get('hero_pos', 'center 60%'))}"></div>
  <div style="position:absolute;inset:0 0 auto 0;height:260px;background:linear-gradient(180deg,rgba(3,19,56,.55),rgba(3,19,56,0))"></div>
  <div style="position:absolute;left:-30px;top:44px;transform:rotate(-4deg);background:var(--red);padding:14px 60px 10px 80px;box-shadow:0 14px 30px rgba(0,0,0,.35)">
    <div class="fit" style="font:400 112px/1 Anton;color:#fff;letter-spacing:1px;max-width:800px;text-shadow:0 4px 0 rgba(0,0,0,.18)">{e(c.get('badge', ''))}</div></div>
  {price}{star}
  <div style="position:absolute;left:36px;right:36px;top:590px;display:grid;grid-template-columns:repeat({cols},1fr);gap:18px">{pol}</div>
  <div style="position:absolute;left:52px;top:880px;width:560px">
    <div class="fit" style="font:400 64px/1.05 Anton;color:var(--navy);width:560px">{e(c.get('headline', '')).upper()}</div>
    <div class="fit" style="font:700 28px/1.2 Montserrat;color:var(--red);margin-top:6px;letter-spacing:.5px;width:560px">{e(c.get('subline', '')).upper()}</div>
    <ul style="list-style:none;margin-top:20px;display:grid;gap:9px">{lis}</ul>
  </div>
  <div style="position:absolute;right:44px;top:870px;width:390px;text-align:center">{contact}</div>
  {foot()}
</div>"""


# ---------------------------------------------------------------- F2 MAGAZINE
ICONS = {
    "bed": '<svg viewBox="0 0 24 24" width="40" height="40" fill="#fff"><path d="M3 7h2v6h14a2 2 0 0 1 2 2v4h-2v-2H5v2H3zM7 9h4a2 2 0 0 1 2 2v1H7z"/></svg>',
    "bath": '<svg viewBox="0 0 24 24" width="40" height="40" fill="#fff"><path d="M4 12h16v2a5 5 0 0 1-4 4.9V21h-2v-2h-4v2H8v-2.1A5 5 0 0 1 4 14zM6 11V5a2 2 0 0 1 4 0h-2v6z"/></svg>',
    "area": '<svg viewBox="0 0 24 24" width="40" height="40" fill="none" stroke="#fff" stroke-width="2.2"><path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"/></svg>',
    "people": '<svg viewBox="0 0 24 24" width="40" height="40" fill="#fff"><circle cx="8" cy="8" r="3.2"/><circle cx="16.5" cy="9" r="2.6"/><path d="M2 20c0-3.6 2.7-6 6-6s6 2.4 6 6zM13.5 20c0-1.7-.5-3.2-1.4-4.4.9-.6 2-.9 3.2-.9 2.9 0 4.7 2.1 4.7 5.3z"/></svg>',
    "cal": '<svg viewBox="0 0 24 24" width="40" height="40" fill="none" stroke="#fff" stroke-width="2.2"><rect x="4" y="5" width="16" height="15" rx="2"/><path d="M4 10h16M9 3v4M15 3v4"/></svg>',
    "star": '<svg viewBox="0 0 24 24" width="40" height="40" fill="#fff"><path d="M12 2l3 6.6 7 .7-5.3 4.8 1.6 7L12 17.5 5.7 21l1.6-7L2 9.3l7-.7z"/></svg>',
}


def icon_for(small):
    s = small.upper()
    if "BED" in s:
        return ICONS["bed"]
    if "BATH" in s:
        return ICONS["bath"]
    if "SQ" in s or "ACRE" in s or "LOT" in s:
        return ICONS["area"]
    if "SLEEP" in s or "GUEST" in s:
        return ICONS["people"]
    if "BUILT" in s or "YEAR" in s:
        return ICONS["cal"]
    return ICONS["star"]


def f2(c):
    stats = c.get("stats") or []
    st = "".join(f'''<div style="display:flex;align-items:center;gap:14px">
      <div style="width:72px;height:72px;border-radius:50%;background:var(--blue);display:flex;align-items:center;justify-content:center;flex:none">{icon_for(s)}</div>
      <div><div style="font:600 38px/1 Playfair;color:var(--navy)">{e(b)}</div><div style="font:600 16px/1.2 Montserrat;color:#4a5165;letter-spacing:2px;margin-top:4px">{e(s)}</div></div></div>''' for b, s in stats[:4])
    insets = [photo(c, i) for i in (1, 2) if photo(c, i)]
    ins = "".join(f'<div class="ph" style="height:205px;{bg(u)}"></div>' for u in insets)
    price = (f'''<div style="position:absolute;right:34px;bottom:34px;background:var(--red);color:#fff;padding:18px 28px;transform:rotate(-2deg);box-shadow:0 10px 24px rgba(0,0,0,.25);text-align:center">
      <div style="font:700 52px/1 Playfair">{e(c["price"])}</div>{f'<div style="font:600 17px/1.2 Montserrat;letter-spacing:3px;margin-top:6px">{e(c.get("price_label"))}</div>' if c.get("price_label") else ''}</div>''' if c.get("price") else "")
    if is_rental(c):
        b = booking(c)
        contact = f'''<div style="flex:1"><div style="font:400 30px/1 Kaushan;color:var(--red)">Book your stay</div>
      <div class="fit" style="font:700 40px/1.1 Playfair;color:var(--navy);width:900px">{e(b["site"])}</div>
      <div style="font:600 22px/1.4 Montserrat;color:var(--ink)">{e(b["note"])}</div></div>'''
    else:
        h = heads(c, 128, "box-shadow:0 0 0 5px #fff,0 0 0 8px var(--blue)", 0.2)
        contact = f'''{h}<div style="flex:1;min-width:0"><div style="font:400 30px/1 Kaushan;color:var(--red)">Listed by</div>
      <div class="fit" style="font:700 36px/1.1 Playfair;color:var(--navy);max-width:760px">{e(agent_names(c))}</div>
      <div class="agent-phone fit" style="font:600 {min(24, AGENT_PHONE_PX)}px/1.4 Montserrat;color:var(--ink);max-width:760px">{e(agent_phone(c))}{(" &nbsp;|&nbsp; " + e(agents(c)[0].get("email"))) if agents(c)[0].get("email") else ""}</div></div>'''
    return f"""<div class="card" style="background:#fff">
  <div style="height:178px;display:flex;align-items:center;justify-content:space-between;gap:30px;padding:0 48px">
    <div class="logo" style="width:250px;height:110px;flex:none"></div>
    <div style="text-align:right;min-width:0">
      <div class="fit" style="font:700 72px/0.95 Playfair;color:var(--navy);max-width:690px">{e(c.get('badge', 'Now Showing'))}</div>
      <div class="fit" style="font:500 italic 26px/1.3 Montserrat;color:var(--blue);max-width:690px">{e(c.get('tagline', ''))}</div></div></div>
  <div class="fit" style="background:var(--navy);color:#fff;font:600 25px/1 Montserrat;letter-spacing:4px;text-align:center;padding:20px 30px">{e(c.get('kicker', '')).upper()}</div>
  <div class="ph" style="position:relative;height:440px;{bg(photo(c, 0), c.get('hero_pos', 'center 60%'))}">
    <div style="position:absolute;left:0;bottom:34px;background:rgba(255,255,255,.95);padding:20px 40px 20px 48px;box-shadow:0 10px 24px rgba(0,0,0,.2);max-width:640px">
      <div class="fit" style="font:700 48px/1 Playfair;color:var(--navy);max-width:560px">{e(c.get('headline', ''))}</div>
      <div class="fit" style="font:600 18px/1.4 Montserrat;color:#4a5165;letter-spacing:3px;margin-top:6px;max-width:560px">{e(c.get('subline', '')).upper()}</div></div>
    {price}</div>
  <div style="display:grid;grid-template-columns:repeat({max(1, len(insets))},1fr);gap:10px;padding:10px 0 0">{ins}</div>
  <div style="display:flex;justify-content:space-between;padding:26px 48px 22px;border-bottom:2px solid #e3e6ee">{st}</div>
  <div style="display:flex;align-items:center;gap:26px;padding:18px 48px 0">{contact}</div>
  {foot(logo=False)}
</div>"""


# ---------------------------------------------------------------- F3 LUXURY FULL-BLEED
def f3(c):
    if is_rental(c):
        b = booking(c)
        contact = f'''<div style="color:#fff;min-width:0">
      <div style="font:600 18px/1 Montserrat;letter-spacing:5px;color:#f3dcc0">{e(b["label"])}</div>
      <div class="fit" style="font:400 46px/1.15 DMSerif;max-width:900px">{e(b["site"])}</div>
      <div style="font:500 24px/1.3 Montserrat">{e(b["note"])}</div></div>'''
    else:
        h = heads(c, 112, "border:3px solid #fff", 0.2)
        a0 = agents(c)[0]
        contact = f'''{h}<div style="color:#fff;min-width:0">
      <div style="font:600 18px/1 Montserrat;letter-spacing:5px;color:#f3dcc0">PRIVATE SHOWINGS</div>
      <div class="fit" style="font:400 42px/1.15 DMSerif;max-width:800px">{e(agent_names(c))}</div>
      <div class="agent-phone fit" style="font:500 {min(25, AGENT_PHONE_PX)}px/1.3 Montserrat;max-width:800px">{e(a0.get("phone", ""))}{(" &nbsp;|&nbsp; " + e(a0.get("email"))) if a0.get("email") else ""}</div></div>'''
    stats = "<br>".join(filter(None, [stats_text(c), e(c.get("stats_line2", ""))]))
    price = f'<div class="fit" style="font:600 68px/1 Playfair;max-width:560px;flex:none">{e(c["price"])}</div><div style="height:56px;width:2px;background:rgba(255,255,255,.5);flex:none"></div>' if c.get("price") else ""
    return f"""<div class="card" style="background:var(--deep)">
  <div class="ph" style="position:absolute;inset:0 0 140px 0;{bg(photo(c, 0), c.get('hero_pos', 'center 45%'))}"></div>
  <div style="position:absolute;inset:0 0 140px 0;background:linear-gradient(180deg,transparent 30%,color-mix(in srgb,var(--deep) 55%,transparent) 58%,color-mix(in srgb,var(--deep) 96%,transparent) 100%)"></div>
  <div style="position:absolute;left:0;right:0;top:0;height:200px;background:linear-gradient(180deg,rgba(3,19,56,.6),rgba(3,19,56,0))"></div>
  <div class="fit" style="position:absolute;left:60px;top:54px;max-width:480px;font:600 22px/1 Montserrat;color:#fff;letter-spacing:7px">{e(c.get('kicker', '')).upper()}</div>
  {f'<div class="fit" style="position:absolute;right:60px;top:42px;max-width:470px;background:var(--red);color:#fff;font:600 19px/1 Montserrat;letter-spacing:5px;padding:14px 20px">{e(c["badge"]).upper()}</div>' if c.get('badge') else ''}
  <div style="position:absolute;left:60px;right:60px;bottom:330px;color:#fff">
    <div class="fit" style="font:400 italic 40px/1.15 Playfair;color:#f3dcc0;max-width:960px">{e(c.get('tagline', ''))}</div>
    <div class="fit" style="font:400 100px/1.05 DMSerif;margin-top:6px;max-width:960px">{e(c.get('headline', ''))}</div>
    <div style="display:flex;align-items:center;gap:26px;margin-top:20px">{price}
      <div class="fit2" style="font:600 23px/1.5 Montserrat;letter-spacing:3px;max-height:72px">{stats}</div></div>
  </div>
  <div style="position:absolute;left:60px;right:60px;bottom:170px;display:flex;align-items:center;gap:24px;border-top:1px solid rgba(255,255,255,.35);padding-top:24px">{contact}</div>
  {foot(h=140, rule="var(--deep)")}
</div>"""


# ---------------------------------------------------------------- F4 COLLAGE
def f4(c):
    chips = c.get("chips") or [f"{b} {s}" for b, s in (c.get("stats") or [])]
    ch = "".join(f'<div style="background:#fff;color:var(--blue);font:800 28px/1 Barlow;letter-spacing:1px;padding:14px 22px;border-radius:40px;white-space:nowrap">{e(t).upper()}</div>' for t in chips[:4])
    p1, p2, p3 = photo(c, 0), photo(c, 1), photo(c, 2)
    frame = "border:8px solid #fff;box-shadow:0 18px 36px rgba(0,0,0,.35)"
    if p2 and p3:
        grid = f'''<div class="ph" style="grid-row:1/3;{bg(p1, c.get('hero_pos', 'center 60%'))};{frame}"></div>
    <div class="ph" style="{bg(p2)};{frame}"></div><div class="ph" style="{bg(p3)};{frame}"></div>'''
        cols = "1.55fr 1fr"
    else:
        grid = f'<div class="ph" style="grid-row:1/3;{bg(p1, c.get("hero_pos", "center 60%"))};{frame}"></div>'
        cols = "1fr"
    if is_rental(c):
        b = booking(c)
        contact = f'''<div><div style="font:600 21px/1 Montserrat;letter-spacing:4px;color:#cfe0ff">{e(b["label"])}</div>
      <div class="fit" style="font:800 46px/1.05 Barlow;max-width:900px">{e(b["site"]).upper()}</div><div style="font:600 24px/1.2 Montserrat">{e(b["note"])}</div></div>'''
    else:
        h = heads(c, 116, "border:5px solid #fff", 0.2)
        contact = f'''{h}<div style="min-width:0"><div style="font:600 21px/1 Montserrat;letter-spacing:4px;color:#cfe0ff">CALL OR TEXT</div>
      <div class="fit" style="font:800 40px/1.05 Barlow;max-width:780px">{e(agent_names(c)).upper()}</div><div class="agent-phone" style="font:700 {AGENT_PHONE_PX}px/1.2 Montserrat">{e(agent_phone(c))}</div></div>'''
    return f"""<div class="card" style="background:var(--blue)">
  <div style="position:absolute;inset:0;background:radial-gradient(circle at 85% 8%,rgba(255,255,255,.18),transparent 45%),repeating-linear-gradient(135deg,rgba(255,255,255,.05) 0 2px,transparent 2px 22px)"></div>
  <div style="position:absolute;left:48px;top:40px;color:#fff;width:600px">
    <div class="fit" style="font:800 24px/1 Barlow;letter-spacing:6px;color:#cfe0ff">{e(c.get('kicker', '')).upper()}</div>
    <div class="fit2" style="font:800 92px/0.92 Barlow;text-transform:uppercase;margin-top:8px;height:176px">{ml(c.get('badge', ''))}</div></div>
  <div style="position:absolute;right:48px;top:52px;text-align:right;color:#fff;width:360px">
    <div class="fit2" style="font:600 22px/1.3 Montserrat;letter-spacing:3px;color:#cfe0ff;max-height:58px">{e(c.get('subline', '')).upper()}</div>
    <div class="fit2" style="font:500 20px/1.3 Montserrat;color:#e8efff;max-height:80px">{e(c.get('tagline', ''))}</div></div>
  <div style="position:absolute;left:48px;right:48px;top:270px;display:grid;grid-template-columns:{cols};grid-template-rows:290px 290px;gap:14px">{grid}</div>
  <div style="position:absolute;left:-20px;top:790px;transform:rotate(-3deg);background:var(--red);padding:16px 50px 14px 70px;box-shadow:0 14px 28px rgba(0,0,0,.35);display:flex;align-items:center;gap:30px;max-width:1060px">
    {f'<span style="font:400 88px/1 Anton;color:#fff;white-space:nowrap">{e(c["price"])}</span>' if c.get('price') else ''}
    <span class="fit2" style="font:800 30px/1.05 Barlow;color:#fff;letter-spacing:2px;max-height:66px;max-width:520px">{ml(c.get('headline', '')).upper()}{(' <span style="font-weight:600;opacity:.85">' + e(c.get('price_label')).upper() + '</span>') if c.get('price_label') and is_rental(c) else ''}</span></div>
  <div style="position:absolute;left:48px;right:48px;top:950px;display:flex;gap:14px;flex-wrap:nowrap;overflow:hidden">{ch}</div>
  <div style="position:absolute;left:48px;right:48px;top:1052px;display:flex;align-items:center;gap:22px;color:#fff">{contact}</div>
  {foot(rule="var(--blue)")}
</div>"""


# ---------------------------------------------------------------- F5 CREAM EDITORIAL
def f5(c):
    stats = (c.get("stats") or [])[:3]
    st = "".join(f'<div style="padding:16px 30px 14px {0 if i == 0 else 30}px;{"border-left:1px solid var(--ink);" if i else ""}"><div style="font:400 48px/1 DMSerif;white-space:nowrap">{e(a)}</div><div style="font:700 15px/1.4 Montserrat;letter-spacing:3px;margin-top:4px;white-space:nowrap">{e(b)}</div></div>' for i, (a, b) in enumerate(stats))
    insets = [photo(c, i) for i in (1, 2) if photo(c, i)]
    ins = "".join(f'<div class="ph" style="{bg(u)}"></div>' for u in insets)
    if is_rental(c):
        b = booking(c)
        contact = f'''<div style="font:700 17px/1.2 Montserrat;letter-spacing:5px;color:var(--red);flex:none">{e(b["label"])}</div>
    <div style="flex:1;min-width:0"><div class="fit" style="font:400 38px/1.1 DMSerif;max-width:700px">{e(b["site"])}</div>
      <div style="font:600 21px/1.4 Montserrat">{e(b["note"])}</div></div>'''
    else:
        h = heads(c, 92, "box-shadow:0 0 0 3px var(--cream),0 0 0 5px var(--ink)", 0.2)
        a0 = agents(c)[0]
        contact = f'''{h or '<div style="font:700 17px/1.2 Montserrat;letter-spacing:5px;color:var(--red);flex:none">LISTED BY</div>'}
    <div style="flex:1;min-width:0"><div class="fit" style="font:400 38px/1.1 DMSerif;max-width:760px">{e(agent_names(c))}</div>
      <div class="agent-phone fit" style="font:600 {min(21, AGENT_PHONE_PX)}px/1.4 Montserrat;max-width:760px">{e(a0.get("phone", ""))}{(" &nbsp;|&nbsp; " + e(a0.get("email"))) if a0.get("email") else ""}</div></div>'''
    return f"""<div class="card" style="background:var(--cream)">
  <div style="position:absolute;inset:34px 34px 124px;border:2px solid var(--ink);border-bottom:0"></div>
  <div style="position:absolute;left:62px;right:62px;top:62px;display:flex;justify-content:space-between;align-items:center;gap:20px">
    <div class="fit" style="font:700 19px/1 Montserrat;letter-spacing:6px;max-width:470px">{e(c.get('kicker', '')).upper()}</div>
    <div class="fit" style="font:700 19px/1 Montserrat;letter-spacing:4px;color:var(--red);max-width:470px">{e(c.get('badge', '')).upper()}</div></div>
  <div class="ph" style="position:absolute;left:62px;right:62px;top:104px;height:470px;{bg(photo(c, 0), c.get('hero_pos', 'center 62%'))}"></div>
  <div style="position:absolute;left:62px;right:62px;top:606px;display:grid;grid-template-columns:{'1fr 330px' if insets else '1fr'};gap:30px">
    <div style="min-width:0">
      <div style="width:80px;height:5px;background:var(--red)"></div>
      <div class="fit" style="font:400 68px/1.05 DMSerif;margin-top:16px;max-width:{580 if insets else 940}px">{e(c.get('headline', ''))}</div>
      <div class="fit" style="font:400 italic 30px/1.2 DMSerif;color:#3b3f48;margin-top:8px;max-width:{580 if insets else 940}px">{e(c.get('tagline', ''))}</div>
      <div style="display:grid;grid-template-columns:repeat({max(1, len(stats))},auto);justify-content:start;margin-top:28px;border-top:1px solid var(--ink);border-bottom:1px solid var(--ink)">{st}</div>
      <div style="margin-top:22px;display:flex;align-items:center;gap:20px">
        {f'<div style="font:400 66px/1 DMSerif;color:var(--blue);white-space:nowrap">{e(c["price"])}</div>' if c.get('price') else ''}
        <div class="fit2" style="font:600 20px/1.3 Montserrat;color:#5a5f6b;max-height:80px">{ml(c.get('price_note', ''))}</div></div>
    </div>
    {f'<div style="display:grid;grid-template-rows:240px 240px;gap:16px;padding-top:6px">{ins}</div>' if insets else ''}
  </div>
  <div style="position:absolute;left:62px;right:62px;top:1090px;display:flex;align-items:center;gap:22px;border-top:1px solid var(--ink);padding-top:14px">{contact}</div>
  {foot(rule="var(--ink)")}
</div>"""


# ---------------------------------------------------------------- F6 SPLIT PANEL
def f6(c):
    def pstat(big, small):
        return f'<div style="padding:20px 0;border-bottom:2px solid rgba(255,255,255,.25)"><div class="fit" style="font:400 78px/0.95 Bebas;color:#fff;max-width:378px">{e(big)}</div><div class="fit" style="font:700 18px/1.2 Montserrat;color:#cfe0ff;letter-spacing:4px;max-width:378px">{e(small)}</div></div>'
    panel = c.get("panel_stats") or c.get("stats") or []
    if is_rental(c):
        b = booking(c)
        contact = f'''<div style="flex:1;min-width:0"><div style="font:700 18px/1 Montserrat;letter-spacing:4px;color:var(--red)">{e(b["label"])}</div>
      <div class="fit" style="font:400 46px/1.05 Bebas;color:var(--navy);letter-spacing:1px;max-width:960px;margin-top:6px">{e(b["site"]).upper()}</div>
      <div style="font:600 22px/1.4 Montserrat">{e(b["note"])}</div></div>'''
    else:
        h = heads(c, 100, "box-shadow:0 0 0 4px #fff,0 0 0 7px var(--red)", 0.22)
        a0 = agents(c)[0]
        contact = f'''{h}<div style="flex:1;min-width:0"><div class="fit" style="font:400 36px/1 Bebas;color:var(--navy);letter-spacing:1px;max-width:780px">{e(agent_names(c)).upper()}</div>
      <div class="agent-phone fit" style="font:600 {min(22, AGENT_PHONE_PX)}px/1.4 Montserrat;max-width:780px">{e(a0.get("phone", ""))}{(" &nbsp;|&nbsp; " + e(a0.get("email"))) if a0.get("email") else ""}</div></div>'''
    inset = photo(c, 1)
    return f"""<div class="card" style="background:#fff">
  <div class="ph" style="position:absolute;left:0;top:0;width:610px;height:860px;{bg(photo(c, 0), c.get('hero_pos', '42% 50%'))}"></div>
  <div style="position:absolute;left:610px;top:0;width:470px;height:860px;background:var(--navy);padding:46px 46px 0">
    {f'<div class="fit2" style="display:inline-block;max-width:378px;max-height:90px;background:var(--red);color:#fff;font:700 21px/1.3 Montserrat;letter-spacing:4px;padding:10px 18px">{e(c["badge"]).upper()}</div>' if c.get('badge') else ''}
    <div style="margin-top:12px">{''.join(pstat(a, b) for a, b in panel[:4])}</div></div>
  {f'<div class="ph" style="position:absolute;left:400px;top:690px;width:330px;height:250px;{bg(inset)};border:8px solid #fff;box-shadow:0 18px 34px rgba(0,0,0,.35)"></div>' if inset else ''}
  <div style="position:absolute;left:50px;top:880px;width:{330 if inset else 980}px">
    {f'<div class="fit" style="font:400 100px/0.9 Bebas;color:var(--red);max-width:{330 if inset else 980}px">{e(c["price"])}</div>' if c.get('price') else ''}
    {f'<div style="font:700 18px/1.2 Montserrat;letter-spacing:4px;color:var(--red);margin-top:4px">{e(c.get("price_label")).upper()}</div>' if c.get('price') and c.get('price_label') and is_rental(c) else ''}
  </div>
  <div style="position:absolute;left:50px;right:50px;top:{1000 if c.get('price') else 900}px">
    <div class="fit" style="font:400 56px/1 Bebas;color:var(--navy);max-width:{980 if not inset or c.get('price') else 330}px">{e(c.get('headline', ''))}</div>
    <div class="fit" style="font:700 21px/1.3 Montserrat;letter-spacing:5px;color:#4a5165;margin-top:2px;max-width:980px">{e(c.get('subline', '')).upper()}</div></div>
  <div style="position:absolute;left:50px;right:50px;top:1110px;display:flex;align-items:center;gap:22px">{contact}</div>
  {foot()}
</div>"""


# ---------------------------------------------------------------- F7 DATA / LAND & COMMERCIAL
def f7(c):
    def row(k, v):
        return f'<div style="display:flex;justify-content:space-between;align-items:baseline;gap:16px;padding:13px 0;border-bottom:1px solid rgba(255,255,255,.18)"><span style="font:600 18px/1 Montserrat;letter-spacing:3px;color:#9fb3d9;white-space:nowrap">{e(k)}</span><span class="fit" style="font:600 32px/1 Oswald;color:#fff;max-width:330px">{e(v)}</span></div>'
    rows = c.get("rows") or [(s, b) for b, s in (c.get("stats") or [])]
    right = []
    for i in (1, 2):
        u = photo(c, i)
        if u:
            lb = label(c, i)
            color = "var(--red)" if i == 1 else "rgba(11,11,15,.85)"
            tag = (f'<div style="position:absolute;left:0;bottom:0;background:{color};color:#fff;font:600 17px/1 Montserrat;'
                   f'letter-spacing:2px;padding:9px 12px">{e(lb).upper()}</div>') if lb else ""
            right.append(f'<div class="ph" style="height:182px;{bg(u)};position:relative">{tag}</div>')
    pn = c.get("panel")
    if pn and len(right) < 2:
        right.append(f'''<div style="height:182px;background:var(--red);display:flex;align-items:center;gap:22px;padding:0 28px;color:#fff">
      <div style="font:400 130px/1 Anton">{e(pn.get("big", ""))}</div><div class="fit2" style="font:700 40px/1.05 Oswald;letter-spacing:1px;max-height:170px">{ml(pn.get("text", ""))}</div></div>''')
    if c.get("note_box") and len(right) < 2:
        nb = c["note_box"]
        right.append(f'''<div style="height:182px;border:3px solid #fff;display:flex;flex-direction:column;justify-content:center;padding:0 26px;color:#fff">
      <div style="font:600 17px/1 Montserrat;letter-spacing:4px;color:#9fb3d9">{e(nb.get("label", "")).upper()}</div>
      <div class="fit2" style="font:600 30px/1.2 Oswald;margin-top:10px;max-height:110px">{ml(nb.get("text", ""))}</div></div>''')
    if is_rental(c):
        b = booking(c)
        contact = f'<div style="text-align:right;font:600 22px/1.25 Montserrat">{e(b["label"].title())}<br><span class="fit" style="display:inline-block;font:700 28px/1.2 Montserrat;max-width:520px">{e(b["site"])}</span></div>'
    else:
        h = heads(c, 76, "border:3px solid #fff", 0.21)
        contact = f'{h}<div style="text-align:right;font:600 22px/1.25 Montserrat;min-width:0"><span class="fit" style="display:inline-block;max-width:470px">{e(agent_names(c))}</span><br><span class="agent-phone" style="font:700 {min(26, AGENT_PHONE_PX)}px/1.2 Montserrat">{e(agent_phone(c))}</span></div>'
    return f"""<div class="card" style="background:var(--deep)">
  <div style="position:absolute;left:0;right:0;top:0;height:176px;padding:36px 48px 0">
    <div class="fit" style="display:inline-block;max-width:984px;background:var(--red);color:#fff;font:700 21px/1 Montserrat;letter-spacing:5px;padding:11px 16px">{e(c.get('badge', '')).upper()}</div>
    <div class="fit" style="font:700 76px/1.05 Oswald;color:#fff;margin-top:12px;letter-spacing:1px;max-width:984px">{e(c.get('headline', '')).upper()} <span style="color:#9fb3d9;font-weight:400">{e(c.get('headline_tail', '')).upper()}</span></div></div>
  <div class="ph" style="position:absolute;left:48px;right:48px;top:196px;height:480px;{bg(photo(c, 0), c.get('hero_pos', 'center 46%'))}">
    {f'<div style="position:absolute;left:18px;bottom:18px;background:rgba(11,11,15,.82);color:#fff;font:600 19px/1 Montserrat;letter-spacing:3px;padding:12px 16px">{e(label(c, 0)).upper()}</div>' if label(c, 0) else ''}</div>
  <div style="position:absolute;left:48px;top:700px;width:{540 if right else 984}px">
    <div style="font:600 18px/1 Montserrat;letter-spacing:5px;color:#9fb3d9">{e(c.get('price_label', 'ASKING')).upper()}</div>
    <div class="fit" style="font:700 92px/1 Oswald;color:#fff;margin-top:6px;max-width:540px">{e(c.get('price', ''))}{(' <span style="font:500 30px/1 Oswald;color:#9fb3d9">' + e(c.get('price_suffix')).upper() + '</span>') if c.get('price_suffix') else ''}</div>
    <div style="margin-top:14px">{''.join(row(k, v) for k, v in rows[:4])}</div></div>
  {f'<div style="position:absolute;right:48px;top:704px;width:400px;display:grid;gap:14px">{"".join(right)}</div>' if right else ''}
  <div style="position:absolute;left:48px;right:48px;top:1104px;display:flex;justify-content:space-between;align-items:flex-end;gap:24px;color:#fff">
    <div style="font:600 24px/1.25 Montserrat;min-width:0"><span class="fit" style="display:inline-block;max-width:460px">{e(c.get('address', c.get('headline', '')))}</span><br><span style="color:#9fb3d9">{e(c.get('subline', ''))}</span></div>
    <div style="display:flex;align-items:center;gap:16px;min-width:0">{contact}</div></div>
  {foot(h=118)}
</div>"""


TEMPLATES = {"f1": f1, "f2": f2, "f3": f3, "f4": f4, "f5": f5, "f6": f6, "f7": f7}


def page(spec, font_css=None):
    """Full HTML document for a spec. font_css overrides the Google Fonts link (local testing)."""
    tpl = TEMPLATES[spec["template"]]
    scheme = SCHEMES[spec.get("scheme", "classic")]
    fonts = f"<style>{font_css}</style>" if font_css else f'<link rel="stylesheet" href="{FONTS_URL}">'
    body = tpl(spec["card"])
    for short, full in FAMILY_ALIASES.items():   # map short names onto the real family names
        body = body.replace(f" {short};", f" '{full}';").replace(f" {short}\"", f" '{full}'\"")
    return (f"<!doctype html><html><head><meta charset='utf-8'>{fonts}<style>{BASE_CSS}:root{{{scheme}}}</style></head>"
            f"<body>{body}</body></html>")
