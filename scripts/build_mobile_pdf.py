"""Build the phone-friendly PDF edition of the AI agent field guide."""

from __future__ import annotations

import html
import re
from dataclasses import dataclass
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A5
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
)


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class BookConfig:
    source: Path
    output: Path
    document_title: str
    cover_title: str
    subtitle: str
    description: str
    start_heading: str
    running_title: str


BOOKS = (
    BookConfig(
        source=ROOT / "docs" / "AI_AGENT_ENGINEERING_FIELD_GUIDE.md",
        output=ROOT / "output" / "pdf" / "AI_AGENT_ENGINEERING_FIELD_GUIDE.pdf",
        document_title="Инженерия AI-агентов",
        cover_title="ИНЖЕНЕРИЯ<br/>AI-АГЕНТОВ",
        subtitle="Теоретический путеводитель для поездки",
        description=(
            "От языковой модели и tool calling до harness engineering, evals, RAG, MCP, "
            "наблюдаемости и безопасного production-запуска."
        ),
        start_heading="# Как пользоваться книгой",
        running_title="Инженерия AI-агентов",
    ),
    BookConfig(
        source=ROOT / "docs" / "AI_AGENT_ENGINEERING_OFFLINE_WORKBOOK.md",
        output=ROOT / "output" / "pdf" / "AI_AGENT_ENGINEERING_OFFLINE_WORKBOOK.pdf",
        document_title="Практикум инженера AI-агентов",
        cover_title="ПРАКТИКУМ<br/>ИНЖЕНЕРА<br/>AI-АГЕНТОВ",
        subtitle="Задания и расширенное чтение без компьютера",
        description=(
            "Бизнес-кейсы, архитектурные упражнения, аварийные сценарии, evals, backend, "
            "безопасность, эксплуатация и сто вопросов для повторения."
        ),
        start_heading="# Как пользоваться практикумом",
        running_title="Практикум инженера AI-агентов",
    ),
)


def register_fonts() -> None:
    fonts = Path("C:/Windows/Fonts")
    pdfmetrics.registerFont(TTFont("GuideSans", str(fonts / "arial.ttf")))
    pdfmetrics.registerFont(TTFont("GuideSans-Bold", str(fonts / "arialbd.ttf")))
    pdfmetrics.registerFont(TTFont("GuideMono", str(fonts / "consola.ttf")))
    pdfmetrics.registerFontFamily(
        "GuideSans",
        normal="GuideSans",
        bold="GuideSans-Bold",
    )


class GuideDocTemplate(BaseDocTemplate):
    """A5 document with bookmarks and restrained running furniture."""

    def __init__(self, filename: str, config: BookConfig) -> None:
        self.config = config
        super().__init__(
            filename,
            pagesize=A5,
            leftMargin=15 * mm,
            rightMargin=15 * mm,
            topMargin=16 * mm,
            bottomMargin=16 * mm,
            title=config.document_title,
            author="Учебный проект Кирилла",
            subject="Теоретический путеводитель по production AI-агентам",
        )
        frame = Frame(
            self.leftMargin,
            self.bottomMargin,
            self.width,
            self.height,
            id="body",
            leftPadding=0,
            rightPadding=0,
            topPadding=0,
            bottomPadding=0,
        )
        self.addPageTemplates(PageTemplate(id="main", frames=[frame], onPage=self._decorate_page))

    def _decorate_page(self, canvas, doc) -> None:  # noqa: ANN001
        canvas.saveState()
        canvas.setFillColor(colors.white)
        canvas.rect(0, 0, A5[0], A5[1], stroke=0, fill=1)
        canvas.restoreState()
        if doc.page == 1:
            return
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#D7E0EA"))
        canvas.setLineWidth(0.45)
        canvas.line(15 * mm, 12.5 * mm, A5[0] - 15 * mm, 12.5 * mm)
        canvas.setFillColor(colors.HexColor("#667085"))
        canvas.setFont("GuideSans", 8)
        canvas.drawString(15 * mm, 8.3 * mm, self.config.running_title)
        canvas.drawRightString(A5[0] - 15 * mm, 8.3 * mm, str(doc.page))
        canvas.restoreState()

    def afterFlowable(self, flowable) -> None:  # noqa: ANN001
        bookmark = getattr(flowable, "bookmark_name", None)
        level = getattr(flowable, "outline_level", None)
        if bookmark is None or level is None:
            return
        self.canv.bookmarkPage(bookmark)
        self.canv.addOutlineEntry(flowable.getPlainText(), bookmark, level=level, closed=False)


