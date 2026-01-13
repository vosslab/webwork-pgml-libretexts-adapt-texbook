# Textbook page summaries

This document provides a high-level summary of each HTML page in `Textbook/` to help plan and organize the book.

Guideline: each entry below has exactly three sentences describing purpose, what you will have accomplished by the end, what you can do immediately after finishing, and how to apply it in practice, but written in natural prose without using formal educational jargon.
SEO tags appear on a separate line under each entry; aim for 3 tags, but allow fewer or more when it helps.
Prefer tags that make the page easy to find by its unique topic, rather than repeating the same global tags on every page.

## Chapter 1: Introduction
- `Textbook/01_Introduction/1.0-Index.html`: Introduces the book with a section map and a practical PG vs PGML split for science-first authoring. After finishing, you can pick a task-based starting point from the "Where to start today" table and know where PGML belongs. Use it as your orientation page before jumping into terms, quickstart, or templates.
  SEO tags: science assessment, PGML-first authoring, book roadmap
- `Textbook/01_Introduction/1.1-What_is_WeBWorK.html`: Explains what WeBWorK is and how PGML fits into a typical problem. After finishing, you can separate minimal setup from the PGML prompt and focus effort in the right place. Use it when you need a clear mental model of what a WeBWorK problem file is doing.
  SEO tags: WeBWorK basics, MathObjects, PGML prompt
- `Textbook/01_Introduction/1.2-Why_use_WeBWorK.html`: Describes why WeBWorK works well for repeated practice with immediate feedback in science courses. After finishing, you can decide whether a prompt belongs in WeBWorK and which patterns to prefer for maintainability. Use it when choosing between WeBWorK and a simpler question format for a specific activity.
  SEO tags: immediate feedback, randomized variants, maintainable items
- `Textbook/01_Introduction/1.3-Key_Features_of_WeBWorK.html`: Summarizes the features that matter most when building science-friendly prompts. After finishing, you can choose between answer checking approaches, randomization, and interaction patterns without overcomplicating the code. Use it as a checklist when planning a new question.
  SEO tags: answer checking, interaction patterns, problem features
- `Textbook/01_Introduction/1.4-Comparing_WeBWorK_to_other_formats.html`: Compares WeBWorK to other automated assessment formats so you can choose an appropriate tool. After finishing, you can recognize when robust parsing and algorithmic variants are worth the setup cost. Use it when deciding between WeBWorK and a simpler, more portable question pattern.
  SEO tags: H5P comparison, LMS question banks, portability tradeoffs
- `Textbook/01_Introduction/1.5-Common_terms_and_names.html`: Defines the small set of terms that show up constantly in this book, including PG, PGML, macros, MathObjects, Context, seed, and the ADAPT names you will see in the interface. After finishing, you can read the later chapters without guessing what a term means or where it shows up in a problem file or workflow. Use it as a quick reference when vocabulary slows you down, and consult your campus LibreTexts glossary for platform-wide definitions.
  SEO tags: PG vs PGML, WeBWorK terminology, ADAPT terms
- `Textbook/01_Introduction/1.6-Quickstart_copy_edit_first_problem.html`: Walks you through a fast first win by copy-editing a complete PGML-first problem. After finishing, you can take a working template and make small changes without breaking grading. Use it when you want to move from reading to shipping your first working item, and when ADAPT reports only a generic error, use Chapter 7 to get a line-level error.
  SEO tags: copy-edit workflow, first problem, line-level debugging

## Chapter 2: Problem Generation (PG)
- `Textbook/02_Problem_Generation_PG/2.0-Index.html`: Sets expectations that regular PG is discouraged and treated as scaffolding for PGML. After finishing, you can keep setup code focused and put student-facing text where it belongs in the PGML block. Use it to keep your problems short, readable, and consistent.
  SEO tags: minimal PG setup, PGML-first style, authoring conventions
- `Textbook/02_Problem_Generation_PG/2.1-Introduction_to_PG_Language.html`: Introduces PG as the setup layer behind a PGML-first problem. After finishing, you can edit small setup blocks to define values and answer checkers without building a large Perl program. Use it when you need to adjust a problem setup while keeping the prompt stable in PGML.
  SEO tags: Perl setup layer, Context(), random values
