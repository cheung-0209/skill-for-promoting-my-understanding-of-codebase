#!/usr/bin/env python3
"""Offline course setup, exact source extraction, assembly and structural checks.

Python 3.9+; standard library only. This does not execute a repository's code.
"""
import argparse
import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import shutil
import sys
from urllib.parse import unquote, urlsplit


def digest(data):
    return hashlib.sha256(data).hexdigest()


def contained(root, relative):
    root = Path(root).resolve()
    path = (root / relative).resolve()
    try:
        path.relative_to(root)
    except ValueError:
        raise ValueError("Path escapes its root: " + str(relative))
    return path


class Element:
    def __init__(self, tag, attrs=()):
        self.tag = tag
        self.attrs = dict(attrs)
        self.children = []

    def has(self, cls):
        return cls in (self.attrs.get("class") or "").split()

    def walk(self):
        for child in self.children:
            if isinstance(child, Element):
                yield child
                yield from child.walk()

    def text(self):
        return "".join(c.text() if isinstance(c, Element) else c for c in self.children)


class Document(HTMLParser):
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}

    def __init__(self, content):
        super().__init__(convert_charrefs=True)
        self.root = Element("root")
        self.stack = [self.root]
        self.feed(content)

    def handle_starttag(self, tag, attrs):
        el = Element(tag, attrs)
        self.stack[-1].children.append(el)
        if tag not in self.VOID:
            self.stack.append(el)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def read_manifest(course):
    path = course / "snippets.json"
    data = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
    if not isinstance(data, list):
        raise ValueError("snippets.json must be a list")
    ids = [item["id"] for item in data]
    if len(set(ids)) != len(ids):
        raise ValueError("Duplicate snippet IDs in manifest")
    return data


def init(args):
    out = args.out.resolve()
    if out.exists() and (not out.is_dir() or any(out.iterdir())):
        raise ValueError("Destination must be absent or empty: " + str(out))
    if not re.fullmatch(r"[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*", args.lang):
        raise ValueError("Invalid language tag")
    source = Path(__file__).resolve().parents[1] / "assets" / "course"
    shutil.copytree(source, out, dirs_exist_ok=True)
    (out / "modules").mkdir()
    base = (out / "_base.html").read_text(encoding="utf-8")
    zh = args.lang.lower().startswith("zh")
    values = {"LANG": args.lang, "TITLE": args.title,
              "SKIP": "跳到课程内容" if zh else "Skip to content",
              "NAV_LABEL": "课程章节" if zh else "Course modules",
              "PROGRESS": "阅读进度" if zh else "Reading progress"}
    for key, value in values.items():
        base = base.replace("{{" + key + "}}", html.escape(value, quote=True))
    (out / "_base.html").write_text(base, encoding="utf-8")
    (out / "snippets.json").write_text("[]\n", encoding="utf-8")
    print("Initialized: " + str(out))


def extract(args):
    course = args.course.resolve()
    if not (course / "modules").is_dir():
        raise ValueError("Initialize the course first")
    if not re.fullmatch(r"[a-z][a-z0-9-]*", args.id):
        raise ValueError("Snippet ID must be lowercase letters, digits and hyphens")
    path = contained(args.repo, args.file)
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    if args.start < 1 or args.end < args.start or args.end > len(lines):
        raise ValueError("Invalid inclusive line range")
    entries = read_manifest(course)
    if any(entry["id"] == args.id for entry in entries):
        raise ValueError("Snippet ID already exists: " + args.id)
    text = "".join(lines[args.start - 1:args.end])
    relative = path.relative_to(args.repo.resolve()).as_posix()
    entry = {"id": args.id, "file": relative, "start": args.start, "end": args.end,
             "text": text, "sha256": digest(text.encode("utf-8")),
             "file_sha256": digest(path.read_bytes())}
    label = "{}:L{}–L{} · 原始源码 / Original source".format(relative, args.start, args.end)
    figure = ('<figure class="source-block">\n<figcaption>' + html.escape(label) +
              '</figcaption>\n<pre tabindex="0"><code data-snippet-id="' + args.id + '">' +
              html.escape(text, quote=False) + '</code></pre>\n</figure>\n')
    folder = course / "snippets"
    folder.mkdir(exist_ok=True)
    target = folder / (args.id + ".html")
    target.write_text(figure, encoding="utf-8")
    entries.append(entry)
    (course / "snippets.json").write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(str(target))


