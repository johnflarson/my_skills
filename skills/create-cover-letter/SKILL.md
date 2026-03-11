---
name: create-cover-letter
description: Generate a tailored cover letter from a job description URL or pasted text. Uses John Larson's resume, background, and a Word template (.dotx) to produce a professional .docx and .pdf cover letter. Trigger this skill whenever the user mentions cover letters, applying to a job, writing an application letter, or wants to create a cover letter for a specific company or role — even if they don't say "cover letter" explicitly (e.g., "I want to apply to this job at Google").
---

# Cover Letter Generator

Generate a professional, tailored cover letter from a job description. The skill reads a Word template (.dotx), fills in placeholders with content matched to the job, and outputs both .docx and .pdf files.

## Paths

- **Template:** `99 System/Agent/Claude/skills/create-cover-letter/references/coverletter-template.dotx`
- **Resume:** `99 System/Agent/Claude/skills/create-cover-letter/references/resume.pdf`
- **Examples:** `99 System/Agent/Claude/skills/create-cover-letter/references/coverletter-example1.pdf` through `coverletter-example5.pdf`
- **Fill script:** `99 System/Agent/Claude/skills/create-cover-letter/scripts/fill_template.py`
- **Output directory:** `99 System/Output/coverletters/`
- **Output filename pattern:** `coverletter-{company-name-lowercase}.docx` and `.pdf`

## Background Context

Read the resume PDF and at least 2 example cover letter PDFs before writing content. The examples show the voice, tone, structure, and level of detail expected. The candidate is:

- **John Larson** — Director of Technology with 20+ years in enterprise data and infrastructure
- **Specialties:** Data architecture, database administration, team leadership, M&A consolidation, healthcare IT
- **Key achievements:** $25M+ cost savings, 4000+ databases managed, 2000TB+ data migrations, 83% improvement in team deliverables
- **Current focus:** Expanding into AI integrations, agent-driven automation, LLM development
- **Contact:** 313-389-6875, john.larson@outlook.com, Ann Arbor, MI
- **LinkedIn:** https://www.linkedin.com/in/johnflarson/
- **Website:** https://www.luminaldata.com/

## Workflow

### Step 1: Get the Job Description

Accept either:
- A URL to a job posting (fetch and extract the job details)
- Pasted job description text

Extract from the job description:
- **Company name**
- **Job title**
- **Key requirements** (skills, experience, qualifications)
- **Company values/mission** (if mentioned)
- **Industry/domain**
- **Location requirements**

### Step 2: Read Reference Materials

Read the resume PDF and at least 2 example cover letters to understand:
- The writing voice and tone (professional but personable, first-person)
- The structure (opening paragraph, body paragraphs with specific metrics, closing)
- How achievements from the resume are woven into the narrative
- How company-specific language is incorporated

### Step 3: Generate Cover Letter Content

The template has these placeholders to fill. Each one is wrapped in `{{}}` in the Word template:

| Placeholder | What to Write |
|-------------|---------------|
| `DATE` | Today's date in M/D/YYYY format |
| `JOB TITLE` | The exact job title from the posting (appears twice in template) |
| `COMPANY NAME` | The company name |
| `QUALIFICATIONS` | Opening paragraph: state the role being applied for, summarize 20+ years of relevant experience, and highlight 2-3 key qualifications that make the candidate a strong fit. This is the hook — make it specific to the job. |
| `PARAGRAPH 1` | Body paragraph: Connect specific career achievements to the job requirements. Use concrete metrics ($25M savings, 600TB migration, 4000+ databases, etc.) that are relevant to what the role asks for. Mirror the job posting's language. |
| `PARAGRAPH 2` | Body paragraph: Show genuine interest in the company. Reference the company's mission, values, products, or recent initiatives. Explain why the candidate wants to work there specifically, not just any similar role. |
| `PARAGRAPH 3` | Closing paragraph: Summarize what the candidate brings to the company. Express enthusiasm for contributing. Thank the reader and express interest in discussing further. |

### Writing Guidelines

Based on the example cover letters, follow these patterns:

- **Length:** Each body paragraph should be 4-8 sentences. The full letter is typically one page.
- **Tone:** Professional, confident, not boastful. Use "I have" and "I am" rather than "I believe I could."
- **Specificity:** Every claim should reference a concrete achievement with numbers where possible.
- **Mirroring:** Use terminology from the job posting. If they say "data pipelines," use "data pipelines" not "ETL processes."
- **Company research:** If given a URL, research the company to write an authentic paragraph about why the candidate is drawn to them.
- **Avoid generic filler:** No "I am writing to express my interest" — jump straight into the value proposition.
- **Closing:** Always end with "Sincerely," followed by "John Larson" (the template handles this — just fill the content paragraphs).

### Step 4: Fill the Template and Save

Run the fill_template.py script to create the .docx:

```bash
python "99 System/Agent/Claude/skills/create-cover-letter/scripts/fill_template.py" \
  "99 System/Agent/Claude/skills/create-cover-letter/references/coverletter-template.dotx" \
  "99 System/Output/coverletters/coverletter-{company}.docx" \
  '{"DATE": "...", "JOB TITLE": "...", "COMPANY NAME": "...", "QUALIFICATIONS": "...", "PARAGRAPH 1": "...", "PARAGRAPH 2": "...", "PARAGRAPH 3": "..."}'
```

The JSON keys must match exactly: `DATE`, `JOB TITLE`, `COMPANY NAME`, `QUALIFICATIONS`, `PARAGRAPH 1`, `PARAGRAPH 2`, `PARAGRAPH 3`.

Use the full vault path (relative from the vault root) when running the script. The company name in the filename should be lowercase with hyphens replacing spaces (e.g., `coverletter-corewell-health.docx`).

### Step 5: Convert to PDF

```bash
python -c "from docx2pdf import convert; convert('99 System/Output/coverletters/coverletter-{company}.docx')"
```

This creates the PDF in the same directory. If docx2pdf fails (requires Word installed on Windows, or LibreOffice on Linux), try:

```bash
# Windows fallback using COM automation
python -c "
import comtypes.client
import os
word = comtypes.client.CreateObject('Word.Application')
doc = word.Documents.Open(os.path.abspath('99 System/Output/coverletters/coverletter-{company}.docx'))
doc.SaveAs(os.path.abspath('99 System/Output/coverletters/coverletter-{company}.pdf'), FileFormat=17)
doc.Close()
word.Quit()
"
```

### Step 6: Confirm to User

Tell the user:
- The .docx and .pdf files have been created
- Where they are saved
- A brief summary of how the cover letter was tailored to the role
- Offer to make adjustments if anything needs changing

## Important Notes

- The placeholder text in the template is split across multiple XML runs inside the .dotx file. The `fill_template.py` script handles this — do not try to use python-docx's paragraph replacement directly on the template.
- The `QUALIFICATIONS` placeholder replaces the full opening paragraph text including the qualification summary.
- `PARAGRAPH 1`, `PARAGRAPH 2`, and `PARAGRAPH 3` each replace an entire body paragraph.
- `JOB TITLE` appears twice in the template (opening and closing) — the script handles replacing both occurrences.
- Always use full absolute paths or vault-relative paths when calling the script.
