# Mining Report: webwork-pg-renderer

## Repo Overview

The webwork-pg-renderer is a standalone Mojolicious (Perl) web application that renders WeBWorK PG/PGML problems via an HTTP API and an optional browser-based editor UI. It is derived from the WeBWorK2 codebase and vendored with the PG engine (PG-2.17+ branch from openwebwork/pg). The renderer accepts PG source code (inline, by file path, or fetched from a remote URL), invokes the PG rendering engine inside a subprocess, and returns formatted HTML plus structured JSON metadata including answer data, diagnostics, JWT tokens, and resource lists.

The repo is maintained as a fork by Neil Voss (@vossab) with additions for local development via podman-compose, a `private/` directory for local problems, a lint-via-API script, smoke tests in Perl, Python, and Bash, and comprehensive API documentation. The application runs inside a Docker/Podman container based on Ubuntu 24.04 with TeX Live, ImageMagick, GD, and all required Perl and Node.js dependencies.

## API Endpoints

### Primary Render Endpoints

| Endpoint | Method | Description |
| --- | --- | --- |
| `POST /` | POST | Primary render endpoint (same behavior as `/render-api`) |
| `POST /render-api` | POST | Compatibility render endpoint; accepts form data or JSON |
| `GET /render-api` | GET | Returns 405 with hint to use POST |
| `POST /render-ptx` | POST | Renders problem in PreTeXt (PTX) XML format |
| `GET /health` | GET | Returns JSON with status, mode, and dependency versions (PG, jQuery, jQuery UI, CodeMirror, Node) |

### JWT Endpoints (development mode only)

| Endpoint | Method | Description |
| --- | --- | --- |
| `POST /render-api/jwt` | POST | Returns a signed problem JWT (HS256) from request parameters |
| `POST /render-api/jwe` | POST | Returns a JWE-encrypted problem JWT (PBES2-HS512+A256KW / A256GCM) |

### Library/IO Endpoints (development mode only)

| Endpoint | Method | Description |
| --- | --- | --- |
| `POST /render-api/tap` | POST | Read raw PG source from a file path |
| `POST /render-api/can` | POST | Write PG source to a file path (private/ only) |
| `GET /render-api/cat` | GET | Catalog directory contents (depth-limited search) |
| `GET /render-api/find` | GET | Search for PG files by path fragments (ranked matching) |
| `POST /render-api/upload` | POST | Upload a file to private/ |
| `DELETE /render-api/remove` | DELETE | Delete a file or empty directory from private/ |
| `POST /render-api/clone` | POST | Clone a file or directory within private/ |
| `POST /render-api/tags` | POST | Get/set problem metadata tags |
| `POST /render-api/sma` | POST | ShowMeAnother: find a new seed producing a different variant |
| `POST /render-api/unique` | POST | Find N unique seeds that produce distinct problem variants |

### UI Pages (development mode only)

| Endpoint | Method | Description |
| --- | --- | --- |
| `GET /` | GET | Two-column editor UI (CodeMirror editor + rendered preview iframe) |
| `GET /opl` | GET | OPL browser UI |

### Required Render Parameters

One source parameter is required (in order of precedence):

1. `problemSourceURL` (string) - URL to fetch JSON containing `raw_source`
2. `problemSource` (string, optionally base64) - raw PG source code
3. `sourceFilePath` (string) - path relative to `Library/`, `Contrib/`, or `private/`

Plus:

- `problemSeed` (integer, required) - seed for reproducible randomization

### Display/Formatting Parameters

| Key | Type | Default | Notes |
| --- | --- | --- | --- |
| `_format` | string | `html` | Response structure: `html` or `json` |
| `outputFormat` | string | `default` | Output style: `default`, `static`, `ptx`, `raw`, `json` |
| `displayMode` | string | `MathJax` | Math rendering: `MathJax` or `ptx` |
| `language` | string | `en` | Locale for template strings |

### Interaction Parameters

| Key | Type | Default | Notes |
| --- | --- | --- | --- |
| `hidePreviewButton` | number(bool) | 0 | Hide "Preview My Answers" |
| `hideCheckAnswersButton` | number(bool) | 0 | Hide "Submit Answers" |
| `showCorrectAnswersButton` | number(bool) | isInstructor | Show "Show Correct Answers" |

