#!/usr/bin/env python3
"""Fail-closed policy checker for axloop/axloop-community.

Standard library only. Exit 0 when the tree is compliant; print every
violation and exit 1 otherwise. Every text file in the tree is scanned,
including Markdown. Each violation line names a rule category and a file
location and never echoes the matched value:

  private repository reference    the private enterprise repository (URL or slug)
  obsolete boundary language      old "where the source lives" pointers to a factory repo
  release publication             release workflow, publish/tag command, nonempty release metadata
  staging tag as release input    the historical 2026-08-29 acceptance-staging tag
  Community CI signing material   PKCS#8, signing commands, or key secrets in CI; private keys anywhere
  Community CLI naming            axloop-radar presented as the Community user-facing CLI
  CLI rename migration code       a radar->crawler rename implemented as code in Community
  v0.1.0 archive honesty          a claim that the published v0.1.0 archive contains axloop-crawler
  copied factory workflow         enterprise factory workflow names or tooling
  forbidden implementation tree   top-level src/, tools/, packaging/ and other factory trees
  enterprise project file         enterprise project/metadata file copied into Community

Sensitive match values are assembled from neutral fragments so they do not
appear literally in this repository.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# --- sensitive values assembled from fragments -------------------------------

PRIVATE_ORG = "ascendant" + "ventures"
PRIVATE_NAME = "axloop-edge" + "-poc"
PRIVATE_REPO = "/".join((PRIVATE_ORG, PRIVATE_NAME))
STAGING_TAG = "-".join(("community", "acceptance", "staging", "2026", "08", "29"))
OBSOLETE_SLOGAN = re.compile(r"\benterprise\s+stays?\s+in\b", re.I)

PRIVATE_REPO_PATTERNS = [
    re.compile(re.escape(PRIVATE_REPO), re.I),
    re.compile(r"\b" + re.escape(PRIVATE_NAME) + r"\b", re.I),
    re.compile(r"\b" + re.escape(PRIVATE_ORG) + r"\b", re.I),
]
OBSOLETE_LANGUAGE_PATTERNS = [
    OBSOLETE_SLOGAN,
    re.compile(r"\b(remains?|stays?|lives?|kept)\s+in\s+(the\s+)?(enterprise|factory|private)\s+(repo|repository|factory)", re.I),
    re.compile(r"\bfactory\b.*\bgithub\.com\b|\bgithub\.com\b.*\bfactory\b", re.I),
    re.compile(r"\bcopy\s+(or\s+mirror\s+)?of\s+(that|the)\s+factory\b", re.I),
]

# --- structural policy --------------------------------------------------------

FORBIDDEN_TREES = {"src", "tools", "packaging", "hosted", "supabase", "acceptance", "release"}
ENTERPRISE_PROJECT_FILES = {"verify.py", "pyproject.toml", "setup.py", "DESIGN.md", "PRODUCT.md"}
FACTORY_WORKFLOWS = {
    "community-bundles.yml",
    "community-inputs.yml",
    "community-windows-input-review.yml",
    "community-acceptance.yml",
}
FACTORY_LANGUAGE = [
    re.compile(r"\bcommunity_signing_request\b"),
    re.compile(r"\bcommunity_native_build\b"),
    re.compile(r"\bcommunity[-_](bundles|inputs|acceptance|windows[-_]input[-_]review)\b", re.I),
]
RELEASE_METADATA_FILES = {".community-release.json", "community-release.json", "release.json", ".release.json"}
EMPTY_METADATA = {"", "{}", "[]", "null"}

SKIP_DIRS = {".git", "__pycache__", ".venv", "node_modules"}
MARKDOWN_SUFFIXES = {".md", ".markdown", ".rst"}
STRUCTURED_SUFFIXES = {".json", ".yml", ".yaml", ".toml"}

# Publish/tag instructions. Regex sources are written so they do not match themselves.
PUBLISH_COMMAND_PATTERNS = [
    re.compile(r"\bgh\s+release\s+(create|edit|upload|delete|delete-asset)\b"),
    re.compile(r"\bhub\s+release\s+(create|edit)\b"),
    re.compile(r"\bgit\s+tag\s+(?!(-l\b|--list\b|-n\b|--contains\b|--points-at\b))\S"),
    re.compile(r"\bgit\s+push\b.*(--tags|--follow-tags|\brefs/tags/)"),
    re.compile(r"\bdraft\s*[:=]\s*[\"']?(false|no|off|0)\b", re.I),
    re.compile(r"--draft\s*=\s*(false|0|no)\b", re.I),
    re.compile(r"\bpublish[_-]?release\b|\breleases?/publish\b|\bmake[_-]?latest\b", re.I),
    re.compile(r"uses:\s*[^#\n]*(gh-release|create-release|release-action|upload-release)", re.I),
]
PUBLISHED_METADATA_KEY = re.compile(r"\bpublished[_]at\b")
RELEASE_WORKFLOW_NAME = re.compile(r"release|publish", re.I)
RELEASE_WORKFLOW_CONTENT = re.compile(r"^\s*name\s*:\s*.*\b(release|publish)", re.I | re.M)

# Community CLI naming contract.
CANONICAL_COMMUNITY_COMMAND = "axloop-crawler"
FORBIDDEN_COMMUNITY_COMMAND = "axloop-radar"
PUBLISHED_V010_BINARY = "bin/axloop-community"

FORBIDDEN_COMMAND_PATTERN = re.compile(r"\baxloop[-\s]+radar\b", re.I)
# A line that negates the radar name, or labels it as the separate enterprise
# factory implementation, states policy rather than presenting a Community CLI.
FORBIDDEN_COMMAND_EXEMPT = re.compile(
    r"\b(not|never|no\s+longer|must\s+not|instead\s+of|factory|enterprise|out\s+of\s+scope)\b", re.I
)
CLI_RENAME_CODE_PATTERNS = [
    re.compile(r"s/radar/crawler/"),
    re.compile(r"replace\(\s*['\"]radar['\"]\s*,\s*['\"]crawler['\"]\s*\)"),
    re.compile(r"\bgit\s+mv\b.*radar.*crawler"),
    re.compile(r"\b(mv|ren)\b.*\bradar\b.*\bcrawler\b"),
]
V010_CRAWLER_CLAIM = re.compile(
    r"\bv?0\.1\.0\b(?:(?!\b(?:not|never|no)\b)[^.\n]){0,80}"
    r"\b(?:ships?|contains?|includes?|bundles?|provides?|carries|carry)\b"
    r"(?:(?!\b(?:not|never|no)\b)[^.\n]){0,40}`?(?:bin/)?" + re.escape(CANONICAL_COMMUNITY_COMMAND) + r"`?",
    re.I,
)
NAMING_RULE = (
    f"{CANONICAL_COMMUNITY_COMMAND} is the canonical Community user-visible command; "
    f"{FORBIDDEN_COMMUNITY_COMMAND} must not be presented as the Community user-facing CLI"
)
ARCHIVE_RULE = f"published v0.1.0 must remain documented as shipping {PUBLISHED_V010_BINARY}"

PRIVATE_KEY_BLOCK = re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")
CI_SIGNING_PATTERNS = [
    PRIVATE_KEY_BLOCK,
    re.compile(r"\bPKCS\s*#?\s*8\b", re.I),
    re.compile(r"\bpkcs8\b", re.I),
    re.compile(r"\bed25519\b.*\b(key|sign)", re.I),
    re.compile(r"secrets\.[A-Za-z0-9_]*(SIGN|PRIVATE|PKCS|KEY)[A-Za-z0-9_]*", re.I),
    re.compile(r"\b(SIGNING|PRIVATE)_KEY\b"),
    re.compile(r"\bopenssl\s+(pkeyutl|dgst)\b.*-sign", re.I),
    re.compile(r"\b(gpg|minisign|cosign|signtool|codesign|rcodesign)\b.*\b(sign|-s\b)", re.I),
    re.compile(r"\bsigning[_-]?key\b", re.I),
]

FENCE = re.compile(r"^\s*(```|~~~)\s*([A-Za-z0-9_+-]*)")
SHELL_LANGS = {"", "bash", "sh", "shell", "zsh", "console", "shell-session", "powershell", "ps1", "cmd", "bat"}
SELF_PATHS = {"scripts/check-community-split.py", "tests/test_community_split.py"}


def iter_files(root: Path):
    for path in sorted(root.rglob("*")):
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        if path.is_file():
            yield path


def is_workflow(root: Path, path: Path) -> bool:
    rel = path.relative_to(root)
    return (
        len(rel.parts) >= 3
        and rel.parts[0] == ".github"
        and rel.parts[1] == "workflows"
        and path.suffix in {".yml", ".yaml"}
    )


def read_text(path: Path) -> str | None:
    try:
        data = path.read_bytes()
    except OSError:
        return None
    if b"\x00" in data[:8192]:
        return None
    return data.decode("utf-8", errors="replace")


def strip_yaml_comment(line: str) -> str:
    in_single = in_double = False
    for i, ch in enumerate(line):
        if ch == "'" and not in_double:
            in_single = not in_single
        elif ch == '"' and not in_single:
            in_double = not in_double
        elif ch == "#" and not in_single and not in_double and (i == 0 or line[i - 1].isspace()):
            return line[:i]
    return line


def markdown_segments(lines: list[str]):
    """Yield (lineno, line, kind) where kind is 'prose', 'shell', or 'code'."""
    fence_lang = None
    for lineno, line in enumerate(lines, 1):
        match = FENCE.match(line)
        if match:
            fence_lang = None if fence_lang is not None else match.group(2).lower()
            continue
        if fence_lang is None:
            yield lineno, line, "prose"
        elif fence_lang in SHELL_LANGS:
            yield lineno, line, "shell"
        else:
            yield lineno, line, "code"


def instruction_lines(path: Path, lines: list[str]) -> list[tuple[int, str]]:
    """Lines treated as executable instructions.

    Markdown prose may discuss commands; only fenced code blocks count. Every
    line of a non-Markdown text file counts.
    """
    if path.suffix.lower() not in MARKDOWN_SUFFIXES:
        return list(enumerate(lines, 1))
    return [(lineno, line) for lineno, line, kind in markdown_segments(lines) if kind != "prose"]


def command_lines(path: Path, lines: list[str]) -> list[tuple[int, str]]:
    """Lines where a CLI command or migration counts as implemented.

    In Markdown that is prose plus shell fences; other-language fences (for
    example a Python test fixture quoted in a design document) are not
    commands a visitor is told to run.
    """
    if path.suffix.lower() not in MARKDOWN_SUFFIXES:
        return list(enumerate(lines, 1))
    return [(lineno, line) for lineno, line, kind in markdown_segments(lines) if kind != "code"]


class Report:
    def __init__(self) -> None:
        self.violations: list[str] = []

    def add(self, category: str, location: str, note: str = "") -> None:
        suffix = f" ({note})" if note else ""
        self.violations.append(f"{category}: {location}{suffix}")


def check_tree_layout(root: Path, report: Report) -> None:
    for child in sorted(root.iterdir()):
        if child.name in SKIP_DIRS:
            continue
        if child.is_dir() and child.name in FORBIDDEN_TREES:
            report.add("forbidden implementation tree", f"{child.name}/", "Community carries no build or packaging source")
        if child.is_file() and child.name in ENTERPRISE_PROJECT_FILES:
            report.add("enterprise project file", child.name, "must not be copied into Community")


def first_match(patterns, text: str) -> bool:
    return any(pattern.search(text) for pattern in patterns)


def check_leakage(rel: str, lines: list[str], report: Report) -> None:
    for lineno, line in enumerate(lines, 1):
        loc = f"{rel}:{lineno}"
        if first_match(PRIVATE_REPO_PATTERNS, line):
            report.add("private repository reference", loc)
        if first_match(OBSOLETE_LANGUAGE_PATTERNS, line):
            report.add("obsolete boundary language", loc)
        if STAGING_TAG.lower() in line.lower():
            report.add("staging tag as release input", loc)
        if PRIVATE_KEY_BLOCK.search(line):
            report.add("Community CI signing material", loc, "private-key block")


def check_cli_naming(path: Path, rel: str, lines: list[str], report: Report) -> None:
    for lineno, line in command_lines(path, lines):
        loc = f"{rel}:{lineno}"
        if FORBIDDEN_COMMAND_PATTERN.search(line) and not FORBIDDEN_COMMAND_EXEMPT.search(line):
            report.add("Community CLI naming", loc, NAMING_RULE)
        if first_match(CLI_RENAME_CODE_PATTERNS, line):
            report.add("CLI rename migration code", loc, "Community carries no CLI implementation to rename")
        if V010_CRAWLER_CLAIM.search(line):
            report.add("v0.1.0 archive honesty", loc, ARCHIVE_RULE)


def check_publication(path: Path, rel: str, text: str, lines: list[str], report: Report) -> None:
    if path.name in RELEASE_METADATA_FILES and text.strip() not in EMPTY_METADATA:
        report.add("release publication", rel, "nonempty release metadata")
    if path.suffix.lower() in STRUCTURED_SUFFIXES and PUBLISHED_METADATA_KEY.search(text):
        report.add("release publication", rel, "published release metadata")
    for lineno, line in instruction_lines(path, lines):
        if first_match(PUBLISH_COMMAND_PATTERNS, line):
            report.add("release publication", f"{rel}:{lineno}", "publish or tag instruction")


def check_workflow(path: Path, rel: str, text: str, lines: list[str], report: Report) -> None:
    if path.name in FACTORY_WORKFLOWS:
        report.add("copied factory workflow", rel)
    if RELEASE_WORKFLOW_NAME.search(path.stem) or RELEASE_WORKFLOW_CONTENT.search(text):
        report.add("release publication", rel, "release workflow")
    for lineno, raw in enumerate(lines, 1):
        line = strip_yaml_comment(raw)
        loc = f"{rel}:{lineno}"
        if first_match(CI_SIGNING_PATTERNS, line):
            report.add("Community CI signing material", loc)
        if first_match(FACTORY_LANGUAGE, line):
            report.add("copied factory workflow", loc)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"usage: {Path(argv[0]).name} <repo-root>", file=sys.stderr)
        return 2
    root = Path(argv[1]).resolve()
    if not root.is_dir():
        print(f"error: {root} is not a directory", file=sys.stderr)
        return 2

    report = Report()
    check_tree_layout(root, report)

    scanned = 0
    for path in iter_files(root):
        text = read_text(path)
        if text is None:
            continue
        scanned += 1
        rel = path.relative_to(root).as_posix()
        lines = text.splitlines()
        check_leakage(rel, lines, report)
        # The checker and its tests hold non-sensitive rejection fixtures (publish
        # commands, rename commands, CI signing snippets). They are still scanned
        # for leakage above: private repository, obsolete language, staging tag.
        if rel in SELF_PATHS:
            continue
        check_cli_naming(path, rel, lines, report)
        check_publication(path, rel, text, lines, report)
        if is_workflow(root, path):
            check_workflow(path, rel, text, lines, report)

    if report.violations:
        print(f"FAIL: {len(report.violations)} Community policy violation(s) in {root}")
        for violation in report.violations:
            print(f"  - {violation}")
        return 1

    print(f"PASS: {root} satisfies the Community policy (text files scanned: {scanned})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
