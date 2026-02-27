# Linking and section numbering

Rules for cross-references and navigation links in LibreTexts textbook HTML files.
These rules derive from the
[LibreTexts Construction Guide](Sources/Construction_Guide_for_LibreTexts_2e/)
and project-specific conventions.

## Internal links use page IDs, not URLs

LibreTexts assigns every page a stable numeric page ID. Use the `/@go/page/{pageID}`
form for all internal cross-references:

```html
<a href="/@go/page/555715">Multiple Choice</a>
```

The page ID survives reorganization, renaming, and remixing. A full URL does not.

Reference:
[Sources/Construction_Guide_for_LibreTexts_2e/00008.5_Hyperlinking.txt](Sources/Construction_Guide_for_LibreTexts_2e/00008.5_Hyperlinking.txt)

## Link text uses titles, never section numbers

Section numbers (e.g., "2.4", "Section 5.2", "Chapter 6") are dynamic. LibreTexts
reassigns them automatically when the book is reorganized
([Sources/Construction_Guide_for_LibreTexts_2e/00008.8_Page_Titles.txt](Sources/Construction_Guide_for_LibreTexts_2e/00008.8_Page_Titles.txt)).
There is no mechanism for dynamic section numbering in link text, so any number
written into an `<a>` tag becomes stale after a reorder.

Rules:
- Link text is always the section title: `<a href="/@go/page/555715">Multiple Choice</a>`
- Never use "Section X.Y", "Chapter X", or bare "X.Y" as link text.
- Never add a parenthetical section number after a link: `</a> (Section 5.2)`.
- If plain text references a section by number without a link, convert it to a proper
  `<a>` tag with the title as link text.

## External links

Avoid linking outside LibreTexts unless necessary. When an external link is required,
point to a stable URL and use descriptive link text.

Reference:
[Sources/Construction_Guide_for_LibreTexts_2e/00008.5_Hyperlinking.txt](Sources/Construction_Guide_for_LibreTexts_2e/00008.5_Hyperlinking.txt)

## Page title format

LibreTexts page titles follow the format `XX.YY: Title`. The platform uses the title
for automatic figure, table, and equation numbering. Colons within a title are
converted to dashes.

Reference:
[Sources/Construction_Guide_for_LibreTexts_2e/00008.8_Page_Titles.txt](Sources/Construction_Guide_for_LibreTexts_2e/00008.8_Page_Titles.txt)

## Anchors for within-page links

Headings are automatically set as section anchors. Additional anchors can be placed
next to equations, images, tables, or other targets. Use the "Jump to anchor or
section" selector in the link dialog to reference them.

Reference:
[Sources/Construction_Guide_for_LibreTexts_2e/00008.5_Hyperlinking.txt](Sources/Construction_Guide_for_LibreTexts_2e/00008.5_Hyperlinking.txt)

## Accessibility requirements for links

The LibreTexts accessibility review checks links for:
- No empty links (`<a href="..."></a>`).
- No suspicious link text ("click here", "here", "link", "read more").
- External URLs labelled with their destination, not raw URLs.

Reference:
[Sources/Construction_Guide_for_LibreTexts_2e/00005.3.6_Accessibility_Review.txt](Sources/Construction_Guide_for_LibreTexts_2e/00005.3.6_Accessibility_Review.txt),
[Sources/Construction_Guide_for_LibreTexts_2e/00008.7_Accessibility_Checking.txt](Sources/Construction_Guide_for_LibreTexts_2e/00008.7_Accessibility_Checking.txt)

## Page ID lookup

The CSV file `Textbook/The_ADAPT_WeBWorK_Handbook.reremix.csv` maps every page ID to
its section number and title. The automated tool `tools/fix_section_links.py` reads
this CSV and replaces numeric link text with titles across all HTML files.

Usage:

```bash
python3 tools/fix_section_links.py           # dry-run (preview changes)
python3 tools/fix_section_links.py --apply   # write changes to files
```

## What not to change

- Self-references within the same chapter used as prose ("Chapter 4 is a single worked
  problem...").
- Code examples inside `<pre>` blocks.
- Narrative mentions not intended as navigation ("Chapter 2 exists because...").
