#!/usr/bin/env python3
"""Extract and check external URLs from repository Markdown and HTML files."""

import re
import time
import enum
import html
import random
import pathlib
import argparse
import dataclasses
import html.parser
import urllib.error
import urllib.parse
import urllib.request


DEFAULT_PATHS = ("README.md", "docs", "Textbook")
SUPPORTED_SUFFIXES = {".html", ".md"}
SKIPPED_HOSTS = {"127.0.0.1", "::1", "localhost"}
BROKEN_STATUS_CODES = {404, 410}
NON_RETRYABLE_STATUS_CODES = {401, 403}
MAX_ATTEMPTS = 2
REQUEST_TIMEOUT_SECONDS = 10
URL_RE = re.compile(r"https?://[^\s<>\"]+", re.IGNORECASE)
INLINE_CODE_RE = re.compile(r"`[^`]*`")


class Outcome(enum.StrEnum):
	"""Possible results from checking an external URL."""

	OK = "ok"
	BROKEN = "broken"
	INCONCLUSIVE = "inconclusive"


@dataclasses.dataclass(frozen=True)
class LinkOccurrence:
	"""One source location containing an external URL."""

	path: str
	line_number: int


@dataclasses.dataclass(frozen=True)
class RequestObservation:
	"""HTTP status or transport error observed during one request."""

	status_code: int | None
	detail: str


@dataclasses.dataclass(frozen=True)
class CheckResult:
	"""Final classification for one checked URL."""

	url: str
	outcome: Outcome
	status_code: int | None
	detail: str


class HtmlUrlParser(html.parser.HTMLParser):
	"""Collect URL-bearing HTML attributes with source line numbers."""

	def __init__(self) -> None:
		super().__init__(convert_charrefs=True)
		self.urls: list[tuple[str, int]] = []

	def handle_starttag(
		self,
		tag: str,
		attrs: list[tuple[str, str | None]],
	) -> None:
		"""Collect href and src values from a start tag."""
		self._collect_attributes(attrs)

	def handle_startendtag(
		self,
		tag: str,
		attrs: list[tuple[str, str | None]],
	) -> None:
		"""Collect href and src values from a self-closing tag."""
		self._collect_attributes(attrs)

	def _collect_attributes(self, attrs: list[tuple[str, str | None]]) -> None:
		"""Record URL-bearing attributes from one HTML tag."""
		line_number, _column_number = self.getpos()
		for key, value in attrs:
			if value is None:
				continue
			if key.lower() in {"href", "src"}:
				self.urls.append((value, line_number))


#============================================
def parse_args() -> argparse.Namespace:
	"""Parse command-line arguments."""
	parser = argparse.ArgumentParser(
		description="Check external URLs found in Markdown and HTML files."
	)
	parser.add_argument(
		"paths",
		nargs="*",
		help="Files or directories to scan (defaults to README.md, docs, and Textbook).",
	)
	return parser.parse_args()


#============================================
def discover_input_files(raw_paths: list[str]) -> list[pathlib.Path]:
	"""
	Find supported Markdown and HTML files beneath the requested paths.

	Args:
		raw_paths: User-supplied files or directories, or an empty list for defaults.

	Returns:
		list[pathlib.Path]: Sorted, unique input files.
	"""
	requested_paths = raw_paths
	if not requested_paths:
		requested_paths = list(DEFAULT_PATHS)

	files: set[pathlib.Path] = set()
	for raw_path in requested_paths:
		path = pathlib.Path(raw_path)
		if not path.exists():
			raise FileNotFoundError(f"Input path does not exist: {path}")
		if path.is_file():
			if path.suffix.lower() not in SUPPORTED_SUFFIXES:
				raise ValueError(f"Unsupported input file type: {path}")
			files.add(path)
			continue
		for candidate in path.rglob("*"):
			if candidate.is_file() and candidate.suffix.lower() in SUPPORTED_SUFFIXES:
				files.add(candidate)
	return sorted(files, key=lambda item: item.as_posix())


#============================================
def normalize_external_url(raw_url: str) -> str:
	"""
	Normalize a checkable HTTP(S) URL or return an empty string.

	Args:
		raw_url: URL text extracted from a source file.

	Returns:
		str: Defragmented external URL, or an empty string when it should be skipped.
	"""
	url = html.unescape(raw_url).strip().rstrip("\"'.,;:!?]}*")
	while url.endswith(")") and url.count(")") > url.count("("):
		url = url[:-1]
	url, _fragment = urllib.parse.urldefrag(url)
	parsed = urllib.parse.urlsplit(url)
	if parsed.scheme.lower() not in {"http", "https"}:
		return ""
	if parsed.hostname is None:
		return ""
	if parsed.hostname.lower() in SKIPPED_HOSTS:
		return ""
	if parsed.path == "":
		parsed = parsed._replace(path="/")
	return urllib.parse.urlunsplit(parsed)


#============================================
def extract_markdown_urls(markdown_text: str) -> list[tuple[str, int]]:
	"""
	Extract external URLs from Markdown while ignoring code regions.

	Args:
		markdown_text: Markdown source text.

	Returns:
		list[tuple[str, int]]: URL and one-based source line pairs.
	"""
	urls: list[tuple[str, int]] = []
	in_fence = False
	for line_number, line in enumerate(markdown_text.splitlines(), start=1):
		stripped = line.lstrip()
		if stripped.startswith("```") or stripped.startswith("~~~"):
			in_fence = not in_fence
			continue
		if in_fence:
			continue
		masked_line = INLINE_CODE_RE.sub("", line)
		seen_on_line: set[str] = set()
		for match in URL_RE.finditer(masked_line):
			url = normalize_external_url(match.group(0))
			if not url or url in seen_on_line:
				continue
			seen_on_line.add(url)
			urls.append((url, line_number))
	return urls


