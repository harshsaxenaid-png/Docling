from docling.document_converter import DocumentConverter
import json
import os

# Initialize converter
converter = DocumentConverter()

# List of PDFs
pdf_files = [
    "FDAW1.pdf",
    "FDAW2.pdf",
    "FDAW3.pdf",
    "chemR.pdf"
]

for pdf in pdf_files:
    print(f"\nProcessing {pdf}...")

    pdf_path = f"documents/{pdf}"

    try:
        result = converter.convert(pdf_path)

        # ---------------- Markdown ----------------
        markdown = result.document.export_to_markdown()

        md_filename = pdf.replace(".pdf", ".md")
        md_path = f"outputs/markdown/{md_filename}"

        with open(md_path, "w", encoding="utf-8") as f:
            f.write(markdown)

        # ---------------- JSON ----------------
        json_data = result.document.export_to_dict()

        json_filename = pdf.replace(".pdf", ".json")
        json_path = f"outputs/json/{json_filename}"

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2)

        print(f"✓ Markdown saved to {md_path}")
        print(f"✓ JSON saved to {json_path}")

    except Exception as e:
        print(f"❌ Error processing {pdf}")
        print(e)

print("\nDone!")