# Video transcript analysis

Analysis of the video transcript for Chapter 08 content planning.

## Video metadata

- **Title:** Writing WeBWorK PG Problems with AI Agents
- **URL:** https://youtube.com/watch?v=lfcJ3ALXEhk
- **Speaker:** Biology instructor adapting Blackboard questions to ADAPT/WeBWorK format
- **Duration:** approximately 11 minutes 44 seconds
- **Date context:** References November 2025 as when AI coding agents transformed his workflow
- **Recording context:** Live demonstration with screen sharing, showing the PG renderer,
  ChatGPT, Codex, and Claude Code in real time

## Timeline overview

| Timestamp | Topic | Section |
| --- | --- | --- |
| 00:00-01:15 | Introduction and motivation: adapting biology homework | 8.0 |
| 01:15-01:35 | AI coding agents and vibe coding since Nov 2025 | 8.1 |
| 01:35-03:05 | ChatGPT fails at WeBWorK: live demo | 8.1 |
| 03:05-03:30 | Why ChatGPT fails: PG looks like Perl but is not | 8.2 |
| 03:30-04:15 | Introducing Codex and Claude Code as alternatives | 8.1 |
| 04:15-04:50 | Skills/prompts: the `webwork_writer` skill for Codex | 8.2 |
| 04:50-05:00 | Codex connects to the renderer to verify code | 8.3 |
| 05:00-06:10 | Complex example: amino acid isoelectric point question | 8.2 |
| 06:10-07:30 | Codex workflow: prompt, picture, skill, documents | 8.2, 8.4 |
| 07:30-08:35 | Reviewing and testing Codex output in the renderer | 8.3 |
| 08:35-09:10 | Claude Code: patience, guidance, and the debug loop | 8.4 |
| 09:10-10:10 | Comparing Claude and Codex output, adding color | 8.3, 8.4 |
| 10:10-11:00 | Randomization, pKa variation, anti-cheating strategy | 8.4 |
| 11:00-11:44 | Color accessibility, summary, and closing | 8.4 |

## Detailed topic sections

### [00:00-01:15] Introduction and motivation

- Speaker has a large collection of biology homework questions in Blackboard format
- Goal is to adapt them to LibreTexts ADAPT, which uses a WeBWorK-type format
- WeBWorK seems to be the best format for biology problems
- Needed a good sandbox tester for WeBWorK first
- Took the WeBWorK PG renderer, which installs via Docker
- Expanded and modernized the renderer for local use
- The renderer runs on localhost:3000
- Has a debug mode showing generated HTML for troubleshooting
- Debug mode is critical for the speaker and especially for AI agents
- **Maps to:** 8.0 (motivation for the chapter), 8.3 (renderer setup)

### [01:15-01:35] AI coding agents transform workflow

- Since November 2025, AI coding agents transformed how the speaker writes code
- "I really don't write computer code much anymore, but I program all day"
- Describes this as "vibe coding" taking over
- **Maps to:** 8.1 (what are AI agents, vibe coding concept)

### [01:35-03:05] ChatGPT fails at writing WeBWorK

- ChatGPT is "just literally terrible at writing WeBWorK questions"
- Live demo: asks ChatGPT 5.2 to write a simple favorite-color question
- ChatGPT adds nonsensical settings like `showPartialCorrectAnswers = 1` for a
  color question
- Pasting ChatGPT output into the renderer produces errors
- Going back and forth with ChatGPT eventually makes it claim your renderer is broken
- Claude Code "on the other hand actually pretty successful" even for this simple case
- The exact example (favorite color = blue, multiple choice radio buttons) exists
  online as the canonical PGML example
- Even though the example is on the internet, ChatGPT still cannot produce correct code
- On DuckDuckGo, the canonical example is hit number 9 for "PGML multiple choice example"
- **Maps to:** 8.1 (why chat-based LLMs fail, why agents are needed)

### [03:05-03:30] Why ChatGPT fails: PG vs. Perl confusion

- PG "is like Perl, but not quite"
- ChatGPT gets confused by all the Perl code on the internet
- Produces code with Perl syntax that is invalid in the PG environment
- Debugging AI-generated code is "the worst part of programming"
- "You're stuck debugging someone else's code"
- **Maps to:** 8.2 (why knowledge documents are essential)

### [03:30-04:15] Claude Code and Codex as alternatives

- Claude Code is "probably the best example" of a working AI agent for WeBWorK
- Codex also works but is "a little bit slower"
- Speaker demonstrates the Codex app with a WeBWorK Codex forum
- Both are AI agents (not just chat interfaces) that can take actions
- **Maps to:** 8.1 (comparing AI agents)