- `Textbook/02_Problem_Generation_PG/2.2-PG_Problem_Files_with_a_pg_file_extension.html`: Breaks down the common structure of a `.pg` file and provides a minimal PGML-first template and annotated skeleton. After finishing, you can place comments, initialization, setup, PGML text, and optional solutions in the right locations consistently. Use it as your starting point when creating or refactoring a problem file, and after any macro or setup change, run local rendering from Chapter 7 to catch missing macros and syntax errors early.
  SEO tags: five PG file sections, DOCUMENT and loadMacros, annotated skeleton
- `Textbook/02_Problem_Generation_PG/2.3-Sections_within_a_PG_question.html`: Breaks down the typical sections of a problem in a PGML-first style. After finishing, you can keep setup, prompt text, and optional solution material separated and easier to maintain. Use it when refactoring a messy problem into a clean structure.
  SEO tags: setup vs prompt, hints and solutions, maintainable structure
- `Textbook/02_Problem_Generation_PG/2.4-Common_PG_Macros.html`: Lists the macro files most commonly needed for PGML-first authoring and the advanced macro families you will see referenced in older problems. After finishing, you can build a minimal `loadMacros()` block and recognize when a macro topic is optional versus necessary. Use it when a problem needs a new interaction pattern and you are not sure which macro file enables it.
  SEO tags: loadMacros, parser macros, InexactValue macro
- `Textbook/02_Problem_Generation_PG/2.5-Legacy_PG_and_deprecated_patterns.html`: Shows how to recognize legacy PG patterns and deprecated approaches that are common in online examples and older problem libraries. After finishing, you can triage a copied problem quickly, identify what is safe to reuse, and translate the core idea into a PGML-first structure without importing fragile formatting or scattered grading logic. Use it before copy-pasting random examples, especially when a problem relies on long `BEGIN_TEXT/END_TEXT` blocks, heavy Perl string assembly, or macros you do not recognize.
  SEO tags: legacy PG, deprecated patterns, safe refactoring
  
## Chapter 3: PGML (PG Markup Language)
- `Textbook/03_PGML_PG_Markup_Language/3.0-Index.html`: Introduces the PGML chapter as the core authoring layer for student-facing prompts. After finishing, you can identify which PGML topic you need next and keep your work PGML-first. Use it as the entry point before writing or revising any prompt text.
  SEO tags: PGML chapter index, prompt formatting, student-facing text
- `Textbook/03_PGML_PG_Markup_Language/3.1-Introduction_to_PGML.html`: Defines PGML and summarizes the small set of math-notation patterns you will use constantly. After finishing, you can choose TeX versus calculator notation and use the correct delimiters reliably. Use it when onboarding a new author or standardizing prompt style in a course team.
  SEO tags: TeX delimiters, calculator notation, math formatting
- `Textbook/03_PGML_PG_Markup_Language/3.2-Answer_blanks_and_answers.html`: Explains answer blanks and the recommended habit of attaching answers directly to blanks. After finishing, you can keep grading rules next to the prompt text and reduce mismatches in multi-part items. Use it when building biology-style prompts where several short answers must stay aligned with the story, and use Chapter 7 when blank binding failures show up as a generic ADAPT error.
  SEO tags: answer blanks, attach answers, Formula answers
- `Textbook/03_PGML_PG_Markup_Language/3.3-Lists_and_workflows.html`: Shows how to write numbered and bulleted lists in PGML and how to keep multi-step instructions readable. After finishing, you can express lab-style workflows with explicit units and reporting requirements inside each step. Use it when a prompt has procedural steps or a short grading checklist.
  SEO tags: numbered lists, workflow prompts, procedural instructions
- `Textbook/03_PGML_PG_Markup_Language/3.4-Tables_and_structured_data.html`: Frames tables as the default way to present measurements and observations in science prompts and introduces the DataTable/LayoutTable split. After finishing, you can decide when a table is real data versus a layout trick and pick the helper that fits. Use it when a question depends on reading a small dataset and computing from it.
  SEO tags: DataTable, LayoutTable, accessible tables
- `Textbook/03_PGML_PG_Markup_Language/3.5-Layout_controls.html`: Collects light-weight structure and layout tools like headings, emphasis, horizontal rules, and limited justification syntax. After finishing, you can improve scanability without creating fragile formatting that breaks across renderers. Use it as a finishing pass for longer prompts once the grading logic is correct.
  SEO tags: headings, emphasis, justification