def module_parts(course):
    parts, ids = [], set()
    for path in sorted((course / "modules").glob("*.html")):
        content = path.read_text(encoding="utf-8")
        doc = Document(content)
        nodes = list(doc.root.walk())
        if any(n.tag in {"html", "head", "body", "script", "style"} for n in nodes):
            raise ValueError("Module contains document/script/style wrapper: " + path.name)
        roots = [c for c in doc.root.children if isinstance(c, Element)]
        if len(roots) != 1 or roots[0].tag != "section" or not roots[0].has("module"):
            raise ValueError("Module must contain one section.module: " + path.name)
        mod = roots[0]
        ident = mod.attrs.get("id", "")
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", ident) or ident in ids:
            raise ValueError("Missing/invalid/duplicate module ID: " + path.name)
        heading = next((n.text().strip() for n in mod.walk() if n.tag in {"h1", "h2", "h3"}), "")
        title = mod.attrs.get("data-title") or heading
        if not title:
            raise ValueError("Module title missing: " + path.name)
        ids.add(ident)
        parts.append((ident, title, content))
    if not parts:
        raise ValueError("No modules/*.html found")
    return parts


def build(args):
    course = args.course.resolve()
    parts = module_parts(course)
    nav = "\n".join('<button type="button" class="nav-dot" data-target="{}" data-tooltip="{}" aria-label="{}"></button>'.format(
        html.escape(ident, quote=True), html.escape(title, quote=True), html.escape(title, quote=True))
        for ident, title, _ in parts)
    base = (course / "_base.html").read_text(encoding="utf-8")
    if base.count("{{NAV_DOTS}}") != 1:
        raise ValueError("Shell must contain one {{NAV_DOTS}} token")
    base = base.replace("{{NAV_DOTS}}", nav)
    if re.search(r"\{\{[A-Z_]+\}\}", base):
        raise ValueError("Unresolved shell token")
    output = base + "\n".join(part[2] for part in parts) + (course / "_footer.html").read_text(encoding="utf-8")
    (course / "index.html").write_text(output, encoding="utf-8")
    print("Built {} ({} modules)".format(course / "index.html", len(parts)))


