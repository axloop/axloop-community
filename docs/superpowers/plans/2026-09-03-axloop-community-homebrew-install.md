# AxLoop Community Homebrew Install Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add one pinned Apple Silicon Homebrew item, prove it from a clean real Mac, and only then update Community's tested visitor contract.

**Architecture:** Keep the tap artifact and Community docs in separate repositories with closed allowlists. Recommend a cask, retain a mutually exclusive formula alternative, and place live evidence before the mandatory Community red-green cycle.

**Tech Stack:** Homebrew Ruby, Markdown, Python `unittest`, existing fail-closed checker, macOS Apple Silicon.

**Spec:** `docs/superpowers/specs/2026-09-03-axloop-community-homebrew-install-design.md`

## Global Constraints

- Homebrew does not work today: v0.1.0 is published, but the existing tap has only its 55-byte README.
- Community base is `81c55c0eebee70d6e4364dda24605f0c435f722d`; `v0.1.0` is the only tag and is at that SHA.
- Release ID `381577289`, published `2026-09-02T21:12:15Z`, is final, public, and titled `AxLoop Community 0.1.0 for Mac (Apple Silicon)`.
- Pin `https://github.com/axloop/axloop-community/releases/download/v0.1.0/axloop-community-darwin-arm64-3a7bfeeb.tar.gz` and `27e993467ee3b57c891c416ab5963032020b38218f2c57d890f094f791ca2043`; expose `bin/axloop-community`.
- The only other asset is `axloop-community-darwin-arm64-3a7bfeeb-SHA256SUMS`, 112 bytes, digest `17970d7b67f9e87cf972da7e9289f7e8cf0a1b0a42b4cc827032a041fcb18a22`. No `.pkg`, `.dmg`, Linux, or Windows asset exists.
- Current tap repository is `axloop/homebrew-axloop-community`, ID `1356097533`, branch `main`; the stranger command is `brew install axloop/axloop-community/axloop-community`.
- A rename to `axloop/homebrew-community` changes only that string to `brew install axloop/community/axloop-community`. Do not resolve this or quote an unconfirmed name.
- Recommend only `Casks/axloop-community.rb`; if Imani and Reed select the alternative, use only `Formula/axloop-community.rb`.
- Tap allowlist: the selected Ruby file plus only the existing `README.md` heading correction from `# homebrew-community` to `# homebrew-axloop-community`; no other README rewrite or tap README install instructions. Community allowlist: only `tests/test_community_split.py`, `README.md`, `CHANGELOG.md`, `docs/COMMUNITY_RELEASES.md`.
- Forbid `.github`, workflows, tags, releases, assets, signing material, runtime code, checker/fixture edits, invented versions, and every other file.
- The tap item must land through a separate tap pull request owned by named tap actors. Do not start Community RED until the exact tap `main` SHA and clean-machine evidence record are bound to the Community change and Elena completes the clean real-Mac run.
- README has no fenced blocks. Stranger commands have no source checkout, command-line downloader, manual checksum, archive unpack, quarantine removal, Python package install, or diagnostic bypass flags.
- Intel macOS and Linux are unsupported; do not invent exact Homebrew errors. Add no quarantine assertion or visitor claim.
- The checksum proves payload integrity, not producer identity. A third-party tap is unsupported by Homebrew and its Ruby runs with the user's privileges. Community has no signing material or workflow.
- Nolan's `.pkg` is later, non-blocking, attended Developer ID on Abe's Mac, and never Community CI. The upstream packaging process writes `manifest.sig` before wrapping; wrapping retains payload verification. Current state: zero identities, no `notarytool` profile, no team.
- Kit independently verified the pinned archive from the shared box on 2026-09-03 at 12:12 EDT: HTTP 200; 44,950,048 bytes; locally computed SHA-256 `27e993467ee3b57c891c416ab5963032020b38218f2c57d890f094f791ca2043`; 157 entries; zero absolute paths; zero parent-traversal paths; top-level `bin`, `share`, `osquery`, `licenses`, `manifest.json`, `manifest.sig`, `provenance.json`, `sbom.cdx.json`, `trust-anchor.json`, and `THIRD_PARTY_NOTICES.md`; and root entry `bin/axloop-community` at mode `-rwxr-xr-x`, size 2,245,664 bytes. This proves bytes and layout, not Homebrew's transaction.
- PR #7 head `6bebf6bc58c108f03900d8efc9a4fafaa0fdf1ec` is unmerged. Rebase prose on launch-time `main`; exclude PRs #1, #3, #5 and PR #6's old Finder content.
- The only existing GitHub review is pinned to removed Finder-era content at `501a1da7c167bf5072b0235548f763217ac7b217` and never signs off a later head. This amendment creates a new head requiring a fresh Imani dated pack, a fresh Reed critic, and Kit's COMMENT on the current full head SHA.
- Gates are Imani, Reed, then Kit's GitHub COMMENT. No writer launch, merge, or publication in this authoring stream.