- `Textbook/03_PGML_PG_Markup_Language/3.6-Command_substitution_and_inserts.html`: Explains command substitution as a controlled escape hatch for inserting computed or helper-generated content. After finishing, you can decide when to use a small substitution and how to keep it readable and testable. Use it sparingly for advanced insertion patterns, and keep textbook content self-contained without page links.
  SEO tags: command substitution, helper-generated output, no links

## Chapter 4: Breaking Down the Components of a WeBWorK Problem
- `Textbook/04_Breaking_Down_the_Components/4.0-Index.html`: Explains that Chapter 4 is a single worked problem sliced into Preamble, Setup, Statement, Solution, plus a Put it together workflow page. After finishing, you can use the section map and anatomy tables to locate where edits belong and what usually breaks. Use it as the navigation page before you touch the full file and when ADAPT errors need a quick local render pointer to Chapter 7.
  SEO tags: section map, problem anatomy, workflow roadmap
- `Textbook/04_Breaking_Down_the_Components/4.1-Full_file.html`: Shows the full reference .pg file with section markers and a short anchor map. After finishing, you can scan the entire flow and confirm which section contains a change you just made. Use it as a reference copy after you edit in 4.2 to 4.5, not as the first editing target.
  SEO tags: full .pg file, anchor map, reference copy
- `Textbook/04_Breaking_Down_the_Components/4.2-Preamble.html`: Focuses on the Preamble as the macro-loading layer and points to official choice and MultiAnswer patterns by name. After finishing, you can choose the right macros, avoid deprecated PopUp usage, and recognize when a missing macro causes a render failure. Use it when adding a new interaction type or cleaning up a legacy macro list.
  SEO tags: preamble, macro selection, PGchoicemacros
- `Textbook/04_Breaking_Down_the_Components/4.3-Setup.html`: Covers Setup as the place for variables, constraints, computed targets, and tolerance decisions. After finishing, you can set biologically plausible ranges, keep units consistent, and apply the NumericalTolerance-style options in the right place. Use it when adjusting randomization, grading strictness, or answer formatting before you touch the prompt text.
  SEO tags: setup block, tolerance patterns, unit consistency
- `Textbook/04_Breaking_Down_the_Components/4.4-Statement.html`: Breaks down the Statement as PGML text plus blanks, with a blanks map and structure patterns table. After finishing, you can align each blank with its answer object and choose the right structure (paragraphs, lists, tables, inline math) without breaking readability. Use it when rewriting the story or adding choice-based inserts that follow the OpenWeBWorK technique samples.
  SEO tags: PGML statement, blanks map, structure patterns
- `Textbook/04_Breaking_Down_the_Components/4.5-Solution.html`: Explains the Solution as a short, trust-building explanation aligned with the checker. After finishing, you can keep the solution consistent with tolerances, units, and rounding while adding minimal feedback hooks. Use it when students or graders need clarity about the expected method and format.
  SEO tags: solution block, grading alignment, rounding notes
- `Textbook/04_Breaking_Down_the_Components/4.6-Putting_it_together.html`: Turns the deep dive into a repeatable edit workflow with a common-edits table and preflight checks. After finishing, you can jump to the right section first, then verify alignment before importing to ADAPT. Use it as the final workflow page when you want a fast local render option and a techniques menu for swapping interaction types.
  SEO tags: edit workflow, preflight checklist, techniques menu

## Chapter 5: Different Question Types in WeBWorK
- `Textbook/05_Different_Question_Types/5.0-Index.html`: Frames the chapter as a bridge between WeBWorK authoring and using WeBWorK inside ADAPT, with life-science-first examples. After finishing, you can choose between interaction patterns, workflow habits, and QA checks depending on what you are trying to ship. Use it to start Chapter 5 and pick the subsection you need next.
  SEO tags: ADAPT workflow, question types, QA checklist
- `Textbook/05_Different_Question_Types/5.1-Question_types_overview.html`: Introduces a shared set of common question types and when each one is a good fit. After finishing, you can map a task to an interaction pattern before writing any code or distractors. Use it to choose between single-answer, multi-answer, matching, numeric entry, blanks, and ordering.
  SEO tags: interaction patterns, item design, question selection
