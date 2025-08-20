# resume_templates.py
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

import random

# Register some additional fonts (if available in system)
try:
    pdfmetrics.registerFont(TTFont("Helvetica-Bold", "Helvetica-Bold.ttf"))
    pdfmetrics.registerFont(TTFont("Times-Roman", "Times-Roman.ttf"))
    pdfmetrics.registerFont(TTFont("Courier", "Courier.ttf"))
except:
    pass

def generate_resume_pdf(resume_text, template_id, buffer):
    """
    Generate resume PDF with different templates based on template_id (1-50).
    """
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()

    # Different fonts & colors for templates
    fonts = ["Helvetica", "Helvetica-Bold", "Times-Roman", "Courier"]
    colors_list = [
        colors.black, colors.darkblue, colors.green, colors.purple, colors.red, colors.teal
    ]

    # Template variations
    font_choice = fonts[template_id % len(fonts)]
    color_choice = colors_list[template_id % len(colors_list)]
    leading = 14 + (template_id % 6)  # line spacing variation
    alignment = template_id % 4  # 0=left,1=center,2=right,3=justify

    # Define custom style
    custom_style = ParagraphStyle(
        "CustomStyle",
        parent=styles["Normal"],
        fontName=font_choice,
        fontSize=12,
        textColor=color_choice,
        leading=leading,
        alignment=alignment,
    )

    # Build document
    story = []
    story.append(Paragraph(f"<b>Resume Template {template_id}</b>", styles["Title"]))
    story.append(Spacer(1, 12))

    # Split resume text into paragraphs
    for line in resume_text.split("\n"):
        if line.strip():
            story.append(Paragraph(line.strip(), custom_style))
            story.append(Spacer(1, 6))

    doc.build(story)
