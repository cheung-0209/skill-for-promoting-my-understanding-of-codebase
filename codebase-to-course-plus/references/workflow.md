# Reading a codebase and using the helper

## General software

Identify what the program accepts and produces. Trace one actual action: CLI arguments or a UI event → entrypoint → domain operation → external I/O → returned result. Explain the responsibilities of components at their call sites. Show request/response shapes and failure paths where they matter. Distinguish real external services from mocked examples.

Read declared dependencies and existing scripts before suggesting commands. Annotate version-sensitive commands with their source and environment assumptions. Prefer lightweight existing checks; a reading task rarely needs a complete production deployment.

## Source snapshot

`source-map.md` should record:

```text
Repository: canonical URL or local source path
Snapshot: full commit / non-Git directory
Worktree: clean, or relevant modified files
Entrypoint and config: exact files inspected
Learning route: input → functions/modules → outputs
Evidence: module → source paths/line ranges or paper section
Execution: commands actually run, environment, observed outcomes
Unresolved: missing assets, unknown dimensions, code/paper discrepancies
```

Use commit-pinned GitHub links when possible. Do not put secrets, private datasets, or personal local paths into a shareable course unnecessarily. If the worktree differs from its commit, label the course as based on that worktree; a GitHub permalink may not reproduce the modified snippet.

## Helper commands

Requires Python 3.9+ standard library only. Resolve `<skill-dir>` from the installed skill's actual location; do not assume it is in the current working directory.

```bash
python3 <skill-dir>/scripts/course.py init --out <course-dir> --title "项目源码课程" --lang zh-CN
python3 <skill-dir>/scripts/course.py extract --repo <repo-dir> --file src/core.py --start 10 --end 20 --id core-step --course <course-dir>
python3 <skill-dir>/scripts/course.py build --course <course-dir>
python3 <skill-dir>/scripts/course.py check --course <course-dir> --repo <repo-dir>
```

- `init` refuses a nonempty destination. It copies assets; it does not clone or install packages.
- `extract` writes `snippets/<id>.html` and appends an entry to `snippets.json`. Lines are one-based and inclusive. It rejects out-of-root paths and duplicate IDs. Embed the figure into a module; the build does not insert snippets automatically.
- `build` reads UTF-8 files from `modules/*.html` in filename order. Titles come from `data-title`, then a heading. It refuses missing/duplicate module IDs, unresolved shell tokens, and modules containing document wrappers or script/style tags. Rebuilding replaces only `index.html`.
- `check` exits nonzero for structural failures. Pass `--repo` for checking against the original checkout; without it only the saved manifest and rendered source blocks are compared. A matching checksum does not validate the explanation.

## Authoring structure

```html
<section class="module" id="module-1" data-title="从输入到输出">
  <div class="module-content">
    <p class="module-number">01</p>
    <h1 class="module-title">从输入到输出</h1>
    <p>学习目标：找到入口并预测这次调用的结果。</p>
    <!-- Paste the generated source figure, then add the explanation. -->
    <!-- Add an interaction using the relevant reference pattern. -->
  </div>
</section>
```

Use `<details><summary>提示 / 参考答案</summary>…</details>` for progressive hints. Source code uses `<pre><code>` with preserved indentation; let long lines scroll within the code panel. A visual diagram should have a text equivalent that remains useful without animation. Do not render exercise text as executable browser code.
