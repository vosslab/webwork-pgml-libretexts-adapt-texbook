#!/usr/bin/env python3

import argparse
import json
import os
import re
import sys

# PyPi
import lxml.etree
import lxml.html


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
		description="Validate PG/PGML code blocks inside Textbook HTML files.",
	)
	parser.add_argument(
		"-i",
		"--input",
		dest="input_file",
		help="Path to a single HTML file to validate.",
	)
	parser.add_argument(
		"-d",
		"--directory",
		dest="input_dir",
		default="Textbook",
		help="Directory to scan for .html files (default: Textbook).",
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


def find_html_files(input_dir: str) -> list[str]:
	"""
	Find HTML files under input_dir.

	Args:
		input_dir (str): Root directory to scan.

	Returns:
		list[str]: Sorted list of file paths.
	"""
	html_files: list[str] = []
	for root, dirs, files in os.walk(input_dir):
		dirs.sort()
		files.sort()
		for filename in files:
			if filename.lower().endswith(".html"):
				html_files.append(os.path.join(root, filename))
	return sorted(html_files)


#============================================


def _append_fragment(container, fragment) -> None:
	"""
	Append a parsed HTML fragment to a container element.
	"""
	if fragment is None:
		return
	if isinstance(fragment, str):
		if container.text is None:
			container.text = fragment
		else:
			container.text += fragment
		return
	container.append(fragment)


#============================================


def parse_html_fragment(html_text: str, file_path: str) -> lxml.html.HtmlElement:
	"""
	Parse an HTML fragment and return a single container element holding the parsed content.
	"""
	parser = lxml.html.HTMLParser(recover=False)
	container = lxml.html.Element("div")
	fragments = lxml.html.fragments_fromstring(html_text, parser=parser)
	for frag in fragments:
		_append_fragment(container, frag)
	return container


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


def extract_pre_blocks(tree: lxml.html.HtmlElement) -> list[dict[str, object]]:
	"""
	Extract <pre> blocks with text and line metadata.
	"""
	blocks: list[dict[str, object]] = []
	for index, pre in enumerate(tree.xpath(".//pre"), start=1):
		text = pre.text_content()
		line = getattr(pre, "sourceline", None)
		blocks.append(
			{
				"index": index,
				"text": text,
				"line": line,
			},
		)
	return blocks


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


def has_document_markers(text: str) -> bool:
	"""
	Check whether the block includes DOCUMENT or ENDDOCUMENT markers.
	"""
	if re.search(r"\bDOCUMENT\s*\(\s*\)", text):
		return True
	if re.search(r"\bENDDOCUMENT\s*\(\s*\)", text):
		return True
	return False


#============================================


def has_pgml_markers(text: str) -> bool:
	"""
	Check whether the block includes PGML markers.
	"""
	if re.search(r"\bBEGIN_PGML\b", text):
		return True
	if re.search(r"\bEND_PGML\b", text):
		return True
	return False


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


def validate_block(
	block: dict[str, object],
	block_rules: list[dict[str, str]],
	macro_rules: list[dict[str, object]],
) -> list[dict[str, str]]:
	"""
	Validate a single <pre> block.
	"""
	text = str(block["text"])
	macros_loaded = extract_loaded_macros(text)

	issues: list[dict[str, str]] = []
	issues.extend(check_block_pairs(text, block_rules))

	should_check_macros = has_loadmacros(text) or has_document_markers(text) or has_pgml_markers(text)
	if should_check_macros is True:
		issues.extend(check_macro_rules(text, macros_loaded, macro_rules))
	return issues


#============================================


def validate_file(
	file_path: str,
	block_rules: list[dict[str, str]],
	macro_rules: list[dict[str, object]],
) -> list[dict[str, str]]:
	"""
	Validate a single HTML file and return a list of issue dicts.
	"""
	with open(file_path, "r", encoding="utf-8") as handle:
		html_text = handle.read()

	tree = parse_html_fragment(html_text, file_path)
	blocks = extract_pre_blocks(tree)

	issues: list[dict[str, str]] = []
	for block in blocks:
		block_issues = validate_block(block, block_rules, macro_rules)
		if not block_issues:
			continue
		line = block.get("line")
		line_text = str(line) if line is not None else "?"
		block_index = block["index"]
		for issue in block_issues:
			issues.append(
				{
					"severity": issue["severity"],
					"message": issue["message"],
					"file": file_path,
					"line": line_text,
					"block": str(block_index),
				},
			)
	return issues


#============================================


def main() -> None:
	"""
	Run the code block validator.
	"""
	args = parse_args()
	block_rules, macro_rules = load_rules(args.rules_file)

	if args.input_file:
		files_to_check = [args.input_file]
	else:
		files_to_check = find_html_files(args.input_dir)

	all_issues: list[dict[str, str]] = []
	for file_path in files_to_check:
		all_issues.extend(validate_file(file_path, block_rules, macro_rules))

	error_count = 0
	warn_count = 0
	for issue in all_issues:
		severity = issue["severity"]
		if severity == "ERROR":
			error_count += 1
		else:
			warn_count += 1
		print(
			f"{issue['file']}:{issue['line']}: BLOCK {issue['block']}: {severity}: {issue['message']}",
		)

	if all_issues:
		print(
			f"Found {error_count} errors and {warn_count} warnings across {len(files_to_check)} files.",
		)

	if error_count > 0:
		sys.exit(1)
	if args.fail_on_warn and warn_count > 0:
		sys.exit(1)


if __name__ == "__main__":
	main()
