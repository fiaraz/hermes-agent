---
name: exam-content-query
description: "Query the exam-content vector KB for specifications, and update the KB with examiner reports and past papers"
version: 1.0
author: Oracle
tags: [exams, specifications, examiner-reports, past-papers, aqa, edexcel, chemistry, biology, physics]
---

# Exam Content Query

Query the vector knowledge base of exam board specifications, examiner reports, and past papers for AQA and Edexcel Chemistry, Biology, and Physics.

## Knowledge Base

- **Name:** exam-content
- **Location:** `~/oracle-kb/dbs/exam-content.db`
- **Web UI:** https://oracle.shunka.org/kb/
- **CLI:** `kb query exam-content "question" -k 5` (semantic search)
- **CLI:** `kb ask exam-content "question" -k 5` (RAG answer)

## Status

| Metric | Value |
|--------|-------|
| Documents | ~1730 chunks |
| Size | ~19.6 MB |
| Specs ingested | 4 AQA GCSE, 3 AQA A-level, 3 Edexcel GCSE, 3 Edexcel A-level |
| Examiner reports | AQA GCSE Chemistry 8462 Paper 1H 2023, AQA GCSE Biology 8461 Paper 1H 2023, AQA A-level Chemistry 7405 Paper 1 2023 |
| Past papers | Not yet added |

## What's indexed

### AQA GCSE (8461, 8462, 8463, 8464)
All 4 specs: Physics, Chemistry, Biology, Combined Science: Trilogy

### AQA A-level (7402, 7405, 7408)
All 3 specs: Physics, Chemistry, Biology

### Edexcel GCSE (1BI0, 1CH0, 1PH0)
All 3 specs: Biology, Chemistry, Physics

### Edexcel A-level (9BI0, 9CH0, 9PH0)
All 3 specs: Biology B, Chemistry, Physics

## Query examples

```bash
# Semantic search
kb query exam-content "Newton's Third Law force pairs gcse physics" -k 5

# RAG (answer with sources)
kb ask exam-content "What specification points cover organic chemistry in AQA A-level Chemistry?" -k 5

# Find examiner guidance on a topic
kb query exam-content "examiner report common mistakes mole calculations" -k 5
```

## Adding examiner reports

To add examiner reports for a specific subject/board:

1. **Find the report URL**: Exam board websites have examiner reports under "Past papers and mark schemes" or "Resources"
2. **Download and extract text**: Use `curl` for the PDF, then pymupdf to extract text
3. **Ingest into KB**:
```bash
python3 -c "
import fitz, subprocess
# Download examiners report
# curl -sL -o /tmp/report.pdf <url>
doc = fitz.open('/tmp/report.pdf')
text = ''
for page in doc:
    text += page.get_text()
doc.close()
# Ingest in chunks
chunk_size = 50000
chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
for i, chunk in enumerate(chunks):
    title = f'AQA GCSE Chemistry Examiner Report 2025 (part {i+1}/{len(chunks)})'
    subprocess.run(['kb', 'add-text', 'exam-content', title, chunk])
"
```

### AQA Examiner Report URL patterns
```
# A-level 2024
https://filestore.aqa.org.uk/sample-papers-and-mark-schemes/2024/june/AQA-74051-WRE-JUN24.PDF
# GCSE 2024
https://filestore.aqa.org.uk/sample-papers-and-mark-schemes/2024/june/AQA-84621-WRE-JUN24.PDF
```

Replace subject code (74051, 84621, etc.) and year as needed.

### Edexcel Examiner Report URL patterns
Search qualifications.pearson.com for specific report links.

## Adding past papers (optional)

Past papers can be added using a similar process. However, they are large (100+ pages each) and may contain embedded images that don't extract well as text. Focus on specifications and examiner reports first.

## CLI helper

```bash
# Quick check what's in the KB
kb list
kb query exam-content "topic name" -k 3

# Check the web UI
# Open https://oracle.shunka.org/kb/ and select "exam-content" KB
```