# Mining Report: biology-problems-website

## Repo Overview

The biology-problems-website repo builds and deploys the MkDocs-based website at biologyproblems.org. It is the public-facing distribution hub for the Biology Problems OER project, providing downloadable question sets (BBQ text, Blackboard Ultra QTI v2.1, and Canvas/ADAPT QTI v1.2) organized by subject and topic, along with LMS import tutorials and interactive daily puzzles. The site is authored by Dr. Neil Voss (Roosevelt University) and funded by an Illinois State Library OER Grant titled "Dynamic and Sharing-Resistant OER Problem Sets for Biochemistry and Genetics" (2024-2026).

The repo contains: (1) site content under site_docs/ covering five subjects (Biochemistry, Genetics, Laboratory, Molecular Biology, Biostatistics), (2) three LMS import tutorials (Blackboard Learn, Blackboard Ultra, Canvas), (3) three interactive daily puzzles (Peptidyle, Deletion Mutants, Mutant Screen), (4) Python scripts for generating topic pages and subject indexes, (5) a BBQ batch runner system for bulk question set generation, and (6) an LLM-assisted problem set title generator. The site uses the Material for MkDocs theme with CC BY-SA 4.0 licensing.

## Content Found

### LMS Import Tutorials (site_docs/tutorials/)
- **Blackboard Learn BBQ Text File Upload** (bbq_tutorial.md): Detailed 5-part walkthrough with 35 annotated screenshots covering pool creation, BBQ text upload, test building, random block configuration, and student availability settings.
- **Blackboard Ultra QTI .zip Import Guide** (bbq_ultra_tutorial.md): 2-part tutorial with 12 annotated screenshots covering QTI 2.1 package import and quiz creation from question banks.
- **Canvas QTI .zip Import Guide** (canvas_tutorial.md): 3-part tutorial with screenshots covering QTI .zip import, question bank renaming, and randomized quiz creation using question groups.
- **Planned but not yet written**: LibreTexts ADAPT QTI v1.2 Question Import Guide.

### Subject Coverage (site_docs/)
- **Biochemistry**: 11 topics (Life Molecules through Human Senses), each with LibreTexts chapter links and downloadable question sets in three formats.
- **Genetics**: 11 topics (Genetic Disorders through Gene Trees), each with LibreTexts chapter links and downloadable question sets.
- **Laboratory**: 4 topics (Measurement Basics, Solutions, Dilutions, Serial Dilutions).
- **Molecular Biology**: Index page only, limited content.
- **Biostatistics**: Index page only, limited content.

### Topics Metadata (topics_metadata.yml)
- Structured YAML mapping of all subjects and topics with descriptions and LibreTexts URLs.
- Biochemistry and Genetics topics link to Roosevelt University LibreTexts courses.

### Question Set Distribution
- Each topic page provides download buttons for three formats: Blackboard Learn TXT, Blackboard Ultra QTI v2.1, and Canvas/ADAPT QTI v1.2.
- Human-readable HTML previews are also available.
- Problem set titles follow a structured naming guide (docs/GUIDE_TO_NAMING_PROBLEM_SETS.md).

### BBQ Batch Runner System (bbq_control/)
- CSV-driven task runner for bulk question set generation.
- Supports YMATCH, YMCS, YMMS script aliases for matching sets and multiple choice.
- Auto-detects output filenames and moves them into the correct site_docs topic folders.
- Sync mode regenerates outputs only when inputs change.

### Daily Puzzles (site_docs/daily_puzzles/)
- **Peptidyle**: Wordle-style game where students identify a pentapeptide sequence from its molecular structure.
- **Deletion Mutants**: Drosophila deletion mutant puzzle for gene ordering.
- **Mutant Screen**: Neurospora auxotroph puzzle based on Beadle and Tatum experiments.

### Page Generation Pipeline (flow_for_html_generation.txt)
- Documents the full workflow: obtain topic title from mkdocs.yml, get descriptions, identify BBQ files, convert to HTML, generate LLM titles, add download links, and include HTML in topic pages.

## Chapter Mapping

