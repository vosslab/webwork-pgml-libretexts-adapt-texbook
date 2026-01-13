# Reading JSON map file

This doc explains how to read a LibreTexts "Remixer map" JSON file (like
`Textbook/Using_WeBWork_in_ADAPT-Map.json`) and extract a mapping from a section label to a
LibreTexts `page_id`.

## What you are extracting

Each node in the map typically has:

- `title`: a human-facing label like `6.4: The Laws of Thermodynamics`
- `data.id`: the LibreTexts page id (for example `555880`)

That `title` + `data.id` pair is the mapping you want:

- `label` -> `page_id`

This is enough to build stable LibreTexts links like `/@go/page/<page_id>` later without
hand-copying ids.

## Map structure (high level)

The map JSON is a nested tree.

- The root object usually contains a `RemixTree` object.
- Each tree node is a dict with keys like `title`, `data`, and `children`.
- `children` is a list of more nodes (subsections/pages).

In practice, you can parse the file, take `root["RemixTree"]` as the starting node, and then walk
recursively through `children`.

## How section labels are split

When the `title` starts with a section number prefix like `X.Y: ...`, split it into:

- `section_number`: `X.Y` (for example `6.4`)
- `section_title`: the remainder (for example `The Laws of Thermodynamics`)

If the title does not match that pattern, leave `section_number` blank and put the full text into
`section_title`.

## Script: JSON map to CSV mapping

Use `tools/libretexts_map_json_to_page_id_csv.py` to walk a LibreTexts map JSON and write a CSV
mapping.

Example (repo default input and output):

`/opt/homebrew/opt/python@3.12/bin/python3.12 tools/libretexts_map_json_to_page_id_csv.py`

By default, the script names the output file by changing the input extension to `.csv`.

Example (explicit input/output):

`/opt/homebrew/opt/python@3.12/bin/python3.12 tools/libretexts_map_json_to_page_id_csv.py -i Textbook/Using_WeBWork_in_ADAPT-Map.json -o page_id_map.csv`

The CSV includes at least (first column is `page_id`):

- `page_id`: the `data.id` value as a string
- `label`: the original `title` text from the map

It also records additional fields (when present) that are useful for debugging or later
rewriting:

- `section_number`, `section_title`
- `url`, `relativePath`, `padded`, `parentID`, `parent_title`

Notes:

- If the parsed `section_title` starts with `_` (for example `01:_TitlePage`), the script strips
  the leading underscore in `section_title` (the original `label` is unchanged).
- Root nodes often have `parentID = 0`; the script writes that as blank.

## If you already have a CSV and want a lookup dict

Read the CSV created by the script and build a dict keyed by the display label:

```python
import csv

title_to_id: dict[str, str] = {}
with open("page_id_map.csv", newline="", encoding="utf-8") as handle:
	for row in csv.DictReader(handle):
		title_to_id[row["label"]] = row["page_id"]
```
