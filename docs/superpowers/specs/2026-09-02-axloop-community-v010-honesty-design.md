# AxLoop Community v0.1.0 Visitor-Docs Honesty Design

**Date:** 2026-09-02  
**Status:** Ready for GitHub COMMENT review  
**Repository:** `axloop/axloop-community`  
**Base:** `81c55c0eebee70d6e4364dda24605f0c435f722d`

## Problem

AxLoop Community has a live public v0.1.0 release, but the visitor-facing README, changelog, and release guide still say that no release has been published. A stranger following those documents receives a false account of the product and no direct path to the available Mac Apple Silicon build.

The honesty change makes the published release the single visitor contract. It does not alter the application, build a release, add automation, or expand platform availability.

## Design decision

Use a contract-first documentation change. First invert the real-file assertions in `VisitorJourneyTests` so the old unpublished story fails. Then update the three visitor documents together until the new contract passes. Keep the existing checker fail-closed and leave its fixture trees alone: an unpublished mini README inside a checker fixture is test input, not the live visitor contract.

This is preferable to a prose-only edit because the false claim could return unnoticed. It is also preferable to release or workflow work because v0.1.0 is already live and this change exists only to describe that fact accurately.

## Source-of-truth release facts

- Version and tag: `v0.1.0`
- Release ID: `381577289`
- Published: `2026-09-02T21:12:15Z`
- State: public, final, and not a prerelease
- Title: `AxLoop Community 0.1.0 for Mac (Apple Silicon)`
- Release page: https://github.com/axloop/axloop-community/releases/tag/v0.1.0
- Latest-release path: https://github.com/axloop/axloop-community/releases/latest
- Available platform: Mac with Apple Silicon only, represented by `darwin-arm64`
- Archive: `axloop-community-darwin-arm64-3a7bfeeb.tar.gz`, 44,950,048 bytes
- Archive SHA-256: `27e993467ee3b57c891c416ab5963032020b38218f2c57d890f094f791ca2043`
- Checksum asset: `axloop-community-darwin-arm64-3a7bfeeb-SHA256SUMS`, 112 bytes
- Checksum-asset SHA-256: `17970d7b67f9e87cf972da7e9289f7e8cf0a1b0a42b4cc827032a041fcb18a22`
- Enterprise destination: https://www.axloop.ai

No Linux or Windows artifact is published. The documentation must not imply otherwise.

## Visitor journey

The named visitor is a stranger arriving at the repository README. The README's `First run` path must let that visitor:

1. Open https://github.com/axloop/axloop-community/releases/latest.
2. Download `axloop-community-darwin-arm64-3a7bfeeb.tar.gz` and the adjacent `axloop-community-darwin-arm64-3a7bfeeb-SHA256SUMS`.
3. Confirm that the archive SHA-256 is `27e993467ee3b57c891c416ab5963032020b38218f2c57d890f094f791ca2043`.
4. Unpack the archive.
5. Run `bin/axloop-community` from the unpacked directory.

The path must say plainly that the release is for Mac Apple Silicon only. It must retain the enterprise destination at https://www.axloop.ai. It must not turn source checkout or a network command into an installation method, and the README must contain no fenced code blocks.

## Document contracts

### `README.md`

Replace the unpublished claim with a concise `First run` section implementing the named visitor journey. Use ordinary prose, a Markdown list, links, and inline code only. Identify v0.1.0 as published and identify the artifact as `darwin-arm64` for Mac Apple Silicon only.

### `CHANGELOG.md`

Keep the Keep a Changelog structure. Preserve `## [Unreleased]` for work after v0.1.0 and add `## [0.1.0] - 2026-09-02` for the first `darwin-arm64` install. Remove the claim that no release is published. Release-link definitions, if present, must resolve v0.1.0 to its public release page and Unreleased to comparison from v0.1.0.

### `docs/COMMUNITY_RELEASES.md`

State that v0.1.0 is published for `darwin-arm64` only and link to the latest-release path. Describe the archive, adjacent checksum asset, verification value, unpack step, and executable consistently with the README. State that this documentation change creates no release, tag, workflow, or Linux or Windows asset.

## Test design

Only `VisitorJourneyTests` in `tests/test_community_split.py` own assertions about the real README, changelog, and Community release guide. Invert those assertions before editing the documents.

The visitor tests must fail when any of these regressions occurs:

- A real visitor document says the release is unpublished or says no release has been published.
- `v0.1.0`, `darwin-arm64`, or the latest-release path is missing from the documents where the visitor needs it.
- The README omits either asset, the archive SHA-256, `bin/axloop-community`, or the enterprise destination.
- A document affirmatively claims a Linux or Windows release or asset is published or available.
- A scanned document contains a reference to the private factory or a staging tag.
- The README contains a fenced code block or presents clone, pip, or curl commands as installation.

The existing sensitive-value tests must continue assembling protected values from fragments inside the test or checker. Those values must not be copied into this design, the plan, or visitor prose. Existing fixture trees may keep their intentionally unpublished mini README because they exercise checker behavior rather than the live journey.

The red phase is successful only when the inverted `VisitorJourneyTests` fail against the locked main documentation for the expected honesty reasons. The green phase is successful only when the same tests pass after all three visitor documents are updated. The complete Community test suite and `scripts/check-community-split.py` must then pass without weakening any fail-closed rule.

## Scope and safety boundaries

- Documentation-contract work only; no application runtime changes.
- Do not add `.github` or any workflow.
- Do not publish or modify a release, create a tag, or add an asset.
- Do not describe Linux or Windows as available.
- Do not add signing material. Signing material never belongs in Community CI.
- Do not add a reference to the private factory, an obsolete location slogan, a staging-tag value, tracking parameters, or a private-key block.
- Do not merge leftover plan PR #1 or #3 into this work.
- Jules remains off. Nolan participates only if a workflow appears; no workflow is planned.
- Do not invent pack versions.

## Delivery and approval

The plan and design land under `docs/superpowers/` on `axloop/axloop-community`, based on `81c55c0eebee70d6e4364dda24605f0c435f722d`. Kit must GitHub COMMENT-sign the plan before execution; a GitHub `APPROVE` review is not the gate because the login `ajrrac` is shared. Kit does not write application code.

After that COMMENT exists, Elena launches Cursor cloud Claude Fable 5.1 (`claude-fable-5-1`) at effort low against Community main. Abe alone controls any later merge decision.

| Reviewer | GitHub COMMENT |
| --- | --- |
| Imani | |
| Reed | |
| Kit | |

## Acceptance criteria

The change is accepted when the stranger path is complete and consistent across the three visitor documents, the old unpublished story fails under the inverted tests, v0.1.0 passes as the sole published Mac Apple Silicon release, protected boundaries remain fail-closed, and the change contains no application, workflow, release, tag, or platform-expansion work.
