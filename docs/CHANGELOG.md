# Changelog

## 2026-01-13
- Switched the Chapter 4 worked example to a radio-button choice prompt, updating the full file
  reference and the Preamble/Setup/Statement/Solution walkthroughs to match the parserRadioButtons
  pattern.
- Updated Chapter 4 index and workflow tables to align with the choice-based example and removed
  unit-specific language where it no longer applied.
- Added orienting paragraphs to the Chapter 4 index and each section page to emphasize how to read
  problems safely, where failures originate, and why the solution matters for trust.
- Added broken-example callouts to Chapter 4 Preamble, Setup, Statement, and Solution pages to
  show common failure modes and the quickest diagnostic checks.
- Refreshed Chapter 4 page summaries in `Textbook/TEXTBOOK_PAGE_SUMMARIES.md` to match the new
  example and macro focus.
- Tuned Chapter 1 pages with instructor-facing reassurance, clearer tool-fit guidance, and
  stronger “where to focus first” cues across sections 1.0 to 1.6.
- Added consistent "How to read this code" blocks to Chapter 4 Preamble, Setup, Statement, and Solution pages,
  including focused code excerpts, line-notes tables, and common mistake callouts to guide interpretation.

## 2026-01-12
- Restored section row styling in Chapter 4 tables without naming colors, and added a brief note
  in the Chapter 4 index explaining the visual cue.
- Tightened Chapter 4 prose and tables by removing deprecated PopUp references, simplifying the
  macro table, adding guided habit paragraphs, and eliminating section color cues inside tables.
- Added narrative lead-ins across Chapter 4 pages to create a guided walkthrough before the
  supporting tables and workflow checklists.
- Removed explicit color labels from Chapter 4 section headers and tables while keeping the
  visual cues for scanning.
- Trimmed Chapter 4 section pages to remove repeated overview tables, tightened the workflow page,
  and added canonical example references plus fast-check guidance for Statement and Solution pages.
- Filled Chapter 2.5 with legacy-pattern guidance, replacement tables, and a PGML-first rewrite
  path so the HTML lint passes.
- Added a Chapter 1 index section map plus the PG vs PGML and "Where to start today" tables for
  a more scannable quickstart path.
- Filled `Textbook/01_Introduction/1.5-Common_terms_and_names.html` with a concise terms table and
  an authoring-focused apply-it-today reminder.
- Added a WeBWorK author workflow row to the Chapter 1.4 comparison table to call out local
  rendering when ADAPT errors are opaque.
- Updated Chapter 1 summaries and the README quickstart path to reflect the current numbering.
- Rebuilt Chapter 4 pages to use the color-coded section map, compact scan tables, and
  OpenWeBWorK-style Preamble/Setup/Statement/Solution framing across the index and subpages.
- Filled Chapter 4 sections (Full file, Preamble, Setup, Statement, Solution, Put it together)
  with table-driven guidance, official pattern references, and workflow checks.
- Updated the Chapter 4 entries in `Textbook/TEXTBOOK_PAGE_SUMMARIES.md` to match the new layout
  and workflow focus.
- Refined the Chapter 1.6 and Chapter 2.2 local-testing notes to explicitly use the ADAPT preview as the final check
  and webwork-pg-renderer (Chapter 7) as the line-level debugging path.
- Updated `Textbook/TEXTBOOK_PAGE_SUMMARIES.md` to refer to the Chapter 7 health check without a leading slash.
- Updated Chapter 1 and Chapter 2 pages to reference Chapter 7 local rendering at the points where authors most often
  hit generic ADAPT errors (quickstart and after macro/setup changes).
- Merged the Chapter 5 workflow and QA pages into
  `Textbook/05_Different_Question_Types/5.9-Workflow_and_QA_in_ADAPT.html` so Chapter 5 has at most 9 subsections
  after the index.
- Updated `Textbook/TEXTBOOK_PAGE_SUMMARIES.md` to recommend Chapter 7 local testing as the default for authors building
  a bank (with fallbacks), and to reference Chapter 7 from key workflow pages (Quickstart, file skeleton, blanks,
  deep-dive randomization, and QA).
- Updated `README.md` to better reflect the current repo layout by adding links to `docs/` and
  `Textbook/TEXTBOOK_PAGE_SUMMARIES.md` and by restoring the Chapter 7 entry point in the chapter list.
- Added an external resource list to `README.md` (kept out of `Textbook/` to avoid HTML links in LibreTexts-imported
  content) and added the same URLs to `Links/webwork_links.txt`.
- Tightened Chapter 2 to treat minimal PG as an explicit contract (PG is setup, PGML is the prompt), added a
  life-science-first mindset checklist, updated the minimal template to a dilution-style prompt, and labeled advanced
  macros as recognition-only.
- Tightened Chapter 1 pages to use a more consistent page structure (short opener, decision-oriented sections, and an
  "Apply it today" closer) while keeping content aligned with `Textbook/TEXTBOOK_PAGE_SUMMARIES.md`.
- Filled previously-empty Chapter 7 local-testing pages to match `Textbook/TEXTBOOK_PAGE_SUMMARIES.md` and to restore
  a clean `tests/run_html_lint.sh` run.
- Updated `README.md` into a clearer landing page and corrected the chapter entry-point paths to match the current
  `Textbook/` layout.
