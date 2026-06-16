from pathlib import Path

from docling.chunking import HybridChunker
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
    TesseractCliOcrOptions,
)
from docling.document_converter import (
    DocumentConverter,
    PdfFormatOption,
)


# -----------------------------
# Configure OCR
# -----------------------------
pipeline_options = PdfPipelineOptions()

pipeline_options.do_ocr = True

ocr_options = TesseractCliOcrOptions(
    force_full_page_ocr=True
)

pipeline_options.ocr_options = ocr_options


# -----------------------------
# Create Converter
# -----------------------------
converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(
            pipeline_options=pipeline_options
        )
    }
)


# -----------------------------
# Convert FDAW1
# -----------------------------
pdf_path = Path("documents/FDAW1.pdf")

print(f"Processing {pdf_path.name}...")

result = converter.convert(pdf_path)

doc = result.document

print("Document converted successfully!")


# -----------------------------
# Hybrid Chunking
# -----------------------------
chunker = HybridChunker()

chunks = list(chunker.chunk(dl_doc=doc))

print(f"Total Chunks Generated: {len(chunks)}")


# -----------------------------
# Save Chunks
# -----------------------------
output_dir = Path("outputs/chunks")
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / "FDAW1_chunks.txt"

with open(output_file, "w", encoding="utf-8") as f:

    for i, chunk in enumerate(chunks, start=1):

        f.write("=" * 80 + "\n")
        f.write(f"CHUNK {i}\n")
        f.write("=" * 80 + "\n")

        f.write(chunk.text.strip())
        f.write("\n\n")


print(f"Chunks saved to {output_file}")