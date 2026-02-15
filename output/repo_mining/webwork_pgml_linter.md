# Mining Report: webwork-pgml-linter

## Repo Overview

The webwork-pgml-linter is a Python-based static analysis tool that lints WeBWorK `.pg` problem files for modern PGML standards. It uses a modular plugin architecture with 44 built-in plugins (43 enabled by default, 1 disabled) that detect common authoring mistakes, deprecated patterns, and syntax errors without executing Perl. The linter parses PG files, strips comments and heredocs, extracts macro lists, identifies PGML regions, and runs each plugin against a shared context dictionary.

The tool is invoked via `pgml-lint -i file.pg` or `pgml-lint -d problems/` and supports custom rules via JSON configuration files, external plugin loading, PG version targeting (defaults to PG 2.17), and selective enable/disable of plugins. The plugin system follows a registration pattern where each plugin defines `PLUGIN_ID`, `PLUGIN_NAME`, `DEFAULT_ENABLED`, and a `run(context)` function returning issue dicts with severity (ERROR/WARNING), message, and optional line number.

## Lint Rules Catalog

### Category: Document Structure

- **Rule**: `document_pairs` - DOCUMENT/ENDDOCUMENT pairing
  - **Error message**: "DOCUMENT() present without ENDDOCUMENT()"
  - **Error message**: "ENDDOCUMENT() present without DOCUMENT()"
  - **Error message**: "DOCUMENT() count does not match ENDDOCUMENT() (start=N, end=N)"
  - **Error message**: "ENDDOCUMENT() appears before DOCUMENT()"
  - **Textbook reference**: Ch2 (Problem Generation PG), Ch7 (Testing and Debugging)

- **Rule**: `block_markers` - BEGIN/END block pairing
  - **Error message**: "END_PGML without matching BEGIN" (and variants for all block types)
  - **Error message**: "BEGIN_PGML without matching END" (and variants)
  - **Error message**: "BEGIN_PGML_HINT appears inside another PGML block" (nesting)
  - **Error message**: Mismatched pairs (e.g., BEGIN_PGML closed by END_TEXT)
  - **Textbook reference**: Ch3 (PGML), Ch7 (Testing and Debugging)

- **Rule**: `block_rules` - Custom block rule counts
  - **Error message**: "{label} counts do not match (start=N, end=N)"
  - **Error message**: "{label} appears only on one side (start=N, end=N)"
  - **Textbook reference**: Ch2 (Problem Generation PG)

- **Rule**: `pgml_text_blocks` - Deprecated TEXT blocks
  - **Error message**: "BEGIN_TEXT is deprecated legacy PG syntax; use BEGIN_PGML with PGML.pl for modern WebWork problems"
  - **Textbook reference**: Ch2 (Problem Generation PG), Ch3 (PGML)

### Category: PGML Heredocs

- **Rule**: `pgml_heredocs` - PGML heredoc terminators
  - **Error message**: "PGML heredoc terminator 'END_PGML' not found"
  - **Textbook reference**: Ch3 (PGML), Ch7 (Testing and Debugging)

### Category: Header/Metadata Quality

- **Rule**: `pgml_header_tags` - PG header tag quality
  - **Error message**: "Header contains smart quotes or non-ASCII punctuation"
  - **Error message**: "Missing DESCRIPTION block in header"
  - **Error message**: "DESCRIPTION block missing ENDDESCRIPTION"
  - **Error message**: "ENDDESCRIPTION present without DESCRIPTION"
  - **Error message**: "DESCRIPTION block is empty"
  - **Error message**: "DESCRIPTION block is long; keep to 1-4 sentences"
  - **Error message**: "Missing KEYWORDS tag in header"
  - **Error message**: "KEYWORDS tag is malformed; expected KEYWORDS('k1','k2',...)"
  - **Error message**: "KEYWORDS tag is empty"
  - **Error message**: "KEYWORDS should include at least 3 entries"
  - **Error message**: "KEYWORDS should include at most 10 entries"
  - **Error message**: "KEYWORDS contains duplicates: {list}"
  - **Error message**: "Missing DBsubject tag in header"
  - **Error message**: "DBsubject '{value}' is a placeholder or noisy value"
  - **Error message**: "Missing DBchapter tag in header"
  - **Error message**: "DBchapter is empty"
  - **Error message**: "DBchapter uses placeholder reference text"
  - **Error message**: "Missing DBsection tag in header"
  - **Error message**: "DBsection is empty"
  - **Error message**: "DBsection uses placeholder reference text"
  - **Textbook reference**: Ch2 (Problem Generation PG), Ch90 (Appendices - metadata)

