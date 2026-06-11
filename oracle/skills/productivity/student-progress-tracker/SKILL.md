---
name: student-progress-tracker
description: "Track student progress: lessons, topics, homework, and weak areas"
version: 1.0
author: Oracle
tags: [teaching, students, progress, tracking, tutoring]
---

# Student Progress Tracker

Maintain a lightweight record of tutoring students, lesson history, topics covered, homework, and areas for improvement.

## When to use

Load this skill when the user asks to:
- Record what was covered in a lesson
- Check a student's progress or history
- Plan the next lesson based on weak areas
- Generate a progress report for a parent
- List all students and their current topics
- Add a new student to the tracker

## Data storage

Student data is stored as JSON files in `~/tutoring-materials/students/`:

```
~/tutoring-materials/students/
  students.json           # Master list of all students
  Holly.json              # Individual student files
  Harry.json
  ...
```

### students.json structure

```json
{
  "students": [
    {
      "id": "holly",
      "name": "Holly",
      "subject": "A-level Chemistry",
      "board": "AQA",
      "contact": "parent email/phone",
      "rate": 45,
      "started": "2024-09-01",
      "current_topics": ["Amount of substance", "Bonding"],
      "weak_areas": ["Mole calculations"],
      "completed_lessons": 15
    }
  ]
}
```

### Individual student file structure

```json
{
  "name": "Holly",
  "subject": "A-level Chemistry",
  "board": "AQA",
  "rate": 45,
  "contact": "",
  "started": "2024-09-01",
  "lessons": [
    {
      "date": "2025-06-03",
      "topics_covered": ["Atomic structure", "Mass spectrometry"],
      "homework_set": "Past paper questions on mass spec",
      "homework_completed": true,
      "weaknesses_noted": ["Interpreting fragmentation patterns"],
      "strengths": ["Electron configuration"],
      "next_steps": "Review fragmentation, move to ionisation energy"
    }
  ],
  "progress_summary": {
    "total_lessons": 15,
    "topics_completed": ["Atomic structure", "Amount of substance", "Bonding"],
    "topics_in_progress": ["Energetics"],
    "persistent_weaknesses": ["Mole calculations"],
    "strengths": ["Organic mechanisms", "Electron configuration"]
  }
}
```

## Process

### Add a new student

Ask for:
- Name
- Subject and level
- Exam board
- Hourly rate (if known)
- Contact (parent email/phone, optional)
- Starting topic

Write the student files and add to students.json.

### Log a lesson

Ask for:
- Student name
- Date (default: today)
- Topics covered
- Homework set (optional)
- Homework completed (yes/no/pending)
- Weaknesses noted
- Strengths shown
- Next steps

Update the student's JSON file and recalculate progress_summary.

### Generate a progress report

Ask for:
- Student name
- Date range (optional, default: all)

Output a formatted summary with:
- Total lessons and cumulative hours
- Topics completed
- Current topics
- Persistent weak areas
- Improvement over time
- Homework completion rate
- Recommended focus areas

### List all students

Read students.json and display:
```
Holly        A-level Chemistry     AQA    15 lessons    [Mole calculations]
Harry        GCSE Chemistry         AQA     8 lessons    [Balancing equations]
Finley      GCSE Biology           Edexcel 6 lessons    [Mitosis vs meiosis]
Rohan       A-level Biology        CIE     3 lessons    [Cell structure]
```

### Plan next lesson

Given a student name, read their file and suggest:
- What to revise from last time
- Next topic(s) based on syllabus order
- Specific areas to drill (weaknesses)
- Number and type of practice questions to prepare
- Any pending homework to review

## Pitfalls

- **Use consistent student IDs** (lowercase, no spaces -- derived from name)
- **Back up students.json** before bulk edits
- **Don't store sensitive data** -- no full addresses, no bank details
- **Don't overwrite** -- always append new lesson entries, never edit old ones (add corrections as new entries)
- **Keep contact info minimal** -- just enough to identify the parent/student

## Verification

After any update:
- Read back the file to confirm valid JSON
- Check that student IDs match across students.json and individual files
- Confirm lesson entries are chronological (newest appended)