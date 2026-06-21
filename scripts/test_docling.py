from docling.document_converter import DocumentConverter
import json

converter = DocumentConverter()

result = converter.convert("documents/chemR.pdf")

markdown = result.document.export_to_markdown()

print("Markdown Length:", len(markdown))
print(markdown)

print("\n\nJSON Preview:\n")

json_data = result.document.export_to_dict()

print(json.dumps(json_data, indent=2)[:3000])