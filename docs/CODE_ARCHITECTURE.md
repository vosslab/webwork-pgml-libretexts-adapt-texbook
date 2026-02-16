# Code architecture

## Overview
- This repo does not build an application; it maintains a LibreTexts-imported textbook in [Textbook/](../Textbook/).
- The primary workflow is: edit chapter HTML under [Textbook/](../Textbook/), keep content PGML-first, then lint HTML
  for LibreTexts compatibility.
- Supporting tooling lives in [tools/](../tools/) (authoring utilities) and [tests/](../tests/) (local verification
  scripts).

## Major components
- Textbook content ([Textbook/](../Textbook/))
  - What it does: the book chapters as LibreTexts-ready HTML.
  - Structure: chapters are folders; each chapter index file is named like `X.0-Index.html`.
  - Key constraints: no HTML links and no JavaScript in textbook pages; see the
    [LibreTexts HTML guide](LIBRETEXTS_HTML_GUIDE.md).
- HTML authoring rules ([LibreTexts HTML guide](LIBRETEXTS_HTML_GUIDE.md))
  - What it does: defines the allowed HTML patterns for LibreTexts import (tables, index footer, and disallowed tags).
  - Key dependency: enforced by [tools/html_lint_checker.py](../tools/html_lint_checker.py).
- HTML linting tool ([tools/html_lint_checker.py](../tools/html_lint_checker.py))
  - What it does: parses HTML fragments and rejects LibreTexts-incompatible patterns (for example `<script>`, event
    handler attributes, `javascript:` URLs, and non-anchor links unless explicitly allowed).
  - Key dependencies: `lxml` (HTML parsing).
  - Entry point: invoked by [tests/run_html_lint.sh](../tests/run_html_lint.sh).
- Test scripts ([tests/](../tests/))
  - What they do: run local checks for HTML compatibility and Python linting.
  - Entry points:
    - [tests/run_html_lint.sh](../tests/run_html_lint.sh) runs the HTML lint checker against `Textbook/`.
    - [tests/run_pyflakes.sh](../tests/run_pyflakes.sh) runs `pyflakes` over `*.py` and writes `pyflakes.txt` at repo
      root.
- Source material archives (`Insight-HTML/`, `WebWorK-HTML/`, `Links/`)
  - What they do: store extracted reference material used as writing input (do not edit as textbook content).
  - Notes: [tools/extract_url_links_from_html_file.py](../tools/extract_url_links_from_html_file.py) and
    [tools/get_insight.py](../tools/get_insight.py) relate to collecting these references.
- Web rendering fetch tool ([tools/get_insight.py](../tools/get_insight.py))
  - What it does: renders a URL list with Playwright and saves simplified HTML snapshots (one output file per URL)
    plus a tab-separated render log (`render_log.tsv`) in the chosen output directory.
  - Key dependencies: `playwright` (and Playwright browser installs, if not already present).
  - Notes: uses a persistent profile directory (default `pw-profile/`) and rate-limits via
    `time.sleep(random.random())`.

## Data flow
- PGML validation pipeline
  - [tools/lint_textbook_problems.py](../tools/lint_textbook_problems.py) orchestrates the full workflow:
    1. Extract `<pre>` blocks from `Textbook/` HTML (reuses [extract_textbook_pre_blocks.py](../tools/extract_textbook_pre_blocks.py))
    2. Filter to complete PG problems (contain both `DOCUMENT()` and `ENDDOCUMENT()`)
    3. Run static lint via [webwork_simple_lint.py](../tools/webwork_simple_lint.py) `lint_text_to_result()`
    4. If renderer is available, run renderer lint via [pglint.py](../tools/pglint.py) `lint_file_to_result()`
    5. Write `lint_report.csv` with per-problem results and print a console summary
  - Entry point: `source source_me.sh && python3 tools/lint_textbook_problems.py --skip-renderer`
  - Key dependencies: `lxml` (HTML parsing), `requests` (renderer API calls)
- Primary authoring flow
  - Edit chapter HTML under [Textbook/](../Textbook/) (PGML-first writing with minimal PG scaffolding).
  - Ensure chapter index pages end with the LibreTexts section listing include:
    - `<p>{{template.ShowOrg()}}</p>` (see the [LibreTexts HTML guide](LIBRETEXTS_HTML_GUIDE.md)).
  - From repo root, run local checks:
    - `bash tests/run_html_lint.sh` to enforce LibreTexts constraints.
    - `bash tests/run_pyflakes.sh` to check Python helper scripts (writes `pyflakes.txt`).
- Reference ingestion flow (optional)
  - Collect URLs (for example under `Links/`).
  - Run [tools/get_insight.py](../tools/get_insight.py) to render and save simplified HTML snapshots to a chosen output
    directory.
  - Use the saved snapshots as writing input for [Textbook/](../Textbook/) content (not as imported textbook pages).

## Testing and verification
- HTML linting: [tests/run_html_lint.sh](../tests/run_html_lint.sh) runs
  [tools/html_lint_checker.py](../tools/html_lint_checker.py) against `Textbook/`.
- Python linting: [tests/run_pyflakes.sh](../tests/run_pyflakes.sh) runs `pyflakes` across repo `*.py` and writes
  `pyflakes.txt` (ignored by `.gitignore`).

## Extension points
- New chapters and pages: add `*.html` pages under [Textbook/](../Textbook/) and update
  `Textbook/TEXTBOOK_PAGE_SUMMARIES.md`.
- New authoring rules: update the [LibreTexts HTML guide](LIBRETEXTS_HTML_GUIDE.md) and, when enforcement is needed,
  add checks to [tools/html_lint_checker.py](../tools/html_lint_checker.py).
- New utilities: add single-purpose scripts under [tools/](../tools/) and document the intended workflow in
  `README.md` (and in `docs/` when it is a reusable convention).
- New verification steps: add scripts under [tests/](../tests/) (keep them runnable directly and repo-root aware).

## Known gaps
- The chapter directory names listed in `README.md` do not match the current `../Textbook/` folder names; verify and
  update `README.md` if it is intended to be a canonical chapter map.
- There is no pinned dependency manifest for Python tooling in this repo; verify the intended install steps for
  `lxml`, `pyflakes`, and `playwright` before documenting a setup command.