---

## Execution Gate

| Reviewer | GitHub COMMENT |
| --- | --- |
| Imani | |
| Reed | |
| Kit | |

Do not begin Task 1 until the comments exist in that order.

### Task 1: Select the single tap artifact

**Files:**

- Create, recommended: `Casks/axloop-community.rb`
- Create, alternative only: `Formula/axloop-community.rb`
- Modify: tap `README.md`, heading only

**Interfaces:**

- Consumes: Imani's trust review, Reed's shape review, exact v0.1.0 pin, confirmed repository name.
- Produces: one reviewed item and one reviewed heading correction for the separately owned tap change.

- [ ] **Step 1: Confirm the GitHub name**

Confirm `axloop/homebrew-axloop-community`, repository ID `1356097533`, and `main`. Expected: tap identifier `axloop/axloop-community`; if renamed, stop for Abe's confirmation and change only the command string.

- [ ] **Step 2: Name and verify the tap actors before cask work begins**

Name Abe / GitHub login `ajrrac` as the sole tap writer and sole tap merger for `axloop/homebrew-axloop-community`. Elena confirmed on 2026-09-03 via a read-only collaborator listing that he is the only account with admin/maintain/push/pull/triage on that repository; do not add anyone and do not assume cloud-writer access. Abe's explicit merge approval is required for every tap pull request. Public visibility is not write authority. A cloud writer launched at `axloop/axloop-community` cannot touch the tap repository; the tap change is separate and has its own owner. Abe authorized Kit on 2026-09-03 to prepare the exact cask and open the tap pull request under his identity for his review only — not to merge it. **STOP** before drafting either Ruby shape if that authority changes or is missing, and return that fact to Abe without relocating the cask into the source repository.

- [ ] **Step 3: Record the shape decision**

Compare cask `Casks/axloop-community.rb` (idiomatic binary archive, native `arch`, `:macos`, `binary`) with formula `Formula/axloop-community.rb` (valid third-party alternative, less idiomatic, explicit guards and `bin.install`). Expected: Imani and Reed select exactly one; the visitor stays at one command either way.

- [ ] **Step 4: Write the recommended cask when selected**

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

Expected: exact immutable pin, both guards, one binary artifact, plus only the separately reviewed README heading correction.

- [ ] **Step 5: Use the formula only if selected instead**

```ruby
class AxloopCommunity < Formula
  desc "Community edition of AxLoop"
  homepage "https://github.com/axloop/axloop-community"
  url "https://github.com/axloop/axloop-community/releases/download/v0.1.0/axloop-community-darwin-arm64-3a7bfeeb.tar.gz"
  version "0.1.0"
  sha256 "27e993467ee3b57c891c416ab5963032020b38218f2c57d890f094f791ca2043"

  def install
    odie "AxLoop Community supports macOS only" unless OS.mac?
    odie "AxLoop Community supports Apple Silicon only" unless Hardware::CPU.arm?
    bin.install "bin/axloop-community"
  end
end
```

Expected: identical pin, explicit platform rejection, same executable, and no cask file.

- [ ] **Step 6: Correct and audit the tap README heading**

Change only the first line from `# homebrew-community` to `# homebrew-axloop-community`. Add no install instructions and rewrite no other README text. Record both the selected Ruby file and `README.md` as named paths in the tap scope audit. Expected: exactly one proposed Ruby path plus the one-line heading correction. The heading is never tap-name evidence; Homebrew resolution in Task 3 is authoritative.

### Task 2: Establish tap authority and land the separate tap change

**Files:**

- Change in tap pull request: selected Ruby item and `README.md` heading only
- Change in Community pull request: none
- Capture: authority and landing record outside both change sets

**Interfaces:**

- Consumes: reviewed Task 1 artifact, confirmed repository identity, tap repository's normal controls.
- Produces: immutable tap pull-request and `main` evidence for Task 3, or a hard stop returned to Abe.

- [ ] **Step 1: Reconfirm the tap actors and permissions before landing**

