# AxLoop Community Homebrew Install Design

**Date:** 2026-09-03  
**Repository:** `axloop/axloop-community`  
**Base:** `81c55c0eebee70d6e4364dda24605f0c435f722d`  
**Status:** Later two-repository work; Homebrew installation does not work today

## Purpose and Current Truth

Give a stranger on Apple Silicon one honest Homebrew command without weakening repository or trust boundaries. Today v0.1.0 is published as a tarball plus checksum, and the public tap exists but is empty of installable items. No Homebrew install works today and no visitor document may claim it does.

Community has one tag, `v0.1.0`, at the base SHA. Live release `381577289` was published `2026-09-02T21:12:15Z`, is neither draft nor prerelease, and is titled `AxLoop Community 0.1.0 for Mac (Apple Silicon)`. Its only assets are:

| Asset | Bytes | SHA-256 |
| --- | ---: | --- |
| `axloop-community-darwin-arm64-3a7bfeeb.tar.gz` | 44,950,048 | `27e993467ee3b57c891c416ab5963032020b38218f2c57d890f094f791ca2043` |
| `axloop-community-darwin-arm64-3a7bfeeb-SHA256SUMS` | 112 | `17970d7b67f9e87cf972da7e9289f7e8cf0a1b0a42b4cc827032a041fcb18a22` |

