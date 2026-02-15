# AI Agent Content Expansion Guide

This document provides detailed instructions for expanding the skeletal HTML pages in the textbook
with comprehensive content from source documentation.

## Current State

All 53 HTML files have been created and pass HTML lint, but most are skeletal (46-88 lines) with
basic patterns only. They need expansion to 150-300 lines with detailed explanations, biology
examples, failure modes, and step-by-step guidance.

## Essential Reading Before Starting

1. **Master plan**: [Textbook/TEXTBOOK_PAGE_SUMMARIES.md](../Textbook/TEXTBOOK_PAGE_SUMMARIES.md)
   - Three-sentence summary for each page showing what content should be included
2. **Style constraints**: [docs/LIBRETEXTS_HTML_GUIDE.md](LIBRETEXTS_HTML_GUIDE.md)
   - HTML authoring rules, table format, no internal links
3. **Repo conventions**: [AGENTS.md](../AGENTS.md)
   - Textbook constraints, changelog requirements
4. **Migration notes**: [docs/TEXTBOOK_MIGRATION_GUIDE.md](TEXTBOOK_MIGRATION_GUIDE.md)
   - Content migration notes showing which biology examples go where

## Content Expansion Principles

### 1. Target length and structure
- **Skeletal pages (< 100 lines)**: Expand to 150-300 lines
- **Adequate pages (> 150 lines)**: Review and enhance examples
- **Structure**: Intro paragraph -> Use this when -> Main content sections -> Biology examples -> Apply it today

### 2. Biology-first examples
Every advanced technique page should include **3-5 short biology examples** (5-15 lines of PG code each):
- Show the pattern, not a complete problem
- Use realistic units, data, and scientific context
- Reference actual problems from biology-problems repo where applicable

### 3. Cross-referencing strategy
- **Forward references**: "See Chapter X for..." when a topic will be covered later
- **Backward references**: "Building on Chapter X..." when extending previous content
- **External references**: Cite source docs from OTHER_REPOS but do not link them in HTML
- **Internal flow**: Each chapter should feel self-contained while connecting to others

### 4. Failure modes and fixes
Every technique section should include:
- **Common failure**: What breaks and why
- **Symptom**: What the user sees (error message, wrong rendering)
- **Fix**: Step-by-step correction
- **Prevention**: How to avoid the failure

## Priority Order for Content Expansion

### Phase 1: High-priority pages (expand first)
These pages are referenced frequently and need comprehensive content:

1. **Chapter 2.2 OPL header** (currently 87 lines -> target 200 lines)
2. **Chapter 6.3 Matching** (currently 61 lines -> target 250 lines)
3. **Chapter 2.5 Common PG Macros** (currently 296 lines -> enhance with comparison table)
4. **Chapter 4.2 OPL Header** (currently 81 lines -> target 150 lines)
5. **Chapter 7.2 API usage** (currently 83 lines -> target 200 lines)

### Phase 2: Medium-priority pages
Foundation pages that need biology examples and failure modes:

6. **Chapter 6.1 Coloring** (currently 46 lines -> target 150 lines)
7. **Chapter 6.2 Tables** (currently 88 lines -> target 200 lines)
8. **Chapter 6.4 MC Statements** (currently 48 lines -> target 150 lines)
9. **Chapter 6.5 Randomization** (currently 48 lines -> target 180 lines)
10. **Appendix 90.1 Templates** (currently 147 lines -> enhance examples)

### Phase 3: Enhancement phase
Pages that are adequate but could use refinement:

11. Chapter 4 sections (add more failure mode examples)
12. Chapter 5 question types (add biology context)
13. Chapter 3 PGML sections (add science-specific examples)

## Detailed Page-by-Page Expansion Instructions

---

## Chapter 2.2: OPL Header and Metadata

**Current**: 87 lines, basic table and examples
**Target**: 200 lines
**Priority**: High (referenced throughout)

### Source documents
Primary: `OTHER_REPOS-do_not_commit/biology-problems/docs/webwork/WEBWORK_HEADER_STYLE.md`

### Content to add

1. **Expand TITLE field guidance** (add 20 lines):
   - Show 3-4 biology examples of good vs bad titles
   - "Compute dilution factor" (good) vs "This is a problem about dilutions" (bad)
   - Character count guidelines (< 80 chars)

2. **Expand DESCRIPTION block** (add 30 lines):
   - Template with placeholders
   - 3 complete biology examples:
     - Enzyme kinetics problem description
     - Genetics cross problem description
     - Dilution series problem description
   - What NOT to include (no solutions, no code)