### Content Parameters

| Key | Type | Default | Notes |
| --- | --- | --- | --- |
| `isInstructor` | number(bool) | 0 | Enable instructor view |
| `showHints` | number(bool) | 1 | Show hints |
| `showSolutions` | number(bool) | isInstructor | Show solutions |
| `hideAttemptsTable` | number(bool) | 0 | Hide answer preview/results table |
| `showSummary` | number(bool) | 1 | Show summary under attempts table |
| `showComments` | number(bool) | 0 | Render author comments |
| `showFooter` | number(bool) | 0 | Show version/copyright footer |
| `includeTags` | number(bool) | 0 | Include metadata tags in JSON |
| `permissionLevel` | number | 0 | Deprecated; use isInstructor |

### JSON Response Schema (`_format: "json"`)

```json
{
  "renderedHTML": "<!doctype html>...",
  "debug": {
    "perl_warn": null,
    "pg_warn": ["..."],
    "debug": ["..."],
    "internal": ["..."]
  },
  "problem_result": { "score": 0 },
  "problem_state": {},
  "flags": { "error_flag": 0 },
  "resources": {
    "regex": [],
    "alias": {},
    "assets": []
  },
  "JWT": {
    "problem": "...",
    "session": "...",
    "answer": "..."
  }
}
```

Conditional fields when `isInstructor=1`: `answers`, `inputs`, `pgcore`.
Conditional fields when `includeTags=1`: `tags`, `raw_metadata_text`.

### Error Response Schema

```json
{
  "message": "[request_id] Error description.",
  "status": 500
}
```

### Validation Error Schema

```json
{
  "statusCode": 412,
  "error": "Precondition Failed",
  "message": ["Field 'sourceFilePath' failed to validate 'like' check"],
  "data": { "failed": ["sourceFilePath"], "passed": [] }
}
```

## Setup/Configuration

### Docker Setup (primary)

```bash
mkdir volumes container
git clone https://github.com/openwebwork/webwork-open-problem-library volumes/webwork-open-problem-library
git clone --recursive https://github.com/openwebwork/renderer container/
docker build --tag renderer:1.0 ./container
docker run -d --rm --name standalone-renderer --publish 3000:3000 \
  --mount type=bind,source="$(pwd)"/volumes/webwork-open-problem-library/,target=/usr/app/webwork-open-problem-library \
  --env MOJO_MODE=development renderer:1.0
```

### Podman Compose (fork workflow)

```bash
mkdir private
./run.sh
```

The `run.sh` script builds the image with podman, starts `podman-compose up -d`, opens the health check and UI in a browser, and tails container logs. Ctrl-C triggers `podman-compose down`.

### Container Details

- Base image: Ubuntu 24.04
- Exposes port 3000
- Server: Hypnotoad (Mojolicious production server) or Morbo (development)
- PG engine: cloned at build time from openwebwork/pg PG-2.17+ branch
- TeX: texlive-latex-recommended, texlive-fonts-recommended, dvipng
- Image tools: ImageMagick, GD
- Node deps: jQuery, jQuery UI, Bootstrap, MathJax, CodeMirror, iframeResizer

### Configuration File: `render_app.conf`

Copy `render_app.conf.dist` to `render_app.conf`. Key settings:

| Key | Default | Description |
| --- | --- | --- |
| `secrets` | `['abracadabra']` | Mojolicious session secrets |
| `baseURL` | `''` | URL prefix for renderer routes |
| `formURL` | `'/render-api'` | Form submission target URL |
| `SITE_HOST` | `'http://localhost:3000'` | Public hostname |
| `CORS_ORIGIN` | `'http://localhost:3000'` | CORS origin header |
| `STRICT_JWT` | 0 | Require JWT for all requests |
| `STATIC_EXPIRES` | 86400 | Cache-Control max-age for static assets |

Hypnotoad settings: 10 workers, 5 spare, 100 clients per worker, 400 max accepts.

### PG Configuration: `conf/pg_config.yml`

