#!/usr/bin/env python3

import argparse
import json
import os
import re
import sys


DEFAULT_BLOCK_RULES: list[dict[str, str]] = [
	{
		"label": "BEGIN_PGML/END_PGML",
		"start_pattern": r"\bBEGIN_PGML\b",
		"end_pattern": r"\bEND_PGML\b",
	},
	{
		"label": "BEGIN_TEXT/END_TEXT",
		"start_pattern": r"\bBEGIN_TEXT\b",
		"end_pattern": r"\bEND_TEXT\b",
	},
	{
		"label": "BEGIN_SOLUTION/END_SOLUTION",
		"start_pattern": r"\bBEGIN_SOLUTION\b",
		"end_pattern": r"\bEND_SOLUTION\b",
	},
	{
		"label": "BEGIN_HINT/END_HINT",
		"start_pattern": r"\bBEGIN_HINT\b",
		"end_pattern": r"\bEND_HINT\b",
	},
	{
		"label": "DOCUMENT()/ENDDOCUMENT()",
		"start_pattern": r"\bDOCUMENT\s*\(\s*\)",
		"end_pattern": r"\bENDDOCUMENT\s*\(\s*\)",
	},
]

DEFAULT_MACRO_RULES: list[dict[str, object]] = [
	{
		"label": "MathObjects functions",
		"pattern": r"\b(?:Context|Compute|Formula|Real)\s*\(",
		"required_macros": ["MathObjects.pl"],
	},
	{
		"label": "RadioButtons",
		"pattern": r"\bRadioButtons\s*\(",
		"required_macros": ["parserRadioButtons.pl", "PGchoicemacros.pl"],
	},
	{
		"label": "CheckboxList",
		"pattern": r"\bCheckboxList\s*\(",
		"required_macros": ["parserCheckboxList.pl", "PGchoicemacros.pl"],
	},
	{
		"label": "PopUp",
		"pattern": r"\bPopUp\s*\(",
		"required_macros": ["parserPopUp.pl", "PGchoicemacros.pl"],
	},
	{
		"label": "DataTable",
		"pattern": r"\bDataTable\s*\(",
		"required_macros": ["niceTables.pl"],
	},
	{
		"label": "LayoutTable",
		"pattern": r"\bLayoutTable\s*\(",
		"required_macros": ["niceTables.pl"],
	},
	{
		"label": "NumberWithUnits",
		"pattern": r"\bNumberWithUnits\s*\(",
		"required_macros": ["parserNumberWithUnits.pl", "contextUnits.pl"],
	},
	{
		"label": "Context('Fraction')",
		"pattern": r"\bContext\s*\(\s*['\"]Fraction['\"]\s*\)",
		"required_macros": ["contextFraction.pl"],
	},
	{
		"label": "DraggableSubsets",
		"pattern": r"\bDraggableSubsets\s*\(",
		"required_macros": ["draggableSubsets.pl"],
	},
]


def parse_args() -> argparse.Namespace:
	"""
	Parse command-line arguments.
	"""
	parser = argparse.ArgumentParser(
		description="Run a simple static lint pass on WeBWorK .pg files.",
	)
	parser.add_argument(
		"-i",
		"--input",
		dest="input_file",
		help="Path to a single .pg file to lint.",
	)
	parser.add_argument(
		"-d",
		"--directory",
		dest="input_dir",
		default=".",
		help="Directory to scan for .pg files (default: current directory).",
	)
	parser.add_argument(
		"-e",
		"--extensions",
		dest="extensions",
		default=".pg",
		help="Comma-separated list of file extensions (default: .pg).",
	)
	parser.add_argument(
		"-r",
		"--rules",
		dest="rules_file",
		help="Optional JSON file defining block and macro rules.",
	)
	parser.add_argument(
		"--fail-on-warn",
		dest="fail_on_warn",
		action="store_true",
		help="Exit non-zero if warnings are found.",
	)
	parser.set_defaults(fail_on_warn=False)
	return parser.parse_args()


#============================================


def load_rules(rules_file: str | None) -> tuple[list[dict[str, str]], list[dict[str, object]]]:
	"""
	Load block and macro rules from JSON or fall back to defaults.
	"""
	if rules_file is None:
		return DEFAULT_BLOCK_RULES, DEFAULT_MACRO_RULES
	with open(rules_file, "r", encoding="utf-8") as handle:
		data = json.load(handle)
	block_rules = data.get("block_rules", DEFAULT_BLOCK_RULES)
	macro_rules = data.get("macro_rules", DEFAULT_MACRO_RULES)
	return block_rules, macro_rules


#============================================


def normalize_extensions(extensions: str) -> list[str]:
	"""
	Normalize comma-separated extensions into a list.
	"""
	exts = [ext.strip() for ext in extensions.split(",") if ext.strip()]
	normalized: list[str] = []
	for ext in exts:
		if ext.startswith("."):
			normalized.append(ext.lower())
		else:
			normalized.append(f".{ext.lower()}")
	return normalized


#============================================


def find_files(input_dir: str, extensions: list[str]) -> list[str]:
	"""
	Find files under input_dir matching extensions.
	"""
	matches: list[str] = []
	for root, dirs, files in os.walk(input_dir):
		dirs.sort()
		files.sort()
		for filename in files:
			ext = os.path.splitext(filename)[1].lower()
			if ext in extensions:
				matches.append(os.path.join(root, filename))
	return sorted(matches)


#============================================


def extract_loaded_macros(text: str) -> set[str]:
	"""
	Extract macro filenames mentioned in the block.
	"""
	macro_pattern = re.compile(r"['\"]([A-Za-z0-9_]+\.pl)['\"]")
	macros = {macro.lower() for macro in macro_pattern.findall(text)}
	return macros


