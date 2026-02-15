# Changelog

## 2026-02-15

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
