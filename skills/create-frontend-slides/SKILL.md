---
name: create-frontend-slides
description: Create stunning, animation-rich HTML presentations from scratch or by converting PowerPoint files. Use when the user wants to build a presentation, convert a PPT/PPTX to web, or create slides for a talk/pitch. Helps non-designers discover their aesthetic through visual exploration rather than abstract choices. Triggers on "create slides", "make a presentation", "convert my pptx", "slide deck", "frontend slides".
---
# Create Frontend Slides Skill

Create zero-dependency, animation-rich HTML presentations that run entirely in the browser. Helps non-designers discover their preferred aesthetic through visual exploration ("show, don't tell").

## Core Philosophy

1. **Zero Dependencies** — Single HTML files with inline CSS/JS. No npm, no build tools.
2. **Show, Don't Tell** — Generate visual previews, not abstract choices.
3. **Distinctive Design** — Avoid generic "AI slop" aesthetics. Every presentation should feel custom-crafted.
4. **Production Quality** — Well-commented, accessible, performant code.
5. **Viewport Fitting (CRITICAL)** — Every slide MUST fit exactly within the viewport. No scrolling within slides, ever.

---

## CRITICAL: Viewport Fitting Requirements

**Every slide MUST fit exactly in the viewport. No scrolling within slides, ever.**

### Content Density Limits

| Slide Type | Maximum Content |
|------------|-----------------|
| Title slide | 1 heading + 1 subtitle + optional tagline |
| Content slide | 1 heading + 4-6 bullet points OR 1 heading + 2 paragraphs |
| Feature grid | 1 heading + 6 cards maximum (2x3 or 3x2 grid) |
| Code slide | 1 heading + 8-10 lines of code maximum |
| Quote slide | 1 quote (max 3 lines) + attribution |
| Image slide | 1 heading + 1 image (max 60vh height) |

**If content exceeds these limits, split into multiple slides.**

### Required Base CSS

Include in ALL presentations. See `references/style-presets.md` for the full mandatory CSS block. Key rules:

- Every `.slide`: `height: 100vh; height: 100dvh; overflow: hidden;`
- All font sizes: `clamp(min, preferred, max)`
- All spacing: `clamp()` or viewport units
- Content containers: `max-height` constraints
- Images: `max-height: min(50vh, 400px)`
- Grids: `auto-fit` with `minmax()`
- Breakpoints for heights: 700px, 600px, 500px
- Reduced motion: `@media (prefers-reduced-motion: reduce)`

### When Content Doesn't Fit

**DO:** Split into multiple slides, reduce bullets (max 5-6), shorten text, create "continued" slides.
**DON'T:** Reduce font below readable limits, remove padding, allow scrolling, cram content.

---

## Phase 0: Detect Mode

**Mode A: New Presentation** — Proceed to Phase 1.
**Mode B: PPT Conversion** — Proceed to Phase 4.
**Mode C: Enhancement** — Read existing file, understand structure, enhance.

---

## Phase 1: Content Discovery (New Presentations)

Ask via AskUserQuestion:

**Question 1 — Purpose** (Header: "Purpose"):
- "Pitch deck" — Selling an idea/product/company
- "Teaching/Tutorial" — Educational content
- "Conference talk" — Event speaking
- "Internal presentation" — Team updates

**Question 2 — Length** (Header: "Length"):
- "Short (5-10)" — Quick pitch, lightning talk
- "Medium (10-20)" — Standard presentation
- "Long (20+)" — Deep dive

**Question 3 — Content** (Header: "Content"):
- "I have all content ready" — Just design
- "I have rough notes" — Help organizing
- "I have a topic only" — Full outline needed

If user has content, ask them to share it.

---

## Phase 2: Style Discovery

### Available Presets (12 styles)

| Preset | Vibe | Best For |
|--------|------|----------|
| Bold Signal | Confident, high-impact | Pitch decks, keynotes |
| Electric Studio | Clean, professional | Agency presentations |
| Creative Voltage | Energetic, retro-modern | Creative pitches |
| Dark Botanical | Elegant, sophisticated | Premium brands |
| Notebook Tabs | Editorial, organized | Reports, reviews |
| Pastel Geometry | Friendly, approachable | Product overviews |
| Split Pastel | Playful, modern | Creative agencies |
| Vintage Editorial | Witty, personality-driven | Personal brands |
| Neon Cyber | Futuristic, techy | Tech startups |
| Terminal Green | Developer-focused | Dev tools, APIs |
| Swiss Modern | Minimal, precise | Corporate, data |
| Paper & Ink | Literary, thoughtful | Storytelling |

**For full preset details (colors, fonts, signature elements), read `references/style-presets.md`.**

### Step 2.0: Style Path Selection

Ask: "How would you like to choose your presentation style?"
- "Show me options" — Generate 3 previews based on mood (recommended)
- "I know what I want" — Pick from preset list directly

