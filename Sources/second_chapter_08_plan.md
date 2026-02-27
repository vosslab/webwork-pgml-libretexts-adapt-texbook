# Plan: Write Chapter 08 - Using AI Agents to Write WeBWorK

## Context

Chapter 08 of the ADAPT WeBWorK Handbook has five placeholder HTML files with stub text. The user has a video transcript (SRT files) from "Writing WeBWorK PG Problems with AI Agents" plus the webwork-writer skill documentation. The goal is to fill all five sections with substantive textbook content drawn from these sources, matching the existing style (science-first tone, short focused pages, `<h2>` headings, responsive tables, "Apply it today" closings).

## Source Material

- **Video transcript**: `Textbook/Writing_WeBWorK_PG_Problems_with_AI_Agents-yt-lfcJ3ALXEhk.en.srt` (primary), plus `.en-orig.srt` and `.en-en.srt` (all ~identical content)
- **Webwork-writer skill docs**: `~/.claude/skills/webwork-writer/references/` (renderer API, linting, authoring guide, pitfalls)

## Verified Page IDs for Cross-References

| Section | Title | Page ID |
|---------|-------|---------|
| 2.2 | OPL Header and Metadata | 557378 |
| 2.5 | Common PG Macros | 488659 |
| 6.1 | Text Coloring and Emphasis | 555723 |
| 6.2 | Making Tables with niceTables | 555724 |
| 6.4 | Advanced Randomization Techniques | 555727 |
| 6.5 | Randomized Matching Problems | 555725 |
| 7.1 | Simple Syntax Checking (Linting) | 557407 |
| 7.2 | Setting Up the PG Renderer | 555732 |
| 7.3 | Scripting and Automation | 557409 |
| 7.4 | Common Mistakes | 555733 |
| 7.5 | Testing Randomization | 557411 |
| 7.6 | QA Checklist | 557412 |
| 8.0 | Chapter 8 Index | 557413 |
| 8.1 | What are AI Agents? | 555730 |
| 8.2 | Knowledge Documents | 557415 |
| 8.3 | Connecting to PG Renderer | 557416 |
| 8.4 | Advance AI Agents Advice | 557417 |
| Ch 2 | Problem Generation (PG) | 488655 |
| Ch 3 | PGML | 488660 |

## Files to Edit

All under `Textbook/08_Using_AI_Agents_to_Write_WeBWorK/`:

### 1. `8.0-Index.html` (~100 lines, ~2.5 KB)

**Intro** (no heading): Two paragraphs framing the chapter - AI agents can write WeBWorK PG code so you focus on subject expertise, not Perl syntax. Lab analogy: directing a trained lab tech (describe the experiment, provide protocols, check results).

**`<h2>` What is your goal today?** - Decision table (`mt-responsive-table`, 3 cols: "What you want to do" / "Go to" / "What you will find") routing readers to 8.1-8.4 based on need.

**`<h2>` Section map** - Two-column summary table of all four content sections.

**`<h2>` Start here** - Bulleted list: 3 paths by experience level (never used agents -> 8.1; agent writes broken code -> 8.2; complex problems -> 8.4).

**`<h2>` Prerequisites** - Bullets: running renderer (link 7.2), basic WeBWorK structure (link Ch 2), an AI agent installed.

**`<h2>` Apply it today** - Two bullets: use decision table; try writing one simple problem.

**Closing**: `{{template.ShowOrg()}}`

---

### 2. `8.1-What_are_AI_Agents.html` (~130 lines, ~3.5 KB)

**Intro**: Define AI agents for science educators. An agent reads files, runs commands, connects to tools, revises its own work - unlike a chatbot. Since late 2025, agents transformed code writing: "vibe coding."

**`<h2>` Chatbots versus agents** - Comparison table (3 cols: Capability / Chatbot / Agent) covering: reads files, runs commands, connects to renderer, revises on error, accesses docs, tests output. Follow-up paragraph: the ability to self-test is what makes agents practical.

**`<h2>` Why chatbots fail at WeBWorK** - From transcript: PG looks like Perl but is not. ChatGPT confuses them (wrong `my`, `use`, I/O). The debugging trap: without a renderer, chatbot convinces you YOUR tools are broken. Recommendation: do not debug chatbot WeBWorK output without a renderer. Link to 7.2, 7.4.

**`<h2>` What makes agents work for WeBWorK** - Bulleted list of 4 capabilities: documentation access, renderer connection, self-correction loop, file management.

**`<h2>` Available agents** - Table (3 cols: Agent / Provider / Notes) listing Claude Code and Codex. Brief paragraph: both follow the same workflow; terminology differs (skills vs forums).

**`<h2>` What you need before starting** - Ordered list: renderer on localhost:3000 (link 7.2), agent installed, knowledge docs (link 8.2), problem description.

**`<h2>` Apply it today** - Install an agent; verify renderer health check.

---

### 3. `8.2-Knowledge_Documents_for_AI_Agents.html` (~140 lines, ~3.5 KB)

**Intro**: Why documentation is essential - without it, agents fall back on Perl training data and make the same errors as chatbots. The solution: a curated doc set ("skill" in Claude Code, "forum" in Codex). From transcript: "all the documents it needs is in the skill."

**`<h2>` Skills and forums: same idea, different names** - Short paragraph + 2-col table (Agent / Documentation mechanism).