- `Textbook/05_Different_Question_Types/5.2-Multiple_choice.html`: Shows how to write strong multiple choice items with science-relevant distractors. After finishing, you can produce a single-best-answer concept check that targets a specific misconception. Use it when you want a fast, reliable concept check that is easy to grade.
  SEO tags: distractor design, biology multiple choice, misconception targeting
- `Textbook/05_Different_Question_Types/5.3-Multiple_answer.html`: Shows how to write select-all-that-apply questions with clear criteria. After finishing, you can design choices that avoid ambiguity and make it clear why each selection is correct or incorrect. Use it when the concept requires recognizing a set of correct statements rather than one best answer.
  SEO tags: checkbox questions, clear criteria, multiple correct
- `Textbook/05_Different_Question_Types/5.4-Matching.html`: Shows how to use matching for definitions and associations in science. After finishing, you can create prompt and choice sets that test understanding rather than trivia recall. Use it when you want students to connect terms, steps, or concepts to their correct descriptions.
  SEO tags: matching items, concept associations, vocabulary mapping
- `Textbook/05_Different_Question_Types/5.5-Numerical_entry.html`: Shows how to use numeric entry with explicit tolerance and units expectations. After finishing, you can set tolerances that match rounding and measurement context and avoid unexpected grading behavior. Use it for quick calculations where a single numeric result is the right target.
  SEO tags: dilution math, tolerance choice, unit expectations
- `Textbook/05_Different_Question_Types/5.6-Fill_in_the_blank.html`: Shows how to use fill-in-the-blank for short textual answers. After finishing, you can define acceptable variants such as plural forms and common synonyms in a controlled way. Use it for vocabulary checks and short labels where a small set of responses is appropriate.
  SEO tags: acceptable variants, short answers, terminology checks
- `Textbook/05_Different_Question_Types/5.7-Multi_part_fill_in_the_blank.html`: Shows how to design prompts with multiple blanks that each ask for a specific item. After finishing, you can write multi-step prompts with unambiguous blank labels and consistent formatting for answers. Use it for short multi-step prompts where each step has a short response.
  SEO tags: multi-step prompts, blank labeling, consistent formatting
- `Textbook/05_Different_Question_Types/5.8-Ordered_list.html`: Shows how to test sequencing knowledge with an ordered list question. After finishing, you can choose sequences that have a single standard order and avoid turning the item into a memory game. Use it for protocols and workflows that have a single standard sequence.
  SEO tags: protocol sequencing, ordered list, workflow grading
- `Textbook/05_Different_Question_Types/5.9-Workflow_and_QA_in_ADAPT.html`: Combines a practical ADAPT workflow checklist with a compact QA pass for biology-style WeBWorK items. After finishing, you can run a repeatable clone-edit-preview-publish process and catch the common failure modes that lead to "generic error" screens. Use it as your final pre-release routine whenever you add or revise questions in a bank.
  SEO tags: ADAPT workflow, QA checklist, common failure modes

## Chapter 6: Subject-Specific Applications in WeBWorK
- `Textbook/06_Subject-Specific_Applications/6.0-Index.html`: Explains how to adapt the Chapter 5 question types into subject-authentic prompts with realistic units, data, and expectations. After finishing, you can recognize what tends to break in biology-style questions and choose patterns that stay robust for grading. Use it as a bridge from generic question types to life-science-first question writing.
  SEO tags: biology prompt patterns, grading robustness, realistic data
- `Textbook/06_Subject-Specific_Applications/6.1-Dilution_series_and_standard_curves.html`: Covers dilution-series prompts and standard-curve setups as a reliable life-science pattern. After finishing, you can write dilution questions that avoid unit drift and rounding disputes. Use it when building wet-lab prompts for stocks, working solutions, and serial dilutions.
  SEO tags: serial dilution, standard curve, concentration series
- `Textbook/06_Subject-Specific_Applications/6.2-Enzyme_kinetics_Michaelis_Menten.html`: Summarizes Michaelis-Menten question patterns that stay focused and grade reliably. After finishing, you can separate parameter reading from calculation and keep units and tolerances explicit. Use it when building kinetics items around Vmax, Km, and substrate concentration.
  SEO tags: Michaelis-Menten, Km and Vmax, reaction velocity
