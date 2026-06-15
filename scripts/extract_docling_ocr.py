from pathlib import Path
import json

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
    TableStructureOptions,
    TesseractCliOcrOptions,
)
from docling.document_converter import (
    DocumentConverter,
    PdfFormatOption,
)

# PDFs to process
pdf_files = [
    "FDAW1.pdf",
    "FDAW2.pdf",
    "FDAW3.pdf",
    "chemR.pdf",
]

# Configure OCR pipeline
pipeline_options = PdfPipelineOptions()

pipeline_options.do_ocr = True
pipeline_options.do_table_structure = True

pipeline_options.table_structure_options = TableStructureOptions(
    do_cell_matching=True
)

# Full-page OCR
ocr_options = TesseractCliOcrOptions(
    force_full_page_ocr=True
)

pipeline_options.ocr_options = ocr_options

# Create converter
converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(
            pipeline_options=pipeline_options
        )
    }
)

# Process all PDFs
for pdf in pdf_files:

    print(f"\nProcessing {pdf}...")

    try:

        pdf_path = Path("documents") / pdf

        result = converter.convert(pdf_path)

        doc = result.document

        # Save Markdown
        markdown = doc.export_to_markdown()

        md_path = (
            Path("outputs/markdown_ocr")
            / pdf.replace(".pdf", ".md")
        )

        with open(md_path, "w", encoding="utf-8") as f:
            f.write(markdown)

        # Save JSON
        json_data = doc.export_to_dict()

        json_path = (
            Path("outputs/json_ocr")
            / pdf.replace(".pdf", ".json")
        )

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2)

        print(f"✓ Markdown saved: {md_path}")
        print(f"✓ JSON saved: {json_path}")
        print(
            f"✓ Text elements: "
            f"{len(json_data.get('texts', []))}"
        )

    except Exception as e:

        print(f"❌ Error processing {pdf}")
        print(e)

print("\nDone!")