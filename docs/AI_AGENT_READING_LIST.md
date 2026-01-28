# AI Agent Reading List for Textbook Updates

This document provides a prioritized reading list for AI agents working on implementing the textbook restructure.

## Essential Files (Read These First)

### 1. Plan and Structure
**File**: `Textbook/TEXTBOOK_PAGE_SUMMARIES.md`
- **Purpose**: Master plan showing what each page should contain
- **Contains**: Three-sentence summaries for every HTML page, SEO tags, usage guidance
- **Why critical**: This is the source of truth for content and structure

**File**: `docs/TEXTBOOK_MIGRATION_GUIDE.md`
- **Purpose**: Step-by-step implementation instructions
- **Contains**: File renames, new files to create, content migration notes, implementation checklist
- **Why critical**: Tells you exactly which files to create/rename/update

### 2. Style Guides
**File**: `AGENTS.md`
- **Purpose**: Agent instructions and repo-specific constraints
- **Contains**: Textbook is HTML for LibreTexts, no JavaScript, changelog requirements
- **Why critical**: Top-level constraints for all work

**File**: `docs/LIBRETEXTS_HTML_GUIDE.md`
- **Purpose**: HTML authoring rules for LibreTexts compatibility
- **Contains**: Table format, no internal links, template.ShowOrg() requirement
- **Why critical**: Every HTML file must follow these rules

**File**: `docs/REPO_STYLE.md`
- **Purpose**: Repository conventions and file organization
- **Contains**: Naming conventions, file structure, documentation standards
- **Why critical**: Ensures consistency across the repo

## Source Content Files (By Chapter)

### Chapter 2: OPL Header (New Section 2.2)
**File**: `OTHER_REPOS-do_not_commit/biology-problems/docs/webwork/WEBWORK_HEADER_STYLE.md`
- Complete OPL header guide with examples
- TITLE, DESCRIPTION, KEYWORDS, DBsubject/DBchapter/DBsection format
- Copy-paste template at the end

### Chapter 2: Macros (Update Section 2.5)
**File**: `OTHER_REPOS-do_not_commit/biology-problems/docs/webwork/PG_2_17_RENDERER_MACROS.md`
- Complete macro allowlist for ADAPT/renderer
- Used for macro availability reference

**File**: `docs/PG_MACRO_VERSION_COMPARISON.md`
- Comparison across PG versions (ADAPT/renderer vs full PG 2.17+ vs PG 2.20)
- Add table to Chapter 2.5

### Chapter 6: Advanced PGML Techniques (Complete Restructure)

**6.1 MODES and HTML-only output:**
- `OTHER_REPOS-do_not_commit/biology-problems/docs/webwork/WEBWORK_PROBLEM_AUTHOR_GUIDE.md` (sections on MODES, HTML whitelist)
- `OTHER_REPOS-do_not_commit/biology-problems/docs/webwork/PGML_LINTER_EXPECTATIONS.md` (MODES pitfalls)

**6.2 Coloring text and emphasis:**
- `OTHER_REPOS-do_not_commit/biology-problems/docs/webwork/COLOR_TEXT_IN_WEBWORK.md`
- Complete guide on CSS styling vs TeX color commands

**6.3 Tables with niceTables:**
- `OTHER_REPOS-do_not_commit/biology-problems/docs/webwork/NICETABLES_TRANSLATION_PLAN.md`
- DataTable vs LayoutTable patterns
- Add biology examples: dilution series, enzyme kinetics

**6.4 Matching problems:**
- `OTHER_REPOS-do_not_commit/biology-problems/docs/webwork/MATCHING_PROBLEMS.md`
- `OTHER_REPOS-do_not_commit/biology-problems/problems/matching_sets/yaml_match_to_pgml.py` (first 200 lines)
- Add biology examples: pathway matching, bond types

**6.5 Multiple choice statements:**
- `OTHER_REPOS-do_not_commit/biology-problems/docs/webwork/PGML_QUESTION_TYPES.md` (MC sections)
- `OTHER_REPOS-do_not_commit/biology-problems/problems/multiple_choice_statements/yaml_mc_statements_to_pgml.py` (first 200 lines)
- Add biology examples: experimental design, pathway regulation

**6.6 Advanced randomization:**
- `OTHER_REPOS-do_not_commit/biology-problems/docs/webwork/RANDOMIZATION_REFERENCE.md`
- `OTHER_REPOS-do_not_commit/biology-problems/docs/webwork/WEBWORK_PROBLEM_AUTHOR_GUIDE.md` (randomization sections)
- Add biology examples: qPCR conditions, genetics crosses

### Chapter 7: Renderer API (New Section 7.2)
**File**: `OTHER_REPOS-do_not_commit/webwork-pg-renderer/docs/RENDERER_API_USAGE.md`
- Complete API documentation
- POST / vs POST /render-api
- Parameter precedence: problemSourceURL > problemSource > sourceFilePath

**File**: `OTHER_REPOS-do_not_commit/webwork-pg-renderer/README.md`
- Renderer overview, private/ folder workflow
- GET /health endpoint

## Reference Files