- Aligned Chapter 1 HTML pages with `Textbook/TEXTBOOK_PAGE_SUMMARIES.md` by adding a quick-start/navigation section
  to `Textbook/01_Introduction/1.0-Index.html` and tightening the Chapter 1 feature and quickstart pages.
- Added `docs/CODE_ARCHITECTURE.md` and `docs/FILE_STRUCTURE.md` to document the repo workflows, components, and
  directory layout.
- Rewrote `README.md` as a stable repository overview and authoring guide (LibreTexts constraints,
  chapter map, editing workflow, and validation commands).
- Expanded `README.md` with repository layout, topic coverage, and usage guidance
  based on the Insight-HTML exports.
- Replaced `README.md` with the chapter expansion plan for the `Textbook/` guide.
- Removed autogenerated `Textbook/00_Front_Matter/` and `Textbook/99_Back_Matter/` folders to
  avoid confusion about where editable content belongs.
- Filled previously-empty chapter HTML files and expanded existing chapter pages with PGML-first,
  science-focused guidance using the local Insight/WebWorK HTML archives as source material.
- Added `tools/html_lint_checker.py` (lxml-based) and `tests/run_html_lint.sh` to lint textbook HTML
  for LibreTexts compatibility (no links, no JavaScript).
- Updated `AGENTS.md` with the repo intent (textbook/guide) and the HTML authoring constraints.
- Updated `README.md` plan to reflect the no-link rule and removal of front/back matter.
- Added a new Chapter 1 comparison page and a brief comparison section in Chapter 1.2 to position
  WeBWorK against other autograded formats (H5P, LMS packages, quiz banks, etc.).
- Updated the Chapter 1.4 comparison table to use LibreTexts responsive table markup while keeping
  explicit column widths.
- Added `docs/LIBRETEXTS_HTML_GUIDE.md` documenting the standard LibreTexts-compatible table format
  and other HTML authoring rules for `Textbook/`.
- Documented the requirement that every `X.0-Index.html` chapter index ends with
  `<p>{{template.ShowOrg()}}</p>` and updated all chapter index files to include it.
- Removed explicit subsection filename lists from `Textbook/06_WeBWorK_for_Different_Subjects/6.0-Index.html`
  to avoid link-like navigation in LibreTexts and rely on `{{template.ShowOrg()}}` instead.
- Added Chapter 5 question type subsections with science examples for MC, MA, MATCH, NUM, FIB,
  MULTI_FIB, and ORDER.
- Refocused Chapter 6 back to subject-specific guidance that assumes the Chapter 5 question types.
- Added `Textbook/TEXTBOOK_PAGE_SUMMARIES.md` with page summaries for each `Textbook/` HTML page.
- Updated `Textbook/TEXTBOOK_PAGE_SUMMARIES.md` to use three human-readable sentences per page and
  to avoid the words "learning", "objective", "outcome", and "goal".
- Added a short "SEO tags" list to the third sentence of each page summary in
  `Textbook/TEXTBOOK_PAGE_SUMMARIES.md`.
- Rewrote `Textbook/TEXTBOOK_PAGE_SUMMARIES.md` to vary sentence openers while keeping the
  three-sentence structure and the stable "Use it ..." third sentence.
- Moved the `Textbook/TEXTBOOK_PAGE_SUMMARIES.md` SEO tags onto a separate line under each entry.
- Expanded the `Textbook/TEXTBOOK_PAGE_SUMMARIES.md` guideline language to better match the intended
  three-sentence structure while avoiding formal jargon.
- Updated `Textbook/TEXTBOOK_PAGE_SUMMARIES.md` SEO tags to be intentionally short (aiming for ~3
  tags per page, allowing fewer or more when it helps).
- Shifted `Textbook/TEXTBOOK_PAGE_SUMMARIES.md` SEO tags away from repeated global terms and toward
  page-specific, index-like topics.
- Reorganized the textbook chapter layout by adding a Chapter 1 quickstart and splitting question
  types into `Textbook/05_Question_Types/` with life-science-first examples and checklists.
- Expanded `Textbook/02_Problem_Generation_PG/2.2-PG_Problem_Files_with_a_pg_file_extension.html`
  with a five-section structure guide and an annotated PGML-first skeleton.
- Expanded `Textbook/02_Problem_Generation_PG/2.4-Common_PG_Macros.html` with advanced macro topics
  frequently referenced in older problems (algorithmic and InexactValue-related patterns).
- Condensed the PGML chapter to a smaller set of focused subsections under
  `Textbook/03_PGML_PG_Markup_Language/` and updated the chapter index accordingly.
- Updated the worked example in `Textbook/04_Simple_Problem_Example_in_WeBWorK/4.0-Index.html` to a
  PCR mix concentration calculation (life-science lab context).
- Integrated ADAPT workflow notes and QA guidance into Chapter 5 via
  `Textbook/05_Different_Question_Types/5.9-Workflow_and_QA_in_ADAPT.html` and removed the separate
  `Textbook/07_*` through `Textbook/13_*` standalone chapter folders to keep the main chapter list compact.
- Added Chapter 6 subject-specific subsections with a biology-first pattern catalog (dilutions,
  kinetics, genetics mapping, pathways, gels/blots, qPCR Ct, pedigrees, and experimental design).
- Added `Textbook/90_Appendices/90.5-Advanced_patterns_and_further_techniques.html` as a curated
  "further techniques" section (strings in context, data tables, custom feedback, and scaffolding).
