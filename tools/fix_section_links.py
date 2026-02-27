#!/usr/bin/env python3

"""Replace section/chapter number link text with titles in textbook HTML files.

Reads the CSV mapping of pageID -> section_title from the reremix CSV and
replaces link text that contains section/chapter numbers with the actual
section titles. Also removes redundant parenthetical section references
after links.

Usage:
    python3 tools/fix_section_links.py            # dry-run (default)
    python3 tools/fix_section_links.py --apply     # write changes to files
"""

import argparse
import csv
import glob
import os
import re
import sys

# ============================================================
# PageID -> title mapping from CSV + overrides
# ============================================================

# Title overrides: shorter or corrected link text for specific pages.
# These take precedence over the CSV section_title column.
TITLE_OVERRIDES = {
	"488657": "PG Problem Files",
	"488661": "Breaking Down the Components",
	"488662": "Different Question Types",
	"555187": "Quickstart: Edit Your First Problem",
	"555726": "Randomized MC True and False Statements",
	"555727": "Advanced Randomization Techniques",
	"557407": "Simple Syntax Checking (Linting)",
	"557409": "Scripting and Automation",
}


def load_page_titles(repo_root):
	"""Load page_id -> title mapping from the reremix CSV file."""
	csv_path = os.path.join(
		repo_root, "Textbook", "The_ADAPT_WeBWorK_Handbook.reremix.csv"
	)
	if not os.path.exists(csv_path):
		print(f"ERROR: CSV not found: {csv_path}", file=sys.stderr)
		sys.exit(1)

	titles = {}
	with open(csv_path, encoding="utf-8") as f:
		for row in csv.DictReader(f):
			page_id = row["page_id"]
			title = row["section_title"].replace("_", " ")
			if title and page_id:
				titles[page_id] = title

	# Apply overrides (shorter/corrected titles for link text)
	titles.update(TITLE_OVERRIDES)
	return titles


# Number pattern: matches "1", "1.2", "1.23", etc.
NUM = r"\d+(?:\.\d+)?"


def strip_pre_blocks(html):
	"""Return list of (start, end) char ranges that are inside <pre> blocks."""
	ranges = []
	for m in re.finditer(r"<pre[\s>].*?</pre>", html, re.DOTALL | re.IGNORECASE):
		ranges.append((m.start(), m.end()))
	return ranges


def in_pre_block(pos, pre_ranges):
	"""Check whether character position pos falls inside any <pre> block."""
	for start, end in pre_ranges:
		if start <= pos < end:
			return True
	return False


def fix_link_text(html, pre_ranges, page_titles):
	"""Replace section/chapter number link text with titles.

	Patterns handled:
	  A: <a href="/@go/page/{id}">Section X.Y</a>
	  B: <a href="/@go/page/{id}">Chapter X</a>
	  C: <a href="/@go/page/{id}">Chapter X.Y</a>
	  D: <a href="/@go/page/{id}">X.Y</a>  (bare number)
	  E: <a href="/@go/page/{id}">X.Y Title</a>  (number + title)
	"""
	changes = []

	# Combined pattern: anchor with /@go/page/{id} href and text starting with
	# Section/Chapter/number
	pattern = re.compile(
		r'(<a\s+href="/@go/page/(\d+)"[^>]*>)'  # group 1=open tag, group 2=pageID
		r"((?:Section|Chapter)\s+" + NUM + r"|" + NUM + r"(?:\s+\S.*?)?)"  # group 3=link text
		r"(</a>)",  # group 4=close tag
		re.IGNORECASE,
	)

	def replacer(m):
		if in_pre_block(m.start(), pre_ranges):
			return m.group(0)
		page_id = m.group(2)
		old_text = m.group(3)
		title = page_titles.get(page_id)
		if title is None:
			return m.group(0)
		# Skip if the link text already equals the title
		if old_text.strip() == title:
			return m.group(0)
		# Check: is the link text a section/chapter ref or bare number?
		is_section_ref = re.match(
			r"(?:Section|Chapter)\s+" + NUM + r"$", old_text, re.IGNORECASE
		)
		is_bare_number = re.match(NUM + r"$", old_text)
		is_number_plus_title = re.match(NUM + r"\s+", old_text)
		if is_section_ref or is_bare_number or is_number_plus_title:
			changes.append((page_id, old_text, title))
			return m.group(1) + title + m.group(4)
		return m.group(0)

	new_html = pattern.sub(replacer, html)
	return new_html, changes


def fix_parenthetical_refs(html, pre_ranges):
	"""Remove redundant parenthetical section/chapter refs after links.

	Patterns:
	  </a> (Section X.Y)  ->  </a>
	  </a> (Chapter X)    ->  </a>
	  </a> (Chapter X.Y)  ->  </a>
	"""
	changes = []
	pattern = re.compile(
		r"(</a>)\s*\((?:Section|Chapter)\s+" + NUM + r"\)",
		re.IGNORECASE,
	)

	def replacer(m):
		if in_pre_block(m.start(), pre_ranges):
			return m.group(0)
		changes.append(m.group(0))
		return m.group(1)

	new_html = pattern.sub(replacer, html)
	return new_html, changes


def process_file(filepath, page_titles, apply=False):
	"""Process a single HTML file, return summary of changes."""
	with open(filepath, "r", encoding="utf-8") as f:
		original = f.read()

	pre_ranges = strip_pre_blocks(original)

	html, link_changes = fix_link_text(original, pre_ranges, page_titles)
	# Recompute pre ranges after link text changes (positions may shift)
	pre_ranges = strip_pre_blocks(html)
	html, paren_changes = fix_parenthetical_refs(html, pre_ranges)

	if not link_changes and not paren_changes:
		return None

	result = {
		"file": filepath,
		"link_changes": link_changes,
		"paren_changes": paren_changes,
	}

	if apply and html != original:
		with open(filepath, "w", encoding="utf-8") as f:
			f.write(html)

	return result


def main():
	parser = argparse.ArgumentParser(
		description="Replace section/chapter numbers with titles in link text"
	)
	parser.add_argument(
		"--apply",
		action="store_true",
		help="Write changes to files (default is dry-run)",
	)
	args = parser.parse_args()

	repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	textbook_dir = os.path.join(repo_root, "Textbook")

	page_titles = load_page_titles(repo_root)

	html_files = sorted(glob.glob(os.path.join(textbook_dir, "**", "*.html"), recursive=True))

	if not html_files:
		print("ERROR: No HTML files found in Textbook/", file=sys.stderr)
		sys.exit(1)

	mode = "APPLYING" if args.apply else "DRY-RUN"
	print(f"=== {mode} mode === ({len(html_files)} files, {len(page_titles)} page titles)")
	print()

	total_link = 0
	total_paren = 0

	for filepath in html_files:
		result = process_file(filepath, page_titles, apply=args.apply)
		if result is None:
			continue

		rel_path = os.path.relpath(filepath, repo_root)
		print(f"  {rel_path}:")

		for page_id, old_text, new_title in result["link_changes"]:
			print(f"    LINK: [{old_text}] -> [{new_title}] (page {page_id})")
			total_link += 1

		for old_match in result["paren_changes"]:
			print(f"    PAREN: removed '{old_match.strip()}'")
			total_paren += 1

		print()

	print(f"Total: {total_link} link text replacements, {total_paren} parenthetical removals")
	if not args.apply:
		print("(dry-run — use --apply to write changes)")


if __name__ == "__main__":
	main()
