#!/usr/bin/env python3

"""
Extract complete PGML problems from textbook HTML and validate them
via static lint and the pg-renderer API.
"""

# Standard Library
import os
import csv
import sys
import argparse

# Ensure sibling tools are importable
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
if TOOLS_DIR not in sys.path:
	sys.path.insert(0, TOOLS_DIR)

# local repo modules (sibling scripts under tools/)
import pglint
import webwork_simple_lint
import extract_textbook_pre_blocks


def parse_args() -> argparse.Namespace:
	"""
	Parse command-line arguments.
	"""
	parser = argparse.ArgumentParser(
		description="Extract textbook PGML problems and validate via static + renderer lint.",
	)
	parser.add_argument(
		"-d",
		"--directory",
		dest="input_dir",
		default="Textbook",
		help="Directory to scan for .html files (default: Textbook).",
	)
	parser.add_argument(
		"-o",
		"--output",
		dest="output_dir",
		default=os.path.join("output", "textbook_pre_blocks"),
		help="Directory to write extracted .pg files (default: output/textbook_pre_blocks).",
	)
	parser.add_argument(
		"--skip-renderer",
		dest="skip_renderer",
		action="store_true",
		help="Skip renderer lint (static-only mode).",
	)
	parser.add_argument(
		"--no-skip-renderer",
		dest="skip_renderer",
		action="store_false",
		help="Run renderer lint (default).",
	)
	parser.set_defaults(skip_renderer=False)
	parser.add_argument(
		"-H",
		"--host",
		dest="host",
		default="http://localhost:3000",
		help="Renderer base URL (default: http://localhost:3000).",
	)
	parser.add_argument(
		"-s",
		"--seed",
		dest="seed",
		type=int,
		default=1,
		help="Problem seed for reproducibility (default: 1).",
	)
	args = parser.parse_args()
	return args


#============================================


def extract_problems(input_dir: str, output_dir: str) -> list[dict]:
	"""
	Extract <pre> blocks from HTML files and write full problems to .pg files.

	Returns a list of dicts with keys: source_file, block_index, pg_file, text.
	Only blocks that look like full PG problems are included.
	"""
	html_files = extract_textbook_pre_blocks.find_html_files(input_dir)
	os.makedirs(output_dir, exist_ok=True)
	problems: list[dict] = []
	for file_path in html_files:
		with open(file_path, "r", encoding="utf-8") as handle:
			html_text = handle.read()
		tree = extract_textbook_pre_blocks.parse_html_fragment(html_text, file_path)
		pre_blocks = tree.xpath(".//pre")
		if not pre_blocks:
			continue
		rel_path = os.path.relpath(file_path, start=input_dir)
		for index, pre in enumerate(pre_blocks, start=1):
			text = pre.text_content()
			if not extract_textbook_pre_blocks.is_full_problem(text):
				continue
			# Write the block to a .pg file
			line = getattr(pre, "sourceline", None)
			pg_file = extract_textbook_pre_blocks.write_block(
				output_dir=output_dir,
				rel_path=rel_path,
				block_index=index,
				line=str(line) if line is not None else None,
				text=text,
			)
			problems.append({
				"source_file": rel_path,
				"block_index": index,
				"pg_file": pg_file,
				"text": text,
			})
	return problems


#============================================


def run_static_lint(problems: list[dict]) -> list[dict]:
	"""
	Run static lint on each extracted problem text.

	Adds static_status and static_messages keys to each problem dict.
	"""
	for problem in problems:
		result = webwork_simple_lint.lint_text_to_result(problem["text"])
		problem["static_status"] = result["status"]
		# Format messages as semicolon-separated strings
		messages = []
		for issue in result["issues"]:
			messages.append(f"{issue['severity']}: {issue['message']}")
		problem["static_messages"] = "; ".join(messages)
	return problems


#============================================


def run_renderer_lint(problems: list[dict], host: str, seed: int) -> list[dict]:
	"""
	Run renderer lint on each extracted .pg file.

	Adds renderer_status and renderer_messages keys to each problem dict.
	"""
	for problem in problems:
		from pathlib import Path
		pg_path = Path(problem["pg_file"])
		result = pglint.lint_file_to_result(pg_path, host=host, seed=seed)
		problem["renderer_status"] = result["status"]
		problem["renderer_messages"] = "; ".join(result["issues"])
	return problems


