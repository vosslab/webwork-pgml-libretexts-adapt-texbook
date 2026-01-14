#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys

# PyPi
import lxml.html


def parse_args() -> argparse.Namespace:
	"""
	Parse command-line arguments.
	"""
	parser = argparse.ArgumentParser(
		description="Extract <pre> blocks from Textbook HTML into .pg files.",
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
		"--lint",
		dest="run_lint",
		action="store_true",
		help="Run webwork_simple_lint on the extracted files.",
	)
	parser.set_defaults(run_lint=False)
	return parser.parse_args()


#============================================


def find_html_files(input_dir: str) -> list[str]:
	"""
	Find HTML files under input_dir.
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


def parse_html_fragment(html_text: str, file_path: str) -> lxml.html.HtmlElement:
	"""
	Parse an HTML fragment and return a container element holding the parsed content.
	"""
	parser = lxml.html.HTMLParser(recover=False)
	container = lxml.html.Element("div")
	fragments = lxml.html.fragments_fromstring(html_text, parser=parser)
	for frag in fragments:
		if frag is None:
			continue
		if isinstance(frag, str):
			if container.text is None:
				container.text = frag
			else:
				container.text += frag
		else:
			container.append(frag)
	return container


#============================================


def sanitize_filename(value: str) -> str:
	"""
	Sanitize a filename component.
	"""
	allowed = []
	for char in value:
		if char.isalnum() or char in ("-", "_"):
			allowed.append(char)
		else:
			allowed.append("_")
	return "".join(allowed)


#============================================


def write_block(
	output_dir: str,
	rel_path: str,
	block_index: int,
	line: str | None,
	text: str,
) -> str:
	"""
	Write a single block to a .pg file.
	"""
	base_name = sanitize_filename(rel_path.replace(os.sep, "__"))
	filename = f"{base_name}__block_{block_index:02d}.pg"
	output_path = os.path.join(output_dir, filename)

	with open(output_path, "w", encoding="utf-8") as handle:
		handle.write(f"# Source: {rel_path}\n")
		handle.write(f"# Block: {block_index}\n")
		if line is not None:
			handle.write(f"# Line: {line}\n")
		handle.write("\n")
		handle.write(text.rstrip())
		handle.write("\n")
	return output_path


#============================================


def extract_blocks(input_dir: str, output_dir: str) -> list[str]:
	"""
	Extract <pre> blocks from HTML files and return written file paths.
	"""
	written_files: list[str] = []
	html_files = find_html_files(input_dir)
	os.makedirs(output_dir, exist_ok=True)
	for file_path in html_files:
		with open(file_path, "r", encoding="utf-8") as handle:
			html_text = handle.read()
		tree = parse_html_fragment(html_text, file_path)
		pre_blocks = tree.xpath(".//pre")
		if not pre_blocks:
			continue
		rel_path = os.path.relpath(file_path, start=input_dir)
		for index, pre in enumerate(pre_blocks, start=1):
			text = pre.text_content()
			line = getattr(pre, "sourceline", None)
			output_path = write_block(
				output_dir=output_dir,
				rel_path=rel_path,
				block_index=index,
				line=str(line) if line is not None else None,
				text=text,
			)
			written_files.append(output_path)
	return written_files


#============================================


def run_lint(output_dir: str) -> int:
	"""
	Run webwork_simple_lint on the extracted files.
	"""
	tools_dir = os.path.dirname(os.path.abspath(__file__))
	lint_script = os.path.join(tools_dir, "webwork_simple_lint.py")
	command = [sys.executable, lint_script, "-d", output_dir]
	result = subprocess.run(command, check=False)
	return result.returncode


#============================================


def main() -> None:
	"""
	Extract <pre> blocks and optionally lint them.
	"""
	args = parse_args()
	written_files = extract_blocks(args.input_dir, args.output_dir)
	print(f"Wrote {len(written_files)} extracted blocks to {args.output_dir}")
	if args.run_lint is True:
		sys.exit(run_lint(args.output_dir))


if __name__ == "__main__":
	main()
