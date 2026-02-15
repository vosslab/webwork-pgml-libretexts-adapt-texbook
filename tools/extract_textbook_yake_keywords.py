#!/usr/bin/env python3
"""
Extract YAKE keywords from textbook HTML pages.

Outputs:
- Per-reference keyword rows (CSV)
- Aggregated index candidates with reference lists (CSV)
"""

import argparse
import csv
import html.parser
import importlib.util
import math
import re
from pathlib import Path

YAKE_LANGUAGE = "en"
YAKE_MAX_NGRAM = 3
YAKE_DEDUP_LIMIT = 0.9
SINGLE_TERM_MIN_IDF = 3.0
MULTI_TERM_MIN_AVG_IDF = 2.1
MULTI_TERM_MIN_TOKEN_IDF = 1.0
MIN_REFERENCE_WORDS = 8
MIN_PAGE_COUNT = 2
TARGET_DOC_COUNT = 4
SHORTLIST_MIN_SCORE = 0.74
SHORTLIST_MAX_ROWS = 120

CONNECTOR_WORDS = {
	"a",
	"an",
	"and",
	"as",
	"at",
	"by",
	"for",
	"from",
	"in",
	"into",
	"of",
	"on",
	"or",
	"the",
	"to",
	"via",
	"with",
	"without",
}

LOW_SIGNAL_TOKENS = {
	"attribution",
	"easier",
	"generic",
	"improve",
	"needed",
	"placeholder",
	"rarely",
	"read",
	"readability",
	"searchability",
	"student",
}


#============================================

class VisibleTextExtractor(html.parser.HTMLParser):
	"""Collect visible text and ignore script/style blocks."""

	def __init__(self) -> None:
		super().__init__()
		self.text_chunks: list[str] = []
		self.skip_stack: list[str] = []

	def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
		tag_name = tag.lower()
		if tag_name in {"script", "style"}:
			self.skip_stack.append(tag_name)

	def handle_endtag(self, tag: str) -> None:
		tag_name = tag.lower()
		if not self.skip_stack:
			return
		if self.skip_stack[-1] == tag_name:
			self.skip_stack.pop()

	def handle_data(self, data: str) -> None:
		if self.skip_stack:
			return
		text = " ".join(data.split())
		if text:
			self.text_chunks.append(text)


#============================================

class ParagraphExtractor(html.parser.HTMLParser):
	"""Collect paragraph-like text blocks and ignore script/style blocks."""

	PARAGRAPH_TAGS = {"p", "li", "td", "th", "h2", "h3", "h4", "h5", "h6"}

	def __init__(self) -> None:
		super().__init__()
		self.paragraphs: list[str] = []
		self.skip_stack: list[str] = []
		self.capture_depth = 0
		self.current_chunks: list[str] = []

	def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
		tag_name = tag.lower()
		if tag_name in {"script", "style"}:
			self.skip_stack.append(tag_name)
			return
		if self.skip_stack:
			return
		if tag_name in self.PARAGRAPH_TAGS:
			self.capture_depth += 1
			if self.capture_depth == 1:
				self.current_chunks = []

	def handle_endtag(self, tag: str) -> None:
		tag_name = tag.lower()
		if self.skip_stack and self.skip_stack[-1] == tag_name:
			self.skip_stack.pop()
			return
		if self.skip_stack:
			return
		if tag_name in self.PARAGRAPH_TAGS and self.capture_depth > 0:
			self.capture_depth -= 1
			if self.capture_depth == 0:
				text = " ".join(self.current_chunks).strip()
				if text:
					self.paragraphs.append(text)
				self.current_chunks = []

	def handle_data(self, data: str) -> None:
		if self.skip_stack:
			return
		if self.capture_depth <= 0:
			return
		text = " ".join(data.split())
		if text:
			self.current_chunks.append(text)


#============================================