### [04:15-05:00] The `webwork_writer` skill and knowledge documents

- Speaker wrote a skill called `webwork_writer` invoked with a dollar sign command
- The skill provides the agent with documentation on how to write good WeBWorK questions
- The skill contains all the documents the agent needs
- The agent can also connect itself to the renderer to confirm its code works
- The agent is "obsessed with finding other files on my file system to use to cheat"
- Speaker tells the agent that all documents it needs are in the skill, so "please
  don't search my hard drive"
- **Maps to:** 8.2 (knowledge documents), 8.3 (connecting to renderer)

### [05:00-06:10] Complex example: amino acid isoelectric points

- Speaker was teaching isoelectric points of amino acids to students
- Students had trouble understanding pI (isoelectric point) from titration curves
- "I got like 50 glazed eyes looking back at me"
- Decided this would be a great question to add to ADAPT
- The question is two parts: (1) identify the amino acid charge state with zero
  net charge, (2) calculate the pI from pKa values
- Shows a hypothetical amino acid with three pKa values
- Question involves randomized amino acid structures with different charges
- Students add plus and minus charges to find net zero charge, then determine pI
- **Maps to:** 8.2 (writing detailed prompts), 8.4 (advanced question design)

### [06:10-07:30] Codex workflow for the complex question

- Speaker wrote a detailed prompt and gave it to Codex (not ChatGPT)
- The repo is empty / fresh project, but has knowledge documents loaded via skill
- ChatGPT wants to use its own random function, which is wrong for WeBWorK
- WeBWorK has its own randomization system that must be used
- Speaker gave Codex: the prompt, a picture/screenshot, and told it to load the skill
- Instructed Codex that all needed documents are in the skill
- Codex created a new problem file and a changelog entry
- Codex ran the local renderer and found problems, then debugged them itself
- "I don't want to have to debug all that. Let it do it."
- **Maps to:** 8.2 (knowledge documents), 8.4 (workflow tips)

### [07:30-08:35] Testing and verifying Codex output

- Pastes Codex final code back into the local renderer
- The code properly tags the question with metadata
- The rendered question works and the speaker scores 100%
- The charge state choices are "a little bit harder to read" without color
- The correct pI answer is around 3.2
- Graph options in WeBWorK are limited; some classic ways use LaTeX
- Meanwhile Claude Code is still working on its version (launched 15 minutes prior)
- Claude asks permission to run the renderer, adding 15-20 minutes to the process
- **Maps to:** 8.3 (testing in the renderer)

### [08:35-09:10] Claude Code: patience and the debug loop

- "You have to have patience when working with these AI things"
- Claude Code launched 15 minutes ago, came back and asked questions, still "tinkering"
- "It's better for it to sit there and struggle getting the problem correct than me
  sitting there to struggle"
- Claude is sending the problem to the local renderer to verify
- Speaker knows where Claude is stuck, considers giving it guidance
- Tells Claude to re-read the skill documentation
- Speaker has a document on "how to render HTML correctly" and "PG common pitfalls"
- **Maps to:** 8.4 (debug loop, giving guidance to agents)

### [09:10-10:10] Comparing outputs and adding color

- Claude Code finally produces a testable file
- Claude's version renders fine in the renderer
- Speaker asks the agent to add color to charge states
- Agent initially does not read the color documentation
- Eventually gets CSS-based colors working but only on side chains, not backbone
- Speaker gives a screenshot back to the agent to show what needs fixing
- This illustrates the iterative feedback loop with screenshots
- PG version mentioned is 2.17
- **Maps to:** 8.3 (renderer feedback), 8.4 (iterative debugging with screenshots)

### [10:10-11:44] Randomization, accessibility, and closing

- Speaker emphasizes randomizing questions so pKa values vary between versions
- Uses a "dice" button in the renderer to see different random seeds
- Randomization prevents students from posting answers online for others to copy
- ChatGPT probably cannot write the question but could solve it
- Discusses color accessibility: avoid red-green combinations
- Uses Chicago Bears colors (navy blue and orange) for good contrast
- Neutral chemical groups could be gray for better visual distinction
- Acknowledges needing to learn more about accessibility
- "I did need to give it some guidance. But all the tools are there to debug it."
- Closing: "I just don't need to know how to program"
- **Maps to:** 8.4 (advanced advice: randomization, accessibility, color)

## Key quotes with timestamps

- [01:23] "AI coding agents have really transformed how I write computer code."
- [01:27] "I really don't write computer code much anymore, but I program all day."
- [01:32] "Vibe coding has really taken over."
- [01:38] "ChatGPT is just literally terrible at writing WeBWorK questions."
- [02:18] "You can actually go back and forth with ChatGPT on this and eventually
  it'll convince you that your renderer is broken."
