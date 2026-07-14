#!/usr/bin/env node
/** Capture the published handbook landing page for README documentation. */

import assert from "node:assert/strict";
import { mkdirSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { chromium } from "playwright";

const HANDBOOK_URL =
  "https://chem.libretexts.org/Courses/Remixer_University/The_ADAPT_WeBWorK_Handbook";
const DESKTOP_USER_AGENT =
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) " +
  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36";
const repoRoot = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
);
const outputPath =
  process.argv[2] ??
  path.join(repoRoot, "docs", "screenshots", "published_handbook.png");

mkdirSync(path.dirname(outputPath), { recursive: true });

const browser = await chromium.launch();
try {
  const page = await browser.newPage({
    colorScheme: "light",
    locale: "en-US",
    userAgent: DESKTOP_USER_AGENT,
    viewport: { width: 1440, height: 900 },
  });
  await page.goto(HANDBOOK_URL, { waitUntil: "domcontentloaded" });

  await page.locator("body").waitFor({ state: "visible" });
  assert.match(await page.title(), /The ADAPT WeBWorK Handbook/);

  await page.screenshot({
    animations: "disabled",
    path: outputPath,
  });
  console.log(`Screenshot saved: ${outputPath}`);
} finally {
  await browser.close();
}
