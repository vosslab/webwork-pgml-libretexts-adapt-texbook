# Textbook Migration Guide - 2026-01-28 Restructure

This document tracks all file renames, new files, and section changes needed to implement the restructured textbook plan in `Textbook/TEXTBOOK_PAGE_SUMMARIES.md`.

## Chapter 2: Problem Generation (PG) - Renumbered for OPL Header

### New Files to Create
- `Textbook/02_Problem_Generation_PG/2.2-OPL_header_and_metadata.html` (NEW)

### Files to Rename
- `Textbook/02_Problem_Generation_PG/2.2-PG_Problem_Files_with_a_pg_file_extension.html` -> `2.3-PG_Problem_Files_with_a_pg_file_extension.html`
- `Textbook/02_Problem_Generation_PG/2.3-Sections_within_a_PG_question.html` -> `2.4-Sections_within_a_PG_question.html`
- `Textbook/02_Problem_Generation_PG/2.4-Common_PG_Macros.html` -> `2.5-Common_PG_Macros.html`
- `Textbook/02_Problem_Generation_PG/2.5-Legacy_PG_and_deprecated_patterns.html` -> `2.6-Legacy_PG_and_deprecated_patterns.html`

### Files to Update
- `Textbook/02_Problem_Generation_PG/2.0-Index.html` - Update to acknowledge five-section structure
- `Textbook/02_Problem_Generation_PG/2.5-Common_PG_Macros.html` (renamed from 2.4) - Add macro version comparison table showing ADAPT/renderer subset vs full PG 2.17+ vs PG 2.20

## Chapter 4: Breaking Down Components - Renumbered for OPL Header

### New Files to Create
- `Textbook/04_Breaking_Down_the_Components/4.2-OPL_Header.html` (NEW)

### Files to Rename
- `Textbook/04_Breaking_Down_the_Components/4.2-Preamble.html` -> `4.3-Preamble.html`
- `Textbook/04_Breaking_Down_the_Components/4.3-Setup.html` -> `4.4-Setup.html`
- `Textbook/04_Breaking_Down_the_Components/4.4-Statement.html` -> `4.5-Statement.html`
- `Textbook/04_Breaking_Down_the_Components/4.5-Solution.html` -> `4.6-Solution.html`
- `Textbook/04_Breaking_Down_the_Components/4.6-Putting_it_together.html` -> `4.7-Putting_it_together.html`

### Files to Update
- `Textbook/04_Breaking_Down_the_Components/4.0-Index.html` - Update to show five-section structure
- `Textbook/04_Breaking_Down_the_Components/4.1-Full_file.html` - Add OPL header to example

## Chapter 6: Subject-Specific -> Advanced PGML Techniques - Complete Restructure

### Directory to Rename
- `Textbook/06_Subject-Specific_Applications/` -> `Textbook/06_Advanced_PGML_Techniques/`

### New Files to Create (All in `Textbook/06_Advanced_PGML_Techniques/`)
- `6.0-Index.html` (update existing)
- `6.1-Coloring_text_and_emphasis.html` (NEW)
- `6.2-Tables_with_niceTables.html` (NEW)
- `6.3-Matching_problems.html` (NEW - includes MODES explanation folded in)
- `6.4-Multiple_choice_statements.html` (NEW)
- `6.5-Advanced_randomization_patterns.html` (NEW)

### Files to Remove/Archive
- `6.1-Dilution_series_and_standard_curves.html` (integrate examples into 6.3, 6.6)
- `6.2-Enzyme_kinetics_Michaelis_Menten.html` (integrate examples into 6.3)
- `6.3-Genotype_to_phenotype_mapping.html` (integrate examples into 6.6)
- `6.4-Pathway_logic_and_regulation.html` (integrate examples into 6.4, 6.5)
- `6.5-Gels_blots_and_band_interpretation.html` (integrate examples into 6.3)
- `6.6-qPCR_Ct_and_relative_expression.html` (integrate examples into 6.6)
- `6.7-Pedigrees_and_probability.html` (integrate examples into 6.6)
- `6.8-Experimental_design_and_controls.html` (integrate examples into 6.5)

## Chapter 7: Local Testing - Renumbered for API Section

### New Files to Create
- `Textbook/07_Local_Testing_with_webwork_pg_renderer/7.2-API_usage_for_scripts.html` (NEW)

### Files to Rename
- `Textbook/07_Local_Testing_with_webwork_pg_renderer/7.2-Testing_habits_and_troubleshooting.html` -> `7.3-Testing_habits_and_troubleshooting.html`

### Files to Update
- `Textbook/07_Local_Testing_with_webwork_pg_renderer/7.0-Index.html` - Add /health endpoint, PG 2.17 subset note
- `Textbook/07_Local_Testing_with_webwork_pg_renderer/7.1-Quickstart_and_editor_workflow.html` - Add private/ folder workflow

