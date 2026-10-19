"""Build the static recruiting profile and its one-page letter-size PDF."""
import html
import json
import shutil
from pathlib import Path
from string import Template
from urllib.parse import urlparse

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
PROFILE = json.loads((ROOT / "profile.json").read_text())
E = lambda value: html.escape(str(value), quote=True)


def icon(path, extra=""):
    return f'<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" {extra}>{path}</svg>'


ARROW = icon('<path d="M6 18 18 6M6 6h12v12"/>')
DOWN = icon('<path d="M12 4v16m-6-6 6 6 6-6"/>')
DOWNLOAD = icon('<path d="M12 3v12m-5-5 5 5 5-5M4 15v6h16v-6"/>')
TROPHY = icon('<path d="M7 3h10v6a5 5 0 0 1-10 0V3ZM7 5H3v3a4 4 0 0 0 4 4m10-7h4v3a4 4 0 0 1-4 4m-5 2v7m-4 0h8"/>')
CALENDAR = icon('<rect x="3" y="5" width="18" height="16" rx="1"/><path d="M7 3v4m10-4v4M3 11h18m-13 4h2m4 0h2"/>')
PRINT = icon('<path d="M7 8V3h10v5M7 17H3V9h18v8h-4M7 14h10v7H7zM17 11h1"/>')
PLAY = icon('<path d="m8 5 11 7-11 7V5Z" fill="currentColor" stroke="none"/>')
LAUREL = icon('<circle cx="12" cy="12" r="11" stroke-dasharray="1 1.2"/><path d="M6.7 18c-4-4-3-9 .3-12M5.7 15l-2-.8m1.3-2-2-1m2.2-1.5-1.5-1.8M17.3 18c4-4 3-9-.3-12m1.3 9 2-.8m-1.3-2 2-1m-2.2-1.5 1.5-1.8" stroke-width=".6"/>')


def source_url(row):
    url = PROFILE["sources"][row["source"]]
    return url + (f'#page={row["page"]}' if row.get("page") else "")