3. **Expand KEYWORDS guidance** (add 25 lines):
   - Show keyword selection process for 3 biology problems
   - Good: `'serial dilution', 'concentration', 'stock solution'`
   - Bad: `'biology', 'lab', 'science'` (too generic)
   - Show how to avoid duplicating DBsubject terms

4. **Expand DBsubject/DBchapter/DBsection** (add 40 lines):
   - Table showing biology-appropriate classifications:
     - `DBsubject('Biology - molecular')`
     - `DBsubject('Biology - introductory')`
     - `DBsubject('Biochemistry')`
     - `DBsubject('Genetics')`
   - Decision tree: how to choose the right subject
   - 3 complete examples showing subject/chapter/section for different problem types

5. **Add complete worked examples section** (add 30 lines):
   - Full OPL header for a dilution problem
   - Full OPL header for a genetics problem
   - Full OPL header for a pathway problem
   - Point to Appendix 90.1 for more templates

6. **Add common mistakes section** (add 15 lines):
   - Empty DBsubject strings
   - Smart quotes in header (breaks parsing)
   - Missing ENDDESCRIPTION tag
   - Too many keywords (> 5)

### Cross-references to add
- Forward: "See Chapter 4.2 for how this header fits into a complete problem"
- Forward: "Templates in Appendix 90.1 include complete OPL headers"
- Backward: "Building on the five-section structure introduced in Chapter 2.0"

---

## Chapter 6.3: Matching Problems

**Current**: 61 lines, basic MODES explanation
**Target**: 250 lines
**Priority**: High (most complex pattern, MODES explanation here)

### Source documents
Primary: `OTHER_REPOS-do_not_commit/biology-problems/docs/webwork/MATCHING_PROBLEMS.md`
Secondary: `OTHER_REPOS-do_not_commit/biology-problems/problems/matching_sets/yaml_match_to_pgml.py` (first 200 lines)

### Content to add

1. **Expand intro and when to use matching** (add 20 lines):
   - Matching vs multiple choice decision guide
   - Best for: definitions, associations, component identification
   - Not ideal for: memorization, sequence ordering
   - Typical problem sizes: 4-8 pairs

2. **Complete PopUp widget section** (add 40 lines):
   - Full example showing widget creation:
     ```perl
     my @choices = ('A', 'B', 'C', 'D');
     my @answer_dropdowns = map { PopUp(\@choices, $shuffle[$_]) } 0 .. $#questions;
     ```
   - Explain shuffle array and correct answer mapping
   - Show how to load `parserPopUp.pl`
   - Note: DropDown is PG 2.18+ (not in ADAPT/renderer subset)

3. **Expand MODES explanation with examples** (add 50 lines):
   - Show BOTH patterns side by side:
     - Pattern 1: Wrapper tags directly in PGML (preferred when possible)
     - Pattern 2: MODES when wrapper must be in eval block
   - Complete working example of Pattern 1:
     ```perl
     BEGIN_PGML
     Match each term with its definition.

     <div class="two-column">
     <div>
     [@ join("\n\n", map { ... } @questions) @]**
     </div>
     <div>
     [@ join("\n\n", map { ... } @answers) @]**
     </div>
     </div>
     END_PGML
     ```
   - Complete working example of Pattern 2 (MODES required):
     ```perl
     [@ MODES(HTML => '<div class="two-column"><div>') @]*
     [@ join(...) @]**
     [@ MODES(HTML => '</div><div>') @]*
     [@ join(...) @]**
     [@ MODES(HTML => '</div></div>') @]*
     ```
   - Explain WHY Pattern 2 needs MODES (wrapper HTML gets escaped otherwise)
   - Show what happens when you forget MODES (layout collapses)

4. **Add CSS styling section** (add 30 lines):
   - Complete HEADER_TEXT example with flexbox CSS:
     ```perl
     HEADER_TEXT(MODES(HTML => <<END_STYLE));
     <style>
     .two-column {
       display: flex;
       flex-wrap: wrap;
       gap: 2rem;
       align-items: flex-start;
       justify-content: space-evenly;
     }
     </style>
     END_STYLE
     ```
   - Alternative: use justify-content, align-items options
   - Mobile-friendly considerations (flex-wrap)

