"""Holiday and community card template (h1) for REMAX Surfside.

Full-bleed photo with a short centered greeting at the top and the standard office
footer from cards.foot() (lighthouse logo, office address, "Each Office
Independently Owned and Operated", office phone). No agent, price or stats.
Registered into cards.TEMPLATES by render.py. Spec: render/SPEC.md.
"""
from cards import bg, e, foot, photo


def h1(c):
    kicker = c.get("kicker", "")
    tagline = c.get("tagline", "")
    kick = (f'<div class="fit" style="font:600 21px/1 Montserrat;letter-spacing:8px;color:#f3e6cf;'
            f'max-width:940px;margin:0 auto">{e(kicker).upper()}</div>') if kicker else ""
    tag = (f'<div style="width:64px;height:2px;background:#f3e6cf;margin:26px auto 0"></div>'
           f'<div class="fit" style="font:400 italic 34px/1.2 Playfair;color:#fff;margin:22px auto 0;'
           f'max-width:940px;text-shadow:0 1px 10px rgba(0,0,0,.35)">{e(tagline)}</div>') if tagline else ""
    top = "22px" if kicker else "0"
    return f"""<div class="card" style="background:var(--deep)">
  <div class="ph" style="position:absolute;inset:0 0 132px 0;{bg(photo(c, 0), c.get('hero_pos', 'center 60%'))}"></div>
  <div style="position:absolute;left:0;right:0;top:0;height:470px;background:linear-gradient(180deg,rgba(3,12,32,.62) 0%,rgba(3,12,32,.34) 55%,rgba(3,12,32,0) 100%)"></div>
  <div style="position:absolute;left:70px;right:70px;top:78px;text-align:center;color:#fff">
    {kick}
    <div class="fit" style="font:400 104px/1.08 DMSerif;margin:{top} auto 0;max-width:940px;text-shadow:0 2px 18px rgba(0,0,0,.35)">{e(c.get('headline', ''))}</div>
    {tag}
  </div>
  {foot(h=132, rule="var(--red)")}
</div>"""
