"""Check deployable assets, evidence links, and the letter-size recruiting PDF."""
import json
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from pypdf import PdfReader
from build import contrast, plain

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
profile = json.loads((ROOT / "profile.json").read_text())
schools = json.loads((ROOT / "schools.json").read_text())


class PageAssets(HTMLParser):
    def __init__(self):
        super().__init__()
        self.html_attributes = {}
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "html":
            self.html_attributes = attributes
        if tag == "a":
            self.links.append(attributes)
        if attributes.get("id"):
            self.ids.add(attributes["id"])
        values = [attributes.get(key, "") for key in ("href", "src")]
        values.extend(candidate.strip().split()[0] for candidate in attributes.get("srcset", "").split(",") if candidate.strip())
        for value in values:
            parsed = urlsplit(value)
            if not value or parsed.scheme or parsed.netloc or not parsed.path:
                continue
            if not parsed.path.startswith("/"):
                raise ValueError(f"Local assets must resolve from school paths: {value}")
            asset = (DIST / unquote(parsed.path).lstrip("/")).resolve()
            if not asset.is_relative_to(DIST.resolve()) or not asset.is_file():
                raise ValueError(f"Missing or invalid local asset: {value}")


site = (DIST / "index.html").read_text()
if f'<link rel="canonical" href="{profile["siteUrl"]}/">' not in site:
    raise ValueError("Website canonical URL differs from the profile URL")

pdf = PdfReader(DIST / "lindsey-cochran-recruiting.pdf")
if len(pdf.pages) != 1 or tuple(pdf.pages[0].mediabox) != (0, 0, 612, 792):
    raise ValueError("Recruiting PDF must remain one US letter page")
pdf_text = pdf.pages[0].extract_text()
pdf_links = {
    annotation.get_object().get("/A", {}).get("/URI")
    for annotation in pdf.pages[0].get("/Annots", [])
}
for mark in profile["primaryMarks"]:
    if mark["mark"] not in pdf_text or mark["mark"] not in site:
        raise ValueError(f"Personal best missing from website or PDF: {mark['event']}")
    if mark["source"]:
        url = profile["sources"][mark["source"]]
        if url not in pdf_links or url not in site:
            raise ValueError(f"Evidence link missing: {mark['event']}")
if profile["siteUrl"] not in pdf_links:
    raise ValueError("PDF must link back to the recruiting website")
for honor in profile["honors"]:
    if escape(honor["title"]) not in site or plain(honor["title"]) not in pdf_text:
        raise ValueError(f"Honor missing from website or PDF: {honor['title']}")
    if escape(honor["detail"]) not in site or plain(honor["detail"]) not in pdf_text:
        raise ValueError(f"Honor events or context missing: {honor['title']}")
    if honor["source"]:
        url = profile["sources"][honor["source"]]
        if url not in pdf_links or escape(url, quote=True) not in site:
            raise ValueError(f"Honor source missing: {honor['title']}")

pages = {"": site, "404": (DIST / "404.html").read_text()}
pages.update({slug: (DIST / slug / "index.html").read_text() for slug in schools})
for slug, page in pages.items():
    parser = PageAssets()
    parser.feed(page)
    for link in parser.links:
        href = link.get("href", "")
        if href.startswith("#") and href[1:] not in parser.ids:
            raise ValueError(f"Broken section link on {slug or 'main'}: {href}")
        if href.startswith("mailto:") and link.get("target") != "_blank":
            raise ValueError("Recruiting contact links must request a new tab")
    for mark in profile["primaryMarks"]:
        if mark["mark"] not in page:
            raise ValueError(f"Personal best missing on {slug}: {mark['event']}")
    if page.split('<div class="print-only">')[1] != site.split('<div class="print-only">')[1]:
        raise ValueError("All paths must keep the same universal print resume")
    if slug not in schools:
        if "data-school=" in page or 'class="school-note"' in page:
            raise ValueError("Main and fallback pages must keep the default theme")
        continue
    school = schools[slug]
    if parser.html_attributes.get("data-school") != slug:
        raise ValueError(f"Missing school theme for {slug}")
    palette = dict(part.split(":", 1) for part in parser.html_attributes["style"].split(";"))
    for foreground, background, minimum in [
        (palette["--red"], "#eeede5", 4.5),
        (palette["--school-heading"], "#f8f7f2", 3),
        ("#ffffff", palette["--red"], 4.5),
        ("#ffffff", palette["--school-banner"], 4.5),
        (palette["--school-highlight"], palette["--school-banner"], 4.5),
        (palette["--school-muted"], palette["--school-banner"], 4.5),
    ]:
        if contrast(foreground, background) < minimum:
            raise ValueError(f"Insufficient school theme contrast: {slug}")
    note = school.get("note")
    if note:
        if escape(note["text"]) not in page or not page.index('class="school-note"') < page.index('id="honors"'):
            raise ValueError(f"Missing or misplaced personal note: {slug}")
    elif 'class="school-note"' in page:
        raise ValueError(f"Unexpected personal note: {slug}")
print(f"Validated {len(pages)} pages, assets, school colors and notes, source links, and universal one-page PDF.")
