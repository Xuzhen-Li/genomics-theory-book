#!/usr/bin/env python3
"""Build a GitHub Wiki tree from book chapters in this repository."""

from __future__ import annotations

import argparse
import posixpath
import re
import sys
from pathlib import Path

REPO = "Xuzhen-Li/genomics-theory-book"
CHAPTER_DIR = "book/chapters"
INDEX_EN = "book/INDEX.md"
INDEX_ZH = "book/INDEX.zh.md"
BLOB_BASE = f"https://github.com/{REPO}/blob/main"
RAW_BASE = f"https://github.com/{REPO}/raw/main"
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".bmp"}

HEADER_TEMPLATE = (
    "<!-- This page is copied from {source} in the {repo} repository "
    "after each update of main. Changes made here on the Wiki website "
    "are overwritten. Edit the repository file instead. -->\n\n"
)

GENERATED_HEADER = (
    "<!-- This page is generated from book/INDEX.md and book/INDEX.zh.md "
    f"in the {REPO} repository after each update of main. "
    "Changes made here on the Wiki website are overwritten. "
    "Edit the index files in the repository instead. -->\n\n"
)

LINK_RE = re.compile(r"(!?\[[^\]]*\]\()([^)]+)(\))")
SECTION_RE = re.compile(r"^## (.+)$")
ENTRY_RE = re.compile(
    r"^(\d+|[A-Z])\. \[([^\]]+)\]\(([^)]+)\)(?: — (.*))?$"
)
PLAIN_ENTRY_RE = re.compile(r"^(\d+|[A-Z])\. (.+)$")


class SyncError(Exception):
    pass


def split_frag(href):
    if href.startswith("#"):
        return "", href
    if "#" in href:
        path, frag = href.split("#", 1)
        return path, "#" + frag
    return href, ""


def page_name(wiki_file):
    if wiki_file.endswith(".md"):
        return wiki_file[:-3]
    return wiki_file


def parse_index(text, index_path):
    index_dir = posixpath.dirname(index_path)
    sections = []
    current = None
    for raw in text.splitlines():
        line = raw.rstrip()
        msec = SECTION_RE.match(line)
        if msec:
            current = {"title": msec.group(1), "entries": []}
            sections.append(current)
            continue
        ment = ENTRY_RE.match(line)
        if ment:
            if current is None:
                raise SyncError(f"{index_path}: entry before any section: {line}")
            number = ment.group(1)
            title = ment.group(2)
            rel = ment.group(3)
            status = ment.group(4) or ""
            path_only, frag = split_frag(rel)
            if frag:
                raise SyncError(
                    f"{index_path}: unexpected fragment in chapter link: {rel}"
                )
            source = posixpath.normpath(posixpath.join(index_dir, path_only))
            if not source.startswith(CHAPTER_DIR + "/"):
                raise SyncError(
                    f"{index_path}: chapter path outside {CHAPTER_DIR}: {source}"
                )
            wiki = posixpath.basename(source)
            current["entries"].append(
                {
                    "number": number,
                    "title": title,
                    "source": source,
                    "status": status.strip(),
                    "wiki": wiki,
                }
            )
            continue
        mplain = PLAIN_ENTRY_RE.match(line)
        if mplain and current is not None:
            current["entries"].append(
                {
                    "number": mplain.group(1),
                    "title": mplain.group(2).strip(),
                    "source": None,
                    "status": "",
                    "wiki": None,
                }
            )
    if not sections:
        raise SyncError(f"{index_path}: no sections found")
    return sections


def list_chapter_files(repo_root: Path):
    folder = repo_root / CHAPTER_DIR
    if not folder.is_dir():
        raise SyncError(f"missing {CHAPTER_DIR}")
    names = sorted(p.name for p in folder.iterdir() if p.is_file() and p.suffix == ".md")
    return names


def build_mapping(sections_en, sections_zh):
    mapping = {}
    for sections in (sections_en, sections_zh):
        for sec in sections:
            for ent in sec["entries"]:
                if ent["source"] is None:
                    continue
                if ent["source"] in mapping and mapping[ent["source"]] != ent["wiki"]:
                    raise SyncError("conflicting wiki names for {0}".format(ent["source"]))
                mapping[ent["source"]] = ent["wiki"]
    return mapping