def make_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName="GuideSans",
            fontSize=10.4,
            leading=15.2,
            textColor=colors.HexColor("#17202A"),
            spaceAfter=3.2 * mm,
            alignment=TA_LEFT,
            allowWidows=0,
            allowOrphans=0,
        ),
        "h1": ParagraphStyle(
            "H1",
            parent=base["Heading1"],
            fontName="GuideSans-Bold",
            fontSize=19,
            leading=23,
            textColor=colors.HexColor("#163A5F"),
            spaceAfter=6 * mm,
            keepWithNext=True,
        ),
        "h2": ParagraphStyle(
            "H2",
            parent=base["Heading2"],
            fontName="GuideSans-Bold",
            fontSize=13.2,
            leading=17,
            textColor=colors.HexColor("#176B87"),
            spaceBefore=3.5 * mm,
            spaceAfter=2.5 * mm,
            keepWithNext=True,
        ),
        "h3": ParagraphStyle(
            "H3",
            parent=base["Heading3"],
            fontName="GuideSans-Bold",
            fontSize=11.2,
            leading=14.5,
            textColor=colors.HexColor("#30475E"),
            spaceBefore=2.5 * mm,
            spaceAfter=1.7 * mm,
            keepWithNext=True,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            parent=base["BodyText"],
            fontName="GuideSans",
            fontSize=10.2,
            leading=14.7,
            leftIndent=5.5 * mm,
            firstLineIndent=-3.4 * mm,
            spaceAfter=1.4 * mm,
            textColor=colors.HexColor("#17202A"),
        ),
        "quote": ParagraphStyle(
            "Quote",
            parent=base["BodyText"],
            fontName="GuideSans",
            fontSize=10.4,
            leading=15,
            leftIndent=6 * mm,
            rightIndent=2 * mm,
            borderColor=colors.HexColor("#28A7C7"),
            borderWidth=0,
            borderPadding=(2 * mm, 3 * mm, 2 * mm, 4 * mm),
            backColor=colors.HexColor("#EAF7FA"),
            textColor=colors.HexColor("#163A5F"),
            spaceBefore=1.5 * mm,
            spaceAfter=4 * mm,
        ),
        "code": ParagraphStyle(
            "Code",
            parent=base["Code"],
            fontName="GuideMono",
            fontSize=7.6,
            leading=10.3,
            leftIndent=3 * mm,
            rightIndent=2 * mm,
            borderPadding=3 * mm,
            backColor=colors.HexColor("#F2F4F7"),
            textColor=colors.HexColor("#1D2939"),
            spaceBefore=1.5 * mm,
            spaceAfter=3.5 * mm,
        ),
        "toc": ParagraphStyle(
            "TOC",
            parent=base["BodyText"],
            fontName="GuideSans",
            fontSize=10.5,
            leading=14.5,
            leftIndent=4 * mm,
            firstLineIndent=-4 * mm,
            spaceAfter=1.8 * mm,
            textColor=colors.HexColor("#176B87"),
        ),
        "cover_title": ParagraphStyle(
            "CoverTitle",
            parent=base["Title"],
            fontName="GuideSans-Bold",
            fontSize=27,
            leading=32,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#163A5F"),
            spaceAfter=8 * mm,
        ),
        "cover_subtitle": ParagraphStyle(
            "CoverSubtitle",
            parent=base["BodyText"],
            fontName="GuideSans",
            fontSize=13,
            leading=18,
            textColor=colors.HexColor("#176B87"),
            spaceAfter=8 * mm,
        ),
        "cover_note": ParagraphStyle(
            "CoverNote",
            parent=base["BodyText"],
            fontName="GuideSans",
            fontSize=10.5,
            leading=15,
            textColor=colors.HexColor("#475467"),
        ),
    }


