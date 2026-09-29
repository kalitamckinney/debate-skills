"""Build paste-ready Google Sites embed snippets from the pages in site/.

Each snippet is self-contained (inline CSS, images as data URIs) for
Google Sites > Insert > Embed > Embed code. Links to other lesson pages use
the {{SITE}} token, which the embed kit page replaces with the site address.
"""
import base64, io, json, re
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
OUT = ROOT / "google-sites"

# Page file -> (Google Sites page name, URL path segment)
PAGES = {
    "index.html": ("Home", "home"),
    "learn.html": ("Learn", "learn"),
    "example.html": ("Worked Example", "worked-example"),
    "assessment.html": ("Assessment", "assessment"),
    "about.html": ("About the Author", "about-the-author"),
    "credits.html": ("Credits", "credits"),
    "transcript.html": ("Audio Transcript", "audio-transcript"),
    "worksheet.html": ("CER Worksheet", "cer-worksheet"),
}

# Long pages are split before these headings so each embed box stays short.
SPLIT_BEFORE = {
    "learn.html": ['<h2 id="claims">', '<h2 id="cer">', '<h2 id="rebuttal">', '<h2 id="present">'],
    "example.html": ["<h2>Step 4:", "<h2>Step 6:"],
    "assessment.html": ["<h2>Instructions</h2>", "<h2>How you will be graded</h2>"],
}

# Light theme only: the embed sits on a light Google Sites page.
CSS = """
*{box-sizing:border-box}
body{margin:0;padding:16px;background:#ffffff;color:#1c1c1c;font:17px/1.65 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
h1,h2,h3{line-height:1.25;text-wrap:balance}
h1{font-size:2rem;margin-top:.25rem}
a{color:#0b4f8a;text-underline-offset:.15em}
a:focus-visible,summary:focus-visible{outline:3px solid #0b4f8a;outline-offset:2px}
.lead{font-size:1.2rem}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(14rem,1fr));gap:1rem;padding:0;list-style:none}
.card{background:#f1f4f8;border:1px solid #6b7280;border-radius:.75rem;padding:1rem 1.25rem}
.card h3{margin-top:0}
.tip{background:#fff1cc;border-left:6px solid #0b4f8a;border-radius:.5rem;padding:.75rem 1rem;margin:1rem 0}
.tip h3,.tip h4{margin:0 0 .25rem}
.tag{font-weight:700}.tag.claim{color:#0b4f8a}.tag.evidence{color:#1f6b3a}.tag.reasoning{color:#8a3b0b}
details{background:#f1f4f8;border:1px solid #6b7280;border-radius:.5rem;padding:.5rem 1rem;margin:.75rem 0}
summary{cursor:pointer;font-weight:600}
.table-wrap{overflow-x:auto}
table{border-collapse:collapse;width:100%;margin:1rem 0}
th,td{border:1px solid #6b7280;padding:.5rem;text-align:left;vertical-align:top}
th{background:#f1f4f8}
figure{margin:1.5rem 0}
figure img{max-width:100%;height:auto;display:block;border-radius:.5rem}
figcaption,.note{color:#4a4a4a;font-size:.95rem}
blockquote{margin:1rem 0;padding-left:1rem;border-left:4px solid #6b7280}
.line{border-bottom:1px solid #6b7280;height:2rem}
.site-note{background:#f1f4f8;border:1px dashed #6b7280;border-radius:.5rem;padding:.75rem 1rem}
"""


def data_uri(path: Path) -> str:
    if path.suffix == ".svg":
        return "data:image/svg+xml;base64," + base64.b64encode(path.read_bytes()).decode()
    im = Image.open(path).convert("RGB")
    im.thumbnail((800, 800))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=78, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def image_src(src: str) -> Path:
    p = SITE / src
    svg = p.with_suffix(".svg")
    return svg if svg.exists() else p  # prefer the small vector version


def page_link(m: re.Match) -> str:
    page, text = m.group(1), m.group(3)
    name, slug = PAGES[page]
    return f'<a href="{{{{SITE}}}}/{slug}" target="_top">{text}</a>'


def build(page: str) -> list[str]:
    html = (SITE / page).read_text()
    main = html[html.index("<main"):html.index("</main>")]
    main = main[main.index(">") + 1:]
    # Drop the audio player; the recording goes in natively with Insert > Drive.
    main = re.sub(
        r'<h2>🎧 Audio walkthrough.*?</p>\s*(?=<!--)',
        '<p class="site-note">🎧 <strong>Audio walkthrough:</strong> listen with the player on this page, '
        'or read the <a href="{{SITE}}/audio-transcript" target="_top">audio walkthrough transcript</a>.</p>\n\n    ',
        main, flags=re.S)
    main = re.sub(r"<!--.*?-->", "", main, flags=re.S)
    main = re.sub(r'<a href="([a-z]+\.html)(#[\w-]+)?">(.*?)</a>', page_link, main, flags=re.S)
    main = re.sub(r'<a href="(https?:|mailto:)', r'<a target="_blank" rel="noopener" href="\1', main)
    main = re.sub(r'src="(images/[^"]+)"', lambda m: f'src="{data_uri(image_src(m.group(1)))}"', main)
    main = re.sub(r"\n\s*\n+", "\n\n", main).strip()
    parts, rest = [], main
    for marker in SPLIT_BEFORE.get(page, []):
        i = rest.index(marker)
        parts.append(rest[:i].strip())
        rest = rest[i:]
    parts.append(rest.strip())
    return [f'<style>{CSS.strip()}</style>\n<main>\n{p}\n</main>\n' for p in parts]


def main():
    OUT.mkdir(exist_ok=True)
    manifest = []
    for page, (name, slug) in PAGES.items():
        snippets = build(page)
        for n, snippet in enumerate(snippets, 1):
            suffix = f"-{n}" if len(snippets) > 1 else ""
            out = OUT / f"{slug}{suffix}.html"
            out.write_text(snippet)
            manifest.append({"name": name, "slug": slug, "part": n, "parts": len(snippets),
                             "file": out.name, "kb": round(len(snippet.encode()) / 1024)})
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=1))
    for m in manifest:
        print(f'{m["name"]:18} {m["part"]}/{m["parts"]} {m["file"]:24} {m["kb"]} KB')


if __name__ == "__main__":
    main()