### Chapter 1: Introduction
- **Relevant content**: The site's index.md and author.md provide context about the OER project, its scope (biochemistry, genetics, molecular biology, biostatistics, laboratory), and its funding through the Illinois State Library OER Grant. The CC BY-SA 4.0 licensing information is clearly documented.
- **Textbook gap it fills**: Provides real-world context for what the WeBWorK/ADAPT ecosystem produces and why -- OER problem sets for biology education. The grant information connects to the broader LibreTexts ADAPT integration goals.

### Chapter 5: Different Question Types
- **Relevant content**: The topic pages demonstrate multiple question types in practice: MATCH (matching sets), MC (multiple choice), and various problem set structures. The BBQ batch runner's script aliases (YMATCH, YMCS, YMMS) enumerate the question generation patterns. The naming guide (GUIDE_TO_NAMING_PROBLEM_SETS.md) shows how problem sets are organized by concept rather than question type.
- **Textbook gap it fills**: Provides concrete examples of how different question types look when deployed on a real website. The download buttons show the three output formats (BBQ text, QTI v2.1, QTI v1.2) which directly maps to the textbook's coverage of question formats and LMS compatibility.

### Chapter 8: Using AI Agents (placeholders)
- **Relevant content**: The repo uses LLM-assisted title generation (llm_generate_problem_set_title.py with llm_wrapper.py using ollama) and has a structured BBQ batch runner that could be extended with AI agents. The generate_topic_pages.py and generate_subject_indexes.py scripts automate content generation from metadata. The AGENTS.md file defines agent workflow rules.
- **Textbook gap it fills**: Demonstrates a practical use case for AI agents in question set development -- automating title generation and batch processing. This connects to the textbook's AI agent chapter by showing how LLMs can assist in educational content workflows.

### Cross-Chapter: LMS Integration Tutorials
- **Relevant content**: The three LMS tutorials (Blackboard Learn, Blackboard Ultra, Canvas) are highly detailed, screenshot-heavy guides that walk educators through question bank import and randomized test creation. The planned but unwritten LibreTexts ADAPT tutorial is a notable gap.
- **Textbook gap it fills**: These tutorials could serve as reference material or appendix content for the textbook's coverage of deploying WeBWorK/PGML problems through various LMS platforms. The missing ADAPT tutorial represents a direct opportunity for textbook content.

### Cross-Chapter: LibreTexts Integration
- **Relevant content**: topics_metadata.yml contains direct URLs to Roosevelt University LibreTexts chapters for both Biochemistry and Genetics. The Canvas/ADAPT QTI v1.2 download format explicitly supports ADAPT import.
- **Textbook gap it fills**: Demonstrates the end-to-end pathway from question creation to LibreTexts ADAPT deployment, which is central to the textbook's subject matter.

## Recommended Actions

1. **Reference the LMS tutorials as companion material**: The Blackboard Learn, Blackboard Ultra, and Canvas tutorials are high-quality, screenshot-annotated guides that complement the textbook's coverage of deploying questions through LMS platforms. Consider linking to biologyproblems.org/tutorials/ from the textbook.

2. **Fill the ADAPT tutorial gap**: The biology-problems-website lists a planned "LibreTexts ADAPT QTI v1.2 Question Import Guide" as an upcoming tutorial. Writing this tutorial could serve both the website and the textbook.

3. **Use question type examples from topic pages**: The topic pages (e.g., biochemistry/topic01) demonstrate how MATCH and MC question types look when packaged for download in multiple formats. These are concrete examples for Chapter 5.

4. **Document the LLM title generation workflow**: The llm_generate_problem_set_title.py script and its integration with ollama is a practical AI agent use case that maps directly to Chapter 8 content.

5. **Cross-reference the topics_metadata.yml LibreTexts URLs**: The structured mapping of topics to LibreTexts chapters could be referenced in the textbook to show how problem sets align with open textbook content.

6. **Note the BBQ batch runner as an automation example**: The bbq_control system demonstrates how question set generation can be automated at scale, relevant to both Chapter 5 (question types) and Chapter 8 (AI/automation workflows).

7. **Highlight the daily puzzles as engagement tools**: Peptidyle, Deletion Mutants, and Mutant Screen are interactive browser-based puzzles that showcase creative approaches to biology assessment beyond traditional question types.
