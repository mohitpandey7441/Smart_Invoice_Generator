import random
import streamlit as st
import pandas as pd
from datetime import datetime

from database import (
    save_invoice,
    load_invoices,
    get_invoice_by_id,
    delete_invoice,
    get_total_revenue,
    get_invoice_count
)

from pdf_generator import generate_pdf

# =========================================================
# RANDOM INVOICE NUMBER
# =========================================================

def generate_invoice_number():
    return f"INV-{random.randint(1000,9999)}"

# Generate invoice number only once
if "invoice_number" not in st.session_state:
    st.session_state.invoice_number = generate_invoice_number()

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Invoice Generator",
    page_icon="📄",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 12px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}

.stat-box {
    background: #f0f2f6;
    padding: 1.5rem;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.stat-value {
    font-size: 2rem;
    font-weight: bold;
    color: #667eea;
}

.stat-label {
    font-size: 1rem;
    color: #666;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827 0%, #1f2937 100%);
}

section[data-testid="stSidebar"] * {
    color: white;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SESSION STATE
# =========================================================

if 'page' not in st.session_state:
    st.session_state.page = 'create'

if 'invoice_items' not in st.session_state:
    st.session_state.invoice_items = [
        {
            'description': '',
            'quantity': 1,
            'rate': 0.0
        }
    ]

if 'pdf_ready' not in st.session_state:
    st.session_state.pdf_ready = None

if 'invoice_saved' not in st.session_state:
    st.session_state.invoice_saved = False

# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="main-header">
    <h1>📄 Smart Invoice Generator</h1>
    <p>Create Professional Invoices Instantly</p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("📌 Navigation")

    if st.button("➕ Create Invoice", use_container_width=True):
        st.session_state.page = 'create'

    if st.button("📊 View All Invoices", use_container_width=True):
        st.session_state.page = 'list'

    if st.button("📈 Dashboard", use_container_width=True):
        st.session_state.page = 'dashboard'

    st.divider()

    st.subheader("📌 Quick Stats")

    total_invoices = get_invoice_count()
    total_revenue = get_total_revenue()

    st.metric("Total Invoices", total_invoices)
    st.metric("Total Revenue", f"₹{total_revenue:,.2f}")

# =========================================================
# CREATE PAGE
# =========================================================

if st.session_state.page == 'create':

    st.header("➕ Create New Invoice")

    # =====================================================
    # ADD / REMOVE ITEM BUTTONS
    # =====================================================

    col_add, col_remove = st.columns(2)

    with col_add:

        if st.button("➕ Add Item", use_container_width=True):

            st.session_state.invoice_items.append({
                'description': '',
                'quantity': 1,
                'rate': 0.0
            })

            st.rerun()

    with col_remove:

        if len(st.session_state.invoice_items) > 1:

            if st.button("➖ Remove Last Item", use_container_width=True):

                st.session_state.invoice_items.pop()

                # st.rerun()

    # =====================================================
    # FORM
    # =====================================================

    with st.form("invoice_form"):

        # =================================================
        # INVOICE DETAILS
        # =================================================

        col1, col2, col3 = st.columns(3)

        with col1:

            invoice_number = st.text_input(
                "Invoice Number*",
                value=st.session_state.invoice_number,
                disabled=True
            )

        with col2:

            invoice_date = st.date_input(
                "Invoice Date*",
                value=datetime.now()
            )

        with col3:

            due_date = st.date_input(
                "Due Date*"
            )

        st.divider()

        # =================================================
        # PARTY DETAILS
        # =================================================

        st.subheader("🏢 Party Details")

        col1, col2 = st.columns(2)

        # FROM
        with col1:

            st.markdown("### From")

            from_name = st.text_input("Company / Name*")
            from_email = st.text_input("Email")
            from_phone = st.text_input("Phone")
            from_address = st.text_area("Address")

        # TO
        with col2:

            st.markdown("### Bill To")

            to_name = st.text_input("Client Name*")
            to_email = st.text_input("Client Email")
            to_phone = st.text_input("Client Phone")
            to_address = st.text_area("Client Address")

        st.divider()

        # =================================================
        # ITEMS
        # =================================================

        st.subheader("🛒 Invoice Items")

        items_data = []

        for i, item in enumerate(st.session_state.invoice_items):

            st.markdown(f"### Item {i+1}")

            col1, col2, col3 = st.columns([3, 1, 1.5])

            with col1:

                desc = st.text_input(
                    "Description",
                    value=item['description'],
                    key=f"desc_{i}"
                )

            with col2:

                qty = st.number_input(
                    "Qty",
                    min_value=1,
                    value=item['quantity'],
                    key=f"qty_{i}"
                )

            with col3:

                rate = st.number_input(
                    "Rate (₹)",
                    min_value=0.0,
                    value=item['rate'],
                    key=f"rate_{i}",
                    format="%.2f"
                )

            amount = qty * rate

            st.markdown(f"**Amount: ₹{amount:,.2f}**")

            items_data.append({
                'description': desc,
                'quantity': qty,
                'rate': rate,
                'amount': amount
            })

            st.divider()

        # =================================================
        # TOTALS
        # =================================================

        subtotal = sum(item['amount'] for item in items_data)

        col1, col2, col3 = st.columns([2, 1, 1])

        with col2:

            tax_rate = st.number_input(
                "Tax (%)",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=0.1
            )

        tax_amount = (subtotal * tax_rate) / 100

        total = subtotal + tax_amount

        # =================================================
        # SUMMARY
        # =================================================

        st.markdown("## 💰 Invoice Summary")

        col1, col2 = st.columns([3, 1])

        with col2:

            st.success(f"""
Subtotal: ₹{subtotal:,.2f}

Tax: ₹{tax_amount:,.2f}

Total: ₹{total:,.2f}
""")

        notes = st.text_area(
            "Additional Notes",
            placeholder="Payment terms, thank you message, etc..."
        )

        # =================================================
        # SUBMIT BUTTON
        # =================================================

        submitted = st.form_submit_button(
            "📥 Generate & Save Invoice",
            type="primary",
            use_container_width=True
        )

        # =================================================
        # SAVE INVOICE
        # =================================================

        if submitted:

            if st.session_state.invoice_saved:

                st.warning("Invoice already saved.")

            else:

                if not from_name or not to_name:

                    st.error("⚠️ Please fill all required fields.")

                else:

                    invoice_data = {

                        'invoice_number': invoice_number,

                        'date': invoice_date.strftime('%Y-%m-%d'),

                        'due_date': due_date.strftime('%Y-%m-%d'),

                        'from': {
                            'name': from_name,
                            'email': from_email,
                            'phone': from_phone,
                            'address': from_address
                        },

                        'to': {
                            'name': to_name,
                            'email': to_email,
                            'phone': to_phone,
                            'address': to_address
                        },

                        'items': items_data,

                        'subtotal': subtotal,

                        'tax': tax_rate,

                        'tax_amount': tax_amount,

                        'total': total,

                        'notes': notes
                    }

                    saved = save_invoice(invoice_data)

                    if saved:

                        st.session_state.invoice_saved = True

                        st.success(
                            f"✅ Invoice #{invoice_number} saved successfully!"
                        )

                        # Generate PDF
                        pdf_buffer = generate_pdf(invoice_data)

                        st.session_state.pdf_ready = {
                            "buffer": pdf_buffer,
                            "file_name": f"invoice_{invoice_number}.pdf"
                        }

                        # New Invoice Number
                        st.session_state.invoice_number = generate_invoice_number()

                        # Reset Items
                        st.session_state.invoice_items = [
                            {
                                'description': '',
                                'quantity': 1,
                                'rate': 0.0
                            }
                        ]

                    else:

                        st.error("⚠️ Duplicate Invoice Number Found!")

    # =====================================================
    # DOWNLOAD BUTTON
    # =====================================================

    if st.session_state.pdf_ready:

        st.download_button(
            label="📄 Download Invoice PDF",
            data=st.session_state.pdf_ready["buffer"],
            file_name=st.session_state.pdf_ready["file_name"],
            mime="application/pdf",
            type="primary",
            use_container_width=True
        )

        # Reset save flag
        st.session_state.invoice_saved = False

# =========================================================
# LIST PAGE
# =========================================================

elif st.session_state.page == 'list':

    st.header("📊 All Invoices")

    invoices = load_invoices()

    if not invoices:

        st.info("No invoices found.")

    else:

        df = pd.DataFrame(invoices)

        df['Date'] = df['date']

        df['Client'] = df['to'].apply(
            lambda x: x['name']
        )

        df['Amount'] = df['total'].apply(
            lambda x: f"₹{x:,.2f}"
        )

        display_df = df[
            ['id', 'invoice_number', 'Date', 'Client', 'Amount']
        ]

        display_df.columns = [
            'ID',
            'Invoice #',
            'Date',
            'Client',
            'Total'
        ]

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            invoice_id = st.selectbox(
                "Select Invoice",
                options=[inv['id'] for inv in invoices]
            )

        with col2:

            if st.button(
                "🗑️ Delete Selected Invoice",
                type="secondary"
            ):

                delete_invoice(invoice_id)

                st.success("Invoice deleted successfully!")

                st.rerun()

        if st.button(
            "👁️ View Invoice Details",
            type="primary"
        ):

            invoice = get_invoice_by_id(invoice_id)

            if invoice:

                st.subheader(
                    f"Invoice #{invoice['invoice_number']}"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.markdown("### From")

                    st.write(invoice['from']['name'])

                    st.write(invoice['from']['email'])

                with col2:

                    st.markdown("### To")

                    st.write(invoice['to']['name'])

                    st.write(invoice['to']['email'])

                st.markdown("### Invoice Items")

                items_df = pd.DataFrame(invoice['items'])

                st.dataframe(
                    items_df,
                    use_container_width=True,
                    hide_index=True
                )

                st.success(
                    f"Total Amount: ₹{invoice['total']:,.2f}"
                )

# =========================================================
# DASHBOARD PAGE
# =========================================================

elif st.session_state.page == 'dashboard':

    st.header("📈 Dashboard")

    invoices = load_invoices()

    total_revenue = sum(
        inv['total'] for inv in invoices
    ) if invoices else 0

    avg_invoice = (
        total_revenue / len(invoices)
        if invoices else 0
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-value">{len(invoices)}</div>
            <div class="stat-label">Total Invoices</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-value">₹{total_revenue:,.0f}</div>
            <div class="stat-label">Total Revenue</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:

        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-value">₹{avg_invoice:,.0f}</div>
            <div class="stat-label">Average Invoice</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    if invoices:

        st.subheader("🕒 Recent Invoices")

        recent = invoices[-5:][::-1]

        for inv in recent:

            with st.expander(
                f"Invoice #{inv['invoice_number']} - ₹{inv['total']:,.2f}"
            ):

                st.write(f"**Client:** {inv['to']['name']}")
                st.write(f"**Date:** {inv['date']}")
                st.write(f"**Items:** {len(inv['items'])}")
                st.write(f"**Total:** ₹{inv['total']:,.2f}")