Copied into the container at `/usr/app/lib/PG/conf/pg_config.yml`. Key settings:

- Macro search path: `.`, `$pg_root/macros`, plus `$render_root/private/macros` for custom macros
- External programs: latex, pdflatex, dvisvgm, pdf2svg, convert, dvipng
- Math entry: MathQuill by default
- SVG method: dvisvgm
- Default grader: `avg_problem_grader`
- Answer evaluator defaults for numeric and function comparisons

### Environment Variables

| Variable | Set In | Description |
| --- | --- | --- |
| `RENDER_ROOT` | RenderApp.pm | Application root directory |
| `PG_ROOT` | RenderApp.pm | PG engine root |
| `OPL_DIRECTORY` | RenderApp.pm | OPL root path |
| `PERL5LIB` | Dockerfile/compose | Perl library search path |
| `MOJO_MODE` | compose/CLI | `development` or `production` |
| `MOJO_CONFIG` | RenderApp.pm | Path to config file |
| `MOJO_LOG_LEVEL` | RenderApp.pm | Log verbosity (default: debug) |

## Macro Availability

The renderer ships with the full PG-2.17+ macro set cloned at build time. All macros live in `lib/PG/macros/` (flat directory in this branch). The macro search path from `pg_config.yml` includes `$pg_root/macros` plus `$render_root/private/macros` for user-defined custom macros.

### Complete Macro List (130+ files)

**Core macros**: PG.pl, PGstandard.pl, PGbasicmacros.pl, PGanswermacros.pl, PGauxiliaryFunctions.pl, PGchoicemacros.pl, PGcourse.pl, PGcommonFunctions.pl, PGinfo.pl, MathObjects.pl, Value.pl, Parser.pl, PGML.pl

**Context macros** (27): contextFraction.pl, contextInequalities.pl, contextCurrency.pl, contextPercent.pl, contextScientificNotation.pl, contextString.pl, contextTF.pl, contextTrigDegrees.pl, contextInteger.pl, contextLimitedNumeric.pl, contextLimitedPolynomial.pl, contextLimitedFactor.pl, contextLimitedRadical.pl, contextLimitedPowers.pl, contextLimitedComplex.pl, contextLimitedPoint.pl, contextLimitedVector.pl, contextPiecewiseFunction.pl, contextPolynomialFactors.pl, contextRationalFunction.pl, contextReaction.pl, contextArbitraryString.pl, contextOrdering.pl, contextPartition.pl, contextPermutation.pl, contextPeriodic.pl, contextTypeset.pl

**Parser macros** (25): parserPopUp.pl, parserRadioButtons.pl, parserMultiAnswer.pl, parserMultiPart.pl, parserFormulaWithUnits.pl, parserNumberWithUnits.pl, parserFormulaUpToConstant.pl, parserFunction.pl, parserFunctionPrime.pl, parserAssignment.pl, parserImplicitEquation.pl, parserImplicitPlane.pl, parserGraphTool.pl, parserWordCompletion.pl, parserOneOf.pl, parserVectorUtils.pl, parserLinearInequality.pl, parserParametricLine.pl, parserParametricPlane.pl, parserDifferenceQuotient.pl, parserFormulaAnyVar.pl, parserRoot.pl, parserPrime.pl, parserSolutionFor.pl, parserQuotedString.pl

**Answer/grading macros**: answerHints.pl, answerCustom.pl, answerComposition.pl, extraAnswerEvaluators.pl, PGgraders.pl, weightedGrader.pl, PGessaymacros.pl

**Graphics macros**: PGgraphmacros.pl, PGtikz.pl, PGlateximage.pl, PGanalyzeGraph.pl, PGstatisticsGraphMacros.pl, LiveGraphics3D.pl, CanvasObject.pl

**UI/interaction macros**: scaffold.pl, draggableProof.pl, draggableSubsets.pl, niceTables.pl, unionTables.pl, unionLists.pl, quickMatrixEntry.pl, alignedChoice.pl

