# Writing Automated Questions using WeBWorK in ADAPT

This repository is a chapter-based textbook/guide (not a traditional software project).
The primary content lives in `Textbook/` as LibreTexts-ready HTML and is written for an audience
in the sciences and descriptive fields, with life-science-first examples.

The guide is PGML-first: regular PG is treated as minimal scaffolding, and most authoring effort
should go into clear, structured PGML prompts.

## Quick start
- If you want a first win fast: start at `Textbook/01_Introduction/1.6-Quickstart_copy_edit_first_problem.html`.
- If you want the framing and workflow first: start at `Textbook/01_Introduction/1.0-Index.html`.
- If you are editing chapter content: use `Textbook/TEXTBOOK_PAGE_SUMMARIES.md` as the source of truth for what each
  page is intended to cover (align the HTML pages to match it).

## Documentation
- Book plan and intended scope per page: [Textbook/TEXTBOOK_PAGE_SUMMARIES.md](Textbook/TEXTBOOK_PAGE_SUMMARIES.md)
- LibreTexts authoring constraints: [docs/LIBRETEXTS_HTML_GUIDE.md](docs/LIBRETEXTS_HTML_GUIDE.md)
- Repo conventions: [docs/REPO_STYLE.md](docs/REPO_STYLE.md)
- Markdown style: [docs/MARKDOWN_STYLE.md](docs/MARKDOWN_STYLE.md)
- Python style (for `tools/` scripts): [docs/PYTHON_STYLE.md](docs/PYTHON_STYLE.md)
- Repo maps: [docs/CODE_ARCHITECTURE.md](docs/CODE_ARCHITECTURE.md), [docs/FILE_STRUCTURE.md](docs/FILE_STRUCTURE.md)
- Changelog: [docs/CHANGELOG.md](docs/CHANGELOG.md)

## Repository layout
- `Textbook/`: the book content (HTML), organized by chapter folders.
- `Insight-HTML/` and `WebWorK-HTML/`: extracted source material used for writing (do not edit).
- `docs/`: repo conventions and HTML authoring rules.
- `tools/`: authoring utilities (for example, linting/formatters).
- `tests/`: local checks (HTML lint, Python checks).

## External resources
Textbook pages under `Textbook/` avoid HTML links (`<a href=...>`) for LibreTexts compatibility, so external
references live here (and in `Links/`).

- LibreTexts Insight: [WeBWorK techniques](https://commons.libretexts.org/insight/webwork-techniques)
- OpenWeBWorK PG docs: [sample problems index](https://openwebwork.github.io/pg-docs/sample-problems/)
- OpenWeBWorK PG docs: [MultipleChoiceCheckbox example](https://openwebwork.github.io/pg-docs/sample-problems/Misc/MultipleChoiceCheckbox.html)
- GitHub: [vosslab/webwork-pg-renderer](https://github.com/vosslab/webwork-pg-renderer)
- Biology Problems: [biologyproblems.org](https://biologyproblems.org/)

## Entry points
- `Textbook/01_Introduction/1.0-Index.html`
- `Textbook/02_Problem_Generation_PG/2.0-Index.html`
- `Textbook/03_PGML_PG_Markup_Language/3.0-Index.html`
- `Textbook/04_Breaking_Down_the_Components/4.0-Index.html`
- `Textbook/05_Different_Question_Types/5.0-Index.html`
- `Textbook/06_Subject-Specific_Applications/6.0-Index.html`
- `Textbook/07_Local_Testing_with_webwork_pg_renderer/7.0-Index.html`
- `Textbook/90_Appendices/90.0-Index.html`

## Chapter map (current)
- 01 Introduction: audience, framing, and why WeBWorK is useful in science courses.
- 02 Minimal PG scaffolding: `.pg` structure, macro loading, and keeping setup small.
- 03 PGML: the core authoring layer (blanks, lists, tables, and a small "escape hatch").
- 04 Worked example: a complete copy-and-edit PGML-first life-science problem.
- 05 ADAPT workflow and question types: interaction patterns plus workflow habits and QA checks.
- 06 Different subjects: biology-first pattern catalog and subject adaptations.
- 07 Local testing: preview and debug PG/PGML problems with a tight edit-preview loop.
- 90 Appendices: templates, cheat sheets, glossary, troubleshooting, and "further techniques".

## LibreTexts authoring rules (high importance)
This repo assumes LibreTexts import and LibreTexts navigation:
- Avoid HTML links (`<a href=...>`) in `Textbook/` content (LibreTexts provides its own TOC).
- Do not rely on JavaScript (`<script>` tags or inline event handlers).
- Every chapter index file named `X.0-Index.html` must end with `<p>{{template.ShowOrg()}}</p>`.
- Table format and other HTML conventions are documented in `docs/LIBRETEXTS_HTML_GUIDE.md`.

## Editing workflow
1. Edit or add chapter content in `Textbook/` (HTML).
2. Keep examples life-science-first and PGML-first (PG setup only as needed).
3. Align the page content with `Textbook/TEXTBOOK_PAGE_SUMMARIES.md`.
4. Record your change in `docs/CHANGELOG.md`.

## Validation
Run the local lint checks before considering HTML "done":
```bash
/opt/homebrew/bin/bash tests/run_html_lint.sh
/opt/homebrew/bin/bash tests/run_pyflakes.sh
```

## Source material (do not edit)
The extracted HTML in `Insight-HTML/` and `WebWorK-HTML/` is used as writing input. The textbook
content should integrate the useful ideas as prose and examples, not as copied pages.

## Example style reference (local)
If available on the same machine, use the Biology Problems OER style as a content and prompt
reference:
- `/Users/vosslab/nsh/biology-problems/`
- `/Users/vosslab/nsh/biology-problems-website/`
