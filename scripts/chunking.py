from docling.document_converter import DocumentConverter
from docling_core.transforms.chunker.hybrid_chunker import HybridChunker

# Convert ChemR document
converter = DocumentConverter()
result = converter.convert("documents/chemR.pdf")

# Create chunker
chunker = HybridChunker()

# Generate chunks
chunks = list(chunker.chunk(dl_doc=result.document))

print(f"Total Chunks Generated: {len(chunks)}\n")

# Print first 10 chunks
for i, chunk in enumerate(chunks[:10]):
    print("=" * 80)
    print(f"CHUNK {i+1}")
    print("=" * 80)
    print(chunk.text)
    print("\n")