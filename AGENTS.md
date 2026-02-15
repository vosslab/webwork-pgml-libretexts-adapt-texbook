## Coding Style
See Python coding style in docs/PYTHON_STYLE.md.
See Markdown style in docs/MARKDOWN_STYLE.md.
See repo style in docs/REPO_STYLE.md.
When making edits, document them in docs/CHANGELOG.md.
When in doubt, implement the changes the user asked for rather than waiting for a response; the user is not the best reader and will likely miss your request and then be confused why it was not implemented or fixed.
When changing code always run tests, documentation does not require tests.
Agents may run programs in the tests folder, including smoke tests and pyflakes/mypy runner scripts.

## Project intent (read this first)
This repo is primarily a textbook/guide in the `Textbook/` folder, not a traditional software
project. Most work is writing and editing HTML chapter content that will be imported into
LibreTexts.

### Authoring constraints for `Textbook/`
- LibreTexts supports hyperlinks; prefer linking within the LibreTexts library, and avoid linking
  outside the library unless necessary (to reduce "link farming").
- When authoring offline, avoid relative file links (like `href="1.2-Page.html"`); add internal
  LibreTexts links using the LibreTexts editor/browse tool or verify the final URLs after import.
- The textbook cannot rely on JavaScript; do not add `<script>` tags or inline event handlers.
- Prefer PGML-focused writing; regular PG authoring is discouraged except for minimal setup.

### Content examples
Use the style of science prompts and structured data from the Biology Problems OER as a guide
when creating examples:
- `/Users/vosslab/nsh/biology-problems/`
- `/Users/vosslab/nsh/biology-problems-website/`

### Linting HTML
Run the local HTML lint checker when editing textbook HTML:
- `tests/run_html_lint.sh`

## Environment
Codex must run Python 3.12 using the repo bootstrap command pattern:
- `source source_me.sh && python ...`
Do not hard-code `/opt/homebrew/opt/python@3.12/bin/python3.12` in routine run commands.
On this user's macOS (Homebrew Python 3.12), Python modules are installed to `/opt/homebrew/lib/python3.12/site-packages/`.
