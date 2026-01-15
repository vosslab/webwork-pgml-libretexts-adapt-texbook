#!/usr/bin/env bash
set -euo pipefail

curl -s http://localhost:3000/health | jq
/opt/homebrew/opt/python@3.12/bin/python3.12 tools/pglint.py tests/sample_pgml_problem.pg --debug
/opt/homebrew/opt/python@3.12/bin/python3.12 tools/pglint.py tests/sample_error_missing_pgml_macro.pg || true
/opt/homebrew/opt/python@3.12/bin/python3.12 tools/pglint.py tests/sample_error_missing_mathobjects.pg || true
/opt/homebrew/opt/python@3.12/bin/python3.12 tools/pglint.py tests/sample_error_syntax.pg || true
