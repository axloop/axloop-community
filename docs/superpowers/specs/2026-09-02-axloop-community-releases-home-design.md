# AxLoop Community Releases Home Design

**Named change:** AxLoop Community vs enterprise split, named by Abe on 2026-09-02.

**Status:** Design for a docs-only plan. No implementation, publication, repository move, merge, or clone is authorized by this document.

## Decision

AxLoop has two distinct homes:

- **Community artifacts + GitHub Releases:** https://github.com/axloop/axloop-community (private, `main` currently README-only at `f5746a39`).
- **Enterprise source, build, signing, acceptance:** https://github.com/ascendantventures/axloop-edge-poc (`main` at `9af8caac`). Do not rename, transfer, or copy that tree.

The Community repository is the Releases home, not a copy or mirror of the enterprise factory. The split changes where accepted Community artifacts are described and, in a later separately approved release operation, hosted. It does not move source code, build logic, signing material, or acceptance machinery.

No Community release is published by this change. The enterprise draft tag `community-acceptance-staging-2026-08-29` is Aug 29 staging only and must never be used, promoted, copied, retagged, attached, or published as part of this split. The CLI `radar`→`crawler` rename belongs to a later change.

## Ownership Boundary

### Community repository owns

- Documentation that says Community artifacts and GitHub Releases live in `axloop/axloop-community`.
- Documentation that points to `ascendantventures/axloop-edge-poc` for source, build, signing, and acceptance without copying that material.
- Documentation that says no Community release has yet been published from this repository.
- Documentation that disclaims the Aug 29 enterprise staging draft as a Community release or valid input.
- Optionally, a GitHub Actions workflow that creates or attaches assets to a **draft-only** release in `axloop/axloop-community`, using only already-signed, already-accepted artifacts supplied from the enterprise process.

The optional workflow is not necessary to establish the ownership boundary. The minimal recommended implementation is documentation first; add the workflow only when its artifact handoff and permissions can be reviewed concretely.

### Enterprise repository retains

- The entire existing repository tree, without rename, transfer, copy, or mirror.
- `.github/workflows/community-bundles.yml`, `.github/workflows/community-inputs.yml`, `.github/workflows/community-windows-input-review.yml`, and `.github/workflows/community-acceptance.yml`.
- `tools.community_native_build`, `tools.community_signing_request`, `tools.community_acquire_inputs`, and all other `tools.community_*` machinery.
- `release/`, including acquisition, inputs, requirements, toolchain, and trust material.
- Community source, packaging, hosted, Supabase, tests, acceptance, project metadata, and product/design documentation.
- Unsigned candidate builds, signing requests, attended signing, offline verification, release envelopes and checksums, clean-host acceptance, notarization, and Authenticode gates.
- The PKCS#8 Ed25519 signing key, which remains on Abe's Mac and never enters Community, GitHub Actions, or any CI system.

Enterprise documentation may point Community *releases* to `axloop/axloop-community`. Such edits are pointers only and are not part of the Community plan PR unless separately authorized in the enterprise repository.

## Community Documentation

The writer updates the Community README and may add focused release documentation. From Community `main`, Abe must be able to determine all of the following without consulting implementation code:

1. Community artifacts and GitHub Releases live in this repository.
2. Enterprise source, build, signing, and acceptance remain in `axloop-edge-poc`.
3. No Community release has been published from this repository yet.
4. The Aug 29 staging draft on `axloop-edge-poc` is not the Community home and is not used.
5. CLI `radar`→`crawler` is not part of this split.

The docs must not imply that the Community repository builds, signs, accepts, notarizes, or publishes artifacts.

## Optional Draft-Only Attachment Workflow

If the later writer adds a workflow, it must satisfy all of these constraints:

