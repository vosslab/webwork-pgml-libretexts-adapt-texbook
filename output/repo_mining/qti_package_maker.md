# Mining Report: qti_package_maker

## Repo Overview

qti_package_maker is a Python package and CLI for converting Blackboard Question Upload (BBQ) text files into QTI packages and other export formats. It supports six output engines: Canvas QTI v1.2, Blackboard QTI v2.1, Blackboard BBQ text upload, human-readable text, HTML self-test, and text2qti. Two input readers exist (BBQ text upload and text2qti). The tool is aimed at instructors and developers who need to move assessments across LMS platforms (Canvas, Blackboard, LibreTexts ADAPT).

The architecture uses an engine-based plugin system where each format adapter is an isolated package under `qti_package_maker/engines/`. A shared ItemBank data model decouples question representation from format-specific XML/text rendering. Seven question types are supported: MC, MA, MATCH, NUM, FIB, MULTI_FIB, and ORDER. Not all engines support all types (see capability matrix below).

## QTI Format Details

### Supported output formats

| Engine name         | Format type                   | Compatible LMS                      | Read | Write |
|---------------------|-------------------------------|-------------------------------------|------|-------|
| canvas_qti_v1_2     | QTI v1.2 (IMS XML ZIP)       | Canvas, LibreTexts ADAPT            | no   | yes   |
| blackboard_qti_v2_1 | QTI v2.1 (IMS XML ZIP)       | Blackboard                          | no   | yes   |
| bbq_text_upload     | Blackboard text upload (.txt) | Blackboard (Original Course View)   | yes  | yes   |
| human_readable      | Plain-text review             | Any (non-import, review only)       | no   | yes   |
| html_selftest       | Self-contained HTML quiz      | Any web browser                     | no   | yes   |
| text2qti            | text2qti plain-text format    | Via text2qti toolchain              | yes  | yes   |

### Question type support by engine

| Item type | bbq text upload | blackboard qti v2.1 | canvas qti v1.2 | html selftest | human readable | text2qti |
|-----------|-----------------|----------------------|------------------|---------------|----------------|----------|
| FIB       | yes             | yes                  | X                | yes           | yes            | yes      |
| MA        | yes             | yes                  | yes              | yes           | yes            | yes      |
| MATCH     | yes             | yes                  | yes              | yes           | yes            | no       |
| MC        | yes             | yes                  | yes              | yes           | yes            | yes      |
| MULTI_FIB | yes             | yes                  | yes              | yes           | yes            | no       |
| NUM       | yes             | yes                  | yes              | yes           | yes            | yes      |
| ORDER     | yes             | yes                  | X                | yes           | yes            | no       |

### QTI v1.2 vs v2.1 differences (from codebase)

- **QTI v1.2** (Canvas/ADAPT): Uses `questestinterop` XML namespace with `assessment > section > item` structure. Questions use `presentation > response_lid > render_choice` for choices and `resprocessing > respcondition` for scoring. Canvas does not support FIB or ORDER in QTI v1.2 imports.
- **QTI v2.1** (Blackboard): Uses `assessmentItem` elements with `responseDeclaration`, `outcomeDeclaration`, `itemBody`, and `responseProcessing`. Supports all seven question types. Feedback mapping uses `modalFeedback` and `feedbackBlock` elements.
- **Key difference**: The XML structures are fundamentally different between v1.2 and v2.1; the `write_item.py` modules for each engine are "very dissimilar" per the developer notes, sharing only about 10% of code despite taking identical inputs.

### Conversion patterns

- Input: BBQ tab-delimited text files (one question per line) following `bbq-<name>-questions.txt` naming.
- Processing: BBQ reader parses into ItemBank (shared data model with typed item classes).
- Output: ItemBank is passed to one or more engines; each engine's `write_item.py` renders items in format-specific XML/text/HTML.
- Round-trip: BBQ and text2qti engines can both read and write, enabling format conversion chains.

### Platform compatibility observations (from TEMP_RDKit_QTI_IMPORT_NOTES.md)

- Canvas QTI 1.2 import: standard HTML renders but JavaScript does not execute.
- Blackboard QTI 2.1 import: HTML renders but script content can be escaped/broken.
- Blackboard BBQ text import: HTML and JavaScript both work.
- ADAPT QTI 1.2 import with script tags: question statement did not load.
- Blackboard export of BBQ-authored pool to QTI 2.1 can damage script content.

