# Mining Report: webwork-open-problem-library

## Repo Overview

The WeBWorK Open Problem Library (OPL) is the largest publicly available collection of WeBWorK problems, containing 72,734 `.pg` files organized under three top-level directories: OpenProblemLibrary (37,692 files from curated institutional contributions), Contrib (28,074 community-contributed files), and Pending (6,968 files awaiting review). The repo has already been analyzed via a symlinked `pg_analyze` tool (from webwork-open-problem-PGML), producing extensive TSV summaries in the `output/` directory covering corpus profiling, discipline classification, question type distribution, macro usage, widget/evaluator cross-tabulation, duplicate detection, and content-hint audits.

Each problem file is tagged with structured metadata: `DBsubject`, `DBchapter`, and `DBsection` headers that classify problems into a hierarchical taxonomy. Coverage is high: 69,550 of 72,734 files (95.6%) have a non-blank DBsubject. The corpus is overwhelmingly math-focused (43,358 problems classified under math), with significant engineering (5,911), physics (4,384), and statistics (2,967) content. There is essentially zero biology or chemistry content by DBsubject classification, though 1,102 files mention chemistry terms (mostly "equilibrium" and "kinetics" in physics/engineering contexts) and only 29 files mention biology terms.

## Directory Structure

```
webwork-open-problem-library/
  analyze.sh -> ../webwork-open-problem-PGML/analyze.sh  (symlink)
  pg_analyze -> ../webwork-open-problem-PGML/pg_analyze   (symlink)
  OTHER_REPOS-do_not_commit/                              (symlinks to sibling repos)
  output/                                                 (pre-computed analysis)
    INDEX.txt
    summary/           (12 TSV files: corpus_profile, discipline_counts, etc.)
    lists/             (per-discipline and per-type file lists)
      discipline/      (10 discipline file lists)
      type/            (10 question type file lists)
      evaluator/
      subtype/
      widget/
    content_hints/     (bio_terms_count.tsv, chem_terms_count.tsv)
    diagnostics/
    needs_review/
    samples/
    other/
  problems/
    OpenProblemLibrary/   37,692 files across 60 institutional directories
    Contrib/              28,074 files across 40+ contributor directories
    Pending/              6,968 files across 23 contributor directories
```

### Files by Discipline (DBsubject classification)

| Discipline    | Count  | Percentage |
|---------------|--------|------------|
| Math          | 43,358 | 62.2%      |
| Meta/noise    | 11,168 | 16.0%      |
| Engineering   | 5,911  | 8.5%       |
| Physics       | 4,384  | 6.3%       |
| Statistics    | 2,967  | 4.3%       |
| Meta/missing  | 911    | 1.3%       |
| Finance       | 854    | 1.2%       |
| Other         | 500    | 0.7%       |
| Grade level   | 356    | 0.5%       |
| CS            | 54     | 0.1%       |
| Life sciences | 0      | 0.0%       |
| Chemistry     | 0      | 0.0%       |

### Files by Question Type

| Type                 | Count  |
|----------------------|--------|
| Numeric entry        | 44,575 |
| Multiple choice      | 37,516 |
| Multipart            | 30,828 |
| Other                | 10,251 |
| Graph-like           | 8,908  |
| Fill-in-blank (word) | 3,619  |
| Assignment/ordering  | 1,616  |
| Essay                | 564    |
| Matching             | 189    |

### Top Math Subjects

| Subject                     | Count  |
|-----------------------------|--------|
| Algebra                     | 17,043 |
| Calculus (single variable)  | 11,155 |
| Linear algebra              | 2,697  |
| Calculus (general)          | 2,044  |
| Trigonometry                | 1,985  |
| Calculus (multivariable)    | 1,941  |
| Differential equations      | 1,601  |
| Arithmetic                  | 1,248  |
| Geometry                    | 829    |

### Key Macro Usage (top 10)

| Macro                     | Files  |
|---------------------------|--------|
| PGstandard.pl             | 59,503 |
| PGcourse.pl               | 52,620 |
| MathObjects.pl            | 48,691 |
| PGchoicemacros.pl         | 31,314 |
| PGML.pl                   | 18,075 |
| PGgraphmacros.pl          | 8,908  |
| AnswerFormatHelp.pl       | 8,049  |
| parserPopUp.pl            | 7,964  |
| parserMultiAnswer.pl      | 6,962  |
| parserRadioButtons.pl     | 6,578  |

### PGML Adoption

Only 18,075 of 72,734 files (24.9%) load PGML.pl. The corpus is predominantly legacy PG format. Evaluator sources: 120,248 answer evaluators use `ANS()` calls vs. 29,076 use PGML payloads vs. 208 use PGML star-spec syntax. PGML adoption varies by question type but remains the minority format.

### Duplicates

