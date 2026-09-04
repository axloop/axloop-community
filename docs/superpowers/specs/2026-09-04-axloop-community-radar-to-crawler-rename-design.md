# Axloop Community Radar-to-Crawler Rename Design

**Date:** 2026-09-04
**Repository:** `axloop/axloop-community`
**Base:** `main` at `c529ff68c9d21a791726bb7364844b463c8f9df7` (after honesty #7 squash)
**Decision owner:** Abe

## Purpose

Adopt `axloop-crawler` as the canonical user-visible Community CLI, command, MCP, and future-release name. This change removes the former prohibition on the crawler name without rewriting published history or implying that an unreleased binary already exists.

## Naming Contract

- `axloop-crawler` is the approved user-visible name going forward in Community documentation, command examples, MCP copy, release guidance, policy checks, and tests.
- `axloop-radar` must not appear as the Community user-facing CLI name. The similarly named Factory implementation in `ascendantventures/axloop-edge-poc` is separate and out of scope.
- Published Community v0.1.0 still contains `bin/axloop-community`. Any discussion of that archive must say so explicitly.
- The current v0.1.0 archive must never be described as containing `axloop-crawler`.
- A future release may ship the approved name, but creating or publishing that release is outside this change.
- The Unreleased changelog records the approved rename intent and contains no claim that the rename was delivered in v0.1.0.
- “Deferred,” “later,” and equivalent postponement language about this rename is removed.

## Scope

Only documentation and policy tests in `axloop/axloop-community` change:

- `README.md`
- `CHANGELOG.md`
- `docs/COMMUNITY_RELEASES.md`
- existing Community MCP or command documentation discovered in the repository
- `scripts/check-community-split.py`
- `tests/test_community_split.py`

There is no Community application runtime source tree to rename. No `src/` implementation, console-script packaging, release artifact, or distribution metadata is introduced.

The following are explicitly excluded:

- `ascendantventures/axloop-edge-poc`, including its `axloop-radar` console script and `src/axloop_radar`
- `axloop/homebrew-axloop-community`, whose cask currently ships `bin/axloop-community`
- publishing, cutting a release, changing a tap, merging, or opening a pull request
- changes to the canonical README or tests during this design-and-plan-only phase

## Considered Approaches

### 1. Contract-first documentation and policy rename — selected

Invert the Community policy tests first, observe the expected red state, then align documentation and the split checker with the naming contract. This makes the intended public contract executable and preserves a clear red/green sequence.

### 2. Documentation-only search and replace

This is smaller, but it leaves tests enforcing the old command and risks inaccurate edits to historical v0.1.0 statements. It does not meet the requirement to lift the existing crawler-name ban.

### 3. Cross-repository runtime and distribution rename

Changing Edge POC packaging, the Homebrew tap, or publishing a new Community archive could align artifacts immediately, but it expands authority and contradicts the repository and release boundaries. It is rejected.

## Design

### Policy tests

`tests/test_community_split.py` becomes the executable naming contract. Tests that currently reject a crawler rename are inverted to require `axloop-crawler` in current Community user-facing documentation and to reject `axloop-radar` as the Community CLI name. Separate assertions preserve the historical fact that v0.1.0 ships `bin/axloop-community` and reject claims that the v0.1.0 tarball contains `axloop-crawler`.

The initial test-only edit must fail against the unchanged documentation/checker. That failure is intentional evidence that the test inversion detects the old contract.

### Split checker

`scripts/check-community-split.py` must enforce the same contract as the tests. Its messages and checks must no longer treat `axloop-crawler` as forbidden or deferred. It must identify `axloop-radar` as forbidden Community user-facing CLI copy while permitting references that clearly identify the excluded Factory repository, if such references are necessary for scope or migration honesty.

Historical v0.1.0 checks remain distinct from forward-looking naming checks: `bin/axloop-community` is valid only when describing the published v0.1.0 archive, not as the canonical command going forward.

### User and release documentation

Current usage instructions, examples, MCP/command copy, and forward-looking release instructions use `axloop-crawler`. `CHANGELOG.md` adds an Unreleased entry that announces the approved user-visible rename and states that no new release is part of this work.

Where v0.1.0 is discussed, the text states that the published archive still ships `bin/axloop-community` and will remain so until a new release. The wording must not suggest that an existing archive has changed in place.

### Repository-wide discovery

Implementation begins with a scoped text inventory inside `axloop/axloop-community`. Each match for `axloop-radar`, `axloop-crawler`, `axloop-community`, “deferred,” and “later” is classified as current user-facing copy, historical archive truth, test policy, checker policy, or unrelated prose. Only matches governed by this design are edited.

## Verification

The implementation uses a red-then-green sequence:

1. Invert and add focused tests in `tests/test_community_split.py`.
2. Run those tests and confirm they fail because current docs/checker still enforce or present the old contract.
3. Update the checker and allowed documentation.
4. Run the focused test file and the checker to green.
5. Search the Community repository for forbidden or misleading naming and postponement language.
6. Run the full existing test suite, without publishing or modifying external repositories.

Success means current Community-facing copy consistently names `axloop-crawler`, Community-facing `axloop-radar` copy is absent, v0.1.0 archive statements remain truthful, and all Community policy checks pass.

## Review and Release Gates

| Gate owner | Status | Evidence / comment |
| --- | --- | --- |
| Imani |  |  |
| Reed |  |  |
| Kit |  |  |

Elena launches Fable only after Kit leaves a `COMMENT`. No merge occurs unless Abe explicitly says to merge. Publishing and release creation remain out of scope regardless of gate status.

## Handoff

Implement only from the companion plan at `docs/superpowers/plans/2026-09-04-axloop-community-radar-to-crawler-rename.md`. Begin from the stated Community base, keep every edit within the allowlist, preserve the v0.1.0 archive distinction in review, and stop after verified local changes for the named reviewers and gates. Do not open a PR, merge, publish, or alter either excluded repository.
