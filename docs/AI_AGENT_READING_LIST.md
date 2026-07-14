# AI agent reading list for textbook updates

This document provides a prioritized reading list for AI agents implementing the textbook
restructure.

## Essential files (read first)

### Plan and structure
- [TEXTBOOK_PAGE_SUMMARIES.md](../Textbook/TEXTBOOK_PAGE_SUMMARIES.md): Master plan showing
  what each page should contain and the three-sentence summaries with SEO tags.
- [TEXTBOOK_MIGRATION_GUIDE.md](TEXTBOOK_MIGRATION_GUIDE.md): Step-by-step
  implementation checklist covering renames, new files, and migration notes.

### Style guides
- [AGENTS.md](../AGENTS.md): Repo constraints, LibreTexts rules, linting requirements, and changelog
  expectations.
- [LIBRETEXTS_HTML_GUIDE.md](LIBRETEXTS_HTML_GUIDE.md): LibreTexts HTML whitelist, table
  format, and authoring rules.
- [REPO_STYLE.md](REPO_STYLE.md): Naming, file organization, docs conventions, and git
  safety rules.

## Source content files (by chapter)

### Chapter 2: OPL header (new section 2.2)
- `WEBWORK_HEADER_STYLE.md
  `: OPL header format, metadata fields, and copy-paste template.

### Chapter 2: macros (update section 2.5)
- `PG_2_17_RENDERER_MACROS.md
  `: Renderer macro allowlist for ADAPT/renderer.
- [PG_MACRO_VERSION_COMPARISON.md](PG_MACRO_VERSION_COMPARISON.md): Comparison table
  across PG versions and missing macros.

### Chapter 6: advanced PGML techniques (complete restructure)

6.1 Coloring text and emphasis:
- `COLOR_TEXT_IN_WEBWORK.md
  `: CSS styling guidance, `[$var]*` pattern, and TeX color caveats.

6.2 Tables with niceTables:
- `NICETABLES_TRANSLATION_PLAN.md
  `: DataTable and LayoutTable patterns with biology examples.

6.3 Matching problems (includes MODES):
- `MATCHING_PROBLEMS.md
  `: Matching patterns, PopUp usage, and MODES(HTML => ...) for wrapper divs.
- `yaml_match_to_pgml.py
  `: Read the first 200 lines for conversion patterns.
- **Fold in MODES explanation**: Teach that MODES is only required when wrapper HTML must be emitted
  from inside Perl eval blocks (e.g., divs wrapping join() expressions).

6.4 Multiple choice statements:
- `PGML_QUESTION_TYPES.md
  `: Multiple choice statement patterns.
- `yaml_mc_statements_to_pgml.py
  `: Read the first 200 lines for conversion patterns.

6.5 Advanced randomization:
- `RANDOMIZATION_REFERENCE.md
  `: Randomization rules and examples.
- `WEBWORK_PROBLEM_AUTHOR_GUIDE.md
  `: Read the randomization sections.

### Chapter 7: renderer API (new section 7.2)
- `RENDERER_API_USAGE.md
  `: API docs, POST / vs POST /render-api, and parameter precedence.
- `README.md
  `: Renderer overview, private/ workflow, and GET /health.

## Reference files

### PG/PGML authoring standards
- `WEBWORK_PROBLEM_AUTHOR_GUIDE.md
  `: Canonical file skeleton, PGML requirements, inline grading, and randomization rules.
- `PGML_QUESTION_TYPES.md
  `: Question type patterns and PGML-first examples.
- `PGML_LINTER_EXPECTATIONS.md
  `: Common PGML mismatches and failure modes.

### Existing textbook content (for context)
- [1.0-Index.html](../Textbook/01_Introduction/1.0-Index.html): Tone and
  structure reference.
- `3.1-Introduction_to_PGML.html
  `: PGML basics reference.
- `4.1-Full_file.html
  `: Worked example that needs the OPL header added.

## Changelog and history
- [CHANGELOG.md](CHANGELOG.md): Review the 2026-01-28 entry, then add a new entry after
  completing changes.

## Implementation priority order

### Phase 1: critical renames and structure
1. Read [TEXTBOOK_MIGRATION_GUIDE.md](TEXTBOOK_MIGRATION_GUIDE.md).
2. Rename Chapter 2 files (2.2 to 2.3, 2.3 to 2.4, 2.4 to 2.5, 2.5 to 2.6).
3. Rename Chapter 4 files (4.2 to 4.3, 4.3 to 4.4, 4.4 to 4.5, 4.5 to 4.6, 4.6 to 4.7).
4. Rename Chapter 7 files (7.2 to 7.3).
5. Rename the Chapter 6 directory per the migration guide.

### Phase 2: new content (high priority)
1. Create 2.2 OPL header section.
2. Create 4.2 OPL header section.
3. Update 4.1 full file to add the OPL header.