def parse_args() -> argparse.Namespace:
	"""Parse command-line arguments."""
	parser = argparse.ArgumentParser(
		description="Run YAKE on textbook HTML pages and write keyword CSV outputs.",
	)
	parser.add_argument(
		"-i",
		"--input-dir",
		dest="input_dir",
		default="Textbook",
		help="Input textbook directory (default: Textbook).",
	)
	parser.add_argument(
		"-p",
		"--per-page-output",
		dest="per_page_output",
		default="output/yake_keywords_by_page.csv",
		help="Output CSV path for per-reference keywords.",
	)
	parser.add_argument(
		"-a",
		"--aggregate-output",
		dest="aggregate_output",
		default="output/yake_index_candidates.csv",
		help="Output CSV path for aggregated index candidates.",
	)
	parser.add_argument(
		"-k",
		"--max-ngram",
		dest="max_ngram_unused",
		type=int,
		default=YAKE_MAX_NGRAM,
		help=argparse.SUPPRESS,
	)
	parser.add_argument(
		"-t",
		"--top-k",
		dest="top_k",
		type=int,
		default=25,
		help="Top keywords to keep per paragraph (default: 25).",
	)
	parser.add_argument(
		"-m",
		"--min-docs",
		dest="min_docs",
		type=int,
		default=3,
		help="Minimum paragraph-reference count for aggregate candidates (default: 3).",
	)
	parser.add_argument(
		"-x",
		"--max-docs",
		dest="max_docs",
		type=int,
		default=10,
		help="Maximum paragraph-reference count for aggregate candidates (default: 10).",
	)
	return parser.parse_args()


#============================================

def load_yake_module():
	"""Load YAKE module only when needed."""
	if importlib.util.find_spec("yake") is None:
		return None
	import yake
	return yake


#============================================

def collect_html_files(input_dir: Path) -> list[Path]:
	"""Return sorted non-index HTML file paths under input_dir."""
	html_files = sorted(input_dir.rglob("*.html"))
	filtered_files: list[Path] = []
	for path in html_files:
		if not path.is_file():
			continue
		if path.name.endswith("-Index.html"):
			continue
		filtered_files.append(path)
	return filtered_files


#============================================

def extract_visible_text(html_content: str) -> str:
	"""Extract visible text from HTML content."""
	parser = VisibleTextExtractor()
	parser.feed(html_content)
	return " ".join(parser.text_chunks).strip()


#============================================

def extract_paragraph_texts(html_content: str) -> list[str]:
	"""Extract paragraph-like text blocks from HTML content."""
	parser = ParagraphExtractor()
	parser.feed(html_content)
	if parser.paragraphs:
		return parser.paragraphs
	visible_text = extract_visible_text(html_content)
	if not visible_text:
		return []
	return [visible_text]


#============================================

def normalize_keyword(term: str) -> str:
	"""Normalize extracted keyword text."""
	cleaned = " ".join(term.split()).strip()
	cleaned = cleaned.strip(".,;:!?()[]{}\"'`")
	return cleaned


#============================================

def contains_letters(term: str) -> bool:
	"""Return True when the term has at least one letter."""
	for char in term:
		if char.isalpha():
			return True
	return False


#============================================

def tokenize_words(text: str) -> list[str]:
	"""Tokenize text to lowercase word-like tokens."""
	return re.findall(r"[a-z0-9]+(?:[-_][a-z0-9]+)*", text.lower())


#============================================

def singularize_token(token: str) -> str:
	"""Apply a simple, conservative singularization rule."""
	if len(token) <= 3:
		return token
	if token.endswith("ies") and len(token) > 4:
		return token[:-3] + "y"
	if token.endswith(("ss", "us", "is")):
		return token
	if token.endswith("es") and len(token) > 4 and token[-3] in {"s", "x", "z"}:
		return token[:-2]
	if token.endswith("s") and len(token) > 4:
		return token[:-1]
	return token


#============================================

def canonicalize_term(term: str) -> str:
	"""Return a lowercase canonical key for grouping variants."""
	tokens = tokenize_words(term)
	if not tokens:
		return ""
	canonical_tokens = [singularize_token(token) for token in tokens]
	return " ".join(canonical_tokens)


#============================================

def build_word_document_frequency(
	reference_units: list[dict[str, str]],
) -> dict[str, int]:
	"""Build paragraph-document frequency counts for tokens."""
	word_doc_frequency: dict[str, int] = {}
	for unit in reference_units:
		tokens = set(tokenize_words(unit["text_lower"]))
		for token in tokens:
			word_doc_frequency[token] = word_doc_frequency.get(token, 0) + 1
	return word_doc_frequency


#============================================

def token_idf(
	token: str,
	word_doc_frequency: dict[str, int],
	total_docs: int,
) -> float:
	"""Compute inverse document frequency for a token."""
	doc_freq = word_doc_frequency.get(token, 0)
	return math.log((1 + total_docs) / (1 + doc_freq))


#============================================

def has_technical_signal(term: str) -> bool:
	"""Detect acronym/code-like single-word terms worth keeping."""
	if "_" in term or "-" in term:
		return True
	if any(char.isdigit() for char in term):
		return True
	if any(char.isupper() for char in term[1:]) and not term.isupper():
		return True
	return False


#============================================