5. **Add colored labels section** (add 35 lines):
   - When to use fixed label colors vs position-based
   - Build color mapping in Perl:
     ```perl
     my %answer_html = (
       'polar covalent bond' => '<span style="color: #00b3b3; font-weight:700;">polar covalent bond</span>',
       'ionic bond' => '<span style="color: #009900; font-weight:700;">ionic bond</span>',
       'hydrogen bond' => '<span style="color: #e60000; font-weight:700;">hydrogen bond</span>',
     );
     my @answers_html = map { $answer_html{$_} } @answers;
     ```
   - Show how to emit with `[$answers_html[$shuffle[$_]]]*` (trailing `*` required)
   - Cross-reference Chapter 6.1 for more on `[$var]*` pattern

6. **Add biology examples section** (add 45 lines):
   - **Example 1: Chemical bond types** (15 lines)
     - Left column: molecular scenarios ("Two oxygen atoms share electrons equally")
     - Right column: bond types (polar covalent, non-polar covalent, ionic, hydrogen)
     - Show shuffle and color mapping
   - **Example 2: Pathway components** (15 lines)
     - Left column: enzyme functions ("Converts glucose-6-phosphate to fructose-6-phosphate")
     - Right column: enzyme names (phosphoglucose isomerase, hexokinase, etc.)
   - **Example 3: Genetics terminology** (15 lines)
     - Left column: definitions ("Observable physical characteristic")
     - Right column: terms (phenotype, genotype, allele, locus)

7. **Add common failures section** (add 30 lines):
   - **Failure 1**: Forgot trailing `*` on colored labels
     - Symptom: See raw `<span>` tags in rendered problem
     - Fix: Use `[$var]*` not `[$var]`
   - **Failure 2**: Used MODES for everything
     - Symptom: Wasteful code, no actual benefit
     - Fix: Only use MODES for wrapper divs in eval blocks
   - **Failure 3**: Shuffle array index mismatch
     - Symptom: Wrong answers marked correct
     - Fix: Verify `$shuffle[$_]` indexing in both columns
   - **Failure 4**: PopUp choices don't match answer labels
     - Symptom: Dropdown shows wrong letters
     - Fix: Use same `@choices` array for PopUp creation and right column

### Cross-references to add
- Backward: "Building on PGML basics from Chapter 3"
- Backward: "Uses `[$var]*` pattern from Chapter 6.1"
- Forward: "For statement-based questions, see Chapter 6.4"
- External: "See yaml_match_to_pgml.py in biology-problems for production patterns"

---

## Chapter 2.5: Common PG Macros

**Current**: 296 lines, already substantial
**Target**: Enhance with version comparison table (add 50-75 lines)
**Priority**: High (frequently referenced)

### Source documents
Primary: `docs/PG_MACRO_VERSION_COMPARISON.md`
Secondary: `OTHER_REPOS-do_not_commit/biology-problems/docs/webwork/PG_2_17_RENDERER_MACROS.md`

### Content to add

1. **Add macro version comparison section** (add 60 lines):
   - Insert after the "Macro requirements" section
   - New heading: "## Macro availability across PG versions"
   - Intro paragraph: Explain that ADAPT/renderer uses a PG 2.17 subset
   - Table comparing key macros (copy from PG_MACRO_VERSION_COMPARISON.md):
     - Parser widgets row (PopUp, RadioButtons, CheckboxList)
     - Core macros row (all)
     - Table macros row (niceTables)
     - Context macros row (most, some)
   - After table: "What this means for you" section
     - Use PopUp/RadioButtons, not CheckboxList
     - For statement-based questions, use RadioButtons per statement (Chapter 6.4)
     - Always check the allowlist before copying from online examples

2. **Add "When a macro is missing" section** (add 20 lines):
   - Symptoms of missing macro:
     - "Can't locate [MacroFile].pl" error
     - Functions undefined at render time
   - How to diagnose:
     - Check PG_2_17_RENDERER_MACROS.md allowlist
     - Test locally with Chapter 7 renderer
   - Workarounds:
     - Find alternative macro from allowlist
     - Rewrite pattern (e.g., checkboxes -> RadioButtons per statement)

### Cross-references to add
- Forward: "See Chapter 6.4 for RadioButtons-per-statement pattern (CheckboxList alternative)"
- Forward: "See Chapter 7 for testing with local renderer to catch missing macros"
- External: "Complete allowlist in PG_2_17_RENDERER_MACROS.md"

---

## Chapter 6.1: Coloring Text and Emphasis

**Current**: 46 lines
**Target**: 150 lines
**Priority**: Medium

