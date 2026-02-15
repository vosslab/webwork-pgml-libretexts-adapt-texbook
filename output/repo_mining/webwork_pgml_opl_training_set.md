# Mining Report: webwork-pgml-opl-training-set

## Repo Overview

The webwork-pgml-opl-training-set repository is a curated PGML-forward subset of the full Open Problem Library (OPL), containing 8,963 `.pg` files. It represents roughly 13% of the full OPL (72,734 files) but is 100% PGML -- every single file uses `BEGIN_PGML` rather than the legacy `BEGIN_TEXT` format. Only 3 files still contain any `BEGIN_TEXT` blocks (likely residual or hybrid). The corpus is heavily math-oriented (77.8% by DBsubject), with smaller engineering (15.5%), statistics (1.1%), and CS (0.5%) components. Chemistry and life sciences are structurally absent as DBsubject labels.

The repo also contains a sophisticated `pg_analyze` Python analysis toolkit, detailed corpus statistics documentation, linting infrastructure, and curated output summaries. The analysis was last snapshotted on 2026-01-17. The repo itself includes extensive documentation in `docs/` covering corpus curation methodology, lint architecture, and style guides.

## Directory Structure Analysis

```
webwork-pgml-opl-training-set/
  problems/                     (8,963 .pg files total)
    Contrib/                    (6,824 files - 76.1%)
      CCCS/                    (2,970 - PreCalc, AlgLit, QuantLit, ColAlg, Calc1/2, Trig)
      PCC/                     (918 - Portland Community College)
      CUNY/                    (662 - City University of New York)
      DouglasCollege/          (519 - Physics: Statics, Dynamics, Fluids, Particles)
      UBC/                     (480 - University of British Columbia)
      RRCC/                    (419)
      USask/                   (338 - U of Saskatchewan, mostly mechanics)
      DMOI/                    (122 - Discrete Math)
      BentleyUniversity/       (95)
      Fitchburg/               (62)
      LaTech/                  (43)
      Michigan/                (35)
      Hope/                    (29)
      + 15 smaller contributors
    OpenProblemLibrary/         (2,136 files - 23.8%)
      PCC/                     (1,159 - largest OPL contributor)
      Valdosta/                (258 - APEX Calculus)
      Rochester/               (229 - classic algebra/calculus)
      UBC/                     (79)
      CollegeOfIdaho/          (73)
      Hope/                    (50)
      FortLewis/               (43 - AUTHORING TEMPLATES - high value)
      + 20 smaller contributors
    Pending/                    (3 files)
  pg_analyze/                   (analysis toolkit)
  pgml_lint/                    (linting tools)
  tools/                        (utility scripts)
  docs/                         (extensive documentation)
  output/                       (analysis results)
```

## PGML Coverage

| Metric | Count | Percentage |
|---|---:|---:|
| Files using `BEGIN_PGML` | 8,963 | 100.0% |
| Files using `BEGIN_TEXT` (legacy) | 3 | 0.03% |
| Files with `BEGIN_PGML_SOLUTION` | 7,278 | 81.2% |
| Files with `BEGIN_PGML_HINT` | 577 | 6.4% |
| Files with `DOCUMENT()` | 8,963 | 100.0% |
| Files with `loadMacros` | 8,963 | 100.0% |
| Files with OPL metadata (DBsubject) | 8,606 | 96.0% |

## Macro Usage Census

### Core macros (nearly universal)

| Macro | Files | % of corpus |
|---|---:|---:|
| `PGstandard.pl` | 8,425 | 94.0% |
| `PGML.pl` | 8,419 | 93.9% |
| `MathObjects.pl` | 8,225 | 91.8% |
| `PGcourse.pl` | 7,787 | 86.9% |

### Question-type macros

| Macro | Files | % of corpus |
|---|---:|---:|
| `parserPopUp.pl` | 2,344 | 26.2% |
| `parserRadioButtons.pl` | 1,924 | 21.5% |
| `parserMultiAnswer.pl` | 1,655 | 18.5% |
| `PGchoicemacros.pl` | 1,059 | 11.8% |
| `weightedGrader.pl` | 504 | 5.6% |
| `parserAssignment.pl` | 452 | 5.0% |
| `niceTables.pl` | 334 | 3.7% |
| `scaffold.pl` | 287 | 3.2% |
| `parserOneOf.pl` | 261 | 2.9% |
| `parserNumberWithUnits.pl` | 177 | 2.0% |
| `parserFormulaUpToConstant.pl` | 175 | 2.0% |