### Category: Macro Loading

- **Rule**: `pgml_required_macros` - PGML requires PGML.pl
  - **Error message**: "PGML used without required macros: pgml.pl"
  - **Textbook reference**: Ch2 (Problem Generation PG), Ch3 (PGML)

- **Rule**: `pgml_loadmacros_integrity` - loadMacros syntax integrity
  - **Error message**: "loadMacros() missing closing parenthesis"
  - **Error message**: "loadMacros() missing trailing semicolon"
  - **Error message**: "loadMacros() has an empty macro list"
  - **Error message**: "loadMacros() entries appear to be missing a comma"
  - **Error message**: "loadMacros() contains smart quotes"
  - **Textbook reference**: Ch2 (Problem Generation PG), Ch7 (Testing and Debugging)

- **Rule**: `macro_rules` - Macro requirement coverage
  - **Error message**: "{label} used without required macros: {macros}"
  - **Error message**: "{label} requires PG {version}+ (target is PG {version})"
  - **Error message**: "{label} requires PG {version} or earlier (target is PG {version})"
  - Covers: Context/Compute/Formula/Real (MathObjects.pl), RadioButtons (parserRadioButtons.pl), CheckboxList, PopUp, DropDown, MultiAnswer, OneOf, NchooseK, FormulaUpToConstant, DataTable/LayoutTable (niceTables.pl), NumberWithUnits, Context('Fraction'), DraggableSubsets
  - **Textbook reference**: Ch2 (Problem Generation PG), Ch4 (Breaking Down Components), Ch5 (Different Question Types)

### Category: Seed/Randomization

- **Rule**: `pgml_seed_stability` - Seed stability checks
  - **Error message**: "rand() may bypass PG seeding; use random() or list_random()."
  - **Error message**: "srand() overrides PG seeding; avoid for stable seeds."
  - **Error message**: "time() makes values depend on the clock; avoid for stable seeds."
  - **Error message**: "localtime() makes values depend on the clock; avoid for stable seeds."
  - **Error message**: "gmtime() makes values depend on the clock; avoid for stable seeds."
  - **Error message**: "SRAND() resets the PG random generator; avoid for stable seeds."
  - **Error message**: "ProblemRandomize() reseeds across attempts; confirm this is intended."
  - **Error message**: "PeriodicRerandomization() reseeds by attempt; confirm this is intended."
  - **Error message**: Various rand_button/randomize helpers warnings
  - **Textbook reference**: Ch7 (Testing and Debugging - randomization testing)

- **Rule**: `pgml_seed_variation` - Seed variation detection
  - **Error message**: "No seed-based randomization detected; answer may not vary with seed"
  - Recognizes 35+ randomization patterns including random(), list_random(), shuffle(), NchooseK(), random_subset(), etc.
  - **Textbook reference**: Ch7 (Testing and Debugging - randomization testing)

### Category: Function Signatures

- **Rule**: `pgml_function_signatures` - Function signatures and empty args
  - **Error message**: "Function name '{name}' looks wrong; use '{correct}'" (typo detection: Popup->PopUp, Dropdown->DropDown, Radiobuttons->RadioButtons, Checkboxes->CheckboxList)
  - **Error message**: "{name}() called with no arguments; expected at least {N}"
  - **Error message**: "{name}() called with {N} args; expected at least {min}"
  - **Error message**: "{name}() called with {N} args; expected {max}"
  - **Error message**: "{name}() has an empty argument"
  - Covers: random (exactly 3), NchooseK (exactly 2), includePGproblem, Compute, Formula, Real, Vector, Matrix, DropDown, PopUp, RadioButtons, CheckboxList, NumberWithUnits, MultiAnswer, OneOf, FormulaUpToConstant
  - **Textbook reference**: Ch4 (Breaking Down Components), Ch5 (Different Question Types), Ch7 (Testing and Debugging)

### Category: PGML Inline Code

- **Rule**: `pgml_inline` - PGML inline markers [@ @]
  - **Error message**: "PGML inline close @] without matching [@"
  - **Error message**: "PGML inline open [@ without matching @]"
  - **Textbook reference**: Ch3 (PGML), Ch6 (Advanced PGML Techniques)

