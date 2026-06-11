---
name: exam-question-analyser
description: "Analyse past papers for topic frequency, trends, and revision guidance"
version: 1.0
author: Oracle
tags: [teaching, exams, analysis, past-papers, revision, chemistry, biology]
---

# Exam Question Analyser

Analyse GCSE and A-level past papers (AQA, Edexcel, OCR, CIE) to identify topic frequency, question trends, and provide data-driven revision guidance.

## When to use

Load this skill when the user asks to:
- Analyse which topics appear most often in past papers
- Predict likely topics for an upcoming exam
- Find weak areas by topic across a student's past paper attempts
- Generate a revision priority list based on topic weightings
- Compare exam board emphasis across different topics
- Check what types of questions come up for a specific topic

## Data sources

The analyser can work with:
1. **Past paper PDFs you provide** -- I scan the content and classify questions by topic
2. **Exam board specification documents** -- I use the spec to map questions to topic codes
3. **My own training knowledge** -- I can provide topic weightings from publicly available specifications
4. **Web search** -- I can search for published grade boundaries and examiner reports

For best results, provide the actual past paper files (PDFs). I can read them via web_extract (for online PDFs) or via OCR/document tools if scanned.

## Process

### Step 1: Clarify scope

Ask the user for:
- **Subject:** Chemistry / Biology / Combined Science
- **Level:** GCSE / iGCSE / A-level
- **Exam board:** AQA / Edexcel / OCR A / OCR B / CIE
- **Paper type:** Paper 1 / Paper 2 / Paper 3 / All
- **Years to analyse:** e.g. 2022-2025 (default: last 3 years)
- **Specific topic focus** (optional): e.g. only analyse organic chemistry questions

### Step 2: Retrieve specification document

If the user doesn't provide past papers, use web_search to find the latest specification for their subject/board/level.

Key reference documents:
- AQA specifications have clear topic codes (e.g. 3.1.2, 3.3.4)
- Edexcel specifications use topic numbers
- OCR A uses module numbers

### Step 3: Map papers to topics (if PDFs provided)

When the user provides past papers (via file path or URL):
1. Extract text or read the document
2. Classify each question by:
   - Topic (as per specification)
   - Question type (multiple choice, short answer, calculation, essay, practical)
   - Marks available
   - Command word used (Describe, Explain, Calculate, Evaluate, Suggest)
3. Build a topic frequency table

### Step 4: Generate analysis

Output a structured analysis with these sections:

**Topic frequency table**
```
| Topic | Paper 1 | Paper 2 | Paper 3 | Total marks | % of total |
|-------|---------|---------|---------|-------------|------------|
| Atomic structure | 12 | 8 | 0 | 20 | 8% |
| Bonding | 6 | 14 | 4 | 24 | 10% |
| Energetics | 4 | 0 | 12 | 16 | 7% |
| Rate equations | 0 | 10 | 8 | 18 | 8% |
| ... | ... | ... | ... | ... | ... |
```

**Question type breakdown**
```
Multiple choice:  12 questions (24 marks, 15%)
Short answer:     18 questions (36 marks, 22%)
Calculation:       8 questions (32 marks, 20%)
Extended response: 6 questions (42 marks, 26%)
Practical:         4 questions (28 marks, 17%)
```

**Trends and patterns**
- Topics appearing every year (highly likely to appear again)
- Topics appearing every other year (alternating)
- Topics that haven't appeared in 2+ years (due for reappearance)
- Shifts in emphasis (more calculation questions recently, etc.)
- Recurring question formats ("Describe a method for..."

**Revision priority list**
```
HIGH PRIORITY (appear on every paper):
1. Amount of substance - 15% of marks
2. Organic mechanisms - 12% of marks

MEDIUM PRIORITY (appear frequently):
3. Energetics - 8% of marks
4. Kinetics - 7% of marks

LOWER PRIORITY (appear occasionally):
5. NMR spectroscopy - 4% of marks
6. Periodicity - 3% of marks

WATCH LIST (overdue for appearance):
7. Born-Haber cycles - last appeared 2023
8. Transition metal complexes - last appeared 2022
```

### Step 5: Provide actionable revision guidance

Based on the analysis:
- Which topics to prioritise for last-minute revision
- Which question formats to practise
- Common pitfalls per high-weight topic
- Mark scheme traps (what examiners look for)
- Timing strategy (how many minutes per mark)

### Step 6: Save analysis (optional)

If the user wants it saved:
```
~/tutoring-materials/analysis/{subject}-{level}-{board}-{date}.md
```

## Topic lookup reference

### AQA A-level Chemistry topic codes
- 3.1.1 Atomic structure
- 3.1.2 Amount of substance
- 3.1.3 Bonding
- 3.1.4 Energetics
- 3.1.5 Kinetics
- 3.1.6 Equilibria
- 3.1.7 Oxidation/reduction
- 3.1.8 Thermodynamics
- 3.1.9 Rate equations
- 3.1.10 Equilibrium constant
- 3.1.11 Electrode potentials
- 3.1.12 Acids and bases
- 3.2.1 Periodicity
- 3.2.2 Group 2
- 3.2.3 Group 7
- 3.2.4 Properties of Period 3
- 3.2.5 Transition metals
- 3.2.6 Reactions of ions
- 3.3.1 Introduction to organic
- 3.3.2 Alkanes
- 3.3.3 Halogenoalkanes
- 3.3.4 Alkenes
- 3.3.5 Alcohols
- 3.3.6 Organic analysis
- 3.3.7 Optical isomerism
- 3.3.8 Aldehydes and ketones
- 3.3.9 Carboxylic acids
- 3.3.10 Aromatic chemistry
- 3.3.11 Amines
- 3.3.12 Polymers
- 3.3.13 Amino acids
- 3.3.14 Organic synthesis
- 3.3.15 NMR
- 3.3.16 Chromatography

## Pitfalls

- **Papers change format** -- a 2025 paper may have a different structure to a 2018 paper (spec changes, exam reform)
- **Topic mapping is approximate** -- question may span multiple topics
- **Don't guarantee predictions** -- frame as "likely" / "tends to appear", never "guaranteed to come up"
- **Grade boundaries change** per year and session
- **Don't claim exam board insider knowledge** -- use only publicly available information

## Verification

After analysis:
- Cross-check topic allocations with the specification document
- Verify marks sum to the paper total
- Flag any unusual patterns (e.g. a topic appearing far more than the spec weighting suggests)