**Math/science macros**: PGcomplexmacros.pl, PGdiffeqmacros.pl, PGmatrixmacros.pl, PGmorematrixmacros.pl, MatrixCheckers.pl, MatrixReduce.pl, MatrixUnits.pl, PGnumericalmacros.pl, PGpolynomialmacros.pl, PGstatisticsmacros.pl, LinearProgramming.pl, Distributions (via PG modules)

**Special macros**: problemRandomize.pl, problemPanic.pl, problemPreserveAnswers.pl, compoundProblem.pl/2/5, RserveClient.pl, sage.pl, text2PG.pl, source.pl, tableau.pl

**Loaded PG Modules** (from pg_config.yml `modules` section): GD, AlgParser, AnswerHash, LaTeXImage, Circle, Complex, Distributions, Fraction, Matrix, PGrandom, Regression, Statistics, Units, VectorField, Parser, Value, Applet, PGcore, DragNDrop, JSON, Rserve, and more.

## Chapter Mapping

### Chapter 1: Introduction
- **Relevant files**: `README.md`, `docs/USAGE.md`
- **What to extract**: High-level description of what the renderer does and why instructors use it
- **Example snippets**:
```
This is a PG Renderer derived from the WeBWorK2 codebase.
ADAPT errors are often opaque. This renderer shows line level errors
and supports fast iteration before you import into ADAPT.
```
- **Textbook gap it fills**: Motivates why a standalone renderer matters for ADAPT workflows

### Chapter 2: Problem Generation PG
- **Relevant files**: `lib/WeBWorK/RenderProblem.pm`, `lib/RenderApp/Model/Problem.pm`
- **What to extract**: How the renderer processes PG source: base64 decoding, UNIX line ending normalization, seed handling, the `DOCUMENT()...ENDDOCUMENT()` parsing and UUID generation
- **Example snippets**:
```perl
# recognize and decode base64 if necessary
$contents = Encode::decode("UTF-8", decode_base64($contents))
    if ($contents =~ m!^([A-Za-z0-9+/]{4})*(...)?$!);
# UNIX style line-endings are required
$contents =~ s!\r\n?!\n!g;
```
- **Textbook gap it fills**: Explains the technical pipeline from PG source to rendered output

### Chapter 3: PGML
- **Relevant files**: `lib/PG/macros/PGML.pl` (vendored PG macro)
- **What to extract**: The PGML.pl macro is available in the renderer; problems using PGML syntax are rendered through the standard macro loading path
- **Textbook gap it fills**: Confirms PGML rendering is supported and available

### Chapter 4: Breaking Down Components
- **Relevant files**: `docs/CODE_ARCHITECTURE.md`, `docs/FILE_STRUCTURE.md`, `lib/RenderApp.pm`, `lib/RenderApp/Controller/Render.pm`
- **What to extract**: Data flow from POST request through controller -> model -> WeBWorK::PG -> FormatRenderedProblem; route definitions; helper registration
- **Example snippets**:
```
1. Client posts to /render-api with sourceFilePath or problemSource plus render options.
2. RenderApp::Controller::Render validates inputs, merges JWT claims, instantiates Problem.
3. Problem->render calls RenderProblem::process_pg_file, which invokes WeBWorK::PG.
4. FormatRenderedProblem turns the PG result into HTML and response metadata.
5. The controller returns JSON with renderedHTML, answer data, flags, and diagnostics.
```
- **Textbook gap it fills**: Detailed architecture reference for how PG problems are processed

### Chapter 5: Different Question Types
- **Relevant files**: `lib/PG/macros/` (full macro directory), `conf/pg_config.yml` (modules section)
- **What to extract**: Complete list of available context and parser macros that define question types; the modules loaded at startup that support different answer types
- **Textbook gap it fills**: Reference for which question types are supported in the standalone renderer vs. full WeBWorK