There is no `.pkg`, `.dmg`, Linux, or Windows asset. The pinned payload is `https://github.com/axloop/axloop-community/releases/download/v0.1.0/axloop-community-darwin-arm64-3a7bfeeb.tar.gz`; its entry point is `bin/axloop-community`. Enterprise remains [axloop.ai](https://www.axloop.ai).

The tap is `axloop/homebrew-axloop-community`, public repository ID `1356097533`, created `2026-09-03T14:52:02Z`, last renamed `2026-09-03T14:58:45Z`, default branch `main`, description `Homebrew tap for AxLoop Community`. It contains exactly one 55-byte `README.md`, no formula or cask, and no `Formula/` or `Casks/` directory. The README's first line is the stale heading `# homebrew-community`; it must be corrected, and it is never naming proof either before or after correction. The `axloop` organization has exactly this tap and `axloop-community`.

## Alternatives and Recommendation

1. **Cask (recommended):** put `axloop-community.rb` at `Casks/axloop-community.rb`. This directly models a prebuilt, platform-specific macOS archive, declares ARM and macOS dependencies, and links `bin/axloop-community` with a `binary` artifact.
2. **Binary formula:** put `axloop-community.rb` at `Formula/axloop-community.rb`. It can pin the same bytes, use explicit macOS/ARM guards, and call `bin.install "bin/axloop-community"`, but is less idiomatic for this payload.
3. **Notarized `.pkg` later:** potentially improves the native trust story, but none exists and it is not a blocker.

The recommendation follows official mechanics. [Acceptable Formulae](https://docs.brew.sh/Acceptable-Formulae) describes requirements for `homebrew/core` and says proprietary or platform-specific binary-only software belongs in a cask. That is core eligibility policy, not a ban on binary formulae in third-party taps, but it is a strong idiomatic signal. The [Cask Cookbook](https://docs.brew.sh/Cask-Cookbook) requires `version`, `sha256`, `url`, `name`, `desc`, `homepage`, and an artifact; it defines `url` for common archives, `binary` as the relative binary linked into `$(brew --prefix)/bin`, `depends_on arch: :arm64` for Apple Silicon, and top-level `depends_on :macos` for macOS-only casks. The [Formula Cookbook](https://docs.brew.sh/Formula-Cookbook) documents `bin.install` and platform guards, while [tap maintenance guidance](https://docs.brew.sh/How-to-Create-and-Maintain-a-Tap) permits formulae at root, `Formula/`, or `HomebrewFormula/`.

Either shape preserves one fully qualified stranger command. The shape remains an explicit Imani trust/quarantine concern and Reed technical concern; this design recommends rather than declares it settled.

## Naming and Command Contract

[Taps](https://docs.brew.sh/Taps) says `brew tap <user>/<repository>` clones `https://github.com/<user>/homebrew-<repository>`. Verbatim: “On GitHub, a repository must be named `homebrew-<name>` to use the one-argument form of `brew tap`. The `homebrew-` prefix can be omitted from the command”. Its two-argument form “does not impose this naming convention because the full URL is explicit”. It also says: “Tapping a repository does not grant whole-tap trust. Install a fully qualified item to trust only that item”. `brew trust --formula user/repository/formula` permits the short name afterward.

The current repository therefore has tap identifier `axloop/axloop-community`, and the post-verification stranger command is `brew install axloop/axloop-community/axloop-community`. A pending decision remains unresolved: `brew install axloop/community/axloop-community` requires renaming the repository to `axloop/homebrew-community`. Both are one command; only the quoted command string changes if Abe renames it again. No document may quote an unconfirmed tap name.

The documentation rule is necessary but not sufficient evidence. The live gate must capture Homebrew itself resolving logical tap `axloop/axloop-community` to physical repository `https://github.com/axloop/homebrew-axloop-community`, for example with `brew tap-info axloop/axloop-community` showing that remote, and resolving the fully qualified token `axloop/axloop-community/axloop-community` to the landed cask. Resolution to any other repository or token fails. Do not invent an alternate command spelling.

## Recommended Cask Contract

The only Ruby addition to the tap is `Casks/axloop-community.rb`:

```ruby
cask "axloop-community" do
  version "0.1.0"
  sha256 "27e993467ee3b57c891c416ab5963032020b38218f2c57d890f094f791ca2043"
  url "https://github.com/axloop/axloop-community/releases/download/v0.1.0/axloop-community-darwin-arm64-3a7bfeeb.tar.gz"
  name "AxLoop Community"
  desc "Community edition of AxLoop"
  homepage "https://github.com/axloop/axloop-community"
  depends_on arch: :arm64
  depends_on :macos
  binary "bin/axloop-community"
end
```

No floating `releases/latest` URL is permitted. Intel macOS must be rejected as incompatible with ARM; Linux must be rejected as incompatible with macOS. Visitor copy names these outcomes without inventing exact Homebrew error text. If the formula alternative wins, it is the sole Ruby addition and pins the same URL/digest, uses explicit macOS/ARM guards, and installs `bin/axloop-community`.

## Trust, Signing, and Later Package

The checksum proves payload integrity, not producer identity. A third-party tap is unsupported by Homebrew, and its Ruby runs with the user's privileges. No official Homebrew documentation substantiates formula quarantine avoidance. That is an open Imani question and a live observation, never visitor copy or an automated assertion.

Community has no signing material and no signing workflow. Nolan owns a later, non-blocking notarized `.pkg`: attended Developer ID work on Abe's Mac, never Community CI. The upstream packaging process writes `manifest.sig` before wrapping, and wrapping does not replace payload verification. Nolan currently has zero codesigning identities, no `notarytool` profile, and no team.

Kit independently fetched and inspected the pinned archive from the shared box on 2026-09-03 at 12:12 EDT. The response was HTTP 200 and 44,950,048 bytes; Kit computed SHA-256 `27e993467ee3b57c891c416ab5963032020b38218f2c57d890f094f791ca2043`, equal to the pin. The archive had 157 entries, zero absolute paths, zero parent-traversal paths, and was flat-rooted with top-level `bin`, `share`, `osquery`, `licenses`, `manifest.json`, `manifest.sig`, `provenance.json`, `sbom.cdx.json`, `trust-anchor.json`, and `THIRD_PARTY_NOTICES.md`. `bin/axloop-community` exists at the archive root with mode `-rwxr-xr-x` and size 2,245,664 bytes. This proves the inspected bytes and layout, not Homebrew's transaction; Homebrew's own checksum verification against the landed cask remains mandatory during a real install.

For the live run, record rather than pre-judge that the payload is a PyInstaller onedir bundle whose launcher sits beside `bin/_internal`, and that `osquery/osquery.app` ships inside it. The run must observe whether the single linked binary still resolves those siblings.

## Repository Boundaries

| Repository | Exclusive allowlist |
| --- | --- |
| `axloop/homebrew-axloop-community` | Exactly one of `Casks/axloop-community.rb` or `Formula/axloop-community.rb`; plus only the existing `README.md` heading corrected from `# homebrew-community` to `# homebrew-axloop-community` |
| `axloop/axloop-community` at the stated base | `tests/test_community_split.py`, `README.md`, `CHANGELOG.md`, `docs/COMMUNITY_RELEASES.md` |

Everything else is forbidden: `.github`, workflows, tags, releases, asset uploads, signing material, runtime code, checker or fixture edits, invented versions, the unselected tap shape, and any other README rewriting or tap README install instructions. The Ruby item and one-line README correction are named, reviewable tap changes in the tap scope audit. The README heading is never naming proof; only Homebrew's own resolution is.

## Cross-Repository Landing Authority and Sequence

Before any cask work begins, name Abe / GitHub login `ajrrac` as the sole tap writer and sole tap merger for `axloop/homebrew-axloop-community`. Elena confirmed on 2026-09-03 via a read-only collaborator listing that he is the only account with admin/maintain/push/pull/triage there; do not add anyone and do not assume cloud-writer access. Abe's explicit merge approval is required. Public visibility is not write authority. A cloud writer launched at `axloop/axloop-community` cannot touch the tap repository, so the tap change is a separate change with its own owner. Abe authorized Kit on 2026-09-03 to prepare the exact cask and open the tap pull request under his identity for his review only — not to merge it.

The selected item and one-line heading correction must land through a tap pull request, never inside or alongside the Community source change. The landing record must contain the tap pull-request number, reviewer/merger, selected Ruby file blob SHA, and resulting tap `main` SHA. The Community visitor-doc change must then bind itself to that exact tap `main` SHA and the clean-machine evidence record; documentation cannot go green against an unrecorded or later-mutated tap state.

**STOP:** if the named actor lacks permission to open or merge the tap change, stop and return that fact to Abe. Do not relocate the cask into the source repository as a workaround.

## Hard Stop and Live Verification

Before Community RED, the selected item must actually be on tap `main`, the authority and landing record must be complete, and Elena must drive a stranger-style run against that exact tap SHA from a clean, untapped, uninstalled state on Abe's connected real Apple Silicon Mac. The exact visitor commands are numbered: (1) `brew install axloop/axloop-community/axloop-community`; (2) `axloop-community`. A confirmed rename changes only command 1.

Capture Mac model/architecture, macOS and Homebrew versions, starting state, every exact command, full stdout/stderr and status, Homebrew's logical-to-physical tap resolution, fully qualified cask resolution, applicable cask style and audit results, Homebrew's own checksum verification, `brew info --cask` and `brew list --cask` output, Caskroom staging as applicable, installed and resolved linked-binary paths, sibling resolution and observed invocation output, tap commit SHA, and URL/digest actually fetched. Then uninstall and prove cleanup, reinstall from the clean result, and repeat enough resolution and invocation evidence to rule out success caused by residue. Separately demonstrate an honest unsupported-architecture failure without predicting its text, or explicitly record the architecture gate as unverified. Any missing field or failed journey keeps the hard stop closed. Diagnostic evidence may follow the visitor journey, but never enters visitor copy.

The first invocation of the Homebrew-installed binary must occur without removing quarantine and without any policy bypass. Before and around that invocation, record the quarantine attribute state, signature assessment, and what actually happens. A prompt, denial, crash, or any need for manual rescue **FAILS** the one-command stranger claim; the visitor contract stops until a compliant path is chosen and verified. Homebrew delivery must not be assumed to cure unsigned or unnotarized behavior. This is a gate, never visitor copy.

## Community Contract and TDD

After the gate, extend or invert real-file `VisitorJourneyTests` first. Observe `python3 -m unittest tests.test_community_split.VisitorJourneyTests -v` fail for the intended missing contract; then update `README.md`, `CHANGELOG.md`, and `docs/COMMUNITY_RELEASES.md` to green. Finally run `python3 -m unittest tests.test_community_split -v` and unchanged `python3 scripts/check-community-split.py`.

README uses inline commands only, with no fenced blocks or source checkout, command-line download, manual checksum, archive unpack, quarantine removal, Python package install, or diagnostic bypass steps. The release guide carries the immutable pin, platform/trust qualifications, checksum limitation, signing boundary, and later-package facts.

PR #7 at head `6bebf6bc58c108f03900d8efc9a4fafaa0fdf1ec` is unmerged and rewrites the same visitor documents around the tarball/checksum path. The writer rebases on whatever `main` holds and keeps the three files consistent. Exclude leftover plan PRs #1, #3, #5 and old Finder content from PR #6.

The only existing GitHub review is pinned to removed Finder-era content at `501a1da7c167bf5072b0235548f763217ac7b217`; it is never sign-off for a later head. This amendment creates a new head and therefore requires a fresh Imani dated pack, a fresh Reed critic, and Kit's COMMENT on the current full head SHA. Any subsequent head change reopens those current-head requirements.

## Execution Gate

| Reviewer | GitHub COMMENT |
| --- | --- |
| Imani | |
| Reed | |
| Kit | |

Order is Imani, Reed, then Kit. No writer launches and nothing publishes in this stream.

## Acceptance and Handoff

Acceptance requires the selected tap shape plus the one-line README heading correction, exact immutable pin, proven cross-repository authority and landing record, exact tap-SHA binding, Homebrew naming and checksum evidence, honest Intel/Linux outcomes, separate allowlists, complete clean-Mac install/uninstall/reinstall and Gatekeeper evidence before RED, observed red then green, full-module pass, unchanged-checker pass, consistent visitor documents, fresh current-head reviews, and blank ordered gates. Hand the evidence and any blocker to Abe. Do not convert missing evidence into optimistic copy.
