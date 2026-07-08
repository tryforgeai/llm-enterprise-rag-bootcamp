from pathlib import Path

from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "reviews" / "ROSSO-HAN-BUILDING-TRUSTWORTHY-ENTERPRISE-RAG.pdf"

PAGE_W, PAGE_H = LETTER
MARGIN = 0.62 * inch

NAVY = colors.HexColor("#102A43")
NAVY_2 = colors.HexColor("#243B53")
TEAL = colors.HexColor("#0B8F87")
TEAL_LIGHT = colors.HexColor("#DDF5F2")
GOLD = colors.HexColor("#E8A23A")
INK = colors.HexColor("#243B53")
MUTED = colors.HexColor("#627D98")
PALE = colors.HexColor("#F4F7FA")
WHITE = colors.white
GREEN = colors.HexColor("#27896F")
BLUE = colors.HexColor("#3973B9")


def paragraph(c, text, x, y, width, size=10, leading=None, color=INK, bold=False):
    leading = leading or size * 1.35
    font = "Helvetica-Bold" if bold else "Helvetica"
    style = ParagraphStyle(
        "body",
        fontName=font,
        fontSize=size,
        leading=leading,
        textColor=color,
        alignment=TA_LEFT,
        spaceAfter=0,
    )
    p = Paragraph(text, style)
    _, h = p.wrap(width, PAGE_H)
    p.drawOn(c, x, y - h)
    return y - h


def label(c, text, x, y, fill=TEAL_LIGHT, color=TEAL):
    font_size = 8.2
    pad_x = 8
    width = stringWidth(text.upper(), "Helvetica-Bold", font_size) + pad_x * 2
    c.setFillColor(fill)
    c.roundRect(x, y - 17, width, 17, 8, stroke=0, fill=1)
    c.setFillColor(color)
    c.setFont("Helvetica-Bold", font_size)
    c.drawString(x + pad_x, y - 12, text.upper())
    return width


def title(c, kicker, heading, subtitle=None):
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(MARGIN, PAGE_H - MARGIN, kicker.upper())
    y = PAGE_H - MARGIN - 34
    y = paragraph(c, heading, MARGIN, y, PAGE_W - 2 * MARGIN, 25, 29, NAVY, True)
    if subtitle:
        y -= 9
        y = paragraph(c, subtitle, MARGIN, y, PAGE_W - 2 * MARGIN, 10.5, 15, MUTED)
    c.setStrokeColor(colors.HexColor("#D9E2EC"))
    c.setLineWidth(0.8)
    c.line(MARGIN, y - 16, PAGE_W - MARGIN, y - 16)
    return y - 36


def footer(c, page_num):
    c.setStrokeColor(colors.HexColor("#D9E2EC"))
    c.line(MARGIN, 0.42 * inch, PAGE_W - MARGIN, 0.42 * inch)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 7.5)
    c.drawString(MARGIN, 0.25 * inch, "ROSSO HAN | ENTERPRISE RAG & AI AGENTS")
    c.drawRightString(PAGE_W - MARGIN, 0.25 * inch, str(page_num))


def bullet(c, text, x, y, width, accent=TEAL, size=9.2):
    c.setFillColor(accent)
    c.circle(x + 3, y - 6, 2.2, stroke=0, fill=1)
    return paragraph(c, text, x + 13, y, width - 13, size, size * 1.38, INK)


def card(c, x, y, w, h, heading, body, accent=TEAL):
    c.setFillColor(WHITE)
    c.setStrokeColor(colors.HexColor("#D9E2EC"))
    c.roundRect(x, y - h, w, h, 8, stroke=1, fill=1)
    c.setFillColor(accent)
    c.roundRect(x, y - h, 5, h, 2, stroke=0, fill=1)
    paragraph(c, heading, x + 16, y - 14, w - 29, 10.2, 13, NAVY, True)
    paragraph(c, body, x + 16, y - 34, w - 29, 8.6, 12, MUTED)