### Chapter 6: Advanced PGML Techniques
- **Relevant files**: `lib/PG/macros/PGtikz.pl`, `lib/PG/macros/PGlateximage.pl`, `lib/PG/macros/scaffold.pl`, `lib/PG/macros/draggableProof.pl`, `lib/PG/macros/draggableSubsets.pl`, `lib/PG/macros/niceTables.pl`, `conf/pg_config.yml` (externalPrograms, latexImageSVGMethod)
- **What to extract**: TikZ/LaTeX image generation configuration; scaffold macro for multi-part problems; drag-and-drop interaction macros; table formatting macros
- **Example snippets**:
```yaml
externalPrograms:
  latex: /usr/bin/latex --no-shell-escape
  pdflatex: /usr/bin/pdflatex --no-shell-escape
  dvisvgm: /usr/bin/dvisvgm
specialPGEnvironmentVars:
  latexImageSVGMethod: dvisvgm
```
- **Textbook gap it fills**: Configuration and toolchain for advanced rendering (TikZ, scaffolds, interactive elements)

### Chapter 7: Testing and Debugging (KEY CHAPTER)
- **Relevant files**: `script/smoke.sh`, `script/pg-smoke.pl`, `script/pg-smoke.py`, `script/lint_pg_via_renderer_api.py`, `script/lint.sh`, `script/lint-full.sh`, `script/HOW_TO_LINT.md`, `docs/RENDERER_API_USAGE.md`, `docs/USAGE.md`
- **What to extract**: Complete testing and debugging workflows including smoke tests, API lint, HTML rendering for visual QA, error detection in JSON responses, and Perl syntax checking
- **Example snippets**:
```bash
# Smoke test
curl -X POST "http://localhost:3000/render-api" \
  -H "Content-Type: application/json" \
  -d '{"sourceFilePath":"private/myproblem.pg","problemSeed":1234,"outputFormat":"classic"}'

# Lint via renderer API
python3 script/lint_pg_via_renderer_api.py -i private/myproblem.pg
# Render HTML for visual QA
python3 script/lint_pg_via_renderer_api.py -i private/myproblem.pg -r > /tmp/pg_render.html
```
- **Textbook gap it fills**: This is the **primary content source** for Chapters 7.2 and 7.3. Provides complete documentation for setting up the renderer, scripting against the API, detecting errors, and automating QA workflows.

#### Sub-mapping for Chapter 7.2: Setting Up the PG Renderer
- Docker install from README.md (build, run, mount volumes)
- Podman compose from docs/USAGE.md and run.sh
- Configuration files: render_app.conf.dist, conf/pg_config.yml
- Health check: GET /health endpoint
- Environment variables

#### Sub-mapping for Chapter 7.3: Scripting and Automation of the PG Renderer
- API endpoints and parameters from docs/RENDERER_API_USAGE.md
- curl examples for rendering, submitting answers, JWT flow
- Python smoke test (script/pg-smoke.py) and lint script (script/lint_pg_via_renderer_api.py)
- Perl smoke test (script/pg-smoke.pl) and Bash smoke (script/smoke.sh)
- Error detection: flags.error_flag, debug.pg_warn, debug.internal, renderedHTML scanning
- HOW_TO_LINT.md: complete lint workflow guide

### Chapter 7 (additional): Error Reporting
- **Relevant files**: `lib/RenderApp/Controller/Render.pm` (exception, croak), `lib/WeBWorK/FormatRenderedProblem.pm` (jsonResponse), `docs/RENDERER_API_USAGE.md`
- **What to extract**: Error handling chain: Problem model sets status codes (400/403/404/405/412/500), Controller::Render::exception formats JSON/HTML errors with request ID prefix, FormatRenderedProblem::jsonResponse includes debug block with pg_warn/internal/debug arrays
- **Example snippets**:
```perl
# Error codes in Problem.pm
our $codes = {
    400 => 'Bad Request',     403 => 'Forbidden',
    404 => 'Not Found',       405 => 'Method Not Allowed',
    412 => 'Precondition Failed', 500 => 'Internal Server Error',
};
# Exception formatting with request ID
sub exception {
    my ($c, $message, $status) = @_;
    $message = "[$id] " . $message;
    return $c->respond_to(
        json => { json => { message => $message, status => $status }, status => $status },
        html => { template => 'exception', message => $message, status => $status }
    );
}
```
- **Textbook gap it fills**: Explains how renderer error messages are structured, which is essential for debugging problem failures

### Chapter 8: Using AI Agents
- **Relevant files**: `AGENTS.md` (if present)
- **What to extract**: Agent workflow instructions if defined
- **Textbook gap it fills**: Could document how AI agents interact with the renderer API for automated testing

