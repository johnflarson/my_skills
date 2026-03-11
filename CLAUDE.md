# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

A personal collection of Claude Code skills, plugins, and commands. Licensed under Apache 2.0.

## Repository Structure

- `skills/` — Claude Code skills, each in its own subdirectory
- `plugins/` — Claude Code plugins

## Skill Anatomy

Each skill is a directory under `skills/` containing:

- `SKILL.md` (required) — YAML frontmatter with `name` and `description`, followed by the skill prompt in markdown
- `references/` (optional) — Supporting files: templates, examples, PDFs
- `scripts/` (optional) — Helper scripts the skill invokes

### SKILL.md Frontmatter Format

```yaml
---
name: skill-name
description: One-line description used for trigger matching
---
```

## Current Skills

Sourced from two locations (being consolidated here):
- **Obsidian vault** (`F:\cloud\obsidian\personal\99 system\Agent\Claude\skills`): apply-job-career, create-cover-letter, create-daily-journal, create-frontend-slides, create-okr, create-weekly-review, extract-content, job-search
- **User .claude dir** (`~/.claude/skills`): notebooklm

## Installed Plugins (user-scoped)

- Notion (official)
- skill-creator (official)
- playwright-skill