## Chapter Mapping

### Chapter 1.4: Comparing WeBWorK to other formats (H5P, LMS quizzes, QTI)

- **Relevant content**: The engine capability matrix provides a concrete comparison of what question types each LMS format supports. The QTI v1.2 vs v2.1 structural differences (different XML schemas, different element hierarchies, different LMS compatibility) are directly relevant. The platform compatibility notes about JavaScript/HTML rendering across Canvas, Blackboard, and ADAPT provide real-world comparison data. The list of related projects (text2qti, amc2moodle, moodle-questions) maps the broader ecosystem of quiz format converters.
- **Textbook gap it fills**: The textbook likely lacks a concrete side-by-side of what question types are portable across formats. The qti_package_maker capability matrix and engine documentation provide empirical data on format limitations (e.g., Canvas QTI 1.2 cannot import FIB or ORDER; text2qti cannot handle MATCH, MULTI_FIB, or ORDER). This is the kind of practical comparison that contrasts with WeBWorK's unlimited question type flexibility.

### Chapter 5: Different Question Types

- **Relevant content**: The seven supported QTI question types (MC, MA, MATCH, NUM, FIB, MULTI_FIB, ORDER) with their input schemas documented in `docs/QUESTION_TYPES.md`. Each type's required fields (e.g., NUM needs `answer_float` + `tolerance_float`, MATCH needs `prompts_list` + `choices_list`) show how static quiz formats model questions compared to WeBWorK's programmatic approach. The per-engine support gaps (Canvas cannot do FIB/ORDER, text2qti cannot do MATCH/MULTI_FIB/ORDER) illustrate portability constraints.
- **Textbook gap it fills**: Provides a concrete mapping of "standard LMS question types" that can be compared to WeBWorK question types. WeBWorK's PGML can express all of these and more (e.g., essay, custom graders, randomized parameters), so this helps frame the limitations of static formats.

### Chapter 8: Using AI Agents (placeholders)

- **Relevant content**: The repo's engine architecture (BaseEngine with pluggable write_item modules, auto-discovery via engine_registration) is a clean example of modular Python design. The ENGINE_AUTHORING.md guide is a well-structured developer reference. The MODULARITY_REPORT.txt shows systematic code review practices. These could serve as examples of AI-assisted software architecture or tool building.
- **Textbook gap it fills**: If Chapter 8 covers AI agents for building educational tools, the qti_package_maker architecture could serve as a case study for how AI agents can help build and extend assessment conversion tools.

## Recommended Actions

1. **Extract format comparison table for Ch1.4**: Use the engine capability matrix from `docs/ENGINES.md` as the basis for a "Question Type Portability" table comparing WeBWorK, QTI v1.2, QTI v2.1, BBQ, and HTML selftest formats. Add a WeBWorK column showing that it supports all types plus more.

2. **Incorporate platform compatibility findings for Ch1.4**: The TEMP_RDKit_QTI_IMPORT_NOTES.md observations about JavaScript/HTML rendering failures across Canvas, Blackboard, and ADAPT provide concrete evidence for why WeBWorK's server-side rendering model avoids these LMS import pitfalls.

3. **Use question type schemas for Ch5**: The `docs/QUESTION_TYPES.md` input field definitions (e.g., MC needs question_text + choices_list + answer_text) provide a useful contrast to WeBWorK's programmatic approach where questions are code, not structured data.

4. **Reference related projects for Ch1.4 ecosystem context**: The `docs/RELATED_PROJECTS.md` list (text2qti, amc2moodle, moodle-questions, etc.) shows the fragmented landscape of quiz format converters, which underscores why WeBWorK's unified approach is valuable.

5. **Note QTI version differences for Ch1.4**: Emphasize that QTI v1.2 (Canvas/ADAPT) and QTI v2.1 (Blackboard) are not interchangeable despite both being "QTI" -- different XML schemas, different element names, different LMS support. This is a practical pain point that WeBWorK avoids by having its own rendering pipeline.

6. **Document format limitations as WeBWorK advantages for Ch1.4**: Key limitations to highlight: (a) no randomization in exported QTI (static snapshots only), (b) no custom grading logic, (c) no programmatic question generation, (d) JavaScript/HTML rendering unreliable across platforms, (e) question type support varies by LMS and QTI version.
