"""
Tests for TEXTBOOK_PAGE_SUMMARIES.md content quality.

Enforces:
- Description text for each entry must be <= 500 characters.
- No "Chapter N" or "Chapter N.N" references in any entry.
"""

import os
import re

import pytest

from git_file_utils import get_repo_root


REPO_ROOT = get_repo_root()
SUMMARIES_PATH = os.path.join(REPO_ROOT, "Textbook", "TEXTBOOK_PAGE_SUMMARIES.md")

# Pattern for entry lines: - `Textbook/...html`: description text
ENTRY_PATTERN = re.compile(r"^- `(Textbook/[^`]+)`:\s*(.+)")

# Pattern for chapter references like "Chapter 2", "Chapter 2.4", "Chapter 10"
CHAPTER_REF_PATTERN = re.compile(r"\bChapter\s+\d+(\.\d+)?\b")

MAX_DESCRIPTION_LENGTH = 500


#============================================
def _parse_entries():
	"""
	Parse TEXTBOOK_PAGE_SUMMARIES.md and return a list of (path, description) tuples.

	Returns:
		list[tuple[str, str]]: Each tuple contains the file path and its
			description text (everything after ']: ' up to the SEO tags line).
	"""
	with open(SUMMARIES_PATH, "r", encoding="utf-8") as handle:
		lines = handle.readlines()

	entries = []
	i = 0
	while i < len(lines):
		match = ENTRY_PATTERN.match(lines[i])
		if match:
			file_path = match.group(1)
			description = match.group(2).strip()
			entries.append((file_path, description))
		i += 1
	return entries


#============================================
def _get_entry_ids():
	"""
	Return test IDs for parametrize.

	Returns:
		list[str]: Short identifiers derived from the HTML file names.
	"""
	entries = _parse_entries()
	ids = []
	for file_path, _ in entries:
		short = os.path.basename(file_path).replace(".html", "")
		ids.append(short)
	return ids


#============================================
# Collect entries once at module level for parametrize
#============================================
_ENTRIES = _parse_entries()
_IDS = [os.path.basename(fp).replace(".html", "") for fp, _ in _ENTRIES]


#============================================
@pytest.mark.parametrize("file_path,description", _ENTRIES, ids=_IDS)
def test_description_length(file_path, description):
	"""Each entry description must be <= 500 characters."""
	length = len(description)
	assert length <= MAX_DESCRIPTION_LENGTH, (
		f"{file_path}: description is {length} chars "
		f"({length - MAX_DESCRIPTION_LENGTH} over limit of {MAX_DESCRIPTION_LENGTH})"
	)


#============================================
@pytest.mark.parametrize("file_path,description", _ENTRIES, ids=_IDS)
def test_no_chapter_references(file_path, description):
	"""No entry should contain 'Chapter N' or 'Chapter N.N' references."""
	matches = CHAPTER_REF_PATTERN.findall(description)
	full_matches = CHAPTER_REF_PATTERN.finditer(description)
	found = [m.group() for m in full_matches]
	assert not found, (
		f"{file_path}: contains chapter reference(s): {found}"
	)