def inline_markup(text: str) -> str:
    """Convert the small Markdown subset used in the guide to ReportLab markup."""
    escaped = html.escape(text, quote=False)
    placeholders: list[str] = []

    def save(value: str) -> str:
        placeholders.append(value)
        return f"@@INLINE{len(placeholders) - 1}@@"

    escaped = re.sub(
        r"\[([^\]]+)\]\((https?://[^)]+)\)",
        lambda match: save(
            f'<link href="{html.escape(match.group(2), quote=True)}" color="#176B87">'
            f"{match.group(1)}</link>"
        ),
        escaped,
    )
    escaped = re.sub(r"`([^`]+)`", lambda match: save(f'<font name="GuideMono">{match.group(1)}</font>'), escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", escaped)
    escaped = re.sub(r"\*([^*]+)\*", r"<i>\1</i>", escaped)
    for index, value in enumerate(placeholders):
        escaped = escaped.replace(f"@@INLINE{index}@@", value)
    return escaped


def heading_paragraph(text: str, level: int, anchor: str, styles: dict[str, ParagraphStyle]) -> Paragraph:
    paragraph = Paragraph(f'<a name="{anchor}"/>{inline_markup(text)}', styles[f"h{level}"])
    paragraph.bookmark_name = anchor
    paragraph.outline_level = level - 1
    return paragraph


def extract_headings(lines: list[str], document_title: str) -> list[tuple[str, str]]:
    headings: list[tuple[str, str]] = []
    number = 0
    for line in lines:
        if line.startswith("# "):
            title = line[2:].strip()
            if title != document_title:
                number += 1
                headings.append((title, f"section-{number}"))
    return headings


def parse_markdown(lines: list[str], styles: dict[str, ParagraphStyle], document_title: str) -> list:
    story: list = []
    paragraph_lines: list[str] = []
    code_lines: list[str] = []
    in_code = False
    heading_number = 0
    first_section = True

    def flush_paragraph() -> None:
        if paragraph_lines:
            story.append(Paragraph(inline_markup(" ".join(paragraph_lines)), styles["body"]))
            paragraph_lines.clear()

    for raw_line in lines:
        line = raw_line.rstrip()
        if line.startswith("```"):
            flush_paragraph()
            if in_code:
                story.append(Preformatted("\n".join(code_lines), styles["code"]))
                code_lines.clear()
            in_code = not in_code
            continue
        if in_code:
            code_lines.append(line)
            continue
        if not line:
            flush_paragraph()
            continue
        if line == "---":
            flush_paragraph()
            story.append(Spacer(1, 2 * mm))
            continue
        if line.startswith("# "):
            flush_paragraph()
            title = line[2:].strip()
            if title == document_title:
                continue
            heading_number += 1
            if not first_section:
                story.append(PageBreak())
            first_section = False
            story.append(heading_paragraph(title, 1, f"section-{heading_number}", styles))
            continue
        if line.startswith("## "):
            flush_paragraph()
            story.append(heading_paragraph(line[3:].strip(), 2, f"subsection-{len(story)}", styles))
            continue
        if line.startswith("### "):
            flush_paragraph()
            story.append(heading_paragraph(line[4:].strip(), 3, f"topic-{len(story)}", styles))
            continue
        if line.startswith("> "):
            flush_paragraph()
            story.append(Paragraph(inline_markup(line[2:].strip()), styles["quote"]))
            continue
        bullet_match = re.match(r"^\s*[-*]\s+(.+)$", line)
        number_match = re.match(r"^\s*(\d+)\.\s+(.+)$", line)
        if bullet_match:
            flush_paragraph()
            story.append(Paragraph("• " + inline_markup(bullet_match.group(1)), styles["bullet"]))
            continue
        if number_match:
            flush_paragraph()
            story.append(
                Paragraph(
                    f"{number_match.group(1)}. " + inline_markup(number_match.group(2)),
                    styles["bullet"],
                )
            )
            continue
        paragraph_lines.append(line)

    flush_paragraph()
    if code_lines:
        story.append(Preformatted("\n".join(code_lines), styles["code"]))
    return story


def build_story(text: str, styles: dict[str, ParagraphStyle], config: BookConfig) -> list:
    lines = text.splitlines()
    headings = extract_headings(lines, config.document_title)

    story: list = [
        Spacer(1, 25 * mm),
        Paragraph(config.cover_title, styles["cover_title"]),
        Paragraph(config.subtitle, styles["cover_subtitle"]),
        Spacer(1, 8 * mm),
        Paragraph(config.description, styles["cover_note"]),
        Spacer(1, 25 * mm),
        Paragraph("Для Кирилла · версия от 16 июля 2026 года", styles["cover_note"]),
        PageBreak(),
        heading_paragraph("Содержание", 1, "contents", styles),
    ]
    for index, (title, anchor) in enumerate(headings, start=1):
        story.append(Paragraph(f'<link href="#{anchor}">{index}. {html.escape(title)}</link>', styles["toc"]))
    story.append(PageBreak())

    start = next(index for index, line in enumerate(lines) if line == config.start_heading)
    story.extend(parse_markdown(lines[start:], styles, config.document_title))
    return story


def main() -> None:
    register_fonts()
    for config in BOOKS:
        config.output.parent.mkdir(parents=True, exist_ok=True)
        text = config.source.read_text(encoding="utf-8")
        document = GuideDocTemplate(str(config.output), config)
        document.build(build_story(text, make_styles(), config))
        print(config.output)


if __name__ == "__main__":
    main()
