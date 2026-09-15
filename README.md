# 🧾 Smart Invoice Generator

A simple and professional invoice management web application built with **Python and Streamlit**. The system allows users to create invoices, calculate invoice totals, save invoice records, generate professional PDF invoices, and manage previously created invoices.

---

## 📌 Project Overview

The **Smart Invoice Generator** is designed to reduce the manual effort involved in creating and managing invoices.

The application provides an easy-to-use Streamlit interface where users can enter customer details, add products or services, calculate invoice amounts automatically, generate a PDF invoice, and manage saved invoice records.

---

## ✨ Features

* 🧾 Create professional invoices
* 👤 Enter customer and business information
* 📦 Add multiple invoice items
* 🔢 Automatic quantity × price calculations
* 💰 Automatic subtotal and total calculation
* 📄 Generate PDF invoices using ReportLab
* 💾 Store invoice records using JSON
* 📋 View all saved invoices
* 🗑️ Delete invoices when required
* 📊 Dashboard for invoice statistics
* 🌐 Simple and interactive Streamlit interface

---

## 🛠️ Technologies Used

| Technology         | Purpose                   |
| ------------------ | ------------------------- |
| **Python 3.11.16** | Core programming language |
| **Streamlit**      | Web application interface |
| **Pandas**         | Data processing           |
| **ReportLab**      | PDF invoice generation    |
| **JSON**           | Invoice data storage      |

---

## 📂 Project Folder Structure

```text
INVOICE_APP\
│
├── app.py
├── database.py
├── pdf_generator.py
├── invoices_data.json
├── invoice_json
├── README.md
└── tempCodeRunnerFile.python
```

### File Description

* **app.py** – Main Streamlit application.
* **database.py** – Handles invoice data loading, saving, retrieving, and deleting.
* **pdf_generator.py** – Generates PDF invoices.
* **invoices_data.json** – Stores invoice records.
* **invoice_json** – Project invoice-data folder.
* **README.md** – Project documentation.
* **tempCodeRunnerFile.python** – Temporary development file.

---

## 🔄 Project Workflow

```text
Start
  │
  ▼
Open Streamlit Application
  │
  ▼
Enter Business & Customer Details
  │
  ▼
Add Invoice Items
  │
  ▼
Calculate Invoice Total
  │
  ▼
Generate & Save Invoice
  │
  ▼
Save Data in JSON
  │
  ▼
Generate PDF using ReportLab
  │
  ▼
View / Download Invoice
  │
  ▼
Manage Saved Invoices
  │
  ▼
End
```


## ▶️ Run the Application

Run the following command from the project directory:

```bash
streamlit run app.py
```

## 📊 Main Modules

### 1. Invoice Creation

Users can enter:

* Business information
* Customer information
* Invoice date
* Due date
* Product/service description
* Quantity
* Price/rate
* Notes

The system automatically calculates invoice amounts.

### 2. Data Management

The `database.py` module manages invoice records stored in:

```text
invoices_data.json
```

It supports:

* Loading invoices
* Saving invoices
* Finding invoices
* Deleting invoices
* Counting invoices
* Calculating total revenue

### 3. PDF Generation

The `pdf_generator.py` module uses **ReportLab** to generate a professional PDF invoice from the entered invoice information.

### 4. Invoice Dashboard

The dashboard provides useful invoice statistics such as:

* Total number of invoices
* Total revenue
* Average invoice value
* Recent invoices

---

## 🔐 Data Storage

Invoice information is stored locally in a JSON file:


## 🎯 Project Objectives

The main objectives of this project are:

* Automate the invoice creation process.
* Reduce manual calculation errors.
* Provide professional PDF invoices.
* Maintain invoice records digitally.
* Provide a simple invoice management interface.
* Demonstrate practical implementation of Python and Streamlit.

## 🚀 Future Scope

The project can be enhanced with:

* User authentication and login
* MySQL/PostgreSQL database integration
* Email invoice functionality
* Cloud data storage
* Invoice search and advanced filtering
* Company logo support
* Payment status tracking
* Online deployment
* Multiple invoice templates
* Tax and discount management

## ⭐ Conclusion

The **Smart Invoice Generator** provides a simple and efficient solution for creating, storing, generating, and managing invoices. By combining **Python, Streamlit, Pandas, JSON, and ReportLab**, the project demonstrates how a practical business application can be developed using Python-based technologies.

