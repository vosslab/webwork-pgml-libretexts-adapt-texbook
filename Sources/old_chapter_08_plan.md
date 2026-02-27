# Plan: Write Chapter 08 - Using AI Agents to Write WeBWorK

## Context

Chapter 8 of the ADAPT WeBWorK Handbook has 5 stub HTML files (8.0-8.4) with placeholder text only. The content source is the video transcript `Writing_WeBWorK_PG_Problems_with_AI_Agents-yt-lfcJ3ALXEhk.en-orig.srt` (best quality of the three SRT files) combined with the webwork-writer skill reference docs. The audience is biology/science instructors who are not programmers.

## Files to modify

1. `Textbook/08_Using_AI_Agents_to_Write_WeBWorK/8.0-Index.html` - chapter index
2. `Textbook/08_Using_AI_Agents_to_Write_WeBWorK/8.1-What_are_AI_Agents.html` - foundations
3. `Textbook/08_Using_AI_Agents_to_Write_WeBWorK/8.2-Knowledge_Documents_for_AI_Agents.html` - knowledge docs
4. `Textbook/08_Using_AI_Agents_to_Write_WeBWorK/8.3-Connecting_AI_Agents_to_the_PG_Renderer.html` - renderer integration
5. `Textbook/08_Using_AI_Agents_to_Write_WeBWorK/8.4-Advance_AI_Agents_Advice.html` - advanced advice
6. `docs/CHANGELOG.md` - record changes

## Style reference

Follow existing chapter patterns (Ch 5, Ch 7):
- Clean semantic HTML: `<p>`, `<h2>`, `<ul>/<li>`, `<table class="mt-responsive-table">`, `<code>`, `<pre>`
- Short practical paragraphs, task-first, biology examples
- Index pages: intro, decision table, section map, "Start here" guide, `{{template.ShowOrg()}}}`
- Section pages: intro, content with `<h2>` headings, tables, examples, "Apply it today" at end
- No JavaScript, no relative file links, no `<h1>` tags
- Internal Chapter 8 cross-refs use plain text ("Section 8.1") since LibreTexts page IDs are unknown
- Cross-refs to existing chapters use `<a href="/@go/page/###">` with known page IDs

## Section content outline

### 8.0-Index.html (~60 lines)
- Intro: Frame the chapter - AI agents write WeBWorK code so you don't have to; you provide biology expertise
- Lab analogy: like delegating to a trained technician
- Decision table: "What is your goal today?" -> maps to sections 8.1-8.4
- Section map table (standard two-column)
- "Start here" bullet guide based on experience level
- `{{template.ShowOrg()}}`

### 8.1-What_are_AI_Agents.html (~120 lines)
From video: motivation, "vibe coding," why ChatGPT fails, favorite-color demo failure
- Define AI agents for non-programmers
- Chatbots vs agents comparison table (reads files? runs code? connects to tools? revises on errors?)
- Why ChatGPT fails at WeBWorK: PG-looks-like-Perl confusion, back-and-forth debugging trap
- What makes agents different: documentation access, renderer connection, self-correction
- Available agents table: Claude Code, Codex - both tested, both work
- Prerequisites list (agent, renderer from Ch 7, knowledge docs, problem description)
- "Apply it today"

### 8.2-Knowledge_Documents_for_AI_Agents.html (~130 lines)
From video: webwork_writer skill/forum, comprehensive docs, prevent filesystem searching
- Why agents need WeBWorK-specific docs (PG is not generic Perl)
- Skills vs forums: two names for the same idea (Claude Code = skills, Codex = forums)
- What to include - table of ~10 document topics ranked by importance (PG author guide, PGML types, macro allowlist, color guide, pitfalls, randomization, matching, renderer API, niceTables, OPL headers)
- How to organize documents for your agent
- Minimal document set for first problem (4 docs)
- "Apply it today"

### 8.3-Connecting_AI_Agents_to_the_PG_Renderer.html (~120 lines)
From video: localhost:3000 sandbox, debug mode, agent sends to renderer, iterative testing
- Why the renderer connection matters (agent self-tests vs you copy-pasting errors)
- Prerequisites: renderer running, health check, API docs in knowledge set
- How agents use the renderer: POST source to API, check error_flag, read pg_warn, inspect renderedHTML
- The agent feedback loop (numbered steps: write -> render -> check -> fix -> repeat)
- Typical timing: 3-8 iterations, 11-15 minutes for complex problems
- What to tell the agent about the renderer (explicit instructions to include)
- Debugging when agent gets stuck (re-read docs, point to macro list, approve renderer access)
- "Apply it today"

### 8.4-Advance_AI_Agents_Advice.html (~140 lines)
From video: filesystem boundaries, patience, visual mockups, color/accessibility refinement, worked example
- Set boundaries: prevent filesystem searching, start with empty project
- Write detailed prompts - table of prompt elements (topic, parts, interaction types, randomization, mockup, constraints)
- Be patient: 11-15 min is normal, agent asks questions (good), approve renderer access
- Iterative refinement: color, accessibility (colorblind-safe), randomization testing
- Worked example: amino acid isoelectric point problem (case study from video - two parts, charges, pI, visual mockup, 11-min agent session, color refinement)
- Common pitfalls table (deprecated patterns, ignoring docs, filesystem searching, untested code, too many questions, variable results)
- Scaling: template prompts, batch processing, quality checks
- "Apply it today"

## Implementation order

1. Write 8.0-Index.html
2. Write 8.1 through 8.4 (can be parallelized)
3. Run HTML lint: `tests/run_html_lint.sh`
4. Update `docs/CHANGELOG.md`

## Verification

- Run `tests/run_html_lint.sh` on all 5 new files
- Visually check that HTML structure matches existing chapter patterns
- Confirm no JavaScript, no relative file links, no `<h1>` tags
- Confirm `{{template.ShowOrg()}}` only on index page