#============================================
def extract_html_urls(html_text: str) -> list[tuple[str, int]]:
	"""
	Extract external URLs from HTML href and src attributes.

	Args:
		html_text: HTML source text.

	Returns:
		list[tuple[str, int]]: URL and one-based source line pairs.
	"""
	parser = HtmlUrlParser()
	parser.feed(html_text)
	urls: list[tuple[str, int]] = []
	for raw_url, line_number in parser.urls:
		url = normalize_external_url(raw_url)
		if url:
			urls.append((url, line_number))
	return urls


#============================================
def collect_external_urls(
	input_files: list[pathlib.Path],
) -> dict[str, list[LinkOccurrence]]:
	"""
	Collect unique external URLs and every source location that uses them.

	Args:
		input_files: Markdown and HTML files to scan.

	Returns:
		dict[str, list[LinkOccurrence]]: URL-to-source-location mapping.
	"""
	collected: dict[str, list[LinkOccurrence]] = {}
	for path in input_files:
		text = path.read_text(encoding="utf-8", errors="replace")
		if path.suffix.lower() == ".md":
			found_urls = extract_markdown_urls(text)
		else:
			found_urls = extract_html_urls(text)
		for url, line_number in found_urls:
			occurrence = LinkOccurrence(path.as_posix(), line_number)
			if url not in collected:
				collected[url] = []
			if occurrence not in collected[url]:
				collected[url].append(occurrence)
	return collected


#============================================
def classify_status_code(status_code: int) -> Outcome:
	"""
	Classify an HTTP status code.

	Args:
		status_code: HTTP response status.

	Returns:
		Outcome: Confirmed good, confirmed broken, or inconclusive.
	"""
	if 200 <= status_code < 400:
		return Outcome.OK
	if status_code in BROKEN_STATUS_CODES:
		return Outcome.BROKEN
	return Outcome.INCONCLUSIVE


#============================================
def fetch_url_once(url: str) -> RequestObservation:
	"""
	Request one URL once, reading only enough data to establish connectivity.

	Args:
		url: External URL to request.

	Returns:
		RequestObservation: HTTP status or transport failure detail.
	"""
	time.sleep(random.random())
	headers = {
		"Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
		"User-Agent": "ADAPT-WeBWorK-Handbook-link-checker/1.0",
	}
	request = urllib.request.Request(url, headers=headers, method="GET")
	try:
		# normalize_external_url limits requests to HTTP(S) URLs.
		response = urllib.request.urlopen(  # nosec B310
			request, timeout=REQUEST_TIMEOUT_SECONDS
		)
	except urllib.error.HTTPError as error:
		error.close()
		return RequestObservation(error.code, str(error.reason))
	except (urllib.error.URLError, TimeoutError) as error:
		return RequestObservation(None, str(error.reason if hasattr(error, "reason") else error))
	with response:
		response.read(1)
		status_code = response.getcode()
		detail = str(getattr(response, "reason", ""))
	return RequestObservation(status_code, detail)


#============================================
def check_url(url: str) -> CheckResult:
	"""
	Check one URL with bounded retries for inconclusive failures.

	Args:
		url: External URL to check.

	Returns:
		CheckResult: Final URL classification.
	"""
	for attempt_number in range(1, MAX_ATTEMPTS + 1):
		observation = fetch_url_once(url)
		if observation.status_code is None:
			outcome = Outcome.INCONCLUSIVE
		else:
			outcome = classify_status_code(observation.status_code)
		if outcome is not Outcome.INCONCLUSIVE:
			return CheckResult(url, outcome, observation.status_code, observation.detail)
		if observation.status_code in NON_RETRYABLE_STATUS_CODES:
			return CheckResult(url, outcome, observation.status_code, observation.detail)
		if attempt_number == MAX_ATTEMPTS:
			return CheckResult(url, outcome, observation.status_code, observation.detail)
	raise RuntimeError(f"URL check did not produce a result: {url}")


#============================================
def print_result(
	result: CheckResult,
	occurrences: list[LinkOccurrence],
) -> None:
	"""
	Print one URL result and source locations for non-successes.

	Args:
		result: Final URL check result.
		occurrences: Source locations containing the URL.
	"""
	status_text = "no status"
	if result.status_code is not None:
		status_text = str(result.status_code)
	print(f"{result.outcome.value.upper():12} {status_text:9} {result.url}")
	if result.outcome is Outcome.OK:
		return
	if result.detail:
		print(f"  Detail: {result.detail}")
	for occurrence in occurrences:
		print(f"  Source: {occurrence.path}:{occurrence.line_number}")


#============================================
def main() -> int:
	"""
	Scan repository content and check each unique external URL.

	Returns:
		int: One when confirmed broken links exist, otherwise zero.
	"""
	args = parse_args()
	input_files = discover_input_files(args.paths)
	url_occurrences = collect_external_urls(input_files)
	print(
		f"Found {len(url_occurrences)} unique external URLs "
		f"in {len(input_files)} Markdown and HTML files."
	)

	results: list[CheckResult] = []
	for url in sorted(url_occurrences):
		result = check_url(url)
		results.append(result)
		print_result(result, url_occurrences[url])

	ok_count = sum(result.outcome is Outcome.OK for result in results)
	broken_count = sum(result.outcome is Outcome.BROKEN for result in results)
	inconclusive_count = sum(
		result.outcome is Outcome.INCONCLUSIVE for result in results
	)
	print(
		f"Summary: {ok_count} ok, {broken_count} broken, "
		f"{inconclusive_count} inconclusive."
	)
	if broken_count:
		return 1
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