### Context macros

| Macro | Files | % of corpus |
|---|---:|---:|
| `contextFraction.pl` | 1,824 | 20.3% |
| `contextLimitedPoint.pl` | 460 | 5.1% |
| `contextLimitedPolynomial.pl` | 323 | 3.6% |
| `contextLimitedFactor.pl` | 256 | 2.9% |
| `contextRationalFunction.pl` | 250 | 2.8% |
| `contextTrigDegrees.pl` | 247 | 2.8% |
| `contextPercent.pl` | 217 | 2.4% |
| `contextCurrency.pl` | 175 | 2.0% |
| `contextInequality.pl` | 248 | 2.8% |

### Graphics macros

| Macro | Files | % of corpus |
|---|---:|---:|
| `PGgraphmacros.pl` | 1,279 | 14.3% |
| `init_graph` usage | 569 | 6.3% |
| `PGtikz.pl` / `createTikZImage` | 52 | 0.6% |

## Subject Area Distribution

| Subject | Files | % |
|---|---:|---:|
| Algebra | 3,373 | 37.6% |
| Calculus - single variable | 1,140 | 12.7% |
| Arithmetic | 621 | 6.9% |
| Trigonometry | 608 | 6.8% |
| Statics (engineering) | 573 | 6.4% |
| Elementary Algebra | 387 | 4.3% |
| Dynamics (engineering) | 374 | 4.2% |
| Geometry | 151 | 1.7% |
| Fluid mechanics | 144 | 1.6% |
| Combinatorics | 76 | 0.8% |
| Statistics | 69 | 0.8% |
| Engineering (other) | 113 | 1.3% |
| Linear algebra | 54 | 0.6% |
| Programming Languages | 43 | 0.5% |

## Question Type Patterns

| Pattern | Files | Description |
|---|---:|---|
| PopUp / DropDown | 2,401 | Dropdown select menus |
| RadioButtons | 1,961 | Single-choice MC |
| MultiAnswer | 1,690 | Multi-part coordinated answers |
| AnswerHints | 430 | Custom wrong-answer feedback |
| niceTables (DataTable/LayoutTable) | 369 | Formatted tables |
| Scaffold (multi-part) | 195 | Sequential reveal problems |
| parserOneOf | 261 | Accept multiple valid answers |
| parserImplicitEquation | 85 | Equation-form answers |
| CheckboxList | 16 | Multiple-select (select all that apply) |
| WordCompletion | 13 | Fill-in-the-word |
| contextOrdering | 6 | Ordered list answers |
| Chemistry (contextReaction) | 3 | Chemical equation balancing |

## Chapter Mapping

### Chapter 1: Introduction (WeBWorK basics, quickstart)

- **Relevant files**: `problems/OpenProblemLibrary/FortLewis/Authoring/Templates/` (entire directory, 30 files)
- **What to extract**: The FortLewis authoring templates are official PGML tutorial problems covering every question type. They serve as canonical "hello world" examples.
- **Example snippet** (minimal PGML problem):
```perl
DOCUMENT();
loadMacros("PGstandard.pl", "MathObjects.pl", "PGML.pl", "PGcourse.pl");
Context("Numeric");
$answer = Compute("1+1");

BEGIN_PGML
What is [` 1 + 1 `]? [_________]{$answer}
END_PGML

BEGIN_PGML_SOLUTION
The answer is [` [$answer] `].
END_PGML_SOLUTION
ENDDOCUMENT();
```
- **Textbook gap it fills**: Provide a quick-start example that shows the absolute minimum viable PGML problem structure.

### Chapter 2: Problem Generation PG (PG language, OPL headers, macros)

- **Relevant files**:
  - `problems/Contrib/PCC/BasicAlgebra/SystemsOfLinearEquations/NumberOfSolutionsOfSystem20.pg` (comprehensive OPL headers + complex setup)
  - `problems/Contrib/DouglasCollege/Physics/Statics/OER-Mechanics-S-4-7_SimplificationOfAForceAndCoupleSystem/21-S-4-7-MK-04.pg` (heavy macro loading)
  - `problems/Contrib/CUNY/CityTech/Precalculus/setInverse_Functions/compute-inverse-linear.pg` (clean header + hint + solution)
