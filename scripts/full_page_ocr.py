from pathlib import Path
import json


from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
    TableStructureOptions,
    TesseractCliOcrOptions,
)
from docling.document_converter import DocumentConverter, PdfFormatOption


def main():

    # PDF you want to test
    input_doc_path = Path("documents/FDAW1.pdf")

    # Configure pipeline
    pipeline_options = PdfPipelineOptions()

    pipeline_options.do_ocr = True
    pipeline_options.do_table_structure = True

    pipeline_options.table_structure_options = TableStructureOptions(
        do_cell_matching=True
    )

    # Force OCR on the entire page
    ocr_options = TesseractCliOcrOptions(force_full_page_ocr=True)

    pipeline_options.ocr_options = ocr_options

    # Create converter
    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options
            )
        }
    )

    print("Running OCR...")

    result = converter.convert(input_doc_path)

    doc = result.document

    # Export markdown
    md = doc.export_to_markdown()

    print("\nMarkdown Preview:\n")
    print(md[:5000])

    # Export JSON
    json_data = doc.export_to_dict()

    print("\nNumber of text elements:",
          len(json_data.get("texts", [])))


if __name__ == "__main__":
    main()
