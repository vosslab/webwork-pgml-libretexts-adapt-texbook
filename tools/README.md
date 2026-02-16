# Tools

Single-purpose authoring and validation utilities for the textbook repo.

## PGML extraction and validation pipeline

The main workflow extracts PG problems from textbook HTML and validates them.

- `lint_textbook_problems.py` -- End-to-end pipeline: extract problems, validate via the pg-renderer, CSV report.
  ```bash
  source source_me.sh && python3 tools/lint_textbook_problems.py
  source source_me.sh && python3 tools/lint_textbook_problems.py -H http://localhost:3000
  ```
- `extract_textbook_pre_blocks.py` -- Extract `<pre>` blocks from textbook HTML into `.pg` files.
  ```bash
  source source_me.sh && python3 tools/extract_textbook_pre_blocks.py -d Textbook -o output/textbook_pre_blocks
  ```
- `textbook_code_block_validator.py` -- Scan `<pre>` blocks for unmatched PG/PGML markers.
  ```bash
  source source_me.sh && python3 tools/textbook_code_block_validator.py
  ```

## HTML tools

- `html_lint_checker.py` -- Lint textbook HTML for LibreTexts compatibility (no scripts, no event handlers).
  ```bash
  source source_me.sh && python3 tools/html_lint_checker.py -d Textbook
  ```
- `extract_url_links_from_html_file.py` -- Extract `href`/`src` links from an HTML file into a sorted text list.
  ```bash
  source source_me.sh && python3 tools/extract_url_links_from_html_file.py -i page.html
  ```

## Textbook utilities

- `textbook_html_to_pdf.py` -- Render textbook HTML to a compiled PDF via WeasyPrint.
  ```bash
  source source_me.sh && python3 tools/textbook_html_to_pdf.py
  ```
- `extract_textbook_yake_keywords.py` -- Run YAKE keyword extraction across textbook HTML for index candidates.
  ```bash
  source source_me.sh && python3 tools/extract_textbook_yake_keywords.py
  ```

## Other utilities

- `get_insight.py` -- Render URLs with Playwright and save simplified HTML snapshots.
  ```bash
  source source_me.sh && python3 tools/get_insight.py -i urls.txt -o output_dir
  ```
- `libretexts_map_json_to_page_id_csv.py` -- Extract section label to page ID mappings from a Remixer map JSON.
  ```bash
  source source_me.sh && python3 tools/libretexts_map_json_to_page_id_csv.py -i map.json
  ```
- `xml_formatter.py` -- Format XML files using lxml (in-place with `.bak` backup).
  ```bash
  source source_me.sh && python3 tools/xml_formatter.py -i file.xml
  ```
