#!/usr/bin/env python3
"""Render Textbook HTML pages to PDFs and merge them into one PDF."""

# Standard Library
import sys
import re
import html
import shutil
import pathlib
import tempfile
import argparse
import subprocess
import urllib.parse

# PIP3 modules
import weasyprint
import pygments
import pygments.lexers
import pygments.formatters


ANCHOR_TAG_RE = re.compile(r"<a\b[^>]*>", re.IGNORECASE)
HREF_ATTR_RE = re.compile(r"\s+href\s*=\s*([\"'])([^\"']*)(\1)", re.IGNORECASE)
HEAD_OPEN_RE = re.compile(r"<head[^>]*>", re.IGNORECASE)
HEAD_CLOSE_RE = re.compile(r"</head>", re.IGNORECASE)
BODY_OPEN_RE = re.compile(r"<body[^>]*>", re.IGNORECASE)
PRE_BLOCK_RE = re.compile(r"<pre\b([^>]*)>(.*?)</pre>", re.IGNORECASE | re.DOTALL)
CODE_WRAPPER_RE = re.compile(r"^\s*<code\b[^>]*>(.*?)</code>\s*$", re.IGNORECASE | re.DOTALL)
RELATIVE_LINK_MODE = "strip"
DEFAULT_BODY_STYLE = (
	"html { font-size: 12pt !important; } "
	"body, p, li, td, th, dd, dt, blockquote { "
	"font-family: 'Times New Roman', Times, serif !important; "
	"font-size: 12pt !important; "
	"line-height: 1.3 !important; "
	"}"
)
DEFAULT_HEADING_STYLE = (
	"h1, h2, h3, h4, h5, h6 { "
	"font-family: 'Times New Roman', Times, serif !important; "
	"line-height: 1.2 !important; "
	"margin-top: 0.8em !important; "
	"margin-bottom: 0.2em !important; "
	"} "
	"h1 { font-size: 1.65em !important; } "
	"h2 { font-size: 1.45em !important; } "
	"h3 { font-size: 1.30em !important; } "
	"h4 { font-size: 1.18em !important; } "
	"h5 { font-size: 1.08em !important; } "
	"h6 { font-size: 1.00em !important; } "
	"h1 + p, h2 + p, h3 + p, h4 + p, h5 + p, h6 + p { "
	"margin-top: 0.2em !important; "
	"}"
)
DEFAULT_CODE_STYLE = (
	"pre, code, pre code, code.codehilite, pre code.codehilite, "
	"pre *, code *, pre code *, code.codehilite * { "
	"font-family: 'Courier New', Courier, 'Liberation Mono', monospace !important; "
	"font-size: 11pt !important; "
	"line-height: 1.25 !important; "
	"} "
	"pre { "
	"background: #f7f7f7; "
	"border: 1px solid #d9d9d9; "
	"padding: 0.6em; "
	"white-space: pre-wrap; "
	"}"
)
PYGMENTS_FORMATTER = pygments.formatters.HtmlFormatter(nowrap=True, style="default")
PYGMENTS_CSS = PYGMENTS_FORMATTER.get_style_defs(".codehilite")
PERL_LEXER = pygments.lexers.PerlLexer()


