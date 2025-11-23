 NIYAMR AI – Internship Assignment
AI Agent for Legislative Analysis (Universal Credit Act 2025)

This repository contains my submission for the NIYAMR AI Internship (AI Agent Development).
The project processes the Universal Credit Act 2025 and completes Tasks 1–4:

1. Text Extraction
2. Summarisation
3. Key Section Extraction (JSON)
4. Rule-based Compliance Checks

Built using Streamlit, pdfplumber, and optional Claude 3.5 Sonnet for LLM refinement.

Project Structure
.
├── code/
│   ├── app.py                 # Streamlit application
│   └── requirements.txt       # Python dependencies
│
├── data/
│   └── universal_credit_act_2025_cleaned.txt   # Cleaned extracted text
│
├── output/
│   ├── task3_report.json      # Final structured JSON (Task 3)
│   └── task4_checks.json      # Rule checks (Task 4)
│
└── README.md

 Features
Task 1 — Text Extraction

Extracts full text from the PDF using pdfplumber

Cleans noise, line breaks, and formatting issues

Task 2 — Summary

5–10 concise bullet points covering:

Purpose

Key definitions

Eligibility criteria

Obligations

Payments

Enforcement

Record-keeping

Task 3 — JSON Extraction

Extracts the following sections into a structured JSON:

Definitions

Obligations

Responsibilities

Eligibility

Payments

Penalties

Record-keeping

Task 4 — Rule Checks

Evaluates the Act against 6 logical rules.
Each item includes:

{
  "rule": "…",
  "status": "pass/fail",
  "evidence": "...",
  "confidence": 0–100
}

Optional — Claude 3.5 Sonnet Refinement

Produces high-accuracy JSON for Tasks 3 & 4.
Requires an ANTHROPIC_API_KEY.

 Installation
1. Install dependencies
pip install -r code/requirements.txt

2. (Optional) Add Claude API Key

For Windows:

setx ANTHROPIC_API_KEY "your-key"


macOS/Linux:

export ANTHROPIC_API_KEY="your-key"


Restart your terminal after setting the key.

 Run the App

Run Streamlit:

streamlit run app.py


Then upload the Universal Credit Act 2025 PDF and the app will automatically:

1. Extract
2. Summarise
3. Generate JSON
4. Run rule checks

 Input PDF Used

The analysis was generated using the provided file:

/mnt/data/universal credit act 2025.pdf

 Deliverables Included in Repository

Streamlit application (app.py)

Clean text extraction

Task 3 JSON

Task 4 JSON

requirements.txt

README.md