def score_doc_balance(doc_count: int) -> float:
	"""Score how close reference count is to the index-friendly target range."""
	delta = abs(doc_count - TARGET_DOC_COUNT)
	score = 1.0 - min(delta / TARGET_DOC_COUNT, 1.0)
	return score


#============================================

def score_term_shape(term: str) -> float:
	"""Score a term shape for index usability (2-3 words preferred)."""
	token_count = len(tokenize_words(term))
	if token_count in {2, 3}:
		return 1.0
	if token_count == 1:
		return 0.4
	if token_count == 4:
		return 0.7
	return 0.3


#============================================

def score_term_specificity(
	term: str,
	word_doc_frequency: dict[str, int],
	total_docs: int,
) -> float:
	"""Estimate how specific a term is in this corpus based on IDF."""
	tokens = tokenize_words(term)
	if not tokens:
		return 0.0
	max_idf = math.log(1 + total_docs)
	if max_idf <= 0:
		return 0.0
	idf_values = [token_idf(token, word_doc_frequency, total_docs) for token in tokens]
	avg_idf = sum(idf_values) / len(idf_values)
	score = avg_idf / max_idf
	if score < 0:
		return 0.0
	if score > 1:
		return 1.0
	return score


#============================================

def compute_index_worthiness_score(
	term: str,
	doc_count: int,
	word_doc_frequency: dict[str, int],
	total_docs: int,
) -> float:
	"""Compute a composite score for index-worthiness."""
	doc_balance = score_doc_balance(doc_count)
	term_shape = score_term_shape(term)
	specificity = score_term_specificity(term, word_doc_frequency, total_docs)
	base_score = (0.45 * doc_balance) + (0.35 * specificity) + (0.20 * term_shape)

	# Penalize editorial/meta phrases that are usually poor back-of-book entries.
	tokens = tokenize_words(term)
	low_signal_count = sum(1 for token in tokens if token in LOW_SIGNAL_TOKENS)
	penalty = min(0.25, 0.10 * low_signal_count)
	score = base_score - penalty
	if score < 0:
		return 0.0
	return score


#============================================

def is_low_information_term(
	term: str,
	word_doc_frequency: dict[str, int],
	total_docs: int,
) -> bool:
	"""Heuristic filter for generic terms using corpus statistics."""
	tokens = tokenize_words(term)
	if not tokens:
		return True
	if "placeholder" in tokens:
		return True
	if tokens[0] in CONNECTOR_WORDS or tokens[-1] in CONNECTOR_WORDS:
		return True

	idf_values = [token_idf(token, word_doc_frequency, total_docs) for token in tokens]
	avg_idf = sum(idf_values) / len(idf_values)
	min_idf = min(idf_values)

	if len(tokens) == 1:
		if not has_technical_signal(term):
			return True
		if avg_idf < SINGLE_TERM_MIN_IDF:
			return True
	if len(tokens) > 1 and avg_idf < MULTI_TERM_MIN_AVG_IDF and min_idf < MULTI_TERM_MIN_TOKEN_IDF:
		return True
	return False


#============================================

def choose_display_term(canonical_term: str, variant_counts: dict[str, int]) -> str:
	"""Choose a display term for an aggregate candidate."""
	if canonical_term == "":
		return canonical_term
	display_tokens = canonical_term.split()
	candidate_rows = sorted(
		variant_counts.items(),
		key=lambda item: (-item[1], len(item[0]), item[0].lower()),
	)
	for index, canonical_token in enumerate(display_tokens):
		for variant_text, _count in candidate_rows:
			variant_tokens = tokenize_words(variant_text)
			if len(variant_tokens) <= index:
				continue
			variant_token = variant_tokens[index]
			if variant_token != canonical_token:
				continue
			raw_parts = variant_text.split()
			if len(raw_parts) <= index:
				continue
			raw_token = raw_parts[index]
			if raw_token.isupper():
				display_tokens[index] = raw_token
				break
			if any(char.isupper() for char in raw_token[1:]):
				display_tokens[index] = raw_token
				break
	return " ".join(display_tokens)


#============================================

def is_subphrase_of(longer_term: str, shorter_term: str) -> bool:
	"""Return True when shorter_term appears as full-token subphrase of longer_term."""
	longer = f" {longer_term.lower()} "
	shorter = f" {shorter_term.lower()} "
	return shorter in longer


#============================================