def check(args):
    course = args.course.resolve()
    nodes = list(Document((course / "index.html").read_text(encoding="utf-8")).root.walk())
    errors = []
    ids = [n.attrs["id"] for n in nodes if n.attrs.get("id")]
    if len(ids) != len(set(ids)):
        errors.append("Duplicate HTML IDs")
    mod_ids = [n.attrs.get("id") for n in nodes if n.has("module")]
    nav_ids = [n.attrs.get("data-target") for n in nodes if n.has("nav-dot")]
    if not mod_ids or nav_ids != mod_ids:
        errors.append("Navigation targets must match modules in order")
    if not (course / "source-map.md").is_file():
        errors.append("Missing source-map.md")

    for node in nodes:
        for key in ("href", "src", "poster"):
            value = node.attrs.get(key)
            if not value:
                continue
            url = urlsplit(value)
            asset = key != "href" or node.tag == "link"
            if asset and (url.scheme in {"http", "https"} or url.netloc):
                errors.append("Remote runtime asset: " + value)
            if url.scheme or url.netloc:
                if url.scheme in {"javascript", "file"}:
                    errors.append("Nonportable or executable URL: " + value)
                continue
            if url.path:
                target = contained(course, unquote(url.path))
                if not target.is_file():
                    errors.append("Missing local file: " + value)
            if not url.path and url.fragment and unquote(url.fragment) not in ids:
                errors.append("Missing anchor: " + value)

        if node.has("quiz-question-block"):
            options = [n for n in node.walk() if n.has("quiz-option")]
            correct = node.attrs.get("data-correct")
            if not correct or sum(n.attrs.get("data-value") == correct for n in options) != 1:
                errors.append("Quiz needs one matching correct option")
            if not any(n.has("quiz-feedback") for n in node.walk()):
                errors.append("Quiz feedback element missing")
        if node.has("flow-animation"):
            try:
                steps = json.loads(node.attrs.get("data-steps", "[]"))
                if not isinstance(steps, list) or not steps:
                    raise ValueError("expected nonempty list")
                for step in steps:
                    if not isinstance(step, dict) or not step.get("label"):
                        raise ValueError("step label missing")
                    for endpoint in ("from", "to") if step.get("packet") else ():
                        if "flow-" + str(step.get(endpoint, "")) not in ids:
                            raise ValueError("unknown flow endpoint")
            except (ValueError, TypeError) as exc:
                errors.append("Invalid flow steps: " + str(exc))
        if node.has("chat-window") and not node.attrs.get("id"):
            errors.append("Chat container ID missing")

    entries = read_manifest(course)
    rendered = [n for n in nodes if n.tag == "code" and n.attrs.get("data-snippet-id")]
    lookup = {entry["id"]: entry for entry in entries}
    used = set()
    for node in rendered:
        ident = node.attrs["data-snippet-id"]
        used.add(ident)
        entry = lookup.get(ident)
        if entry is None or node.text() != entry["text"]:
            errors.append("Rendered source differs from manifest: " + ident)
    for entry in entries:
        ident = entry["id"]
        if ident not in used:
            errors.append("Extracted snippet not embedded: " + ident)
        if digest(entry["text"].encode("utf-8")) != entry["sha256"]:
            errors.append("Snippet checksum differs: " + ident)
        if args.repo:
            path = contained(args.repo, entry["file"])
            lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
            actual = "".join(lines[entry["start"] - 1:entry["end"]])
            if actual != entry["text"] or digest(path.read_bytes()) != entry["file_sha256"]:
                errors.append("Source file/range changed since extraction: " + ident)

    for path in course.glob("*.css"):
        css = path.read_text(encoding="utf-8")
        if re.search(r"@import\b|url\(\s*['\"]?(?:https?:)?//", css, re.I):
            errors.append("CSS may load a remote asset: " + path.name)
    for path in course.glob("*.js"):
        js = path.read_text(encoding="utf-8")
        if re.search(r"\bfetch\s*\(|\bXMLHttpRequest\b|\bWebSocket\s*\(", js):
            errors.append("JS uses runtime network/file loading; review offline contract: " + path.name)
    if errors:
        raise ValueError("\n".join(errors))
    print("PASS: navigation, local assets, anchors, quiz/flow wiring, {} snippets{}".format(
        len(entries), " and source files" if args.repo else " (source checkout not checked)"))
    print("Static checks only; browser behavior and teaching accuracy require separate review.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    p = commands.add_parser("init")
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--lang", default="zh-CN")
    p.set_defaults(run=init)
    p = commands.add_parser("extract")
    p.add_argument("--repo", type=Path, required=True)
    p.add_argument("--course", type=Path, required=True)
    p.add_argument("--file", required=True)
    p.add_argument("--start", type=int, required=True)
    p.add_argument("--end", type=int, required=True)
    p.add_argument("--id", required=True)
    p.set_defaults(run=extract)
    for name, func in (("build", build), ("check", check)):
        p = commands.add_parser(name)
        p.add_argument("--course", type=Path, required=True)
        if name == "check":
            p.add_argument("--repo", type=Path)
        p.set_defaults(run=func)
    args = parser.parse_args()
    try:
        args.run(args)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print("ERROR: " + str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