### Source documents
Primary: `OTHER_REPOS-do_not_commit/biology-problems/docs/webwork/COLOR_TEXT_IN_WEBWORK.md`

### Content to add

1. **Expand PGML tag wrapper section** (add 25 lines):
   - Full syntax explanation: `[<text>]{['span', style => '...']}{['','']}`
   - CSS properties to use: color (hex codes), font-weight (700 for bold), font-style
   - 3 examples:
     - ABOVE (orange bold)
     - BELOW (green bold)
     - NOT (red bold)
   - When to use: directional cues, negation, critical qualifiers

2. **Expand HTML variable pattern** (add 30 lines):
   - Show building HTML in setup:
     ```perl
     my $above = "<span style='color:#d96500; font-weight:700;'>ABOVE</span>";
     my $below = "<span style='color:#1f7a1f; font-weight:700;'>BELOW</span>";
     ```
   - Show using in PGML: `[$above]*` (trailing `*` is critical)
   - Compare `[$above]*` (works) vs `[$above]` (broken - shows raw tags)

3. **Add CSS class approach** (add 25 lines):
   - Alternative to inline styles: define classes in HEADER_TEXT
   - Example:
     ```perl
     HEADER_TEXT(MODES(HTML => <<'END_STYLE'));
     <style>
     .emph-above { color:#d96500; font-weight:700; }
     .emph-below { color:#1f7a1f; font-weight:700; }
     </style>
     END_STYLE
     ```
   - Then use: `[<ABOVE>]{['span', class => 'emph-above']}{['','']}`
   - Benefit: consistent colors across problem, easier to change

4. **Add biology examples** (add 40 lines):
   - **Example 1: pH vs pKa** (12 lines)
     - Scenario: "When pH is two units ABOVE the pKa..."
     - Show ABOVE and BELOW colored differently
   - **Example 2: Concentration threshold** (12 lines)
     - Scenario: "Which ions are ABOVE 10 mM threshold?"
     - Show threshold value colored
   - **Example 3: Gel migration** (12 lines)
     - Scenario: "Smaller fragments migrate FARTHER"
     - Show directional cue colored

5. **Add "Why TeX color fails" explanation** (add 15 lines):
   - TeX commands like `\color{...}` or `\textcolor{...}` do not work in this install
   - Backslashes get wrapped in `tex2jax_ignore` spans
   - MathJax never processes the color commands
   - Stick with HTML spans for reliability

6. **Add common failures** (add 15 lines):
   - Forgot trailing `*`: See raw `<span>` in output
   - Used MathJax color: No color appears
   - Inline style has syntax error: Span may not render

### Cross-references to add
- Forward: "Chapter 6.3 shows colored labels in matching problems"
- Forward: "Chapter 6.4 shows emphasis in statement-based questions"
- Backward: "Uses PGML basics from Chapter 3.1"

---

## Chapter 6.2: Tables with niceTables

**Current**: 88 lines
**Target**: 200 lines
**Priority**: Medium

### Source documents
Primary: `OTHER_REPOS-do_not_commit/biology-problems/docs/webwork/NICETABLES_TRANSLATION_PLAN.md`
Secondary: niceTables.pl documentation (if available in renderer)

### Content to add

1. **Expand DataTable vs LayoutTable decision** (add 30 lines):
   - Decision tree graphic (as text):
     - Does the table have column headers or caption? -> DataTable
     - Is it semantic data (measurements, observations)? -> DataTable
     - Is it pure visual layout (two-column list, widget grid)? -> LayoutTable
   - 3 examples showing decision:
     - Enzyme kinetics data with [S] and V&#x2080; columns -> DataTable
     - Serial dilution results -> DataTable
     - Two-column choice layout -> LayoutTable

2. **Add complete DataTable example** (add 40 lines):
   - Build 2D array in Perl:
     ```perl
     my @data = (
       ['[Substrate] (mM)', 'Velocity (&micro;mol/min)'],
       ['0.5', '1.2'],
       ['1.0', '2.1'],
       ['2.0', '3.5'],
       ['5.0', '5.8'],
     );
     ```
   - Create DataTable with options:
     ```perl
     BEGIN_PGML
     [@ DataTable(
       \@data,
       caption => 'Enzyme kinetics data',
       horizontalrules => 1,
       align => '| r | r |',
     ) @]*
     END_PGML
     ```
   - Explain each option: caption, horizontalrules, align, center