def check_complete(mapping, repo_root):
    names = list_chapter_files(repo_root)
    mapped_bases = sorted(posixpath.basename(s) for s in mapping)
    if mapped_bases != names:
        missing = [n for n in names if n not in mapped_bases]
        extra = [n for n in mapped_bases if n not in names]
        raise SyncError(
            "INDEX and book/chapters do not match. "
            f"In chapters but not INDEX: {missing}. "
            f"In INDEX but not chapters: {extra}."
        )
    for source in mapping:
        path = repo_root / source
        if not path.is_file():
            raise SyncError(f"missing chapter file: {source}")


def rewrite_href(src_source, href, mapping):
    href = href.strip()
    if not href:
        return href
    lower = href.lower()
    if lower.startswith(("http://", "https://", "mailto:", "ftp://", "//")):
        return href
    path, frag = split_frag(href)
    if path == "":
        return href
    src_dir = posixpath.dirname(src_source)
    resolved = posixpath.normpath(posixpath.join(src_dir, path))
    if resolved in mapping:
        wiki_file = mapping[resolved]
        return page_name(wiki_file) + frag
    ext = posixpath.splitext(resolved)[1].lower()
    if ext in IMAGE_EXT:
        return RAW_BASE + "/" + resolved + frag
    return BLOB_BASE + "/" + resolved + frag


def rewrite_markdown(src_source, text, mapping):
    def repl(match):
        prefix, href, suffix = match.group(1), match.group(2), match.group(3)
        return prefix + rewrite_href(src_source, href, mapping) + suffix
    return LINK_RE.sub(repl, text)


def render_toc(sections, heading):
    lines = [f"## {heading}", ""]
    for sec in sections:
        lines.append("### " + sec["title"])
        lines.append("")
        for ent in sec["entries"]:
            if ent["wiki"]:
                item = "{0}. [{1}]({2})".format(ent["number"], ent["title"], page_name(ent["wiki"]))
            else:
                item = "{0}. {1}".format(ent["number"], ent["title"])
            if ent["status"]:
                item = item + " — " + ent["status"]
            lines.append(item)
        lines.append("")
    return "\n".join(lines)


def render_home(sections_en, sections_zh):
    parts = [
        GENERATED_HEADER.rstrip(),
        "",
        "# Genomics Theory Book",
        "",
        "This Wiki is a reading copy of the book chapters from the "
        f"[{REPO}](https://github.com/{REPO}) repository. "
        "The Wiki is updated from that repository when main changes. "
        "To change a chapter, edit the file in the repository. "
        "Edits made on the Wiki website are overwritten.",
        "",
        "The contents list, status table, figures, figure scripts and licence "
        "stay in the repository:",
        "",
        f"- [Contents (English)]({BLOB_BASE}/book/INDEX.md)",
        f"- [目录（中文）]({BLOB_BASE}/book/INDEX.zh.md)",
        f"- [Status table]({BLOB_BASE}/book/STATUS.md)",
        f"- [地位总表]({BLOB_BASE}/book/STATUS.zh.md)",
        f"- [Book README]({BLOB_BASE}/book/README.md)",
        f"- [Licence]({BLOB_BASE}/book/LICENSE.md)",
        f"- [Figures]({BLOB_BASE}/book/figures)",
        "",
        "English contents are first; the Chinese contents follow.",
        "",
        render_toc(sections_en, "Contents").rstrip(),
        "",
        render_toc(sections_zh, "目录").rstrip(),
        "",
    ]
    return "\n".join(parts)


def render_sidebar(sections_en, sections_zh):
    lines = [
        GENERATED_HEADER.rstrip(),
        "",
        "# Genomics Theory Book",
        "",
        "- [Home](Home)",
        f"- [Repository](https://github.com/{REPO})",
        "",
        "## English",
        "",
    ]
    for sec in sections_en:
        lines.append("### " + sec["title"])
        for ent in sec["entries"]:
            if ent["wiki"]:
                lines.append(
                    "- [{0}. {1}]({2})".format(ent["number"], ent["title"], page_name(ent["wiki"]))
                )
            else:
                lines.append("- {0}. {1}".format(ent["number"], ent["title"]))
        lines.append("")
    lines.append("## 中文")
    lines.append("")
    for sec in sections_zh:
        lines.append("### " + sec["title"])
        for ent in sec["entries"]:
            if ent["wiki"]:
                lines.append(
                    "- [{0}. {1}]({2})".format(ent["number"], ent["title"], page_name(ent["wiki"]))
                )
            else:
                lines.append("- {0}. {1}".format(ent["number"], ent["title"]))
        lines.append("")
    return "\n".join(lines)


