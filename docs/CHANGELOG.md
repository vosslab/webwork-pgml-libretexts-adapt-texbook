# Changelog

## 2026-02-26

### Add Markdown export script for AI-agent-friendly textbook output
- Created `tools/textbook_html_to_markdown.py` — converts all `Textbook/*/*.html` files into a
  single merged Markdown file via `pandoc`, with table of contents and section separators.
- Reuses the same chapter/section sort logic as `tools/textbook_html_to_pdf.py`.
- Added `pandoc` to `Brewfile`.

### Add Section 6.8: Displaying Chemical Formulas with mhchem
- Created `Textbook/06_Advanced_PGML_Techniques/6.8-Displaying_Chemical_Formulas_with_mhchem.html`
  covering the `\ce{}` command for typesetting chemical formulas and reaction equations via MathJax.
- Page includes inline vs display-mode syntax, common mhchem syntax table, usage inside
  RadioButtons choices, and a complete PGML working example (cellular respiration oxidation question).
- Updated `6.0-Index.html` with a new bullet ("I need to display chemical formulas or reaction
  equations") and a new row in the Quick patterns table for Section 6.8.

## 2026-02-16

### Expand Section 2.6 with high-frequency legacy patterns from OPL analysis
- Added `beginproblem()` (78% of OPL), `num_cmp()` (46%), `str_cmp()` (7%), and
  `fun_cmp()` to the "Legacy patterns to recognize" table with OPL prevalence counts.
- Added new "Legacy answer evaluators" section with a 5-row replacement table covering
  `num_cmp`, `str_cmp`, `fun_cmp`, `std_num_str_cmp`, and `numerical_compare_with_units`,
  each with OPL prevalence, description, and MathObjects replacement.
- Added "beginproblem(): safe to delete" section explaining that `DOCUMENT()` alone
  handles initialization (based on analysis of 72,734 OPL files).
- Added 4 new rows to "Deprecated or fragile behaviors" table: legacy answer evaluators,
  `TEXT(beginproblem())`, `AnswerFormatHelp.pl`, and `compoundProblem.pl`.

## 2026-02-15

### Create Appendix 90.4: Macro Demonstrations with Version History
- Created `Textbook/90_Appendices/90.4-Macro_Demonstrations.html` with 22 macro entries: 6
  cross-references to existing demos elsewhere in the textbook plus 16 new complete PG problems.
- Each entry includes a one-line version history note (PG version introduced, key updates).
- New demos organized into four groups: interaction widgets (PGchoicemacros.pl,
  draggableSubsets.pl, parserWordCompletion.pl, PGessaymacros.pl), science-native contexts
  (parserNumberWithUnits.pl, parserFormulaWithUnits.pl, contextScientificNotation.pl,
  contextReaction.pl, contextFraction.pl, contextPercent.pl), grading and feedback
  (answerCustom.pl, answerHints.pl, parserMultiAnswer.pl, PGgraders.pl, weightedGrader.pl),
  and layout and scaffolding (scaffold.pl).
- Cross-references point to existing demos in Sections 5.2, 5.4, 5.6, 5.8, 6.2, 6.3, and
  Appendix 90.1 for parserRadioButtons.pl, parserPopUp.pl, draggableProof.pl,
  contextArbitraryString.pl, niceTables.pl, and PGgraphmacros.pl.
- All biology-themed: organelle matching, macromolecule sorting, enzyme kinetics, dilutions,
  bacterial growth, Mendelian genetics, Hardy-Weinberg, pH range checking, scaffolded genetics.
- All demos use PGML (`BEGIN_PGML`/`END_PGML`). Only 2 `ANS()` calls remain where
  required by macro design: `PGchoicemacros.pl` (`str_cmp` for match list form fields)
  and `PGessaymacros.pl` (`essay_cmp` for essay box form field).
- Updated `90.0-Index.html` with description and link for Appendix 90.4.
- Updated `TEXTBOOK_PAGE_SUMMARIES.md` with 3-sentence summary and SEO tags.

### Add PGchoicemacros.pl deprecation guide to Section 2.6
- Added three rows to the "Deprecated or fragile behaviors" table in
  `2.6-Legacy_PG_and_deprecated_patterns.html`: `NchooseK()`, `shuffle()`, and
  `new_match_list` with `print_q`/`print_a`.
- Added a dedicated "PGchoicemacros.pl: widely used, mostly deprecated" section with a
  5-row replacement table covering `NchooseK`, `shuffle`, `new_match_list`,
  `new_select_list`, and `new_multiple_choice` with modern equivalents.
- Clarified that `PGsort` is a core function from PGbasicmacros.pl, not from
  PGchoicemacros.pl, and is not deprecated.

### Add complete working PG problem examples to Chapter 6
- Added `<h2>Complete working example</h2>` sections with full PG problems to
  seven Chapter 6 files: 6.1 through 6.7.
- Each example includes a complete OPL header, `DOCUMENT()`/`ENDDOCUMENT()` wrapper,
  `loadMacros(...)` block, `BEGIN_PGML`/`END_PGML` body, and biology-themed content.
- Section 6.1 (Text coloring): amino acid charge at given pH with CSS class emphasis.
- Section 6.2 (niceTables): enzyme kinetics DataTable with RadioButtons.
- Section 6.3 (Graphs): linear function graph with PGgraphmacros and numeric answer.
- Section 6.4 (Randomization): genetics offspring count using random() and list_random().
- Section 6.5 (Matching): organelle function matching with PopUp dropdowns.
- Section 6.6 (True/false MC): enzyme behavior true/false with per-statement RadioButtons.
- Section 6.7 (RDKit): amino acid identification from RDKit.js chemical structure.
- All 7 extracted PG problems pass renderer lint (0 errors, 0 warnings).

### Add complete working PG problem examples to Chapter 5
- Added `<h2>Complete working examples</h2>` sections with two full PG problems each
  to seven Chapter 5 files: 5.2 through 5.8.
- Each example includes a complete OPL header, `DOCUMENT()`/`ENDDOCUMENT()` wrapper,
  `loadMacros(...)` block, `BEGIN_PGML`/`END_PGML` body, and biology-themed content.
- Section 5.2 (Multiple choice): genetics RadioButtons and organelle identification.
- Section 5.3 (Multiple answer): PCR requirements and enzyme properties via per-statement RadioButtons.
- Section 5.4 (Matching): macromolecule-to-monomer and bond-type PopUp matching.
- Section 5.5 (Numerical entry): dilution calculation and surface-area-to-volume ratio with tolerance.
- Section 5.6 (Fill in the blank): organelle naming and nucleic acid abbreviation using ArbitraryString context; added `contextArbitraryString.pl` macro to loadMacros.
- Section 5.7 (Multi-part fill in the blank): monohybrid cross fractions and three-part dilution.
- Section 5.8 (Ordered list): PCR steps and mitosis phases using DraggableProof with ANS().
- All 14 extracted PG problems pass renderer lint (0 errors, 0 warnings).

### Add complete PG problem examples to Chapter 4.7 and Appendix 90.1
- Added a complete biology RadioButtons example to `Textbook/04_Breaking_Down_the_Components/4.7-Putting_it_together.html` demonstrating all five sections (OPL header, preamble, setup, statement, PGML prompt).
- Added two new templates to `Textbook/90_Appendices/90.1-Minimal_templates.html`: DraggableProof (ordered list) and fill-in-the-blank (String context), bringing the template count from 4 to 6.
- Fixed fill-in-the-blank template: added missing `contextArbitraryString.pl` to `loadMacros()` so `Context("ArbitraryString")` resolves.

### Fix broken PGML templates in Appendix 90.1
- Fixed Block 3 (PopUp matching template): changed macro load from `PGchoicemacros.pl` to
  `parserPopUp.pl` so the `PopUp()` function is defined, and switched from `\@choices`
  named array reference to inline anonymous arrayrefs `[...]` as required by PG 2.17's
  `parserPopUp.pl`.
- Fixed Block 4 (multi-part template): replaced invalid inline `Compute("$ratio > 1")` in a
  PGML answer blank with a pre-computed `$double = Real(2 * $ratio)` variable and a
  pedagogically meaningful second prompt.

### Remove static linter, use pg-renderer only
- Removed `tools/webwork_simple_lint.py` (static lint produced false-positive warnings on
  valid PG patterns like bare `$var =` assignments).
- Refactored `tools/lint_textbook_problems.py` to validate exclusively via the pg-renderer
  API (`/render-api` endpoint), removing the static lint step, `pglint.py` dependency, and
  `--skip-renderer` flag.
- Added HTML-based error detection to `is_error_flagged()` so Translator errors in non-JSON
  renderer responses are caught.
- Simplified CSV report columns from 8 to 5 (removed `static_status`, `static_messages`,
  `renderer_status`, `renderer_messages`; replaced with `status` and `messages`).
- Cleaned up `tools/extract_textbook_pre_blocks.py`: removed `run_lint()` and `run_pglint()`
  functions, `--mode` argument, and unused `subprocess`/`sys` imports.
- Updated `tests/test_lint_textbook_problems.py` to remove static lint tests and use
  renderer-based assertions.
- Updated `tools/README.md`, `docs/CODE_ARCHITECTURE.md`, and `docs/FILE_STRUCTURE.md` to
  remove `webwork_simple_lint.py` and `pglint.py` references.
- Changed `extract_textbook_pre_blocks.py` HTML parser from `recover=False` to `recover=True`
  so the lint pipeline can scan directories with malformed HTML (e.g., `WebWorK-HTML/`)
  without crashing on misplaced tags.

### PGML validation pipeline
- Added `tools/lint_textbook_problems.py` -- end-to-end pipeline that extracts complete PG
  problems from textbook HTML, runs static lint via `webwork_simple_lint`, optionally runs
  renderer lint via `pglint`, and produces a CSV report (`lint_report.csv`) with per-problem
  pass/warn/error/skipped status and a console summary.
- Updated `tools/pglint.py` with JWT redaction (regex patterns ported from
  `webwork-pg-renderer/script/lint_pg_via_renderer_api.py`), a `check_renderer_health()` function
  that GETs `/health`, and a `lint_file_to_result()` importable API that returns structured dicts
  without printing.
- Updated `tools/webwork_simple_lint.py` with a `lint_text_to_result()` importable wrapper that
  calls `validate_text()` and returns a structured dict with status, issues, error count, and
  warning count.
- Added `tools/README.md` documenting all 12 tools with one-line descriptions, usage examples,
  grouped by purpose (pipeline, HTML, textbook utilities, other).
- Added `tests/test_lint_textbook_problems.py` with 17 tests covering `is_full_problem()`,
  HTML extraction, static lint, CSV report columns, `compute_overall_status()` logic, and
  renderer integration (skipped when renderer is unavailable).
- Added `output/textbook_pre_blocks/` to `.gitignore` (generated extraction artifacts).

### Prose density improvements (Chapters 2-4 and 6)
- Added contextual prose around code blocks and tables across 8 files in Chapters 2, 3, 4,
  and 6 to improve readability and explain *why* and *when* for each code pattern.
- Section 2.4 (`2.4-Sections_within_a_PG_question.html`): skeleton description before the
  section map code block, customization guidance after it, top-to-bottom execution explanation
  before the "Common failure and fix" block, and a lookup sentence before the "Where does this
  go?" table.
- Section 2.5 (`2.5-Common_PG_Macros.html`): "start here" note directing first-time authors
  to the four core macros, symptom explanation before the "Common failure and fix" block,
  foundation sentences before 6 macro reference tables, and a lookup sentence before the
  "Quick reference" table.
- Section 2.7 (`2.7-Future_PG_Version_Features.html`): practical impact summaries before PG
  2.18, 2.19, and 2.20 feature tables, and workaround-mapping framing before the "What this
  means for ADAPT authors today" summary table.
- Section 3.1 (`3.1-Introduction_to_PGML.html`): lead-in and follow-up sentences for the
  "Copy and edit" PGML template, and a symptom explanation before the "Common failure and
  fix" block.
- Section 3.2 (`3.2-Answer_blanks_and_answers.html`): lead-in and follow-up for the "Copy
  and edit" template, symptom explanation before the failure/fix block, motivating paragraph
  before text answers code, guidance on `Compute()`/`Formula()` for expression blanks, and a
  grading-pipeline explanation before the "Why attach answers to blanks" list.
- Section 4.1 (`4.1-Full_file.html`): debugging guidance before the "Section anchors" table,
  expanded cross-reference paragraph, summary sentence before "Section quick reference", and
  a read-it-as-a-story paragraph before the complete file code block.
- Section 4.2 (`4.2-OPL_Header.html`): lead-in and follow-up for the "Worked example header"
  code block, and a license-first sentence before the "License comments" code block.
- Section 6.2 (`6.2-Making_Tables_with_niceTables.html`): template descriptions before both
  "Copy and edit" code blocks, a plain-text-first tip before "Cell content formats", a
  convenience note before "PGML table syntax", and a conversion context sentence before
  "Translating HTML tables".

### Sibling repo content mining
- Created `output/repo_mining/` with 9 structured reports (2,946 lines, 193KB total) mining all 8
  sibling repos for textbook-relevant content.
- Individual reports: `biology_problems.md`, `webwork_pgml_opl_training_set.md`, `pg_v2_17.md`,
  `webwork_pgml_linter.md`, `webwork_pg_renderer.md`, `webwork_open_problem_library.md`,
  `biology_problems_website.md`, `qti_package_maker.md`.
- Consolidated `SYNTHESIS.md` with per-chapter findings, 20 priority actions, 10 content gaps,
  per-repo value summaries, and cross-repo synergy analysis.

### New Section 2.7: Future PG Version Features
- Created `Textbook/02_Problem_Generation_PG/2.7-Future_PG_Version_Features.html` documenting PG
  features from versions 2.18, 2.19, and 2.20 that are not yet available in ADAPT.
- Content sourced from `biology-problems/docs/webwork/PG_2.19_to_2.16_features.txt` (OpenWeBWorK
  wiki release notes for WW 2.16–2.19).
- Includes workaround-to-replacement mapping table showing what changes when ADAPT upgrades
  (CheckboxList replaces RadioButtons fallback, DropDown replaces PopUp, PGML div/span syntax
  replaces MODES wrappers, native PGML images, plotly3D, TikZ).
- PG 2.20 section populated with plots.pl, contextUnits.pl, contextExtensions.pl, GraphTool
  improvements, contextReaction.pl updates, HTML in DropDown items, and breaking changes
  (custom_problem_grader_0_60_100 removed).
- Added PG 2.19 breaking changes (PopUp integer handling) and deprecations (compoundProblem.pl).
- Updated Ch2 index (2.0) with new task-first entry for Section 2.7.
- Updated `TEXTBOOK_PAGE_SUMMARIES.md` with summary and SEO tags for Section 2.7.

### Internal link fixes
- Converted ~30 bare "Section X.X" text references to proper `/@go/page/` hyperlinks across
  8 files (2.0, 2.1, 2.4, 4.0, 4.2, 5.9, 6.4, 7.0, 7.6).
- Fixed page IDs in Section 2.7 cross-references to match textbook display numbering convention.
- Confirmed zero TBD links remain in the textbook.
- Audit found Ch6 has the same display-vs-file numbering discrepancy as Ch7 (sections 6.3-6.6
  are reordered in the textbook display order vs LibreTexts file paths).

### Summary refresh for TEXTBOOK_PAGE_SUMMARIES.md
- Polished 14 of 63 page summaries in `Textbook/TEXTBOOK_PAGE_SUMMARIES.md` after comparing
  existing text against fresh summaries generated independently from the HTML source files.
- Chapter 1 (6 updates): added specific content types (concentrations, dilutions, fold-change),
  named comparison targets (H5P, LMS-native), expanded platform terms (OPL, Commons, Insight,
  Studio), added OPL life-science content caveat, and more specific copy-edit guidance.
- Chapter 5 (7 updates): added widget and implementation details previously missing from
  summaries (RadioButtons, PopUp widgets, DraggableProof with legacy Print/ANS, string Context,
  Compute tolerance, named variables for inline blanks, RadioButtons fallback for checkbox
  unavailability in PG 2.17).
- Chapter 6 (1 update): added YAML statement banks and conflict groups to 6.6 summary.
- Improved SEO tags across updated entries to be more specific and unique per page.
- No changes to Chapters 2, 3, 4, 7, 8, or 90 (existing summaries already matched HTML content).

### Textbook PDF build tooling
- Added `tools/textbook_html_to_pdf.py` to render all `Textbook/*/*.html` pages to per-page PDFs
  with headless `weasyprint`, then merge them in order with `cpdf` into one compiled textbook PDF.
- Simplified the script to minimal argparse: only `-o/--output` remains; default output is
  `./<cwd_name>.pdf` (for this repo, `webwork-pgml-libretexts-adapt-texbook.pdf`).
- Switched input detection to auto-resolve repo root using `tests/git_file_utils.py`
  (`get_repo_root()`), then read from `<repo_root>/Textbook`.
- Switched temporary build storage to the system temp directory via `tempfile.TemporaryDirectory`
  (no persistent build cache folder in repo).
- Kept source HTML untouched while using temporary rewritten HTML (base tag insertion and stripped
  relative links) for PDF rendering compatibility.
- Added an explicit per-page header in temporary HTML (`chapter/file.html`) so the first page of
  each rendered section is clearly labeled in the merged PDF.
- Set default temporary render CSS to `body { font-size: 12pt; }` so compiled PDF body text uses
  a consistent 12pt baseline.
- Updated default render font to Times-style serif while keeping 12pt baseline so print sizing
  looks more natural.
- Added syntax highlighting for temporary `<pre>` code blocks using Pygments and set code block
  font sizing to 11pt monospace in the compiled PDF.
- Set code-block syntax highlighting to default Perl lexer (no auto-guessing) to keep PG/PGML
  variable coloring stable (for example `$a`, `$b`, `$ans`).
- Strengthened default CSS precedence by injecting render styles at the end of `<head>` and
  applying `!important` rules for 12pt body text and 11pt code blocks.
- Further tightened code-block sizing by forcing 11pt on all nested syntax-token spans (`pre *`,
  `code *`) and switching to a visually smaller Courier-style monospace stack.
- Produced `webwork-pgml-libretexts-adapt-texbook.pdf` (205 pages via WeasyPrint).
- Auto-fixed a pre-existing whitespace issue by adding a final newline to
  `Textbook/The_ADAPT_WeBWorK_Handbook.reremix.json` (triggered by `tests/test_whitespace.py`).

### Cross-references and CSV page map
- Updated `Textbook/Using_WeBWork_in_ADAPT-Map.csv` with corrected section numbers (shifted Ch 2
  and Ch 4 to reflect inserted 2.2 and 4.2 sections), updated "New Page" titles across Chapters
  5-7 to match actual content, corrected chapter titles for Ch 6 (Advanced PGML Techniques) and
  Ch 7 (Testing and Debugging), fixed underscore titles in Ch 1.5 and Ch 3.x, and added TBD
  placeholder rows for 10 sections without LibreTexts page IDs (2.2, 4.2, 7.3-7.6, 90.0-90.3).
- Added 221 internal cross-reference links across 57 HTML files using the `/@go/page/PAGE_ID`
  format. Links connect related content throughout the textbook: PG concepts to their PGML
  counterparts, question type basics to advanced patterns, macro references to usage examples,
  and error types to their debugging sections. Sections without page IDs (2.2, 4.2, 7.3-7.6,
  90.x) are referenced as plain text without hyperlinks.
- Added `/@go/page/` links to all chapter index pages (1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0,
  90.0) for their section listings where page IDs exist.

### New subchapters
- Created Chapter 6.6 Making graphs (566 lines) from HOW_TO_MAKE_GRAPHS.md. Covers
  PGgraphmacros.pl quick decision table, minimal example, init_graph parameters, axis labels and
  tick labels with Label constructor, add_functions syntax with computed coefficients, multiple
  curves, point-by-point curves with moveTo/lineTo, dashed lines, dots/stamps, label sizing and
  GD bitmap font table, worked triprotic titration curve example (speciation model vs cubic
  polynomial), GraphTool answer evaluator interference warning, sizing/margins guidance, variable
  scoping reminder, and unavailable macros list.
- Created Chapter 6.7 Rendering chemical structures (640 lines) from RDKIT_MOLECULAR_STRUCTURES.md
  and four PubChem docs (README_PUBCHEM_PGML.md, README_PUBCHEM_BPTOOLS.md,
  PUBCHEM_PGML_SYNTAX_NOTES.md, PGML_PUBCHEM_CONVERSION_SUMMARY.md). Covers RDKit.js quick start,
  SMILES basics from scratch, charged species notation (critical for biochemistry), common
  ionizable groups table, imidazole protonation notes, SMILES validation methods, canvas sizing
  guidelines, rendering options (mdetails), multiple molecules (sequential and side-by-side),
  randomization with sorted hash keys, common pitfalls, chemistry-specific guidelines (amino acids,
  nucleotides, peptides), and troubleshooting.

### Content enrichments
- Enriched Chapter 6.5 Advanced randomization (49 to 254 lines) from RANDOMIZATION_REFERENCE.md.
  Added comprehensive function reference table (core PG, auxiliary, parser widget, context, matrix,
  statistics), built-in seeding explanation (random() is already seeded by problemSeed), manual
  PGrandom pattern with correct/incorrect examples, expanded guard patterns with biology examples,
  and practical tips for hash key sorting and avoiding deprecated macros.
- Enriched Chapter 2.1 Introduction to PG Language (to 345 lines) from
  WEBWORK_PROBLEM_AUTHOR_GUIDE.md. Added five-component problem skeleton, PGML-first requirement,
  inline grading principle, minimum recommended macro set, context selection guidance, question
  order recommendation, file extension guidance (.pgml vs .pg), and key structural rules.
- Enriched Chapter 6.1 Coloring text and emphasis (47 to 350 lines) from
  QUESTION_STATEMENT_EMPHASIS.md, COLOR_CLASS_MIGRATION_PLAN.md, and COLOR_TEXT_IN_WEBWORK.md.
  Added emphasis styles by use case (numeric values, key terms, negation, multiple values), CSS
  class approach with HEADER_TEXT, font size guidelines, color palette recommendations table,
  accessibility considerations (contrast ratios, multiple emphasis methods), complete working
  examples, matching label colors, and what does not work (TeX/MathJax color commands).
- Enriched Chapter 2.2 OPL header (360 to 611 lines) and Chapter 4.2 OPL Header (207 to 311
  lines) from WEBWORK_HEADER_STYLE.md. Added Bloom's taxonomy level examples, additional
  biology-specific DBsubject classifications, attribution patterns for adapted problems, and
  expanded worked header examples.
- Enriched Chapter 2.5 Common PG Macros (497 to 825 lines) from PG_2_17_RENDERER_MACROS.md.
  Added expanded macro inventory organized by category with notes on graph macros, statistics
  macros, matrix macros, complex macros, and rarely-needed macros for biology.
- Enriched Chapter 6.2 Tables with niceTables (89 to 223 lines) from
  NICETABLES_TRANSLATION_PLAN.md. Added supported input shapes (plain text, hashrefs, arrayrefs),
  table-level options reference, PGML table syntax, translation approach for HTML tables, and
  unsupported table guidance.
- Enriched Chapter 6.3 Matching problems (484 to 742 lines) from MATCHING_PROBLEMS.md and
  MATCHING_SET_AUTHORING_GUIDE.md. Added YAML matching set authoring workflow including file
  naming, YAML structure, matching pairs format, same-concept-different-phrasing rule, excluding
  confusable pairs, replacement rules, quality checks, difficulty control, and yaml_match_to_pgml.py
  workflow with copy-paste YAML example.
- Enriched Chapter 6.4 Multiple choice statements (to 302 lines) from
  MC_STATEMENTS_AUTHORING_GUIDE.md. Added YAML statement bank authoring including conflict groups,
  statement IDs, replacement rules, when to use MC statements vs matching, good false statement
  patterns, avoiding accidental cues, difficulty control, quality checks, and
  yaml_mc_statements_to_pgml.py workflow with copy-paste YAML example.
- Distributed PGML linter expectations across Chapter 3 (3.1, 3.3, 3.5, 3.6) from
  PGML_LINTER_EXPECTATIONS.md. Added single-pass parsing rule to 3.1, ordered list auto-parsing
  gotcha to 3.3, HTML escaping in variables to 3.6, MODES in eval blocks warning to 3.6, and
  cross-references to 6.1 (MathJax color) and 6.2 (blocked HTML tags).
- Distributed preferred PGML question type patterns across Chapter 5 (5.2-5.8) from
  PGML_QUESTION_TYPES.md. Added RadioButtons pattern to 5.2, checkbox workaround to 5.3, PopUp
  matching pattern to 5.4, numeric tolerance pattern to 5.5, string Context to 5.6, multi-part
  evaluators to 5.7, and DraggableProof ordering pattern to 5.8.

### Navigation and metadata updates
- Updated 6.0-Index.html with entries for new subchapters 6.6 (graphs) and 6.7 (chemical
  structures) in both the task-first menu and quick patterns table.
- Updated TEXTBOOK_PAGE_SUMMARIES.md with three-sentence summaries and SEO tags for 6.6 and 6.7.
- Total content expansion: approximately 3,700 new lines across 2 new files and 17 enriched files,
  with content sourced from 15 documentation files in biology-problems/docs/webwork/ and
  biology-problems/problems/.

### Reremix rename alignment
- Added `tools/rename_textbook_reremix_filenames.sh` with explicit `git mv` commands to align
  local textbook filenames with the new reremix section titles and ordering from
  `Textbook/The_ADAPT_WeBWorK_Handbook.reremix.csv`.
- Added `tools/rename_textbook_reremix_titlecase_filenames.sh` with explicit `git mv` commands
  to normalize case and match reremix title casing exactly in filenames.
- Renamed Chapter 6 files to full title-based filenames and updated section numbering order:
  6.3 (Making Graphs), 6.4 (Advanced Randomization Techinques), 6.5 (Randomized Matching
  Problems), and 6.6 (Randomized MC True/False Statements).
- Renamed Chapter 7 files to full title-based filenames and updated section numbering order:
  7.1 (Simple Syntax Checking/Linting), 7.2 (Setting Up the PG Renderer), 7.3 (Scripting and
  Automation of the PG Renderer), 7.4 (Common Mistakes), 7.5 (Testing Randomization), and
  7.6 (QA Checklist).
- Added new Chapter 8 placeholder files under
  `Textbook/08_Using_AI_Agents_to_Write_WeBWorK/` for sections 8.0 through 8.4.
- Updated `Textbook/TEXTBOOK_PAGE_SUMMARIES.md` to match renamed Chapter 6 and Chapter 7 paths,
  and added Chapter 8 summary entries for the new placeholders.
- Updated `README.md` chapter entry points and chapter map to include the current Chapter 6, Chapter 7,
  and new Chapter 8 locations.
- Updated `docs/FILE_STRUCTURE.md` chapter directory map to replace obsolete Chapter 6 and add
  Chapters 7 and 8.
- Verified chapter filename coverage against `Textbook/The_ADAPT_WeBWorK_Handbook.reremix.csv`
  for Chapters 6 through 8 (no missing or extra files).
- Re-ran HTML lint after all renames and placeholder creation (`OK: linted 63 HTML files`).

### Index tooling
- Added `tools/extract_textbook_yake_keywords.py` to run YAKE keyword extraction across
  `Textbook/**/*.html` and write two CSV outputs:
  `output/yake_keywords_by_page.csv` (per-reference terms) and
  `output/yake_index_candidates.csv` (aggregated index candidates filtered by paragraph-reference count).
- Simplified argparse to the frequently changed options only (input/output paths, top-k, and min/max references),
  and removed the page/paragraph switch so paragraph is the fixed reference unit.
- Updated aggregate counting to use raw paragraph-hit counts per candidate term (algorithmic filtering), so
  ubiquitous title-level terms are excluded by the min/max reference window without a hard-coded exclude list.
- Updated YAKE missing-dependency guidance in the script to use the repo workflow:
  `source source_me.sh && python -m pip install yake`.
- Improved candidate quality with algorithmic post-processing:
  canonical singular/plural grouping, corpus-based low-information filtering, and
  subphrase deduplication when two terms point to identical references.
- Updated single-word candidate handling to keep only technical/code-like tokens
  (for example mixed-case identifiers), reducing generic one-word noise without a
  manual project-specific exclude list.
- Excluded chapter index pages (`*-Index.html`) from extraction so repeated
  navigation boilerplate does not dominate index candidates.
- Added a minimum paragraph length gate (8+ words) so short boilerplate/list
  fragments are not treated as index references.
- Tightened default aggregate candidate thresholds for manual review:
  `--min-docs` now defaults to 3 and candidates must appear on at least
  2 distinct pages.
- Changed aggregate ranking from frequency-first to an index-worthiness score
  that balances reference-count range, term specificity, and term shape.
- Added `tier` (`A`, `B`, `C`) and `index_score` columns in aggregate output to
  support faster manual curation.
- Added automatic shortlist output:
  `output/yake_index_shortlist.csv` (top `A`/`B` candidates by score).
- Added an editorial/meta penalty model and placeholder-term suppression so
  non-index boilerplate phrases are deprioritized or removed from shortlist.
- Updated aggregate sorting priority to tier and index-worthiness score,
  then reference/page coverage and YAKE score.

### Python command policy update
- Updated `AGENTS.md` environment guidance to explicitly require the bootstrap pattern
  `source source_me.sh && python ...` for repo Python commands and to avoid hard-coded
  `/opt/homebrew/opt/python@3.12/bin/python3.12` in routine run commands.
- Updated `docs/PYTHON_STYLE.md` Python execution examples to use
  `source source_me.sh && python ...`.
- Updated `docs/REPO_STYLE.md` scripts section to codify the same bootstrap command pattern for
  repo-local Python usage.
- Updated `source_me.sh` to check for `BASH_VERSION`, print `use bash for your shell`, and exit
  early for all non-bash shells before sourcing `.bashrc`.

## 2026-02-14

### Chapter 7 enrichments
- Enriched Chapter 7.2 Common mistakes (618 to 790 lines) by cross-referencing
  PG_COMMON_PITFALLS.md. Added: local vs my comparison for PGML visibility (expanded scoping
  table to 3 rows), answer field naming section (ans_rule/ANS mismatch), RDKit SMILES chemistry
  errors (imidazole formal charge pitfall), four debugging strategies (check line numbers, binary
  search PGML blocks, minimal example, renderer output), prevention checklist (12 items), and
  'open' trapped error to the quick reference table. Added colgroup tags to all three tables.

### Chapter 7 rewrites
- Rewrote Chapter 7.0 Index (116 lines) with a symptom-based "What just went wrong?" decision
  table mapping common failure symptoms to sections, a section map table with one-line descriptions
  of all six subsections (7.1 through 7.6), and a "Start here" guide directing new users to 7.1,
  broken-problem users to 7.2, and pre-publish users to 7.5.
- Rewrote Chapter 7.1 Setting up and first render (167 lines) as a beginner-friendly setup
  quickstart with a lab-workflow analogy, container startup steps (Podman/Docker), health check
  verification, working-vs-broken diagnostic table, browser editor walkthrough, private folder
  workflow, debugging discipline ("the one rule that saves hours"), a "what to record" table for
  reproducibility, an eight-step first render checklist, and guidance that HTML render is the
  primary test.
- Rewrote Chapter 7.2 Common mistakes and how to fix them (618 lines) as the centerpiece
  debugging reference. Covers PGML parsing errors (asterisks/bold around variables, bullet
  ambiguity), variable scoping (my keyword invisibility with symbol table explanation), HTML
  escaping ([$var]* rule), missing macros (symptom table for DropDown/RadioButtons/DataTable/
  NchooseK), use statement trapping, blocked HTML tags (niceTables.pl alternative), MODES
  misuse (returns 1 in eval context), order of operations (define-before-use, shuffle timing,
  hash key determinism), Perl-in-PG gotchas (backslash references broken, loops in BEGIN_TEXT),
  and a 15-row quick reference error message lookup table. Content sourced from
  PG_COMMON_PITFALLS.md and PGML_LINTER_EXPECTATIONS.md.
- Rewrote Chapter 7.3 Linting your problems (182 lines) with static checks table (PGML tag
  wrappers in variables, HTML without *, MODES in eval blocks, TeX color macros, blocked HTML
  tags, ordered list label patterns), structural checks table (DOCUMENT/ENDDOCUMENT, BEGIN/END
  PGML matching, eval block balance), renderer-based lint workflow using lint_pg_via_renderer_api.py
  with -r and -s flags, and a seven-step lint workflow. Content sourced from
  PGML_LINTER_EXPECTATIONS.md and HOW_TO_LINT.md.
- Wrote Chapter 7.4 Testing randomization and edge cases (183 lines) covering seed-sweep
  methodology, five guard patterns (zero denominators with non_zero_random, repeated values,
  invalid domains, sorted hash keys, shuffle-after-define), boundary value testing for biology
  domains (concentrations, probabilities, pH, rates, percentages), and a six-row checklist table
  of common randomization failures. Content sourced from RANDOMIZATION_REFERENCE.md and
  PG_COMMON_PITFALLS.md.
- Wrote Chapter 7.5 QA checklist before publishing (203 lines) with two checklists adapted from
  PG_COMMON_PITFALLS.md and WEBWORK_PROBLEM_AUTHOR_GUIDE.md. Prevention checklist table (12 rows)
  covers code-level checks (variable definition order, my keyword on PGML variables, backslash
  references, use statements, asterisk parsing, HTML variable syntax, loops in BEGIN_TEXT, hash key
  sorting, shuffle timing, blocked HTML tags, required macros, DOCUMENT/ENDDOCUMENT). Author
  checklist table (9 rows) covers student-facing checks (multiple variants, question-grader
  agreement, correct/wrong answer testing, edge cases, course-local dependencies, inline
  evaluators, solution block, units/rounding). Includes debugging note template, "ready to
  publish" criteria, and quick sanity test.
- Wrote Chapter 7.6 Scripting and automation (220 lines) condensed from the old Chapter 7.2 API
  documentation. Covers API endpoints table (/, /render-api, /health), parameter precedence with
  table (problemSourceURL > problemSource > sourceFilePath), curl example with form-encoded POST,
  Python render function with error/warning reporting, batch linting pattern using os.walk,
  response format table (renderedHTML, flags.error_flag, debug.pg_warn, answers), and success
  checking code pattern. Written for advanced users comfortable with command-line tools.

### Structural changes
- Renamed Chapter 7 folder from `07_Local_Testing_with_webwork_pg_renderer` to
  `07_Testing_and_Debugging` to reflect the broader scope of the rewritten chapter.
- Renamed `7.1-Quickstart_and_editor_workflow.html` to `7.1-Setting_up_and_first_render.html`,
  `7.2-API_usage_for_scripts.html` to `7.2-Common_mistakes_and_how_to_fix_them.html`, and
  `7.3-Testing_habits_and_troubleshooting.html` to `7.3-Linting_your_problems.html`.
- Added three new files: `7.4-Testing_randomization_and_edge_cases.html`,
  `7.5-QA_checklist_before_publishing.html`, and `7.6-Scripting_and_automation.html`.
- Updated `Textbook/TEXTBOOK_PAGE_SUMMARIES.md` with new Chapter 7 section covering all seven
  pages (7.0 through 7.6) with updated folder paths, file names, and three-sentence summaries.
- Total chapter size grew from approximately 640 lines (4 pages) to approximately 1,690 lines
  (7 pages), with content sourced from PG_COMMON_PITFALLS.md, PGML_LINTER_EXPECTATIONS.md,
  RANDOMIZATION_REFERENCE.md, WEBWORK_PROBLEM_AUTHOR_GUIDE.md, PG_2_17_RENDERER_MACROS.md,
  and HOW_TO_LINT.md.

## 2026-01-28

### Content expansion (high-priority pages)
- Expanded Chapter 2.2 OPL header from 88 to 360 lines with comprehensive TITLE/DESCRIPTION/KEYWORDS guidance,
  biology-appropriate DBsubject classification table and decision tree, good vs bad examples for each field,
  three complete worked headers (dilution, genetics, pathway), and common mistakes section.
- Expanded Chapter 6.3 Matching from 62 to 483 lines with detailed PopUp widget usage, three MODES layout patterns
  (preferred direct-in-PGML, eval-block wrapper, inline segments), shuffle array explanation, CSS flexbox styling,
  colored label `[$var]*` pattern, three biology examples (chemical bonds, pathway enzymes, genetics terms), and
  five common failures with symptoms/causes/fixes/prevention.
- Expanded Chapter 2.5 Common PG Macros from 296 to 497 lines with macro version comparison tables (parser widgets,
  core macros, context macros) showing ADAPT/renderer PG 2.17 subset vs full PG 2.17+ vs PG 2.20, "What this means
  for problem authors" section explaining CheckboxList unavailability and RadioButtons-per-statement workaround,
  "When a macro is missing" section with symptoms/diagnosis/workarounds, and prevention tips.
- Expanded Chapter 4.2 OPL Header from 82 to 207 lines with five-section structure explanation (acknowledging OPL
  header as "section zero"), classification decision guide table for different biology problem types (dilution,
  enzyme kinetics, genetics, cell biology, molecular biology), quick reference for each header field with
  cross-references to Chapter 2.2 for detailed guidance, and common mistakes in problem context.
- Expanded Chapter 7.2 API usage from 84 to 448 lines with complete endpoint documentation (POST /, POST /render-api,
  GET /health), detailed parameter precedence (problemSourceURL > problemSource > sourceFilePath), four curl examples
  (form-encoded, JSON, HTML output, instructor mode), Python batch rendering example with requests library, lint
  workflow for checking multiple files in CI/CD, response format documentation with field table, three common use
  cases (lint checks, preview generation, regression testing), and cross-references.
- Total content expansion: Added approximately 1,300 lines across five high-priority pages with biology examples,
  failure modes, decision trees, and comprehensive cross-referencing.

### Structural changes
- Added Chapter 2 OPL header page (2.2), renumbered Chapter 2 files, and updated the PG skeleton,
  section map, and macro guidance to reflect five sections and the PG 2.17 subset.
- Added Chapter 4 OPL header page (4.2), renumbered the remaining Chapter 4 sections, and updated
  the full-file and workflow pages to include OPL header guidance.
- Rebuilt Chapter 6 as Advanced PGML Techniques with new sections on coloring, niceTables,
  matching (MODES guidance), multiple-choice statements, and randomization, removing the old
  subject-specific Chapter 6 pages.
- Added the renderer API usage page (7.2), renumbered testing habits to 7.3, and updated Chapter 7
  pages to mention /health checks and the private/ workflow.
- Simplified the appendices to 90.1 minimal templates (with OPL headers), 90.2 glossary, and 90.3
  troubleshooting checklist, removing the macro cheat sheet and advanced patterns appendix.
- Updated `Textbook/01_Introduction/1.0-Index.html` to note the PG 2.17 subset, macro allowlist
  reference, and the five-section worked example wording.
- Updated `docs/AI_AGENT_READING_LIST.md` to use repo-style Markdown links and sentence-case
  headings for consistency.
- Clarified MODES usage guidance: use `MODES(HTML => ...)` not `MODES(TeX => '', HTML => ...)` since
  we never care about TeX output; MODES is only required when wrapper HTML must be emitted from inside
  Perl eval blocks (e.g., divs wrapping join() expressions in matching layouts), and wrapper tags
  should be written directly in PGML when possible to avoid MODES; use `[$var]*` for simple HTML
  variables instead of MODES.
- Folded MODES explanation into Chapter 6.3 Matching (removed separate 6.1 MODES section) since
  matching problems are the primary use case where MODES is required; renumbered Chapter 6 sections:
  6.1 Coloring (was 6.2), 6.2 Tables (was 6.3), 6.3 Matching with MODES (was 6.4), 6.4 MC statements
  (was 6.5), 6.5 Randomization (was 6.6).
- Refined MODES guidance based on real problem testing: MODES is only needed for flexbox wrapper HTML
  inside eval blocks (e.g., `<div class="two-column"><div>` wrapping join() expressions) where
  removing MODES causes HTML to be escaped and layout to collapse; MODES is NOT needed for subscripts,
  superscripts, charge labels, colored choices, canvas HTML, or other plain HTML that renders fine
  (examples from chemical_group_pka_forms.pgml and macromolecule_identification.pgml).
- Restructured Chapter 6 from "Subject-Specific Applications" to "Advanced PGML Techniques" to focus on
  MODES wrappers, CSS-based text coloring, niceTables.pl for structured data, comprehensive matching problem
  patterns with PopUp widgets and flexbox layouts, multiple choice statements using RadioButtons per statement,
  and advanced randomization patterns.
- Reordered Chapter 6 sections to put MODES first (6.1) as the foundational method before coloring text (6.2),
  since MODES is the recommended approach for HTML-only output that other techniques build upon.
- Integrated biology-specific examples directly into Chapter 6 sections (dilution tables in 6.3, pathway
  matching in 6.4, qPCR randomization in 6.6) rather than maintaining a separate appendix for worked examples.
- Minimized appendices to quick-reference material only: 90.1 Minimal templates, 90.2 Glossary, 90.3
  Troubleshooting checklist (removed separate worked examples section 90.6).
- Added OPL header coverage throughout the textbook acknowledging the five-section reality (OPL Header,
  Preamble, Setup, Statement, Solution) versus the traditional four-section model, with new section 2.2 OPL
  header and metadata covering TITLE, DESCRIPTION, KEYWORDS, DBsubject/DBchapter/DBsection, and attribution
  fields.
- Renumbered Chapter 2 sections to accommodate OPL header: 2.2 OPL header (new), 2.3 PG Problem Files
  (was 2.2), 2.4 Sections within a PG question (was 2.3), 2.5 Common PG Macros (was 2.4), 2.6 Legacy PG
  (was 2.5).
- Updated Chapter 4 to show five-section structure including new 4.2 OPL Header section for the worked
  example, renumbering subsequent sections: 4.3 Preamble (was 4.2), 4.4 Setup (was 4.3), 4.5 Statement
  (was 4.4), 4.6 Solution (was 4.5), 4.7 Putting it together (was 4.6).
- Updated Appendix 90.1 templates to include complete OPL headers with placeholder metadata values.
- Updated Chapter 7 to reflect webwork-pg-renderer changes: added GET /health endpoint coverage, POST / as
  primary endpoint with POST /render-api compatibility, private/ folder workflow, and new 7.2 API usage
  section for programmatic rendering with parameter precedence guidance, renumbering 7.3 Testing habits
  (was 7.2).
- Added PG 2.17 subset scope notes throughout the textbook (Chapters 1.0, 1.1, 2.5, 6.0, 7.0) documenting that
  this guide is based on the flattened PG macro tree in ADAPT and webwork-pg-renderer with some macros
  unavailable (parserCheckboxList.pl, VectorListCheckers.pl), and referencing Chapter 2.5 as the macro
  allowlist.
- Added macro version comparison documentation in `docs/PG_MACRO_VERSION_COMPARISON.md` showing macro
  availability across ADAPT/renderer subset, full PG 2.17+, and PG 2.20, with notes on commonly missing
  macros (parserCheckboxList.pl, VectorListCheckers.pl) and workarounds.
- Updated Chapter 2.5 (Common PG Macros) to include version comparison table reference.
- Created `docs/TEXTBOOK_MIGRATION_GUIDE.md` documenting all file renames, new files, and content migration
  needed to implement the restructured textbook plan.
- Created `docs/AI_AGENT_READING_LIST.md` providing a prioritized reading list for AI agents implementing
  the textbook updates, organized by essential files, source content by chapter, implementation phases, and
  quality checks.
- Updated `Textbook/TEXTBOOK_PAGE_SUMMARIES.md` to reflect all structural changes: new Chapter 6 structure,
  minimized appendices, OPL header section, renumbered Chapter 2/4/7 sections, updated Chapter 7 for renderer
  changes, macro version comparison, and added PG 2.17 subset notes.
- Documented that niceTables.pl is the only supported way to create tables since HTML table tags (table, tr,
  td, th) are blocked in this install, and that TeX color commands do not work reliably so CSS-based styling
  via MODES wrappers is required.

## 2026-01-15
- Added `tools/pglint.py` to lint PG files by posting to the renderer HTTP API, with optional JSON
  payload templates and pyflakes-style issue output.
- Updated `tools/pglint.py` defaults to use `/render-api` with `_format: json` and adjusted error
  handling so non-200 responses report a lint error instead of a protocol failure.
- Expanded `tools/pglint.py` to detect renderer JSON warning fields, scan rendered HTML for warning
  blocks, and optionally base64-encode `problemSource` to match the UI payload.
- Simplified `tools/pglint.py` to a seed-and-host CLI, hardcoding the UI-style JSON payload and
  writing all lint output to stdout for pyflakes-like behavior.
- Added `tests/sample_pgml_problem.pg` as a minimal PGML problem for exercising `pglint.py`.
- Updated `tools/pglint.py` to request JSON responses explicitly and to summarize non-JSON error
  pages instead of printing raw HTML.
- Updated `tools/pglint.py` to strip HTML error pages into readable text when JSON is unavailable.
- Updated `tools/pglint.py` to retry with raw source when base64 JSON renders return 500, and to
  extract `<pre>`/heading error text from HTML error pages.
- Updated `tools/pglint.py` to omit `sourceFilePath` when `problemSource` is provided.
- Updated `tools/pglint.py` to ignore non-alphanumeric HTML snippets and fall back to HTTP status
  when an HTML error page has no readable message.
- Updated `tools/pglint.py` to fall back to form-encoded requests and to treat clean HTML 200
  responses with no warnings as a successful lint.
- Updated `tools/pglint.py` to prefer multipart form-data (UI-style) when JSON renders fail.
- Added a `--debug` flag to `tools/pglint.py` to print request and response details to stderr.
- Added three PG lint fixtures in `tests/` covering missing PGML macros, missing choice macros, and
  a syntax error for pglint validation.
- Added `tests/run_pglint_samples.sh` to exercise the renderer health check and run pglint against
  the sample PG files.
- Updated `tests/run_pglint_samples.sh` so expected-failure samples do not halt the script.
- Updated `tests/run_pglint_samples.sh` to echo the expected error before each failing sample.
- Updated `tools/extract_textbook_pre_blocks.py` to support both simple lint and pglint runs, with
  a full-problem-only option for pglint.
- Updated `tools/pglint.py` to extract line numbers from more warning patterns and to surface
  warning text from HTML <pre> blocks instead of generic placeholders.
- Updated `tools/pglint.py` to request instructor fields and surface `pgcore` source lines when
  available, improving line-level diagnostics.
- Updated `tests/run_pglint_samples.sh` to add spacing and headers for readability.
- Updated `tools/pglint.py` to keep non-debug output concise by filtering generic render lines.
- Updated `tools/pglint.py` to suppress source-line dumps and low-signal warning fragments in
  non-debug output.
- Updated `tools/pglint.py` to suppress empty source-line markers and trimmed debug output from
  the sample runner.
- Updated `tools/pglint.py` to unescape HTML entities in error messages for cleaner debug output.
- Updated `tests/run_pglint_samples.sh` to accept an optional `--debug` flag and pass it through to
  pglint.
- Updated `tools/extract_textbook_pre_blocks.py` to use a single `--mode` switch that runs simple
  lint on all blocks or pglint on full problems only.
- Updated `tests/run_pglint_samples.sh` to report and exit when the renderer health check fails.

## 2026-01-14
- Added `tools/webwork_simple_lint.py` for a lightweight static lint pass on .pg files (macro coverage, balanced markers, PGML blank assignment hints).
- Added `tools/extract_textbook_pre_blocks.py` to extract `<pre>` blocks into .pg files and optionally run the simple lint pass.
- Added `tools/textbook_code_block_validator.py` to scan `<pre>` blocks for unmatched PG/PGML markers and likely missing macro loads.
- Fixed PGML syntax in Chapter 4 Solution examples: changed math delimiters `` [`$radio->correct_ans`] ``
  to variable substitution `[$radio->correct_ans]` in `4.1-Full_file.html` and `4.5-Solution.html`.
- Added "Math formatting vs variable substitution" section to `3.1-Introduction_to_PGML.html` explaining
  when to use backticks (math) vs plain brackets (variable values) with a common mistake example.
- Added required `niceTables.pl` macro documentation to `3.4-Tables_and_structured_data.html` with
  a loadMacros example and a missing-macro failure case.
- Clarified MathObjects.pl requirement in `2.4-Common_PG_Macros.html`: it is needed for Real(),
  Compute(), Formula(), or Context() but not required for RadioButtons or CheckboxList problems.
- Updated `tests/check_ascii_compliance.py` to replace U+037C, U+2264, U+2004, and U+2005 with ASCII equivalents and to drop U+200E.
- Added replacements in `tests/check_ascii_compliance.py` for U+FEFF and common emoji to ASCII words.
- Removed the default emoji word replacements in `tests/check_ascii_compliance.py` so emoji are handled case by case.
- Added an emoji count warning to `tests/run_ascii_compliance.py` to flag emoji for manual handling.

## 2026-01-13
- Updated `docs/LIBRETEXTS_HTML_GUIDE.md` with Construction Guide-derived rules for headings, links,
  templates, titles, tables, images, and embedded media.
- Moved and expanded the internal-link guidance in `docs/LIBRETEXTS_HTML_GUIDE.md` into a dedicated
  section after Core rules, including a repeatable page-id workflow and a small CSV lookup helper.
- Refined the external-link guidance in `docs/LIBRETEXTS_HTML_GUIDE.md` to emphasize in-library
  links first and to allow sparse, stable scholarly outbound links while avoiding "link farming".
- Updated `AGENTS.md` and the HTML lint checker so internal LibreTexts links are allowed while
  relative file links are still flagged as errors.
- Added `docs/READING_JSON_MAP_FILE.md` and `tools/libretexts_map_json_to_page_id_csv.py` to
  document and extract LibreTexts section label to `page_id` mappings from a Remixer map JSON.
- Updated the map parser script to fix section label parsing, add `-i/-o` flags, default the
  output filename from the input, and put `page_id` as the first CSV column.
- Generated `Textbook/Using_WeBWork_in_ADAPT-Map.csv` from the map JSON and added internal
  `/@go/page/<page_id>` links across chapter index and workflow pages using those ids, plus an
  internal-linking note in `docs/LIBRETEXTS_HTML_GUIDE.md`.
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
  stronger "where to focus first" cues across sections 1.0 to 1.6.
- Strengthened Chapter 2 guidance with reassurance, explicit failure modes, and a refactored
  2.4 macros page that separates always-load, interaction-specific, and legacy macros plus a safe
  removal checklist, and added a PopUp warning to 2.5.
- Expanded Chapter 2.4 with science-native contexts, grading helpers, and visual tools while
  keeping the minimal macro set and safe removal checklist front and center.
- Added a Chapter 7 row to the Chapter 1 index "Where to start today" table for local debugging.
- Added instructor-focused reassurance and guardrails across Chapter 3 pages (PGML intro, blanks,
  lists, tables, layout controls, and command substitution) plus a clarity-first wrap-up on the
  chapter index.
- Added Chapter 3 "Use this when" guidance and short "Common failure and fix" micro examples,
  plus instructor-facing additions for PGML notation, text answers, lists, tables, layout, and
  command substitution.
- Added instructor-facing decision support and common failure guidance across Chapter 5 question
  type pages, plus sharper workflow testing advice on the QA page.
- Reorganized Chapter 3 into a task-first menu with quick patterns on the index, standardized
  top-of-page "Use this when / Copy and edit / Common failure and fix" blocks, and added
  next-step guidance at the bottom of each PGML subsection.
- Reworked Chapter 2 into a task-first PG scaffolding guide with standardized top layouts, a
  reusable minimal skeleton in 2.2, a navigation-focused 2.3, a symptom-based macro reference in
  2.4, and a legacy-code safety rail in 2.5.
- Added references to official OpenWeBWorK PG sample problems in Chapter 5 examples for each
  interaction type.
- Linked Chapter 5 official example references directly to the OpenWeBWorK pg-docs pages,
  including matching macro docs and the problem techniques index for ordering.
- Updated the HTML lint checker to allow external links while still flagging internal or
  relative links.
- Expanded Chapter 7 with instructor-facing guidance: a local-vs-ADAPT decision table and
  prerequisites in 7.0, a first-run checklist plus "what to record" table and done criteria in
  7.1, and triage steps with common-failure patterns and a debugging note template in 7.2.
- Expanded the README external resources list with official OpenWeBWorK PG sample example links
  used in Chapter 5.
- Added official OpenWeBWorK sample URLs (MultipleChoicePopup, MultipleChoiceRadio, Multianswer,
  NumericalTolerance, Matching) and the PGchoicemacros reference to the external links lists.
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
- Updated `AGENTS.md` authoring constraints to allow external HTML links while prohibiting internal
  textbook links that could break in LibreTexts.
