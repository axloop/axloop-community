# Community releases

This page explains how AxLoop Community versions and installs are tracked, announced, and verified.

## Current release

AxLoop Community v0.1.0 is published. It is the first Community install, and it supports Mac with Apple Silicon only, identified as `darwin-arm64`. No Linux or Windows build exists.

The install is a plain tar.gz archive plus a checksum file. It is not a notarized installer, so the checksum is your verification step.

1. Start at the latest release: <https://github.com/axloop/axloop-community/releases/latest>.
2. Download `axloop-community-darwin-arm64-3a7bfeeb.tar.gz` and `axloop-community-darwin-arm64-3a7bfeeb-SHA256SUMS`.
3. Check that the archive SHA-256 is `27e993467ee3b57c891c416ab5963032020b38218f2c57d890f094f791ca2043`. The `SHA256SUMS` file carries the same value.
4. Unpack the archive.
5. From the unpacked directory, run `bin/axloop-community`. That is the binary the published v0.1.0 archive ships.

For enterprise AxLoop, visit <https://www.axloop.ai>.

## Command name

`axloop-crawler` is the approved user-visible Community CLI, command, and MCP name. Future release notes, install steps, and MCP configuration examples in this repository use `axloop-crawler`; a future release may ship it as the command to run after unpacking.

The published v0.1.0 archive still ships `bin/axloop-community`; it does not contain `axloop-crawler`. `axloop-crawler` is the approved user-visible name for a future release, which is not created or published here.

## Where to look

- [`CHANGELOG.md`](../CHANGELOG.md) records notable Community changes. Work that has not shipped yet is listed under `Unreleased`; each published version has its own dated section.
- [GitHub Releases](https://github.com/axloop/axloop-community/releases) is the canonical place to find Community installs. The newest one is always at <https://github.com/axloop/axloop-community/releases/latest>.

## Scope of this documentation

This documentation describes the existing v0.1.0 release. It creates no release, tag, workflow, or Linux or Windows asset.

## Rules that stay fixed

- Release signing material never belongs in Community CI. Signing keys and PKCS#8 material are not stored, referenced, or used by anything in this repository.
- Historical staging tags are not release inputs. Only tags published on the Releases page are Community releases.
- `axloop-crawler` is the canonical Community user-visible command. `axloop-radar` is not the Community user-facing CLI name, and documentation of the published v0.1.0 archive must keep saying it ships `bin/axloop-community`.

## Policy check

`scripts/check-community-split.py` enforces these rules across every text file in the repository, including Markdown. Run it from the repository root:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/check-community-split.py .
```
