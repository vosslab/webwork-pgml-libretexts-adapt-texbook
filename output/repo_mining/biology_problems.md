# Mining Report: biology-problems

## Repo Overview

The `biology-problems` repository at `/Users/vosslab/nsh/PROBLEMS/biology-problems/` contains 37 WeBWorK problem files (9 `.pg` + 28 `.pgml`) authored by Dr. Neil R. Voss at Roosevelt University. The problems span biochemistry (amino acids, buffers, pKa, electrophoresis, macromolecules), genetics (X-linked inheritance), and general biology. All files are licensed CC BY 4.0 with LGPLv3 for source code portions.

The repo is a rich source of real-world examples for the textbook. It demonstrates every major question type (RadioButtons MC, DropDown/PopUp matching, DraggableProof ordering, GraphTool interactive, custom HTML radio cards), advanced rendering techniques (RDKit.js chemistry, simulated gel electrophoresis via CSS, PGgraphmacros titration curves, niceTables LayoutTable grids), and sophisticated randomization strategies (PGrandom seed-stable selection, large data pools with 50+ items, programmatic distractor generation). The `webwork_examples/` subdirectory contains diagnostic utilities useful for debugging PG environments.

---

## Chapter Mapping

### Chapter 1: Introduction and Getting Started

- **Relevant files**: `webwork_examples/check_pg_version.pg`, `webwork_examples/get_webwork_env_variables.pg`, `webwork_examples/get_macro_paths.pg`
- **What to extract**: Environment introspection patterns; how to detect PG version at runtime; how to dump envir variables for debugging setup issues.
- **Example snippet** (from `check_pg_version.pg`, lines 29-48):
```perl
# Detect PG version by probing for specific functions
my $pg_version = 'PG 2.16 or older';
if (defined(&GraphTool::new)) {
    $pg_version = 'PG 2.17';
}
if (defined(&parser::DropDown::new)) {
    $pg_version = 'PG 2.18 or newer';
}
```
- **Textbook gap it fills**: Ch1 currently lacks practical guidance on checking which PG version is running or inspecting the environment. These diagnostics help new authors verify their installation.

### Chapter 2: OPL Metadata and Problem Structure

- **Relevant files**: Nearly all files use the standard OPL header block; best examples are `isoelectric_one_protein.pgml`, `protein_gel_migration.pgml`, `poisson_flies.pgml`
- **What to extract**: Complete OPL header examples with DBsubject/DBchapter/DBsection for biology topics; consistent 4-section anatomy (Preamble, Setup, Statement, Solution) with numbered comment headers.
- **Example snippet** (from `isoelectric_one_protein.pgml`, lines 1-20):
```perl
## TITLE('Biochemistry: Net protein charge from pI and solution pH')
## DESCRIPTION
## Determine the net charge of a protein in buffer ...
## ENDDESCRIPTION
## KEYWORDS('isoelectric point','protein charge','pH','biochemistry')
## DBsubject('Biochemistry')
## DBchapter('Chemical Properties')
## DBsection('Isoelectric Point')
## Level(2)
## Date('2026-02-12')
## Author('Dr. Neil R. Voss')
## Institution('Roosevelt University')
## Language(en)

DOCUMENT();
loadMacros(
    'PGstandard.pl',
    'PGML.pl',
    'parserRadioButtons.pl',
    'PGcourse.pl',
);
```
- **Textbook gap it fills**: Provides biology-specific OPL taxonomy examples (Biochemistry > Chemical Properties > Isoelectric Point) complementing the existing math-oriented examples.

### Chapter 3: PGML Formatting and Display