def draw_cover(c):
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    c.setFillColor(TEAL)
    c.circle(PAGE_W - 44, PAGE_H - 45, 94, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.circle(PAGE_W - 30, 32, 48, stroke=0, fill=1)

    c.setStrokeColor(colors.Color(1, 1, 1, alpha=0.13))
    c.setLineWidth(1)
    for i in range(7):
        x = MARGIN + i * 0.72 * inch
        c.line(x, 1.1 * inch, x + 1.8 * inch, PAGE_H - 1.1 * inch)

    y = PAGE_H - 1.28 * inch
    label(c, "Enterprise AI Engineering", MARGIN, y, fill=WHITE, color=NAVY)
    y -= 62
    y = paragraph(
        c,
        "Building Trustworthy<br/>Enterprise RAG<br/>and AI Agents",
        MARGIN,
        y,
        5.7 * inch,
        31,
        35,
        WHITE,
        True,
    )
    y -= 22
    y = paragraph(
        c,
        "From retrieval demos to measurable, governable, and dependable systems.",
        MARGIN,
        y,
        4.8 * inch,
        13,
        19,
        colors.HexColor("#D9EAF0"),
    )

    y -= 38
    tags = ["RAG", "AI AGENTS", "EVALUATION", "GUARDRAILS"]
    x = MARGIN
    for tag in tags:
        w = label(c, tag, x, y, fill=colors.HexColor("#DDF5F2"), color=TEAL)
        x += w + 8

    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(MARGIN, 1.08 * inch, "Rosso Han")
    c.setFillColor(colors.HexColor("#B8D8E5"))
    c.setFont("Helvetica", 9.5)
    c.drawString(
        MARGIN,
        0.82 * inch,
        "Engineering Leader | Applied AI | Distributed Systems | Cloud Platforms",
    )


def draw_problem(c):
    y = title(
        c,
        "01 | The Enterprise Problem",
        "A fluent answer is not enough.",
        "Enterprise AI must handle fragmented knowledge, changing policy, permissions, and operational risk.",
    )

    left_w = 3.25 * inch
    right_x = MARGIN + left_w + 0.28 * inch
    right_w = PAGE_W - MARGIN - right_x

    paragraph(c, "What the system must do", MARGIN, y, left_w, 13, 16, NAVY, True)
    y2 = y - 32
    items = [
        "<b>Retrieve</b> the right evidence within permission boundaries.",
        "<b>Decide</b> whether to answer, ask, abstain, refuse, escalate, or use a tool.",
        "<b>Expose</b> provenance, uncertainty, and failure paths.",
        "<b>Protect</b> private, unsafe, and stale information.",
        "<b>Measure</b> quality before adding architectural complexity.",
    ]
    for item in items:
        y2 = bullet(c, item, MARGIN, y2, left_w, TEAL, 9.5) - 12

    c.setFillColor(PALE)
    c.roundRect(right_x, y, right_w, -3.45 * inch, 10, stroke=0, fill=1)
    paragraph(c, "The common demo", right_x + 18, y - 20, right_w - 36, 12, 15, NAVY, True)
    paragraph(
        c,
        "query -> retrieve -> generate",
        right_x + 18,
        y - 56,
        right_w - 36,
        12,
        16,
        MUTED,
        True,
    )
    c.setStrokeColor(colors.HexColor("#BCCCDC"))
    c.setLineWidth(1.2)
    c.line(right_x + 20, y - 88, right_x + right_w - 20, y - 88)
    paragraph(c, "What is missing?", right_x + 18, y - 110, right_w - 36, 11, 14, NAVY, True)
    missing = [
        "Decision policy",
        "Permission scope",
        "Traceability",
        "Evaluation",
        "Fallback behavior",
    ]
    my = y - 140
    for item in missing:
        my = bullet(c, item, right_x + 18, my, right_w - 36, GOLD, 9.2) - 9

    callout_y = 1.3 * inch
    c.setFillColor(NAVY)
    c.roundRect(MARGIN, callout_y, PAGE_W - 2 * MARGIN, 0.75 * inch, 10, stroke=0, fill=1)
    paragraph(
        c,
        "<b>Design principle:</b> RAG is not the product. It is the evidence layer inside an observable agent loop.",
        MARGIN + 20,
        callout_y + 0.49 * inch,
        PAGE_W - 2 * MARGIN - 40,
        11,
        15,
        WHITE,
    )
    footer(c, 2)


def draw_architecture(c):
    y = title(
        c,
        "02 | Agent-First Architecture",
        "Make every important decision visible.",
        "The loop connects evidence retrieval to bounded action, traceability, and continuous evaluation.",
    )

    names = [
        ("INTENT", "Task, risk,<br/>scope"),
        ("RETRIEVE", "Permitted<br/>evidence"),
        ("DECIDE", "Bounded<br/>next step"),
        ("RESPOND", "Grounded<br/>output"),
        ("TRACE", "Evidence +<br/>decisions"),
        ("EVALUATE", "Quality +<br/>safety"),
    ]
    gap = 0.09 * inch
    box_w = (PAGE_W - 2 * MARGIN - gap * 5) / 6
    box_h = 1.05 * inch
    x = MARGIN
    top = y - 12
    accents = [BLUE, TEAL, GOLD, BLUE, TEAL, GREEN]
    for idx, ((name, desc), accent) in enumerate(zip(names, accents)):
        c.setFillColor(WHITE)
        c.setStrokeColor(colors.HexColor("#BCCCDC"))
        c.roundRect(x, top - box_h, box_w, box_h, 8, stroke=1, fill=1)
        c.setFillColor(accent)
        c.roundRect(x, top - 8, box_w, 8, 4, stroke=0, fill=1)
        paragraph(c, name, x + 8, top - 22, box_w - 16, 8.3, 10, NAVY, True)
        paragraph(c, desc, x + 8, top - 43, box_w - 16, 8.1, 10.5, MUTED)
        if idx < 5:
            c.setStrokeColor(MUTED)
            c.setLineWidth(1)
            c.line(x + box_w + 1, top - box_h / 2, x + box_w + gap - 2, top - box_h / 2)
        x += box_w + gap

    y2 = top - box_h - 34
    paragraph(c, "Decision taxonomy", MARGIN, y2, 3.1 * inch, 12, 15, NAVY, True)
    paragraph(c, "Trace contract", 4.18 * inch, y2, 3.1 * inch, 12, 15, NAVY, True)

    left_items = [
        "answer with evidence",
        "ask a clarifying question",
        "retrieve again or use a tool",
        "abstain or refuse",
        "escalate for human review",
    ]
    right_items = [
        "intent and risk classification",
        "retrieved evidence and permissions",
        "decision and reason code",
        "model, prompt, latency, and cost",
        "safety and evaluation outcome",
    ]
    ly = y2 - 28
    ry = y2 - 28
    for item in left_items:
        ly = bullet(c, item, MARGIN, ly, 3.1 * inch, TEAL, 9.1) - 8
    for item in right_items:
        ry = bullet(c, item, 4.18 * inch, ry, 3.1 * inch, BLUE, 9.1) - 8

    c.setFillColor(TEAL_LIGHT)
    c.roundRect(MARGIN, 1.18 * inch, PAGE_W - 2 * MARGIN, 0.92 * inch, 10, stroke=0, fill=1)
    paragraph(
        c,
        "<b>Outcome:</b> When a result is wrong, the team can identify whether the failure came from intent classification, retrieval, decision policy, generation, or safety review.",
        MARGIN + 18,
        1.79 * inch,
        PAGE_W - 2 * MARGIN - 36,
        10.2,
        14,
        NAVY,
    )
    footer(c, 3)


def draw_trust(c):
    y = title(
        c,
        "03 | Evaluation & Governance",
        "Trust requires more than retrieval.",
        "Quality, privacy, safety, and operations must be measured as separate system properties.",
    )

    card(
        c,
        MARGIN,
        y,
        3.3 * inch,
        1.3 * inch,
        "Retrieval",
        "<b>Recall@k</b>, MRR, NDCG, no-match precision, stale retrievals, and latency.",
        TEAL,
    )
    card(
        c,
        4.08 * inch,
        y,
        3.3 * inch,
        1.3 * inch,
        "Grounding",
        "Claim support, contradiction rate, citation correctness, freshness, and uncertainty.",
        BLUE,
    )
    y2 = y - 1.55 * inch
    card(
        c,
        MARGIN,
        y2,
        3.3 * inch,
        1.3 * inch,
        "Agent Behavior",
        "Correct answer, ask, abstain, refuse, escalate, or tool-use decision.",
        GOLD,
    )
    card(
        c,
        4.08 * inch,
        y2,
        3.3 * inch,
        1.3 * inch,
        "Operations",
        "Latency, token cost, retries, cache quality, observability, and fallback success.",
        GREEN,
    )

    y3 = y2 - 1.63 * inch
    paragraph(c, "Governance sequence", MARGIN, y3, 3.2 * inch, 12, 15, NAVY, True)
    paragraph(c, "Architecture escalation", 4.08 * inch, y3, 3.2 * inch, 12, 15, NAVY, True)

    gov = [
        "Authenticate and authorize.",
        "Determine allowed memory and knowledge scope.",
        "Retrieve only permitted evidence.",
        "Generate under versioned policy.",
        "Review, repair, or use a safe fallback.",
    ]
    arch = [
        "Start with a measurable baseline.",
        "Name the failure and target metric.",
        "Estimate latency, cost, privacy, and maintenance.",
        "Compare against a fixed evaluation set.",
        "Remove components that do not earn their place.",
    ]
    gy = y3 - 27
    ay = y3 - 27
    for item in gov:
        gy = bullet(c, item, MARGIN, gy, 3.2 * inch, TEAL, 8.9) - 7
    for item in arch:
        ay = bullet(c, item, 4.08 * inch, ay, 3.2 * inch, BLUE, 8.9) - 7

    footer(c, 4)


def draw_evidence(c):
    y = title(
        c,
        "04 | Evidence From The Work",
        "Separate demonstrated capability from active experiments.",
        "Credibility comes from working systems, tests, explicit boundaries, and measurable next steps.",
    )

    left_x = MARGIN
    right_x = 4.13 * inch
    col_w = 3.25 * inch
    c.setFillColor(TEAL_LIGHT)
    c.roundRect(left_x, y, col_w, -4.77 * inch, 10, stroke=0, fill=1)
    c.setFillColor(colors.HexColor("#EDF3F8"))
    c.roundRect(right_x, y, col_w, -4.77 * inch, 10, stroke=0, fill=1)

    paragraph(c, "DEMONSTRATED", left_x + 18, y - 22, col_w - 36, 11, 14, TEAL, True)
    demonstrated = [
        "<b>Mixed-format RAG:</b> Markdown, Excel, and Word ingestion with 487 indexed chunks, persistent vector retrieval, and grounded generation.",
        "<b>AI automation:</b> A nine-node workflow connecting CRM data, model reasoning, workflow updates, and notifications.",
        "<b>Avaloka AI:</b> Risk routing, planning, guardian review, repair, fallback, evidence-backed memory, diagnostics, and behavior evals.",
        "<b>Verification:</b> 77 Avaloka tests and 200 Auralith tests passed on June 8, 2026.",
    ]
    dy = y - 58
    for item in demonstrated:
        dy = bullet(c, item, left_x + 18, dy, col_w - 36, TEAL, 8.9) - 14

    paragraph(c, "ACTIVE EXPERIMENTS", right_x + 18, y - 22, col_w - 36, 11, 14, BLUE, True)
    experiments = [
        "<b>Normalize</b> complete agent traces across classification, retrieval, decision, generation, and review.",
        "<b>Benchmark</b> deterministic memory retrieval using Recall@5, MRR, NDCG@5, privacy checks, and latency.",
        "<b>Escalate</b> to embeddings, hybrid retrieval, reranking, RAPTOR, or GraphRAG only for measured failures.",
        "<b>Verify</b> final claims against permitted evidence, provenance, freshness, and uncertainty.",
    ]
    ey = y - 58
    for item in experiments:
        ey = bullet(c, item, right_x + 18, ey, col_w - 36, BLUE, 8.9) - 14

    footer(c, 5)


def draw_close(c):
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    c.setFillColor(TEAL)
    c.rect(0, PAGE_H - 0.18 * inch, PAGE_W, 0.18 * inch, stroke=0, fill=1)

    y = PAGE_H - 0.9 * inch
    paragraph(c, "PROFESSIONAL FOCUS", MARGIN, y, 5.8 * inch, 9, 12, TEAL, True)
    y -= 42
    y = paragraph(
        c,
        "Engineering leadership for<br/>AI systems that can be trusted<br/>in real use.",
        MARGIN,
        y,
        5.7 * inch,
        27,
        32,
        WHITE,
        True,
    )
    y -= 22
    paragraph(
        c,
        "I bring together distributed systems, AWS and event-driven architecture, Applied AI, retrieval, guardrails, evaluation, and operational reliability.",
        MARGIN,
        y,
        4.8 * inch,
        11.3,
        17,
        colors.HexColor("#D9EAF0"),
    )

    line_y = 2.45 * inch
    c.setStrokeColor(colors.HexColor("#486581"))
    c.line(MARGIN, line_y, PAGE_W - MARGIN, line_y)
    paragraph(c, "Rosso Han", MARGIN, line_y - 24, 3.6 * inch, 15, 18, WHITE, True)
    paragraph(
        c,
        "Engineering Leader | Applied AI | Enterprise RAG | Agent Systems",
        MARGIN,
        line_y - 48,
        4.8 * inch,
        9.3,
        13,
        colors.HexColor("#B8D8E5"),
    )
    paragraph(
        c,
        "linkedin.com/in/rossohan",
        MARGIN,
        line_y - 82,
        3.5 * inch,
        9.5,
        13,
        TEAL,
        True,
    )

    qr = QrCodeWidget("https://www.linkedin.com/in/rossohan/")
    bounds = qr.getBounds()
    qr_w = bounds[2] - bounds[0]
    qr_h = bounds[3] - bounds[1]
    size = 0.96 * inch
    qr_x = PAGE_W - MARGIN - size
    qr_y = 0.72 * inch
    c.setFillColor(WHITE)
    c.roundRect(qr_x - 8, qr_y - 8, size + 16, size + 16, 6, stroke=0, fill=1)
    drawing = Drawing(size, size, transform=[size / qr_w, 0, 0, size / qr_h, 0, 0])
    drawing.add(qr)
    drawing.drawOn(c, qr_x, qr_y)


def generate():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUTPUT), pagesize=LETTER)
    c.setTitle("Building Trustworthy Enterprise RAG and AI Agents")
    c.setAuthor("Rosso Han")
    c.setSubject("Enterprise RAG, AI agents, evaluation, governance, and engineering leadership")

    draw_cover(c)
    c.showPage()
    draw_problem(c)
    c.showPage()
    draw_architecture(c)
    c.showPage()
    draw_trust(c)
    c.showPage()
    draw_evidence(c)
    c.showPage()
    draw_close(c)
    c.save()
    print(OUTPUT)


if __name__ == "__main__":
    generate()
