# Observations Report: Parsing and Chunking using Docling

## 1. Parsing Documents using Docling

Docling was used to parse all four documents (`FDAW1.pdf`, `FDAW2.pdf`, `FDAW3.pdf`, and `chemR.pdf`). The outputs were exported into Markdown and JSON formats.

### Observations

* For **FDAW1, FDAW2, and FDAW3**, the Markdown output mainly contained image placeholders (`<!-- image -->`).

* In the JSON output of these documents, no text was extracted, but picture and group objects were present.

* This means that Docling was able to identify document regions and images but could not extract meaningful text from these documents.

* For **chemR.pdf**, Docling performed much better.

* Headings were preserved correctly.

* Paragraphs were extracted properly and remained readable.

* Tables were preserved in Markdown format.

* The JSON output contained structured information such as texts, tables, pictures, and groups.

### Summary of Docling Outputs

| Document | Structured Text | Tables | Pictures | Groups |
| -------- | --------------- | ------ | -------- | ------ |
| FDAW1    | No              | No     | Yes      | Yes    |
| FDAW2    | No              | No     | Yes      | Yes    |
| FDAW3    | No              | No     | Yes      | Yes    |
| chemR    | Yes             | Yes    | Yes      | Yes    |

---

## 2. Comparison with pdfplumber (Naive Baseline)

The same four documents were parsed using `pdfplumber` and compared with Docling outputs.

### Observations

* For **FDAW1, FDAW2, and FDAW3**, pdfplumber failed to extract any content, resulting in empty output files.

* Although Docling did not extract text from these documents, it still detected pictures and document groups, providing more information than pdfplumber.

* For **chemR.pdf**, pdfplumber extracted readable text and preserved headings reasonably well.

* However, tables lost their original structure and appeared as plain text.

### Comparison for chemR.pdf

| Feature                | Docling | pdfplumber |
| ---------------------- | ------- | ---------- |
| Headings Preserved     | Yes     | Yes        |
| Paragraphs Intact      | Yes     | Mostly Yes |
| Reading Order Correct  | Yes     | Mostly Yes |
| Tables Preserved       | Yes     | No         |
| Structured JSON Output | Yes     | No         |

### Comparison for FDAW Documents

| Feature                  | Docling                             | pdfplumber  |
| ------------------------ | ----------------------------------- | ----------- |
| Text Extracted           | No                                  | No          |
| Pictures Detected        | Yes                                 | No          |
| Document Groups Detected | Yes                                 | No          |
| Output Generated         | Image placeholders and JSON objects | Empty files |

---

## 3. Table Deep-Dive (chemR.pdf)

The `chemR.pdf` document contained several tables.

### Observations

* In Docling's JSON output, tables were represented as separate table objects.
* This preserved the table structure and document information.
* In pdfplumber output, the same tables were flattened into plain text, losing the row and column relationships.

### Table Comparison

| Feature                            | Docling | pdfplumber |
| ---------------------------------- | ------- | ---------- |
| Table Detection                    | Yes     | No         |
| Structured Table Representation    | Yes     | No         |
| Row-Column Relationships Preserved | Yes     | No         |

### Conclusion

Docling handled tables much better than pdfplumber by preserving their structure.

---

## 4. HybridChunker Evaluation

The HybridChunker was applied to `chemR.pdf`.

### Observations

* A total of **80 chunks** were generated.
* Most chunks contained information from a single logical section of the document.
* Examples included approval details, drug product information, manufacturing information, and recommendations.
* Some large sections were split into multiple chunks due to chunk size limitations.

### HybridChunker Results

| Observation                            | Result |
| -------------------------------------- | ------ |
| Total Chunks Generated                 | 80     |
| Section Boundaries Generally Respected | Yes    |
| Meaningful Chunks Produced             | Yes    |
| Long Sections Split Occasionally       | Yes    |

### Conclusion

The HybridChunker generally respected document structure and produced useful chunks suitable for downstream tasks such as Retrieval-Augmented Generation (RAG).

---

# Overall Conclusion

Docling performed significantly better on structured documents like `chemR.pdf` by preserving headings, paragraphs, tables, and document structure.

For the FDA warning letter documents, Docling could not extract textual content but still identified document elements such as pictures and groups. In contrast, pdfplumber generated empty outputs for these documents.

Overall, Docling provided richer and more structured document representations compared to a basic PDF extraction approach.
