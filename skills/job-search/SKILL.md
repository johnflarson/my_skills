---
name: job-search
description: Search for job opportunities and manage the job tracker. Use this skill whenever the user wants to find jobs, search for open positions, add a job to their tracker, update job application status, review their job pipeline, or anything related to job hunting and career opportunities. Triggers on phrases like "find jobs", "search for roles", "add this job", "update job status", "show my job tracker", "what jobs are open", "look for positions", or even casual mentions like "I saw a posting at Google" or "check LinkedIn for data jobs".
---

# Job Search & Tracker

Search for job opportunities matching the user's background and manage a persistent job tracker in the Obsidian vault.

## Reference Materials

- **Resume:** `99 System/Agent/Claude/skills/create-cover-letter/references/resume.pdf`
- **Job Tracker:** `30 Projects/job search/job tracker.md`

## Candidate Profile

- **John Larson** — Director of Technology with 20+ years in enterprise data and infrastructure
- **Specialties:** Data architecture, database administration, team leadership, M&A consolidation, healthcare IT
- **Key achievements:** $25M+ cost savings, 4000+ databases managed, 2000TB+ data migrations
- **Current focus:** AI integrations, agent-driven automation, LLM development
- **LinkedIn:** https://www.linkedin.com/in/johnflarson/
- **Website:** https://www.luminaldata.com/
- **Location:** Ann Arbor, MI

Use this profile to assess job fit and tailor search queries. The user is targeting senior/director-level roles in data, infrastructure, AI/ML, or technology leadership.

## Job Tracker Schema

The tracker lives at `30 Projects/job search/job tracker.md` as a Markdown table with these columns:

| Column | Description | Values |
|--------|-------------|--------|
| ID | Auto-incremented integer (1, 2, 3...) | Next available number |
| Company | Company name | Free text |
| Role | Job title | Free text |
| Location | Work arrangement and/or geography | Remote, Hybrid, On-site, and/or City, State |
| Salary | Compensation if known | Range or "—" if unknown |
| Link | URL to the job posting | Full URL or "—" |
| Added | Date the row was created | YYYY-MM-DD |
| Status | Current status of this opportunity | Active, Pass, Expired, Rejected |
| Applied | Date the application was submitted | YYYY-MM-DD or "—" if not yet applied |

## Workflow

### Searching for Jobs

When the user asks to find or search for jobs:

1. Read the resume PDF to understand the full background and qualifications.
2. Use WebSearch to find relevant open positions. Build search queries from:
   - The user's specialties and target roles (data architecture, director of technology, VP of data, etc.)
   - Any specific companies, industries, or locations the user mentions
   - Job boards: LinkedIn, Indeed, Glassdoor, company career pages
3. For each promising result, use WebFetch to get the full job posting details.
4. Present findings to the user in a summary format:
   - Company and role
   - Location and salary (if listed)
   - Why it's a good fit based on their background
   - Link to the posting
5. Ask the user which jobs they want to add to the tracker.

### Adding Jobs to the Tracker

When adding jobs (from search results or a URL/description the user provides):

1. Read the current tracker file to determine the next ID number.
2. If the user provides a URL, fetch the posting to extract company, role, location, and salary details.
3. Append a new row to the Markdown table with:
   - **ID:** Next sequential number
   - **Added:** Today's date (YYYY-MM-DD)
   - **Status:** Active (default)
   - **Applied:** — (default, unless user says they already applied)
4. Confirm what was added.

### Updating Job Status

When the user wants to update a job's status or mark it as applied:

1. Read the current tracker file.
2. Find the job by ID, company name, or role (ask if ambiguous).
3. Update the relevant field(s):
   - Status changes: Active → Pass, Expired, or Rejected
   - Applied: Set the date when the user submits an application
4. Write the updated table back.

### Reviewing the Tracker

When the user wants to see their pipeline:

1. Read the tracker file.
2. Present a summary: total jobs tracked, active count, applied count, pass/rejected/expired counts.
3. If requested, filter or sort by status, date, company, etc.

## Important Notes

- Always read the tracker file before modifying it to get the current state and next ID.
- Preserve existing rows exactly — only append or edit the specific row being changed.
- When searching, prioritize roles that match the user's seniority level (Director, VP, Senior Manager) and domain expertise (data, infrastructure, AI/ML).
- If a job posting URL is dead or inaccessible, note it and set the status to Expired.
- The tracker is a simple Markdown table for Obsidian compatibility — no complex formatting.
