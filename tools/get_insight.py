#!/usr/bin/env python3
"""
Render and save text-focused HTML for:

1) LibreTexts Insight pages
	https://commons.libretexts.org/insight/*

2) Common WeBWorK docs and wiki links, for example:
	https://openwebwork.github.io/pg-docs/...
	https://webwork.maa.org/wiki/...
	https://courses1.webwork.maa.org/webwork2/...

Input:
- One URL per line.

Output:
- One simplified HTML file per URL.
- Filenames are deterministic and do not include hex hashes.
- URL order is shuffled by default.
- Between pages: time.sleep(random.random())

ASCII only. No Unicode punctuation.
"""

import argparse
import html
import random
import re
import time
from pathlib import Path
from urllib.parse import parse_qsl, urlparse

from playwright.sync_api import sync_playwright


#============================================

def parse_args() -> argparse.Namespace:
	"""Parse command-line arguments."""
	parser = argparse.ArgumentParser(
		description="Render Insight and WeBWorK pages and save text-focused HTML."
	)

	parser.add_argument(
		"-i",
		"--input",
		dest="input_file",
		required=True,
		help="URL list file (one URL per line)",
	)

	parser.add_argument(
		"-o",
		"--output-dir",
		dest="output_dir",
		required=True,
		help="Output directory",
	)

	parser.add_argument(
		"-p",
		"--profile-dir",
		dest="profile_dir",
		default="pw-profile",
		help="Playwright persistent profile directory",
	)

	parser.add_argument(
		"--headed",
		dest="headed",
		action="store_true",
		help="Show the browser window",
	)

	parser.add_argument(
		"--login",
		dest="login",
		action="store_true",
		help="Open a headed browser to establish cookies/session, then exit",
	)

	parser.add_argument(
		"--shuffle",
		dest="shuffle",
		action="store_true",
		help="Shuffle URL order (default)",
	)

	parser.add_argument(
		"--no-shuffle",
		dest="shuffle",
		action="store_false",
		help="Do not shuffle URL order",
	)
	parser.set_defaults(shuffle=True)

	return parser.parse_args()


#============================================

def read_urls(input_file: str) -> list[str]:
	"""Read URLs from a file, ignoring blank lines and comments."""
	urls: list[str] = []
	for raw in Path(input_file).read_text(encoding="utf-8").splitlines():
		line = raw.strip()
		if not line:
			continue
		if line.startswith("#"):
			continue
		urls.append(line)
	return urls


#============================================

def safe_token(text: str) -> str:
	"""Convert text into a filename-safe token."""
	out = re.sub(r"[^A-Za-z0-9._-]+", "-", text).strip("-")
	if not out:
		out = "page"
	return out


#============================================

def make_basename(url: str) -> str:
	"""
	Make a deterministic basename for a URL without hashes.

	Strategy:
	- Prefer the final path segment.
	- Include a short host tag to reduce cross-site collisions.
	- Include a compact query token for important keys (stable sort).
	"""
	parsed = urlparse(url.strip())
	host = parsed.netloc.lower()
	host_tag = host.split(":")[0]
	host_tag = safe_token(host_tag.replace(".", "-"))

	path = parsed.path.rstrip("/")
	leaf = path.split("/")[-1] if path else "index"
	leaf = safe_token(leaf)

	query_items = parse_qsl(parsed.query, keep_blank_values=True)
	if query_items:
		query_items.sort()
		parts: list[str] = []
		for k, v in query_items:
			k_tok = safe_token(k)[:24]
			if v:
				v_tok = safe_token(v)[:24]
				parts.append(f"{k_tok}_{v_tok}")
			else:
				parts.append(k_tok)
		query_tok = "__" + "__".join(parts)[:120]
	else:
		query_tok = ""

	return f"{host_tag}__{leaf}{query_tok}"


#============================================