def make_site():
    p = PROFILE
    for key, url in p["sources"].items():
        if urlparse(url).scheme != "https":
            raise ValueError(f"Source {key} requires an HTTPS URL")
    if p["email"] and ("@" not in p["email"] or any(c in p["email"] for c in "\r\n?<> ")):
        raise ValueError("Use a plain recruiting email address")
    marks = "".join(
        f'<a class="mark-card" href="{E(p["sources"][m["source"]])}" target="_blank" rel="noopener noreferrer" aria-label="{E(m["event"])} personal best {E(m["mark"])}; verify on MileSplit"><span class="mark-event">{E(m["event"])} {ARROW}</span><strong class="mark-value">{E(m["mark"])}</strong><span class="mark-context">{E(m["context"])}</span></a>'
        for m in p["primaryMarks"]
    )
    supporting = "".join(f'<span class="supporting-mark">{E(m["event"])} <strong>{E(m["mark"])}</strong> <small>{E(m["context"])}</small></span>' for m in p["supportingMarks"])
    rows = "".join(
        f'<tr><td><span class="meet-name">{E(r["meet"])}</span><span class="meet-division">{E(r["division"])}</span></td><td>{E(r["event"])}</td><td><span class="placing {"first" if r["place"] == "1st" else ""}">{E(r["place"])}</span></td><td>{E(r["mark"])}</td><td><a href="{E(source_url(r))}" target="_blank" rel="noopener noreferrer" aria-label="View {E(r["meet"])} {E(r["event"])} published result">{ARROW}</a></td></tr>'
        for r in p["championships"]
    )
    videos = "".join(
        f'<a class="video-card" href="{E(v["url"])}" target="_blank" rel="noopener noreferrer" aria-label="Watch {E(v["title"])} on MileSplit"><div class="video-visual"><img class="video-still" src="{E(v["thumbnail"])}" alt="" width="620" height="349" loading="lazy"><span class="video-lines" aria-hidden="true"></span><div class="video-topline"><span>2026 OHSAA STATE CHAMPIONSHIPS</span><span>{E(v["duration"])}</span></div><span class="film-event" aria-hidden="true">{E(v["event"])}m</span><div><strong class="film-mark">{E(v["mark"])}</strong><span class="film-caption">{E(v["place"])}</span></div><span class="play-icon">{PLAY}</span></div><div class="video-details"><div><strong>{E(v["title"])}</strong><small>{E(v["subtitle"])}</small></div><span class="watch-link">MileSplit {ARROW}</span></div></a>'
        for v in p["videos"]
    )
    contact_url = "mailto:" + p["email"] if p["email"] else p["sources"]["runcruit"]
    contact_label = "Recruiting contact" if p["email"] else "Connect on Runcruit"
    print_marks = "".join(f'<div><span>{E(m["event"])}</span><strong>{E(m["mark"])}</strong></div>' for m in p["primaryMarks"])
    print_rows = "".join(f'<tr><td>{E(r["meet"])}<br><small>{E(r["division"])}</small></td><td>{E(r["event"])}</td><td>{E(r["place"])}</td><td><a href="{E(source_url(r))}">{E(r["mark"])}</a></td></tr>' for r in p["championships"])
    print_supporting = " · ".join(f'{E(m["event"])} {E(m["mark"])} ({E(m["context"]).lower()})' for m in p["supportingMarks"])
    print_resume = f'<article><header class="resume-header"><p class="eyebrow">CLASS OF {E(p["classYear"])} / WOMEN’S TRACK & FIELD / CROSS COUNTRY</p><h1>{E(p["name"])}</h1><p>{E(p["school"])} · {E(p["location"])}</p></header><p class="resume-title">{E(p["headline"])} · Division II</p><div class="resume-marks">{print_marks}</div><div class="resume-supporting">{print_supporting}</div><h2>Championship performances</h2><table><thead><tr><th>MEET</th><th>EVENT</th><th>PLACE</th><th>MARK</th></tr></thead><tbody>{print_rows}</tbody></table><h2>Academics & athlete profile</h2><div class="resume-academics"><strong>GPA:</strong> {E(p["gpa"])} ({E(p["gpaNote"]).lower()})<br><strong>Academic interests:</strong> {E(p["interests"])}<br><strong>Additional sport:</strong> {E(p["otherSport"])}</div><p class="resume-bio">{E(p["bio"])}</p><div class="resume-links"><a href="{E(p["sources"]["athletic"])}">Athletic.net</a><a href="{E(p["sources"]["milesplit"])}">MileSplit</a><a href="{E(p["sources"]["runcruit"])}">Runcruit</a><a href="{E(p["sources"]["videos"])}">Race videos</a></div><p class="resume-footer">{E(p["siteUrl"])}<br>Updated {E(p["updated"])}. Actual marks; full mile and 1600m are distinct. 4×800m mark is a team time.{("<br>Recruiting contact: " + E(p["email"])) if p["email"] else ""}</p></article>'
    fields = dict(
        class_year=E(p["classYear"]), school=E(p["school"]), location=E(p["location"]), headline=E(p["headline"]),
        site_url=E(p["siteUrl"]), primary_marks=marks, supporting_marks=supporting, championship_rows=rows,
        video_cards=videos, bio=E(p["bio"]), gpa=E(p["gpa"]), gpa_note=E(p["gpaNote"]), interests=E(p["interests"]),
        other_sport=E(p["otherSport"]), updated=E(p["updated"]), contact_url=E(contact_url), contact_label=contact_label,
        season_label=E(p["seasonNote"]["label"]), season_title=E(p["seasonNote"]["title"]), season_text=E(p["seasonNote"]["text"]),
        email_cta=f'<a class="text-link" href="{E(contact_url)}">{contact_label} {ARROW}</a>' if p["email"] else "",
        arrow=ARROW, arrow_down=DOWN, download=DOWNLOAD, trophy=TROPHY, laurel=LAUREL, calendar=CALENDAR, print_icon=PRINT,
        print_resume=print_resume, **p["sources"]
    )
    (DIST / "index.html").write_text(Template((ROOT / "template.html").read_text()).substitute(fields))


def plain(s):
    return s.replace("—", "-").replace("–", "-").replace("’", "'").replace("×", "x").replace("·", " / ")