### Chapter 90: Appendices
- **Relevant files**: `conf/pg_config.yml` (full config reference), complete macro list, `cpanfile` (Perl dependencies)
- **What to extract**: Configuration reference, macro catalog, dependency list
- **Textbook gap it fills**: Reference appendix for all available macros, configuration options, and system requirements

## Top 10 Most Useful Files

1. **`docs/RENDERER_API_USAGE.md`** - Complete API reference with endpoints, parameters, response schemas, error detection guide, curl examples, JWT flow, UI request payloads, and lint guidance. Primary source for Ch7.3.
2. **`docs/USAGE.md`** - Instructor-focused quickstart workflow, setup options, troubleshooting basics. Primary source for Ch7.2.
3. **`README.md`** - Docker/local install instructions, complete API parameter tables, JWT documentation, editor UI description.
4. **`script/lint_pg_via_renderer_api.py`** - Python script for linting PG files via the renderer API. Demonstrates error detection from JSON responses. Key example for Ch7.3.
5. **`lib/RenderApp/Controller/Render.pm`** - Request parsing, JWT handling, remote source fetching, error handling. Explains the render pipeline.
6. **`lib/WeBWorK/RenderProblem.pm`** - Core render pipeline: PG invocation, JWT generation, error flag handling, resource tracking.
7. **`conf/pg_config.yml`** - PG configuration: macro search paths, external programs, answer evaluator defaults, module loading. Essential for understanding what the renderer supports.
8. **`docs/CODE_ARCHITECTURE.md`** - Architecture overview, data flow, extension points. Good for understanding the codebase structure.
9. **`script/HOW_TO_LINT.md`** - Complete lint workflow guide with script comparison table, prereqs, examples, and common errors.
10. **`lib/WeBWorK/FormatRenderedProblem.pm`** - Response formatting, JSON response construction, template rendering. Shows how debug info and error flags are structured in responses.

## Recommended Actions

1. **Extract Ch7.2 content from `docs/USAGE.md` and `README.md`**: These contain copy-paste Docker setup instructions, podman-compose workflow, and configuration guidance that directly map to the "Setting Up the PG Renderer" chapter.

2. **Extract Ch7.3 content from `docs/RENDERER_API_USAGE.md` and `script/HOW_TO_LINT.md`**: These provide complete scripting documentation including API endpoints, curl examples, Python/Perl smoke tests, lint workflows, and error detection strategies.

3. **Build a "Quick Reference" appendix from the API parameter tables**: The README.md contains comprehensive parameter tables (required, infrastructure, display, interaction, content) that should be reproduced as a textbook appendix.

4. **Document the JSON response error detection workflow**: The layered approach (flags.error_flag -> debug.pg_warn -> debug.internal -> renderedHTML scanning) from RENDERER_API_USAGE.md is critical for Chapter 7 and not documented elsewhere.

5. **Catalog the complete macro list for Chapter 5/Appendix**: The 130+ macros available in the renderer define what question types are supported. Cross-reference this with the textbook's question type chapters.

6. **Extract the JWT workflow for advanced automation docs**: The three-tier JWT system (problemJWT -> sessionJWT -> answerJWT) enables stateful problem interactions and grade reporting. This is relevant for Ch7.3 and any ADAPT integration content.

7. **Document the `problemSource` vs `sourceFilePath` vs `problemSourceURL` precedence**: This is a common source of confusion and should be prominent in Ch7.3.

8. **Include the smoke test scripts as textbook examples**: `script/pg-smoke.py` (53 lines) and `script/lint_pg_via_renderer_api.py` (130 lines) are concise, well-documented examples of renderer API automation that can be included directly in the textbook.

9. **Map the `pg_config.yml` macro search path to explain custom macro loading**: The fact that `$render_root/private/macros` is on the search path means instructors can add custom macros. This belongs in Ch6 or Ch7.

10. **Extract error codes and messages for a troubleshooting guide**: The Problem model's status code map (400/403/404/405/412/500) and the Controller's error formatting provide material for a troubleshooting section in Ch7.