**If "I know what I want"** — Show preset picker, skip to Phase 3.

### Step 2.1: Mood Selection (Guided Discovery)

Ask (multiSelect: true, up to 2): "What feeling should the audience have?"
- "Impressed/Confident" — Professional, trustworthy
- "Excited/Energized" — Innovative, bold
- "Calm/Focused" — Clear, thoughtful
- "Inspired/Moved" — Emotional, memorable

### Mood → Preset Mapping

| Mood | Preset Options |
|------|---------------|
| Impressed/Confident | Bold Signal, Electric Studio, Dark Botanical |
| Excited/Energized | Creative Voltage, Neon Cyber, Split Pastel |
| Calm/Focused | Notebook Tabs, Paper & Ink, Swiss Modern |
| Inspired/Moved | Dark Botanical, Vintage Editorial, Pastel Geometry |

### Step 2.2: Generate 3 Style Previews

Read `references/style-presets.md` for the chosen presets' full specs. Generate 3 mini HTML files in `.claude-design/slide-previews/`:

```
.claude-design/slide-previews/
├── style-a.html
├── style-b.html
└── style-c.html
```

Each preview: self-contained, single title slide, ~50-100 lines, animated.

Present to user and open with `open` command. Ask which they prefer via AskUserQuestion.

### Pre-built Previews

All 12 style previews are available in `references/previews/`. Open any file to see the style in action:
- `references/previews/01-bold-signal.html` through `12-paper-and-ink.html`

These can be shown to the user during style discovery for instant visual browsing, or used as reference when generating custom previews.

---

## Phase 3: Generate Presentation

Read `references/style-presets.md` for the chosen preset's full spec (colors, fonts, signature elements).

### HTML Architecture

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Presentation Title</title>
    <!-- Fonts (Fontshare or Google Fonts) -->
    <style>
        /* CSS Custom Properties (theme) with clamp() values */
        /* Base styles with viewport fitting */
        /* Slide container: height: 100vh; overflow: hidden; */
        /* Responsive breakpoints (height-based) */
        /* Animations triggered via .visible class */
    </style>
</head>
<body>
    <!-- Optional: progress bar, nav dots -->
    <section class="slide title-slide">
        <h1 class="reveal">Title</h1>
    </section>
    <!-- More slides... -->
    <script>
        /* SlidePresentation class: keyboard, touch, wheel, progress, nav dots */
        /* Intersection Observer for scroll-triggered animations */
    </script>
</body>
</html>
```

### Required JavaScript Features

1. **SlidePresentation Class** — Keyboard (arrows, space), touch/swipe, wheel, progress bar, nav dots
2. **Intersection Observer** — Add `.visible` class on scroll for CSS animations
3. **Optional enhancements** (per style): custom cursor, particles, parallax, 3D tilt, magnetic buttons, counter animations

### Code Quality

- Section comments explaining what/why/how
- Semantic HTML (`<section>`, `<nav>`, `<main>`)
- ARIA labels, keyboard nav, reduced motion support
- **Never negate CSS functions directly** — `-clamp()`, `-min()`, `-max()` are silently ignored by browsers. Always use `calc(-1 * clamp(...))`. See `references/style-presets.md` → "CSS Gotchas" for details.

### Anti-AI-Slop Rules

**NEVER use:** Inter, Roboto, Arial as display fonts; `#6366f1` generic indigo; purple gradients on white; identical card grids; realistic illustrations; gratuitous glassmorphism.

**INSTEAD use:** Distinctive font pairings (Clash Display, Satoshi, Cormorant, etc.); cohesive color themes with personality; atmospheric backgrounds; signature animation moments.

---

## Phase 4: PPT Conversion

### Step 4.1: Extract with Python

Use `python-pptx` to extract text, images, notes. Save images to `assets/`.

### Step 4.2: Confirm extracted content with user.

### Step 4.3: Proceed to Phase 2 for style selection.

### Step 4.4: Generate HTML preserving all content, images, slide order, notes.

---

## Phase 5: Delivery

1. Delete `.claude-design/slide-previews/` if it exists
2. Open presentation with `open [filename].html`
3. Provide summary with file location, style name, slide count, navigation instructions, and customization tips (`:root` variables, font links, `.reveal` timings)

---

## Style Reference: Effect → Feeling

| Feeling | Effects |
|---------|---------|
| Dramatic/Cinematic | Slow fades (1-1.5s), scale transitions, dark + spotlight, parallax |
| Techy/Futuristic | Neon glow, particles, grid patterns, monospace accents, glitch effects |
| Playful/Friendly | Bouncy easing, large radius, pastels, floating animations |
| Professional/Corporate | Fast subtle animations (200-300ms), clean sans-serif, navy/slate, data-viz |
| Calm/Minimal | Very slow motion, high whitespace, muted palette, serif, generous padding |
| Editorial/Magazine | Strong type hierarchy, pull quotes, grid-breaking layouts, one accent color |