**`<h2>` Why agents need WeBWorK-specific documents** - Bulleted list of PG-vs-Perl traps: sandbox traps (`use`, `require`, `open`), `my` keyword, backslash refs, single-pass PGML, blocked HTML tags, TeX color macros, PG 2.17 subset. Link to 7.4, 2.5.

**`<h2>` What to include in your knowledge documents** - Priority table (3 cols: Topic / Why the agent needs it / Textbook reference) covering ~10 topics: PG author guide, common mistakes, macro allowlist, renderer API, color guide, randomization, niceTables, matching patterns, lint tools, OPL header. Each with links to relevant sections.

**`<h2>` How to organize your documents** - 3 paragraphs: single location, explicit "use only provided docs" instruction (agents "obsessed with finding other files"), start minimal and add as needed.

**`<h2>` A minimal document set for your first problem** - Ordered list of 4 essentials: PGML authoring guide, common mistakes reference, macro allowlist, renderer API docs.

**`<h2>` Apply it today** - Assemble minimal 4-doc set; test with simplest possible question ("favorite color" multiple choice).

---

### 4. `8.3-Connecting_AI_Agents_to_the_PG_Renderer.html` (~130 lines, ~3.5 KB)

**Intro**: The renderer connection separates productive agent workflow from chatbot copy-paste frustration. Lab analogy: the renderer is the agent's bench assay - never trust code that was never rendered.

**`<h2>` Prerequisites** - Bullets: renderer running (link 7.2), health check confirmed, renderer API docs in knowledge docs (link 8.2), agent has terminal command permission.

**`<h2>` How the agent uses the renderer** - Two paragraphs describing the technical workflow, then a numbered step list (the feedback loop): write .pg -> POST to renderer -> check error_flag + pg_warn -> if errors, consult docs and revise -> repeat until clean.

**`<h2>` What to tell the agent about the renderer** - Bulleted instructions: URL, `_format=json`, check error_flag + pg_warn, fixed problemSeed for dev, test 3+ seeds after clean, lint script with `-r` flag.

**`<h2>` Typical timing** - From transcript: simple problems 3-5 min; complex multi-part problems 15-20+ min. Specific example from video (amino acid pI question). This is normal.

**`<h2>` When the agent gets stuck** - From transcript: tell it to re-read docs; point to specific sections; approve renderer permission requests. Link to 7.4.

**`<h2>` Apply it today** - Confirm agent can reach renderer (health check); ask agent to write + render a simple problem.

---

### 5. `8.4-Advance_AI_Agents_Advice.html` (~160 lines, ~4 KB)

**Intro**: Once agent has renderer + docs, quality depends on communication. Covers prompt writing, boundaries, patience, iteration, accessibility. Video demonstrates these through an amino acid pI worked example.

**`<h2>` Set boundaries before starting** - From transcript: start with empty/clean project; tell agent not to search filesystem; keep working directory simple.

**`<h2>` Write detailed prompts** - Table (2 cols: Prompt element / Example) covering: topic, learning objective, number of parts, interaction types, randomization requirements, visual description, constraints.

**`<h2>` Be patient** - From transcript: complex problems take 15-20+ min; agents may ask clarifying questions (good behavior); let the render-fix loop complete.

**`<h2>` Refine iteratively** - Three passes: first pass (basic working question), second pass (presentation - color, layout), third pass (accessibility, polish). Each from transcript examples.

**`<h2>` Accessibility and color** - CSS-based styling (not TeX). Bulleted rules: avoid red-green, use high-contrast pairs, gray for neutral items, pair color with another cue. Link to 6.1.

**`<h2>` Worked example: amino acid isoelectric point** - Narrative walkthrough from transcript: problem description (two-part pI question), the prompt, the process (15 min, agent asks questions, renders, debugs), refinement (color, accessibility), result (randomized pKa values, color-coded groups). Not full PG code - a narrative case study.

**`<h2>` Common pitfalls** - Table (3 cols: Pitfall / What happens / Prevention) covering: no knowledge docs, agent searches filesystem, skipping renderer, ignoring docs after first read, impatient intervention, no seed testing.

**`<h2>` Apply it today** - Write a detailed prompt for one question; let agent work the full cycle; test with 5+ seeds.

---

## Style Rules (from existing chapters)

- HTML only, no JavaScript, no `<script>` tags
- `<h2>` for sections, `<h3>` for subsections (use sparingly)
- Tables: `<table class="mt-responsive-table">` with `<colgroup>`, `data-th` attributes on `<td>`
- Code inline: `<code>` tags; code blocks: `<pre>` tags
- Lists: `<ul>` with `<li>`
- Internal links: `<a href="/@go/page/PAGEID">Section X.Y</a>`
- Only index page gets `{{template.ShowOrg()}}`
- "Apply it today" closing section on every page
- No `<h1>` tags (LibreTexts provides page title)
- Short focused pages, science-first tone, practical and task-oriented

## Verification

1. Run `tests/run_html_lint.sh` on all 5 edited files
2. Visual review: each file should be ~100-160 lines, match surrounding chapter style
3. Cross-references: verify all `/@go/page/` links use correct page IDs from the table above
4. No JavaScript, no relative file links, no `<h1>` tags
5. Update `docs/CHANGELOG.md` with the changes