- **Rule**: `pgml_inline_braces` - PGML inline brace balance
  - **Error message**: "PGML inline code has unclosed '{' brace"
  - **Error message**: "PGML inline code has unbalanced '}' brace"
  - **Textbook reference**: Ch3 (PGML), Ch7 (Testing and Debugging)

- **Rule**: `pgml_inline_pgml_syntax` - PGML syntax inside inline code
  - **Error message**: "PGML tag wrapper token '[<' found inside [@ @] block"
  - **Error message**: "PGML tag wrapper token '>]{' found inside [@ @] block"
  - **Error message**: "Nested BEGIN_PGML found inside [@ @] block"
  - **Error message**: "Nested END_PGML found inside [@ @] block"
  - **Error message**: "PGML interpolation [$name] found inside [@ @] block; PGML parses once and will not re-parse strings"
  - **Textbook reference**: Ch3 (PGML), Ch6 (Advanced PGML Techniques), Ch7 (Testing and Debugging)

### Category: PGML Parse Hazards

- **Rule**: `pgml_pgml_parse_hazards` - PGML parse hazard checks
  - **Error message**: "Unknown PGML block token [{token}] may cause parser errors"
  - **Error message**: "PGML inline code has unbalanced parentheses"
  - **Error message**: "PGML tag wrapper '[<' must be closed before line break"
  - **Textbook reference**: Ch3 (PGML), Ch7 (Testing and Debugging)

### Category: MODES() Function Issues

- **Rule**: `pgml_modes_in_inline` - MODES inside inline eval blocks
  - **Error message**: "MODES() used inside [@ @] block; MODES returns 1 in eval context and will not emit HTML"
  - **Error message**: "MODES() inside [@ @] uses raw HTML layout; use TeX => '' for PG 2.17"
  - **Textbook reference**: Ch6 (Advanced PGML Techniques), Ch7 (Testing and Debugging)

- **Rule**: `pgml_modes_tex_payload` - MODES TeX payloads should be empty
  - **Error message**: "MODES() TeX payload is non-empty; use TeX => '' for PGML output"
  - **Textbook reference**: Ch6 (Advanced PGML Techniques)

- **Rule**: `pgml_modes_html_plain_text` - MODES HTML payloads without tags
  - **Error message**: "MODES() HTML payload has no HTML tags; replace with plain string instead of MODES()"
  - **Textbook reference**: Ch6 (Advanced PGML Techniques)

- **Rule**: `pgml_modes_html_escape` - MODES HTML escaped in interpolation
  - **Error message**: "Variable ${name} contains HTML from MODES() but is used in [$var] interpolation which escapes HTML; use [@ ${name} @]* instead to render HTML"
  - **Textbook reference**: Ch6 (Advanced PGML Techniques), Ch7 (Testing and Debugging)

### Category: PGML Answer Blanks

- **Rule**: `pgml_blanks` - PGML blank specs
  - **Error message**: "PGML blank missing answer spec"
  - **Error message**: "PGML blank spec has unbalanced braces"
  - **Error message**: "PGML blank spec is empty"
  - **Error message**: "PGML blank uses both payload and star specs"
  - **Textbook reference**: Ch3 (PGML), Ch5 (Different Question Types)

- **Rule**: `pgml_blank_assignments` - Variable assignment checking
  - **Error message**: "PGML blank references ${name} without assignment in file"
  - **Textbook reference**: Ch7 (Testing and Debugging)

### Category: PGML Markup Balance

- **Rule**: `pgml_brackets` - PGML bracket balance (DISABLED by default)
  - **Error message**: "PGML bracket open [ without matching ]"
  - **Error message**: "PGML bracket close ] without matching ["
  - **Textbook reference**: Ch3 (PGML)

- **Rule**: `pgml_underscore_emphasis` - PGML underscore emphasis balance
  - **Error message**: "PGML underscore emphasis not closed before paragraph ends"
  - **Textbook reference**: Ch3 (PGML)

### Category: HTML in PGML

- **Rule**: `pgml_html_in_text` - Raw HTML in PGML text
  - **Error message**: "Raw HTML <{tag}> tag in PGML text will be stripped or mangled; {suggestion}"
  - Covers 22 tags: strong, b, i, em, u, sub, sup, br, p, h1-h4, ul, ol, li, font, center, a, span, style
  - **Error message**: "HTML entity '{entity}' in PGML text may be mangled; use Unicode characters or LaTeX instead"
  - **Error message**: "HTML class \"tex2jax_ignore\" found in PGML text; this suppresses MathJax and often indicates rendering problems"
  - **Textbook reference**: Ch3 (PGML), Ch6 (Advanced PGML Techniques), Ch7 (Testing and Debugging)

