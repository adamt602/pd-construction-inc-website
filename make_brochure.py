from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import ImageReader
from PIL import Image

ROOT = Path(__file__).parent
OUT = ROOT / "output" / "pdf" / "PD-Construction-Tri-Fold-Brochure.pdf"
PAGE_W, PAGE_H = landscape(letter)
PANEL = PAGE_W / 3

INK = HexColor("#10110f")
IVORY = HexColor("#f2eee6")
TAN = HexColor("#bd9460")
MUTED = HexColor("#777872")
RULE = HexColor("#cbc4b8")
DARK_2 = HexColor("#242622")


def cover_image(c, path, x, y, w, h, overlay=None):
    img = Image.open(path)
    iw, ih = img.size
    scale = max(w / iw, h / ih)
    crop_w, crop_h = w / scale, h / scale
    left = (iw - crop_w) / 2
    top = (ih - crop_h) / 2
    cropped = img.crop((left, top, left + crop_w, top + crop_h))
    temp = ROOT / "tmp" / "pdfs" / ("crop-" + Path(path).stem + ".jpg")
    temp.parent.mkdir(parents=True, exist_ok=True)
    cropped.save(temp, quality=94)
    c.drawImage(ImageReader(temp), x, y, w, h, mask="auto")
    if overlay:
        c.setFillColor(overlay[0])
        c.setFillAlpha(overlay[1])
        c.rect(x, y, w, h, fill=1, stroke=0)
        c.setFillAlpha(1)


def logo(c, x, y, scale=1, color=INK):
    c.setFillColor(color)
    c.rect(x, y + 34 * scale, 80 * scale, 3.5 * scale, fill=1, stroke=0)
    c.rect(x + 35 * scale, y - 59 * scale, 3.5 * scale, 100 * scale, fill=1, stroke=0)
    c.circle(x + 61 * scale, y + 10 * scale, 19 * scale, fill=1, stroke=0)
    c.rect(x + 84 * scale, y + 2 * scale, 3.5 * scale, 79 * scale, fill=1, stroke=0)
    c.rect(x + 42 * scale, y - 9 * scale, 176 * scale, 3.5 * scale, fill=1, stroke=0)
    c.setFont("Helvetica", 24 * scale)
    c.drawString(x + 98 * scale, y + 1 * scale, "PD Construction INC.")


def label(c, text, x, y, color=TAN):
    c.setFillColor(color)
    c.setFont("Helvetica-Bold", 7.3)
    c.drawString(x, y, text.upper())


def wrapped(c, text, x, y, width, font="Helvetica", size=10, leading=14, color=INK, max_lines=20):
    c.setFont(font, size)
    c.setFillColor(color)
    words = text.split()
    lines, line = [], ""
    for word in words:
        test = (line + " " + word).strip()
        if c.stringWidth(test, font, size) <= width:
            line = test
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    for ln in lines[:max_lines]:
        c.drawString(x, y, ln)
        y -= leading
    return y


def bullet(c, num, title, body, x, y, width):
    c.setFillColor(TAN)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x, y, num)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x + 25, y, title)
    y -= 16
    return wrapped(c, body, x + 25, y, width - 25, size=8.5, leading=11.5, color=MUTED)


c = canvas.Canvas(str(OUT), pagesize=(PAGE_W, PAGE_H))
c.setTitle("PD Construction Inc. Tri-Fold Brochure")
c.setAuthor("PD Construction Inc.")

# PAGE 1: OUTSIDE - fold-in flap / back cover / front cover
c.setFillColor(IVORY)
c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

# Left: fold-in flap
cover_image(c, ROOT / "assets" / "wasatch-04-living-fireplace.jpg", 0, 260, PANEL, PAGE_H - 260)
c.setFillColor(IVORY)
c.rect(0, 0, PANEL, 260, fill=1, stroke=0)
label(c, "Why PD Construction", 26, 224)
c.setFont("Helvetica-Bold", 21)
c.setFillColor(INK)
c.drawString(26, 187, "Built to the")
c.drawString(26, 161, "design intent.")
wrapped(
    c,
    "Deep experience in millwork, framing, concrete and structural steel lets our team anticipate the finish from the first rough member.",
    26, 126, PANEL - 52, size=9, leading=13, color=MUTED,
)
c.setStrokeColor(TAN)
c.setLineWidth(2)
c.line(26, 37, 102, 37)

# Center: back cover
c.setFillColor(INK)
c.rect(PANEL, 0, PANEL, PAGE_H, fill=1, stroke=0)
logo(c, PANEL + 25, PAGE_H - 126, .58, IVORY)
label(c, "Start a conversation", PANEL + 25, 362)
c.setFillColor(IVORY)
c.setFont("Helvetica-Bold", 20)
c.drawString(PANEL + 25, 325, "Have a project")
c.drawString(PANEL + 25, 300, "in mind?")
c.setFont("Helvetica", 10)
c.drawString(PANEL + 25, 252, "661.269.1899")
c.drawString(PANEL + 25, 231, "diane@pdconstructioninc.com")
c.drawString(PANEL + 25, 210, "pdconstructioninc.com")
c.setFillColor(MUTED)
c.setFont("Helvetica", 8)
c.drawString(PANEL + 25, 164, "16654 Soledad Canyon Rd")
c.drawString(PANEL + 25, 150, "Canyon Country, CA 91387")
qr_path = Path("/Users/adampotter/Documents/Codex/2026-07-29/va/PD-Construction-Website-QR-4096.png")
if qr_path.exists():
    c.setFillColor(white)
    c.rect(PANEL + 25, 30, 92, 92, fill=1, stroke=0)
    c.drawImage(str(qr_path), PANEL + 29, 34, 84, 84)