3. **Add complete LayoutTable example** (add 30 lines):
   - Two-column layout for choices:
     ```perl
     my @left = map { "[$_. ]" } (1..4);
     my @right = ('Choice A', 'Choice B', 'Choice C', 'Choice D');
     my @rows = map { [$left[$_], $right[$_]] } (0..3);

     BEGIN_PGML
     [@ LayoutTable(\@rows, align => 'l l') @]*
     END_PGML
     ```

4. **Add biology examples section** (add 60 lines):
   - **Example 1: Serial dilution series** (20 lines)
     - Table with tube number, dilution factor, final concentration
     - Show how to build with randomized starting concentration
   - **Example 2: Enzyme kinetics measurements** (20 lines)
     - Table with [S], V&#x2080;, 1/[S], 1/V&#x2080; for Lineweaver-Burk
     - Show LaTeX in cells for units: `[@ '[$[S]$]* (mM)' @]*`
   - **Example 3: Gel band interpretation** (20 lines)
     - Table with lane, sample, band sizes
     - Show how to format band sizes with units

5. **Add common failures** (add 20 lines):
   - Used HTML `<table>` tags directly: Blocked by whitelist, renders garbage
   - Forgot `\@data` reference: Type error
   - Mixed DataTable and LayoutTable use cases: Confusing output
   - Alignment string wrong: Table formatting breaks

6. **Add options reference** (add 20 lines):
   - Table of common options:
     - `caption => 'text'` (DataTable only)
     - `horizontalrules => 1` (adds lines between rows)
     - `align => '| l | c | r |'` (left, center, right alignment)
     - `center => 1` (centers entire table)
     - `tablecss => 'custom-class'` (add CSS class)

### Cross-references to add
- Backward: "Building on PGML from Chapter 3.4"
- Forward: "For two-column matching, see Chapter 6.3 (use LayoutTable or flexbox)"
- Note: "HTML table tags (table, tr, td, th) are blocked - niceTables.pl is the only supported way"

---

## Chapter 6.4: Multiple Choice Statements

**Current**: 48 lines
**Target**: 150 lines
**Priority**: Medium

### Source documents
Primary: `OTHER_REPOS-do_not_commit/biology-problems/docs/webwork/PGML_QUESTION_TYPES.md` (MC sections)
Secondary: `OTHER_REPOS-do_not_commit/biology-problems/problems/multiple_choice_statements/yaml_mc_statements_to_pgml.py` (first 200 lines)

### Content to add

1. **Expand when to use statement-based** (add 25 lines):
   - Statement-based vs single-best-answer decision guide
   - Best for: Evaluating multiple independent claims
   - Not ideal for: Single fact recall, when only one answer makes sense
   - Pattern: RadioButtons (True/False) or PopUp per statement
   - Why not CheckboxList: Not available in PG 2.17 subset

2. **Add complete RadioButtons pattern** (add 40 lines):
   - Setup code:
     ```perl
     my @statements = (
       'The control group received no treatment.',
       'The treatment group received the experimental drug.',
       'Both groups were the same size.',
     );
     my @correct = ('True', 'True', 'False');  # Based on scenario

     my @radios = map {
       RadioButtons(['True', 'False'], $correct[$_],
                    labels => 'AB', displayLabels => 0)
     } (0 .. $#statements);
     ```
   - PGML rendering:
     ```perl
     BEGIN_PGML
     Evaluate each statement about the experiment:

     1. [$statements[0]]
        [_]{$radios[0]}

     2. [$statements[1]]
        [_]{$radios[1]}

     3. [$statements[2]]
        [_]{$radios[2]}
     END_PGML
     ```

3. **Add biology examples section** (add 50 lines):
   - **Example 1: Experimental design** (18 lines)
     - Scenario paragraph about a drug trial
     - 4 statements about controls, randomization, blinding, sample size
     - Show setup and PGML
   - **Example 2: Pathway regulation** (16 lines)
     - Scenario about insulin signaling pathway
     - 3 statements about activators, inhibitors, feedback loops
     - Show how to emphasize key words (ACTIVATES, INHIBITS) with colors from 6.1
   - **Example 3: Molecular structure claims** (16 lines)
     - Scenario about a molecule
     - 4 statements about polarity, hydrogen bonding, charge
     - Show how to integrate colored emphasis

4. **Add emphasis integration** (add 20 lines):
   - Show how to build statements with colored key words:
     ```perl
     my $activates = "<span style='color:#009900; font-weight:700;'>ACTIVATES</span>";
     my $inhibits = "<span style='color:#e60000; font-weight:700;'>INHIBITS</span>";

     my @statements = (
       "Insulin [$activates]* the PI3K pathway.",
       "PTEN [$inhibits]* the PI3K pathway.",
     );
     ```
   - Cross-reference Chapter 6.1 for more on `[$var]*` pattern

