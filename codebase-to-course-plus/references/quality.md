# Course quality checks

## Content and evidence

- Main execution route follows the inspected config and real calls. Source commit/worktree and key files are recorded.
- Original code blocks match their manifest and source lines exactly after HTML decoding. Path and inclusive line range are visible. Snippets are contiguous and escaped as text.
- Paper concepts, static reasoning, synthetic illustrations, and runtime results are labeled distinctly. Shapes/coordinate conventions and loss/gradient claims have evidence.
- Each module has a useful task/question. Follow-along tasks have starter instructions, expected invariants, and separately accessible solutions.
- No invented execution claims, benchmark scores, author intent, citations, or equation numbers.

## Artifact and interaction

Run `course.py build` and `course.py check --repo …`. Inspect the browser using desktop and narrow widths where tooling permits. Check navigation, glossary on keyboard/touch, one wrong and right quiz answer plus reset, every custom interaction, and links. Test repeated next/play/reset for any chat/flow animations used. A static checker does not exercise these controls.

Keep all runtime assets local. Check for network requests, missing files, console errors, broken IDs, and invalid flow JSON. Verify opening `index.html` directly works; using a server only during QA does not establish file-scheme compatibility.

## Readability and accessibility

Use short explanatory blocks with diagrams where they reduce effort; no forced visual percentage. Maintain Python indentation and allow horizontal scrolling within code panels without making the whole page overflow. Escape HTML characters in code. Keep explanations readable on narrow screens, and make wider tables scroll locally.

Use labeled buttons and native disclosure elements. Avoid drag-only interactions; provide a keyboard-accessible alternative when drag and drop is used. Honor reduced-motion settings and make all instructional content accessible without waiting for animation. Ensure active focus is visible, color is not the only answer cue, and animations explain rather than distract.

## Completion report

State which of the following were actually completed: source/structural checks, visual review, interaction testing, practice solutions, CPU/model forward, training, benchmark reproduction. Include material missing dependencies/data/weights or unavailable tools. Link the runnable course and practice entrypoint; avoid including scratch checkouts or caches.