- **Rule**: `pgml_html_policy` - HTML policy checks
  - **Error message**: "HTML <{tag}> tag detected; avoid raw HTML that can be sanitized" (script, iframe, object, embed = ERROR; style, form, input, img, a, svg, math, canvas, video, audio = WARNING)
  - **Error message**: "Escaped HTML tag &lt;{tag}&gt; detected; output may be escaping HTML"
  - **Error message**: "Inline <style> tag found outside HEADER_TEXT; may be sanitized"
  - **Error message**: "HTML class \"tex2jax_ignore\" found; MathJax is suppressed and output may not render"
  - **Error message**: "PGML tag wrapper uses <{tag}> which is disallowed or sanitized in this install"
  - **Textbook reference**: Ch6 (Advanced PGML Techniques), Ch7 (Testing and Debugging)

- **Rule**: `pgml_html_forbidden_tags` - Forbidden HTML table tags in PGML
  - **Error message**: "HTML <{tag}> tag found in PGML content; use DataTable() or LayoutTable() from niceTables.pl"
  - Covers: table, tr, td, th, thead, tbody, tfoot, colgroup, col
  - **Textbook reference**: Ch6 (Advanced PGML Techniques)

- **Rule**: `pgml_html_div` - HTML div tags in PGML
  - **Error message**: "HTML <div> tag found in PGML content; avoid HTML divs because they often render incorrectly"
  - **Error message**: "Escaped HTML <div> tag found in PGML output; this indicates HTML is being escaped instead of rendered"
  - PG 2.17 compatibility: raw `<div>` allowed when targeting PG 2.17
  - **Textbook reference**: Ch6 (Advanced PGML Techniques)

- **Rule**: `pgml_span_interpolation` - Span HTML interpolation checks
  - **Error message**: "Variable ${name} contains <span> HTML but is not interpolated with [$name] in PGML; HTML may be escaped"
  - **Textbook reference**: Ch6 (Advanced PGML Techniques)

- **Rule**: `pgml_html_var_passthrough` - HTML variables without passthrough
  - **Error message**: "Variable ${name} contains HTML but is output without raw passthrough; use [$name]* to avoid escaping"
  - **Textbook reference**: Ch6 (Advanced PGML Techniques)

### Category: PGML Tag Wrapper Issues

- **Rule**: `pgml_tag_wrapper_tex` - PGML tag wrappers with TeX payloads
  - **Error message**: "PGML tag wrapper has non-empty TeX payload; use an empty TeX payload unless needed"
  - **Textbook reference**: Ch6 (Advanced PGML Techniques)

- **Rule**: `pgml_pgml_wrapper_in_string` - PGML wrapper syntax in strings
  - **Error message**: "PGML tag wrapper syntax found inside a Perl string; PGML parses once and will not re-parse strings"
  - **Textbook reference**: Ch6 (Advanced PGML Techniques), Ch7 (Testing and Debugging)

- **Rule**: `pgml_style_string_quotes` - Unescaped quotes in PGML style strings
  - **Error message**: "PGML style tag inside single-quoted string contains unescaped single quotes; escape as \\' or use double quotes or q{...}"
  - **Textbook reference**: Ch6 (Advanced PGML Techniques)

### Category: Encoding/Characters

- **Rule**: `pgml_nbsp` - Non-breaking space detection
  - **Error message**: "Non-breaking space detected; replace with a normal space to avoid layout surprises"
  - **Textbook reference**: Ch7 (Testing and Debugging)

- **Rule**: `pgml_mojibake` - Mojibake/encoding glitches
  - **Error message**: "Possible mojibake sequence {token} detected; check for UTF-8/Latin-1 encoding mixups"
  - **Textbook reference**: Ch7 (Testing and Debugging)

### Category: TeX Rendering

- **Rule**: `pgml_tex_color` - TeX color command warnings
  - **Error message**: "TeX color commands (\\color, \\textcolor) do not render reliably in PGML; use PGML tag wrappers or HTML spans instead"
  - **Textbook reference**: Ch3 (PGML), Ch6 (Advanced PGML Techniques)

