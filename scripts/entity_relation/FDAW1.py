import json
import re
import subprocess
from pathlib import Path

# -----------------------------
# Configuration
# -----------------------------
CHUNK_FILE = "outputs/chunks/FDAW1_chunks.txt"
OUTPUT_FILE = "outputs/entity_relations/FDAW1_relations.json"

MODEL_NAME = "qwen2.5-coder:1.5b"


# -----------------------------
# Extract chunks from file
# -----------------------------
def extract_chunks(file_path):

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r"={80}\nCHUNK \d+\n={80}\n"

    chunks = re.split(pattern, content)

    return [chunk.strip() for chunk in chunks if chunk.strip()]


# -----------------------------
# Clean chunk text
# -----------------------------
def preprocess_chunk(chunk):

    # Replace FDA redactions
    chunk = re.sub(r"\(b\)\(\d+\)", "[REDACTED]", chunk)

    # Remove extra spaces/newlines
    chunk = re.sub(r"\s+", " ", chunk)

    return chunk.strip()


# -----------------------------
# Remove ANSI escape sequences
# -----------------------------
def clean_output(text):

    ansi_escape = re.compile(
        r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])"
    )

    return ansi_escape.sub("", text).strip()


# -----------------------------
# Extract JSON from model output
# -----------------------------
def extract_json(response):

    match = re.search(r"\{.*\}", response, re.DOTALL)

    if match:
        return match.group()

    return None


# -----------------------------
# Call Ollama
# -----------------------------
def get_entities_relations(chunk):

    prompt = f"""
You are an expert information extraction system.

Extract entities and relations from this FDA warning letter text.

Allowed Entity Types:
- Organization
- Equipment
- Defect
- Risk
- Process
- Corrective_Action
- Regulatory_Action

Rules:
1. Ignore pronouns like "your", "it", "this".
2. Completely ignore FDA redaction placeholders like [REDACTED].
3. Never output [REDACTED] as an entity.
4. Never output relations involving [REDACTED].
5. Extract only meaningful entities.
6. Prefer these relation types:
   - causes
   - compromises
   - results_in
   - requires
   - recommends
   - manufactures
   - affects
7. Return ONLY valid JSON.

Return this format:

{{
    "entities": [
        {{
            "entity": "",
            "type": ""
        }}
    ],
    "relations": [
        {{
            "source": "",
            "relation": "",
            "target": ""
        }}
    ]
}}

Text:
{chunk}
"""

    result = subprocess.run(
        ["ollama", "run", MODEL_NAME],
        input=prompt,
        capture_output=True,
        text=True,
    )

    response = clean_output(result.stdout)

    json_text = extract_json(response)

    if json_text:
        try:
            return json.loads(json_text)

        except json.JSONDecodeError:
            return {
                "error": "Invalid JSON",
                "raw_output": response,
            }

    return {
        "error": "No JSON Found",
        "raw_output": response,
    }


# -----------------------------
# Filter bad entities/relations
# -----------------------------
def clean_results(result):

    if "entities" in result:

        result["entities"] = [

            entity

            for entity in result["entities"]

            if (
                "[REDACTED]" not in entity.get("entity", "")
                and entity.get("entity", "").lower()
                not in [
                    "your",
                    "your firm",
                    "it",
                    "this",
                ]
            )
        ]

    if "relations" in result:

        result["relations"] = [

            relation

            for relation in result["relations"]

            if (
                "[REDACTED]" not in relation.get("source", "")
                and "[REDACTED]" not in relation.get("target", "")
                and relation.get("source", "").lower()
                not in [
                    "your",
                    "your firm",
                    "it",
                    "this",
                ]
                and relation.get("target", "").lower()
                not in [
                    "your",
                    "your firm",
                    "it",
                    "this",
                ]
            )
        ]

    return result


# -----------------------------
# Main
# -----------------------------
def main():

    chunks = extract_chunks(CHUNK_FILE)

    
    print(f"Processing {len(chunks)} chunk(s)...")

    all_results = []

    for i, chunk in enumerate(chunks, start=1):

        print(f"\nProcessing Chunk {i}...")

        chunk = preprocess_chunk(chunk)

        result = get_entities_relations(chunk)

        result = clean_results(result)

        all_results.append(
            {
                "chunk_number": i,
                "result": result,
            }
        )

    Path("outputs/entity_relations").mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:

        json.dump(
            all_results,
            f,
            indent=4,
            ensure_ascii=False,
        )

    print("\nDone!")
    print(f"Saved results to:\n{OUTPUT_FILE}")


if __name__ == "__main__":
    main()