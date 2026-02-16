#!/usr/bin/env python3

"""
Tests for the textbook problem lint pipeline.
"""

import os
import csv
import sys

import pytest

# Ensure tools/ is importable
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(REPO_ROOT, "tools")
if TOOLS_DIR not in sys.path:
	sys.path.insert(0, TOOLS_DIR)

import pglint
import webwork_simple_lint
import extract_textbook_pre_blocks

# Import the pipeline module
import lint_textbook_problems


#============================================
# Tests for is_full_problem()
#============================================


def test_is_full_problem_good():
	"""Full problem with DOCUMENT() and ENDDOCUMENT() should return True."""
	text = "DOCUMENT();\nloadMacros('PGstandard.pl');\nENDDOCUMENT();"
	result = extract_textbook_pre_blocks.is_full_problem(text)
	assert result is True


def test_is_full_problem_missing_enddocument():
	"""Missing ENDDOCUMENT() should return False."""
	text = "DOCUMENT();\nloadMacros('PGstandard.pl');"
	result = extract_textbook_pre_blocks.is_full_problem(text)
	assert result is False


def test_is_full_problem_missing_document():
	"""Missing DOCUMENT() should return False."""
	text = "loadMacros('PGstandard.pl');\nENDDOCUMENT();"
	result = extract_textbook_pre_blocks.is_full_problem(text)
	assert result is False


def test_is_full_problem_snippet():
	"""A code snippet without either marker should return False."""
	text = "BEGIN_PGML\nSolve: [__]{$answer}\nEND_PGML"
	result = extract_textbook_pre_blocks.is_full_problem(text)
	assert result is False


#============================================
# Tests for extraction from HTML
#============================================


SAMPLE_HTML = """
<html><body>
<pre>
DOCUMENT();
loadMacros("PGstandard.pl", "MathObjects.pl", "PGML.pl");
TEXT(beginproblem());
$a = random(1, 5, 1);
$ans = Compute("$a + 2");
BEGIN_PGML
What is [$a] + 2? [__]{$ans}
END_PGML
ENDDOCUMENT();
</pre>
<pre>
This is just a code snippet, not a full problem.
BEGIN_PGML
Some text here.
END_PGML
</pre>
<pre>
DOCUMENT();
loadMacros("PGstandard.pl", "PGML.pl");
TEXT(beginproblem());
BEGIN_PGML
Hello world.
END_PGML
ENDDOCUMENT();
</pre>
</body></html>
"""


def test_extraction_count(tmp_path):
	"""Extracting from sample HTML should find exactly 2 full problems."""
	# Write sample HTML to a temp file
	html_dir = tmp_path / "html"
	html_dir.mkdir()
	html_file = html_dir / "test_page.html"
	html_file.write_text(SAMPLE_HTML, encoding="utf-8")
	output_dir = tmp_path / "output"
	output_dir.mkdir()
	# Run extraction
	problems = lint_textbook_problems.extract_problems(
		str(html_dir), str(output_dir)
	)
	assert len(problems) == 2


def test_extraction_writes_pg_files(tmp_path):
	"""Extracted problems should be written as .pg files."""
	html_dir = tmp_path / "html"
	html_dir.mkdir()
	html_file = html_dir / "sample.html"
	html_file.write_text(SAMPLE_HTML, encoding="utf-8")
	output_dir = tmp_path / "output"
	output_dir.mkdir()
	problems = lint_textbook_problems.extract_problems(
		str(html_dir), str(output_dir)
	)
	for problem in problems:
		assert os.path.isfile(problem["pg_file"])
		assert problem["pg_file"].endswith(".pg")


#============================================
# Tests for static lint
#============================================


def test_static_lint_missing_macros():
	"""Static lint should detect missing MathObjects.pl when Compute() is used."""
	# PG uses bare $ans = ... (no my/our), so use a non-blank variable to avoid
	# the unrelated blank-assignment warning
	text = (
		"DOCUMENT();\n"
		"loadMacros('PGstandard.pl', 'PGML.pl');\n"
		"$ans = Compute('5');\n"
		"BEGIN_PGML\nWhat is 5?\nEND_PGML\n"
		"ENDDOCUMENT();\n"
	)
	result = webwork_simple_lint.lint_text_to_result(text)
	assert result["status"] == "warn"
	assert result["warn_count"] > 0
	# Check that MathObjects or mathobjects is mentioned
	found_macro_warning = False
	for issue in result["issues"]:
		if "mathobjects" in issue["message"].lower():
			found_macro_warning = True
			break
	assert found_macro_warning