#============================================


def skip_renderer_lint(problems: list[dict]) -> list[dict]:
	"""
	Mark all problems as renderer-skipped when the renderer is not available.
	"""
	for problem in problems:
		problem["renderer_status"] = "skipped"
		problem["renderer_messages"] = ""
	return problems


#============================================


def compute_overall_status(static_status: str, renderer_status: str) -> str:
	"""
	Compute an overall status from static and renderer results.
	"""
	# Error from either means overall error
	if static_status == "error" or renderer_status == "error":
		return "error"
	# Warning from either means overall warn
	if static_status == "warn" or renderer_status == "warn":
		return "warn"
	# Skipped renderer with passing static is still pass
	if renderer_status == "skipped" and static_status == "pass":
		return "pass"
	# Both pass
	if static_status == "pass" and renderer_status == "pass":
		return "pass"
	return "warn"


#============================================


def write_csv_report(problems: list[dict], output_dir: str) -> str:
	"""
	Write a CSV report of lint results.

	Returns the path to the written CSV file.
	"""
	csv_path = os.path.join(output_dir, "lint_report.csv")
	fieldnames = [
		"source_file",
		"block_index",
		"pg_file",
		"static_status",
		"static_messages",
		"renderer_status",
		"renderer_messages",
		"overall_status",
	]
	with open(csv_path, "w", encoding="utf-8", newline="") as handle:
		writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
		writer.writeheader()
		for problem in problems:
			# Compute overall status
			problem["overall_status"] = compute_overall_status(
				problem.get("static_status", "pass"),
				problem.get("renderer_status", "skipped"),
			)
			writer.writerow(problem)
	return csv_path


#============================================


def print_summary(problems: list[dict]) -> None:
	"""
	Print a console summary of lint results.
	"""
	total = len(problems)
	pass_count = 0
	warn_count = 0
	error_count = 0
	skipped_count = 0
	for problem in problems:
		overall = problem.get("overall_status", "pass")
		if overall == "pass":
			pass_count += 1
		elif overall == "warn":
			warn_count += 1
		elif overall == "error":
			error_count += 1
	# Count renderer-skipped separately
	for problem in problems:
		if problem.get("renderer_status") == "skipped":
			skipped_count += 1
	print("")
	print("=" * 50)
	print("Textbook PGML Problem Lint Summary")
	print(f"  Total problems extracted: {total}")
	print(f"  Pass:    {pass_count}")
	print(f"  Warn:    {warn_count}")
	print(f"  Error:   {error_count}")
	if skipped_count > 0:
		print(f"  Renderer skipped: {skipped_count}")
	print("=" * 50)
	print("")


#============================================


def main() -> None:
	"""
	Run the full textbook problem extraction and lint pipeline.
	"""
	args = parse_args()

	# Step 1: Extract full problems from HTML
	print(f"Scanning HTML files in: {args.input_dir}")
	problems = extract_problems(args.input_dir, args.output_dir)
	print(f"Extracted {len(problems)} complete PG problems to: {args.output_dir}")
	if not problems:
		print("No complete PG problems found. Nothing to lint.")
		return

	# Step 2: Static lint
	print("Running static lint...")
	problems = run_static_lint(problems)

	# Step 3: Renderer lint (or skip)
	if args.skip_renderer:
		print("Renderer lint: skipped (--skip-renderer)")
		problems = skip_renderer_lint(problems)
	else:
		# Check renderer health before trying
		print(f"Checking renderer health at {args.host}...")
		is_healthy = pglint.check_renderer_health(args.host)
		if is_healthy:
			print("Renderer is healthy. Running renderer lint...")
			problems = run_renderer_lint(problems, args.host, args.seed)
		else:
			print(f"Renderer at {args.host} is not reachable. Marking as skipped.")
			problems = skip_renderer_lint(problems)

	# Step 4: Write CSV report
	csv_path = write_csv_report(problems, args.output_dir)
	print(f"Lint report written to: {csv_path}")

	# Step 5: Print summary
	print_summary(problems)


if __name__ == "__main__":
	main()
