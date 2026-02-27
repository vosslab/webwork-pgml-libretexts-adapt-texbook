#!/usr/bin/env python3
"""Convert Textbook HTML pages to a single Markdown file via pandoc."""

# Standard Library
import re
import sys
import shutil
import pathlib
import argparse
import subprocess


#============================================
def parse_args() -> argparse.Namespace:
	"""Parse command line arguments."""
	parser = argparse.ArgumentParser(
		description="Build one merged Markdown file from Textbook HTML files.",
	)
	parser.add_argument(
		"-o", "--output", dest="output_md", type=str, default="",
		help="Output Markdown path. Default: ./<cwd_name>.md",
	)
	args = parser.parse_args()
	return args


#============================================
def get_repo_root() -> pathlib.Path:
	"""Resolve repository root by reusing tests/git_file_utils.py."""
	script_path = pathlib.Path(__file__).resolve()
	repo_root_from_script = script_path.parent.parent
	tests_dir = repo_root_from_script / "tests"
	sys.path.insert(0, str(tests_dir))
	import git_file_utils
	repo_root = pathlib.Path(git_file_utils.get_repo_root()).resolve()
	return repo_root


#============================================
def get_output_md_path(output_arg: str) -> pathlib.Path:
	"""Resolve output path with a default based on current directory name."""
	if output_arg:
		output_md = pathlib.Path(output_arg).resolve()
		return output_md
	cwd_path = pathlib.Path.cwd().resolve()
	default_name = f"{cwd_path.name}.md"
	output_md = cwd_path / default_name
	return output_md


#============================================
def extract_number_chunks(text: str) -> list[int]:
	"""Extract numeric chunks from text in left-to-right order."""
	chunks = re.findall(r"\d+", text)
	values = []
	for chunk in chunks:
		values.append(int(chunk))
	return values


#============================================
def html_sort_key(path: pathlib.Path) -> tuple:
	"""Build a stable chapter/section sort key for a textbook page path."""
	chapter_name = path.parent.name
	filename = path.name
	file_stem = path.stem
	section_prefix = file_stem.split("-", 1)[0]
	chapter_numbers = extract_number_chunks(chapter_name)
	section_numbers = extract_number_chunks(section_prefix)
	key = (chapter_numbers, section_numbers, filename)
	return key


#============================================
def find_html_files(input_root: pathlib.Path) -> list[pathlib.Path]:
	"""Collect and sort Textbook chapter HTML files."""
	pattern = "*/*.html"
	files = list(input_root.glob(pattern))
	sorted_files = sorted(files, key=html_sort_key)
	return sorted_files


#============================================
def convert_html_to_markdown(html_text: str) -> str:
	"""Convert an HTML string to Markdown via pandoc."""
	result = subprocess.run(
		["pandoc", "-f", "html", "-t", "markdown"],
		input=html_text,
		capture_output=True,
		text=True,
		check=True,
	)
	return result.stdout


#============================================
def build_section_label(source_path: pathlib.Path, input_root: pathlib.Path) -> str:
	"""Build a section label from the relative path (without .html extension)."""
	relative_path = source_path.relative_to(input_root)
	label = str(relative_path.with_suffix(""))
	return label


#============================================
def build_table_of_contents(html_files: list[pathlib.Path], input_root: pathlib.Path) -> str:
	"""Build a Markdown table of contents listing all sections."""
	lines = ["# Table of Contents", ""]
	for source_path in html_files:
		label = build_section_label(source_path, input_root)
		anchor = label.lower().replace("/", "").replace(".", "").replace("_", "-").replace(" ", "-")
		lines.append(f"- [{label}](#{anchor})")
	lines.append("")
	toc_text = "\n".join(lines)
	return toc_text


#============================================
def build_markdown(repo_root: pathlib.Path, output_md: pathlib.Path) -> pathlib.Path:
	"""Convert all Textbook HTML files to one merged Markdown file."""
	input_root = repo_root / "Textbook"

	if not input_root.exists():
		raise RuntimeError(f"Input root does not exist: {input_root}")

	if shutil.which("pandoc") is None:
		raise RuntimeError("Required tool not found on PATH: pandoc")

	html_files = find_html_files(input_root)
	if not html_files:
		raise RuntimeError(f"No HTML files found under: {input_root}")

	sections = []
	for index, source_html in enumerate(html_files, start=1):
		label = build_section_label(source_html, input_root)
		raw_html = source_html.read_text(encoding="utf-8")
		markdown_body = convert_html_to_markdown(raw_html)
		section = f"# {label}\n\n{markdown_body.strip()}\n"
		sections.append(section)
		print(f"[{index}/{len(html_files)}] converted {label}")

	toc = build_table_of_contents(html_files, input_root)
	separator = "\n---\n\n"
	full_markdown = toc + separator + separator.join(sections) + "\n"

	output_md.parent.mkdir(parents=True, exist_ok=True)
	output_md.write_text(full_markdown, encoding="utf-8")

	print(f"Markdown file: {output_md}")
	print(f"Sections converted: {len(sections)}")
	return output_md


#============================================
def main() -> None:
	"""Run the textbook Markdown build flow."""
	args = parse_args()
	repo_root = get_repo_root()
	output_md = get_output_md_path(args.output_md)
	build_markdown(repo_root, output_md)


if __name__ == "__main__":
	main()