- **Relevant files**: `which_hydrophobic-simple.pgml`, `ph_h_concentration_ratio.pgml`, `alpha_helix_h-bonds.pgml`
- **What to extract**: PGML text formatting patterns, inline variables with `[$var]`, inline HTML chemical formulas (subscripts/superscripts), BEGIN_PGML_HINT and BEGIN_PGML_SOLUTION blocks.
- **Example snippet** (from `isoelectric_one_protein.pgml`, lines 190-215):
```perl
BEGIN_PGML
[$protein_panel]*

The protein in the panel is placed in a buffer solution
with a pH of [$ph_display].

What is the correct net charge on the [$abbr] protein
at pH [$ph_display]?

[_]{$rb}
END_PGML

BEGIN_PGML_HINT
For proteins in this model:
- if pH < pI, net charge is positive
- if pH > pI, net charge is negative
END_PGML_HINT

BEGIN_PGML_SOLUTION
Here, pI = [$pi_display] and pH = [$ph_display],
so the correct choice is [$charge_phrase].
END_PGML_SOLUTION
```
- **Textbook gap it fills**: Real-world HINT and SOLUTION blocks; embedding raw HTML inside PGML with `[...]*` escape.

### Chapter 4: Randomization and Data Pools

- **Relevant files**: `macromolecules-matching.pgml`, `macromolecule_identification.pgml`, `functional_groups_bond_types.pgml`, `pKa_buffer_state-diprotic.pgml`, `protein_gel_migration.pgml`
- **What to extract**: Large data pool design (50-350+ items), PGrandom for seed-stable randomization, helper functions (random_choice, shuffle_list, sample_unique, sort_proteins_by_mw), programmatic distractor generation, retry-loop pattern for valid problem construction.
- **Example snippet** (from `protein_gel_migration.pgml`, lines 95-123):
```perl
sub random_choice {
    my (@items) = @_;
    my $count = scalar(@items);
    die 'Random choice requires at least one item.' if $count < 1;
    my $idx = random(0, $count - 1, 1);
    return $items[$idx];
}

sub shuffle_list {
    my (@items) = @_;
    for (my $i = $#items; $i > 0; $i--) {
        my $j = random(0, $i, 1);
        @items[$i, $j] = @items[$j, $i];
    }
    return @items;
}

sub sample_unique {
    my ($count, @items) = @_;
    die 'Sample size exceeds pool size.' if $count > scalar(@items);
    my @pool = @items;
    my @sampled = ();
    for my $k (1 .. $count) {
        my $idx = random(0, $#pool, 1);
        push @sampled, $pool[$idx];
        splice(@pool, $idx, 1);
    }
    return @sampled;
}
```
- **Example snippet** (retry-loop from `protein_gel_migration.pgml`, lines 290-335):
```perl
my $max_attempts = 60;
my $question_built = 0;

for my $attempt (1 .. $max_attempts) {
    my @gel_set = get_protein_set_for_gel($NUM_CHOICES + 1);
    next if scalar(@gel_set) < ($NUM_CHOICES + 1);

    my ($unknown_mw, $unknown_dist, $mw_range, $gap) =
        get_unknown(undef, @gel_set);
    # ... build choices ...
    next if scalar(@choices_unique) < 3;

    $question_built = 1;
    last;
}

if (!$question_built) {
    die 'Failed to build a valid question.';
}
```
- **Textbook gap it fills**: The textbook needs examples of managing large randomized data pools, the retry-loop pattern for complex constraints, and seed-stable randomization with PGrandom vs global random().

### Chapter 5: Question Types (MC, Matching, Ordering, Numeric)