def prune_subphrase_duplicates(rows: list[dict[str, object]]) -> list[dict[str, object]]:
	"""Remove shorter terms when a longer term has identical references."""
	kept_rows: list[dict[str, object]] = []
	rows_sorted = sorted(
		rows,
		key=lambda row: (
			-len(str(row["term"]).split()),
			-len(str(row["term"])),
			str(row["term"]).lower(),
		),
	)
	for row in rows_sorted:
		term = str(row["term"])
		reference_signature = tuple(row["references_list"])
		duplicate = False
		for kept in kept_rows:
			if tuple(kept["references_list"]) != reference_signature:
				continue
			kept_term = str(kept["term"])
			if is_subphrase_of(kept_term, term):
				duplicate = True
				break
		if not duplicate:
			kept_rows.append(row)
	return kept_rows


#============================================

def ensure_parent(path: Path) -> None:
	"""Create parent directory for path when needed."""
	if path.parent and not path.parent.exists():
		path.parent.mkdir(parents=True, exist_ok=True)


#============================================

def write_keywords_csv(output_path: Path, rows: list[dict[str, str]]) -> None:
	"""Write per-reference keyword rows to CSV."""
	ensure_parent(output_path)
	fieldnames = ["ref_id", "page_path", "keyword", "score"]
	with output_path.open("w", newline="", encoding="utf-8") as handle:
		writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
		writer.writeheader()
		for row in rows:
			writer.writerow(row)


#============================================

def write_aggregate_csv(output_path: Path, rows: list[dict[str, str]]) -> None:
	"""Write aggregated index candidates to CSV."""
	ensure_parent(output_path)
	fieldnames = [
		"term",
		"tier",
		"index_score",
		"doc_count",
		"page_count",
		"avg_score",
		"references",
		"page_paths",
	]
	with output_path.open("w", newline="", encoding="utf-8") as handle:
		writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
		writer.writeheader()
		for row in rows:
			writer.writerow(row)


#============================================

def classify_tier(index_score: float, doc_count: int) -> str:
	"""Classify candidate into review tiers for manual indexing."""
	if index_score >= 0.85 and 3 <= doc_count <= 6:
		return "A"
	if index_score >= SHORTLIST_MIN_SCORE:
		return "B"
	return "C"


#============================================

def build_term_pattern(term: str) -> re.Pattern[str]:
	"""Build a case-insensitive regex that matches a phrase as a standalone term."""
	escaped = re.escape(term.lower())
	escaped = escaped.replace(r"\ ", r"\s+")
	pattern_text = r"(?<!\w)" + escaped + r"(?!\w)"
	return re.compile(pattern_text)


#============================================

def find_term_references(
	terms: list[str],
	reference_units: list[dict[str, str]],
) -> tuple[list[str], list[str]]:
	"""Find reference ids and page paths where a term variant appears."""
	patterns = [build_term_pattern(term) for term in terms if term]
	if not patterns:
		return [], []
	reference_hits: list[str] = []
	page_hits_set: set[str] = set()
	for unit in reference_units:
		text_lower = unit["text_lower"]
		if any(pattern.search(text_lower) for pattern in patterns):
			reference_hits.append(unit["ref_id"])
			page_hits_set.add(unit["page_path"])
	page_hits = sorted(page_hits_set)
	return reference_hits, page_hits


#============================================