### Category: Code Quality

- **Rule**: `pgml_line_length` - Extreme line length warnings
  - **Error message**: "Line length {N} exceeds 200 characters"
  - **Error message**: "Line length {N} exceeds 400 characters"
  - **Error message**: "Long line without whitespace suggests embedded blob payload"
  - **Textbook reference**: Ch7 (Testing and Debugging)

- **Rule**: `pgml_blob_payloads` - Embedded blob payload detection
  - **Error message**: "Base64-like blob payload detected; consider removing embedded data"
  - **Error message**: "ggbbase64 payload marker detected; avoid embedded applet blobs"
  - **Error message**: "base64 payload marker detected; avoid embedded blobs"
  - **Textbook reference**: Ch7 (Testing and Debugging)

- **Rule**: `pgml_label_dot` - Label dot list parsing trap
  - **Error message**: "Label built as A. (chr(65 + $i) . '. ') can trigger PGML list parsing; use '*A.*' or 'A)' instead"
  - **Textbook reference**: Ch6 (Advanced PGML Techniques)

### Category: Legacy PG Syntax Detection

- **Rule**: `pgml_ans_style` - PGML answer style consistency
  - **Error message**: "ANS() call after END_PGML block (mixed style). Pure PGML uses inline answer specs: [_]{$answer} instead of ANS($answer->cmp())"
  - **Textbook reference**: Ch2 (Problem Generation PG), Ch3 (PGML), Ch5 (Different Question Types)

- **Rule**: `pgml_ans_rule` - Legacy ans_rule() function
  - **Error message**: "ans_rule() is deprecated legacy PG syntax; use PGML inline answer blanks like [_]{$answer} instead"
  - **Textbook reference**: Ch2 (Problem Generation PG), Ch3 (PGML)

- **Rule**: `pgml_br_variable` - Legacy $BR variable
  - **Error message**: "$BR is deprecated legacy PG syntax; use blank lines in PGML for paragraph breaks"
  - **Textbook reference**: Ch2 (Problem Generation PG), Ch3 (PGML)

- **Rule**: `pgml_old_answer_checkers` - Legacy answer checker functions
  - **Error message**: "{checker_name}() is deprecated legacy PG syntax; use MathObjects with ->cmp() method instead (e.g., $answer->cmp())"
  - Detects: num_cmp, str_cmp, fun_cmp, std_num_cmp, std_str_cmp, std_fun_cmp, std_num_str_cmp, strict_num_cmp, strict_str_cmp
  - **Textbook reference**: Ch2 (Problem Generation PG), Ch4 (Breaking Down Components)

- **Rule**: `pgml_solution_hint_macros` - Legacy SOLUTION/HINT macros
  - **Error message**: "SOLUTION() macro is deprecated legacy PG syntax; use BEGIN_PGML_SOLUTION...END_PGML_SOLUTION blocks instead"
  - **Error message**: "HINT() macro is deprecated legacy PG syntax; use BEGIN_PGML_HINT...END_PGML_HINT blocks instead"
  - **Textbook reference**: Ch3 (PGML), Ch5 (Different Question Types)

### Category: Include Files

- **Rule**: `pgml_include_pgproblem` - includePGproblem usage
  - **Error message**: "includePGproblem() used; target file not verified by linter"
  - **Error message**: "includePGproblem() appears to be the only content in this file"
  - **Textbook reference**: Ch2 (Problem Generation PG)

## Chapter Mapping

### Chapter 2: Problem Generation PG
- **Relevant files**: `pgml_lint/plugins/document_pairs.py`, `pgml_lint/plugins/pgml_required_macros.py`, `pgml_lint/plugins/pgml_loadmacros_integrity.py`, `pgml_lint/plugins/macro_rules.py`, `pgml_lint/plugins/pgml_include_pgproblem.py`, `pgml_lint/plugins/pgml_header_tags.py`, `pgml_lint/plugins/pgml_text_blocks.py`, `pgml_lint/plugins/pgml_ans_style.py`, `pgml_lint/plugins/pgml_ans_rule.py`, `pgml_lint/plugins/pgml_br_variable.py`, `pgml_lint/plugins/pgml_old_answer_checkers.py`
- **What to extract**: Structure rules (DOCUMENT/ENDDOCUMENT pattern), loadMacros() syntax, macro requirements per function, header metadata format, legacy-to-modern migration patterns
- **Example snippets**:
```perl
# Correct loadMacros structure (from loadmacros_integrity checks)
loadMacros(
    'PGstandard.pl',
    'PGML.pl',
    'MathObjects.pl',
);
# Missing comma error:
loadMacros(
    'PGstandard.pl'
    'PGML.pl'  # ERROR: missing comma
);
```
```perl
# Header tag format (from pgml_header_tags checks)
## DBsubject(Algebra)
## DBchapter(Linear Equations)
## DBsection(Solving for a variable)
## KEYWORDS('algebra', 'linear equations', 'solving')
## DESCRIPTION
## Solve a linear equation for x.
## ENDDESCRIPTION
```
- **Textbook gap it fills**: The textbook should document loadMacros() common errors and fix them, header metadata best practices with full examples