- **Relevant files**: `isoelectric_one_protein.pgml` (RadioButtons), `bond_types-matching.pgml` (DropDown matching), `ordering_entropy.pgml` (DraggableProof), `amino_acids_properties-matching.pgml` (matching with exclude_pairs), `histidine_protonation_states.pg` (custom radio cards)
- **What to extract**: RadioButtons configuration (labels, displayLabels, randomize, separator), DropDown/PopUp matching pattern with partial credit grading, DraggableProof with DamerauLevenshtein scoring, custom HTML radio card pattern with hidden ans_rule.
- **Example snippet** (RadioButtons from `isoelectric_one_protein.pgml`, lines 166-173):
```perl
$rb = RadioButtons(
    [@choices],
    $answer_text,
    labels        => 'ABC',
    displayLabels => 1,
    randomize     => 0,
    separator     => '<div style="margin-bottom: 0.7em;"></div>',
);
```
- **Example snippet** (DraggableProof from `ordering_entropy.pgml`, lines 46-52):
```perl
$proof = DraggableProof(
    [@correct_order],
    [],
    AllowNewBlanks   => 0,
    NumBuckets       => 1,
    OrderMatters     => 1,
    ResetButtonText  => 'Reset',
    Levenshtein      => 1,
);
```
- **Example snippet** (matching with partial credit from `bond_types-matching.pgml`, lines 134-145):
```perl
install_problem_grader(~~&custom_problem_grader_fluid);
$ENV{'grader_numright'} = [
    int($num_questions * 0.5),
    int($num_questions * 0.8),
    $num_questions
];
$ENV{'grader_scores'} = [0.25, 0.75, 1];
$ENV{'grader_message'} = 'To get full credit, all answers must be correct.';
```
- **Textbook gap it fills**: Comprehensive coverage of all major question types with biology-specific examples; partial credit grading configuration; custom UI patterns beyond standard macros.

### Chapter 6: Advanced PGML, HTML, CSS, and Graphics

- **Relevant files**: `kaleidoscope_ladder_unknown_band.pgml` (simulated gel), `rdkit_working_in_webwork.pgml` (RDKit.js), `macromolecule_identification.pgml` (RDKit at scale), `polypeptide_mc_sequence-easy.pgml` (RDKit highlighting), `titration_pI.pgml` (PGgraphmacros), `two_dimensional_gel_spots.pgml` (LayoutTable grid), `titration_buffer_graph_tool.pg` (GraphTool), `color_render_test.pg` (color methods), `matching_from_web.pgml` (two-column CSS layout), `poisson_flies.pgml` (niceTables)
- **What to extract**: RDKit.js integration pattern; HEADER_TEXT for CSS/JS injection; simulated gel via HTML/CSS absolute positioning; PGgraphmacros (init_graph, lineTo, stamps); niceTables LayoutTable; GraphTool with custom AnswerEvaluator; MODES() for HTML vs TeX; color rendering methods; two-column flex layouts.
- **Example snippet** (RDKit.js initialization from `rdkit_working_in_webwork.pgml`, lines 27-47):
```perl
HEADER_TEXT(<<'END_HEADER');
<script src="https://unpkg.com/@rdkit/rdkit/dist/RDKit_minimal.js"></script>
<script>
let RDKitReady = null;
function getRDKit() {
    if (!RDKitReady) { RDKitReady = initRDKitModule(); }
    return RDKitReady;
}
function initMoleculeCanvases() {
    getRDKit().then(function(RDKit) {
        const canvases = document.querySelectorAll('canvas[data-smiles]');
        canvases.forEach((canvas) => {
            const smiles = canvas.dataset.smiles;
            const mol = RDKit.get_mol(smiles);
            const mdetails = {"explicitMethyl": true};
            if (canvas && mol) {
                mol.draw_to_canvas_with_highlights(canvas,
                    JSON.stringify(mdetails));
            }
        });
    });
}
</script>
END_HEADER
```
- **Example snippet** (simulated SDS-PAGE gel band from `kaleidoscope_ladder_unknown_band.pgml`, lines 187-199):
```perl
sub build_gel_html {
    my ($gel_width, $lane_width, $well_width, $gel_height,
        @entries) = @_;
    my $html = "<div style='position:relative;"
        . " width:${gel_width}px; height:${gel_height}px;"
        . " background:linear-gradient(to bottom,"
        . " #e8e8f0 0%, #c0c0d8 100%);"
        . " border:2px solid #333;"
        . " font-size:11px;'>";
    # ... bands positioned with absolute CSS ...
    return $html;
}
```
- **Example snippet** (PGgraphmacros titration curve from `titration_pI.pgml`, lines 170-195):
```perl
$graph = init_graph(-0.3, -0.5, $x_max + 0.3, 15.5,
    axes => [0, 0],
    grid => [$x_max, 15],
    size => [500, 500],
);
$graph->lb('reset');
# draw titration curve segments
for my $seg_idx (0 .. $#curve_segments) {
    my @seg = @{$curve_segments[$seg_idx]};
    for my $i (0 .. $#seg - 1) {
        $graph->lineTo($seg[$i+1][0], $seg[$i+1][1], 'blue', 2);
    }
}
```
- **Textbook gap it fills**: This chapter benefits most from the repo. RDKit.js chemistry rendering, simulated gel electrophoresis, PGgraphmacros, and GraphTool with custom checkers are all patterns not yet covered in the textbook.

