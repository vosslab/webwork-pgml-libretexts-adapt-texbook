#!/usr/bin/env python3

"""
Extract complete PGML problems from textbook HTML and validate them
via the pg-renderer API.
"""

# Standard Library
import os
import csv
import sys
import json
import time
import random
import argparse
import urllib.request

# Ensure sibling tools are importable
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
if TOOLS_DIR not in sys.path:
	sys.path.insert(0, TOOLS_DIR)

# local repo modules (sibling scripts under tools/)
import extract_textbook_pre_blocks

# Path to the full pg-renderer lint script
RENDERER_SCRIPT_DIR = os.path.normpath(
	os.path.join(TOOLS_DIR, "..", "..", "webwork-pg-renderer", "script")
)


def parse_args() -> argparse.Namespace:
	"""
	Parse command-line arguments.
	"""
	parser = argparse.ArgumentParser(
		description="Extract textbook PGML problems and validate via the pg-renderer.",
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


def check_renderer_health(host: str) -> bool:
	"""
	Check whether the renderer is reachable by GETting its /health endpoint.
	"""
	url = f"{host.rstrip('/')}/health"
	request = urllib.request.Request(url, method="GET")
	try:
		with urllib.request.urlopen(request, timeout=5) as response:
			is_healthy = response.status == 200
	except Exception:
		is_healthy = False
	return is_healthy


#============================================


def render_pg_source(source_text: str, host: str, seed: int) -> dict:
	"""
	Post PG source to the renderer /render-api endpoint and return the JSON response.
	"""
	url = f"{host.rstrip('/')}/render-api"
	payload = {
		"problemSource": source_text,
		"problemSeed": seed,
		"outputFormat": "classic",
	}
	body = json.dumps(payload).encode("utf-8")
	headers = {"Content-Type": "application/json"}
	# throttle API calls per repo guidance
	time.sleep(random.random())
	request = urllib.request.Request(url, data=body, headers=headers, method="POST")
	with urllib.request.urlopen(request, timeout=60) as response:
		raw_body = response.read().decode("utf-8")
		try:
			json_body = json.loads(raw_body)
			return json_body
		except json.JSONDecodeError:
			return {
				"renderedHTML": raw_body,
				"warnings": ["renderer returned non-JSON response; parsing HTML only"],
			}


#============================================


def normalize_messages(value) -> list[str]:
	"""
	Normalize response fields into a list of strings.
	"""
	if value is None:
		return []
	if isinstance(value, list):
		return [str(item) for item in value if item is not None]
	return [str(value)]


#============================================


def collect_lint_messages(response: dict) -> list[str]:
	"""
	Collect lint messages from the layered response fields.
	"""
	messages: list[str] = []
	messages += normalize_messages(response.get("errors"))
	# filter out informational notes about response format
	raw_warnings = normalize_messages(response.get("warnings"))
	for warning in raw_warnings:
		if "non-JSON response" in warning:
			continue
		messages.append(warning)
	messages += normalize_messages(response.get("error"))
	messages += normalize_messages(response.get("warning"))
	messages += normalize_messages(response.get("message"))

	debug = response.get("debug", {}) if isinstance(response.get("debug"), dict) else {}
	messages += normalize_messages(debug.get("pg_warn"))
	messages += normalize_messages(debug.get("internal"))
	messages += normalize_messages(debug.get("debug"))

	if messages:
		return messages

	# fall back to scanning rendered HTML for error sections
	rendered_html = response.get("renderedHTML", "")
	if not rendered_html:
		return messages
	warning_terms = ("Translator errors", "Warning messages")
	for term in warning_terms:
		if term in rendered_html:
			messages.append(f"renderedHTML contains '{term}' section")
	return messages


#============================================


def is_error_flagged(response: dict) -> bool:
	"""
	Check whether the response flags an error via JSON fields or HTML content.
	"""
	# check structured JSON error fields
	flags = response.get("flags", {}) if isinstance(response.get("flags"), dict) else {}
	if bool(flags.get("error_flag")):
		return True
	if response.get("errors"):
		return True
	if response.get("error"):
		return True
	# check rendered HTML for error indicators (non-JSON responses)
	rendered_html = response.get("renderedHTML", "")
	if "Translator errors" in rendered_html:
		return True
	if "ERROR caught by Translator" in rendered_html:
		return True
	return False


#============================================


def run_renderer_lint(problems: list[dict], host: str, seed: int) -> list[dict]:
	"""
	Render each extracted problem through the pg-renderer and record status.

	Adds status and messages keys to each problem dict.
	"""
	for problem in problems:
		# read the extracted .pg file
		with open(problem["pg_file"], "r", encoding="utf-8") as handle:
			source_text = handle.read()
		response = render_pg_source(source_text, host, seed)
		has_error = is_error_flagged(response)
		messages = collect_lint_messages(response)
		if has_error:
			problem["status"] = "error"
		elif messages:
			problem["status"] = "warn"
		else:
			problem["status"] = "pass"
		problem["messages"] = "; ".join(messages)
	return problems


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
		"status",
		"messages",
	]
	with open(csv_path, "w", encoding="utf-8", newline="") as handle:
		writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
		writer.writeheader()
		for problem in problems:
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
	for problem in problems:
		status = problem.get("status", "pass")
		if status == "pass":
			pass_count += 1
		elif status == "warn":
			warn_count += 1
		elif status == "error":
			error_count += 1
	print("")
	print("=" * 50)
	print("Textbook PGML Problem Lint Summary")
	print(f"  Total problems extracted: {total}")
	print(f"  Pass:    {pass_count}")
	print(f"  Warn:    {warn_count}")
	print(f"  Error:   {error_count}")
	print("=" * 50)
	print("")


#============================================


def main() -> None:
	"""
	Run the full textbook problem extraction and renderer lint pipeline.
	"""
	args = parse_args()

	# Step 1: Extract full problems from HTML
	print(f"Scanning HTML files in: {args.input_dir}")
	problems = extract_problems(args.input_dir, args.output_dir)
	print(f"Extracted {len(problems)} complete PG problems to: {args.output_dir}")
	if not problems:
		print("No complete PG problems found. Nothing to lint.")
		return

	# Step 2: Check renderer health
	print(f"Checking renderer health at {args.host}...")
	is_healthy = check_renderer_health(args.host)
	if not is_healthy:
		print(f"Renderer at {args.host} is not reachable. Cannot lint.")
		raise SystemExit(1)
	print("Renderer is healthy. Running renderer lint...")

	# Step 3: Render each problem through the pg-renderer
	problems = run_renderer_lint(problems, args.host, args.seed)

	# Step 4: Write CSV report
	csv_path = write_csv_report(problems, args.output_dir)
	print(f"Lint report written to: {csv_path}")

	# Step 5: Print summary
	print_summary(problems)


if __name__ == "__main__":
	main()