- **What to extract**: OPL metadata headers (`DBsubject`, `DBchapter`, `DBsection`, `KEYWORDS`), macro loading patterns, `DOCUMENT()`/`ENDDOCUMENT()` boilerplate, `Context()` usage patterns.
- **Example snippet** (OPL header):
```perl
## DBsubject('Algebra')
## DBchapter('Systems of Equations and Inequalities')
## DBsection('Systems of Linear Equations')
## KEYWORDS('system','equation','solution')
## DBCCSS('8.EE.8','A.REI.6')
## Author('Alex Jordan, Carl Yao, Chris Hughes')
## Institution('PCC')
```
- **Textbook gap it fills**: The textbook needs a comprehensive list of all common macros with one-line descriptions of what each does, organized by category (core, question-type, context, graphics).

### Chapter 3: PGML (answer blanks, lists, tables, layout)

- **Relevant files**:
  - `problems/Contrib/Fitchburg/Algebra/lines/function-evaluation-1.pg` (DataTable with PGML answer blanks inside cells)
  - `problems/OpenProblemLibrary/FortLewis/Authoring/Templates/Sequences/AnswerOrderedList1_PGML.pg` (ordered list answers)
  - `problems/OpenProblemLibrary/Valdosta/APEX_Calculus/1.1/APEX_1.1_22.pg` (DataTable/LayoutTable)
- **What to extract**: PGML syntax for answer blanks (`[_]{$ans}`), inline math (`` [`...`] ``), display math (`` [``...``] ``), centering (`>> ... <<`), bold/italic, DataTable with embedded PGML.
- **Example snippet** (DataTable with PGML answer blanks):
```perl
@rows = (
    [ '`x`',                 '`y`' ],
    [ PGML('[``[$x[0]]``]'), PGML('[_]{$y[0]}') ],
    [ PGML('[``[$x[1]]``]'), PGML('[_]{$y[1]}') ],
);
$tab = DataTable([@rows], padding => [0.25, 0.25]);

BEGIN_PGML
[$tab]*
END_PGML
```
- **Textbook gap it fills**: Need concrete examples of DataTable with embedded PGML for interactive tables; the `PGML()` wrapper function for embedding PGML snippets inside Perl data structures.

### Chapter 4: Breaking Down Components (file anatomy)

- **Relevant files**:
  - `problems/Contrib/PCC/BasicAlgebra/SystemsOfLinearEquations/NumberOfSolutionsOfSystem20.pg` (full anatomy: description, header, setup, statement, solution)
  - `problems/OpenProblemLibrary/FortLewis/Authoring/Templates/Misc/Scaffolding2_PGML.pg` (clean section structure)
- **What to extract**: The standard file sections (Description block, OPL metadata, DOCUMENT/loadMacros, Context/setup, BEGIN_PGML statement, BEGIN_PGML_SOLUTION, ENDDOCUMENT). Variable naming conventions. Comment style patterns.
- **Example snippet** (section dividers):
```perl
###########################
#  Initialization
DOCUMENT();
loadMacros(...);

###########################
#  Setup
Context("Numeric");
$a = random(1,10,1);

###########################
#  Main text
BEGIN_PGML
...
END_PGML

###########################
#  Solution
BEGIN_PGML_SOLUTION
...
END_PGML_SOLUTION

ENDDOCUMENT();
```
- **Textbook gap it fills**: Show the canonical section ordering used by the major OPL contributors; explain each section's purpose.

### Chapter 5: Different Question Types

- **Relevant files**:
  - MC (RadioButtons): `problems/Contrib/CUNY/BMCC/MAT303/JiangChen/13.2/13.2_32.pg`
  - Multiple answer (CheckboxList): `problems/OpenProblemLibrary/Valdosta/APEX_Calculus/3.1/APEX_3.1_6.pg`
  - Dropdown (PopUp): `problems/Contrib/PCC/BasicAlgebra/SystemsOfLinearEquations/NumberOfSolutionsOfSystem20.pg`
  - Multi-part (Scaffold): `problems/Contrib/Hope/Calc2/APEX_06_01_Substitution/Reading_Q_01.pg`
  - Ordered list: `problems/OpenProblemLibrary/FortLewis/Authoring/Templates/Sequences/AnswerOrderedList1_PGML.pg`
  - Fill-in-blank (numeric): essentially all 8,963 files
  - WordCompletion: `problems/Contrib/Hope/Calc2/APEX_06_01_Substitution/Reading_Q_01.pg`
