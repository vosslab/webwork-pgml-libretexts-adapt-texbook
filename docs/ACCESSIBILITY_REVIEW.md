# Accessibility review

Rules for accessible content in LibreTexts textbook HTML files. These rules derive
from the
[LibreTexts Construction Guide](Sources/Construction_Guide_for_LibreTexts_2e/)
accessibility checklist and WCAG conventions.

## Images

- Every `<img>` must have a meaningful `alt` attribute.
- Keep alt text under 150 characters. Use a caption for longer descriptions.
- Mark purely decorative images as `alt=""` so screen readers skip them.
- Use PNG, JPG, or GIF. Never use BMP; avoid TIFF.
- Set image size to "responsive" so it adapts to screen width.
- Do not hotlink images from external servers. Upload originals to LibreTexts.

Reference:
[Sources/Construction_Guide_for_LibreTexts_2e/00008.2_Adding_Images_and_Figures.txt](Sources/Construction_Guide_for_LibreTexts_2e/00008.2_Adding_Images_and_Figures.txt)

## Links

- No empty links (`<a href="..."></a>`).
- No suspicious link text ("click here", "here", "link", "read more").
- External URLs must be labeled with their destination, not left as raw URLs.
- Internal links use `/@go/page/{pageID}` with the section title as link text.
  See [docs/LINKING_AND_SECTION_NUMBERING.md](docs/LINKING_AND_SECTION_NUMBERING.md).

Reference:
[Sources/Construction_Guide_for_LibreTexts_2e/00005.3.6_Accessibility_Review.txt](Sources/Construction_Guide_for_LibreTexts_2e/00005.3.6_Accessibility_Review.txt)

## Color contrast

- Text 18pt and smaller: minimum 4.5:1 contrast ratio against the background.
- Text over 18pt: minimum 3:1 contrast ratio.
- Graphical links and buttons: minimum 3:1 contrast ratio.
- Never rely on color alone to convey meaning. Pair color with bold, italics, or labels.

LibreTexts platform colors already meet these ratios on white backgrounds
(link color `#0372a6` gives 5.3:1). Custom background colors in this textbook use
light pastels with black text, which exceed the 4.5:1 threshold.

Reference:
[Sources/Construction_Guide_for_LibreTexts_2e/00015.1_Color_Codes_and_Contrasts.txt](Sources/Construction_Guide_for_LibreTexts_2e/00015.1_Color_Codes_and_Contrasts.txt)

## Text and typography

- All text must be larger than 10pt.
- Line height: at least 1.5 times the font size.
- Paragraph spacing: at least 2 times the font size.
- Letter spacing: at least 0.12 times the font size.
- Word spacing: at least 0.16 times the font size.

This textbook does not set font sizes or spacing in its HTML. LibreTexts platform CSS
provides accessible defaults for all of these.

Reference:
[Sources/Construction_Guide_for_LibreTexts_2e/00005.3.6_Accessibility_Review.txt](Sources/Construction_Guide_for_LibreTexts_2e/00005.3.6_Accessibility_Review.txt)

## Headings

- No empty headings.
- Maintain a logical heading outline (no skipped levels).
- Start each page with `<h2>` (the page title is the `<h1>`).
- Do not use bold `<p>` tags as visual headers. Use proper `<h3>` or `<h4>` elements.

## Tables

- Every table must have column headers (`<th>` elements in a `<thead>`).
- Add row headers where applicable.
- Use the `data-th` attribute on `<td>` elements for responsive display.
- Every `<table>` must have a `<caption>` as its first child element.
  Captions should be descriptive sentence fragments ending with a period (30–80 chars).
- Add a table caption or describe the table in surrounding text.
- Never embed a table as an image.
- Use the LibreTexts "Make table responsive" class (`mt-responsive-table`).

Reference:
[Sources/Construction_Guide_for_LibreTexts_2e/00008.4_Adding_Tables.txt](Sources/Construction_Guide_for_LibreTexts_2e/00008.4_Adding_Tables.txt)

## Lists

- Use `<ol>` for ordered lists and `<ul>` for unordered lists.
- Do not fake lists with manual numbering or line breaks.

## Forms and interactive elements

- Every form field must have a `<label>`.
- Radio buttons and checkboxes must be keyboard-navigable.
- Instructions must not rely solely on shape, color, size, or visual location.

## Multimedia

- Videos must have captions.
- Video player controls must be navigable via keyboard.
- Audio content needs a transcript or media alternative.

## Navigation

- All content must be accessible via keyboard alone.
- Prefer semantic HTML (`<section>`, `<nav>`, `<article>`) over generic `<div>` tags.
- Time-limited interactions must meet accessibility timing criteria.

## Code blocks

- Use `<pre>` for code examples.
- Include alt text or surrounding descriptions for code that would be opaque to
  screen readers (e.g., ASCII diagrams).

## Built-in accessibility checker

The LibreTexts CKEditor includes an accessibility checker that tests 8 categories:
headings, image alt tags, tables, links, color contrast, labels, abbreviations, and
general issues. Run it before publishing any page.

Reference:
[Sources/Construction_Guide_for_LibreTexts_2e/00008.7_Accessibility_Checking.txt](Sources/Construction_Guide_for_LibreTexts_2e/00008.7_Accessibility_Checking.txt)

## Current textbook status

As of 2026-02-27, all 66 HTML files pass the following accessibility checks:
- Zero `<img>` tags (no images used).
- Zero empty links.
- Zero suspicious link text.
- Zero empty headings.
- All 129 tables have `<thead>` with `<th>` headers and `data-th` attributes.
- All 129 tables have `<caption>` elements (120 added via `tools/add_table_captions.py`,
  9 already present in Chapter 8).
- No bold `<p>` pseudo-headers remain (89 converted to `<h3>`/`<h4>` via
  `tools/fix_pseudo_headers.py`).
- No inline font sizing or spacing overrides.
- All color usage (inline styles) is inside `<pre>` code examples or section-label
  headings. Background colors are light pastels with black text.

## Automated verification

```bash
# HTML lint (checks structure, nesting, required attributes)
bash tests/run_html_lint.sh

# Check for empty links
grep -rn '<a [^>]*>\s*</a>' Textbook/

# Check for suspicious link text
grep -rni '>click here<\|>here<\|>link<\|>read more<' Textbook/

# Check for empty headings
grep -rn '<h[1-6][^>]*>\s*</h[1-6]>' Textbook/

# Check for tables missing headers
# (compare table count to thead count -- should be equal)
grep -rcn '<table' Textbook/ | awk -F: '{s+=$2} END{print "tables:",s}'
grep -rcn '<thead' Textbook/ | awk -F: '{s+=$2} END{print "theads:",s}'

# Check for tables missing captions (counts should match)
grep -rcn '<table' Textbook/ | awk -F: '{s+=$2} END{print "tables:",s}'
grep -rcn '<caption' Textbook/ | awk -F: '{s+=$2} END{print "captions:",s}'

# Check for pseudo-headers (bold paragraphs used as visual headers)
grep -rn '<p><strong>Line notes</strong></p>' Textbook/
grep -rn '<p><strong>Common failure and fix</strong></p>' Textbook/
grep -rn '<p style="background-color.*"><strong>.*</strong></p>' Textbook/
grep -rn '<p><strong>Wrong:</strong></p>' Textbook/
```