5. **Add common failures** (add 15 lines):
   - Used CheckboxList: Macro not available in subset
   - Forgot to create separate RadioButtons for each statement: All statements share one widget
   - Answer array index mismatch: Wrong statements marked correct
   - Colored emphasis without `*`: Raw HTML shows in statement

### Cross-references to add
- Backward: "Uses RadioButtons from Chapter 2.5"
- Backward: "Uses colored emphasis from Chapter 6.1"
- Forward: "For matching pairs, see Chapter 6.3"
- Note: "CheckboxList (parserCheckboxList.pl) is not available in the PG 2.17 subset"

---

## Chapter 6.5: Advanced Randomization Patterns

**Current**: 48 lines
**Target**: 180 lines
**Priority**: Medium

### Source documents
Primary: `OTHER_REPOS-do_not_commit/biology-problems/docs/webwork/RANDOMIZATION_REFERENCE.md`
Secondary: `WEBWORK_PROBLEM_AUTHOR_GUIDE.md` (randomization sections)

### Content to add

1. **Expand guard patterns** (add 40 lines):
   - Why guards are needed: Avoid degenerate cases
   - Common guards:
     - Avoid zero denominators
     - Avoid repeated values in choice sets
     - Avoid invalid domains (log of negative, sqrt of negative)
     - Bound magnitudes for readability
   - 4 complete examples:
     - Guard for division: `do { $b = random(2,9); } while ($b == 0);`
     - Guard for distinct values: `do { $b = random(2,9); } while ($b == $a);`
     - Guard for positive (log domain): `do { $x = random(-5,5); } while ($x <= 0);`
     - Guard for reasonable magnitude: `do { $conc = random(0.1, 10, 0.1); } while ($conc > 5);`

2. **Expand deterministic seeding** (add 30 lines):
   - Use built-in problemSeed: `$envir{problemSeed}` or `$problemSeed`
   - Why deterministic matters: Same seed -> same problem -> reproducible debugging
   - For local PGrandom instance:
     ```perl
     my $rng = PGrandom->new();
     $rng->srand($envir{problemSeed});
     my $value = $rng->random(1, 10, 1);
     ```
   - Avoid hash key order issues: sort keys before selection
     ```perl
     my @keys = sort keys %data;
     my $selected = $keys[random(0, $#keys)];
     ```

3. **Add randomization functions reference** (add 40 lines):
   - Table of common functions from RANDOMIZATION_REFERENCE.md:
     - `random(begin, end, incr)` - Basic random integer
     - `non_zero_random(begin, end, incr)` - Avoids zero
     - `list_random(@list)` - Pick one from list
     - `random_subset(n, @set)` - Pick n distinct items
     - `shuffle(n)` - Permutation of 0..(n-1)
   - When to use each:
     - `random`: Numeric parameters, simple selection
     - `list_random`: Picking one choice from predefined list
     - `random_subset`: Selecting multiple distinct items (e.g., 4 from 8 questions)
     - `shuffle`: Reordering items (e.g., answer choices)

4. **Add biology examples section** (add 50 lines):
   - **Example 1: Randomized dilution factors** (18 lines)
     - Pick stock concentration from realistic range
     - Guard: Avoid factors that make final concentration too small
     - Show: `my $stock = random(10, 100, 5);  # 10-100 mM in 5 mM steps`
     - Guard: `do { $factor = random(2, 20); } while ($stock/$factor < 0.5);`
   - **Example 2: Genetics crosses** (16 lines)
     - Randomize parent genotypes from valid combinations
     - Guard: Ensure at least one heterozygote for interesting cross
     - Show allele selection and guard
   - **Example 3: qPCR Ct values** (16 lines)
     - Randomize control Ct in realistic range (15-25)
     - Randomize treatment offset (0.5-3 cycles)
     - Guard: Ensure Ct values stay in valid range (< 35)
     - Calculate fold change deterministically from Ct values

5. **Add interaction constraints** (add 20 lines):
   - When multiple random values interact:
     - Example: Km and [S] in enzyme kinetics must be in reasonable ratio
     - Example: Dilution series must have monotonic concentrations
   - Pattern: Generate first value, then constrain second based on first
   - Show example:
     ```perl
     my $Km = random(0.5, 5.0, 0.1);  # mM
     my $S = random($Km * 0.2, $Km * 5, 0.1);  # Keep [S] near Km
     ```

