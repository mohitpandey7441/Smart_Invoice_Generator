from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)

from reportlab.lib.enums import (
    TA_CENTER
)

from io import BytesIO


def generate_pdf(invoice_data):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=0.5 * inch,
        bottomMargin=0.5 * inch
    )

    elements = []

    styles = getSampleStyleSheet()

    # =====================================================
    # TITLE STYLE
    # =====================================================

    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Heading1"],
        fontSize=24,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#667eea"),
        spaceAfter=30
    )

    title = Paragraph(
        "INVOICE",
        title_style
    )

    elements.append(title)

    elements.append(
        Spacer(1, 0.2 * inch)
    )

    # =====================================================
    # INVOICE DETAILS
    # =====================================================

    invoice_details = [
        ["Invoice #", invoice_data["invoice_number"]],
        ["Date", invoice_data["date"]],
        ["Due Date", invoice_data["due_date"]]
    ]

    details_table = Table(
        invoice_details,
        colWidths=[2 * inch, 3 * inch]
    )

    details_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("FONTSIZE", (0, 0), (-1, -1), 10)
    ]))

    elements.append(details_table)

    elements.append(
        Spacer(1, 0.3 * inch)
    )

    # =====================================================
    # PARTY DETAILS
    # =====================================================

    party_data = [
        ["FROM", "BILL TO"],

        [
            invoice_data["from"]["name"],
            invoice_data["to"]["name"]
        ],

        [
            invoice_data["from"]["email"],
            invoice_data["to"]["email"]
        ],

        [
            invoice_data["from"]["phone"],
            invoice_data["to"]["phone"]
        ],

        [
            invoice_data["from"]["address"],
            invoice_data["to"]["address"]
        ]
    ]

    party_table = Table(
        party_data,
        colWidths=[3 * inch, 3 * inch]
    )

    party_table.setStyle(TableStyle([

        ("BACKGROUND", (0, 0), (-1, 0),
         colors.HexColor("#f2f2f2")),

        ("FONTNAME", (0, 0), (-1, 0),
         "Helvetica-Bold"),

        ("TEXTCOLOR", (0, 0), (-1, 0),
         colors.grey),

        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),

        ("FONTSIZE", (0, 0), (-1, -1), 10)
    ]))

    elements.append(party_table)

    elements.append(
        Spacer(1, 0.3 * inch)
    )

    # =====================================================
    # ITEMS TABLE
    # =====================================================

    items_data = [
        ["Description", "Qty", "Rate", "Amount"]
    ]

    for item in invoice_data["items"]:

        items_data.append([
            item["description"],
            str(item["quantity"]),
            f"₹{item['rate']:.2f}",
            f"₹{item['amount']:.2f}"
        ])

    items_table = Table(
        items_data,
        colWidths=[3 * inch, 1 * inch, 1 * inch, 1.5 * inch]
    )

    items_table.setStyle(TableStyle([

        ("BACKGROUND", (0, 0), (-1, 0),
         colors.HexColor("#667eea")),

        ("TEXTCOLOR", (0, 0), (-1, 0),
         colors.white),

        ("FONTNAME", (0, 0), (-1, 0),
         "Helvetica-Bold"),

        ("ALIGN", (1, 0), (-1, -1),
         "CENTER"),

        ("GRID", (0, 0), (-1, -1),
         1, colors.grey),

        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),

        ("FONTSIZE", (0, 0), (-1, -1), 9)
    ]))

    elements.append(items_table)

    elements.append(
        Spacer(1, 0.3 * inch)
    )

    # =====================================================
    # TOTALS
    # =====================================================

    totals_data = [
        ["Subtotal", f"₹{invoice_data['subtotal']:.2f}"],

        [
            f"Tax ({invoice_data['tax']}%)",
            
        ],

        ["Total", f"₹{invoice_data['total']:.2f}"]
    ]

    totals_table = Table(
        totals_data,
        colWidths=[2 * inch, 2 * inch],
        hAlign="RIGHT"
    )

    totals_table.setStyle(TableStyle([

        ("FONTNAME", (0, 2), (-1, 2),
         "Helvetica-Bold"),

        ("TEXTCOLOR", (0, 2), (-1, 2),
         colors.HexColor("#667eea")),

        ("LINEABOVE", (0, 2), (-1, 2),
         2, colors.HexColor("#667eea")),

        ("ALIGN", (0, 0), (-1, -1),
         "RIGHT"),

        ("BOTTOMPADDING", (0, 0), (-1, -1), 8)
    ]))

    elements.append(totals_table)

    # =====================================================
    # NOTES
    # =====================================================

    if invoice_data.get("notes"):

        elements.append(
            Spacer(1, 0.3 * inch)
        )

        notes = Paragraph(
            f"<b>Notes:</b><br/>{invoice_data['notes']}",
            styles["Normal"]
        )

        elements.append(notes)

    # =====================================================
    # BUILD PDF
    # =====================================================

    doc.build(elements)

    buffer.seek(0)

    return buffer
