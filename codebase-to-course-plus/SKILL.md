---
name: codebase-to-course-plus
description: "Turn a repository into an interactive, source-grounded course with step-by-step coding practice. Use for codebase courses, 中文源码导读、源码跟敲、科研代码学习、论文与实现对照. Supports general software and research/ML projects; a request only to find a repo, review a skill, or fix one bug does not call for generating a course."
---

# Codebase to Course Plus

Create an interactive course that lets the learner follow the real implementation and practice small parts of it. Adapted from Zara Zhang's `codebase-to-course`; see [SOURCE.md](SOURCE.md). Preserve its code/explanation layout, reusable interaction engines, and warm notebook design. Add source evidence, research-code tracing, and verifiable practice.

## Choose the learning contract

Use the user's language, background, repository, and goal from the conversation. Chinese requests produce Chinese teaching prose while keeping identifiers and original code unchanged. Do not assume either zero programming knowledge or ML expertise.

- **Overview:** understand responsibilities and one end-to-end execution path.
- **Follow along:** read, retype, run small examples, and diagnose errors. Use this when the user says “跟敲/敲源码”.
- **Research:** map a paper to its implementation and trace tensors, geometry, training, and inference. Combine with follow along when appropriate.

If a repository and goal are known, proceed and state any material assumptions briefly. Ask only for inputs that cannot be discovered and prevent useful work. When the request is to author or inspect this skill, work on the skill itself; do not start a course automatically.

## 1. Establish the source snapshot

Read relevant `AGENTS.md`. Use an existing local checkout when supplied. For a GitHub URL, acquire the source in a unique scratch directory within the permitted workspace. Respect the requested branch or commit. Do not reuse a different checkout silently, execute repository setup scripts, or install training dependencies just to read code.

Record the repository URL, full commit, worktree modifications if any, and inspected config/entrypoint in the course's `source-map.md`. For a non-Git folder, record that fact and the hashes of cited files. Inspect README, configs, entrypoints, data processing, core modules, losses, and evaluation as relevant. Follow actual imports and calls rather than inferring architecture from filenames.

For general software and CLI workflow details, read [references/workflow.md](references/workflow.md). For research/ML work, also read [references/research.md](references/research.md). Read linked papers only when needed, through available document/web tools; cite exact sections or equations you actually inspected.

## 2. Build evidence before explanations

Every displayed **original-source** block must be an unmodified, contiguous range of the inspected file, with its path and one-based line range visible. Extract with the helper:

```bash
python3 <skill-dir>/scripts/course.py extract \
  --repo <repo-dir> --file <relative-file> --start 10 --end 24 \
  --id core-forward --course <course-dir>
```

This emits a reusable HTML figure and writes `snippets.json`. Embed that figure directly, then add explanations beside it; keep the generated `code[data-snippet-id]` text intact. Multiple shorter extracts are preferable to inserting ellipses in one extract. Pseudocode, exercises, proposed fixes, and synthetic examples need explicit labels and must not carry an original-source snippet ID.

Separate what is **observed in source**, **inferred statically**, **described by the paper**, and **verified by execution**. State an unknown instead of inventing dimensions, results, author intent, installed versions, or a successful run. Cite a paper/code mismatch as a mismatch without resolving it by guesswork.

## 3. Design the learning path

Start with a concrete input and expected output. Choose the number and depth of modules to fit the task; four to six is a useful starting point. Cover the shortest meaningful path first and postpone peripheral utilities.

Each substantive module should have:

- A practical objective and a source-backed code/explanation pair.
- A visual or interactive element that helps reasoning, such as a data-flow stepper, tensor-shape table, or architecture explorer.
- An application question or a small coding task with a way to check the result.

Use metaphors when helpful and name the actual operation immediately afterward. Chat animations are optional. For research code, prioritize numerical examples and geometry over personifying components. Define unfamiliar terms selectively based on the learner's background.

For follow-along or research practice, read [references/practice.md](references/practice.md). Prepare tasks before writing polished HTML. Use separate learner files and collapsible solutions; preserve the inspected source checkout. A sandboxed exercise is a teaching aid and must not be presented as reproducing the full paper.

## 4. Author the course

Initialize the reusable shell with:

```bash
python3 <skill-dir>/scripts/course.py init \
  --out <course-dir> --title "Course title" --lang zh-CN
```

The helper copies `assets/course/` and creates `_base.html`, `_footer.html`, and `modules/`. Write each `modules/NN-topic.html` as one `<section class="module" id="module-N" data-title="…">` containing only module content. Use unique IDs throughout. Read the relevant patterns in [references/interactive-elements.md](references/interactive-elements.md); match their classes, `data-*` attributes, and function names. Keep the provided engines, and add custom behavior in separate local files only if it serves the teaching goal.

The default output is a **directory**, with all runtime assets local. It opens through `file://` without npm, a web server, API keys, Google Fonts, remote JavaScript, or runtime `fetch()`. External source links are allowed; automatic remote asset requests are not. Do not describe it as a single HTML file. If the user requests a portable single file, inline and verify the required assets explicitly.

Write modules sequentially by default. Delegate only when the user or applicable higher-priority instructions authorize it. If authorized, pass each writer a brief containing verified snippets, learning objectives, interface conventions, and adjacent-module context. A large repo alone does not authorize agents.

## 5. Assemble and verify

Read [references/quality.md](references/quality.md), then run:

```bash
python3 <skill-dir>/scripts/course.py build --course <course-dir>
python3 <skill-dir>/scripts/course.py check --course <course-dir> --repo <repo-dir>
```

`build` creates navigation from module IDs/titles and assembles `index.html`. `check` verifies local assets, anchors, module navigation, original snippets against their manifest/source files, and basic quiz/flow wiring. It is a static structural check, not a browser test or proof of conceptual correctness.

Use an available browser to inspect desktop and narrow layouts and exercise the controls actually used. Verify source line ranges and the main learning path independently of the design. Run small practice checks appropriate to the available environment. Report checks separately: source/static checks, browser interactions, CPU examples, model forward pass, training, and benchmark reproduction. Claim only those actually performed. If browser tooling is unavailable, disclose the missing visual check and still deliver the verified artifacts.

## Delivery

Deliver the complete course directory or ZIP with `index.html`, local assets, `source-map.md`, `snippets.json`, and practice materials if selected. Keep scratch clones, caches, data, and model weights out. Link the launch file and briefly explain what the learner can do, the starting point, and any unresolved execution or source limits. Course creation authorizes local authoring; it does not imply publishing, sending messages, or full training runs.