### Chapter 7: Debugging and Environment

- **Relevant files**: `check_pg_version.pg`, `get_webwork_env_variables.pg`, `get_macro_paths.pg`, `check_pg_macro_status_v2.18.pg`
- **What to extract**: PG version detection via function probing, envir variable dumping, macro path inspection, findMacroFile() usage, fallback patterns for cross-version compatibility.
- **Example snippet** (from `check_pg_macro_status_v2.18.pg`, lines 30-42):
```perl
my @test_macros = (
    'PGstandard.pl', 'PGML.pl',
    'parserRadioButtons.pl', 'PGcourse.pl',
    'parserPopUp.pl', 'niceTables.pl',
    'MathObjects.pl', 'PGchoicemacros.pl',
    'PGgraders.pl', 'parserGraphTool.pl',
    'draggableProof.pl', 'PGgraphmacros.pl',
);
for my $macro (@test_macros) {
    my $found = findMacroFile($macro);
    # report whether each macro is available
}
```
- **Textbook gap it fills**: Practical debugging tools for WeBWorK problem authors; version-aware coding patterns.

### Chapter 8: AI-Assisted Authoring and Scripting

- **Relevant files**: `alpha_amino_acid_identification.pg` (generated by Python script from YAML), `macromolecule_identification.pgml` (large generated data pool)
- **What to extract**: Examples of problems generated or assisted by scripts; YAML-to-PG pipeline pattern; large curated data sets that were likely assembled programmatically.
- **Example snippet** (from `alpha_amino_acid_identification.pg`, header comment):
```perl
# Generated by: amino_acid_radio_card_maker.py
# Input YAML: amino_acid_identification.yaml
```
- **Textbook gap it fills**: Shows real-world AI/scripting pipeline for generating WeBWorK problems at scale.

### Chapter 90: Appendix / Reference

- **Relevant files**: `color_render_test.pg` (color method catalog), all files for macro usage survey
- **What to extract**: Comprehensive macro reference; color rendering method comparison (6 methods); complete list of PG macros used across the repo.
- **Complete macro catalog across all files**:
  - `PGstandard.pl` - in all files
  - `PGML.pl` - in all .pgml files
  - `parserRadioButtons.pl` - MC problems
  - `parserPopUp.pl` - matching/dropdown problems
  - `PGcourse.pl` - in all files
  - `PGchoicemacros.pl` - older matching format
  - `PGgraders.pl` - partial credit grading
  - `niceTables.pl` - LayoutTable grid display
  - `MathObjects.pl` - Context("Numeric") etc.
  - `parserGraphTool.pl` - interactive graph problems
  - `draggableProof.pl` - ordering/drag-drop problems
  - `PGgraphmacros.pl` - static graph generation
  - `parserUtils.pl` - utility functions
- **Textbook gap it fills**: Appendix reference material for quick lookup of available macros and rendering techniques.

---

## Top 10 Most Useful Files

