import io
import logging
from pathlib import Path

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Image as RLImage
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

logger = logging.getLogger(__name__)


class PDFExporter:
    """
    Generates a clean, professional PDF document from DocVision OCR results,
    including metadata header, confidence badge, processed document scan image,
    and formatted extracted text.
    """

    def generate_pdf(
        self,
        document_id: str,
        text: str,
        confidence: float,
        image_path: Path | None = None
    ) -> io.BytesIO:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40
        )

        styles = getSampleStyleSheet()

        # Custom typography styles
        title_style = ParagraphStyle(
            'DocVisionTitle',
            parent=styles['Heading1'],
            fontSize=22,
            leading=26,
            textColor=colors.HexColor('#0f172a'),
            spaceAfter=6
        )

        meta_style = ParagraphStyle(
            'DocVisionMeta',
            parent=styles['Normal'],
            fontSize=9,
            leading=12,
            textColor=colors.HexColor('#475569')
        )

        body_style = ParagraphStyle(
            'DocVisionBody',
            parent=styles['Normal'],
            fontSize=10,
            leading=15,
            textColor=colors.HexColor('#1e293b')
        )

        story = []

        # 1. Title & Header
        story.append(Paragraph("DocVision &bull; Scanned Document Report", title_style))
        story.append(Paragraph(f"Document ID: <b>{document_id}</b> &bull; OCR Confidence: <b>{confidence}%</b>", meta_style))
        story.append(Spacer(1, 15))

        # 2. Processed Document Image Preview (if provided)
        if image_path and Path(image_path).exists():
            try:
                with PILImage.open(image_path) as pil_img:
                    orig_w, orig_h = pil_img.size
                    aspect = orig_h / float(orig_w) if orig_w > 0 else 1.0

                    target_width = 320
                    target_height = min(target_width * aspect, 260)

                img_flowable = RLImage(str(image_path), width=target_width, height=target_height)
                story.append(img_flowable)
                story.append(Spacer(1, 15))
            except Exception as e:
                logger.warning("Could not include image in PDF: %s", e)

        # 3. Section Heading
        section_style = ParagraphStyle(
            'SectionHeader',
            parent=styles['Heading2'],
            fontSize=14,
            leading=18,
            textColor=colors.HexColor('#2563eb'),
            spaceAfter=8
        )
        story.append(Paragraph("Extracted Text", section_style))

        # 4. Extracted Text Body
        paragraphs = text.split("\n")
        for para in paragraphs:
            clean_para = para.strip()
            if clean_para:
                story.append(Paragraph(clean_para, body_style))
                story.append(Spacer(1, 4))
            else:
                story.append(Spacer(1, 6))

        # Build Document
        doc.build(story)
        buffer.seek(0)
        return buffer