Reconfirm the Task 1 record names the tap writer and tap merger and demonstrates their respective open/merge paths through the tap repository's normal controls. Public visibility remains insufficient evidence.

- [ ] **Step 2: Apply the permission hard stop**

**STOP:** if either named actor lacks the required permission, stop and return that exact fact to Abe. Do not relocate the cask into the source repository as a workaround, and do not begin any cask work or Community RED.

- [ ] **Step 3: Land only through a tap pull request**

The named tap writer opens the selected Ruby item and heading-only README correction as a tap pull request; the named tap reviewer/merger reviews and merges it through normal controls. Never place either tap file in the Community source pull request.

- [ ] **Step 4: Freeze the tap landing record**

Record the tap pull-request number, writer, reviewer/merger, selected Ruby file blob SHA, and resulting full tap `main` SHA. Expected: every field names completed evidence, and the tap scope is exactly the two allowed paths.

- [ ] **Step 5: Bind the downstream work**

Bind the Community visitor-doc change to that exact tap `main` SHA and to the Task 3 clean-machine evidence record. If the recorded tap state cannot be recovered or no longer matches the landed file blob, stop; docs cannot go green against a tap state that no longer exists.

### Task 3: Clear the live Apple Silicon hard stop

**Files:**

- Read: selected item on the recorded tap `main` SHA
- Change: no repository file
- Capture: evidence outside both change sets

**Interfaces:**

- Consumes: Task 2 landing record, confirmed tap name, Abe's connected real Apple Silicon Mac in clean state.
- Produces: complete evidence unlocking Task 4, or a hard stop.

- [ ] **Step 1: Capture machine and starting state**

Record the Mac model in System Information and the tap SHA, then run individually:

```text
uname -m
sw_vers
brew --version
brew tap
brew list --cask axloop-community
brew list --formula axloop-community
```

Expected: `arm64`; versions captured; confirmed tap absent; both item checks absent/nonzero; no prior linked binary or relevant Caskroom residue. Record full stdout, stderr, and status. If not clean, stop and reschedule after Abe restores a clean state.

- [ ] **Step 2: Prove Homebrew's tap and token mapping**

Capture Homebrew resolving logical tap `axloop/axloop-community` to physical repository `https://github.com/axloop/homebrew-axloop-community`, for example with `brew tap-info axloop/axloop-community` output showing the remote. Capture the fully qualified token `axloop/axloop-community/axloop-community` resolving to the landed cask at the recorded tap `main` SHA. Resolution to any other repository or token fails. Do not invent an alternate command spelling, and never use the README heading as proof.

- [ ] **Step 3: Run the applicable cask checks**

Against the exact landed tap SHA, run Homebrew's applicable cask style and audit checks and capture each exact command, stdout, stderr, and status. Expected: all applicable checks pass. Do not substitute Ruby source inspection for Homebrew results.

- [ ] **Step 4: Run the exact stranger install**

Run `brew install axloop/axloop-community/axloop-community`.

Expected: exit 0 with full stdout/stderr captured, including Homebrew's own successful checksum verification against the landed cask. A confirmed rename substitutes only the verified command. Add no flags and no separate tap command.

- [ ] **Step 5: Capture cask and link mechanics**

Run `brew info --cask axloop/axloop-community/axloop-community`, capture `brew list --cask` output, resolve `command -v axloop-community`, and resolve the linked path to its destination. Record the cask version, tap SHA, staging/Caskroom path as applicable, installed binary path, link destination, fetched URL, and cached digest. Observe whether the PyInstaller onedir launcher still resolves its siblings beside `bin/_internal` and the shipped `osquery/osquery.app`; do not assume that it does.

- [ ] **Step 6: Enforce the Gatekeeper stop on first invocation**

Before first invocation, record the installed payload's quarantine attribute state and signature assessment. Then run `axloop-community` without removing quarantine and without any policy bypass, capturing full stdout, stderr, status, prompts, denial, crash, and functional output exactly as observed. A prompt, denial, crash, or any need for manual rescue **FAILS** the one-command stranger claim: stop the visitor contract until a compliant path is chosen and verified. Homebrew delivery must not be assumed to cure unsigned or unnotarized behavior. Keep this evidence out of visitor copy.

- [ ] **Step 7: Prove uninstall cleanup and clean reinstall**

Uninstall the cask, record full output/status, and prove the cask record, Caskroom staging as applicable, linked path, and binary resolution are gone. Reinstall with the exact stranger command from that cleaned state, recapture Homebrew checksum success, cask/list information, link resolution, and invocation outcome. Expected: the second journey passes without leftover residue accounting for success.

