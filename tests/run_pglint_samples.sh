#!/usr/bin/env bash
set -euo pipefail

debug_flag=""
if [ "${1-}" = "--debug" ]; then
	debug_flag="--debug"
fi

health_json="$(curl -s http://localhost:3000/health)" || {
	echo "Health check failed: curl error"
	exit 1
}
echo ""
echo "Renderer health"
echo "---------------"
echo "${health_json}" | jq
echo ""
echo "${health_json}" | jq -e '.status == "ok"' > /dev/null || {
	echo "Health check failed: status not ok"
	exit 1
}
echo ""
/opt/homebrew/opt/python@3.12/bin/python3.12 tools/pglint.py tests/sample_pgml_problem.pg ${debug_flag:+$debug_flag}
echo ""
echo "Expected: missing PGML macro error"
/opt/homebrew/opt/python@3.12/bin/python3.12 tools/pglint.py tests/sample_error_missing_pgml_macro.pg ${debug_flag:+$debug_flag} || true
echo ""
echo "Expected: missing choice macro error (RadioButtons)"
/opt/homebrew/opt/python@3.12/bin/python3.12 tools/pglint.py tests/sample_error_missing_mathobjects.pg ${debug_flag:+$debug_flag} || true
echo ""
echo "Expected: syntax error (missing semicolon)"
/opt/homebrew/opt/python@3.12/bin/python3.12 tools/pglint.py tests/sample_error_syntax.pg ${debug_flag:+$debug_flag} || true
