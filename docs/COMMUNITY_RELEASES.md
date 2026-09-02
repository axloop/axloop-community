# Community releases

This page explains how AxLoop Community versions and installs are tracked and announced.

## Where to look

- [`CHANGELOG.md`](../CHANGELOG.md) records notable Community changes. Work that has not shipped yet is listed under `Unreleased`; each published version gets its own dated section when it is released.
- [GitHub Releases](https://github.com/axloop/axloop-community/releases) is the canonical place to find Community installs. The newest one will always be at <https://github.com/axloop/axloop-community/releases/latest>.

## Current state

No Community GitHub Release has been published yet. There is no supported Community install until the first release appears on the Releases page.

This documentation change creates no release, tag, artifact, release draft, or publishing workflow. Publishing the first Community release is a separate, future approval.

## Rules that stay fixed

- Release signing material never belongs in Community CI. Signing keys and PKCS#8 material are not stored, referenced, or used by anything in this repository.
- The historical 2026-08-29 acceptance-staging tag is not a release input. It must not be reused, retagged, attached, or published as a Community release.

## Policy check

`scripts/check-community-split.py` enforces these rules across every text file in the repository, including Markdown. Run it from the repository root:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/check-community-split.py .
```