- [ ] **Step 8: Record the unsupported-architecture result honestly**

Either capture a clean failure on unsupported architecture using the landed cask, with exact command/output/status and no invented error text, or explicitly record `architecture gate unverified` in the evidence. The unverified result does not become a visitor claim.

- [ ] **Step 9: Apply the hard stop**

Expected record: tap pull request, actors, file blob and tap SHA; model/architecture; macOS/Homebrew versions; clean start; all exact commands and full stdout/stderr/status; logical-to-physical tap resolution; fully qualified token resolution; style/audit results; Homebrew checksum result; `brew info --cask` and `brew list --cask`; staging, binary and link paths; sibling resolution; quarantine and signature assessments; first invocation outcome; fetched URL/digest; uninstall cleanup; reinstall result; and unsupported-architecture result or explicit unverified status. If any required field or success is missing, stop before Community RED and report: `Blocked: the clean Apple Silicon Homebrew journey is not fully verified; no Community visitor-contract file changed.`

### Task 4: Extend real-file tests and prove RED

**Files:**

- Modify: `tests/test_community_split.py`, only `VisitorJourneyTests` and needed standard-library imports
- Read: `README.md`, `CHANGELOG.md`, `docs/COMMUNITY_RELEASES.md`
- Leave unchanged: checker and fixtures

**Interfaces:**

- Consumes: Task 3 evidence bound to the exact tap SHA, confirmed command, existing real-file readers.
- Produces: failing visitor assertions for Task 5; no quarantine assertion.

- [ ] **Step 1: Inspect launch-time truth**

Record whether unmerged PR #7 reached `main`; preserve truthful current release facts and exclude the named old PR content. Expected: one internally consistent baseline before editing.

- [ ] **Step 2: Add README contract assertions**

```python
def test_readme_has_verified_homebrew_journey(self):
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    self.assertIn("brew install axloop/axloop-community/axloop-community", readme)
    self.assertIn("`axloop-community`", readme)
    self.assertIn("Apple Silicon", readme)
    self.assertIn("https://www.axloop.ai", readme)
    self.assertNotIn("```", readme)
    forbidden_commands = (
        r"(?i)\bgit\s+clone\b",
        r"(?i)\bpip\s+install\b",
        r"(?i)\bcurl\b",
        r"(?i)\b(?:sha256sum|shasum)\b",
        r"(?i)\btar\b",
        r"(?i)\bxattr\b",
        r"(?i)\bbrew\s+doctor\b",
    )
    for pattern in forbidden_commands:
        self.assertNotRegex(readme, pattern)
```

Reuse existing reader names; if renamed, change only the command string.

- [ ] **Step 3: Add release-guide assertions**

```python
def test_release_guide_has_pinned_homebrew_contract(self):
    guide = (ROOT / "docs/COMMUNITY_RELEASES.md").read_text(encoding="utf-8")
    for required in (
        "https://github.com/axloop/axloop-community/releases/download/v0.1.0/axloop-community-darwin-arm64-3a7bfeeb.tar.gz",
        "27e993467ee3b57c891c416ab5963032020b38218f2c57d890f094f791ca2043",
        "bin/axloop-community", "Apple Silicon", "Intel", "Linux",
        "payload integrity", "producer identity", "third-party tap",
        "user's privileges", "no signing material", "no signing workflow",
    ):
        self.assertIn(required, guide)
```

- [ ] **Step 4: Add consistency assertions**

```python
def test_homebrew_story_is_consistent_and_published(self):
    docs = {p: (ROOT / p).read_text(encoding="utf-8") for p in
            ("README.md", "CHANGELOG.md", "docs/COMMUNITY_RELEASES.md")}
    joined = "\n".join(docs.values())
    self.assertNotRegex(joined, r"(?i)no (?:homebrew )?install (?:works|is available)")
    self.assertNotRegex(joined, r"(?i)homebrew (?:is )?unpublished")
    self.assertRegex(docs["CHANGELOG.md"], r"(?m)^## \[Unreleased\]\s*$")
    self.assertIn("v0.1.0", joined)