- **What to extract**: Constructor patterns for each question type; how to embed each in PGML; grading options.
- **Example snippet** (CheckboxList):
```perl
$mc = CheckboxList(
    [
        ["Absolute maximum", "Relative maximum",
         "Absolute minimum", "Relative minimum"],
        "None of the above"
    ],
    ["Absolute maximum", "Relative maximum"]  # correct answers
);
BEGIN_PGML
[_]{$mc}
END_PGML
```
- **Example snippet** (PopUp):
```perl
$popup = PopUp(
  ['?','no solution','one solution','infinitely many solutions'],
  'one solution',
  order=>['no solution','one solution','infinitely many solutions']
);
BEGIN_PGML
The system has [__]{$popup}.
END_PGML
```
- **Textbook gap it fills**: Need complete constructor syntax for CheckboxList (only 16 examples in corpus -- underrepresented), WordCompletion (13 examples), and contextOrdering (6 examples). These rare types need more textbook coverage.

### Chapter 6: Advanced PGML (tables, graphs, randomization, chemistry)

- **Relevant files**:
  - niceTables: `problems/Contrib/Fitchburg/Algebra/lines/function-evaluation-1.pg`
  - TikZ graphs: `problems/OpenProblemLibrary/Rochester/setAlgebra10QuadraticEqns/sw3_3_69.pg`
  - PGgraphmacros: `problems/OpenProblemLibrary/Valdosta/APEX_Calculus/3.1/APEX_3.1_6.pg`
  - Chemical reactions: `problems/OpenProblemLibrary/FortLewis/Authoring/Templates/Misc/ChemicalReaction1_PGML.pg`
  - Randomization: `problems/Contrib/PCC/BasicAlgebra/SystemsOfLinearEquations/NumberOfSolutionsOfSystem20.pg` (complex conditional randomization)
  - Weighted grading: `problems/OpenProblemLibrary/FortLewis/Calc3/14-3-Local-linearity/HGM4-14-3-14-Local-linearity-differential.pg`
- **What to extract**: TikZ image creation (`createTikZImage`, `BEGIN_TIKZ`), PGgraphmacros (`init_graph`, `FEQ`, `plot_functions`), `contextReaction` for chemistry, `install_weighted_grader()`, `list_random()` for randomized text.
- **Example snippet** (TikZ):
```perl
$image = createTikZImage();
$image->BEGIN_TIKZ
\draw (0,0) -- (4,0) -- (4,3) -- cycle;
\draw (2,0) node[anchor=north] {base};
END_TIKZ

BEGIN_PGML
>>[@ image($image, width => 300) @]*<<
END_PGML
```
- **Example snippet** (Chemical Reaction):
```perl
Context("Reaction");
$reactants = Formula("2 Na OH + Mg Cl_2");
$products = Formula("2 Na Cl + Mg (OH)_2");

BEGIN_PGML
[` [$reactants] \longrightarrow `] [____]{$products}
END_PGML
```
- **Textbook gap it fills**: Chemistry context is barely represented (3 files). TikZ examples are sparse (52 files). The textbook should expand both. Also need coverage of `weightedGrader` (504 files) and `answerHints` (430 files) for partial-credit and feedback patterns.

### Chapter 7: Testing and Debugging

- **Relevant files**: The repo itself contains `pgml_lint/` and `tests/` directories with linting infrastructure
- **What to extract**: The repo's `pg_analyze` tool provides a model for QA analysis of `.pg` files. The `PGML_LINT_ARCHITECTURE.md` and related docs describe a linting pipeline.
- **Textbook gap it fills**: QA checklist items: verify all files have `DOCUMENT()`/`ENDDOCUMENT()`, verify all answer blanks have evaluators, check for common mistakes like missing `$showPartialCorrectAnswers`.

### Chapter 8: Using AI Agents (placeholders)

- **Relevant files**: `AGENTS.md` in the repo root
- **What to extract**: The repo has an `AGENTS.md` file that may contain instructions for AI-assisted development
- **Textbook gap it fills**: All content needed -- this repo demonstrates how a corpus can be curated and analyzed programmatically, which could inform AI-assisted problem authoring workflows.

### Chapter 90: Appendices (templates, glossary)

- **Relevant files**: `problems/OpenProblemLibrary/FortLewis/Authoring/Templates/` (30 template files spanning all question types)
- **What to extract**: The FortLewis templates are essentially a ready-made appendix of problem templates organized by math topic and question type.
- **Textbook gap it fills**: These templates are a goldmine for an appendix of starter templates.

## Top 10 Most Useful Files