- [02:26] "Claude Code on the other hand actually pretty successful."
- [03:01] "It just gets confused with all the Perl out there because PG is like Perl,
  but not quite."
- [03:08] "This is like the worst part of programming. You're stuck debugging someone
  else's code."
- [03:38] "[I] written a skill which is invoked with [a slash command] called
  webwork_writer, which basically gives it a whole bunch of documentation."
- [03:52] "It actually is able to connect itself to the renderer to confirm that its
  code actually works."
- [04:00] "It's obsessed with finding other files on my file system to use to cheat."
- [05:12] "I got like 50 glazed eyes looking back at me and I'm like, this would be a
  great question to add to ADAPT."
- [05:57] "ChatGPT wants to use kind of its own random function, which is not how
  WeBWorK works."
- [06:38] "I don't want to have to debug all that. Let it do it."
- [07:33] "You have to have patience when working with these AI things."
- [07:52] "It's better for it to sit there and struggle getting the problem correct
  than me sitting there to struggle."
- [08:04] "You can see it's kind of sending the problem to the local renderer to verify."
- [10:40] "I just thought I'd share kind of my system for writing WeBWorK code using
  AI agents."
- [11:33] "I did need to give it some guidance. But all the tools are there to debug
  it at least."
- [11:40] "I just don't need to know how to program."

## Video topic to chapter section mapping

| Video topic | Section | Teaching points to include |
| --- | --- | --- |
| Motivation: adapting biology homework | 8.0 Index | Frame the chapter around real instructor needs |
| Vibe coding concept | 8.1 What are AI Agents? | Define vibe coding, contrast with traditional coding |
| ChatGPT fails at WeBWorK | 8.1 What are AI Agents? | Demo why plain LLM chat is insufficient |
| PG vs. Perl confusion | 8.1, 8.2 | Explain why PG syntax confuses LLMs trained on Perl |
| Claude Code vs. Codex comparison | 8.1 What are AI Agents? | Compare agent capabilities and speed |
| The `webwork_writer` skill | 8.2 Knowledge Documents | How to create and invoke a skill/knowledge doc |
| Documents prevent wrong patterns | 8.2 Knowledge Documents | Why agents need curated PG documentation |
| WeBWorK randomization functions | 8.2 Knowledge Documents | Document WeBWorK-specific random() vs. Perl rand() |
| Connecting agent to renderer | 8.3 Connecting to Renderer | Agent sends code to localhost:3000 to verify |
| Debug mode and HTML inspection | 8.3 Connecting to Renderer | Using debug mode to diagnose rendering errors |
| Giving the agent a screenshot | 8.3, 8.4 | Iterative feedback: screenshot -> agent -> fix |
| Patience and the debug loop | 8.4 Advanced Advice | Expect 15-20 min per complex question |
| Telling agent to re-read docs | 8.4 Advanced Advice | Redirect agents back to skill documentation |
| Agent "cheats" by searching disk | 8.4 Advanced Advice | Instruct agents to use only provided documents |
| Randomizing pKa values | 8.4 Advanced Advice | Anti-cheating through randomized question variants |
| Color and accessibility | 8.4 Advanced Advice | CSS-based colors, avoid red-green, Bears palette |
| `my` keyword pitfall | 8.2, 8.4 | PG does not allow Perl `my` variable declarations |

## Transcription corrections

| Misheard text | Correct text |
| --- | --- |
| "claw odd code" / "cloud code" / "Clod code" | Claude Code |
| "Pearl" | Perl |
| "chat GBT" / "chatbt" / "chatgbt" / "chatt" | ChatGPT |
| "codeex" / "codex" | Codex (OpenAI) |
| "Libra text" / "library text" | LibreTexts |
| "Mai's" / "mice" | `my`'s (Perl keyword) |
| "PG2 2.17" / "WebRK 2.0" | PG 2.17 |
| "CPCA colors" / "CPC colors" | CSS-based colors |
| "latte" | LaTeX |
| "dollars on here" | slash command (skill invocation) |
| "webwork codex forum" | WeBWorK Codex forum (project workspace) |
| "up seeds problems" | "it sees problems" / debugging issues |
| "isometric points" | isoelectric points |
| "PA KAS" / "PA the PA KAS" | pKa's (pKa values) |
| "the co version" / "COOH version" | COOH version (carboxyl group) |
| "cloud" / "claud" | Claude (Anthropic AI) |
| "Bears colors" | Chicago Bears colors (navy/orange for contrast) |
