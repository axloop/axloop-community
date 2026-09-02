#!/usr/bin/env python3
"""Verify that axloop/axloop-community stays a Releases home, not an enterprise factory copy.

Standard library only. Exit 0 when the tree is allowed; print every violation
and exit 1 otherwise. Each violation line is prefixed with its rule id:

  enterprise-tree          top-level enterprise directory copied into Community
  enterprise-project-file  enterprise project/metadata file copied into Community
  factory-workflow         enterprise factory workflow name under .github/workflows
  release-publish          a workflow path that can publish or un-draft a release
  staging-tag              community-acceptance-staging-2026-08-29 used in executable config
  cli-rename               radar->crawler rename implemented in code or workflow
  signing-key              private-key material, signing command, or key secret in CI
  enterprise-checkout      workflow checks out or downloads the enterprise repository
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ENTERPRISE_DIRS = {"src", "tools", "packaging", "hosted", "supabase", "acceptance", "release"}
ENTERPRISE_PROJECT_FILES = {"verify.py", "pyproject.toml", "setup.py", "DESIGN.md", "PRODUCT.md"}
FACTORY_WORKFLOWS = {
    "community-bundles.yml",
    "community-inputs.yml",
    "community-windows-input-review.yml",
    "community-acceptance.yml",
}
STAGING_TAG = "community-acceptance-staging-2026-08-29"
ENTERPRISE_REPO = "ascendantventures/axloop-edge-poc"

SKIP_DIRS = {".git", "__pycache__", ".venv", "node_modules"}
MARKDOWN_SUFFIXES = {".md", ".markdown", ".rst", ".txt"}

PUBLISH_PATTERNS = [
    re.compile(r"draft\s*:\s*(false|no|off|0)\b", re.I),
    re.compile(r"--draft\s*=\s*(false|0|no)\b", re.I),
    re.compile(r"\bgh\s+release\s+edit\b"),
    re.compile(r"\bgh\s+release\s+(create|upload)\b.*--(publish|latest)\b"),
    re.compile(r"\bpublish[_-]?release\b|\breleases?/publish\b|\bmake[_-]?latest\b", re.I),
    re.compile(r"\bprerelease\s*:\s*false\b.*\bdraft\b", re.I),
    re.compile(r"\bhub\s+release\s+edit\b|\bgithub-release\s+edit\b"),
    re.compile(r"\"draft\"\s*:\s*false", re.I),
]
RELEASE_CREATE = re.compile(r"\bgh\s+release\s+create\b")
DRAFT_FLAG = re.compile(r"--draft(\s|$|=true|\"|')")
ACTION_RELEASE_STEP = re.compile(r"uses:\s*[^#\n]*(gh-release|create-release|release-action)", re.I)

CLI_RENAME_PATTERNS = [
    re.compile(r"s/radar/crawler/"),
    re.compile(r"replace\(\s*['\"]radar['\"]\s*,\s*['\"]crawler['\"]\s*\)"),
    re.compile(r"\bgit\s+mv\b.*radar.*crawler"),
    re.compile(r"\b(mv|rename|ren)\b.*\bradar\b.*\bcrawler\b"),
    re.compile(r"\brename\b.*\bradar\b.*(->|→|to)\s*\bcrawler\b", re.I),
]
CLI_RENAME_DEFERRED = re.compile(r"\b(later|deferred|not part of this split|future)\b", re.I)

SIGNING_PATTERNS = [
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\bPKCS\s*#?\s*8\b", re.I),
    re.compile(r"\bed25519\b.*\b(key|sign)", re.I),
    re.compile(r"secrets\.[A-Za-z0-9_]*(SIGN|PRIVATE|PKCS|KEY)[A-Za-z0-9_]*", re.I),
    re.compile(r"\b(SIGNING|PRIVATE)_KEY\b"),
    re.compile(r"\bopenssl\s+(pkeyutl|dgst)\b.*-sign", re.I),
    re.compile(r"\bopenssl\s+pkcs8\b", re.I),
    re.compile(r"\b(gpg|minisign|cosign|signtool|codesign|rcodesign)\b.*\b(sign|-s\b)", re.I),
    re.compile(r"\bcommunity_signing_request\b"),
    re.compile(r"\bsigning[_-]?key\b", re.I),
]

ENTERPRISE_CHECKOUT_PATTERNS = [
    re.compile(r"repository\s*:\s*['\"]?" + re.escape(ENTERPRISE_REPO), re.I),
    re.compile(r"\bgit\s+clone\b.*" + re.escape(ENTERPRISE_REPO)),
    re.compile(r"github\.com/" + re.escape(ENTERPRISE_REPO)),
    re.compile(r"\bgh\s+(release|run)\s+download\b.*--repo\s+['\"]?" + re.escape(ENTERPRISE_REPO)),
    re.compile(r"--repo\s+['\"]?" + re.escape(ENTERPRISE_REPO)),
]


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


def is_markdown(path: Path) -> bool:
    return path.suffix.lower() in MARKDOWN_SUFFIXES


def read_lines(path: Path) -> list[str]:
    try:
        return path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as exc:  # pragma: no cover - defensive
        return [f"<<unreadable: {exc}>>"]


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


def check_tree_layout(root: Path, violations: list[str]) -> None:
    for child in sorted(root.iterdir()):
        if child.name in SKIP_DIRS:
            continue
        if child.is_dir() and child.name in ENTERPRISE_DIRS:
            violations.append(
                f"enterprise-tree: top-level '{child.name}/' belongs to {ENTERPRISE_REPO}; "
                "Community is the Releases home, not a copy of the factory"
            )
        if child.is_file() and child.name in ENTERPRISE_PROJECT_FILES:
            violations.append(
                f"enterprise-project-file: '{child.name}' is an enterprise project file and must not be copied"
            )


def check_workflow(root: Path, path: Path, violations: list[str]) -> None:
    rel = path.relative_to(root)
    if path.name in FACTORY_WORKFLOWS:
        violations.append(
            f"factory-workflow: {rel} is an enterprise factory workflow and must stay in {ENTERPRISE_REPO}"
        )

    lines = read_lines(path)
    code_lines = [strip_yaml_comment(line) for line in lines]

    for lineno, line in enumerate(code_lines, 1):
        loc = f"{rel}:{lineno}"
        for pattern in PUBLISH_PATTERNS:
            if pattern.search(line):
                violations.append(f"release-publish: {loc} can publish or un-draft a release: {line.strip()}")
                break
        if RELEASE_CREATE.search(line) and not DRAFT_FLAG.search(line):
            violations.append(f"release-publish: {loc} creates a release without --draft: {line.strip()}")
        if STAGING_TAG in line:
            violations.append(
                f"staging-tag: {loc} references {STAGING_TAG} in executable workflow configuration"
            )
        for pattern in CLI_RENAME_PATTERNS:
            if pattern.search(line):
                violations.append(f"cli-rename: {loc} implements radar->crawler rename (deferred): {line.strip()}")
                break
        for pattern in SIGNING_PATTERNS:
            if pattern.search(line):
                violations.append(f"signing-key: {loc} signing material or key secret in Community CI: {line.strip()}")
                break
        for pattern in ENTERPRISE_CHECKOUT_PATTERNS:
            if pattern.search(line):
                violations.append(f"enterprise-checkout: {loc} pulls enterprise source or artifacts: {line.strip()}")
                break

    # A release action step must set draft: true explicitly.
    for lineno, line in enumerate(code_lines, 1):
        if ACTION_RELEASE_STEP.search(line):
            window = "\n".join(code_lines[lineno - 1 : lineno + 15])
            if not re.search(r"draft\s*:\s*true\b", window):
                violations.append(
                    f"release-publish: {rel}:{lineno} release action step does not set 'draft: true' explicitly"
                )


def check_code_file(root: Path, path: Path, violations: list[str]) -> None:
    rel = path.relative_to(root)
    for lineno, line in enumerate(read_lines(path), 1):
        for pattern in CLI_RENAME_PATTERNS:
            if pattern.search(line) and not CLI_RENAME_DEFERRED.search(line):
                violations.append(f"cli-rename: {rel}:{lineno} implements radar->crawler rename (deferred): {line.strip()}")
                break
        if re.search(r"-----BEGIN [A-Z ]*PRIVATE KEY-----", line):
            violations.append(f"signing-key: {rel}:{lineno} contains private-key material")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"usage: {Path(argv[0]).name} <repo-root>", file=sys.stderr)
        return 2
    root = Path(argv[1]).resolve()
    if not root.is_dir():
        print(f"error: {root} is not a directory", file=sys.stderr)
        return 2

    # The checker and its unit tests intentionally contain forbidden strings as fixtures.
    self_files = {Path(__file__).resolve(), (root / "tests" / "test_community_split.py").resolve()}
    violations: list[str] = []
    check_tree_layout(root, violations)

    workflows = 0
    for path in iter_files(root):
        if path.resolve() in self_files:
            continue
        if is_workflow(root, path):
            workflows += 1
            check_workflow(root, path, violations)
        elif is_markdown(path):
            continue
        else:
            check_code_file(root, path, violations)

    if violations:
        print(f"FAIL: {len(violations)} Community boundary violation(s) in {root}")
        for violation in violations:
            print(f"  - {violation}")
        return 1

    print(
        f"PASS: {root} is a Community Releases home "
        f"(no enterprise tree, no publish path, no staging-tag input, no CLI rename, "
        f"no signing key; workflows checked: {workflows})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