1. **`problems/OpenProblemLibrary/FortLewis/Authoring/Templates/Misc/ChemicalReaction1_PGML.pg`** -- Only chemistry example; shows contextReaction with randomized chemical formulas
2. **`problems/OpenProblemLibrary/FortLewis/Authoring/Templates/Misc/Scaffolding2_PGML.pg`** -- Canonical scaffold/multi-part template; clean and minimal
3. **`problems/Contrib/Fitchburg/Algebra/lines/function-evaluation-1.pg`** -- DataTable with embedded PGML answer blanks; rare interactive table pattern
4. **`problems/OpenProblemLibrary/Valdosta/APEX_Calculus/3.1/APEX_3.1_6.pg`** -- CheckboxList with PGgraphmacros; complex multi-point classification problem
5. **`problems/Contrib/PCC/BasicAlgebra/SystemsOfLinearEquations/NumberOfSolutionsOfSystem20.pg`** -- Complete anatomy: OPL headers, PopUp, conditional randomization, detailed solution
6. **`problems/OpenProblemLibrary/Rochester/setAlgebra10QuadraticEqns/sw3_3_69.pg`** -- TikZ images with variable substitution; geometry application problem
7. **`problems/Contrib/Hope/Calc2/APEX_06_01_Substitution/Reading_Q_01.pg`** -- Scaffold with WordCompletion, FunctionPrime, FormulaUpToConstant; multiple rare features
8. **`problems/Contrib/CUNY/CityTech/Precalculus/setInverse_Functions/compute-inverse-linear.pg`** -- Clean hint + solution + pedagogical narrative pattern
9. **`problems/OpenProblemLibrary/FortLewis/Calc3/14-3-Local-linearity/HGM4-14-3-14-Local-linearity-differential.pg`** -- weightedGrader with CheckboxList; partial credit pattern
10. **`problems/OpenProblemLibrary/FortLewis/Authoring/Templates/Sequences/AnswerOrderedList1_PGML.pg`** -- Ordered comma-separated list answer with `cmp(ordered=>1)`

## Recommended Actions

1. **Add a macro reference table to Ch2**: The corpus loads 30+ distinct macros. Create a categorized reference (core, question-type, context, graphics) with one-line descriptions and example usage, based on the macro census above.

2. **Expand CheckboxList coverage in Ch5**: Only 16 files in the entire corpus use CheckboxList. Extract the Valdosta APEX_3.1_6.pg and FortLewis templates as canonical examples. This is the most underrepresented question type.

3. **Add WordCompletion and contextOrdering to Ch5**: Only 13 WordCompletion and 6 contextOrdering files exist. These need dedicated sections with examples.

4. **Create a DataTable-with-PGML section in Ch3 or Ch6**: The Fitchburg function-evaluation-1.pg pattern of embedding `PGML('[_]{$ans}')` inside DataTable cells is powerful but barely documented.

5. **Add a Chemistry section to Ch6**: The ChemicalReaction1_PGML.pg template shows `contextReaction` with randomized elements. Expand this with more chemistry examples (only 3 in corpus).

6. **Document the weightedGrader pattern in Ch6**: 504 files use `weightedGrader.pl`. Show `install_weighted_grader()` and `cmp_options => {weight => N}` syntax for partial credit allocation.

7. **Add answerHints coverage to Ch6 or Ch7**: 430 files use `answerHints.pl` for custom wrong-answer feedback. This is a quality-of-life feature that improves student experience.

8. **Create a TikZ cookbook in Ch6**: Only 52 files use TikZ. Extract the Rochester quadratic box-folding example and build 3-4 additional TikZ patterns (coordinate plane, triangle, function graph).

9. **Expand the PGML_HINT section**: Only 577 files (6.4%) include hints. The CUNY inverse function example shows the hint pattern well. Add this to Ch3 or Ch4 with emphasis on when and how to write effective hints.

10. **Use FortLewis templates as appendix**: The 30 FortLewis authoring template files are organized by math topic and cover every major question type. Include them (or adapted versions) as a "Starter Templates" appendix (Ch90).

11. **Document Scaffold patterns thoroughly in Ch5**: 195 files use scaffolding. Show both `Scaffold::Begin()` and `Scaffold::Begin('is_open' => 'correct_or_first_incorrect')` variants. The Hope substitution Reading_Q_01.pg is an ideal example of progressive scaffolding.

12. **Add science-oriented problems**: The corpus is 77.8% math, 0.6% physics, 0% biology/chemistry by DBsubject. The textbook should include non-math STEM examples to broaden the audience. The biology-problems repo may fill this gap.
