#!/usr/bin/env python3
"""
Extract all links from an HTML file and write a sorted, unique list.

Defaults:
- If -o/--output is not provided, write to <input_root>_links.txt next to the input file.
- Output appends by default.

Usage:
	python3 extract_url_links_from_html_file.py -i file.html
	python3 extract_url_links_from_html_file.py -i file.html -o file_links.txt
	python3 extract_url_links_from_html_file.py -i file.html --no-append
"""

import argparse
import html.parser
from pathlib import Path
from urllib.parse import urldefrag


#============================================

class LinkExtractor(html.parser.HTMLParser):
	"""HTML parser that collects href and src links."""

	def __init__(self) -> None:
		super().__init__()
		self.links: list[str] = []

	def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
		attr_map: dict[str, str] = {}
		for key, value in attrs:
			if value is None:
				continue
			attr_map[key.lower()] = value

		for key in ("href", "src"):
			if key in attr_map:
				self.links.append(attr_map[key])


#============================================

def parse_args() -> argparse.Namespace:
	"""Parse command-line arguments."""
	parser = argparse.ArgumentParser(description="Extract and sort all links from an HTML file.")

	parser.add_argument(
		"-i",
		"--input",
		dest="input_file",
		required=True,
		help="Input HTML file",
	)

	parser.add_argument(
		"-o",
		"--output",
		dest="output_file",
		default="",
		help="Output text file (defaults to <input_root>_links.txt)",
	)

	parser.add_argument(
		"-a",
		"--append",
		dest="append",
		action="store_true",
		help="Append to output file (default)",
	)

	parser.add_argument(
		"--no-append",
		dest="append",
		action="store_false",
		help="Overwrite output file",
	)
	parser.set_defaults(append=True)

	return parser.parse_args()


#============================================

def default_output_path(input_file: str) -> str:
	"""Return default output path <input_root>_links.txt next to the input file."""
	in_path = Path(input_file)
	return str(in_path.with_name(in_path.stem + "_links.txt"))


#============================================

def normalize_link(raw_link: str) -> str:
	"""Normalize a link by stripping whitespace and removing fragments."""
	link = raw_link.strip()
	if not link:
		return ""

	link, _frag = urldefrag(link)
	link = link.strip()
	return link


#============================================

def extract_all_links(html_text: str) -> list[str]:
	"""Extract all href and src attribute values from HTML."""
	parser = LinkExtractor()
	parser.feed(html_text)

	seen: set[str] = set()
	out: list[str] = []

	for raw in parser.links:
		link = normalize_link(raw)
		if not link:
			continue
		if link in seen:
			continue
		seen.add(link)
		out.append(link)

	out.sort()
	return out


#============================================

def write_links(output_file: str, links: list[str], append: bool) -> None:
	"""Write links to the output file."""
	mode = "a" if append else "w"

	out_text = ""
	for link in links:
		out_text += link + "\n"

	Path(output_file).open(mode, encoding="utf-8").write(out_text)


#============================================

def main() -> None:
	"""Program entry point."""
	args = parse_args()

	output_file = args.output_file
	if not output_file:
		output_file = default_output_path(args.input_file)

	html_text = Path(args.input_file).read_text(encoding="utf-8", errors="replace")
	links = extract_all_links(html_text)

	write_links(output_file, links, args.append)
	print(f"Wrote {len(links)} links to {output_file}")


if __name__ == "__main__":
	main()
