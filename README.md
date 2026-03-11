# my_skills

A collection of Claude Code skills, plugins, and commands.

## Structure

```
skills/          # Claude Code skills (each in its own directory)
  <skill-name>/
    SKILL.md     # Skill definition (frontmatter + prompt)
    references/  # Optional: reference files (PDFs, templates, examples)
    scripts/     # Optional: helper scripts used by the skill
plugins/         # Claude Code plugins
```

## Skills

Skills are user-scoped Claude Code extensions. Each skill lives in its own directory under `skills/` and must contain a `SKILL.md` with YAML frontmatter (`name`, `description`) followed by the skill prompt.

To install a skill, copy or symlink its directory into `~/.claude/skills/`.

## License

Apache 2.0
