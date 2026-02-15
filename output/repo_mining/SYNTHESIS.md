# Content Mining Synthesis

## Summary Statistics

| Metric | Value |
|--------|-------|
| Repos analyzed | 8 |
| Mining reports produced | 8 |
| Total report lines | 2,411 |
| Total .pg files across all repos | ~81,734 (72,734 OPL + 8,963 training set + 37 biology-problems) |
| Distinct macros cataloged | 260+ (from OPL) / 130+ shipped with renderer |
| PG macro source files documented | 161 (from PG v2.17 macro catalog) |
| Sample problems in PG repo | 157 |
| Lint plugins cataloged | 44 (from linter repo) |
| QTI question types documented | 7 (from qti_package_maker) |
| Top recommended files across all repos | 80+ specific files cited |

## Per-Chapter Findings

### Chapter 1: Introduction

**Contributing repos**: webwork-open-problem-library, qti_package_maker, biology-problems-website, pg_v2_17, webwork-pgml-opl-training-set, webwork-pg-renderer

**Aggregated findings**:

- **OPL scale and structure**: The Open Problem Library contains 72,734 .pg files from 60+ institutions, organized under OpenProblemLibrary/ (37,692), Contrib/ (28,074), and Pending/ (6,968). The DBsubject/DBchapter/DBsection taxonomy covers 109 normalized subjects, 559 chapters, and 1,952 sections. 95.6% of files have metadata classification. This provides the "how big is WeBWorK" narrative for Ch1.
  - Source: `webwork-open-problem-library/output/summary/` (TSV files)

- **PGML vs legacy adoption**: Only 24.9% of OPL files (18,075/72,734) use PGML.pl. The training set is a 100%-PGML subset of 8,963 files. The textbook should clearly recommend PGML for all new problems while acknowledging the legacy base.
  - Source: `webwork-open-problem-library/output/summary/corpus_profile*.tsv`
  - Source: `webwork-pgml-opl-training-set/output/` (analysis results)

- **WeBWorK vs other formats comparison**: qti_package_maker provides an engine capability matrix comparing QTI v1.2 (Canvas/ADAPT), QTI v2.1 (Blackboard), BBQ text, and HTML selftest. Key WeBWorK advantages: unlimited question types, server-side rendering (avoids JS/HTML rendering failures across LMS platforms), randomization, custom grading logic, programmatic generation. Canvas QTI v1.2 cannot import FIB or ORDER types; text2qti cannot handle MATCH, MULTI_FIB, or ORDER.
  - Source: `qti_package_maker/docs/ENGINES.md` (capability matrix)
  - Source: `qti_package_maker/TEMP_RDKit_QTI_IMPORT_NOTES.md` (platform compatibility)

- **PG system basics**: PGstandard.pl loads five core macros: PG.pl, PGbasicmacros.pl, PGanswermacros.pl, PGauxiliaryFunctions.pl, customizeLaTeX.pl. Understanding this loading chain is essential for Ch1.
  - Source: `PG_v2.17/macros/core/PGstandard.pl`

- **Standalone renderer motivation**: The renderer provides line-level error reporting that ADAPT cannot. It supports fast iteration before importing into ADAPT.
  - Source: `webwork-pg-renderer/README.md`, `webwork-pg-renderer/docs/USAGE.md`

- **Minimum viable PGML problem**: The FortLewis authoring templates provide canonical "hello world" examples showing DOCUMENT/loadMacros/Context/BEGIN_PGML/END_PGML/ENDDOCUMENT.
  - Source: `webwork-pgml-opl-training-set/problems/OpenProblemLibrary/FortLewis/Authoring/Templates/`

- **Real-world OER context**: The biology-problems-website demonstrates the end-to-end pathway from question creation to LibreTexts ADAPT deployment, funded by an Illinois State Library OER Grant.
  - Source: `biology-problems-website/site_docs/index.md`

---

### Chapter 2: Problem Generation (PG)

**Contributing repos**: pg_v2_17, webwork-pgml-opl-training-set, webwork-open-problem-library, biology-problems, webwork-pgml-linter

**Aggregated findings**:

- **Macro frequency data** (from OPL corpus, most important for prioritizing what to teach):
  - PGstandard.pl: 59,503 files (82%)
  - PGcourse.pl: 52,620 (72%)
  - MathObjects.pl: 48,691 (67%)
  - PGchoicemacros.pl: 31,314 (43%) -- legacy but still dominant
  - PGML.pl: 18,075 (25%)
  - PGgraphmacros.pl: 8,908 (12%)
  - parserPopUp.pl: 7,964 (11%)
  - parserMultiAnswer.pl: 6,962 (10%)
  - parserRadioButtons.pl: 6,578 (9%)
  - Source: `webwork-open-problem-library/output/summary/` (macro usage TSV)

- **Complete MathObject type system** (from PG v2.17): Real, Complex, Point, Vector, Matrix, Interval, Set, Union, Formula, String, List. Context system controls tolerance, formatting, and allowed operations. `Compute()` vs type constructors, `->cmp()` for answer checking, `->eval()`, `->TeX`, `->reduce`, `->substitute`.
  - Source: `PG_v2.17/lib/Value.pm`, `PG_v2.17/doc/UsingMathObjects.pod`, `PG_v2.17/doc/MathObjectsAnswerCheckers.pod`

- **OPL header metadata format** (validated by linter): DBsubject, DBchapter, DBsection, KEYWORDS (3-10 entries, no duplicates), DESCRIPTION/ENDDESCRIPTION blocks. The linter has 20+ validation checks for header quality.
  - Source: `webwork-pgml-linter/pgml_lint/plugins/pgml_header_tags.py` (282 lines of validation rules)
  - Source: `biology-problems/` (biology-specific taxonomy: Biochemistry > Chemical Properties > Isoelectric Point)
  - Source: `webwork-pgml-opl-training-set/problems/Contrib/PCC/` (math taxonomy examples)

- **loadMacros() syntax and common errors** (from linter): Missing commas between entries, smart quotes, missing closing parenthesis, empty macro list. The linter's loadmacros_integrity plugin catches these.
  - Source: `webwork-pgml-linter/pgml_lint/plugins/pgml_loadmacros_integrity.py` (223 lines)

