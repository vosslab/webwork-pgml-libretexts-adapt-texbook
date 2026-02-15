# PG Macro Version Comparison

This document compares macro availability across different PG versions to help authors understand which macros work in ADAPT/renderer versus full PG installations.

## Version Context

- **ADAPT/Renderer Subset (PG 2.17 base)**: Flattened macro tree used in ADAPT and webwork-pg-renderer
- **Full PG 2.17+**: Standard PG 2.17 and later point releases with complete macro structure
- **PG 2.20**: Current stable release (as of 2026-01-28) with latest macros

## Macro Availability by Category

### Parser Widgets (Interaction Macros)

| Macro File | ADAPT/Renderer | PG 2.17+ | PG 2.20 | Notes |
|------------|----------------|----------|---------|-------|
| `parserPopUp.pl` | Available | | | Use for matching, dropdowns |
| `parserRadioButtons.pl` | Available | | | Use for multiple choice |
| `parserCheckboxList.pl` | Missing | | | **Use RadioButtons per statement instead** |
| `parserMultiAnswer.pl` | Available | | | Multi-part grading |
| `parserWordCompletion.pl` | Available | | | Autocomplete text entry |

### Core Macros (Always Available)

| Macro File | ADAPT/Renderer | PG 2.17+ | PG 2.20 | Notes |
|------------|----------------|----------|---------|-------|
| `PGstandard.pl` | Available | | | Required |
| `MathObjects.pl` | Available | | | Strongly recommended |
| `PGML.pl` | Available | | | Required for PGML authoring |
| `PGcourse.pl` | Available | | | Commonly expected |

### Table and Layout Macros

| Macro File | ADAPT/Renderer | PG 2.17+ | PG 2.20 | Notes |
|------------|----------------|----------|---------|-------|
| `niceTables.pl` | Available | | | **Only supported way to create tables** |
| `unionTables.pl` | Available | | | Legacy table approach |

### Context Macros (Science/Units)

| Macro File | ADAPT/Renderer | PG 2.17+ | PG 2.20 | Notes |
|------------|----------------|----------|---------|-------|
| `contextReaction.pl` | Available | | | Chemical equations |
| `contextCurrency.pl` | Available | | | Money values |
| `contextScientificNotation.pl` | Available | | | Scientific notation |
| `parserNumberWithUnits.pl` | Available | | | Numeric with units |
| `parserFormulaWithUnits.pl` | Available | | | Formula with units |

### Vector and Matrix Macros

| Macro File | ADAPT/Renderer | PG 2.17+ | PG 2.20 | Notes |
|------------|----------------|----------|---------|-------|
| `parserVectorUtils.pl` | Available | | | Vector operations |
| `MatrixCheckers.pl` | Available | | | Matrix answer checking |
| `VectorListCheckers.pl` | Missing | | | List of vectors checking |

### Legacy Choice Macros

| Macro File | ADAPT/Renderer | PG 2.17+ | PG 2.20 | Notes |
|------------|----------------|----------|---------|-------|
| `PGchoicemacros.pl` | Available | | | **Legacy - use parser macros instead** |

## Commonly Missing Macros in ADAPT/Renderer

These macros appear in online examples and full PG but are NOT available in the ADAPT/renderer subset:

1. **`parserCheckboxList.pl`** - Checkbox widgets
   - **Workaround**: Use multiple `RadioButtons` (one per statement) or `PopUp` widgets
   - See Chapter 6.5 for multiple choice statements pattern

2. **`VectorListCheckers.pl`** - List of vectors validation
   - **Workaround**: Use standard MathObjects list contexts when available

3. Subdirectory macros from `macros/math/` and `macros/parsers/`
   - The renderer snapshot has a flattened macro tree; subdirectories do not exist
   - All available macros are listed in `OTHER_REPOS-do_not_commit/biology-problems/docs/webwork/PG_2_17_RENDERER_MACROS.md`

## How to Check Macro Availability

### For ADAPT/Renderer Subset
1. Check the allowlist: `OTHER_REPOS-do_not_commit/biology-problems/docs/webwork/PG_2_17_RENDERER_MACROS.md`
2. Test locally with webwork-pg-renderer (Chapter 7)
3. If a macro from an online example is missing, find an alternative from the allowlist

### For Full PG 2.17+ or PG 2.20
- Consult the official WeBWorK PG documentation: https://openwebwork.github.io/pg-docs/
- Check the PG repository: https://github.com/openwebwork/pg

## Version Upgrade Notes

If you are authoring for:

- **ADAPT only**: Stick to the ADAPT/Renderer subset allowlist
- **Local WeBWorK 2.17+**: You can use full PG 2.17 macros, but note portability if sharing to ADAPT
- **Local WeBWorK 2.20**: You have access to latest macros, but problems may not render in ADAPT

## Recommendations for Portability

1. **Prefer ADAPT/Renderer subset macros** when possible - ensures problems work in both ADAPT and local WeBWorK
2. **Document dependencies** in the OPL header DESCRIPTION if using macros outside the subset
3. **Test in ADAPT or local renderer** before publishing to a shared library
4. **Avoid deprecated macros** like `PGchoicemacros.pl` even if available - use parser macros instead

## Reference

- ADAPT/Renderer macro allowlist: `OTHER_REPOS-do_not_commit/biology-problems/docs/webwork/PG_2_17_RENDERER_MACROS.md`
- PG documentation: https://openwebwork.github.io/pg-docs/
- PG repository: https://github.com/openwebwork/pg