### Phase 3: Chapter 6 (advanced PGML)
1. Create 6.1 Coloring text and emphasis (show `[$var]*` and PGML tag wrappers).
2. Create 6.2 Tables with niceTables.
3. Create 6.3 Matching problems (fold in MODES explanation showing `MODES(HTML => ...)` only when wrapper HTML must be in eval blocks).
4. Create 6.4 Multiple choice statements.
5. Create 6.5 Advanced randomization patterns.

### Phase 4: Chapter 7 updates
1. Create 7.2 API usage for scripts.
2. Update 7.0 Index (add /health, PG 2.17 subset note).
3. Update 7.1 Quickstart and editor workflow (add private/ folder).

### Phase 5: appendices
1. Create 90.1 Minimal templates (with OPL headers).
2. Create 90.2 Glossary.
3. Create 90.3 Troubleshooting checklist.
4. Update 90.0 Index.

### Phase 6: updates to existing files
1. Update 2.0 Index (five-section acknowledgment).
2. Update 2.5 Common PG macros (add version comparison table).
3. Update 4.0 Index (five-section structure).
4. Update 6.0 Index (advanced techniques focus).
5. Update Chapter 1 sections with PG 2.17 subset notes.

## Quality checks before completion
- Each `X.0-Index.html` ends with `<p>{{template.ShowOrg()}}</p>`.
- No internal `<a href=...>` links in `Textbook/` HTML files.
- No `<script>` tags or inline JavaScript.
- Tables follow the LibreTexts format in
  [LIBRETEXTS_HTML_GUIDE.md](LIBRETEXTS_HTML_GUIDE.md).
- Run HTML lint: `/opt/homebrew/bin/bash tests/run_html_lint.sh`.
- Update [CHANGELOG.md](CHANGELOG.md) after completing work.

## Quick reference card

**When creating new HTML pages:**
- Follow the three-sentence structure from
  [TEXTBOOK_PAGE_SUMMARIES.md](../Textbook/TEXTBOOK_PAGE_SUMMARIES.md).
- Match tone and layout from existing textbook pages.
- Follow LibreTexts constraints in
  [LIBRETEXTS_HTML_GUIDE.md](LIBRETEXTS_HTML_GUIDE.md).
- Include biology-first examples where noted in the page summaries.
- Avoid internal `<a href=...>` links.
- Use LibreTexts-compatible tables only.

**When writing about MODES (folded into Chapter 6.3 Matching):**

When authoring Chapter 6.3 Matching, fold in the MODES explanation as part of building the two-column layout. Teach that `MODES(HTML => ...)` is only required when wrapper HTML tags must be emitted from inside Perl eval blocks (e.g., `[@ ... @]*`) because they wrap dynamically-generated content like `join()` expressions-**without MODES, the wrapper HTML gets escaped and the layout collapses**. If wrapper tags can be written directly in PGML outside the eval blocks, avoid MODES entirely and write them in PGML instead-this is the preferred approach. Always use `MODES(HTML => ...)` not `MODES(TeX => '', HTML => ...)` since we never care about TeX output. Show the matching problems pattern from `MATCHING_PROBLEMS.md` where MODES is necessary (wrapper divs must be inside eval blocks with the join expressions). For simple HTML variables in 6.1 Coloring, teach `[$var]*` instead of MODES.

**Specific guidance (based on real problems):**
- MODES is only for **flexbox wrapper HTML inside eval blocks** - not for all HTML injection.
- **MODES IS needed** for: flexbox layout wrappers (`<div class="two-column"><div>`) inside `[@ ... @]*` blocks that wrap join() expressions.
- **MODES is NOT needed** for: subscript/superscript HTML (`<sub>`, `<sup>`), charge labels, colored choices, canvas HTML, or any plain HTML that renders fine without MODES.
- If wrapper tags can be written directly in PGML, do that instead of using MODES.
- Use `MODES(HTML => ...)` not `MODES(TeX => '', HTML => ...)`.
- For simple HTML variables: use `[$var]*` instead of MODES (teach in 6.1 Coloring).
- Real example where MODES is needed: `[@ MODES(HTML => '<div class="two-column"><div>') @]*` for flexbox layout in matching (see `chemical_group_pka_forms.pgml`).
- Real examples where MODES is NOT needed: subscripts, charge labels, colored choices, canvas HTML (see `macromolecule_identification.pgml`).

**When working on OPL headers:**
- Use the template from
  `WEBWORK_HEADER_STYLE.md
  `.
- Include TITLE, DESCRIPTION, KEYWORDS, DBsubject, DBchapter, DBsection, Date, Author,
  Institution.
- Use biology-appropriate DBsubject classifications.

**When integrating biology examples:**
- Follow the migration notes in
  [TEXTBOOK_MIGRATION_GUIDE.md](TEXTBOOK_MIGRATION_GUIDE.md).
- Keep examples short (about 5 to 15 lines of PG code).
- Show the pattern, not a full problem.

**When in doubt:**
- Check [TEXTBOOK_PAGE_SUMMARIES.md](../Textbook/TEXTBOOK_PAGE_SUMMARIES.md) first.
- Check [TEXTBOOK_MIGRATION_GUIDE.md](TEXTBOOK_MIGRATION_GUIDE.md) second.
- Check the source content files third.