#============================================
def parse_args() -> argparse.Namespace:
	"""Parse command line arguments."""
	parser = argparse.ArgumentParser(
		description="Build one merged textbook PDF from Textbook HTML files.",
	)
	parser.add_argument(
		"-o", "--output", dest="output_pdf", type=str, default="",
		help="Merged output PDF path. Default: ./<cwd_name>.pdf",
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
def get_output_pdf_path(output_arg: str) -> pathlib.Path:
	"""Resolve output path with a default based on current directory name."""
	if output_arg:
		output_pdf = pathlib.Path(output_arg).resolve()
		return output_pdf
	cwd_path = pathlib.Path.cwd().resolve()
	default_name = f"{cwd_path.name}.pdf"
	output_pdf = cwd_path / default_name
	return output_pdf


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
def is_relative_href(href: str) -> bool:
	"""Return True when href looks like a relative URL."""
	if not href:
		return False
	lower_href = href.lower()
	if lower_href.startswith("#"):
		return False
	if lower_href.startswith("/"):
		return False
	if lower_href.startswith("http://"):
		return False
	if lower_href.startswith("https://"):
		return False
	if lower_href.startswith("mailto:"):
		return False
	if lower_href.startswith("tel:"):
		return False
	if lower_href.startswith("file:"):
		return False
	if lower_href.startswith("data:"):
		return False
	return True


#============================================
def resolve_relative_href(source_path: pathlib.Path, href: str) -> str:
	"""Resolve a relative href to an absolute file URI."""
	parts = urllib.parse.urlsplit(href)
	decoded_path = urllib.parse.unquote(parts.path)
	target_path = (source_path.parent / decoded_path).resolve()
	target_uri = target_path.as_uri()
	if parts.query:
		target_uri += f"?{parts.query}"
	if parts.fragment:
		target_uri += f"#{parts.fragment}"
	return target_uri


#============================================
def rewrite_anchor_tag(tag: str, source_path: pathlib.Path, relative_links: str) -> str:
	"""Rewrite one opening anchor tag based on relative link handling mode."""
	href_match = HREF_ATTR_RE.search(tag)
	if href_match is None:
		return tag
	href_value = href_match.group(2)
	if not is_relative_href(href_value):
		return tag
	if relative_links == "strip":
		replaced = tag[:href_match.start()] + tag[href_match.end():]
		return replaced
	absolute_href = resolve_relative_href(source_path, href_value)
	replaced = tag[:href_match.start(2)] + absolute_href + tag[href_match.end(2):]
	return replaced


#============================================
def rewrite_relative_links(html_text: str, source_path: pathlib.Path, relative_links: str) -> str:
	"""Rewrite relative anchor href values in an HTML document."""
	def replace_tag(match: re.Match) -> str:
		tag_text = match.group(0)
		updated_tag = rewrite_anchor_tag(tag_text, source_path, relative_links)
		return updated_tag

	rewritten_html = ANCHOR_TAG_RE.sub(replace_tag, html_text)
	return rewritten_html


#============================================
def insert_base_tag(html_text: str, source_path: pathlib.Path) -> str:
	"""Insert a base tag so local assets resolve from the original HTML location."""
	source_dir_uri = source_path.parent.resolve().as_uri()
	if not source_dir_uri.endswith("/"):
		source_dir_uri += "/"
	base_tag = f"<base href=\"{source_dir_uri}\">"
	head_match = HEAD_OPEN_RE.search(html_text)
	if head_match is None:
		prefixed = f"<head>{base_tag}</head>\n{html_text}"
		return prefixed
	insert_at = head_match.end()
	updated = html_text[:insert_at] + base_tag + html_text[insert_at:]
	return updated


#============================================
def insert_default_style(html_text: str) -> str:
	"""Insert default CSS to normalize body text size in rendered PDF."""
	style_text = DEFAULT_BODY_STYLE + DEFAULT_HEADING_STYLE + DEFAULT_CODE_STYLE + PYGMENTS_CSS
	style_tag = f"<style>{style_text}</style>"
	head_close_match = HEAD_CLOSE_RE.search(html_text)
	if head_close_match is not None:
		insert_at = head_close_match.start()
		updated = html_text[:insert_at] + style_tag + html_text[insert_at:]
		return updated

	head_open_match = HEAD_OPEN_RE.search(html_text)
	if head_open_match is None:
		prefixed = f"<head>{style_tag}</head>\n{html_text}"
		return prefixed
	insert_at = head_open_match.end()
	updated = html_text[:insert_at] + style_tag + html_text[insert_at:]
	return updated


#============================================
def strip_html_tags(text: str) -> str:
	"""Remove HTML tags from a string."""
	no_tags = re.sub(r"<[^>]+>", "", text)
	return no_tags


#============================================
def extract_pre_code_text(pre_inner_html: str) -> str:
	"""Extract plain code text from pre block HTML."""
	code_match = CODE_WRAPPER_RE.match(pre_inner_html)
	if code_match is not None:
		code_html = code_match.group(1)
	else:
		code_html = pre_inner_html
	code_text = strip_html_tags(code_html)
	unescaped_text = html.unescape(code_text)
	return unescaped_text


#============================================
def highlight_pre_blocks(html_text: str) -> str:
	"""Apply syntax highlighting to pre blocks in temporary HTML."""
	def replace_pre(match: re.Match) -> str:
		attrs = match.group(1)
		inner_html = match.group(2)
		code_text = extract_pre_code_text(inner_html)
		highlighted = pygments.highlight(code_text, PERL_LEXER, PYGMENTS_FORMATTER)
		rewritten = f"<pre{attrs}><code class=\"codehilite\">{highlighted}</code></pre>"
		return rewritten

	highlighted_html = PRE_BLOCK_RE.sub(replace_pre, html_text)
	return highlighted_html


#============================================
def insert_page_header(
		html_text: str,
		source_path: pathlib.Path,
		input_root: pathlib.Path,
) -> str:
	"""Insert a visible source-page header at the top of the HTML body."""
	relative_path = source_path.relative_to(input_root)
	page_label = str(relative_path)
	header_html = (
		"<div style='font-family: monospace; font-size: 12pt; "
		"font-weight: bold; border-bottom: 1px solid #888; "
		"padding-bottom: 6px; margin-bottom: 12px;'>"
		f"{page_label}</div>"
	)
	body_match = BODY_OPEN_RE.search(html_text)
	if body_match is None:
		prefixed = f"<body>{header_html}</body>\n{html_text}"
		return prefixed
	insert_at = body_match.end()
	updated = html_text[:insert_at] + header_html + html_text[insert_at:]
	return updated


#============================================
def write_temp_html(
		source_path: pathlib.Path,
		temp_html_path: pathlib.Path,
		input_root: pathlib.Path,
) -> None:
	"""Create one temporary HTML file with link handling adjustments."""
	raw_html = source_path.read_text(encoding="utf-8")
	with_base = insert_base_tag(raw_html, source_path)
	with_style = insert_default_style(with_base)
	with_highlight = highlight_pre_blocks(with_style)
	with_header = insert_page_header(with_highlight, source_path, input_root)
	rewritten = rewrite_relative_links(with_header, source_path, RELATIVE_LINK_MODE)
	temp_html_path.parent.mkdir(parents=True, exist_ok=True)
	temp_html_path.write_text(rewritten, encoding="utf-8")


#============================================
def merge_pdfs(pdf_paths: list[pathlib.Path], output_pdf: pathlib.Path) -> None:
	"""Merge page PDFs into a single PDF with cpdf."""
	output_pdf.parent.mkdir(parents=True, exist_ok=True)
	command = ["cpdf"]
	for path in pdf_paths:
		command.append(str(path))
	command.extend(["-o", str(output_pdf)])
	subprocess.run(command, check=True)


#============================================
def run_weasyprint(html_path: pathlib.Path, pdf_path: pathlib.Path) -> None:
	"""Render one HTML file to one PDF file with WeasyPrint."""
	pdf_path.parent.mkdir(parents=True, exist_ok=True)
	html = weasyprint.HTML(
		filename=str(html_path),
		base_url=str(html_path.parent),
	)
	html.write_pdf(str(pdf_path))


#============================================
def build_book(repo_root: pathlib.Path, output_pdf: pathlib.Path) -> pathlib.Path:
	"""Build per-page PDFs and merge to a single textbook PDF."""
	input_root = repo_root / "Textbook"

	if not input_root.exists():
		raise RuntimeError(f"Input root does not exist: {input_root}")

	if shutil.which("cpdf") is None:
		raise RuntimeError("Required tool not found on PATH: cpdf")

	html_files = find_html_files(input_root)
	if not html_files:
		raise RuntimeError(f"No HTML files found under: {input_root}")

	with tempfile.TemporaryDirectory(prefix="textbook_pdf_build_") as temp_dir:
		temp_root = pathlib.Path(temp_dir)
		temp_html_root = temp_root / "html"
		temp_pdf_root = temp_root / "pdf"
		manifest_path = temp_root / "rendered_pages.txt"

		pdf_paths = []
		manifest_lines = []
		for index, source_html in enumerate(html_files, start=1):
			relative_path = source_html.relative_to(input_root)
			temp_html_path = temp_html_root / relative_path
			temp_pdf_path = temp_pdf_root / relative_path.with_suffix(".pdf")
			write_temp_html(source_html, temp_html_path, input_root)
			run_weasyprint(temp_html_path, temp_pdf_path)
			pdf_paths.append(temp_pdf_path)
			manifest_lines.append(str(relative_path))
			print(f"[{index}/{len(html_files)}] rendered {relative_path}")

		manifest_path.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")
		merge_pdfs(pdf_paths, output_pdf)

	print(f"Merged PDF: {output_pdf}")
	print(f"Pages rendered: {len(pdf_paths)}")
	return output_pdf


#============================================
def main() -> None:
	"""Run the textbook PDF build flow."""
	args = parse_args()
	repo_root = get_repo_root()
	output_pdf = get_output_pdf_path(args.output_pdf)
	build_book(repo_root, output_pdf)


if __name__ == "__main__":
	main()
