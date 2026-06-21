import pdfplumber
import os

pdf_files = [
    "FDAW1.pdf",
    "FDAW2.pdf",
    "FDAW3.pdf",
    "chemR.pdf"
]

os.makedirs("outputs/naive", exist_ok=True)

for pdf in pdf_files:
    print(f"Processing {pdf}")

    text = ""

    try:
        with pdfplumber.open(f"documents/{pdf}") as pdf_file:
            for page in pdf_file.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n\n"

        output_path = f"outputs/naive/{pdf.replace('.pdf', '.txt')}"

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"Saved → {output_path}")

    except Exception as e:
        print(f"Error in {pdf}")
        print(e)