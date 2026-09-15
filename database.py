import json
import os

DATABASE_FILE = "invoices_data.json"


def load_invoices():
    """Load all invoices from JSON file"""

    if os.path.exists(DATABASE_FILE):

        with open(DATABASE_FILE, "r") as file:
            return json.load(file)

    return []


def save_invoice(invoice_data):
    """Save invoice and prevent duplicate invoice numbers"""

    invoices = load_invoices()
    print("SAVE CALLED")
    print(invoice_data)

    # Duplicate Check
    for inv in invoices:

        if inv["invoice_number"] == invoice_data["invoice_number"]:
            return False

    # Auto ID
    invoice_data["id"] = len(invoices) + 1

    invoices.append(invoice_data)

    with open(DATABASE_FILE, "w") as file:
        json.dump(invoices, file, indent=4)

    return True


def get_invoice_by_id(invoice_id):
    """Get invoice by ID"""

    invoices = load_invoices()

    for invoice in invoices:

        if invoice["id"] == invoice_id:
            return invoice

    return None


def delete_invoice(invoice_id):
    """Delete invoice"""

    invoices = load_invoices()

    updated_invoices = [
        inv for inv in invoices
        if inv["id"] != invoice_id
    ]

    with open(DATABASE_FILE, "w") as file:
        json.dump(updated_invoices, file, indent=4)


def get_total_revenue():
    """Get total revenue"""

    invoices = load_invoices()

    return sum(inv["total"] for inv in invoices)


def get_invoice_count():
    """Get total invoice count"""

    return len(load_invoices())