def uniquify_path(path: Path) -> Path:
	"""If path exists, append _2, _3, ... (no hashes)."""
	if not path.exists():
		return path

	stem = path.stem
	suffix = path.suffix
	parent = path.parent

	i = 2
	while True:
		candidate = parent / f"{stem}_{i}{suffix}"
		if not candidate.exists():
			return candidate
		i += 1


#============================================

def html_template(title_text: str, source_url: str, meta_text: str, body_html: str) -> str:
	"""Wrap extracted content in a minimal readable HTML scaffold."""
	title_esc = html.escape(title_text, quote=True)
	url_esc = html.escape(source_url, quote=True)
	meta_esc = html.escape(meta_text, quote=False)

	out = ""
	out += "<!doctype html>\n"
	out += "<html lang=\"en\">\n"
	out += "<head>\n"
	out += "\t<meta charset=\"utf-8\">\n"
	out += f"\t<title>{title_esc}</title>\n"
	out += "\t<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
	out += "\t<style>\n"
	out += "\t\tbody { max-width: 900px; margin: 2rem auto; padding: 0 1rem; }\n"
	out += "\t\tbody { font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; }\n"
	out += "\t\tpre, code { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }\n"
	out += "\t\tpre { overflow-x: auto; padding: 0.75rem; border: 1px solid #ddd; }\n"
	out += "\t\tblockquote { border-left: 4px solid #ddd; padding-left: 1rem; color: #444; }\n"
	out += "\t\t.meta { color: #555; font-size: 0.95rem; margin: 0.75rem 0 1.25rem 0; }\n"
	out += "\t\t.source { color: #555; font-size: 0.95rem; margin-bottom: 0.25rem; }\n"
	out += "\t</style>\n"
	out += "</head>\n"
	out += "<body>\n"
	out += f"\t<h1>{title_esc}</h1>\n"
	out += f"\t<div class=\"source\">Source: <a href=\"{url_esc}\">{url_esc}</a></div>\n"
	if meta_text:
		out += f"\t<div class=\"meta\">{meta_esc}</div>\n"
	out += body_html + "\n"
	out += "</body>\n"
	out += "</html>\n"
	return out


#============================================

def open_persistent_context(playwright, profile_dir: str, headed: bool):
	"""Open a Playwright persistent context (Firefox)."""
	profile_path = str(Path(profile_dir))
	ctx = playwright.firefox.launch_persistent_context(
		user_data_dir=profile_path,
		headless=not headed,
	)
	return ctx


#============================================

def login_mode(ctx) -> None:
	"""Open a headed browser for manual checks, then exit."""
	page = ctx.new_page()
	page.goto("https://commons.libretexts.org/insight/welcome", wait_until="domcontentloaded")
	print("Browser opened. Complete any normal checks, then close the window.")
	print("Return here and press Enter.")
	input()
	page.close()


#============================================

def extract_insight(page) -> tuple[str, str, str]:
	"""Extract content from LibreTexts Insight pages."""
	title_sel = "p.text-4xl.font-semibold"
	meta_sel = "p.text-sm.text-gray-500"
	desc_sel = "p.max-w-6xl"
	body_sel = "div.prose"

	page.wait_for_load_state("domcontentloaded")
	page.wait_for_selector(body_sel)

	title_text = (page.eval_on_selector(title_sel, "el => el.textContent || ''") or "").strip()
	if not title_text:
		title_text = (page.title() or "").strip() or "Untitled"

	meta_text = ""
	meta_nodes = page.query_selector_all(meta_sel)
	if meta_nodes:
		meta_text = (meta_nodes[0].text_content() or "").strip()

	body_html = ""
	desc_nodes = page.query_selector_all(desc_sel)
	if desc_nodes:
		body_html += desc_nodes[0].evaluate("el => el.outerHTML") + "\n"

	body_nodes = page.query_selector_all(body_sel)
	body_html += body_nodes[0].evaluate("el => el.outerHTML")

	return title_text, meta_text, body_html


#============================================

def first_existing_selector(page, selectors: list[str]) -> str:
	"""Return the first selector that matches at least one element."""
	for sel in selectors:
		node = page.query_selector(sel)
		if node:
			return sel
	return ""


