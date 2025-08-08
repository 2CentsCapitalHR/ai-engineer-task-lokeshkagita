import gradio as gr
from doc_analyzer import analyze_documents
import os

def handle_upload(files):
    os.makedirs("outputs", exist_ok=True)
    message = ""
    for file in files:
        file_path = file.name if hasattr(file, "name") else file
        result = analyze_documents(file_path)
        message += f"\n✅ Reviewed: {file.name} → Saved to outputs/"
    return message

iface = gr.Interface(
    fn=handle_upload,
    inputs=gr.File(file_types=[".docx"], file_count="multiple"),
    outputs="text",
    title="Corporate Agent (ADGM Compliance Assistant)",
    description="Upload ADGM-related legal documents (.docx). This AI tool reviews and returns marked-up files + compliance reports."
)

if __name__ == "__main__":
    iface.launch(share=True)