def main() -> None:
	"""Program entry point."""
	args = parse_args()
	yake = load_yake_module()
	if yake is None:
		print(
			"Missing dependency 'yake'. Install with: "
			"source source_me.sh && python -m pip install yake"
		)
		return

	input_dir = Path(args.input_dir)
	if not input_dir.exists() or not input_dir.is_dir():
		raise RuntimeError(f"Input directory not found: {input_dir}")

	html_files = collect_html_files(input_dir)
	if not html_files:
		raise RuntimeError(f"No HTML files found in: {input_dir}")

	extractor = yake.KeywordExtractor(
		lan=YAKE_LANGUAGE,
		n=YAKE_MAX_NGRAM,
		dedupLim=YAKE_DEDUP_LIMIT,
		top=args.top_k,
	)

	keyword_rows: list[dict[str, str]] = []
	aggregate: dict[str, dict[str, object]] = {}
	all_reference_units: list[dict[str, str]] = []

	for page_path in html_files:
		html_content = page_path.read_text(encoding="utf-8", errors="replace")
		page_id = str(page_path)
		reference_units: list[tuple[str, str]] = []
		paragraphs = extract_paragraph_texts(html_content)
		for index, paragraph_text in enumerate(paragraphs, start=1):
			word_count = len(tokenize_words(paragraph_text))
			if word_count < MIN_REFERENCE_WORDS:
				continue
			ref_id = f"{page_id}#p{index}"
			reference_units.append((ref_id, paragraph_text))
		for ref_id, paragraph_text in reference_units:
			all_reference_units.append(
				{
					"ref_id": ref_id,
					"page_path": page_id,
					"text": paragraph_text,
					"text_lower": paragraph_text.lower(),
				},
			)

	total_reference_units = len(all_reference_units)
	word_doc_frequency = build_word_document_frequency(all_reference_units)

	for unit in all_reference_units:
		ref_id = unit["ref_id"]
		page_id = unit["page_path"]
		reference_text = unit["text"]
		keywords: list[tuple[str, float]] = extractor.extract_keywords(reference_text)
		for keyword_text, score in keywords:
			term = normalize_keyword(keyword_text)
			if len(term) < 3:
				continue
			if not contains_letters(term):
				continue
			if is_low_information_term(term, word_doc_frequency, total_reference_units):
				continue

			canonical_term = canonicalize_term(term)
			if canonical_term == "":
				continue

			keyword_rows.append(
				{
					"ref_id": ref_id,
					"page_path": page_id,
					"keyword": term,
					"score": f"{score:.8f}",
				},
			)

			if canonical_term not in aggregate:
				aggregate[canonical_term] = {
					"canonical_term": canonical_term,
					"variant_counts": {},
					"variant_patterns": set(),
					"scores": [],
				}
			variant_counts = aggregate[canonical_term]["variant_counts"]
			variant_counts[term] = variant_counts.get(term, 0) + 1
			aggregate[canonical_term]["variant_patterns"].add(term.lower())
			aggregate[canonical_term]["scores"].append(score)

	aggregate_rows_raw: list[dict[str, object]] = []
	for term_key in sorted(aggregate):
		term_data = aggregate[term_key]
		variant_patterns = sorted(term_data["variant_patterns"])
		references, page_paths = find_term_references(variant_patterns, all_reference_units)
		doc_count = len(references)
		if doc_count < args.min_docs:
			continue
		if doc_count > args.max_docs:
			continue

		page_count = len(page_paths)
		if page_count < MIN_PAGE_COUNT:
			continue
		scores = term_data["scores"]
		avg_score = sum(scores) / len(scores)
		display_term = choose_display_term(
			str(term_data["canonical_term"]),
			term_data["variant_counts"],
		)
		index_score = compute_index_worthiness_score(
			display_term,
			doc_count,
			word_doc_frequency,
			total_reference_units,
		)
		aggregate_rows_raw.append(
			{
				"term": display_term,
				"index_score": index_score,
				"doc_count": doc_count,
				"page_count": page_count,
				"avg_score": avg_score,
				"references_list": references,
				"page_paths_list": page_paths,
			},
		)

	pruned_rows = prune_subphrase_duplicates(aggregate_rows_raw)
	aggregate_rows: list[dict[str, str]] = []
	for row in pruned_rows:
		aggregate_rows.append(
			{
				"term": str(row["term"]),
				"tier": classify_tier(float(row["index_score"]), int(row["doc_count"])),
				"index_score": f"{row['index_score']:.6f}",
				"doc_count": str(row["doc_count"]),
				"page_count": str(row["page_count"]),
				"avg_score": f"{row['avg_score']:.8f}",
				"references": "; ".join(row["references_list"]),
				"page_paths": "; ".join(row["page_paths_list"]),
			},
		)

	aggregate_rows.sort(
		key=lambda row: (
			row["tier"],
			-float(row["index_score"]),
			-int(row["doc_count"]),
			-int(row["page_count"]),
			float(row["avg_score"]),
			row["term"].lower(),
		)
	)

	per_page_output = Path(args.per_page_output)
	aggregate_output = Path(args.aggregate_output)
	shortlist_output = aggregate_output.with_name("yake_index_shortlist.csv")

	shortlist_rows: list[dict[str, str]] = []
	for row in aggregate_rows:
		if row["tier"] == "C":
			continue
		if float(row["index_score"]) < SHORTLIST_MIN_SCORE:
			continue
		shortlist_rows.append(row)
		if len(shortlist_rows) >= SHORTLIST_MAX_ROWS:
			break

	write_keywords_csv(per_page_output, keyword_rows)
	write_aggregate_csv(aggregate_output, aggregate_rows)
	write_aggregate_csv(shortlist_output, shortlist_rows)

	print(f"HTML files processed: {len(html_files)}")
	print("Reference unit: paragraph")
	print(f"Total reference units: {total_reference_units}")
	print(f"Keyword rows: {len(keyword_rows)} -> {per_page_output}")
	print(f"Aggregate rows: {len(aggregate_rows)} -> {aggregate_output}")
	print(f"Shortlist rows: {len(shortlist_rows)} -> {shortlist_output}")


if __name__ == "__main__":
	main()
