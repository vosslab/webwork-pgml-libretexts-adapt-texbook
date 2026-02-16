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
	html_dir = tmp_path / "html"
	html_dir.mkdir()
	html_file = html_dir / "test_page.html"
	html_file.write_text(SAMPLE_HTML, encoding="utf-8")
	output_dir = tmp_path / "output"
	output_dir.mkdir()
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
	# Run extraction only (no renderer needed for CSV structure test)
	problems = lint_textbook_problems.extract_problems(
		str(html_dir), str(output_dir)
	)
	# Set placeholder status for CSV test
	for problem in problems:
		problem["status"] = "pass"
		problem["messages"] = ""
	csv_path = lint_textbook_problems.write_csv_report(problems, str(output_dir))
	with open(csv_path, "r", encoding="utf-8") as handle:
		reader = csv.DictReader(handle)
		expected_columns = [
			"source_file",
			"block_index",
			"pg_file",
			"status",
			"messages",
		]
		for col in expected_columns:
			assert col in reader.fieldnames


#============================================
# Tests for renderer health check
#============================================


def renderer_available() -> bool:
	"""Check whether localhost:3000 is reachable."""
	return lint_textbook_problems.check_renderer_health("http://localhost:3000")


#============================================
# Integration tests with renderer (skipped if unreachable)
#============================================


@pytest.mark.skipif(
	not renderer_available(),
	reason="pg-renderer not available at localhost:3000",
)
def test_renderer_lint_good_problem():
	"""A valid PG problem should pass renderer lint."""
	source_text = (
		"DOCUMENT();\n"
		"loadMacros('PGstandard.pl', 'MathObjects.pl', 'PGML.pl');\n"
		"Context('Numeric');\n"
		"$a = random(1, 5, 1);\n"
		"$ans = Real($a + 2);\n"
		"BEGIN_PGML\n"
		"What is [$a] + 2? [________]{$ans}\n"
		"END_PGML\n"
		"ENDDOCUMENT();\n"
	)
	response = lint_textbook_problems.render_pg_source(
		source_text, "http://localhost:3000", 1
	)
	has_error = lint_textbook_problems.is_error_flagged(response)
	assert has_error is False


@pytest.mark.skipif(
	not renderer_available(),
	reason="pg-renderer not available at localhost:3000",
)
def test_renderer_lint_undefined_function():
	"""A PG problem calling an undefined macro function should fail renderer lint."""
	# PopUp without parserPopUp.pl triggers a Translator error
	source_text = (
		"DOCUMENT();\n"
		"loadMacros('PGstandard.pl', 'PGML.pl');\n"
		"$popup = PopUp(['?','A','B'], 'A');\n"
		"BEGIN_PGML\nPick: [_]{$popup}\nEND_PGML\n"
		"ENDDOCUMENT();\n"
	)
	response = lint_textbook_problems.render_pg_source(
		source_text, "http://localhost:3000", 1
	)
	has_error = lint_textbook_problems.is_error_flagged(response)
	assert has_error is True
