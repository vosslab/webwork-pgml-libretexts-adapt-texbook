# LibreTexts HTML guide

This doc captures the minimal HTML patterns to use in `Textbook/` so the content imports cleanly
into LibreTexts and remains maintainable.

## Core rules
- LibreTexts supports hyperlinks; prefer linking within the LibreTexts library and avoid linking
  outside the library unless necessary (to reduce "link farming").
- Do not use link text like "click here" or raw pasted URLs; use short, unique, descriptive link
  text.
- Avoid relative file links (like `href="1.2-Page.html"`); use full URLs, site-relative `/...`
  paths, or add internal links in LibreTexts after import.
- Do not use JavaScript; avoid `<script>` tags and inline event handler attributes (like
  `onclick=`).
- Prefer simple, semantic HTML: `p`, `h2`, `h3`, `ul`, `ol`, `li`, `code`, `pre`, and tables for
  real tabular data.

## Headings
- LibreTexts reserves `h1` for the page title; do not use `<h1>` in the body.
- Start body headings at `<h2>`, then use `<h3>` for subsections.
- Do not leave empty headings (headings should always have text).

## Editing in LibreTexts
- Use "Show blocks" in the editor to debug odd nesting or spacing before editing raw HTML.
- Use the `</>` HTML/source view sparingly for targeted fixes (prefer simple HTML that round-trips
  cleanly).

## Index pages (X.0-Index.html)
Every chapter index page named like `X.0-Index.html` must end with this line so LibreTexts shows
the generated list of subsections:

```html
<p>{{template.ShowOrg()}}</p>
```

If you see template lines or article-type/tag lines at the top of a LibreTexts page, do not
remove them; they control how the page is stored and rendered.

LibreTexts pulls the listing text for directory-style pages from the page Summary field (in Page
Settings), so keep summaries short and useful.

## Titles and ordering
- In LibreTexts, titles and URLs are coupled, so keep numbering consistent.
- Use zero-padded numbering in titles when you need stable lexicographic ordering (for example,
  `02.1: ...` so `10.*` does not sort ahead of `2.*`).

## Tables (the standard format)
Use LibreTexts responsive tables so the content remains readable on narrow screens and accessible
to assistive technologies.

### Requirements
- Use `class="mt-responsive-table"` on the `<table>`.
- Use `<thead>` and `<tbody>`.
- In each `<td>`, include a `data-th="Header name"` attribute matching the column header text.
- Prefer a `<colgroup>` with explicit widths when you want consistent column sizing.
- Do not use `border=`, `cellpadding=`, or `cellspacing=` attributes.
- Add a `<caption>` for tables (and if the table is complex, add a short lead-in paragraph
  describing what the reader should take from it).
- Avoid merged "mega tables" that cannot be made accessible (if you need multiple header rows or
  complex spanning, split into smaller tables).

### Template
```html
<table class="mt-responsive-table">
	<caption>Short, descriptive caption.</caption>
	<colgroup>
		<col style="width: 22%;">
		<col style="width: 39%;">
		<col style="width: 39%;">
	</colgroup>
	<thead>
		<tr>
			<th>Format</th>
			<th>Best for</th>
			<th>Tradeoffs</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td data-th="Format">WeBWorK (PGML-first)</td>
			<td data-th="Best for">...</td>
			<td data-th="Tradeoffs">...</td>
		</tr>
	</tbody>
</table>
```

## Images
- Provide meaningful `alt` text for non-decorative images; do not use filenames as `alt` text.
- If an image is decorative, use `alt=""` (and do not repeat the same information in nearby
  text).
- Keep `alt` text under ~150 characters; if more detail is needed, use a visible caption or a
  nearby paragraph.

## Embedded media
- Avoid embedding media that depends on JavaScript.
- For videos, include a short caption and include the source URL in the caption text.

## Validation
- Run `tests/run_html_lint.sh` after editing textbook HTML.
