"""Render a REMAX Surfside brochure card from a JSON spec.

Usage:
  python render/render.py --spec spec.json --out card.jpg
  python render/render.py --issue-body-env BODY --out-root .      (GitHub Action)

The spec format is documented in render/SPEC.md. Exits non-zero with a one-line
reason on stdout (prefixed ERROR:) when the card can't be rendered cleanly.
"""
import argparse, json, os, re, sys, tempfile, pathlib
from urllib.parse import urlparse

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import cards  # noqa: E402

ALLOWED_IMAGE_HOSTS = {"d36xftgacqn2p.cloudfront.net", "d2td4dobkk213c.cloudfront.net",
                       "realtimerental.com", "www.realtimerental.com", "bgroetsch.github.io"}
PATH_RE = re.compile(r"^(remax-cards|rental-cards)/\d{4}-\d{2}-\d{2}/[A-Za-z0-9][A-Za-z0-9._-]*\.jpg$")

FIT_JS = """
() => {
  const bad = [];
  for (const el of document.querySelectorAll('.fit,.fit2')) {
    let fs = parseFloat(getComputedStyle(el).fontSize), min = Math.max(12, fs * 0.55);
    const two = el.classList.contains('fit2');
    const over = () => two ? el.scrollHeight > el.clientHeight + fs * 0.3 : el.scrollWidth > el.clientWidth + 1;
    while (over() && fs > min) { fs -= 1; el.style.fontSize = fs + 'px'; }
    if (over()) bad.push(el.textContent.trim().slice(0, 60));
  }
  return bad;
}"""

CHECK_JS = """
async () => {
  const urls = new Set();
  for (const el of document.querySelectorAll('*')) {
    const b = getComputedStyle(el).backgroundImage;
    const m = b && b.match(/url\\("?(https:[^")]+)"?\\)/);
    if (m) urls.add(m[1]);
  }
  const failed = [];
  await Promise.all([...urls].map(u => new Promise(r => {
    const i = new Image(); i.onload = () => r(); i.onerror = () => { failed.push(u); r(); }; i.src = u;
  })));
  const px = s => parseFloat(getComputedStyle(s).fontSize);
  const office = document.querySelector('.office-phone');
  const agentPx = [...document.querySelectorAll('.agent-phone')].map(px);
  const keys = new Set();
  for (const el of document.querySelectorAll('.card *')) {
    if (![...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) continue;
    const cs = getComputedStyle(el), fam = cs.fontFamily.split(',')[0].replace(/["']/g, '').trim();
    keys.add(`${cs.fontStyle} ${cs.fontWeight} 16px "${fam}"`);
  }
  const fams = [...keys].filter(k => !document.fonts.check(k));
  for (const f of document.fonts) if (f.status === 'error') fams.push(f.family + ' (error)');
  return {failed, officePx: office ? px(office) : 0, agentPx, missingFonts: fams};
}"""


def fail(msg):
    print(f"ERROR: {msg}")
    sys.exit(1)


def parse_issue_body(body):
    m = re.search(r"```(?:json)?\s*(\{.*\})\s*```", body, re.S)
    raw = m.group(1) if m else body.strip()
    try:
        return json.loads(raw)
    except Exception as ex:  # noqa: BLE001
        fail(f"Issue body is not valid JSON ({ex}).")


def validate(spec):
    if spec.get("template") not in cards.TEMPLATES:
        fail(f"Unknown template {spec.get('template')!r}; use one of {sorted(cards.TEMPLATES)}.")
    if spec.get("scheme", "classic") not in cards.SCHEMES:
        fail(f"Unknown scheme {spec.get('scheme')!r}; use one of {sorted(cards.SCHEMES)}.")
    path = spec.get("path", "")
    if path and (".." in path or not PATH_RE.match(path)):
        fail(f"Bad path {path!r}; expected remax-cards/YYYY-MM-DD/<name>.jpg or rental-cards/YYYY-MM-DD/<name>.jpg.")
    c = spec.get("card") or {}
    if not c.get("photos"):
        fail("card.photos is empty; the first photo is the hero.")
    urls = list(c.get("photos", [])) + [a.get("headshot") for a in c.get("agents", []) if a.get("headshot")]
    for u in urls:
        host = urlparse(u).hostname or ""
        if not u.startswith("https://") or host not in ALLOWED_IMAGE_HOSTS:
            fail(f"Image host not allowed: {u}")
    if c.get("kind") != "rental" and not c.get("agents"):
        fail("A listing card needs card.agents (set card.kind to 'rental' for rentals).")


def render(spec, out, font_css=None, url_map=None):
    from playwright.sync_api import sync_playwright
    html = cards.page(spec, font_css=font_css)
    for k, v in (url_map or {}).items():
        html = html.replace(k, v)
    with tempfile.TemporaryDirectory() as td:
        f = pathlib.Path(td) / "card.html"
        f.write_text(html, encoding="utf-8")
        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page(viewport={"width": 1080, "height": 1350})
            pg.goto(f.as_uri(), wait_until="networkidle", timeout=90000)
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(300)
            overflow = pg.evaluate(FIT_JS)
            chk = pg.evaluate(CHECK_JS)
            problems = []
            if chk["failed"]:
                hero = spec["card"]["photos"][0]
                if any(hero in u or (url_map and url_map.get(hero, "~") in u) for u in chk["failed"]):
                    problems.append("hero photo did not load")
                else:
                    print("WARNING: images did not load: " + ", ".join(chk["failed"]))
            if chk["missingFonts"]:
                problems.append("fonts did not load: " + ", ".join(chk["missingFonts"]))
            if not chk["officePx"]:
                problems.append("office phone missing")
            if any(a >= chk["officePx"] for a in chk["agentPx"]):
                problems.append(f"agent phone ({max(chk['agentPx'])}px) is not smaller than office phone ({chk['officePx']}px)")
            if overflow:
                problems.append("text too long to fit: " + " | ".join(overflow))
            if problems:
                b.close()
                fail("; ".join(problems))
            pathlib.Path(out).parent.mkdir(parents=True, exist_ok=True)
            pg.screenshot(path=str(out), type="jpeg", quality=90)
            b.close()
    print(f"OK {out}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec")
    ap.add_argument("--issue-body-env")
    ap.add_argument("--out")
    ap.add_argument("--out-root", default=".")
    ap.add_argument("--font-css")
    ap.add_argument("--url-map")
    a = ap.parse_args()
    if a.issue_body_env:
        spec = parse_issue_body(os.environ.get(a.issue_body_env, ""))
    else:
        spec = json.loads(pathlib.Path(a.spec).read_text())
    validate(spec)
    out = a.out or (spec.get("path") and str(pathlib.Path(a.out_root) / spec["path"]))
    if not out:
        fail("No output path: give spec.path or --out.")
    font_css = pathlib.Path(a.font_css).read_text() if a.font_css else None
    url_map = json.loads(pathlib.Path(a.url_map).read_text()) if a.url_map else None
    render(spec, out, font_css, url_map)
    if a.issue_body_env and os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a") as fh:
            fh.write(f"dest={spec['path']}\n")


if __name__ == "__main__":
    main()