### Cross-references to add
- Backward: "Building on PG basics from Chapter 2.1"
- Forward: "Use in matching (6.3) and statements (6.4)"
- Note: "For reproducible debugging, record problemSeed (see Chapter 7.1)"

---

## Chapter 7.2: API Usage for Scripts

**Current**: 83 lines
**Target**: 200 lines
**Priority**: High (automation/linting use case)

### Source documents
Primary: `OTHER_REPOS-do_not_commit/webwork-pg-renderer/docs/RENDERER_API_USAGE.md`
Secondary: `OTHER_REPOS-do_not_commit/webwork-pg-renderer/README.md`

### Content to add

1. **Expand endpoint explanation** (add 30 lines):
   - POST / (primary, modern)
   - POST /render-api (compatibility, legacy)
   - GET /health (check if renderer is up)
   - Show health check example:
     ```bash
     curl http://localhost:3000/health
     # Returns: {"status":"ok"}
     ```
   - When to use which endpoint: Use POST / for new scripts

2. **Expand parameter precedence** (add 40 lines):
   - Order: problemSourceURL > problemSource > sourceFilePath
   - **problemSourceURL**: Fetch from URL, expects JSON with `raw_source` field
     - Use when: Problem source lives on remote server
     - Example: `problemSourceURL: 'https://example.com/problems/123.json'`
   - **problemSource**: Raw PG source string (can be base64 encoded)
     - Use when: Source is in memory, script-generated, or filesystem unavailable
     - Example: `problemSource: '## DESCRIPTION\n...'`
   - **sourceFilePath**: Path relative to Library/, Contrib/, or private/
     - Use when: File exists in renderer container filesystem
     - Example: `sourceFilePath: 'private/myproblem.pg'`
   - Which to choose: If file is outside container, use problemSource

3. **Add curl examples** (add 50 lines):
   - **Example 1: Render with sourceFilePath** (form-encoded)
     ```bash
     curl -X POST "http://localhost:3000/render-api" \
       -H "Content-Type: application/x-www-form-urlencoded" \
       --data-urlencode "sourceFilePath=private/dilution.pg" \
       --data-urlencode "problemSeed=1234" \
       --data-urlencode "_format=json"
     ```
   - **Example 2: Render with problemSource** (JSON)
     ```bash
     curl -X POST "http://localhost:3000/" \
       -H "Content-Type: application/json" \
       -d '{
         "problemSource": "## DESCRIPTION\n...",
         "problemSeed": 1234,
         "_format": "json"
       }'
     ```
   - **Example 3: Get HTML output**
     ```bash
     curl -X POST "http://localhost:3000/" \
       -H "Content-Type: application/json" \
       -d '{
         "sourceFilePath": "private/enzyme_kinetics.pg",
         "problemSeed": 5678,
         "_format": "html"
       }' > output.html
     ```

4. **Add Python example** (add 40 lines):
   - Using requests library:
     ```python
     import requests

     # Read problem file
     with open('myproblem.pg', 'r') as f:
         pg_source = f.read()

     # Render via API
     response = requests.post(
         'http://localhost:3000/',
         json={
             'problemSource': pg_source,
             'problemSeed': 1234,
             '_format': 'json',
             'isInstructor': 1,
         }
     )

     data = response.json()
     if data.get('flags', {}).get('error_flag'):
         print('Render error!')
     else:
         print('Success!')
     ```
   - Explain isInstructor flag (unlocks instructor-only fields)

5. **Add lint workflow example** (add 30 lines):
   - Pattern for linting multiple files:
     ```python
     import os
     import requests

     def lint_pg_file(filepath, seed=1000):
         with open(filepath) as f:
             source = f.read()

         resp = requests.post('http://localhost:3000/', json={
             'problemSource': source,
             'problemSeed': seed,
             '_format': 'json',
         })

         data = resp.json()
         warnings = data.get('debug', {}).get('pg_warn', [])
         error_flag = data.get('flags', {}).get('error_flag', 0)

         if error_flag or warnings:
             print(f'{filepath}: FAIL')
             for w in warnings:
                 print(f'  {w}')
         else:
             print(f'{filepath}: OK')

     for root, dirs, files in os.walk('problems/'):
         for f in files:
             if f.endswith('.pg'):
                 lint_pg_file(os.path.join(root, f))
     ```