- It runs only in `axloop/axloop-community` and targets a release in that repository.
- It accepts only already-signed, already-accepted artifacts from the enterprise process through an explicitly documented handoff.
- It creates a draft or attaches assets to a draft; every release-creation invocation explicitly sets draft state to true.
- It has no publish, release-edit-to-published, auto-publish, or draft-removal path.
- It does not use, accept as an input, reference, retag, download from, or attach to `community-acceptance-staging-2026-08-29`.
- It does not check out `axloop-edge-poc`, copy enterprise files, invoke enterprise build/signing/acceptance tools, or reconstruct the factory.
- It requests the least permissions needed. It does not accept, read, create, or reference a signing-key secret.
- Nolan scores secrets and access on the writer PR before acceptance of the workflow.
- Publishing remains a separate future approval and is not represented by a dormant flag or commented step.

If these conditions cannot be proven, omit the workflow and ship the documentation-only boundary.

## Forbidden Content

The Community change must not add or copy:

- `src/`, `tools/`, `packaging/`, `hosted/`, `supabase/`, `tests/`, `acceptance/`, or `release/` from enterprise.
- `verify.py`, `pyproject.toml`, `setup.py`, `DESIGN.md`, or `PRODUCT.md` from enterprise.
- `community-bundles.yml`, `community-inputs.yml`, `community-windows-input-review.yml`, `community-acceptance.yml`, or equivalent factory workflows.
- Any signing key, PKCS#8 material, private-key secret name, or Community CI signing step.
- Agent Stack or the CLI `radar`→`crawler` rename.

## Verification Contract

Implementation review follows `superpowers:verification-before-completion`: the writer cannot claim completion until fresh checks have been run and their full output read.

The Superpowers acceptance checks must fail if:

- enterprise source, tools, or factory workflows appear in Community;
- any workflow step can publish a release or change a draft to published;
- `community-acceptance-staging-2026-08-29` is used as workflow input or artifact source;
- CLI `radar`→`crawler` lands in the change; or
- a signing key or signing-key secret enters Community CI.

Positive review also confirms that all five facts in “Community Documentation” are stated and that an optional workflow, if present, is explicitly draft-only. Absence of a workflow is valid.

## Delivery and Review Gates

- The plan PR is docs-only and starts from Community `main` at `f5746a39`.
- Enterprise reference state is `main` at `9af8caac`; that repository is not changed by this plan PR.
- Kit must GitHub-sign the plan with a **COMMENT** before writer launch; APPROVE is rejected because Kit and Abe are the same GitHub user. Chat approval is not the gate.
- After that sign, Elena launches Cursor cloud Claude Fable 5.1 low (`claude-fable-5-1`, effort `low`) against `axloop/axloop-community` `main`.
- No merge occurs unless Abe explicitly says to merge.
- If a workflow is added, Nolan scores secrets/access on the writer PR. PKCS#8 never enters Community.
- The later live-pass stamp is `/workspace/gates/axloop-community-pr<n>-<sha7>.md` matching writer HEAD; “LIVE PASS” in a writer body is not the stamp.

## Review-Pack Citations

No Imani pack exists yet. Do not invent a pack name or version.

- Imani pack: `[cite after this plan exists]`
- Reed review, after Imani: `[cite after the Imani pack lands]`

## Alternatives Considered

1. **Documentation-first Releases home (recommended).** Establishes ownership with the smallest auditable change and no new token or artifact-transfer surface.
2. **Documentation plus a draft-only attachment workflow.** Reduces later manual attachment work but adds permissions and handoff risk, so it requires Nolan's secrets/access score and stronger negative tests.
3. **Copy or move the factory into Community.** Rejected because it violates the named split, duplicates protected enterprise machinery, and risks exposing signing and release controls.

## Success Criteria

The split is successful when the Community repository unambiguously identifies itself as the Community artifact and GitHub Releases home, points to enterprise for the unchanged factory, states that nothing is published, excludes Aug 29 staging and the CLI rename, and passes every negative boundary check. No artifact publication is required or allowed.