### Chapter 3: PGML
- **Relevant files**: `pgml_lint/plugins/block_markers.py`, `pgml_lint/plugins/pgml_heredocs.py`, `pgml_lint/plugins/pgml_inline.py`, `pgml_lint/plugins/pgml_blanks.py`, `pgml_lint/plugins/pgml_brackets.py`, `pgml_lint/plugins/pgml_underscore_emphasis.py`, `pgml_lint/plugins/pgml_html_in_text.py`, `pgml_lint/plugins/pgml_tex_color.py`, `pgml_lint/pgml.py`
- **What to extract**: PGML block types and pairing rules, inline code syntax [@ @], answer blank syntax [_]{$answer}, bracket and emphasis balance rules, PGML math delimiters, HTML-to-PGML migration table
- **Example snippets**:
```perl
# Answer blank syntax (from pgml_blanks checks)
[_]{$answer}        # basic blank with answer spec
[___]{$answer}      # wider blank (width is visual only)
[_]*{$answer}       # star spec for grading options
# ERRORS:
[_]                 # WARNING: missing answer spec
[_]{}               # WARNING: empty spec
[_]{$ans            # ERROR: unbalanced braces
```
```perl
# Inline code (from pgml_inline checks)
[@ $var @]          # inline Perl
[@ $var @]*         # raw HTML output
# ERRORS:
[@ $var             # WARNING: unclosed [@
@]                  # WARNING: unmatched @]
```
- **Textbook gap it fills**: Complete reference of valid PGML answer blank forms, emphasis/bracket pitfalls, HTML-to-PGML equivalents table

### Chapter 4: Breaking Down Components
- **Relevant files**: `pgml_lint/plugins/macro_rules.py`, `pgml_lint/plugins/pgml_function_signatures.py`, `pgml_lint/rules.py`, `pgml_lint/function_to_macro_pairs.py`
- **What to extract**: Function-to-macro mapping table, function signature requirements, MathObjects constructor patterns
- **Example snippets**:
```perl
# Function signature checks (from pgml_function_signatures)
random(1, 10, 1);       # OK: exactly 3 args
random(1, 10);           # ERROR: only 2 args, need 3
NchooseK(5, 3);          # OK: exactly 2 args
Compute("x^2");          # OK: at least 1 arg
Compute();               # WARNING: no arguments
# Typo detection:
Dropdown([...], 0);      # ERROR: use 'DropDown' not 'Dropdown'
Popup([...], "A");       # ERROR: use 'PopUp' not 'Popup'
```
- **Textbook gap it fills**: Exhaustive function signature reference, common typos table, macro dependency map

### Chapter 5: Different Question Types
- **Relevant files**: `pgml_lint/plugins/macro_rules.py`, `pgml_lint/plugins/pgml_function_signatures.py`, `pgml_lint/plugins/pgml_ans_style.py`, `pgml_lint/plugins/pgml_blanks.py`
- **What to extract**: Question type patterns (RadioButtons, CheckboxList, PopUp, DropDown, MultiAnswer, NumberWithUnits), required macros per question type, inline answer spec patterns
- **Example snippets**:
```perl
# Pure PGML style (encouraged):
$rb = RadioButtons(["A", "B", "C"], "A");
BEGIN_PGML
[_]{$rb}
END_PGML

# Mixed style (WARNING from pgml_ans_style):
BEGIN_PGML
[@ $rb->buttons() @]*
END_PGML
ANS($rb->cmp());  # WARNING: mixed style
```
- **Textbook gap it fills**: Question type checklist with required macros, pure PGML vs mixed style comparison

