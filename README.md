# AxLoop Community

AxLoop Community is the community edition of AxLoop. This repository is where Community releases are tracked and where installs are published.

---

## First run

AxLoop Community v0.1.0 is published for Mac with Apple Silicon only (`darwin-arm64`). There is no Linux or Windows build. The download is a plain tar.gz archive with a checksum file; it is not a notarized installer, so verify the checksum yourself before running it.

1. Open the [latest release](https://github.com/axloop/axloop-community/releases/latest).
2. Download `axloop-community-darwin-arm64-3a7bfeeb.tar.gz` and `axloop-community-darwin-arm64-3a7bfeeb-SHA256SUMS`.
3. Check that the archive SHA-256 is `27e993467ee3b57c891c416ab5963032020b38218f2c57d890f094f791ca2043`.
4. Unpack the archive.
5. From the unpacked directory, run `bin/axloop-community`. That is the binary the published v0.1.0 archive ships; see [Command name](#command-name) for the name used going forward.

Read the [changelog](CHANGELOG.md) for what each version contains.

## Command name

`axloop-crawler` is the approved user-visible Community CLI, command, and MCP name going forward. The published v0.1.0 archive still ships `bin/axloop-community`; it will remain unchanged until a new release is cut. Cutting that release is outside this change.

## Enterprise

For enterprise AxLoop, visit [axloop.ai](https://www.axloop.ai).

## Release information

See [Community releases](docs/COMMUNITY_RELEASES.md) for how versions and installs are announced and verified.

---

Questions or problems? Open an [issue](https://github.com/axloop/axloop-community/issues) in this repository.
