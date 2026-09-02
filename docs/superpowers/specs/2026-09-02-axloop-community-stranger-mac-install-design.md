# AxLoop Community Stranger-First Mac Install Design

**Date:** 2026-09-02  
**Repository:** `axloop/axloop-community`  
**Base:** `81c55c0eebee70d6e4364dda24605f0c435f722d`  
**Status:** Design for a later docs-and-tests change; this stream does not publish an installer

## Purpose

Make the public Community installation path honest and usable for a stranger on a Mac with Apple silicon. The visitor should open [the latest Community release](https://github.com/axloop/axloop-community/releases/latest), download the published installer, open it in Finder, and run Community without using Terminal setup commands.

Enterprise remains at [axloop.ai](https://www.axloop.ai).

## Recommendation

Publish a notarized Apple Silicon `.pkg` installer that Finder can open, then update the Community visitor contract only after that package is actually present on the latest public release.

Three delivery shapes were considered:

- **Notarized `.pkg` (recommended):** gives macOS a native, Finder-first installation path and can carry the already-verified bundle.
- **Archive or unsigned app bundle (rejected):** can still force a stranger into unpacking or quarantine-removal work.
- **Shell bootstrap (rejected):** still requires command-line download or shell execution.

Nolan owns the attended Developer ID packaging and notarization gate. The private factory supplies the payload and writes `manifest.sig` before packaging; notarization wraps that already-verified bundle and does not replace its verification. Community CI does not sign or notarize anything. This design adds no workflow, credential, key, or signing material.

## Current Truth and Hard Stop

At design time, the live latest release is `v0.1.0`. Its only install payload is the `darwin-arm64` archive with an adjacent checksum file. It is not the Finder installer described by the target journey.

This work does not replace that release. The later writer must stop without changing visitor tests or copy unless all of these conditions are true:

1. Kit has COMMENT-signed this plan on GitHub after Imani and Reed. A review approval is not the gate because the login is shared.
2. Nolan has confirmed that the published Apple Silicon package is the notarized package intended for the stranger path.
3. The public latest-release page visibly offers that package as a published asset.
4. The package has been opened from Finder and used to run Community on Apple Silicon without Terminal setup.
5. The asset is not the `v0.1.0` archive or its checksum file relabeled as an installer.

If any condition fails, the writer reports the blocker and makes no visitor-contract edit. Abe alone controls any later publication. The separate honesty stream may document the current archive path; it is not merged into this work.

## Boundaries

| Boundary | Responsibility |
|---|---|
| The private factory | Produces the Community payload and its existing signed manifest. It is not named, copied, or transferred into Community. |
| Nolan's packaging gate | Produces and notarizes the Apple Silicon package outside Community CI and supplies evidence that Finder can open it. |
| Abe's publication gate | Controls whether a later installer is published. This design does not publish or modify a release. |
| Community visitor contract | After the hard stop clears, describes the public Finder-first path in `README.md`, `CHANGELOG.md`, and `docs/COMMUNITY_RELEASES.md`. |
| Community tests | Enforce the visitor contract against real repository files while retaining the existing fail-closed checker and fixture trees. |

No `.github` change is part of this design. There is no Community packaging workflow. Kit does not write application code. Jules is not involved.

## Visitor Journey

The successful journey is deliberately short:

1. The visitor uses a Mac with Apple silicon.
2. The visitor opens `https://github.com/axloop/axloop-community/releases/latest` in a browser.
3. The visitor downloads the published Apple Silicon installer.
4. The visitor opens the installer in Finder and follows the macOS prompts.
5. The visitor opens and runs AxLoop Community.

The visitor does not clone a repository, install a Python package, download through a shell command, unpack an archive, calculate a checksum, remove quarantine attributes, or pass diagnostic bypass flags.

The README contains no fenced code blocks. It presents the Finder journey as installation, not an alternate developer path. It claims no other operating-system release. It links Enterprise visitors only to `https://www.axloop.ai`.

## Documentation Contract

After the hard stop clears:

- `README.md` is the minimal stranger path: latest release, published Apple Silicon installer, Finder, run, and the Enterprise link. It has no code fences and no source- or shell-based install path.
- `CHANGELOG.md` records the visitor-path change under its existing unreleased area without inventing a package version or rewriting historical release facts.
- `docs/COMMUNITY_RELEASES.md` explains that Community's public install surface is GitHub Releases, the visitor-facing artifact is a notarized Apple Silicon installer, Nolan owns packaging/notarization, and Community contains neither signing material nor a signing workflow.

Historical text may truthfully describe the `v0.1.0` archive, but no paragraph, heading, list item, or table row may call that archive a Finder installer or imply it satisfies this journey.

## Test Design

TDD applies only to real-file tests in `VisitorJourneyTests` within `tests/test_community_split.py`:

1. Invert the current real-file visitor assertions first.
2. Run that class and observe failures caused by the current README and release documentation.
3. Change only `README.md`, `CHANGELOG.md`, and `docs/COMMUNITY_RELEASES.md` to make those assertions pass.
4. Run the focused class, the complete test module, and the existing fail-closed checker.

The tests fail when:

- the README First run section still requires `curl`, `shasum`, `tar`, `xattr`, or doctor flags;
- the README contains a fenced code block or presents clone, pip, or `curl` as installation;
- visitor documentation claims a Linux or Windows artifact is published;
- visitor files expose a GitHub reference to the private factory or any staging tag;
- copy describes the `v0.1.0` archive as the live Finder installer; or
- an instruction line introduces a release-publication or tag-publication command.

The existing checker remains fail-closed and unchanged. Existing fixture trees remain unchanged, including fixtures that intentionally model unpublished or archive-shaped READMEs. Sensitive forbidden values remain assembled from existing fragments; this work does not literalize them in tests or documentation.

## Delivery Workflow

This design and its implementation plan are docs-only artifacts based on `81c55c0eebee70d6e4364dda24605f0c435f722d`. They do not incorporate leftover plan pull requests #1 or #3, or the separate honesty pull request #5.

After the required GitHub COMMENT sequence and only after the hard stop clears, Elena launches Cursor cloud Claude Fable 5.1 (`claude-fable-5-1`) at effort low against `axloop/axloop-community` main. Elena changes only the four visitor-contract files named in this design. The implementation does not change runtime code, release automation, signing, or packaging.

## Acceptance Criteria

- A stranger can follow the five-step Finder journey from the latest public release on Apple Silicon.
- The public release actually contains Nolan's notarized installer before the docs claim it does.
- The README has no code fences or Terminal-based installation path.
- The three visitor documents claim only the published Apple Silicon surface and preserve the Enterprise destination.
- Real-file `VisitorJourneyTests` enforce every negative contract above.
- The fail-closed checker and all fixture trees are preserved.
- Only `tests/test_community_split.py`, `README.md`, `CHANGELOG.md`, and `docs/COMMUNITY_RELEASES.md` change during later implementation.
- No release, tag, workflow, `.github` file, signing material, package version, or application code is added by this stream.

## Out of Scope

- Packaging, notarization, or publication itself
- Any replacement release or extra asset upload
- Community CI changes
- Runtime or QC redesign
- Other operating-system artifacts
- The separate archive-honesty stream
- Any merge without Abe's direction