### PG/PGML Authoring Standards
**File**: `OTHER_REPOS-do_not_commit/biology-problems/docs/webwork/WEBWORK_PROBLEM_AUTHOR_GUIDE.md`
- Comprehensive PGML-first authoring guide
- Canonical file skeleton
- PGML requirements, inline grading, randomization rules

**File**: `OTHER_REPOS-do_not_commit/biology-problems/docs/webwork/PGML_QUESTION_TYPES.md`
- Question type patterns (RadioButtons, PopUp, matching, etc.)
- PGML-first examples

**File**: `OTHER_REPOS-do_not_commit/biology-problems/docs/webwork/PGML_LINTER_EXPECTATIONS.md`
- Common PGML mismatches and pitfalls
- What fails and why

### Existing Textbook Content (For Context)
**Read existing sections** to maintain tone and style:
- `Textbook/01_Introduction/1.0-Index.html` (for tone)
- `Textbook/03_PGML_PG_Markup_Language/3.1-Introduction_to_PGML.html` (for PGML basics reference)
- `Textbook/04_Breaking_Down_the_Components/4.1-Full_file.html` (needs OPL header added)

## Changelog and History
**File**: `docs/CHANGELOG.md`
- Read 2026-01-28 entry to understand all recent changes
- Add new entry when work is complete

## Implementation Priority Order

### Phase 1: Critical Renames and Structure
1. Read: `docs/TEXTBOOK_MIGRATION_GUIDE.md` (implementation checklist)
2. Rename Chapter 2 files (2.2→2.3, 2.3→2.4, 2.4→2.5, 2.5→2.6)
3. Rename Chapter 4 files (4.2→4.3, etc.)
4. Rename Chapter 7 files (7.2→7.3)
5. Rename Chapter 6 directory

### Phase 2: New Content (High Priority)
1. Create `2.2-OPL_header_and_metadata.html`
   - Read: `WEBWORK_HEADER_STYLE.md`
   - Read: `TEXTBOOK_PAGE_SUMMARIES.md` for 2.2
2. Create `4.2-OPL_Header.html`
   - Read: `WEBWORK_HEADER_STYLE.md`
   - Read: `TEXTBOOK_PAGE_SUMMARIES.md` for 4.2
3. Update `4.1-Full_file.html` to add OPL header

### Phase 3: Chapter 6 (Advanced PGML)
Create all six new sections reading corresponding source files listed above:
1. `6.1-MODES_and_HTML_only_output.html`
2. `6.2-Coloring_text_and_emphasis.html`
3. `6.3-Tables_with_niceTables.html`
4. `6.4-Matching_problems.html`
5. `6.5-Multiple_choice_statements.html`
6. `6.6-Advanced_randomization_patterns.html`

### Phase 4: Chapter 7 Updates
1. Create `7.2-API_usage_for_scripts.html`
   - Read: `RENDERER_API_USAGE.md`
2. Update `7.0-Index.html` (add /health, PG 2.17 subset note)
3. Update `7.1-Quickstart_and_editor_workflow.html` (add private/ folder)

### Phase 5: Appendices
1. Create `90.1-Minimal_templates.html` (with OPL headers)
2. Create `90.2-Glossary.html`
3. Create `90.3-Troubleshooting_checklist.html`
4. Update `90.0-Index.html`

### Phase 6: Updates to Existing Files
1. Update `2.0-Index.html` (five-section acknowledgment)
2. Update `2.5-Common_PG_Macros.html` (add version comparison table)
3. Update `4.0-Index.html` (five-section structure)
4. Update `6.0-Index.html` (advanced techniques focus)
5. Update Chapter 1 sections with PG 2.17 subset notes

## Quality Checks Before Completion

1. Every HTML file ends with `<p>{{template.ShowOrg()}}</p>` (for X.0-Index.html files only)
2. No `<a href=...>` internal links in Textbook/ HTML files
3. No `<script>` tags or JavaScript
4. All tables use LibreTexts-compatible format (see `docs/LIBRETEXTS_HTML_GUIDE.md`)
5. Run HTML lint: `/opt/homebrew/bin/bash tests/run_html_lint.sh`
6. Update `docs/CHANGELOG.md` with completion entry

## Quick Reference Card

**When creating new HTML pages:**
- Follow three-sentence structure from `TEXTBOOK_PAGE_SUMMARIES.md`
- Use tone/style from existing textbook pages
- Follow LibreTexts constraints from `LIBRETEXTS_HTML_GUIDE.md`
- Include biology-first examples where noted in summaries
- No internal `<a href>` links
- Tables must use LibreTexts format

**When working on OPL headers:**
- Use template from `WEBWORK_HEADER_STYLE.md`
- Include: TITLE, DESCRIPTION, KEYWORDS, DBsubject/DBchapter/DBsection, Date, Author, Institution
- Show biology-appropriate DBsubject classifications

**When integrating biology examples:**
- See `TEXTBOOK_MIGRATION_GUIDE.md` "Content Migration Notes" section
- Examples should be short (5-15 lines of PG code)
- Show the pattern, not a complete problem

**When in doubt:**
- Check `TEXTBOOK_PAGE_SUMMARIES.md` first (what should this page contain?)
- Check `TEXTBOOK_MIGRATION_GUIDE.md` second (what file operations needed?)
- Check source content files third (where is the content to write from?)
