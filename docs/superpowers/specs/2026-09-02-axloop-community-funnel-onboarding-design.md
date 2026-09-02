# AxLoop Community Funnel and Onboarding Design

**Status:** Approved direction recorded by Abe and Kit on 2026-09-02; implementation awaits the review gate below.

**Baseline:** `axloop/axloop-community` `main` at `503de93d439f29fa2367d70b99da7d585d3363c5` (`503de93d`). Plan PR #1 is excluded and must not be merged into this work.

## Purpose

Make AxLoop Community understandable and useful to a stranger on first contact. The repository should present a polished Community product, explain the honest current release state, show where future installs will appear, and direct enterprise interest to <https://www.axloop.ai> without exposing private repository details.

## Recommended Design

Use a documentation-first funnel backed by a fail-closed repository policy checker. Rewrite the README around the visitor journey, make `CHANGELOG.md` and this repository's GitHub Releases page the release-discovery contract, simplify `docs/COMMUNITY_RELEASES.md` to describe that contract, and invert the existing checker/tests from requiring private provenance language to rejecting it everywhere in the Community tree.

This is preferable to either deleting the boundary checker or adding release automation. Deleting the checker would allow private provenance and prohibited capabilities to drift back in. Release automation would create publishing and signing surfaces before Community has an approved release to publish.

## Visitor Journey

The README is a styled Community landing page, not a legal memo about repository separation. Its content order is:

1. A concise product statement and a clear Community identity.
2. A first-run section that starts from this repository.
3. A link to this repository's GitHub Releases page as the future source of the latest install.
4. An explicit notice that no Community release is published yet, with no fabricated download or runnable installation command.
5. A short explanation of `CHANGELOG.md` as the record of notable Community changes.
6. A call to visit <https://www.axloop.ai> for the enterprise product.

Until a release exists, onboarding ends honestly at the availability notice. It must not imply that source checkout is an install, reuse a staging artifact, or manufacture a first-run command whose distributable does not exist.

## Release Tracking

Create `CHANGELOG.md` in Keep a Changelog shape with an `Unreleased` section. It must state that no Community GitHub Release has been published yet and link readers to this repository's Releases page for future latest installs.

Rewrite `docs/COMMUNITY_RELEASES.md` as the operational explanation of the same contract:

- `CHANGELOG.md` records notable Community changes.
- GitHub Releases will be the canonical place to find the latest install after the first approved publication.
- No release, tag, release draft, or publishing workflow is created by this change.
- The historical acceptance-staging tag dated 2026-08-29 is forbidden as release input.
- Signing keys and PKCS#8 material are excluded from Community CI.

The README, changelog, and release guide must agree about the current no-release state.

## Repository Policy

Update `scripts/check-community-split.py` so it recursively inspects tracked Community text files, including Markdown, rather than treating documentation as an exception. The checker must construct sensitive match values from neutral fragments so the forbidden private-repository identifier and obsolete boundary slogan do not appear literally in the checker, tests, design, or plan.

The checker fails on:

- a private enterprise repository identifier or URL assembled from its organization and repository-name fragments;
- the obsolete sentence pattern assembled from `enterprise`, `stays`, and `in`, plus equivalent factory-to-GitHub pointers;
- release publication artifacts, release-tag creation instructions, publishing commands, or a release workflow;
- PKCS#8 or signing-key secrets/configuration in Community CI;
- implementation of the deferred CLI `radar` to `crawler` rename;
- copied factory workflows, `src/`, `tools/`, or `packaging/` trees.

Normal prose may discuss enterprise capabilities and link to <https://www.axloop.ai>. Policy errors report the file and rule category without echoing a sensitive identifier.

## Test Design

Extend `tests/test_community_split.py` with fixture-tree tests that prove both allowed and rejected states. Tests assemble forbidden values from fragments, write each to representative files such as Markdown and workflow YAML, run the checker, and assert a nonzero result plus a category-level diagnostic. A clean fixture containing the public website funnel, empty release metadata, and unchanged CLI terminology must pass.

Required negative cases cover:

- private enterprise repository references in Markdown and non-Markdown text;
- obsolete private-location/factory GitHub language;
- nonempty release metadata and release publication commands;
- a release workflow or tag-creation instruction;
- PKCS#8/signing-key material under `.github/workflows/`;
- the CLI rename appearing as an implemented command or migration;
- the forbidden 2026-08-29 staging tag being selected as release input.

The final review also checks the live repository release state separately from fixture tests. This avoids pretending that a source-tree unit test alone can prove external GitHub state.

## Scope and Governance

This change does not add application code, a workflow, a tag, a release, a release draft, signing material, installable artifacts, the CLI rename, marketing campaigns, or content copied from another repository. It does not install Agent Stack, clone repositories, or merge plan PR #1.

Jules is off. Nolan participates only if a workflow is added; the design adds none, so Nolan is not in the default review path.

Implementation is performed later by Elena using Cursor cloud Claude Fable 5.1 at low effort, targeting `axloop/axloop-community` `main`, only after Imani and Reed review and Kit records a GitHub **COMMENT** signature on this plan. An approval reaction or approval state is not the gate because the `ajrrac` login is shared. No merge occurs unless Abe directs it.

## Review Evidence Slots

- Imani review citation: ____________________
- Reed review citation: ____________________
- Kit GitHub COMMENT signature: ____________________

These intentionally blank evidence slots are filled only with real review references; no version or citation is inferred.

## Acceptance Criteria

- A stranger can identify the Community offering, follow the first-run path, find the changelog and future install location, reach <https://www.axloop.ai>, and see that no release exists yet.
- No private enterprise repository reference or obsolete private-location/factory GitHub pointer exists anywhere in Community, including Markdown.
- The checker and tests reject all prohibited boundary, publishing, signing, and CLI-rename cases.
- No application code, workflow, tag, release, release draft, or publishing operation is part of the change.
- Review and execution follow the governance sequence above from baseline `503de93d`.