def test_static_lint_clean_problem():
	"""A well-formed problem with correct macros and no blanks should pass."""
	text = (
		"DOCUMENT();\n"
		"loadMacros('PGstandard.pl', 'MathObjects.pl', 'PGML.pl');\n"
		"TEXT(beginproblem());\n"
		"BEGIN_PGML\nWhat is 2 + 3?\nEND_PGML\n"
		"ENDDOCUMENT();\n"
	)
	result = webwork_simple_lint.lint_text_to_result(text)
	assert result["status"] == "pass"
	assert result["error_count"] == 0
	assert result["warn_count"] == 0


#============================================
# Tests for CSV report columns
#============================================


def test_csv_report_columns(tmp_path):
	"""CSV report should have all expected columns."""
	html_dir = tmp_path / "html"
	html_dir.mkdir()
	html_file = html_dir / "page.html"
	html_file.write_text(SAMPLE_HTML, encoding="utf-8")
	output_dir = tmp_path / "output"
	output_dir.mkdir()
	# Run the pipeline steps
	problems = lint_textbook_problems.extract_problems(
		str(html_dir), str(output_dir)
	)
	problems = lint_textbook_problems.run_static_lint(problems)
	problems = lint_textbook_problems.skip_renderer_lint(problems)
	csv_path = lint_textbook_problems.write_csv_report(problems, str(output_dir))
	# Read the CSV and check columns
	with open(csv_path, "r", encoding="utf-8") as handle:
		reader = csv.DictReader(handle)
		expected_columns = [
			"source_file",
			"block_index",
			"pg_file",
			"static_status",
			"static_messages",
			"renderer_status",
			"renderer_messages",
			"overall_status",
		]
		for col in expected_columns:
			assert col in reader.fieldnames


#============================================
# Tests for compute_overall_status()
#============================================


def test_overall_status_both_pass():
	"""Both pass should yield pass."""
	result = lint_textbook_problems.compute_overall_status("pass", "pass")
	assert result == "pass"


def test_overall_status_static_error():
	"""Static error should yield error regardless of renderer."""
	result = lint_textbook_problems.compute_overall_status("error", "pass")
	assert result == "error"


def test_overall_status_renderer_error():
	"""Renderer error should yield error regardless of static."""
	result = lint_textbook_problems.compute_overall_status("pass", "error")
	assert result == "error"


def test_overall_status_warn():
	"""Warn from either should yield warn."""
	result = lint_textbook_problems.compute_overall_status("warn", "pass")
	assert result == "warn"
	result = lint_textbook_problems.compute_overall_status("pass", "warn")
	assert result == "warn"


def test_overall_status_skipped():
	"""Skipped renderer with passing static should yield pass."""
	result = lint_textbook_problems.compute_overall_status("pass", "skipped")
	assert result == "pass"


def test_overall_status_error_trumps_warn():
	"""Error should trump warn."""
	result = lint_textbook_problems.compute_overall_status("error", "warn")
	assert result == "error"
	result = lint_textbook_problems.compute_overall_status("warn", "error")
	assert result == "error"


#============================================
# Integration test with renderer (skipped if unreachable)
#============================================


def renderer_available() -> bool:
	"""Check whether localhost:3000 is reachable."""
	return pglint.check_renderer_health("http://localhost:3000")


@pytest.mark.skipif(
	not renderer_available(),
	reason="pg-renderer not available at localhost:3000",
)
def test_renderer_lint_good_problem():
	"""A valid PG problem should pass renderer lint."""
	from pathlib import Path
	pg_file = Path(REPO_ROOT) / "tests" / "sample_pgml_problem.pg"
	result = pglint.lint_file_to_result(pg_file)
	assert result["status"] == "pass"
	assert result["exit_code"] == 0


@pytest.mark.skipif(
	not renderer_available(),
	reason="pg-renderer not available at localhost:3000",
)
def test_renderer_lint_syntax_error():
	"""A PG problem with syntax error should fail renderer lint."""
	from pathlib import Path
	pg_file = Path(REPO_ROOT) / "tests" / "sample_error_syntax.pg"
	result = pglint.lint_file_to_result(pg_file)
	assert result["status"] == "error"
	assert result["exit_code"] != 0