6. **Add response format explanation** (add 20 lines):
   - JSON structure fields:
     - `renderedHTML`: The rendered problem HTML
     - `flags.error_flag`: 0 = success, 1 = error
     - `debug.pg_warn`: Array of warning messages
     - `answers`: (when isInstructor=1) Answer structure
   - HTML format: Returns full HTML page directly

### Cross-references to add
- Backward: "Uses problemSeed from Chapter 6.5 for reproducibility"
- Backward: "Renders .pg files structured per Chapter 2.3"
- Forward: "For manual testing workflow, see Chapter 7.1"

---

## Appendix 90.1: Minimal Templates

**Current**: 147 lines
**Target**: Enhance with more templates (add 50-100 lines)
**Priority**: Medium

### Content to add

1. **Add matching problem template** (add 40 lines):
   - Complete template with:
     - OPL header for a matching problem
     - PopUp widget creation
     - Two-column layout (flexbox)
     - MODES wrapper pattern
     - Shuffle array
   - Based on patterns from Chapter 6.3

2. **Add statement-based template** (add 35 lines):
   - Complete template with:
     - OPL header for statement evaluation
     - RadioButtons per statement
     - Statement array
     - Colored emphasis integration
   - Based on patterns from Chapter 6.4

3. **Add numeric with table template** (add 40 lines):
   - Complete template with:
     - OPL header for data analysis
     - DataTable with measurements
     - Multiple numeric blanks
     - Tolerance settings
   - Based on patterns from Chapter 6.2

4. **Enhance existing templates** (add 20 lines each):
   - Add inline comments explaining each section
   - Add "When to use this template" note at top
   - Add "Next steps after copying" checklist at bottom

### Cross-references to add
- Forward: "For matching, see detailed Chapter 6.3"
- Forward: "For tables, see Chapter 6.2"
- Forward: "For OPL headers, see Chapter 2.2 and 4.2"

---

## General Content Guidelines for All Pages

### Writing style
- **Active voice**: "Use this pattern..." not "This pattern can be used..."
- **Direct instructions**: "Copy this template" not "You might consider copying..."
- **Present tense**: "This creates..." not "This will create..."
- **Biology-first**: Always frame examples in realistic scientific context

### Code examples
- **Self-contained**: Each example should be runnable (with minor edits)
- **Commented**: Add `# comment` lines explaining non-obvious parts
- **Realistic values**: Use 0.5-10 mM, 15-30 Ct, 2-8 dilution factors, etc.
- **Proper units**: Always include units where applicable

### Failure modes
Every technique should show:
1. **What breaks**: The specific mistake
2. **Symptom**: What the user sees
3. **Fix**: Exact correction needed
4. **Prevention**: How to avoid

### Cross-references
- **Forward refs**: "See Chapter X" when topic comes later
- **Backward refs**: "Building on Chapter X" when extending earlier content
- **Appendix refs**: "Templates in Appendix 90.1" for copy-paste starting points
- **Never HTML links**: Just mention by chapter/section, LibreTexts will handle navigation

### Biology examples format
```
**Example N: [Specific topic]** (X lines)
- Scenario: [1-2 sentences setting context]
- Key pattern: [What technique is demonstrated]
- Code: [5-15 lines of PG/PGML]
- Note: [Why this example matters]
```

## Quality Checks Before Completing a Page

1. **Length check**: Target 150-300 lines for skeletal pages
2. **Example count**: 3-5 biology examples per advanced technique
3. **Failure modes**: At least 2-3 common failures with fixes
4. **Cross-references**: Forward and backward refs present
5. **HTML lint**: Run `/opt/homebrew/bin/bash tests/run_html_lint.sh`
6. **LibreTexts format**: Tables use mt-responsive-table class
7. **No internal links**: No `<a href=...>` to other textbook pages
8. **Code blocks**: Use `<pre>` tags, not triple backticks

## After Completing Expansion Work

1. **Update changelog**: Add entry to `docs/CHANGELOG.md`
2. **Verify line counts**: `wc -l Textbook/**/*.html | sort -n`
3. **Run HTML lint**: Confirm all 53 files pass
4. **Spot check**: Read 2-3 expanded pages for flow and completeness

## Getting Help

If you encounter issues during expansion:
- **Source doc missing**: Check migration guide for alternative sources
- **Biology example needed**: Look at biology-problems repo for inspiration
- **HTML format question**: See LIBRETEXTS_HTML_GUIDE.md
- **Unclear target**: Re-read three-sentence summary in TEXTBOOK_PAGE_SUMMARIES.md
