# Axloop Community Radar-to-Crawler Rename Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `axloop-crawler` the canonical user-visible Community command while preserving the exact published v0.1.0 `bin/axloop-community` archive truth.

**Architecture:** Treat naming as a documentation-and-policy contract within `axloop/axloop-community`. Invert the contract tests first to produce a deliberate red result, then update the split checker and user/release documentation until focused and full verification are green; no runtime or release artifact is created.

**Tech Stack:** Markdown, Python 3, pytest, repository-native `scripts/check-community-split.py`, ripgrep

## Global Constraints

- Required repository and complete write boundary: `axloop/axloop-community` only.
- Required base: `main` at `c529ff68c9d21a791726bb7364844b463c8f9df7` (after honesty #7 squash).
- Allowlist: `README.md`, `CHANGELOG.md`, `docs/COMMUNITY_RELEASES.md`, existing Community MCP/command documentation, `scripts/check-community-split.py`, and `tests/test_community_split.py`.
- Forbidden repositories: `ascendantventures/axloop-edge-poc` and `axloop/homebrew-axloop-community`.
- Do not change the Factory `axloop-radar` console script or `src/axloop_radar`.
- Do not change the Homebrew cask that ships `bin/axloop-community`.
- Do not add application runtime code; this Community repository has no `src/` runtime implementation.
- Do not publish, cut a release, alter an archive, open a pull request, or merge as part of implementation.
- Exact forward-looking naming contract: `axloop-crawler` is the canonical Community user-visible binary, command, MCP, and future-release name.
- Exact negative naming contract: `axloop-radar` is not the Community user-facing CLI name.
- Exact historical contract: the published v0.1.0 archive still ships `bin/axloop-community`, not `axloop-radar` or `axloop-crawler`.
- Never claim that the published v0.1.0 tarball now contains `axloop-crawler`.
- The Unreleased changelog must record rename intent; remove “deferred,” “later,” and equivalent postponement language for this rename.
- Elena launches Fable only after Kit leaves a `COMMENT`.
- No merge unless Abe explicitly says to merge.

---

### Task 1: Inventory the Community Naming Surface

**Files:**
- Inspect: `README.md`
- Inspect: `CHANGELOG.md`
- Inspect: `docs/COMMUNITY_RELEASES.md`
- Inspect: `docs/**`
- Inspect: `scripts/check-community-split.py`
- Inspect: `tests/test_community_split.py`

**Interfaces:**
- Consumes: the Global Constraints and naming contract above
- Produces: a scoped list of existing files and exact passages governed by the rename

- [ ] **Step 1: Confirm the expected Community files exist**

Run:

```bash
for path in README.md CHANGELOG.md docs/COMMUNITY_RELEASES.md scripts/check-community-split.py tests/test_community_split.py; do
  test -f "$path" || { printf 'missing required file: %s\n' "$path" >&2; exit 1; }
done
```

Expected: exit 0 with no output.

- [ ] **Step 2: Inventory all naming and postponement language in the allowlisted tree**

Run:

```bash
rg -n -i 'axloop-radar|axloop-crawler|bin/axloop-community|defer(red)?|later' \
  README.md CHANGELOG.md docs scripts/check-community-split.py tests/test_community_split.py
```

Expected: matches showing the existing `bin/axloop-community` instructions and the current tests/checker that reject or defer `axloop-crawler`; no files outside the Community repository.

- [ ] **Step 3: Identify existing MCP and command documentation without inventing new files**

Run:

```bash
rg -l -i 'mcp|command|cli|bin/axloop-community|axloop-radar|axloop-crawler' README.md CHANGELOG.md docs
```

Expected: a list of existing documentation files. Add only files from this result that contain user-visible command, MCP, or release copy to the later documentation edit; do not create a speculative MCP document.

- [ ] **Step 4: Record the inventory in the implementation session notes**

Record each match under exactly one classification: `current user-facing`, `v0.1.0 archive history`, `test policy`, `checker policy`, or `out-of-scope/reference-only`.

Expected: every match from Step 2 is classified, and only the first four classifications can lead to an edit.

### Task 2: Invert the Naming Contract Tests (Red)

**Files:**
- Modify: `tests/test_community_split.py`
- Test: `tests/test_community_split.py`

**Interfaces:**
- Consumes: the inventory from Task 1 and repository-native test helpers already defined in `tests/test_community_split.py`
- Produces: executable assertions for canonical `axloop-crawler`, forbidden Community-facing `axloop-radar`, and truthful v0.1.0 `bin/axloop-community` history

- [ ] **Step 1: Replace the old crawler-rejection expectations with the forward-looking contract**

Edit the existing naming-policy tests, reusing their repository reader/helper, so their assertions express this complete contract:

```python
assert "axloop-crawler" in current_user_facing_copy
assert "axloop-radar" not in current_user_facing_copy
assert "bin/axloop-community" in published_v010_copy
assert "v0.1.0" in published_v010_copy
```

Keep `current_user_facing_copy` limited to current CLI, MCP, and future-release instructions. Keep `published_v010_copy` limited to the paragraph or section describing the already-published v0.1.0 archive, so the historical binary does not become an accepted current command.

- [ ] **Step 2: Add an explicit anti-rewrite assertion for v0.1.0**

Using the same helper style as the existing test file, add an assertion equivalent to:

```python
assert "v0.1.0 archive ships `bin/axloop-crawler`" not in published_v010_copy
assert "v0.1.0 archive ships `axloop-crawler`" not in published_v010_copy
```

If the project normalizes Markdown punctuation before assertions, apply the existing normalization helper and assert the same semantic sentences in normalized form.

- [ ] **Step 3: Remove obsolete deferral-policy assertions**

Delete only assertions that require the crawler rename to be “deferred,” happen “later,” or remain forbidden. Do not weaken unrelated Community/Factory separation assertions.

- [ ] **Step 4: Run the focused tests to verify red**

Run:

```bash
pytest -q tests/test_community_split.py
```

Expected: FAIL because unchanged current documentation and/or checker copy still names `bin/axloop-community`, rejects `axloop-crawler`, or describes the rename as deferred. A collection error or unrelated exception is not an acceptable red result.

- [ ] **Step 5: Preserve red evidence for review**

Record the failing test names and assertion messages in the implementation handoff.

Expected: the evidence connects each failure to the old naming contract, not to broken test setup.

### Task 3: Align the Split Checker with the New Contract

**Files:**
- Modify: `scripts/check-community-split.py`
- Test: `tests/test_community_split.py`

**Interfaces:**
- Consumes: the inverted tests from Task 2
- Produces: repository policy that permits/requires Community-facing `axloop-crawler`, rejects Community-facing `axloop-radar`, and preserves v0.1.0 archive honesty

- [ ] **Step 1: Locate the exact checker rules and messages to invert**

Run:

```bash
rg -n -i 'axloop-radar|axloop-crawler|bin/axloop-community|defer(red)?|later' scripts/check-community-split.py
```

Expected: only the policy constants, patterns, or diagnostics identified in Task 1.

- [ ] **Step 2: Invert the current-name rule with the existing checker structure**

Change the relevant existing constants/patterns so their literal values implement:

```python
CANONICAL_COMMUNITY_COMMAND = "axloop-crawler"
FORBIDDEN_COMMUNITY_COMMAND = "axloop-radar"
PUBLISHED_V010_BINARY = "bin/axloop-community"
```

Use the existing names if the checker already defines equivalent constants; do not add a second policy layer. Limit the forbidden-name scan to Community user-facing CLI/MCP/current-release copy so a clearly labeled statement about the excluded Factory repository is not misclassified.

- [ ] **Step 3: Update checker diagnostics**

Make each affected diagnostic state the violated rule directly:

```text
axloop-crawler is the canonical Community user-visible command
axloop-radar must not be presented as the Community user-facing CLI
published v0.1.0 must remain documented as shipping bin/axloop-community
```

Remove diagnostics that call this rename deferred or later.

- [ ] **Step 4: Run the focused tests**

Run:

```bash
pytest -q tests/test_community_split.py
```

Expected: still FAIL only on documentation expectations that Task 4 will update; checker-policy expectations now PASS.

### Task 4: Make User and Release Documentation Green

**Files:**
- Modify: `README.md`
- Modify: `CHANGELOG.md`
- Modify: `docs/COMMUNITY_RELEASES.md`
- Modify if identified in Task 1: existing `docs/**` files containing Community MCP/command copy
- Test: `tests/test_community_split.py`

**Interfaces:**
- Consumes: Task 1 inventory and the executable naming contract from Tasks 2–3
- Produces: consistent current `axloop-crawler` usage plus explicit v0.1.0 archive honesty

- [ ] **Step 1: Update current README command and MCP copy**

Replace current user instructions and examples that invoke `bin/axloop-community` or present `axloop-radar` as the Community command with `axloop-crawler`. Preserve or add one concise historical note with this meaning:

```markdown
`axloop-crawler` is the approved user-visible Community CLI name going forward. The published v0.1.0 archive still ships `bin/axloop-community`; it will remain unchanged until a new release is cut. Cutting that release is outside this change.
```

Do not place `axloop-crawler` inside a sentence claiming what the v0.1.0 archive contains.

- [ ] **Step 2: Add the Unreleased changelog entry**

Under the existing Unreleased heading, adapt to the file's list style and add:

```markdown
- Rename the approved user-visible Community CLI, command, and MCP name to `axloop-crawler`. The already-published v0.1.0 archive remains unchanged and still ships `bin/axloop-community`; no release is published by this change.
```

Remove any Unreleased statement saying the radar-to-crawler rename is deferred or will be decided later. Do not edit the historical v0.1.0 release record to claim a different artifact.

- [ ] **Step 3: Update Community release guidance**

Make future-facing command, MCP, and next-release examples in `docs/COMMUNITY_RELEASES.md` use `axloop-crawler`. Keep the historical v0.1.0 passage explicit:

```markdown
The published v0.1.0 archive still ships `bin/axloop-community`; it does not contain `axloop-crawler`. `axloop-crawler` is the approved user-visible name for a future release, which is not created or published here.
```

- [ ] **Step 4: Update only discovered MCP/command documentation**

For each existing file classified as current user-facing in Task 1, change invocations, headings, and prose to `axloop-crawler`. Do not alter references that solely document the out-of-scope Factory `axloop-radar`, and do not add new docs just to broaden scope.

- [ ] **Step 5: Remove rename-specific postponement language**

Run:

```bash
rg -n -i 'axloop.{0,40}(defer(red)?|later)|(defer(red)?|later).{0,40}axloop' README.md CHANGELOG.md docs scripts/check-community-split.py tests/test_community_split.py
```

Expected: no match that describes the Community radar-to-crawler rename as deferred or later. A match about an unrelated subject must remain untouched and be recorded as unrelated.

- [ ] **Step 6: Run the focused test file to verify green**

Run:

```bash
pytest -q tests/test_community_split.py
```

Expected: PASS.

- [ ] **Step 7: Run the repository-native split checker**

Run:

```bash
python3 scripts/check-community-split.py
```

Expected: exit 0 with the checker's normal success output and no crawler-ban, radar-as-Community-CLI, or archive-honesty diagnostic.

### Task 5: Verify Scope, Honesty, and the Full Suite

**Files:**
- Verify: `README.md`
- Verify: `CHANGELOG.md`
- Verify: `docs/COMMUNITY_RELEASES.md`
- Verify: discovered Community MCP/command docs
- Verify: `scripts/check-community-split.py`
- Verify: `tests/test_community_split.py`

**Interfaces:**
- Consumes: all changes from Tasks 2–4
- Produces: review-ready local evidence; no PR, merge, release, or publication

- [ ] **Step 1: Verify canonical current naming**

Run:

```bash
rg -n 'axloop-crawler' README.md CHANGELOG.md docs scripts/check-community-split.py tests/test_community_split.py
```

Expected: current user-facing CLI/MCP/future-release copy and policy assertions consistently use `axloop-crawler`; no result claims the published v0.1.0 archive contains it.

- [ ] **Step 2: Verify forbidden Community-facing radar naming**

Run:

```bash
rg -n 'axloop-radar' README.md CHANGELOG.md docs scripts/check-community-split.py tests/test_community_split.py
```

Expected: no Community user-facing CLI usage. Permitted matches are limited to negative policy assertions/checker literals or clearly labeled facts about the excluded Factory repository.

- [ ] **Step 3: Verify v0.1.0 archive honesty**

Run:

```bash
rg -n -C 2 'v0\.1\.0|bin/axloop-community' README.md CHANGELOG.md docs scripts/check-community-split.py tests/test_community_split.py
```

Expected: every description of the published v0.1.0 archive says it still ships `bin/axloop-community`; no description says that archive now contains `axloop-crawler`.

- [ ] **Step 4: Run the full existing test suite**

Run:

```bash
pytest -q
```

Expected: PASS with no failures.

- [ ] **Step 5: Confirm the final file set against the allowlist without Git**

Compare the implementation session's editor/write log with this exact allowlist:

```text
README.md
CHANGELOG.md
docs/COMMUNITY_RELEASES.md
existing docs containing Community MCP/command copy identified in Task 1
scripts/check-community-split.py
tests/test_community_split.py
```

Expected: no created or modified path outside the allowlist and no write in either forbidden repository.

- [ ] **Step 6: Prepare the reviewer handoff**

Include the Task 2 red failures, Task 4 focused green result, Task 5 full-suite result, checker result, final naming search, and v0.1.0 honesty search. State explicitly: no publish, no release, no Homebrew change, no Edge POC change, no PR, and no merge.

## Review Gates

| Gate owner | Status | Evidence / comment |
| --- | --- | --- |
| Imani |  |  |
| Reed |  |  |
| Kit |  |  |

Elena launches Fable only after Kit leaves a `COMMENT`. No merge occurs unless Abe explicitly says to merge.

## Handoff

Give the implementer the design, this plan, the exact base SHA, and the Task 1 inventory. The implementer must complete the red/green evidence and stop with local, review-ready Community changes. Route the evidence through the blank Imani/Reed/Kit gates; after Kit leaves a `COMMENT`, Elena may launch Fable. Do not open a PR, merge, publish, cut a release, or touch `ascendantventures/axloop-edge-poc` or `axloop/homebrew-axloop-community` without a new explicit instruction from the authorized owner.