#============================================

def extract_webworkish(page, url: str) -> tuple[str, str, str]:
	"""
	Extract content for common WeBWorK-related sites.

	openwebwork.github.io (mkdocs): prefer article, then main, then md-content.
	webwork.maa.org/wiki (MediaWiki): prefer #mw-content-text.
	courses1.webwork.maa.org/webwork2: prefer common problem container, else main/body.
	"""
	parsed = urlparse(url)
	host = parsed.netloc.lower()

	page.wait_for_load_state("domcontentloaded")

	title_text = (page.title() or "").strip() or "Untitled"
	meta_text = ""

	if host.endswith("webwork.maa.org"):
		title_sel = "#firstHeading"
		body_sel = "#mw-content-text"
		if page.query_selector(title_sel):
			title_text = (page.eval_on_selector(title_sel, "el => el.textContent || ''") or "").strip()
		if page.query_selector(body_sel):
			body_html = page.eval_on_selector(body_sel, "el => el.outerHTML")
			return title_text, meta_text, body_html

	if host.endswith("openwebwork.github.io"):
		body_sel = first_existing_selector(page, ["article", "main", "div.md-content", "div#content"])
		if body_sel:
			body_html = page.eval_on_selector(body_sel, "el => el.outerHTML")
			return title_text, meta_text, body_html

	if "webwork2" in parsed.path:
		body_sel = first_existing_selector(
			page,
			[
				"#problemMainForm",
				"#problemContent",
				"main",
				"body",
			],
		)
		if body_sel:
			body_html = page.eval_on_selector(body_sel, "el => el.outerHTML")
			return title_text, meta_text, body_html

	body_sel = first_existing_selector(page, ["main", "article", "body"])
	if body_sel:
		body_html = page.eval_on_selector(body_sel, "el => el.outerHTML")
		return title_text, meta_text, body_html

	body_html = page.evaluate("() => document.body ? document.body.innerHTML : ''")
	return title_text, meta_text, body_html


#============================================

def extract_page(page, url: str) -> tuple[str, str, str]:
	"""Dispatch extraction based on URL."""
	if "commons.libretexts.org" in url and "/insight/" in url:
		return extract_insight(page)
	return extract_webworkish(page, url)


#============================================

def main() -> None:
	"""Program entry point."""
	args = parse_args()

	output_dir = Path(args.output_dir)
	output_dir.mkdir(parents=True, exist_ok=True)

	urls = read_urls(args.input_file)
	if not urls:
		raise ValueError("No URLs found in input file.")

	if args.shuffle:
		random.shuffle(urls)

	log_path = output_dir / "render_log.tsv"
	if not log_path.exists():
		log_path.write_text("url\tstatus\toutput_file\ttitle\n", encoding="utf-8")

	with sync_playwright() as p:
		ctx = open_persistent_context(p, args.profile_dir, args.headed or args.login)

		if args.login:
			login_mode(ctx)
			ctx.close()
			return

		page = ctx.new_page()

		for url in urls:
			base = make_basename(url)
			out_path = uniquify_path(output_dir / f"{base}.html")

			try:
				page.goto(url, wait_until="domcontentloaded")
				title_text, meta_text, body_html = extract_page(page, url)
				final_html = html_template(title_text, url, meta_text, body_html)
				out_path.write_text(final_html, encoding="utf-8")
				status = "OK"
				title_log = title_text
				print(f"Saved {url} -> {out_path.name}")
			except Exception as exc:
				status = "FAIL"
				title_log = f"{type(exc).__name__}: {exc}"
				print(f"Failed {url} -> {title_log}")

			line = url + "\t" + status + "\t" + out_path.name + "\t" + title_log.replace("\t", " ") + "\n"
			with log_path.open("a", encoding="utf-8") as f:
				f.write(line)

			time.sleep(random.random())

		page.close()
		ctx.close()


if __name__ == "__main__":
	main()