def make_pdf():
    from reportlab.lib.utils import simpleSplit
    # Embed fonts so the PDF renders consistently without host font substitution.
    pdfmetrics.registerFont(TTFont("Helvetica", str(ROOT / "scripts/fonts/LiberationSans-Regular.ttf")))
    pdfmetrics.registerFont(TTFont("Helvetica-Bold", str(ROOT / "scripts/fonts/LiberationSans-Bold.ttf")))
    p = PROFILE
    pdf_path = DIST / "lindsey-cochran-recruiting.pdf"
    c = canvas.Canvas(str(pdf_path), pagesize=letter, pageCompression=1)
    c.setTitle("Lindsey Cochran | Class of 2029 Recruiting Resume")
    c.setAuthor("Lindsey Cochran")
    c.setSubject("Women's track & field and cross country recruiting profile")
    red, ink, muted, line = map(HexColor, ["#a42132", "#242725", "#666960", "#dedfd6"])
    left, right = 44, 568

    def text(x, y, value, size=10, font="Helvetica", color=ink):
        c.setFillColor(color)
        c.setFont(font, size)
        c.drawString(x, y, plain(value))

    def rule(y):
        c.setStrokeColor(line)
        c.setLineWidth(.6)
        c.line(left, y, right, y)

    def link(x, y, label, url, size=9):
        text(x, y, label, size, "Helvetica-Bold", red)
        width = c.stringWidth(plain(label), "Helvetica-Bold", size)
        c.linkURL(url, (x, y-3, x+width, y+size+2), relative=0, thickness=0)

    text(left, 747, f'CLASS OF {p["classYear"]}  /  WOMEN\'S TRACK & FIELD  /  CROSS COUNTRY', 8, "Helvetica-Bold", red)
    text(left-1, 701, p["name"], 36, "Helvetica-Bold")
    text(left, 678, f'{p["school"]}  /  {p["location"]}', 10, color=muted)
    c.setStrokeColor(red)
    c.setLineWidth(2.5)
    c.line(left, 661, right, 661)
    text(left, 637, p["headline"], 13, "Helvetica-Bold", red)
    text(left, 621, "Ohio Division II / Freshman season", 9, color=muted)
    c.setFillColor(HexColor("#f5f4ef"))
    c.rect(left, 532, right-left, 72, fill=1, stroke=0)
    for i, mark in enumerate(p["primaryMarks"]):
        x = left+16+i*174
        text(x, 586, mark["event"], 9, "Helvetica-Bold")
        text(x, 554, mark["mark"], 27, "Helvetica-Bold", red)
        c.linkURL(p["sources"][mark["source"]], (x,548,x+149,597), relative=0, thickness=0)
    supporting = "   /   ".join(f'{m["event"]} {m["mark"]} ({m["context"].lower()})' for m in p["supportingMarks"])
    text(left, 515, supporting, 8.5)
    text(left, 485, "CHAMPIONSHIP PERFORMANCES", 10, "Helvetica-Bold")
    rule(474)
    cols = [left, 321, 403, 465]
    for x, title in zip(cols, ["MEET", "EVENT", "PLACE", "MARK"]):
        text(x, 459, title, 7.5, "Helvetica-Bold", muted)
    rule(450)
    y = 431
    for row in p["championships"]:
        text(left, y, row["meet"], 9, "Helvetica-Bold")
        text(left, y-12, row["division"], 7.5, color=muted)
        text(cols[1], y-5, row["event"], 9)
        text(cols[2], y-5, row["place"], 9, "Helvetica-Bold", red if row["place"] == "1st" else ink)
        link(cols[3], y-5, row["mark"], source_url(row), 9)
        rule(y-22)
        y -= 40
    text(left, 230, "Actual marks. Full mile and 1600m are distinct events. 4x800m is the team's relay time.", 7.5, color=muted)
    text(left, 202, "ACADEMICS & ATHLETE PROFILE", 10, "Helvetica-Bold")
    text(left, 181, f'GPA: {p["gpa"]} ({p["gpaNote"].lower()})', 9.5)
    text(left, 164, f'Academic interests: {p["interests"]}', 9.5)
    text(left, 147, f'Additional sport: {p["otherSport"]}', 9.5)
    # Keep a concise bio without reducing legibility to fit a page.
    bio_lines = simpleSplit(plain(p["bio"]), "Helvetica", 8.5, right-left)
    for i, bio_line in enumerate(bio_lines):
        text(left, 125-i*12, bio_line, 8.5, color=muted)
    rule(88)
    for x, label, key in [(left,"Athletic.net","athletic"),(144,"MileSplit","milesplit"),(231,"Runcruit","runcruit"),(315,"Race videos","videos")]:
        link(x, 71, label, p["sources"][key], 9)
    if p["email"]:
        link(left, 54, p["email"], "mailto:"+p["email"], 8)
    else:
        link(left, 54, "Recruiting connection: Runcruit", p["sources"]["runcruit"], 8)
    text(left, 33, f'Updated {p["updated"]}', 7, color=muted)
    # Keep the website available as a clickable URL without an overlong footer.
    link(210, 33, p["siteUrl"].removeprefix("https://"), p["siteUrl"], 7)
    c.showPage()
    c.save()
    output = ROOT.parent / "output" / "pdf"
    output.mkdir(parents=True, exist_ok=True)
    shutil.copy2(pdf_path, output / pdf_path.name)


if __name__ == "__main__":
    DIST.mkdir(exist_ok=True)
    make_site()
    make_pdf()
    print("Built dist/index.html and the one-page recruiting PDF from profile.json.")
