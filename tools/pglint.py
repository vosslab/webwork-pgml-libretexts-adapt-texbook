#!/usr/bin/env python3

# Standard Library
import re
import json
import sys
import time
import base64
import random
import argparse
from pathlib import Path

# PIP3 modules
import requests


DEFAULT_ERROR_KEYS: list[str] = ["errors", "warnings"]
DEFAULT_MESSAGE_KEYS: list[str] = ["message", "error", "warning", "detail", "stderr"]
DEFAULT_HOST = "http://localhost:3000"
DEFAULT_ENDPOINT = "/render-api"
DEFAULT_SEED = 1
DEFAULT_TIMEOUT = 30.0
DEFAULT_OUTPUT_FORMAT = "default"
DEFAULT_RESPONSE_FORMAT = "json"


def parse_args() -> argparse.Namespace:
	"""
	Parse command-line arguments.
	"""
	parser = argparse.ArgumentParser(
		description="Lint PGML by rendering through the local renderer API.",
	)
	parser.add_argument(
		"-s",
		"--seed",
		dest="seed",
		type=int,
		default=DEFAULT_SEED,
		help="Seed to render (default: 1).",
	)
	parser.add_argument(
		"-H",
		"--host",
		dest="host",
		default=DEFAULT_HOST,
		help="Renderer base URL (default: http://localhost:3000).",
	)
	parser.add_argument(
		"pg_files",
		nargs="+",
		type=Path,
		help="PG files to lint.",
	)
	parser.add_argument(
		"--debug",
		dest="debug",
		action="store_true",
		help="Print request/response details to stderr.",
	)
	return parser.parse_args()


#============================================


def build_url(host: str) -> str:
	"""
	Build the render URL from host and the default endpoint.
	"""
	host_clean = host.rstrip("/")
	url = f"{host_clean}{DEFAULT_ENDPOINT}"
	return url


#============================================


def build_payload(pg_source: str, seed: int, encode_source: bool) -> dict[str, object]:
	"""
	Build the request payload for the renderer.
	"""
	if encode_source:
		encoded = base64.b64encode(pg_source.encode("utf-8")).decode("ascii")
		problem_source = encoded
	else:
		problem_source = pg_source
	payload = {
		"problemSource": problem_source,
		"outputFormat": DEFAULT_OUTPUT_FORMAT,
		"problemSeed": seed,
		"_format": DEFAULT_RESPONSE_FORMAT,
		"showComments": 1,
	}
	return payload


#============================================


def coerce_int(value: object) -> int | None:
	"""
	Coerce a value to int if possible.
	"""
	if isinstance(value, int):
		return value
	if isinstance(value, str) and value.isdigit():
		return int(value)
	return None


#============================================


def pick_message(item: dict[str, object], message_keys: list[str]) -> str:
	"""
	Select the best message from a dict.
	"""
	for key in message_keys:
		if key in item and item[key] is not None:
			message = str(item[key])
			return message
	message = json.dumps(item, sort_keys=True)
	return message


#============================================


def sanitize_message(message: str) -> str:
	"""
	Flatten message whitespace for single-line output.
	"""
	flat = " ".join(message.split())
	return flat


#============================================


def parse_line_column(message: str) -> tuple[int | None, int | None]:
	"""
	Extract line and column numbers from a message if present.
	"""
	match = re.search(
		r"[Ll]ine\s+(\d+)(?:\D+column\s*(\d+))?",
		message,
	)
	if not match:
		return None, None
	line_value = int(match.group(1))
	column_value = None
	if match.group(2):
		column_value = int(match.group(2))
	return line_value, column_value


#============================================


def truncate_message(message: str, limit: int = 200) -> str:
	"""
	Truncate a message to a safe single-line length.
	"""
	if len(message) <= limit:
		return message
	return message[:limit]


#============================================


