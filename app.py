# app.py (updated for RAG-based analyzer)

import gradio as gr
from doc_analyzer import analyze_documents
import os

def handle_upload(files):
    os.makedirs("outputs", exist_ok=True)
    message = ""
    for file in files:
        file_path = file.name if hasattr(file, "name") else file
        result = analyze_documents(file_path)
        output_docx = result.get("output_docx", "")
        report_json = result.get("report_json", "")

        message += f"\n✅ Reviewed: {file.name}"
        message += f"\n📄 Marked-up File: {output_docx}"
        message += f"\n📊 Report: {report_json}\n"
    return message

iface = gr.Interface(
    fn=handle_upload,
    inputs=gr.File(file_types=[".docx"], file_count="multiple"),
    outputs="text",
    title="Corporate Agent (ADGM Compliance Assistant - RAG Enhanced)",
    description=(
        "Upload ADGM-related legal documents (.docx). This AI tool uses Retrieval-Augmented Generation (RAG) "
        "with Gemini to review files for compliance, flag issues, and return marked-up documents and reports."
    )
)

if __name__ == "__main__":
    iface.launch(share=True)