#============================================


def has_loadmacros(text: str) -> bool:
	"""
	Check whether the block includes a loadMacros call.
	"""
	return re.search(r"\bloadMacros\s*\(", text) is not None


#============================================


def check_block_pairs(text: str, block_rules: list[dict[str, str]]) -> list[dict[str, str]]:
	"""
	Check for balanced begin/end markers within a block.
	"""
	issues: list[dict[str, str]] = []
	for rule in block_rules:
		label = rule["label"]
		start_pattern = rule["start_pattern"]
		end_pattern = rule["end_pattern"]
		start_count = len(re.findall(start_pattern, text))
		end_count = len(re.findall(end_pattern, text))
		if start_count == end_count:
			continue
		if start_count == 0 or end_count == 0:
			issues.append(
				{
					"severity": "WARNING",
					"message": f"{label} appears only on one side (start={start_count}, end={end_count})",
				},
			)
			continue
		issues.append(
			{
				"severity": "ERROR",
				"message": f"{label} counts do not match (start={start_count}, end={end_count})",
			},
		)
	return issues


#============================================


def check_macro_rules(
	text: str,
	macros_loaded: set[str],
	macro_rules: list[dict[str, object]],
) -> list[dict[str, str]]:
	"""
	Check macro rules when macro coverage is expected.
	"""
	issues: list[dict[str, str]] = []
	for rule in macro_rules:
		label = str(rule["label"])
		pattern = str(rule["pattern"])
		required_macros = [macro.lower() for macro in rule["required_macros"]]
		if re.search(pattern, text) is None:
			continue
		if any(macro in macros_loaded for macro in required_macros):
			continue
		joined_macros = ", ".join(required_macros)
		issues.append(
			{
				"severity": "WARNING",
				"message": f"{label} used without required macros: {joined_macros}",
			},
		)
	return issues


#============================================


def extract_blank_variables(text: str) -> list[str]:
	"""
	Extract variable names referenced in PGML blanks.
	"""
	blank_pattern = re.compile(r"\[[^\]]*\]\s*\{\s*\$([A-Za-z_][A-Za-z0-9_]*)\s*\}")
	return blank_pattern.findall(text)


#============================================


def check_blank_assignments(text: str) -> list[dict[str, str]]:
	"""
	Warn when PGML blanks reference variables that are not assigned in the file.
	"""
	issues: list[dict[str, str]] = []
	variables = sorted(set(extract_blank_variables(text)))
	if not variables:
		return issues
	for name in variables:
		assign_pattern = re.compile(rf"\b(?:my|our)?\s*\${name}\b\s*=")
		if assign_pattern.search(text):
			continue
		issues.append(
			{
				"severity": "WARNING",
				"message": f"PGML blank references ${name} without assignment in file",
			},
		)
	return issues


#============================================


def validate_text(
	text: str,
	block_rules: list[dict[str, str]],
	macro_rules: list[dict[str, object]],
) -> list[dict[str, str]]:
	"""
	Validate text and return a list of issue dicts.
	"""
	issues: list[dict[str, str]] = []
	issues.extend(check_block_pairs(text, block_rules))

	macros_loaded = extract_loaded_macros(text)
	should_check_macros = has_loadmacros(text) or re.search(r"\bDOCUMENT\s*\(\s*\)", text)
	if should_check_macros is True:
		issues.extend(check_macro_rules(text, macros_loaded, macro_rules))
	issues.extend(check_blank_assignments(text))
	return issues


#============================================


def lint_text_to_result(text: str) -> dict:
	"""
	Lint PG text using default rules and return a structured result dict.

	Returns a dict with keys: status, issues, error_count, warn_count.
	This is the importable API for use by pipeline scripts.
	"""
	issues = validate_text(text, DEFAULT_BLOCK_RULES, DEFAULT_MACRO_RULES)
	error_count = len([i for i in issues if i["severity"] == "ERROR"])
	warn_count = len([i for i in issues if i["severity"] != "ERROR"])
	if error_count > 0:
		status = "error"
	elif warn_count > 0:
		status = "warn"
	else:
		status = "pass"
	result = {
		"status": status,
		"issues": issues,
		"error_count": error_count,
		"warn_count": warn_count,
	}
	return result


#============================================


def validate_file(
	file_path: str,
	block_rules: list[dict[str, str]],
	macro_rules: list[dict[str, object]],
) -> list[dict[str, str]]:
	"""
	Validate a single file and return a list of issue dicts.
	"""
	with open(file_path, "r", encoding="utf-8") as handle:
		text = handle.read()
	return validate_text(text, block_rules, macro_rules)


#============================================


def main() -> None:
	"""
	Run the lint checker.
	"""
	args = parse_args()
	block_rules, macro_rules = load_rules(args.rules_file)

	issues: list[dict[str, str]] = []
	if args.input_file:
		issues = validate_file(args.input_file, block_rules, macro_rules)
		for issue in issues:
			print(f"{args.input_file}: {issue['severity']}: {issue['message']}")
	else:
		extensions = normalize_extensions(args.extensions)
		files_to_check = find_files(args.input_dir, extensions)
		for file_path in files_to_check:
			file_issues = validate_file(file_path, block_rules, macro_rules)
			for issue in file_issues:
				print(f"{file_path}: {issue['severity']}: {issue['message']}")
			issues.extend(file_issues)

	error_count = len([issue for issue in issues if issue["severity"] == "ERROR"])
	warn_count = len([issue for issue in issues if issue["severity"] != "ERROR"])
	if issues:
		print(f"Found {error_count} errors and {warn_count} warnings.")

	if error_count > 0:
		sys.exit(1)
	if args.fail_on_warn and warn_count > 0:
		sys.exit(1)


if __name__ == "__main__":
	main()
