#!/usr/bin/env python3

import argparse
import csv
import json
import re
from pathlib import Path


SECTION_PREFIX_RE = re.compile(r"^\s*(\d+(?:\.\d+)*)\s*:\s*(.+?)\s*$")


def parse_args() -> argparse.Namespace:
	"""
	Parse command-line arguments.
	"""
	parser = argparse.ArgumentParser(
		description="Parse a LibreTexts Remixer map JSON and write a label -> page_id CSV mapping.",
	)
	parser.add_argument(
		"-i",
		"--input",
		dest="input_file",
		default="Textbook/Using_WeBWork_in_ADAPT-Map.json",
		help="Path to a LibreTexts map JSON file.",
	)
	parser.add_argument(
		"-o",
		"--output",
		dest="output_file",
		help="Output CSV path (default: same as input, with .csv extension).",
	)
	return parser.parse_args()


#============================================


def parse_section_label(title: str) -> tuple[str, str]:
	"""
	Return (section_number, section_title) if title starts with 'X.Y: ...'.
	Otherwise return ("", title).
	"""
	match = SECTION_PREFIX_RE.match(title or "")
	if not match:
		return "", (title or "").strip()
	section_number = match.group(1)
	section_title = match.group(2).strip()
	section_title = section_title.lstrip("_").strip()
	return section_number, section_title


#============================================


def walk_node(node: object, rows: list[dict[str, str]], parent_title: str = "") -> None:
	"""
	Walk a RemixTree node recursively and append mapping rows.
	"""
	if not isinstance(node, dict):
		return

	title = (node.get("title") or "").strip()
	data = node.get("data") if isinstance(node.get("data"), dict) else {}
	page_id = data.get("id")
	parent_id = data.get("parentID")
	parent_id_text = str(parent_id or "")
	if parent_id_text == "0":
		parent_id_text = ""

	if title and (page_id is not None):
		section_number, section_title = parse_section_label(title)
		rows.append(
			{
				"page_id": str(page_id),
				"section_number": section_number,
				"section_title": section_title,
				"label": title,
				"url": str(data.get("url") or ""),
				"relativePath": str(data.get("relativePath") or ""),
				"padded": str(data.get("padded") or ""),
				"parentID": parent_id_text,
				"parent_title": parent_title.strip(),
			},
		)

	children = node.get("children") or []
	if isinstance(children, list):
		for child in children:
			walk_node(child, rows, parent_title=title)


#============================================


def main() -> None:
	"""
	Load a LibreTexts map JSON and write a CSV mapping.
	"""
	args = parse_args()

	input_path = Path(args.input_file)
	if args.output_file:
		output_path = Path(args.output_file)
	else:
		output_path = input_path.with_suffix(".csv")

	with input_path.open("r", encoding="utf-8") as handle:
		root = json.load(handle)

	tree = root.get("RemixTree", root)

	rows: list[dict[str, str]] = []
	walk_node(tree, rows)

	fieldnames = [
		"page_id",
		"section_number",
		"section_title",
		"label",
		"url",
		"relativePath",
		"padded",
		"parentID",
		"parent_title",
	]

	with output_path.open("w", newline="", encoding="utf-8") as handle:
		writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
		writer.writeheader()
		for row in rows:
			writer.writerow(row)

	print(f"Wrote {len(rows)} rows to {output_path}")


if __name__ == "__main__":
	main()