### Chapter 6: Advanced PGML Techniques
- **Relevant files**: `pgml_lint/plugins/pgml_modes_in_inline.py`, `pgml_lint/plugins/pgml_modes_tex_payload.py`, `pgml_lint/plugins/pgml_modes_html_plain_text.py`, `pgml_lint/plugins/pgml_modes_html_escape.py`, `pgml_lint/plugins/pgml_tag_wrapper_tex.py`, `pgml_lint/plugins/pgml_pgml_wrapper_in_string.py`, `pgml_lint/plugins/pgml_style_string_quotes.py`, `pgml_lint/plugins/pgml_html_div.py`, `pgml_lint/plugins/pgml_html_forbidden_tags.py`, `pgml_lint/plugins/pgml_html_policy.py`, `pgml_lint/plugins/pgml_span_interpolation.py`, `pgml_lint/plugins/pgml_html_var_passthrough.py`, `pgml_lint/plugins/pgml_label_dot.py`, `pgml_lint/plugins/pgml_inline_pgml_syntax.py`, `pgml_lint/plugins/pgml_inline_braces.py`, `pgml_lint/plugins/pgml_tex_color.py`
- **What to extract**: MODES() function correct usage, tag wrapper syntax, HTML passthrough patterns, TeX vs HTML rendering, inline code pitfalls, escape/passthrough semantics
- **Example snippets**:
```perl
# MODES() pitfalls (from pgml_modes_in_inline):
# WRONG: MODES inside [@ @] returns 1, not HTML
[@ MODES(TeX => '', HTML => '<b>bold</b>') @]*   # WARNING

# WRONG: [$var] escapes HTML (from pgml_modes_html_escape)
$html = MODES(TeX => '', HTML => '<b>bold</b>');
BEGIN_PGML
[$html]    # WARNING: HTML gets escaped
[@ $html @]*  # CORRECT: raw output
END_PGML
```
```perl
# Tag wrapper syntax (from pgml_tag_wrapper_tex, pgml_style_string_quotes):
[<div class="highlight">]{['div', class => 'highlight']}{['']}   # OK
[<div>]{['div']}{['\\parbox{5in}', '}']}  # WARNING: non-empty TeX payload
```
- **Textbook gap it fills**: Comprehensive MODES() guide, tag wrapper reference, HTML passthrough patterns, TeX/HTML duality

### Chapter 7: Testing and Debugging (KEY CHAPTER)
- **Relevant files**: ALL plugin files (44 plugins), `pgml_lint/engine.py`, `pgml_lint/parser.py`, `pgml_lint/pgml.py`, `pgml_lint/registry.py`, `docs/PGML_LINT_PLUGINS.md`, `docs/PGML_LINT_CONCEPTS.md`, `docs/PGML_LINT_ARCHITECTURE.md`
- **What to extract**: Complete lint rule reference, linter usage guide, common mistakes catalog with examples, seed stability and variation testing, QA checklist derived from lint rules, plugin enable/disable workflow
- **Example snippets**:
```bash
# Basic linting usage
pgml-lint -i path/to/file.pg
pgml-lint -d problems/

# Disable noisy plugins
pgml-lint --disable pgml_blank_assignments -d problems/

# Enable optional plugins
pgml-lint --enable pgml_brackets -d problems/

# Target specific PG version
pgml-lint --pg-version 2.17 -d problems/
```
```perl
# Seed stability (from pgml_seed_stability):
rand()                # WARNING: bypasses PG seeding
random(1, 10, 1)      # OK: uses PG seeded random
time()                # WARNING: clock dependency
$problemSeed          # OK: recognized as seed-aware

# Seed variation (from pgml_seed_variation):
# File with no random() calls: WARNING: no seed variation detected
```
- **Textbook gap it fills**: This is THE key chapter. Should include: full linter setup guide, categorized common mistakes with fixes, seed testing methodology, QA checklist matching all lint rules, troubleshooting flowcharts

### Chapter 8: Using AI Agents (placeholders)
- **Relevant files**: `docs/PGML_LINT_PLUGIN_DEV.md`
- **What to extract**: Plugin development patterns for AI-assisted lint rule creation
- **Textbook gap it fills**: How AI can help write custom lint rules

