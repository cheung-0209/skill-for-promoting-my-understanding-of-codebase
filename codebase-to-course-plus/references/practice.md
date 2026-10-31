# Follow-along practice

Turn understanding into small actions. Preserve the original checkout and put work in the course's `practice/` directory or a user-designated learning workspace.

## A good exercise contract

Each task specifies:

1. **Goal and source:** what behavior to reproduce and the source ranges to read.
2. **Prerequisites:** required concepts and packages; say whether it is CPU-only or needs a specific backend.
3. **Learner action:** a small file or function to type, inspect, or change. State exactly which parts the learner should write.
4. **Inputs and expected invariants:** shapes, deterministic values, bounds, connectivity, or an expected error. Do not invent a successful output.
5. **Command:** how to run the example/check, from which directory.
6. **Hints and solution:** progressive hints, then a separately labeled reference implementation and explanation of common failures.

For a hand-coded exercise, provide a starter plus a separate solution so the learner has meaningful work. HTML quizzes complement executable practice; a browser text editor must not claim to execute Python unless a genuine runtime exists.

## Prefer a short progression

- **Read and predict:** predict a return value, dimension, or branch before revealing it.
- **Implement one primitive:** reproduce a small operation on a toy input.
- **Connect two steps:** pass a documented output into the next component and check its contract.
- **Diagnose one fault:** change an axis, shape, normalization, or config intentionally and explain the observed failure.

In research code, begin with a tiny synthetic example. A toy Chamfer distance or coordinate transform must be labeled as a teaching reimplementation with its own assumptions. Distinguish it from the repository's original implementation and paper reproduction.

## Checks that teach

Use a meaningful invariant instead of a test that merely duplicates the solution's operations: round-trip coordinates, permutation invariance where appropriate, known distances on simple points, zero error on identical inputs, valid shape/device contracts, or behavior on an empty/degenerate case. Choose only cases relevant to the inspected operation.

Run solutions and checks when feasible. An intentionally incomplete starter can fail by design; verify that the expected failure is useful and that the solution passes. Record commands and outcomes in `practice/README.md` or `source-map.md`. If an environment is unavailable, label the command as unrun and explain what remains unverified.

## Source excerpt versus learning code

Original excerpts are exact extracts with snippet IDs and line ranges. Learning code can be simplified but must say “教学示例/teaching example”. Proposed repository fixes must say “建议修改/proposed change”. Keep numerical assumptions near the example. Do not silently present an exercise solution as the author's code.