- `Textbook/06_Subject-Specific_Applications/6.3-Genotype_to_phenotype_mapping.html`: Frames genotype-to-phenotype items as a mix of small computations and explicit interpretation checks. After finishing, you can write genetics prompts that avoid notation ambiguity and keep formatting consistent. Use it when building cross problems, genotype frequency items, and phenotype interpretation checks.
  SEO tags: genotype frequencies, phenotype mapping, notation clarity
- `Textbook/06_Subject-Specific_Applications/6.4-Pathway_logic_and_regulation.html`: Outlines pathway-logic patterns that test inference without turning into a long reading task. After finishing, you can design matching and selection prompts with clear assumptions about activation and inhibition. Use it when writing pathway regulation questions and perturbation reasoning checks.
  SEO tags: pathway regulation, activation inhibition, perturbation logic
- `Textbook/06_Subject-Specific_Applications/6.5-Gels_blots_and_band_interpretation.html`: Describes gel and blot interpretation patterns that remain robust even when images fail to render. After finishing, you can separate what the data shows from the single inference you want graded. Use it when writing band-ordering, lane-identification, and expression interpretation items.
  SEO tags: gel interpretation, band migration, lane ranking
- `Textbook/06_Subject-Specific_Applications/6.6-qPCR_Ct_and_relative_expression.html`: Explains qPCR Ct and relative-expression prompts as a log-scale grading trap and shows how to make expectations explicit. After finishing, you can design Ct and fold-change questions where the model and reporting format are unambiguous. Use it when writing delta Ct, Ct comparison, and simple fold-change interpretation items.
  SEO tags: qPCR Ct, delta Ct, fold change
- `Textbook/06_Subject-Specific_Applications/6.7-Pedigrees_and_probability.html`: Covers pedigree and inheritance probability prompts with explicit model assumptions. After finishing, you can write probability questions that avoid hidden autosomal vs sex-linked or dominance assumptions. Use it when building family-probability and affected-offspring computation items.
  SEO tags: pedigree probability, autosomal recessive, carrier risk
- `Textbook/06_Subject-Specific_Applications/6.8-Experimental_design_and_controls.html`: Focuses on experimental design and controls as concrete decision items that grade reliably. After finishing, you can write control-selection prompts that are anchored to a specific confound or threat to validity. Use it when writing biology design questions about treatments, vehicles, and confound isolation.
  SEO tags: experimental controls, confounds, validity

## Chapter 7: Local Testing with webwork-pg-renderer
- `Textbook/07_Local_Testing_with_webwork_pg_renderer/7.0-Index.html`: Introduces `webwork-pg-renderer` as a lightweight way to preview and test PG and PGML problems locally, especially when ADAPT only reports a generic error. After finishing, you can set up local rendering once (Podman or Docker recommended, or ask campus IT or a TA to run it once) and use it as the default workflow when you are building or editing more than a handful of problems, while keeping ADAPT preview as the final platform check. Use it as the entry point for a first-pass testing loop, and if setup feels like too much, fall back to the ADAPT preview steps in Chapter 5.9 and expect slower debugging when something breaks.
  SEO tags: local PG testing, webwork-pg-renderer, offline preview
- `Textbook/07_Local_Testing_with_webwork_pg_renderer/7.1-Quickstart_and_editor_workflow.html`: Walks through running the renderer and using the editor to load a `.pg` file, set a seed, render, and save edits back to disk. After finishing, you can iterate quickly with a tight loop (for example, open http://localhost:3000/ once it is running) while keeping a failing case reproducible by reusing the same seed and file path. Use it during day-to-day authoring when you want fast iteration, line-level errors, and seed control before you do an ADAPT preview.
  SEO tags: live preview editor, problemSeed, save back to file
- `Textbook/07_Local_Testing_with_webwork_pg_renderer/7.2-Testing_habits_and_troubleshooting.html`: Focuses on a small set of checks that catch most failures, including variant sweeps, boundary values, and student-view behavior like submit controls and permission levels. After finishing, you can diagnose whether a failure is PG syntax, missing dependencies, or a rendering/UI mismatch using line number errors, logs, and the health endpoint. Use it as a repeatable first-pass QA loop before an ADAPT preview and before importing or publishing a revised problem.
  SEO tags: edge case testing, health endpoint, container logs
