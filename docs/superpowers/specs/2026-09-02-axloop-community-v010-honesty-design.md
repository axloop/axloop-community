# AxLoop Community v0.1.0 honesty design

**Date:** 2026-09-02
**Base:** `axloop/axloop-community` `main` `81c55c0eebee70d6e4364dda24605f0c435f722d`
**Status:** docs-only spec. Writer waits for Kit GitHub COMMENT after Imani then Reed.

## Named change

Abe authorized the first public Community GitHub Release. It is live as tag `v0.1.0` at https://github.com/axloop/axloop-community/releases/tag/v0.1.0 (also `/releases/latest`). The visitor docs on `81c55c0` still say no release has been published. That is false. This change makes README, CHANGELOG, and the release guide match the live release. It does not publish another release, tag, workflow, or asset.

## Live facts (opened 2026-09-02)

- Repository is public.
- Release id `381577289`, tag `v0.1.0`, name `AxLoop Community 0.1.0 for Mac (Apple Silicon)`, `draft` is not set, not prerelease.
- Published at 2026-09-02 5:12 PM ET.
- Assets:
  - `axloop-community-darwin-arm64-3a7bfeeb.tar.gz` (44950048 bytes), SHA-256 `27e993467ee3b57c891c416ab5963032020b38218f2c57d890f094f791ca2043`
  - `axloop-community-darwin-arm64-3a7bfeeb-SHA256SUMS` (112 bytes), SHA-256 `17970d7b67f9e87cf972da7e9289f7e8cf0a1b0a42b4cc827032a041fcb18a22`
- Release notes: Mac Apple Silicon only; download the archive; check with the adjacent sums file; unpack; run `bin/axloop-community`; enterprise at https://www.axloop.ai
- No linux or windows assets. Do not claim those installs exist.
- Do not create a second tag. Do not retarget this release. A later source revision is a later release.

## Visitor path

A stranger opens README, follows First run to https://github.com/axloop/axloop-community/releases/latest, downloads both assets, checks the archive SHA-256 `27e993467ee3b57c891c416ab5963032020b38218f2c57d890f094f791ca2043`, unpacks, and runs `bin/axloop-community`. Honest that this is Mac Apple Silicon only. Enterprise stays https://www.axloop.ai. README has no code fence, no clone, no pip, no curl.

## Files

- `README.md` — drop the unpublished lie. First run uses the live latest release. Keep the public site funnel.
- `CHANGELOG.md` — keep `[Unreleased]` for later work. Add `[0.1.0] - 2026-09-02` for this Darwin install. Drop the unpublished lie.
- `docs/COMMUNITY_RELEASES.md` — current state is `v0.1.0` published, Darwin only. This docs change creates no new release. Signing material still never belongs in Community CI. Do not mention any historical staging identifier.
- `tests/test_community_split.py` — invert `VisitorJourneyTests` so they fail if docs still claim unpublished, fail if `v0.1.0` / darwin-arm64 / latest-release / archive SHA are missing, fail if linux or windows is claimed published, fail if README grows a code fence. Checker fixture trees may stay unpublished; they are not the live visitor contract.
- Do not edit `scripts/check-community-split.py` unless a visitor-test change requires it. Default: leave the checker.

## Out of scope

No `.github`. No new GitHub Release. No new tag. No linux/windows. No private factory GitHub path. No clone. No Agent Stack. Jules off. Nolan only if a workflow appears (none planned). Do not detach anyone's Mac checkout.

## Writer brief

Make Community visitor docs honest about live GitHub Release `v0.1.0` (Mac Apple Silicon, darwin-arm64 archive `axloop-community-darwin-arm64-3a7bfeeb.tar.gz`, SHA-256 `27e993467ee3b57c891c416ab5963032020b38218f2c57d890f094f791ca2043`). Invert visitor tests first. Do not publish anything new.
