#!/usr/bin/env python3

import argparse
import os
import sys

# PyPi
import lxml.etree
import lxml.html


def parse_args() -> argparse.Namespace:
	"""
	Parse command-line arguments.
	"""
	parser = argparse.ArgumentParser(
		description="Lint Textbook HTML fragments for LibreTexts compatibility.",
	)
	parser.add_argument(
		"-i",
		"--input",
		dest="input_file",
		help="Path to a single HTML file to lint.",
	)
	parser.add_argument(
		"-d",
		"--directory",
		dest="input_dir",
		default="Textbook",
		help="Directory to scan for .html files (default: Textbook).",
	)
	parser.add_argument(
		"--allow-links",
		dest="allow_links",
		action="store_true",
		help="Allow all <a href='...'> links, including relative file links.",
	)
	parser.add_argument(
		"--allow-iframe",
		dest="allow_iframe",
		action="store_true",
		help="Allow <iframe> tags (default: disallow).",
	)
	parser.set_defaults(allow_links=False, allow_iframe=False)
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
	try:
		fragments = lxml.html.fragments_fromstring(html_text, parser=parser)
	except (lxml.etree.ParserError, lxml.etree.XMLSyntaxError) as err:
		raise ValueError(f"{file_path}: parse error: {err}") from err
	for frag in fragments:
		_append_fragment(container, frag)
	return container


#============================================


def lint_tree(
	tree: lxml.html.HtmlElement,
	file_path: str,
	allow_links: bool,
	allow_iframe: bool,
) -> list[str]:
	"""
	Lint a parsed HTML tree and return a list of error strings.
	"""
	errors: list[str] = []

	for element in tree.iter():
		tag = element.tag.lower() if isinstance(element.tag, str) else ""
		line = getattr(element, "sourceline", None)
		line_text = str(line) if line is not None else "?"

		if tag == "script":
			errors.append(f"{file_path}:{line_text}: ERROR: <script> tags are not allowed")

		if (tag == "iframe") and (allow_iframe is False):
			errors.append(f"{file_path}:{line_text}: ERROR: <iframe> tags are not allowed")

		for attr_name, attr_value in element.attrib.items():
			attr_lower = attr_name.lower()
			if attr_lower.startswith("on"):
				errors.append(
					f"{file_path}:{line_text}: ERROR: event handler attribute '{attr_name}' is not allowed",
				)
			if isinstance(attr_value, str):
				val = attr_value.strip().lower()
				if val.startswith("javascript:"):
					errors.append(
						f"{file_path}:{line_text}: ERROR: javascript: URLs are not allowed",
					)

	for a_tag in tree.xpath(".//a"):
		line = getattr(a_tag, "sourceline", None)
		line_text = str(line) if line is not None else "?"
		href = (a_tag.get("href") or "").strip()
		if href == "":
			continue
		if allow_links is True:
			continue
		href_lower = href.lower()
		if (
			href_lower.startswith("http://")
			or href_lower.startswith("https://")
			or href_lower.startswith("/")
			or href_lower.startswith("#")
			or href_lower.startswith("mailto:")
			or href_lower.startswith("tel:")
		):
			continue
		errors.append(
			f"{file_path}:{line_text}: ERROR: relative file links are not allowed (<a href='{href}'>)",
		)

	return errors


#============================================


def lint_file(file_path: str, allow_links: bool, allow_iframe: bool) -> list[str]:
	"""
	Lint a single HTML file.
	"""
	if os.path.getsize(file_path) == 0:
		return [f"{file_path}:1: ERROR: file is empty"]

	with open(file_path, "r", encoding="utf-8") as handle:
		html_text = handle.read()

	tree = parse_html_fragment(html_text, file_path)
	return lint_tree(tree, file_path, allow_links=allow_links, allow_iframe=allow_iframe)


#============================================


def main() -> None:
	"""
	Run the HTML lint checker.
	"""
	args = parse_args()

	files_to_check: list[str] = []
	if args.input_file:
		files_to_check = [args.input_file]
	else:
		files_to_check = find_html_files(args.input_dir)

	if len(files_to_check) == 0:
		print("No HTML files found to lint.")
		sys.exit(0)

	all_errors: list[str] = []
	for file_path in files_to_check:
		all_errors.extend(
			lint_file(
				file_path,
				allow_links=args.allow_links,
				allow_iframe=args.allow_iframe,
			),
		)

	if len(all_errors) > 0:
		print("HTML lint errors")
		for err in all_errors:
			print(err)
		print(f"Found {len(all_errors)} errors")
		sys.exit(1)

	print(f"OK: linted {len(files_to_check)} HTML files")
	sys.exit(0)


if __name__ == "__main__":
	main()
