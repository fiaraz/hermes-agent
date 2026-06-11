---
name: worksheet-generator
description: "Generate A-level/GCSE Chemistry & Biology worksheets with mark schemes"
version: 1.0
author: Oracle
tags: [teaching, chemistry, biology, worksheets, gcse, a-level, exam-practice]
---

# Worksheet Generator

Create exam-style worksheets for A-level and GCSE Chemistry and Biology, complete with mark schemes.

## When to use

Load this skill when the user asks to:
- Create a worksheet, practice paper, or revision sheet
- Generate exam-style questions on a specific topic
- Make a quick test or quiz for a student
- Produce a mark scheme to accompany questions
- Generate homework or classwork materials

## Subject & level reference

| Level | Subjects | Typical question types |
|-------|----------|----------------------|
| GCSE | Chemistry, Biology, Combined Science | Multiple choice, 1-2 mark short answer, 3-4 mark explain, 5-6 mark extended response |
| A-level | Chemistry, Biology | Multiple choice, short answer, calculation, 3-4 mark explain, 5-6 mark analyse/evaluate, essay (Biology) |
| iGCSE | Chemistry, Biology, Coordinated Science | Same as GCSE with slight rubric differences |

## Question types by subject

### Chemistry (both GCSE and A-level)
- Multiple choice (topic knowledge, recall)
- Short answer (definitions, equations, observations)
- Calculation (moles, concentrations, rates, enthalpy, pH)
- Balancing equations
- Drawing/describing (dot-and-cross diagrams, apparatus, mechanisms)
- Explain/justify (trends, observations, predictions)
- Practical/required practical (method, variables, conclusion)
- Essay (A-level only: organic mechanisms, transition metals, thermodynamics)

### Biology (both GCSE and A-level)
- Multiple choice (recall, data interpretation)
- Short answer (definitions, processes, structures)
- Data analysis (graphs, tables, statistical tests)
- Describe/explain (processes, adaptations, cycles)
- Practical (method, variables, controls, conclusion)
- Essay (A-level only: synoptic essays)
- Calculations (magnification, percentage change, Hardy-Weinberg, chi-squared)

## Process

### Step 1: Clarify requirements

Ask the user for:
- **Subject:** Chemistry, Biology, or Combined Science
- **Level:** GCSE / iGCSE / A-level
- **Exam board:** AQA / Edexcel / OCR / CIE (affects style and wording)
- **Topic(s):** specific topic(s) to cover
- **Question count:** how many questions (default: 8-10)
- **Duration:** suggested time (optional)
- **Student name:** if personalised (optional)
- **Format:** plain text / markdown / LaTeX (default: markdown)

If the user provides a syllabus specification point (e.g. "AQA 3.1.2 Amount of substance"), use it to target the questions precisely.

### Step 2: Generate the worksheet

Create questions that:
- Match the exam board style (command words: Describe, Explain, Calculate, Suggest, Evaluate, Compare)
- Progress from easy to hard
- Mix question types
- Cover the specification points
- Include data/context where realistic (tables, graphs, experimental results)
- For A-level Chemistry: include 6-mark quality of written communication questions

### Step 3: Generate the mark scheme

For each question, provide:
- Correct answer(s)
- Mark allocation
- Alternative acceptable answers
- Common mistakes (optional, helpful for the tutor)

### Step 4: Format output

Present the worksheet and mark scheme as separate sections.

For markdown output:
```
## Worksheet: [Title]

**Subject:** [Subject]
**Level:** [Level]
**Exam board:** [Board]
**Topics:** [Topics]
**Time:** [Duration]

---

### Question 1 (X marks)


---

### Question 2 (X marks)

...
```

```
---

## Mark Scheme

### Question 1 (X marks)
- Answer: ...
- Accept: ...
- Common errors: ...

### Question 2 (X marks)
...
```

### Step 5: Save to file (optional)

If the user wants the worksheet saved, create it in `~/tutoring-materials/worksheets/` with a clear filename:

```
~/tutoring-materials/worksheets/{subject}-{level}-{topic}-{date}.md
```

Also offer to convert to PDF if the user requests it (can be done via pandoc or similar).

## Tips for good questions

- **Command words matter.** Use the exact words from the exam board (Describe, Explain, Suggest, Evaluate, Calculate, Compare, Outline, State, Give)
- **Context is king.** Frame questions around a scenario (a reaction, an experiment, a data set). A-level Biology especially rewards context-rich data interpretation
- **Step-wise scaffolding.** Start with simple recall, build up to application, then evaluation
- **Include data.** Realistic tables, graphs, or experimental set-ups add exam authenticity
- **No trick questions.** Mark schemes should be fair and predictable
- **Leave working space.** For calculations, indicate where working should be shown

## Pitfalls

- **Don't use American spellings/terminology** (color/colorless, aluminum, math) -- use UK exam conventions
- **Don't exceed the typical paper difficulty** -- GCSE questions should not require A-level knowledge
- **Don't forget significant figures** in calculation questions (specify: give your answer to 2 decimal places / 3 significant figures)
- **Use the correct units** -- kJ mol^-1, cm^3, dm^3, etc.
- **Balanced equations must be balanced** -- double-check atom and charge conservation

## Verification

Before delivering, verify:
- All equations are balanced
- All answers are correct (do a mental run-through or calculation check)
- Mark scheme totals add up
- Question numbering is sequential
- Command words match the exam board style
- No spelling/grammar errors in UK English