def write_text(path: Path, text: str, update: bool):
    if not text.endswith("\n"):
        text += "\n"
    data = text.encode("utf-8")
    if path.exists():
        old = path.read_bytes()
        if old == data:
            return "same"
        if not update:
            raise SyncError(
                f"refusing to replace an existing file without --update: {path}"
            )
        path.write_bytes(data)
        return "updated"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as fh:
        fh.write(data)
    return "created"


def file_has_generated_header(path: Path):
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return text.startswith(
        (
            "<!-- This page is copied from ",
            "<!-- This page is generated from ",
        )
    )


def partition_and_maybe_remove_stale(wiki_root: Path, intended, update):
    removed = []
    extras = []
    stale = []
    if not wiki_root.is_dir():
        return removed, extras
    for path in wiki_root.rglob("*"):
        rel = path.relative_to(wiki_root)
        if any(part == ".git" for part in rel.parts):
            continue
        if not path.is_file():
            continue
        name = rel.as_posix()
        if name in intended:
            continue
        if file_has_generated_header(path):
            stale.append((path, name))
        else:
            extras.append(name)
    extras.sort()
    if stale and not update:
        names = ", ".join(item[1] for item in stale)
        raise SyncError(
            "refusing to remove stale generated Wiki pages without --update: " + names
        )
    for path, name in stale:
        path.unlink()
        removed.append(name)
    removed.sort()
    return removed, extras


def sync(repo_root: Path, wiki_root: Path, update: bool):
    repo_root = repo_root.resolve()
    wiki_root = wiki_root.resolve()
    index_en_path = repo_root / INDEX_EN
    index_zh_path = repo_root / INDEX_ZH
    if not index_en_path.is_file() or not index_zh_path.is_file():
        raise SyncError("missing book/INDEX.md or book/INDEX.zh.md")
    sections_en = parse_index(index_en_path.read_text(encoding="utf-8"), INDEX_EN)
    sections_zh = parse_index(index_zh_path.read_text(encoding="utf-8"), INDEX_ZH)
    mapping = build_mapping(sections_en, sections_zh)
    check_complete(mapping, repo_root)
    intended = {"Home.md", "_Sidebar.md"}
    intended.update(mapping.values())
    results = []
    for source, wiki in sorted(mapping.items(), key=lambda kv: kv[1]):
        text = (repo_root / source).read_text(encoding="utf-8")
        rewritten = rewrite_markdown(source, text, mapping)
        header = HEADER_TEMPLATE.format(source=source, repo=REPO)
        dest = wiki_root / wiki
        action = write_text(dest, header + rewritten, update)
        results.append((wiki, source, action))
    action = write_text(
        wiki_root / "Home.md",
        render_home(sections_en, sections_zh),
        update,
    )
    results.insert(0, ("Home.md", "(generated from book/INDEX.md and book/INDEX.zh.md)", action))
    action = write_text(
        wiki_root / "_Sidebar.md",
        render_sidebar(sections_en, sections_zh),
        update,
    )
    results.insert(1, ("_Sidebar.md", "(generated from book/INDEX.md and book/INDEX.zh.md)", action))
    removed, extras = partition_and_maybe_remove_stale(wiki_root, intended, update)
    return results, extras, removed


def main(argv):
    parser = argparse.ArgumentParser(
        description="Build a Wiki tree from book chapters."
    )
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--wiki-root", required=True)
    parser.add_argument(
        "--update",
        action="store_true",
        help="Allow replacing files that already exist in --wiki-root (needed on a Wiki checkout).",
    )
    args = parser.parse_args(argv)
    try:
        results, extras, removed = sync(Path(args.repo_root), Path(args.wiki_root), args.update)
    except SyncError as exc:
        print("error: {0}".format(exc), file=sys.stderr)
        return 1
    print("Wrote {0} pages to {1}:".format(len(results), args.wiki_root))
    for wiki, source, action in results:
        print("  {0}\t{1}\t{2}".format(wiki, action, source))
    if removed:
        print("Removed stale generated pages:")
        for rel in removed:
            print("  {0}".format(rel))
    if extras:
        print("Warning: files in the Wiki tree that this script does not manage (left in place):")
        for rel in extras:
            print("  {0}".format(rel))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