c.setFillColor(MUTED)
c.setFont("Helvetica", 7)
c.drawString(PANEL + 130, 72, "CSLB Lic. #972699")
c.drawString(PANEL + 130, 58, "Licensed, bonded & insured")

# Right: front cover
cover_image(
    c, ROOT / "assets" / "wasatch-01-facade.jpg",
    PANEL * 2, 0, PANEL, PAGE_H,
    overlay=(INK, .48),
)
c.setFillColor(TAN)
c.rect(PANEL * 2, 0, 8, PAGE_H, fill=1, stroke=0)
logo(c, PANEL * 2 + 25, PAGE_H - 135, .55, white)
c.setFillColor(white)
c.setFont("Helvetica-Bold", 27)
c.drawString(PANEL * 2 + 25, 214, "Building modern")
c.drawString(PANEL * 2 + 25, 181, "spaces without")
c.drawString(PANEL * 2 + 25, 148, "compromise.")
label(c, "Residential / Commercial", PANEL * 2 + 25, 96, color=white)
c.showPage()

# PAGE 2: INSIDE SPREAD
c.setFillColor(IVORY)
c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

# Left inside panel
label(c, "What we do", 28, PAGE_H - 48)
c.setFillColor(INK)
c.setFont("Helvetica-Bold", 24)
c.drawString(28, PAGE_H - 88, "Full-scope")
c.drawString(28, PAGE_H - 117, "construction.")
y = PAGE_H - 161
y = bullet(c, "01", "Preconstruction", "Early budgeting, constructability review, scheduling and phasing before drawings are final.", 28, y, PANEL - 52) - 17
y = bullet(c, "02", "General Contracting", "Trade procurement, daily site supervision, quality control and complete closeout.", 28, y, PANEL - 52) - 17
y = bullet(c, "03", "Construction Management", "Owner-side budget, consultant coordination, reporting and documentation.", 28, y, PANEL - 52) - 17
y = bullet(c, "04", "Self-Performed Expertise", "Millwork, finish carpentry, framing, concrete and structural steel knowledge in house.", 28, y, PANEL - 52)

# Center inside panel
cover_image(c, ROOT / "assets" / "lhuillier-01-showroom.jpg", PANEL, 246, PANEL, PAGE_H - 246)
c.setFillColor(DARK_2)
c.rect(PANEL, 0, PANEL, 246, fill=1, stroke=0)
label(c, "How we work", PANEL + 27, 210)
c.setFillColor(white)
c.setFont("Helvetica-Bold", 19)
c.drawString(PANEL + 27, 175, "One accountable team.")
wrapped(
    c,
    "Direct principal access. Weekly schedule and budget visibility. Change orders priced before work proceeds. Punch-list completion backed by as-builts and warranties.",
    PANEL + 27, 143, PANEL - 54, size=9, leading=13, color=HexColor("#d6d2ca"),
)
c.setFillColor(TAN)
c.rect(PANEL + 27, 42, 72, 3, fill=1, stroke=0)

# Right inside panel
cover_image(c, ROOT / "assets" / "wildbeast-01-open-shell.jpg", PANEL * 2, 0, PANEL, 230)
c.setFillColor(INK)
c.setFillAlpha(.42)
c.rect(PANEL * 2, 0, PANEL, 230, fill=1, stroke=0)
c.setFillAlpha(1)
label(c, "From first call to handover", PANEL * 2 + 27, PAGE_H - 48)
c.setFillColor(INK)
c.setFont("Helvetica-Bold", 23)
c.drawString(PANEL * 2 + 27, PAGE_H - 88, "A clear process.")
steps = [
    ("01", "Discovery"),
    ("02", "Preconstruction"),
    ("03", "Planning + coordination"),
    ("04", "Construction"),
    ("05", "Quality control"),
    ("06", "Completion + handover"),
]
sy = PAGE_H - 137
for num, title in steps:
    c.setFillColor(TAN)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(PANEL * 2 + 27, sy, num)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(PANEL * 2 + 57, sy, title)
    c.setStrokeColor(RULE)
    c.setLineWidth(.6)
    c.line(PANEL * 2 + 27, sy - 10, PAGE_W - 27, sy - 10)
    sy -= 37
c.setFillColor(white)
c.setFont("Helvetica-Bold", 11)
c.drawString(PANEL * 2 + 27, 202, "Architectural residential")
c.drawString(PANEL * 2 + 27, 186, "and commercial work")
c.drawString(PANEL * 2 + 27, 170, "across Southern California.")

c.save()
print(OUT)
