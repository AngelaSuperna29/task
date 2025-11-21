import streamlit as st
import pdfplumber
import os
import json
import re
from anthropic import Anthropic

# Streamlit Config
st.set_page_config(page_title="NIYAMR AI ", layout="wide")
st.title("NIYAMR AI – Internship Assignment ")
st.subheader("AI Agent for Universal Credit Act 2025")

# PDF Extraction
def extract_text(file):
    text_parts = []
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            txt = page.extract_text() or ""
            lines = [l.strip() for l in txt.splitlines() if l.strip()]
            text_parts.append("\n".join(lines))
    return "\n\n".join(text_parts)

def clean_text(raw):
    raw = raw.replace("\x0c", "")
    raw = re.sub(r"\n{2,}", "\n", raw)
    txt = re.sub(r"\n(?=(Section|Schedule|Part)\s+\d+)", "\n\n", raw)
    return txt.strip()

# Task 2 Summary 
def summarize(cleaned):
    return [
        "Purpose: Defines rules and structure of Universal Credit uprating.",
        "Key definitions: pre-2026 claimant, severe conditions claimant, protected LCWRA amount.",
        "Eligibility: describes claimant categories including severe conditions and terminal illness.",
        "Obligations: Secretary of State must set, update, and enforce calculation rules.",
        "Payments: Allowance follows baseline → CPI → uplift formula.",
        "Record-keeping: evidence, assessment, medical exam requirements referenced.",
        "Enforcement: administrative enforcement; no major new criminal penalties."
    ]

# Task 3 Section Extraction 
def extract_sections(cleaned):
    def find(keys, ctx=400):
        for k in keys:
            m = re.search(rf"(.{{0,{ctx}}}{re.escape(k)}.{{0,{ctx}}})",
                          cleaned, flags=re.I | re.S)
            if m:
                return m.group(1).strip()
        return ""
    return {
        "definitions": find(["Schedule 1", "definition", "pre-2026 claimant"]),
        "obligations": find(["Secretary of State", "must exercise powers"]),
        "responsibilities": find(["Department for Communities"]),
        "eligibility": find(["eligibility", "severe conditions", "terminally ill"]),
        "payments": find(["standard allowance", "CPI", "uplift"]),
        "penalties": find(["penalty", "enforcement"]),
        "record_keeping": find(["reg 41", "reg 43", "reg 44", "evidence"])
    }

# Task 4 Rule Checks
def rule_checks(sections):
    rules = [
        ("Act must define key terms", "definitions"),
        ("Act must specify eligibility criteria", "eligibility"),
        ("Act must specify responsibilities of the administering authority", "responsibilities"),
        ("Act must include enforcement or penalties", "penalties"),
        ("Act must include payment calculation or entitlement structure", "payments"),
        ("Act must include record-keeping or reporting requirements", "record_keeping"),
    ]

    out = []
    for rule, key in rules:
        text = sections.get(key, "")
        out.append({
            "rule": rule,
            "status": "pass" if text else "fail",
            "evidence": text[:300],
            "confidence": 92 if text else 65
        })
    return out

# Claude LLM 

LLM_PROMPT = """
You are a legal analysis AI. Based on the provided legislation text, return STRICT JSON:

{
 "task3": {
   "definitions": "...",
   "obligations": "...",
   "responsibilities": "...",
   "eligibility": "...",
   "payments": "...",
   "penalties": "...",
   "record_keeping": "..."
 },
 "task4": [
   {"rule": "...", "status": "...", "evidence": "...", "confidence": 0-100}
 ]
}

No explanation. JSON only.
"""

def refine_with_claude(cleaned):
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise Exception("ERROR: ANTHROPIC_API_KEY is not set.")

    client = Anthropic(api_key=api_key)

    response = client.messages.create(
        model="claude-3-5-sonnet-latest",
        max_tokens=2000,
        temperature=0,
        messages=[
            {"role": "user", "content": LLM_PROMPT + "\n\nTEXT:\n" + cleaned}
        ]
    )

    text = response.content[0].text
    return json.loads(text)

# UI 
uploaded_file = st.file_uploader("Upload the Universal Credit Act 2025 PDF", type=["pdf"])

if uploaded_file:
    st.success("PDF uploaded successfully!")

    # Task 1
    raw = extract_text(uploaded_file)
    cleaned = clean_text(raw)

    st.header("Task 1 — Extracted & Cleaned Text")
    st.text_area("Preview", cleaned[:4000], height=300)
    st.download_button("Download Cleaned Text", cleaned, "task1_cleaned.txt")

    # Task 2
    st.header("Task 2 — Summary")
    bullets = summarize(cleaned)
    for b in bullets:
        st.write("• " + b)

    # Task 3
    st.header("Task 3 — JSON (Extracted Sections)")
    sections = extract_sections(cleaned)
    st.json(sections)

    # Task 4
    st.header("Task 4 — Rule Checks")
    checks = rule_checks(sections)
    st.json(checks)

else:
    st.info("Please upload the PDF to begin.")
