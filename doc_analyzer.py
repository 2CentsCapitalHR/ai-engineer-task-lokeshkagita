import os
import json
from docx import Document
import google.generativeai as genai

# ✅ Gemini API setup
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))  # Replace with yours

# ✅ Correct model
model = genai.GenerativeModel("gemini-2.5-pro")

# ✅ Put this ABOVE all functions
ADGM_CONTEXT = """
You are a legal assistant specializing in Abu Dhabi Global Market (ADGM) compliance.
Refer to the ADGM Companies Regulations 2020 and standard incorporation templates.
Ensure documents specify jurisdiction as ADGM, have valid clauses, and proper signatory format.
"""

def ask_gemini(document_text):
    prompt = f"""
    {ADGM_CONTEXT}

    Review the following legal text for ADGM compliance. Identify:
    - Invalid or missing clauses
    - Wrong jurisdiction references
    - Ambiguous or non-binding language
    - Missing signature sections
    - Suggestions to correct each issue

    Text:
    \"\"\"{document_text}\"\"\"

    Respond ONLY in JSON format:
    {{
      "issues_found": [
        {{
          "section": "...",
          "issue": "...",
          "severity": "...",
          "suggestion": "..."
        }}
      ]
    }}
    """

    try:
        # ✅ Correct usage for Gemini Pro
        response = model.generate_content([
            {"role": "user", "parts": [prompt]}
        ])
        raw = response.text.strip()
        print("🧪 Gemini raw output:", raw)

        # Manually extract JSON from string
        json_start = raw.find('{')
        json_end = raw.rfind('}') + 1
        json_str = raw[json_start:json_end]

        result_json = json.loads(json_str)
        return result_json.get("issues_found", [])
    except Exception as e:
        print("❌ Gemini parsing error:", e)
        return []

def analyze_documents(file_path):
    os.makedirs("outputs", exist_ok=True)
    filename = os.path.basename(file_path)
    doc = Document(file_path)
    full_text = "\n".join([p.text for p in doc.paragraphs])
    issues = ask_gemini(full_text)

    output_path = os.path.join("outputs", f"reviewed_{filename}")
    reviewed = Document(file_path)
    reviewed.add_paragraph("")  # spacing
    for issue in issues:
        reviewed.add_paragraph(f"🔍 Comment: {issue['section']} — {issue['issue']} → {issue['suggestion']}")
    reviewed.save(output_path)

    report = {
        "process": "Company Incorporation",
        "documents_uploaded": 1,
        "required_documents": 5,
        "missing_document": [
            "Memorandum of Association",
            "Board Resolution Template",
            "UBO Declaration Form",
            "Register of Members and Directors"
        ],
        "issues_found": issues
    }

    report_path = os.path.join("outputs", f"{filename}_report.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=4)

    return {"output_docx": output_path, "report_json": report_path}