def normalize_issue(item: object, message_keys: list[str]) -> dict[str, object]:
	"""
	Normalize an issue into a line/column/message dict.
	"""
	line_value = 1
	column_value = 1
	if isinstance(item, dict):
		line_keys = ["line", "lineNumber", "lineno", "row"]
		col_keys = ["column", "col", "columnNumber", "colNumber"]
		for key in line_keys:
			if key in item:
				line_candidate = coerce_int(item[key])
				if line_candidate is not None:
					line_value = line_candidate
					break
		for key in col_keys:
			if key in item:
				col_candidate = coerce_int(item[key])
				if col_candidate is not None:
					column_value = col_candidate
					break
		message_value = pick_message(item, message_keys)
	else:
		message_value = str(item)
	message_value = sanitize_message(message_value)
	line_hint, column_hint = parse_line_column(message_value)
	if line_hint is not None:
		line_value = line_hint
	if column_hint is not None:
		column_value = column_hint
	issue = {
		"line": line_value,
		"column": column_value,
		"message": truncate_message(message_value),
	}
	return issue


#============================================


def extract_issues(
	data: object | None,
	error_keys: list[str],
	message_keys: list[str],
) -> list[dict[str, object]]:
	"""
	Extract issues from a JSON response payload.
	"""
	if not isinstance(data, dict):
		return []
	issues: list[dict[str, object]] = []
	for key in error_keys:
		if key not in data:
			continue
		value = data[key]
		if isinstance(value, list):
			for item in value:
				issues.append(normalize_issue(item, message_keys))
			continue
		if value is None:
			continue
		issues.append(normalize_issue(value, message_keys))
	return issues


#============================================


def build_issue_from_message(message: str) -> dict[str, object]:
	"""
	Build an issue dict from a single message string.
	"""
	cleaned = sanitize_message(message)
	line_hint, column_hint = parse_line_column(cleaned)
	line_value = line_hint if line_hint is not None else 1
	column_value = column_hint if column_hint is not None else 1
	issue = {
		"line": line_value,
		"column": column_value,
		"message": truncate_message(cleaned),
	}
	return issue


#============================================


def extract_html_warnings(rendered_html: str) -> list[str]:
	"""
	Extract warning text embedded in rendered HTML.
	"""
	warnings: list[str] = []
	headings = ["Translator errors", "Warning messages"]
	for heading in headings:
		pattern = re.compile(
			rf"{heading}.*?(<pre>.*?</pre>|<ul>.*?</ul>)",
			re.IGNORECASE | re.DOTALL,
		)
		match = pattern.search(rendered_html)
		if match:
			block = match.group(1)
			items = re.findall(
				r"<li[^>]*>(.*?)</li>",
				block,
				flags=re.IGNORECASE | re.DOTALL,
			)
			if items:
				for item in items:
					text = sanitize_message(re.sub(r"<[^>]+>", " ", item))
					if text:
						warnings.append(f"{heading}: {text}")
				continue
			text = sanitize_message(re.sub(r"<[^>]+>", " ", block))
			if text:
				warnings.append(f"{heading}: {text}")
				continue
		if heading.lower() in rendered_html.lower():
			warnings.append(f"{heading} reported in renderedHTML")
	return warnings


#============================================


def extract_html_warning_message(rendered_html: str) -> str | None:
	"""
	Extract a compact warning message from raw HTML responses.
	"""
	warnings = extract_html_warnings(rendered_html)
	if warnings:
		message = warnings[0]
		if re.search(r"[A-Za-z0-9]", message):
			return message
	pre_match = re.search(r"<pre[^>]*>(.*?)</pre>", rendered_html, re.IGNORECASE | re.DOTALL)
	if pre_match:
		pre_text = sanitize_message(re.sub(r"<[^>]+>", " ", pre_match.group(1)))
		if pre_text and re.search(r"[A-Za-z0-9]", pre_text):
			return pre_text
	for tag in ("h1", "h2", "h3", "title"):
		match = re.search(rf"<{tag}[^>]*>(.*?)</{tag}>", rendered_html, re.IGNORECASE | re.DOTALL)
		if match:
			text = sanitize_message(re.sub(r"<[^>]+>", " ", match.group(1)))
			if text and re.search(r"[A-Za-z0-9]", text):
				return text
	return None


#============================================


