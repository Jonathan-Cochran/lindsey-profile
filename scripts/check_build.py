"""Check deployable assets, evidence links, and the letter-size recruiting PDF."""
import json
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from pypdf import PdfReader
from build import plain

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
profile = json.loads((ROOT / "profile.json").read_text())


class PageAssets(HTMLParser):
    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        for attribute in ("href", "src"):
            value = attributes.get(attribute, "")
            parsed = urlsplit(value)
            if not value or parsed.scheme or parsed.netloc or not parsed.path:
                continue
            asset = (DIST / unquote(parsed.path).lstrip("/")).resolve()
            if not asset.is_relative_to(DIST.resolve()) or not asset.is_file():
                raise ValueError(f"Missing or invalid local asset: {value}")


site = (DIST / "index.html").read_text()
PageAssets().feed(site)
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
print("Validated local assets, personal bests, honors, source links, and one-page letter PDF.")