| Rank | File | Why |
|------|------|-----|
| 1 | `PUBCHEM/rdkit_working_in_webwork.pgml` | Cleanest RDKit.js integration pattern; essential for Ch6 chemistry rendering section |
| 2 | `electrophoresis/kaleidoscope_ladder_unknown_band.pgml` | Most sophisticated HTML/CSS visualization (simulated gel); exemplifies advanced Ch6 techniques |
| 3 | `electrophoresis/protein_gel_migration.pgml` | Best example of helper functions, retry-loop, large data pool, and CSS grid table; covers Ch4+Ch6 |
| 4 | `matching_sets/bond_types-matching.pgml` | Complete matching template with partial credit grading, colored labels, DropDown/PopUp compatibility |
| 5 | `electrophoresis/titration_pI.pgml` | PGgraphmacros titration curve + molecule state tiles + dual RadioButtons; covers Ch5+Ch6 |
| 6 | `PUBCHEM/AMINO_ACIDS/histidine_protonation_states.pg` | Custom HTML radio cards with RDKit rendering; advanced UI beyond standard macros |
| 7 | `electrophoresis/two_dimensional_gel_spots.pgml` | niceTables LayoutTable 16x16 grid as 2D gel; most complex table-based visualization |
| 8 | `webwork_examples/ordering_entropy.pgml` | Only DraggableProof example; cleanest ordering question pattern for Ch5 |
| 9 | `buffers/pKa_buffer_state-diprotic.pgml` | Well-structured helper functions for chemical formula HTML formatting; reusable pattern |
| 10 | `webwork_examples/check_pg_version.pg` | Essential debugging tool; PG version detection via feature probing |

---

## Recommended Actions

1. **Add RDKit.js section to Chapter 6**: The repo has 8 files using RDKit.js for chemistry rendering. Extract the initialization pattern from `rdkit_working_in_webwork.pgml` and the SMILES canvas pattern. This is a unique capability not found in the OPL.

2. **Add simulated gel electrophoresis section to Chapter 6**: The `kaleidoscope_ladder_unknown_band.pgml` file is a showcase of HTML/CSS within PGML. Extract the gel simulation pattern as an advanced example.

3. **Add PGgraphmacros examples to Chapter 6**: The `titration_pI.pgml` file provides a complete example of init_graph, lineTo, stamps, and labels for creating static graphs.

4. **Expand Chapter 5 matching section**: The matching files show DropDown/PopUp compatibility wrappers, partial credit with custom_problem_grader_fluid, and exclude_pairs logic. These patterns are more sophisticated than typical OPL matching problems.

5. **Add DraggableProof to Chapter 5**: Currently only one example exists (`ordering_entropy.pgml`), but it demonstrates the complete pattern including DamerauLevenshtein scoring.

6. **Add retry-loop pattern to Chapter 4**: Multiple files use the `for my $attempt (1 .. $max_attempts) { ... next if invalid; ... last; }` pattern for constrained randomization. This should be documented as a best practice.

7. **Add helper function library to Chapter 4**: The `random_choice`, `shuffle_list`, and `sample_unique` functions appear in multiple files. Document these as reusable utilities.

8. **Add GraphTool with custom AnswerEvaluator to Chapter 6**: The `titration_buffer_graph_tool.pg` file shows how to create a custom checker for GraphTool point placement, a pattern not documented elsewhere.

9. **Add niceTables LayoutTable examples to Chapter 6**: The `two_dimensional_gel_spots.pgml` and `poisson_flies.pgml` files show different LayoutTable patterns (grid visualization vs data display).

10. **Extract large data pools for reference**: The protein bank (58 entries), amino acid SMILES (20 entries), and macromolecule SMILES (358 entries) could be referenced in a Chapter 90 appendix as reusable data sets.

---

## Pattern Coverage Summary

| Pattern | Files Using It | Textbook Coverage |
|---------|---------------|-------------------|
| RadioButtons MC | 12 files | Partially covered |
| DropDown/PopUp matching | 6 files | Partially covered |
| DraggableProof ordering | 1 file | Not covered |
| GraphTool interactive | 1 file | Not covered |
| Custom HTML radio cards | 3 files | Not covered |
| RDKit.js chemistry | 8 files | Not covered |
| PGgraphmacros static graphs | 1 file | Not covered |
| niceTables LayoutTable | 2 files | Not covered |
| HEADER_TEXT CSS/JS injection | 12 files | Partially covered |
| PGrandom seed-stable | 5 files | Not covered |
| Retry-loop randomization | 4 files | Not covered |
| Partial credit grading | 5 files | Not covered |
| MODES() HTML vs TeX | 3 files | Not covered |
| Chemical formula HTML | 6 files | Not covered |
| Simulated gel via CSS | 1 file | Not covered |
