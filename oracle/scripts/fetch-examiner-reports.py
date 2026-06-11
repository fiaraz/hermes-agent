#!/usr/bin/env python3
"""
Script to download and ingest AQA examiner reports into the exam-content KB.
Run periodically (e.g. after each exam series) to keep the KB current.

Usage: python3 fetch-examiner-reports.py
"""
import subprocess, os, sys, urllib.request, fitz

# AQA examiner report URL patterns
# Format: https://filestore.aqa.org.uk/sample-papers-and-mark-schemes/{year}/{month}/AQA-{code}-WRE-{period}.PDF
# Where code = subject code + paper, e.g. 84621H = GCSE Chemistry 8462 Paper 1 Higher
# Period = JUN24, JUN23, etc.

REPORTS = {
    # AQA GCSE 2024
    "AQA GCSE Chemistry Paper 1H 2024": "https://filestore.aqa.org.uk/sample-papers-and-mark-schemes/2024/june/AQA-84621H-WRE-JUN24.PDF",
    "AQA GCSE Chemistry Paper 2H 2024": "https://filestore.aqa.org.uk/sample-papers-and-mark-schemes/2024/june/AQA-84622H-WRE-JUN24.PDF",
    "AQA GCSE Biology Paper 1H 2024": "https://filestore.aqa.org.uk/sample-papers-and-mark-schemes/2024/june/AQA-84611H-WRE-JUN24.PDF",
    "AQA GCSE Biology Paper 2H 2024": "https://filestore.aqa.org.uk/sample-papers-and-mark-schemes/2024/june/AQA-84612H-WRE-JUN24.PDF",
    "AQA GCSE Physics Paper 1H 2024": "https://filestore.aqa.org.uk/sample-papers-and-mark-schemes/2024/june/AQA-84631H-WRE-JUN24.PDF",
    "AQA GCSE Physics Paper 2H 2024": "https://filestore.aqa.org.uk/sample-papers-and-mark-schemes/2024/june/AQA-84632H-WRE-JUN24.PDF",
    # AQA A-level 2024
    "AQA A-level Chemistry Paper 1 2024": "https://filestore.aqa.org.uk/sample-papers-and-mark-schemes/2024/june/AQA-74051-WRE-JUN24.PDF",
    "AQA A-level Chemistry Paper 2 2024": "https://filestore.aqa.org.uk/sample-papers-and-mark-schemes/2024/june/AQA-74052-WRE-JUN24.PDF",
    "AQA A-level Biology Paper 1 2024": "https://filestore.aqa.org.uk/sample-papers-and-mark-schemes/2024/june/AQA-74021-WRE-JUN24.PDF",
    "AQA A-level Biology Paper 2 2024": "https://filestore.aqa.org.uk/sample-papers-and-mark-schemes/2024/june/AQA-74022-WRE-JUN24.PDF",
    "AQA A-level Physics Paper 1 2024": "https://filestore.aqa.org.uk/sample-papers-and-mark-schemes/2024/june/AQA-74081-WRE-JUN24.PDF",
    "AQA A-level Physics Paper 2 2024": "https://filestore.aqa.org.uk/sample-papers-and-mark-schemes/2024/june/AQA-74082-WRE-JUN24.PDF",
    # AQA GCSE 2023
    "AQA GCSE Chemistry Paper 1H 2023": "https://filestore.aqa.org.uk/sample-papers-and-mark-schemes/2023/june/AQA-84621H-WRE-JUN23.PDF",
    "AQA GCSE Biology Paper 1H 2023": "https://filestore.aqa.org.uk/sample-papers-and-mark-schemes/2023/june/AQA-84611H-WRE-JUN23.PDF",
    "AQA A-level Chemistry Paper 1 2023": "https://filestore.aqa.org.uk/sample-papers-and-mark-schemes/2023/june/AQA-74051-WRE-JUN23.PDF",
}

os.makedirs("/tmp/exam-reports", exist_ok=True)

success = 0
failed = 0
for title, url in REPORTS.items():
    path = f"/tmp/exam-reports/{title.lower().replace(' ', '-').replace('/', '-')}.pdf"
    txt = path.replace(".pdf", ".txt")
    
    # Download
    try:
        urllib.request.urlretrieve(url, path)
        size = os.path.getsize(path)
        if size < 1000:  # Too small - probably error page
            print(f"  SKIP {title}: only {size} bytes")
            failed += 1
            continue
    except Exception as e:
        print(f"  FAIL {title}: {e}")
        failed += 1
        continue
    
    # Extract
    try:
        doc = fitz.open(path)
        num_pages = len(doc)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        with open(txt, "w") as f:
            f.write(text)
    except Exception as e:
        print(f"  EXTRACT FAIL {title}: {e}")
        failed += 1
        continue
    
    # Ingest
    chunk_size = 50000
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    for i, chunk in enumerate(chunks):
        suffix = f" (part {i+1}/{len(chunks)})" if len(chunks) > 1 else ""
        ct = f"{title} - Examiner Report{suffix}"
        r = subprocess.run(["kb", "add-text", "exam-content", ct, chunk], capture_output=True, text=True, timeout=30)
        if r.returncode != 0:
            print(f"  INGEST FAIL {ct}: {r.stderr[:100]}")
    
    print(f"  OK {title}: {num_pages} pages, {len(text)} chars, {len(chunks)} chunks")
    success += 1

print(f"\nDone. {success} ingested, {failed} failed/missing")