The corpus contains 7,148 exact-duplicate groups spanning 15,386 files (21.2% of total). After whitespace normalization, 7,190 groups spanning 15,550 files. The largest duplicate group has 16 copies of the same problem.

## Biology/Life Science Content

**There is effectively zero biology content in the OPL.** The discipline classifier found 0 files with a biology-related DBsubject. A content-hint search for biology terms found only 29 files, and on manual inspection these are false positives:

- **Incidental word "biology"**: Problems that mention biology as a course name in randomized lists (e.g., "list_random('Mathematics', 'Chemistry', 'Biology', 'English')") in statistics word problems -- not actual biology content
- **DBsection(Biology)**: 6 files from UCSB Stewart Calculus that use "Biology" as a section label for calculus application problems (integrals, growth/decay) -- these are calculus problems with biological context, not biology questions
- **WHFreeman Rogawski Calculus**: 4 files tagged DBsection(Biology) covering exponential growth/decay and net change -- again calculus with biological applications

The OPL has zero problems testing biological knowledge (genetics, ecology, cell biology, physiology, anatomy, evolution, etc.).

## Chapter Mapping

### Chapter 1: Introduction (mentions OPL)

- **Relevant content**: The OPL itself is the primary reference. The repo demonstrates the DBsubject/DBchapter/DBsection taxonomy (123 raw distinct subjects, 559 chapters, 1,952 sections). The metadata coverage (95.6% classified) and organizational structure (institution-based directory layout) are important for explaining how the OPL works.
- **Textbook gap it fills**: Provides concrete numbers for "how big is the OPL" and "what disciplines does it cover." Chapter 1 can reference the 72,734 problems, 60+ contributing institutions, and the taxonomy system.

### Chapter 2: Problem Generation PG (OPL headers, macros)

- **Relevant content**: Extremely relevant. The corpus provides real-world statistics on macro usage patterns:
  - PGstandard.pl is used in 82% of files
  - MathObjects.pl in 67%
  - PGML.pl in only 25% (vs. PGchoicemacros.pl at 43%)
  - 260+ distinct macros in use
  - The DBsubject/DBchapter/DBsection header system is demonstrated across 69,550+ files
  - Randomization is present in 48,159 files (66.2%)
- **Textbook gap it fills**: Provides the empirical basis for "what macros should a problem author know" -- the top 10 macros cover the vast majority of use cases. Documents which question type patterns are most common. Can inform recommended header taxonomy values.

### Chapter 5: Different Question Types

- **Relevant content**: Highly relevant. The OPL analysis quantifies question type distribution:
  - Numeric entry dominates (44,575 files)
  - Multiple choice is second (37,516)
  - Multipart questions are third (30,828)
  - Widget types: blank (88,568), pgml_blank (32,170), radio (8,337), popup (7,732), checkbox (1,741), matching (189)
  - Evaluator types: num_cmp (32,154), cmp (41,003), str_cmp (4,640), radio_cmp (4,372), fun_cmp (5,045)
  - Cross-tabulation of widget vs. evaluator types available
- **Textbook gap it fills**: Provides frequency-based guidance on which question types are most used in practice. Can inform a "by frequency" ordering of question type chapters. Documents the widget-evaluator pairing patterns that problem authors should understand.

### Chapter 90: Appendices

- **Relevant content**: The full macro list (260+ macros with usage counts), the discipline taxonomy (109 normalized subjects), and the question type classification scheme could be appendix reference material.
- **Textbook gap it fills**: Serves as a definitive reference for macro names/popularity, taxonomy values, and evaluator/widget type catalogs.

## Recommended Actions

1. **Use OPL statistics in Chapter 1** to quantify the problem library (72,734 problems, 60+ institutions, 109 subject categories) and explain the DBsubject/DBchapter/DBsection classification system.

2. **Use macro frequency data in Chapter 2** to prioritize which macros to teach: PGstandard.pl, MathObjects.pl, PGML.pl, PGchoicemacros.pl, and PGgraphmacros.pl cover the vast majority of real problems.

3. **Use question type statistics in Chapter 5** to order question type coverage by real-world frequency: numeric entry first, then multiple choice, then multipart, then specialized types.

4. **Use widget/evaluator cross-tabulation data** for Chapter 5 to show which answer evaluators pair with which input widgets, helping authors choose the right combination.

5. **Note the PGML adoption gap** (25% of OPL vs. recommended for new content): the textbook should clearly recommend PGML for new problems while acknowledging that most existing OPL examples use legacy PG format.

6. **Do NOT rely on the OPL for biology content.** The library has zero biology problems. All biology-related content must come from other sources (biology-problems repo, custom development).

7. **Consider creating an appendix** with the top 50 macros by frequency, the full discipline taxonomy, and the question type classification scheme as quick-reference material.

8. **Use the duplicate analysis** (21% duplicates) to inform guidance about checking for existing problems before creating new ones.