### Chapter 90: Appendices
- **Relevant files**: `pgml_lint/function_to_macro_pairs.py`, `pgml_lint/rules.py`, `docs/PGML_LINT_PLUGINS.md`
- **What to extract**: Complete function-to-macro mapping table, full lint rule reference table, PG version compatibility matrix
- **Textbook gap it fills**: Reference tables for macros, functions, and lint rules

## Top 10 Most Useful Files

1. **`docs/PGML_LINT_PLUGINS.md`** (1148 lines) - Complete plugin reference with examples, migration guides, and rationale. The most comprehensive single document for textbook content.
2. **`docs/PGML_LINT_CONCEPTS.md`** (298 lines) - PGML syntax concepts explained with common patterns and limitations. Perfect for Ch3 and Ch7.
3. **`pgml_lint/plugins/pgml_header_tags.py`** (282 lines) - 20+ header metadata checks with exhaustive validation rules for DBsubject/DBchapter/DBsection/KEYWORDS/DESCRIPTION.
4. **`pgml_lint/plugins/pgml_function_signatures.py`** (261 lines) - Function signature validation with typo detection and argument count rules for 16 PG functions.
5. **`pgml_lint/plugins/pgml_modes_in_inline.py`** (213 lines) - MODES() in eval context detection with PG 2.17 compatibility, demonstrating a subtle and common bug.
6. **`pgml_lint/plugins/pgml_html_in_text.py`** (161 lines) - Comprehensive HTML-to-PGML tag mapping for 22 HTML tags with PGML alternatives.
7. **`pgml_lint/plugins/pgml_seed_stability.py`** (97 lines) - 13 unseeded randomness patterns with clear messages explaining why each is problematic.
8. **`pgml_lint/plugins/pgml_seed_variation.py`** (122 lines) - 35+ randomization function patterns for detecting static problems.
9. **`pgml_lint/plugins/pgml_loadmacros_integrity.py`** (223 lines) - 5 syntax validation checks for loadMacros() with smart quote and missing comma detection.
10. **`pgml_lint/pgml.py`** (319 lines) - Core PGML parsing logic: inline spans, blank scanning, bracket balance, math span detection.

## Recommended Actions

1. **Build Ch7 "Common Mistakes" section from lint rules**: The 44 plugins represent a curated catalog of the most common WeBWorK authoring mistakes. Organize them into a troubleshooting guide categorized by error type (structure, syntax, legacy, HTML, encoding).

2. **Create a "Lint Rule Quick Reference" appendix**: A condensed table mapping each lint rule to its error message, severity, and fix. This directly serves as a QA checklist for problem authors.

3. **Write a "Legacy PG to Modern PGML Migration Guide" section**: The linter has 7 plugins specifically detecting legacy patterns (ans_rule, $BR, BEGIN_TEXT, SOLUTION/HINT macros, ANS() calls, old answer checkers). Each includes before/after migration examples that belong in Ch2/Ch3.

4. **Document MODES() function thoroughly in Ch6**: The linter dedicates 4 plugins to MODES() issues (modes_in_inline, modes_tex_payload, modes_html_plain_text, modes_html_escape), revealing this as one of the trickiest PGML topics. Include a decision tree for when/how to use MODES().

5. **Add "Seed Testing" section to Ch7**: The seed_stability and seed_variation plugins provide a complete catalog of randomization functions and anti-patterns. Build a "randomization testing checklist" from this data.

6. **Create a "Function Signature Reference" table**: The function_signatures plugin validates 16 PG functions with exact argument counts. This should be a reference table in Ch4 or Ch90.

7. **Document "HTML in PGML" rules comprehensively**: Four plugins handle HTML policy (html_in_text, html_policy, html_forbidden_tags, html_div), plus three handle HTML passthrough (span_interpolation, html_var_passthrough, modes_html_escape). This complex topic needs a dedicated section in Ch6 with clear rules about when HTML is allowed vs forbidden.

8. **Add the "Header Metadata" best practices**: The header_tags plugin validates 20+ header conditions. Document the full header template with all required fields, noisy DBsubject values to avoid, and KEYWORDS best practices (3-10 entries, no duplicates).

9. **Incorporate linter usage into Ch7 setup guide**: Document how to install and run the linter as part of the problem development workflow, including --pg-version targeting, --disable/--enable patterns, and interpreting output.

10. **Extract the function-to-macro mapping table**: The macro_rules plugin's DEFAULT_MACRO_RULES contains the canonical mapping of PG functions to required macro files. This should be an appendix table with columns: Function, Required Macros, PG Version, Notes.