## Chapter 90: Appendices - Minimized

### New Files to Create
- `Textbook/90_Appendices/90.1-Minimal_templates.html` (NEW)
- `Textbook/90_Appendices/90.2-Glossary.html` (NEW)
- `Textbook/90_Appendices/90.3-Troubleshooting_checklist.html` (NEW)

### Files to Remove/Archive
- `90.5-Advanced_patterns_and_further_techniques.html` (if exists - content can move to relevant chapters)
- `90.6-Subject_specific_worked_examples.html` (examples integrated into Chapter 6)

### Files to Update
- `Textbook/90_Appendices/90.0-Index.html` - Update to reflect minimized structure

## Cross-References to Update

### Throughout the textbook, update references to:
1. **Chapter 2.4 macros** -> now **Chapter 2.5 macros**
2. **Chapter 6 subject-specific examples** -> now **Chapter 6 advanced techniques with integrated examples**
3. **Chapter 7.2 troubleshooting** -> now **Chapter 7.3 troubleshooting**
4. **"Four sections"** -> **"Five sections"** (OPL Header + four traditional)

## Content Migration Notes

### Chapter 6 Biology Examples Integration
- **6.3 Tables**: Add dilution series table example, enzyme kinetics data table example, gel/blot comparison table
- **6.4 Matching**: Add pathway component matching example, chemical bond matching example, genetics terminology matching
- **6.5 MC Statements**: Add experimental design statements example, pathway regulation claims example
- **6.6 Randomization**: Add qPCR conditions randomization example, genetics cross randomization, dilution factor guards

### OPL Header Content Sources
- **Chapter 2.2**: Use `OTHER_REPOS-do_not_commit/biology-problems/docs/webwork/WEBWORK_HEADER_STYLE.md`
- **Chapter 4.2**: Show biology-specific DBsubject classification example
- **Appendix 90.1**: Include OPL header template from WEBWORK_HEADER_STYLE.md

### Advanced PGML Content Sources
- **Chapter 6.1 Coloring**: Use `COLOR_TEXT_IN_WEBWORK.md`; show `[$var]*` pattern for HTML variables, PGML tag wrappers for static styling
- **Chapter 6.2 Tables**: Use `NICETABLES_TRANSLATION_PLAN.md`
- **Chapter 6.3 Matching**: Use `MATCHING_PROBLEMS.md` (lines 7-64) and reference `yaml_match_to_pgml.py`; fold in MODES explanation showing `MODES(HTML => ...)` is only required for flexbox wrapper HTML inside Perl eval blocks (e.g., `<div class="two-column"><div>` wrapping join() expressions) where removing MODES causes HTML to be escaped and layout to collapse; emphasize MODES is NOT needed for subscripts, charge labels, colored choices, or other plain HTML that renders fine
- **Chapter 6.4 MC Statements**: Use `PGML_QUESTION_TYPES.md` and reference `yaml_mc_statements_to_pgml.py`
- **Chapter 6.5 Randomization**: Use `RANDOMIZATION_REFERENCE.md`

### Chapter 7 Renderer Updates
- **7.2 API Usage**: Use `OTHER_REPOS-do_not_commit/webwork-pg-renderer/docs/RENDERER_API_USAGE.md`
- Add GET /health, POST / primary endpoint, parameter precedence, sourceFilePath vs problemSource guidance

## Implementation Checklist

- [ ] Rename Chapter 2 files (2.2->2.3, 2.3->2.4, 2.4->2.5, 2.5->2.6)
- [ ] Create Chapter 2.2 OPL header section
- [ ] Rename Chapter 4 files (4.2->4.3, 4.3->4.4, 4.4->4.5, 4.5->4.6, 4.6->4.7)
- [ ] Create Chapter 4.2 OPL Header section
- [ ] Update Chapter 4.1 Full file with OPL header
- [ ] Rename Chapter 6 directory (06_Subject-Specific_Applications -> 06_Advanced_PGML_Techniques)
- [ ] Create all new Chapter 6 sections (6.1-6.6)
- [ ] Archive old Chapter 6 sections, extracting examples to integrate
- [ ] Rename Chapter 7.2 to 7.3
- [ ] Create Chapter 7.2 API usage section
- [ ] Update Chapter 7.0 and 7.1
- [ ] Create new Appendix sections (90.1, 90.2, 90.3)
- [ ] Update all cross-references throughout textbook
- [ ] Update Chapter 1.0 with PG 2.17 subset scope note
- [ ] Update Chapter 2.0 with five-section acknowledgment
- [ ] Run HTML lint: `/opt/homebrew/bin/bash tests/run_html_lint.sh`