```

Retain assembled protected-value checks. Add no Gatekeeper/quarantine assertion.

- [ ] **Step 5: Run focused RED**

Run `python3 -m unittest tests.test_community_split.VisitorJourneyTests -v`.

Expected: FAIL with assertion failures because current docs lack the verified Homebrew contract; imports/discovery succeed. If it passes, correct the test before any document edit.

### Task 5: Bring the three visitor documents GREEN

**Files:**

- Modify: `README.md`, `CHANGELOG.md`, `docs/COMMUNITY_RELEASES.md`
- Test: `tests/test_community_split.py`

**Interfaces:**

- Consumes: observed RED and exact live evidence bound to the landed tap SHA.
- Produces: consistent visitor copy within the closed Community allowlist.

- [ ] **Step 1: Write inline-only README copy**

Use this model, adapted only to existing headings: “AxLoop Community v0.1.0 is published for Mac with Apple Silicon. Install it with `brew install axloop/axloop-community/axloop-community`, then run `axloop-community`. Intel Macs and Linux are unsupported by this item. For enterprise AxLoop, visit https://www.axloop.ai.”

Expected: verified command, no fence, and no forbidden stranger tool or quarantine claim.

- [ ] **Step 2: Update Unreleased changelog**

```markdown
### Changed

- Documented the verified one-command Homebrew install for AxLoop Community on Mac with Apple Silicon.
```

Expected: under existing Unreleased, no invented version or rewritten v0.1.0 history.

- [ ] **Step 3: Write the release-guide contract**

State the exact two live assets; chosen tap shape/path; pinned URL/digest; `bin/axloop-community`; confirmed command; Intel/Linux rejection; integrity-not-identity limitation; unsupported third-party tap and user-privilege risk; no Community signing material/workflow; and Nolan's later non-blocking package facts. Cite [Taps](https://docs.brew.sh/Taps), [Acceptable Formulae](https://docs.brew.sh/Acceptable-Formulae), and [Cask Cookbook](https://docs.brew.sh/Cask-Cookbook). Do not add quarantine visitor copy.

- [ ] **Step 4: Run focused GREEN**

Run `python3 -m unittest tests.test_community_split.VisitorJourneyTests -v`.

Expected: PASS, zero failures/errors. Fix inaccurate prose/assertions only; never weaken boundaries.

### Task 6: Verify, refresh review, and hand off

**Files:**

- Verify: four Community allowlist files
- Verify unchanged: `scripts/check-community-split.py`, fixtures, all tap README content except the heading
- Verify tap: exactly the selected Ruby file and heading-only `README.md` change

**Interfaces:**

- Consumes: RED, GREEN, live evidence, separate scope lists.
- Produces: fresh evidence; no merge or publication.

- [ ] **Step 1: Run full module**

Run `python3 -m unittest tests.test_community_split -v`.

Expected: PASS with zero failures and zero errors.

- [ ] **Step 2: Run unchanged checker**

Run `python3 scripts/check-community-split.py`.

Expected: exit 0; checker and fixtures unchanged.

- [ ] **Step 3: Audit scopes separately**

Expected tap list: exactly one selected Ruby path and `README.md`, with only its heading changed to `# homebrew-axloop-community`. Expected Community list: exactly `tests/test_community_split.py`, `README.md`, `CHANGELOG.md`, `docs/COMMUNITY_RELEASES.md`; nothing else.

- [ ] **Step 4: Apply verification-before-completion**

Re-read fresh outputs, RED-before-GREEN evidence, live record, and allowlists. Claim success only when every command/status and field supports it; otherwise hand back the precise blocker.

- [ ] **Step 5: Refresh and freeze current-head review**

Record the Community change's current full head SHA. Treat the only existing GitHub review at `501a1da7c167bf5072b0235548f763217ac7b217` as sign-off solely for the removed Finder-era content, never for this or any later head. Because this amendment creates a new head, require a fresh Imani dated pack, then a fresh Reed critic, then Kit's COMMENT on that same current full head SHA. Any head change invalidates those later-head review artifacts and requires a new dated pack, critic, and current-SHA COMMENT.

## Handoff

Return to Abe the ordered current-head reviewer evidence, accepted shape/path, named tap writer and merger, tap pull-request number, reviewer/merger, file blob SHA, confirmed tap/command, exact tap `main` SHA and two-file scope audit, Community-to-tap/evidence binding, Elena's complete Mac evidence including Homebrew resolution and checksum, cask mechanics, Gatekeeper stop result, uninstall/reinstall record, architecture status and fetched URL/digest, focused RED/GREEN outputs, full-module output, unchanged-checker result, Community scope audit, and any blocker. Do not launch, merge, push, open a pull request, publish, tag, release, upload, or fill reviewer cells.