def extract_renderer_issues(data: object | None) -> list[dict[str, object]]:
	"""
	Extract renderer-specific issues from JSON responses.
	"""
	if not isinstance(data, dict):
		return []
	issues: list[dict[str, object]] = []
	flags = data.get("flags")
	if isinstance(flags, dict):
		error_flag = flags.get("error_flag")
		if error_flag not in (0, "0", None, False):
			issues.append(build_issue_from_message("render error (flags.error_flag=1)"))
	debug = data.get("debug")
	if isinstance(debug, dict):
		debug_map = {
			"pg_warn": "PG warning",
			"internal": "Renderer internal",
			"debug": "Renderer debug",
		}
		for key, label in debug_map.items():
			value = debug.get(key)
			if isinstance(value, list):
				for item in value:
					if item:
						issues.append(build_issue_from_message(f"{label}: {item}"))
			elif isinstance(value, str) and value.strip():
				issues.append(build_issue_from_message(f"{label}: {value}"))
	rendered_html = data.get("renderedHTML")
	if isinstance(rendered_html, str):
		for warning in extract_html_warnings(rendered_html):
			issues.append(build_issue_from_message(warning))
	return issues


#============================================


def extract_html_text(rendered_html: str) -> str:
	"""
	Strip HTML tags to recover readable text.
	"""
	without_scripts = re.sub(
		r"<(script|style)[^>]*>.*?</\\1>",
		" ",
		rendered_html,
		flags=re.IGNORECASE | re.DOTALL,
	)
	text = re.sub(r"<[^>]+>", " ", without_scripts)
	flattened = sanitize_message(text)
	if re.search(r"[A-Za-z0-9]", flattened):
		return flattened
	return ""


#============================================


def merge_issues(
	issues: list[dict[str, object]],
	extra: list[dict[str, object]],
) -> list[dict[str, object]]:
	"""
	Merge issue lists without duplicating messages.
	"""
	seen = {str(issue.get("message", "")) for issue in issues}
	for issue in extra:
		message = str(issue.get("message", ""))
		if message in seen:
			continue
		issues.append(issue)
		seen.add(message)
	return issues


#============================================


def parse_json_response(response: requests.Response) -> object | None:
	"""
	Parse JSON if the response appears to be JSON.
	"""
	content_type = response.headers.get("content-type", "")
	should_parse = "json" in content_type.lower()
	text = response.text.strip()
	if not should_parse:
		if text.startswith("{") or text.startswith("["):
			should_parse = True
	if not should_parse:
		return None
	try:
		data = response.json()
	except ValueError:
		return None
	return data


#============================================


def request_render(
	url: str,
	payload: dict[str, object],
	mode: str,
) -> tuple[requests.Response, object | None]:
	"""
	Post a render request and return the response and JSON payload.
	"""
	if mode == "json":
		response = requests.post(
			url,
			json=payload,
			timeout=DEFAULT_TIMEOUT,
			headers={"Accept": "application/json"},
		)
	elif mode == "multipart":
		parts = {key: (None, str(value)) for key, value in payload.items()}
		response = requests.post(
			url,
			files=parts,
			timeout=DEFAULT_TIMEOUT,
			headers={"Accept": "application/json"},
		)
	else:
		response = requests.post(
			url,
			data=payload,
			timeout=DEFAULT_TIMEOUT,
			headers={"Accept": "application/json"},
		)
	data = parse_json_response(response)
	return response, data


#============================================


def format_issue(path: Path, line: int, column: int, message: str) -> str:
	"""
	Format a single issue line for output.
	"""
	formatted = f"{path}:{line}:{column}: {message}"
	return formatted


#============================================


def debug_log(args: argparse.Namespace, message: str) -> None:
	"""
	Write debug output to stderr when enabled.
	"""
	if not args.debug:
		return
	print(f"DEBUG: {message}", file=sys.stderr)


#============================================


def print_issue(path: Path, issue: dict[str, object]) -> None:
	"""
	Print a normalized issue.
	"""
	line_value = int(issue.get("line", 1))
	column_value = int(issue.get("column", 1))
	message_value = str(issue.get("message", ""))
	output_line = format_issue(path, line_value, column_value, message_value)
	print(output_line)


#============================================