- **Legacy-to-modern migration patterns** (from linter): 7 plugins detect deprecated patterns: ans_rule() -> PGML inline blanks, $BR -> blank lines, BEGIN_TEXT -> BEGIN_PGML, SOLUTION()/HINT() macros -> BEGIN_PGML_SOLUTION/BEGIN_PGML_HINT, ANS() calls -> inline answer specs, old answer checkers (num_cmp/str_cmp/fun_cmp) -> MathObjects ->cmp().
  - Source: `webwork-pgml-linter/pgml_lint/plugins/pgml_ans_rule.py`, `pgml_br_variable.py`, `pgml_text_blocks.py`, `pgml_solution_hint_macros.py`, `pgml_ans_style.py`, `pgml_old_answer_checkers.py`

- **Context system catalog** (from PG v2.17): 50 context macros including Fraction, Reaction (chemistry), Boolean (logic), BaseN (CS), Percent, ScientificNotation, Ordering, Currency, Inequalities, LimitedPolynomial, and many more. Each defines a specialized math environment.
  - Source: `PG_v2.17/macros/contexts/` (50 files)

---

### Chapter 3: PGML (PG Markup Language)

**Contributing repos**: pg_v2_17, webwork-pgml-opl-training-set, biology-problems, webwork-pgml-linter

**Aggregated findings**:

- **Complete PGML syntax reference** (from PG v2.17 parser source): Answer blanks (`[_]{$ans}`, `[_]{$ans}{width}`, `[____]{$ans}`, `[_]*{$ans}` for arrays, `[^]{$radio}`, `[o]{$popup}`), math mode (`` [`...`] `` inline, `` [``...``] `` display), bold/italic (`*text*`, `**text**`, `***bold italic***`), headings (`#`, `##`), lists (bullet `-`, numbered `1.`, roman/alpha), code blocks (` ``` `), preformatted (`:   `), alignment (`>>`, `<<`), images (`[!alt!]{url}`), command substitution (`[@ perl @]`, `[@ perl @]*` raw HTML, `[@ perl @]***` LaTeX-processed), variable substitution (`[$var]`), line breaks (three trailing spaces), rules (`---`, `===`).
  - Source: `PG_v2.17/macros/core/PGML.pl` (the parser regex patterns define the grammar)

- **PGML answer blank pitfalls** (from linter): Missing answer spec (`[_]` alone), empty spec (`[_]{}`), unbalanced braces (`[_]{$ans`), mixed payload and star specs, blank referencing undefined variable.
  - Source: `webwork-pgml-linter/pgml_lint/plugins/pgml_blanks.py`, `pgml_blank_assignments.py`

- **HINT and SOLUTION blocks** (from biology-problems): Real-world examples of `BEGIN_PGML_HINT`/`END_PGML_HINT` and `BEGIN_PGML_SOLUTION`/`END_PGML_SOLUTION`. Only 6.4% of training set files include hints -- the textbook should encourage their use.
  - Source: `biology-problems/isoelectric_one_protein.pgml` (lines 178-207)
  - Source: `webwork-pgml-opl-training-set/` (577 files with hints = 6.4%)

- **DataTable with embedded PGML** (from training set): The `PGML('[_]{$ans}')` wrapper function allows embedding PGML answer blanks inside DataTable cells, creating interactive tables. This is a powerful but barely documented pattern.
  - Source: `webwork-pgml-opl-training-set/problems/Contrib/Fitchburg/Algebra/lines/function-evaluation-1.pg`

- **Inline code block pitfalls** (from linter): Unclosed `[@` without matching `@]`, PGML interpolation `[$name]` inside `[@ @]` blocks (PGML parses once and will not re-parse strings), nested BEGIN_PGML inside `[@ @]`, unbalanced braces in inline code.
  - Source: `webwork-pgml-linter/pgml_lint/plugins/pgml_inline.py`, `pgml_inline_braces.py`, `pgml_inline_pgml_syntax.py`

- **HTML-to-PGML tag mapping** (from linter): 22 HTML tags with PGML alternatives. `<b>`/`<strong>` -> `**text**`, `<i>`/`<em>` -> `*text*`, `<sub>` -> use LaTeX, `<br>` -> blank line, `<ul>`/`<li>` -> PGML list syntax, etc. Raw HTML in PGML text will be stripped or mangled.
  - Source: `webwork-pgml-linter/pgml_lint/plugins/pgml_html_in_text.py` (161 lines, 22 tag mappings)

- **TeX color commands do not work in PGML** (from linter): `\color`, `\textcolor` do not render reliably. Use PGML tag wrappers or HTML spans with `[@ @]*` instead.
  - Source: `webwork-pgml-linter/pgml_lint/plugins/pgml_tex_color.py`

---

### Chapter 4: Breaking Down the Components

**Contributing repos**: webwork-pgml-opl-training-set, pg_v2_17, biology-problems, webwork-pgml-linter, webwork-pg-renderer

**Aggregated findings**:

- **Standard file anatomy** (from training set + PG v2.17): The canonical four-section structure is: (1) Description block + OPL metadata, (2) DOCUMENT() + loadMacros() + Context/setup, (3) BEGIN_PGML statement, (4) BEGIN_PGML_SOLUTION + ENDDOCUMENT(). Section dividers using `###########################` comment lines are common in OPL.
  - Source: `webwork-pgml-opl-training-set/problems/Contrib/PCC/BasicAlgebra/` (comprehensive examples)
  - Source: `PG_v2.17/tutorial/sample-problems/` (157 sample problems)
  - Source: `biology-problems/` (numbered comment headers: `###### 1 PREAMBLE`, `###### 2 SETUP`, etc.)

- **Function-to-macro mapping table** (from linter): The linter's macro_rules plugin contains the canonical mapping of PG functions to required macro files. RadioButtons requires parserRadioButtons.pl, CheckboxList requires parserCheckboxList.pl, DataTable/LayoutTable requires niceTables.pl, Context/Compute/Formula require MathObjects.pl, etc.
  - Source: `webwork-pgml-linter/pgml_lint/function_to_macro_pairs.py`
  - Source: `webwork-pgml-linter/pgml_lint/rules.py`

- **Function signature reference** (from linter): The linter validates 16 PG functions with exact argument counts. `random()` requires exactly 3 args (min, max, step), `NchooseK()` requires exactly 2, `Compute()` requires at least 1. Typo detection: Popup -> PopUp, Dropdown -> DropDown, Radiobuttons -> RadioButtons, Checkboxes -> CheckboxList.
  - Source: `webwork-pgml-linter/pgml_lint/plugins/pgml_function_signatures.py` (261 lines)

- **Randomization and data pools** (from biology-problems): Helper functions (`random_choice`, `shuffle_list`, `sample_unique`) for managing large data pools (50-350+ items). Retry-loop pattern for constrained randomization: `for my $attempt (1 .. $max_attempts) { ... next if invalid; ... last; }`. PGrandom vs global `random()` for seed stability.
  - Source: `biology-problems/electrophoresis/protein_gel_migration.pgml` (lines 95-123, helper functions; lines 290-335, retry loop)
  - Source: `biology-problems/PUBCHEM/macromolecule_identification.pgml` (358-entry data pool)

- **Render pipeline** (from renderer): POST request -> Controller validates inputs -> Problem model instantiated -> RenderProblem::process_pg_file invokes WeBWorK::PG -> FormatRenderedProblem returns HTML + JSON metadata. Understanding this pipeline helps authors debug rendering issues.
  - Source: `webwork-pg-renderer/docs/CODE_ARCHITECTURE.md`, `webwork-pg-renderer/lib/RenderApp/Controller/Render.pm`

---

### Chapter 5: Different Question Types

**Contributing repos**: pg_v2_17, webwork-pgml-opl-training-set, biology-problems, webwork-open-problem-library, webwork-pgml-linter, qti_package_maker

**Aggregated findings**:

- **Question type frequency** (from OPL, guides prioritization): Numeric entry: 44,575 files (most common), Multiple choice: 37,516, Multipart: 30,828, Graph-like: 8,908, Fill-in-blank (word): 3,619, Assignment/ordering: 1,616, Essay: 564, Matching: 189.
  - Source: `webwork-open-problem-library/output/summary/` (question type distribution)

- **RadioButtons** (comprehensive coverage from all repos): Constructor with randomization groups, labels (ABC/123), displayLabels, separator HTML, values. 1,924 files in training set (21.5%), 6,578 in full OPL.
  - Source: `PG_v2.17/macros/parsers/parserRadioButtons.pl` (complete POD docs)
  - Source: `biology-problems/isoelectric_one_protein.pgml` (lines 166-173, full constructor)

- **CheckboxList** (underrepresented -- needs more coverage): Only 16 files in training set, 1,741 in full OPL. Multi-select with randomized choices, labels ABC/123/roman. The textbook should give this extra coverage precisely because it is underrepresented.
  - Source: `PG_v2.17/macros/parsers/parserCheckboxList.pl`
  - Source: `webwork-pgml-opl-training-set/problems/OpenProblemLibrary/Valdosta/APEX_Calculus/3.1/APEX_3.1_6.pg`

- **DropDown/PopUp** (from PG v2.17 + training set): PopUp(), DropDown(), DropDownTF() with placeholder support, useHTMLSelect option, showInStatic. 2,344 files in training set (26.2%).
  - Source: `PG_v2.17/macros/parsers/parserPopUp.pl`
  - Source: `biology-problems/matching_sets/bond_types-matching.pgml` (DropDown/PopUp compatibility wrapper)

- **MultiAnswer** (from PG v2.17): Multiple interdependent answer blanks with custom checker function. singleResult option, partialCredit. 1,655 files in training set (18.5%).
  - Source: `PG_v2.17/macros/parsers/parserMultiAnswer.pl`

- **DraggableProof** (NOT CURRENTLY COVERED in textbook): Drag-and-drop proof ordering with Levenshtein/Damerau-Levenshtein scoring. AllowNewBlanks, NumBuckets, OrderMatters, ResetButtonText options.
  - Source: `PG_v2.17/macros/math/draggableProof.pl`
  - Source: `biology-problems/webwork_examples/ordering_entropy.pgml` (lines 46-52, complete constructor)

- **DraggableSubsets** (NOT CURRENTLY COVERED): Drag-and-drop set partitioning into buckets. Complementary to DraggableProof.
  - Source: `PG_v2.17/macros/math/draggableSubsets.pl`

- **RadioMultiAnswer** (NOT CURRENTLY COVERED): Radio buttons with dependent answer blanks per choice.
  - Source: `PG_v2.17/macros/parsers/parserRadioMultiAnswer.pl`

- **WordCompletion** (NOT CURRENTLY COVERED): Autocomplete text input with datalist suggestions. Only 13 files in training set.
  - Source: `PG_v2.17/macros/parsers/parserWordCompletion.pl`

- **OneOf** (NOT CURRENTLY COVERED): Accept any one of several correct answers: `OneOf(pi, "2x+1")`.
  - Source: `PG_v2.17/macros/parsers/parserOneOf.pl`

- **Scaffold/multi-part** (from training set + PG v2.17): `Scaffold::Begin()` with `is_open` options controlling section visibility. 287 files in training set (3.2%).
  - Source: `PG_v2.17/macros/core/scaffold.pl`
  - Source: `webwork-pgml-opl-training-set/problems/Contrib/Hope/Calc2/APEX_06_01_Substitution/Reading_Q_01.pg`

- **Essay** (from PG v2.17): `essay_cmp()`, `essay_box()`, `explanation_box()` for manual grading.
  - Source: `PG_v2.17/macros/core/PGessaymacros.pl`

- **Matching with partial credit** (from biology-problems): `custom_problem_grader_fluid` with configurable score thresholds. `exclude_pairs` logic for constrained matching.
  - Source: `biology-problems/matching_sets/bond_types-matching.pgml` (lines 134-145)
  - Source: `biology-problems/matching_sets/amino_acids_properties-matching.pgml`

- **Custom HTML radio cards** (from biology-problems, NOT COVERED): Custom UI pattern with hidden ans_rule for radio card interfaces with RDKit rendering.
  - Source: `biology-problems/PUBCHEM/AMINO_ACIDS/histidine_protonation_states.pg`

- **QTI comparison** (from qti_package_maker): Standard LMS formats support only 7 question types (MC, MA, MATCH, NUM, FIB, MULTI_FIB, ORDER) with per-platform gaps. WeBWorK supports all of these plus essay, custom graders, randomized parameters, interactive graphs, drag-and-drop, and unlimited custom types.
  - Source: `qti_package_maker/docs/ENGINES.md`, `qti_package_maker/docs/QUESTION_TYPES.md`

---

### Chapter 6: Advanced PGML Techniques

**Contributing repos**: biology-problems, pg_v2_17, webwork-pgml-opl-training-set, webwork-pgml-linter

**Aggregated findings**:

- **RDKit.js chemistry rendering** (from biology-problems, NOT COVERED): HEADER_TEXT for loading RDKit_minimal.js from unpkg CDN. Canvas-based molecule rendering from SMILES strings. Atom highlighting for protonation states. 8 files in biology-problems use this pattern.
  - Source: `biology-problems/PUBCHEM/rdkit_working_in_webwork.pgml` (lines 27-47, initialization)
  - Source: `biology-problems/PUBCHEM/macromolecule_identification.pgml` (RDKit at scale, 358 SMILES)
  - Source: `biology-problems/PUBCHEM/polypeptide_mc_sequence-easy.pgml` (atom highlighting)

- **Simulated gel electrophoresis** (from biology-problems, NOT COVERED): HTML/CSS absolute positioning to render SDS-PAGE gel bands, wells, and molecular weight markers. Linear gradient backgrounds, band coloring, dynamic positioning.
  - Source: `biology-problems/electrophoresis/kaleidoscope_ladder_unknown_band.pgml` (lines 187-199, build_gel_html)

- **PGgraphmacros static graphs** (from biology-problems + training set): `init_graph()`, `lineTo()`, `stamps()`, `lb()` for labels, `FEQ()`, `plot_functions()`. 1,279 files in training set (14.3%), 8,908 in full OPL.
  - Source: `biology-problems/electrophoresis/titration_pI.pgml` (lines 170-195, titration curve)
  - Source: `PG_v2.17/macros/graph/PGgraphmacros.pl`

- **TikZ image creation** (from PG v2.17 + training set): `createTikZImage()`, `tikzLibraries()`, `tikzOptions()`, `texPackages()`, `BEGIN_TIKZ`/`END_TIKZ`. Only 52 files in training set -- sparse but important.
  - Source: `PG_v2.17/macros/graph/PGtikz.pl`
  - Source: `webwork-pgml-opl-training-set/problems/OpenProblemLibrary/Rochester/setAlgebra10QuadraticEqns/sw3_3_69.pg`

- **LaTeX image creation** (from PG v2.17): `createLaTeXImage()` for general LaTeX-rendered images.
  - Source: `PG_v2.17/macros/graph/PGlateximage.pl`

- **GraphTool interactive graphing** (from biology-problems + PG v2.17, NOT COVERED): Interactive JS graphing tool supporting 12+ object types (points, lines, circles, parabolas, quadratics, cubics, intervals, sine waves, triangles, quadrilaterals, segments, vectors, fills). Custom AnswerEvaluator for point placement.
  - Source: `PG_v2.17/macros/graph/parserGraphTool.pl`
  - Source: `biology-problems/electrophoresis/titration_buffer_graph_tool.pg` (custom checker)

- **plotly3D** (from PG v2.17, NOT COVERED): `Graph3D()`, `addCurve()`, `addFunction()`, `addSurface()` for 3D visualization.
  - Source: `PG_v2.17/macros/graph/plotly3D.pl`

- **niceTables DataTable/LayoutTable** (from PG v2.17 + biology-problems + training set): `DataTable()` with align, horizontalrules, caption, center, encase options. `LayoutTable()` for non-data grids. Header cells with `header => 'ch'` or `header => 'rh'`. 334 files in training set (3.7%).
  - Source: `PG_v2.17/macros/ui/niceTables.pl`
  - Source: `biology-problems/electrophoresis/two_dimensional_gel_spots.pgml` (16x16 LayoutTable grid)
  - Source: `biology-problems/buffers/poisson_flies.pgml` (DataTable for data display)

- **MODES() function** (complex topic -- 4 linter plugins dedicated to it): MODES() inside `[@ @]` returns 1, not HTML. `[$var]` escapes HTML from MODES(); must use `[@ $var @]*` for raw output. TeX payload should be empty for PGML output. HTML payloads without tags should be replaced with plain strings.
  - Source: `webwork-pgml-linter/pgml_lint/plugins/pgml_modes_in_inline.py` (213 lines)
  - Source: `webwork-pgml-linter/pgml_lint/plugins/pgml_modes_tex_payload.py`
  - Source: `webwork-pgml-linter/pgml_lint/plugins/pgml_modes_html_plain_text.py`
  - Source: `webwork-pgml-linter/pgml_lint/plugins/pgml_modes_html_escape.py`

- **HEADER_TEXT for CSS/JS injection** (from biology-problems): Pattern for injecting `<script>` and `<style>` tags into the page head. Used by 12 biology-problems files for RDKit.js, custom CSS layouts, and gel simulations.
  - Source: `biology-problems/PUBCHEM/rdkit_working_in_webwork.pgml` (HEADER_TEXT heredoc)

- **HTML in PGML rules** (from linter): Raw `<table>` tags are forbidden (use DataTable/LayoutTable). Raw `<div>` allowed in PG 2.17 but risky in older versions. `<script>`, `<iframe>`, `<object>`, `<embed>` are ERROR-level. `<style>`, `<form>`, `<input>`, `<img>`, `<svg>` are WARNING-level.
  - Source: `webwork-pgml-linter/pgml_lint/plugins/pgml_html_forbidden_tags.py`
  - Source: `webwork-pgml-linter/pgml_lint/plugins/pgml_html_policy.py`
  - Source: `webwork-pgml-linter/pgml_lint/plugins/pgml_html_div.py`

- **Color rendering** (from biology-problems + linter): 6 color methods compared in `color_render_test.pg`. TeX `\color`/`\textcolor` do not render reliably in PGML. Use PGML tag wrappers or HTML spans with `[@ @]*` instead.
  - Source: `biology-problems/webwork_examples/color_render_test.pg`
  - Source: `webwork-pgml-linter/pgml_lint/plugins/pgml_tex_color.py`

- **Chemical formula HTML** (from biology-problems): Subscript/superscript patterns for chemical formulas using inline HTML.
  - Source: `biology-problems/buffers/pKa_buffer_state-diprotic.pgml` (helper functions for chemical HTML)

- **Two-column flex layouts** (from biology-problems): CSS flexbox for side-by-side content within PGML.
  - Source: `biology-problems/matching_sets/matching_from_web.pgml`

- **Chemical Reaction context** (from PG v2.17 + training set): `Context("Reaction")` with ions, states, complexes. Only 3 files in training set.
  - Source: `PG_v2.17/macros/contexts/contextReaction.pl`
  - Source: `webwork-pgml-opl-training-set/problems/OpenProblemLibrary/FortLewis/Authoring/Templates/Misc/ChemicalReaction1_PGML.pg`

- **answerHints for targeted feedback** (from PG v2.17 + training set): Post-filter for specific wrong-answer messages. 430 files in training set use this pattern.
  - Source: `PG_v2.17/macros/answers/answerHints.pl`

- **weightedGrader** (from PG v2.17 + training set): `install_weighted_grader()` with per-answer weight options. 504 files in training set.
  - Source: `PG_v2.17/macros/answers/weightedGrader.pl`

- **randomPerson for inclusive problems** (from PG v2.17): Random person names with correct pronouns (he/she/they), verb conjugation, diverse name database from SSA/Census data.
  - Source: `PG_v2.17/macros/misc/randomPerson.pl`

- **Label dot PGML parsing trap** (from linter): Labels built as `A.` (chr(65+$i) . '. ') trigger PGML list parsing. Use `*A.*` or `A)` instead.
  - Source: `webwork-pgml-linter/pgml_lint/plugins/pgml_label_dot.py`

---

### Chapter 7: Testing and Debugging

**Contributing repos**: webwork-pgml-linter (PRIMARY), webwork-pg-renderer (PRIMARY), biology-problems, webwork-pgml-opl-training-set

**Aggregated findings**:

- **Linter setup and usage** (from linter repo): `pgml-lint -i file.pg` or `pgml-lint -d problems/`. Supports `--pg-version 2.17`, `--disable`/`--enable` plugin options, JSON configuration files. 44 built-in plugins (43 enabled by default).
  - Source: `webwork-pgml-linter/` (entire repo)
  - Source: `webwork-pgml-linter/docs/PGML_LINT_PLUGINS.md` (1,148 lines, complete reference)

- **Common mistakes catalog** (from linter, 44 plugins organized by category):
  - **Document structure**: DOCUMENT/ENDDOCUMENT pairing, BEGIN/END block markers, block nesting
  - **Macro loading**: Missing PGML.pl for PGML, loadMacros syntax errors, function-to-macro requirements
  - **PGML syntax**: Answer blank specs, inline code balance, bracket/emphasis balance, parse hazards
  - **HTML in PGML**: Forbidden table tags, raw HTML stripping, div rendering, span interpolation, HTML passthrough
  - **MODES() pitfalls**: MODES inside eval context, TeX payload, HTML escape, plain text replacement
  - **Seed/randomization**: rand() bypassing PG seeding, time()/localtime() clock dependency, missing seed variation
  - **Legacy patterns**: ANS() after PGML, ans_rule(), $BR, old answer checkers, SOLUTION()/HINT() macros
  - **Encoding**: Non-breaking spaces, mojibake sequences
  - **Code quality**: Extreme line lengths, embedded blob payloads, label dot parsing traps
  - Source: all 44 plugins in `webwork-pgml-linter/pgml_lint/plugins/`

- **Renderer setup** (from renderer repo):
  - Docker: `docker build --tag renderer:1.0 ./container && docker run -d --rm --name standalone-renderer --publish 3000:3000 ...`
  - Podman compose: `./run.sh` (builds image, starts compose, opens browser, tails logs)
  - Configuration: `render_app.conf` (secrets, baseURL, CORS) + `conf/pg_config.yml` (macro paths, external programs, answer defaults)
  - Health check: `GET /health` returns PG/jQuery/Node versions
  - Source: `webwork-pg-renderer/README.md`, `webwork-pg-renderer/docs/USAGE.md`

- **Renderer API scripting** (from renderer repo):
  - Primary endpoint: `POST /render-api` with `sourceFilePath` or `problemSource` + `problemSeed`
  - Response: `_format=json` returns renderedHTML, debug (perl_warn, pg_warn, internal), problem_result, flags, resources, JWT
  - Error detection pipeline: `flags.error_flag` -> `debug.pg_warn` -> `debug.internal` -> renderedHTML scanning
  - Python scripts: `script/pg-smoke.py` (53 lines, smoke test), `script/lint_pg_via_renderer_api.py` (130 lines, lint + optional HTML render)
  - Perl/Bash scripts: `script/pg-smoke.pl`, `script/smoke.sh`
  - Source: `webwork-pg-renderer/docs/RENDERER_API_USAGE.md`, `webwork-pg-renderer/script/HOW_TO_LINT.md`

- **Seed testing methodology** (from linter):
  - Seed stability: 13 unseeded randomness patterns detected (rand, srand, time, localtime, gmtime, SRAND, ProblemRandomize, PeriodicRerandomization)
  - Seed variation: 35+ randomization function patterns recognized (random, list_random, shuffle, NchooseK, random_subset, etc.)
  - A file with no random() calls triggers warning: "No seed-based randomization detected"
  - Source: `webwork-pgml-linter/pgml_lint/plugins/pgml_seed_stability.py` (97 lines)
  - Source: `webwork-pgml-linter/pgml_lint/plugins/pgml_seed_variation.py` (122 lines)

- **PG version detection** (from biology-problems): Feature probing to detect PG version at runtime. `defined(&GraphTool::new)` -> PG 2.17, `defined(&parser::DropDown::new)` -> PG 2.18+. Macro path inspection via `findMacroFile()`.
  - Source: `biology-problems/webwork_examples/check_pg_version.pg` (lines 29-48)
  - Source: `biology-problems/webwork_examples/check_pg_macro_status_v2.18.pg` (macro availability testing)

- **Environment introspection** (from biology-problems): Dumping envir variables for debugging setup issues. Macro path inspection.
  - Source: `biology-problems/webwork_examples/get_webwork_env_variables.pg`
  - Source: `biology-problems/webwork_examples/get_macro_paths.pg`

- **Renderer error codes** (from renderer): 400 Bad Request, 403 Forbidden, 404 Not Found, 405 Method Not Allowed, 412 Precondition Failed, 500 Internal Server Error. Errors prefixed with `[$request_id]`.
  - Source: `webwork-pg-renderer/lib/RenderApp/Model/Problem.pm`, `webwork-pg-renderer/lib/RenderApp/Controller/Render.pm`

- **JWT workflow for stateful interactions** (from renderer): Three-tier JWT system (problemJWT -> sessionJWT -> answerJWT) enables stateful problem interactions and grade reporting.
  - Source: `webwork-pg-renderer/README.md` (JWT documentation)

- **Custom grading strategies** (from PG v2.17): `full_partial_grader`, `custom_problem_grader_fluid`, weighted scoring via PGgraders.pl.
  - Source: `PG_v2.17/macros/core/PGgraders.pl`

---

### Chapter 8: Using AI Agents to Write WeBWorK

**Contributing repos**: biology-problems, biology-problems-website, webwork-pgml-linter, webwork-pgml-opl-training-set, qti_package_maker

**Aggregated findings**:

- **Script-generated problems** (from biology-problems): The `alpha_amino_acid_identification.pg` file was generated by `amino_acid_radio_card_maker.py` from a YAML input file. This demonstrates the YAML-to-PG pipeline pattern for bulk problem generation.
  - Source: `biology-problems/PUBCHEM/AMINO_ACIDS/alpha_amino_acid_identification.pg` (header comment)

- **Large curated data pools** (from biology-problems): 358-entry macromolecule SMILES database, 58-entry protein bank, 20-entry amino acid set -- likely assembled programmatically and suitable for AI-assisted curation.
  - Source: `biology-problems/PUBCHEM/macromolecule_identification.pgml`
  - Source: `biology-problems/electrophoresis/protein_gel_migration.pgml`

- **Corpus as AI training resource** (from training set): 8,963 PGML-format .pg files represent a curated training corpus for AI problem generation. The `pg_analyze` toolkit demonstrates programmatic analysis of PG files.
  - Source: `webwork-pgml-opl-training-set/` (entire repo, curated for PGML)
  - Source: `webwork-pgml-opl-training-set/pg_analyze/` (analysis toolkit)

- **PG macro POD documentation** (from PG v2.17): Every .pl macro file contains embedded POD documentation that serves as a machine-readable specification. The 157 sample problems provide working templates organized by topic.
  - Source: `PG_v2.17/macros/` (all .pl files with POD)
  - Source: `PG_v2.17/tutorial/sample-problems/` (157 examples)

- **Lint rule creation by AI** (from linter): The plugin development guide documents the registration pattern for creating new lint rules. AI agents can help write custom plugins.
  - Source: `webwork-pgml-linter/docs/PGML_LINT_PLUGIN_DEV.md`

- **LLM-assisted title generation** (from biology-problems-website): `llm_generate_problem_set_title.py` with `llm_wrapper.py` using ollama for generating problem set titles.
  - Source: `biology-problems-website/llm_generate_problem_set_title.py`

- **BBQ batch runner automation** (from biology-problems-website): CSV-driven task runner for bulk question set generation, demonstrating automation patterns.
  - Source: `biology-problems-website/bbq_control/`

- **QTI engine plugin architecture** (from qti_package_maker): BaseEngine with pluggable write_item modules demonstrates modular design patterns for educational tool building.
  - Source: `qti_package_maker/docs/ENGINE_AUTHORING.md`

---

### Chapter 90: Appendices

**Contributing repos**: ALL repos contribute

**Aggregated findings**:

- **Macro reference table** (from PG v2.17 + OPL + linter): Complete catalog of 161+ macros organized by category:
  - Core (15): PGstandard.pl, MathObjects.pl, PGML.pl, scaffold.pl, PGgraders.pl, PGessaymacros.pl, etc.
  - Parsers (30): parserRadioButtons.pl, parserCheckboxList.pl, parserPopUp.pl, parserMultiAnswer.pl, parserGraphTool.pl, etc.
  - Contexts (50): contextFraction.pl, contextReaction.pl, contextBoolean.pl, contextBaseN.pl, contextPercent.pl, etc.
  - Graphing (22): PGgraphmacros.pl, PGtikz.pl, PGlateximage.pl, parserGraphTool.pl, plotly3D.pl, etc.
  - UI (12): niceTables.pl, PGchoicemacros.pl, choiceUtils.pl, quickMatrixEntry.pl, etc.
  - Math-domain (31): draggableProof.pl, draggableSubsets.pl, MatrixReduce.pl, PGstatisticsmacros.pl, etc.
  - Answers (14): answerHints.pl, weightedGrader.pl, answerCustom.pl, unorderedAnswer.pl, etc.
  - Misc (2): randomPerson.pl, PCCmacros.pl
  - Source: `PG_v2.17/macros/` (complete directory tree)

- **Function-to-macro mapping table** (from linter): Canonical mapping of PG functions to required .pl files with PG version requirements.
  - Source: `webwork-pgml-linter/pgml_lint/function_to_macro_pairs.py`

- **FortLewis authoring templates** (from training set): 30 official template files covering every question type, organized by math topic. Ready-made "Starter Templates" appendix.
  - Source: `webwork-pgml-opl-training-set/problems/OpenProblemLibrary/FortLewis/Authoring/Templates/` (30 files)

- **Lint rule quick reference** (from linter): 44 rules with rule ID, error message, severity, and fix. Serves as QA checklist.
  - Source: `webwork-pgml-linter/docs/PGML_LINT_PLUGINS.md` (1,148 lines)

- **OPL taxonomy reference** (from OPL): 109 normalized DBsubject values, full discipline distribution.
  - Source: `webwork-open-problem-library/output/summary/discipline_counts*.tsv`

- **Renderer API parameter reference** (from renderer): Complete parameter tables for render endpoints (required, display, interaction, content parameters).
  - Source: `webwork-pg-renderer/README.md`, `webwork-pg-renderer/docs/RENDERER_API_USAGE.md`

- **Unit catalog** (from PG v2.17): Complete physical unit definitions.
  - Source: `PG_v2.17/lib/Units.pm`

- **Context catalog** (from PG v2.17): All 50 contexts with descriptions.
  - Source: `PG_v2.17/macros/contexts/` (50 files)

- **Color rendering method catalog** (from biology-problems): 6 methods compared.
  - Source: `biology-problems/webwork_examples/color_render_test.pg`

- **PG version compatibility notes** (from linter + biology-problems): Feature probing patterns, macro availability testing, version-aware coding patterns.
  - Source: `biology-problems/webwork_examples/check_pg_version.pg`
  - Source: `webwork-pgml-linter/pgml_lint/plugins/macro_rules.py` (version-gated rules)

---

## Priority Actions

Ranked by impact on the textbook, considering both the importance of the topic and the availability of source material.

| Rank | Action | Chapter | Source Repo(s) | Key File(s) |
|------|--------|---------|----------------|-------------|
| 1 | Build "Common Mistakes" section from 44 lint rules, organized by category with before/after examples | Ch7 | webwork-pgml-linter | `docs/PGML_LINT_PLUGINS.md`, all 44 plugins |
| 2 | Add complete PGML syntax reference derived from PGML.pl parser (answer blanks, math, formatting, lists, images, alignment, command substitution) | Ch3 | pg_v2_17 | `macros/core/PGML.pl` |
| 3 | Extract renderer setup guide (Docker/Podman, configuration, health check) for Ch7.2 | Ch7 | webwork-pg-renderer | `README.md`, `docs/USAGE.md` |
| 4 | Extract renderer API scripting guide (endpoints, curl, Python smoke test, error detection) for Ch7.3 | Ch7 | webwork-pg-renderer | `docs/RENDERER_API_USAGE.md`, `script/HOW_TO_LINT.md`, `script/pg-smoke.py` |
| 5 | Document all undocumented question types: DraggableProof, DraggableSubsets, RadioMultiAnswer, WordCompletion, OneOf, CheckboxList, Scaffold | Ch5 | pg_v2_17, biology-problems | `macros/parsers/`, `macros/math/`, `ordering_entropy.pgml` |
| 6 | Add RDKit.js chemistry rendering section with initialization pattern and SMILES canvas rendering | Ch6 | biology-problems | `rdkit_working_in_webwork.pgml`, `macromolecule_identification.pgml` |
| 7 | Document MODES() function thoroughly with decision tree (4 linter plugins reveal this as the trickiest topic) | Ch6 | webwork-pgml-linter, biology-problems | `pgml_modes_in_inline.py`, `pgml_modes_tex_payload.py`, `pgml_modes_html_escape.py` |
| 8 | Create macro reference table with categories, one-line descriptions, and usage frequency from OPL data | Ch2, Ch90 | pg_v2_17, webwork-open-problem-library | `macros/` (all dirs), `output/summary/` |
| 9 | Write legacy PG to modern PGML migration guide using linter's 7 legacy-detection plugins | Ch2, Ch3 | webwork-pgml-linter | `pgml_ans_rule.py`, `pgml_br_variable.py`, `pgml_text_blocks.py`, `pgml_old_answer_checkers.py` |
| 10 | Add niceTables DataTable/LayoutTable examples (data display, grid visualization, embedded PGML answer blanks) | Ch6 | pg_v2_17, biology-problems, training-set | `niceTables.pl`, `two_dimensional_gel_spots.pgml`, `function-evaluation-1.pg` |
| 11 | Add GraphTool interactive graphing section covering 12+ object types and custom AnswerEvaluator | Ch6 | pg_v2_17, biology-problems | `parserGraphTool.pl`, `titration_buffer_graph_tool.pg` |
| 12 | Add TikZ cookbook with 3-4 patterns (coordinate plane, geometry, function graph) | Ch6 | pg_v2_17, training-set | `PGtikz.pl`, `sw3_3_69.pg` |
| 13 | Add PGgraphmacros section with init_graph, lineTo, stamps, labels examples | Ch6 | biology-problems, pg_v2_17 | `titration_pI.pgml`, `PGgraphmacros.pl` |
| 14 | Add seed testing methodology section (stability + variation checklist from linter plugins) | Ch7 | webwork-pgml-linter | `pgml_seed_stability.py`, `pgml_seed_variation.py` |
| 15 | Document partial credit grading: custom_problem_grader_fluid, weightedGrader, answerHints | Ch5, Ch6 | biology-problems, pg_v2_17 | `bond_types-matching.pgml`, `PGgraders.pl`, `weightedGrader.pl`, `answerHints.pl` |
| 16 | Add retry-loop pattern and helper functions (random_choice, shuffle_list, sample_unique) for constrained randomization | Ch4 | biology-problems | `protein_gel_migration.pgml` (lines 95-335) |
| 17 | Add HTML-in-PGML rules section: what is allowed vs forbidden, passthrough patterns, tag wrapper syntax | Ch6 | webwork-pgml-linter | `pgml_html_in_text.py`, `pgml_html_policy.py`, `pgml_html_forbidden_tags.py` |
| 18 | Use FortLewis authoring templates as appendix "Starter Templates" | Ch90 | training-set | `FortLewis/Authoring/Templates/` (30 files) |
| 19 | Add format comparison table (WeBWorK vs QTI v1.2 vs QTI v2.1 vs BBQ) with question type portability | Ch1 | qti_package_maker | `docs/ENGINES.md` |
| 20 | Add OPL header metadata best practices with full template, noisy values to avoid, KEYWORDS rules | Ch2 | webwork-pgml-linter | `pgml_header_tags.py` (282 lines, 20+ validation rules) |

---

## New Content Needed (not found in any repo)

These gaps remain unfilled by any sibling repo and require original authoring or external research:

1. **Chapter 8 content (AI agents)**: All placeholder. While repos provide scattered examples of AI-assisted workflows (YAML-to-PG pipelines, LLM title generation, corpus analysis), no repo provides a coherent narrative about how to use AI agents to write WeBWorK problems. This chapter needs: prompt engineering for PG generation, AI agent workflow patterns, quality assurance for AI-generated problems, iterative refinement strategies.

2. **LibreTexts ADAPT import tutorial**: The biology-problems-website has a planned but unwritten "LibreTexts ADAPT QTI v1.2 Question Import Guide." No repo documents the ADAPT import workflow end-to-end.

3. **plotly3D documentation**: The `plotly3D.pl` macro exists in PG v2.17 but no repo has example problems using it. 3D graphing documentation needs to be written from the macro POD.

4. **Boolean context for logic courses**: `contextBoolean.pl` exists but no example problems were found in any repo.

5. **BaseN context for CS courses**: `contextBaseN.pl` exists but no example problems were found.

6. **R and SageMath integration**: `RserveClient.pl` and `sage.pl` exist in PG but no example problems using them appear in any analyzed repo.

7. **Essay question workflow**: `PGessaymacros.pl` exists with 564 essay files in OPL, but no repo provides detailed guidance on manual grading workflows.

8. **externalData.pl for cross-problem data**: The macro exists for storing/retrieving data across problems but no examples appear in analyzed repos.

9. **Accessibility guidelines**: No repo provides guidance on writing accessible WeBWorK problems (screen reader compatibility, alt text for images, color contrast).

10. **Non-math STEM examples**: The OPL is 62% math, 0% biology, 0% chemistry by DBsubject. The biology-problems repo fills some gaps, but physics, chemistry, and general science examples are still needed beyond the 3 chemistry reaction files and limited physics content.

---

## Per-Repo Value Summary

### biology-problems (HIGH VALUE)

The biology-problems repo is the single most valuable source for unique, advanced content not found elsewhere. Its 37 files provide the only examples of RDKit.js chemistry rendering (8 files), simulated gel electrophoresis via HTML/CSS (1 file), PGgraphmacros titration curves (1 file), GraphTool with custom AnswerEvaluator (1 file), DraggableProof ordering (1 file), custom HTML radio cards (3 files), and large-scale data pool management (50-358 item pools). It fills critical gaps in Chapters 5 and 6 with patterns not found in the OPL or any other repo. It also provides biology-specific OPL taxonomy examples, diagnostic utilities for PG version detection, and the retry-loop randomization pattern. Every single file is worth extracting for the textbook.

### webwork-pgml-opl-training-set (HIGH VALUE)

The training set repo provides the statistical foundation for the textbook: macro usage frequencies, question type distributions, and canonical patterns drawn from a curated 8,963-file PGML corpus. Its FortLewis authoring templates (30 files) are ready-made appendix material. The repo demonstrates DataTable with embedded PGML, CheckboxList, Scaffold, WordCompletion, and chemical reaction patterns. The pg_analyze toolkit and corpus documentation provide infrastructure for ongoing analysis. Its primary gap is the absence of biology or chemistry content by DBsubject classification.

### pg_v2_17 (HIGH VALUE)

The PG v2.17 source repo is the authoritative reference for every macro, context, parser, and MathObject type. Its 161+ macro files with embedded POD documentation define the complete PG API. The 157 sample problems provide canonical examples. Critical contributions include the PGML parser (defining the syntax grammar), 50 context macros, 30 parser macros, and 22 graphing macros. This repo is essential for building reference tables (Ch90) and documenting undocumented question types (Ch5). It is the only source for plotly3D, many context macros, and the complete MathObject type system.

### webwork-pgml-linter (HIGH VALUE)

The linter repo is the primary source for Chapter 7 content. Its 44 plugins represent a curated catalog of the most common WeBWorK authoring mistakes, organized into categories (document structure, macro loading, PGML syntax, HTML in PGML, MODES() pitfalls, seed/randomization, legacy patterns, encoding, code quality). The four MODES() plugins reveal this as the trickiest PGML topic. The seed testing plugins provide a complete randomization QA methodology. The legacy detection plugins map directly to a migration guide. The 1,148-line PGML_LINT_PLUGINS.md is the single most comprehensive document for textbook content.

### webwork-pg-renderer (MEDIUM VALUE)

The renderer repo is the primary source for Chapters 7.2 (setup) and 7.3 (scripting). It provides Docker/Podman setup instructions, the complete render API with endpoints and parameters, JSON response schema, error detection pipeline, smoke test scripts (Python, Perl, Bash), and lint-via-API documentation. The renderer ships with the full PG-2.17+ macro set and configuration reference. Its value is focused narrowly on testing infrastructure rather than problem authoring content.

### webwork-open-problem-library (MEDIUM VALUE)

The OPL provides the empirical backbone for the textbook: 72,734 problems, macro frequency data, question type statistics, discipline distribution, and duplicate analysis. It is essential for framing the scale of the ecosystem in Ch1 and for data-driven prioritization of content in Ch2 and Ch5. However, its direct contribution of extractable problem examples is limited because most content is legacy PG format (only 25% PGML), and it has zero biology or chemistry content. The pre-computed analysis TSVs in output/ are more useful than the raw problem files.

### biology-problems-website (LOW VALUE)

The biology-problems-website provides contextual value rather than extractable code. Its three LMS import tutorials (Blackboard Learn, Blackboard Ultra, Canvas) with screenshot annotations are high-quality companion material. The planned but unwritten ADAPT tutorial represents a direct opportunity. The LLM title generation pipeline and BBQ batch runner are relevant to Chapter 8 as AI/automation case studies. The daily puzzles (Peptidyle, Deletion Mutants, Mutant Screen) showcase creative assessment approaches.

### qti_package_maker (LOW VALUE)

The qti_package_maker provides focused value for Chapter 1.4 (format comparison). Its engine capability matrix, QTI v1.2 vs v2.1 structural differences, and platform compatibility observations (JavaScript/HTML rendering failures across LMS platforms) provide concrete evidence for why WeBWorK's server-side rendering model is superior. The 7 supported question types with per-engine gaps illustrate format portability constraints. Its modular engine architecture is a minor contribution to Chapter 8 as a tool-building case study.

---

## Cross-Repo Synergies and Contradictions

### Key synergies (repos providing complementary content for the same topic):

1. **MODES() function**: The linter (4 plugins detecting MODES issues) + biology-problems (real-world MODES usage) + PG v2.17 (source documentation) provide a complete picture from specification to common mistakes to real examples.

2. **Question types**: PG v2.17 (macro POD documentation) + training set (frequency data + canonical examples) + biology-problems (biology-specific examples) + linter (function signature validation + macro requirements) all contribute to Chapter 5 from different angles.

3. **niceTables**: PG v2.17 (macro source with full options) + biology-problems (LayoutTable grid, DataTable display) + training set (DataTable with embedded PGML) provide three complementary usage patterns.

4. **Header metadata**: Linter (20+ validation rules) + training set (OPL header examples) + biology-problems (biology taxonomy) + OPL (frequency data) each contribute a piece of the header best practices guide.

5. **Seed/randomization**: Linter (stability + variation plugins) + biology-problems (PGrandom, retry-loop, helper functions) + training set (randomization patterns) provide testing methodology + implementation patterns.

### No contradictions found between repos.

All repos are consistent in their recommendations. The linter's rules align with the coding patterns demonstrated in biology-problems and the training set. The PG v2.17 macro documentation matches the renderer's shipped macro set. The OPL statistics validate the training set's curation methodology.