def lint_file(pg_file: Path, args: argparse.Namespace) -> int:
	"""
	Lint a single PG file by rendering it through the HTTP API.
	"""
	if not pg_file.exists():
		message = "file not found"
		print(format_issue(pg_file, 1, 1, message))
		return 2
	try:
		pg_source = pg_file.read_text(encoding="utf-8")
	except OSError as exc:
		message = f"read error: {exc}"
		print(format_issue(pg_file, 1, 1, message))
		return 2
	url = build_url(args.host)
	payload = build_payload(pg_source, args.seed, True)
	time.sleep(random.random())
	try:
		debug_log(args, "attempt json base64")
		response, data = request_render(url, payload, "json")
	except requests.RequestException as exc:
		message = f"transport error: {exc}"
		print(format_issue(pg_file, 1, 1, message))
		return 2
	debug_log(
		args,
		f"status {response.status_code}, content-type {response.headers.get('content-type', '')}",
	)
	debug_log(args, f"json parsed: {data is not None}")
	if response.status_code >= 500 and data is None:
		payload = build_payload(pg_source, args.seed, False)
		try:
			debug_log(args, "attempt json raw")
			response, data = request_render(url, payload, "json")
		except requests.RequestException as exc:
			message = f"transport error: {exc}"
			print(format_issue(pg_file, 1, 1, message))
			return 2
		debug_log(
			args,
			f"status {response.status_code}, content-type {response.headers.get('content-type', '')}",
		)
		debug_log(args, f"json parsed: {data is not None}")
	if response.status_code >= 500 and data is None:
		payload = build_payload(pg_source, args.seed, True)
		try:
			debug_log(args, "attempt multipart base64")
			response, data = request_render(url, payload, "multipart")
		except requests.RequestException as exc:
			message = f"transport error: {exc}"
			print(format_issue(pg_file, 1, 1, message))
			return 2
		debug_log(
			args,
			f"status {response.status_code}, content-type {response.headers.get('content-type', '')}",
		)
		debug_log(args, f"json parsed: {data is not None}")
	if response.status_code >= 500 and data is None:
		payload = build_payload(pg_source, args.seed, False)
		try:
			debug_log(args, "attempt multipart raw")
			response, data = request_render(url, payload, "multipart")
		except requests.RequestException as exc:
			message = f"transport error: {exc}"
			print(format_issue(pg_file, 1, 1, message))
			return 2
		debug_log(
			args,
			f"status {response.status_code}, content-type {response.headers.get('content-type', '')}",
		)
		debug_log(args, f"json parsed: {data is not None}")
	issues = extract_issues(data, DEFAULT_ERROR_KEYS, DEFAULT_MESSAGE_KEYS)
	renderer_issues = extract_renderer_issues(data)
	issues = merge_issues(issues, renderer_issues)
	if response.status_code != 200:
		if issues:
			for issue in issues:
				print_issue(pg_file, issue)
			return 1
		message = None
		if isinstance(data, dict):
			message = pick_message(data, DEFAULT_MESSAGE_KEYS)
		if not message and response.text.strip():
			message = extract_html_warning_message(response.text)
			if message is None:
				plain_text = extract_html_text(response.text)
				if plain_text:
					message = truncate_message(plain_text)
				else:
					message = f"http {response.status_code} (non-json response)"
		if not message:
			message = f"http {response.status_code}"
		message = sanitize_message(message)
		print(format_issue(pg_file, 1, 1, truncate_message(message)))
		return 1
	if data is None and response.status_code == 200:
		debug_log(args, "html 200 response; scanning for warning blocks")
		html_message = extract_html_warning_message(response.text)
		if html_message:
			print(format_issue(pg_file, 1, 1, truncate_message(html_message)))
			return 1
		html_text = extract_html_text(response.text)
		if html_text:
			print(format_issue(pg_file, 1, 1, truncate_message(html_text)))
			return 1
		debug_log(args, "html 200 response with no warnings detected")
		return 0
	if data is None:
		message = "protocol error: expected json response"
		print(format_issue(pg_file, 1, 1, message))
		return 2
	if issues:
		for issue in issues:
			print_issue(pg_file, issue)
		return 1
	return 0


#============================================


def main() -> int:
	"""
	Run the lint command.
	"""
	args = parse_args()
	exit_code = 0
	for pg_file in args.pg_files:
		result = lint_file(pg_file, args)
		if result > exit_code:
			exit_code = result
	return exit_code


if __name__ == "__main__":
	raise SystemExit(main())
