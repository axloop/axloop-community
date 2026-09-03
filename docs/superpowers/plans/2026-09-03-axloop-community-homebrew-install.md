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
- Tap allowlist: the selected Ruby file only; README unchanged. Community allowlist: only `tests/test_community_split.py`, `README.md`, `CHANGELOG.md`, `docs/COMMUNITY_RELEASES.md`.
- Forbid `.github`, workflows, tags, releases, assets, signing material, runtime code, checker/fixture edits, invented versions, and every other file.
- Do not provide a tap-file landing mechanism. Do not start Community RED until the item is on tap `main` and Elena completes the clean real-Mac run.
- README has no fenced blocks. Stranger commands have no source checkout, command-line downloader, manual checksum, archive unpack, quarantine removal, Python package install, or diagnostic bypass flags.
- Intel macOS and Linux are unsupported; do not invent exact Homebrew errors. Add no quarantine assertion or visitor claim.
- The checksum proves payload integrity, not producer identity. A third-party tap is unsupported by Homebrew and its Ruby runs with the user's privileges. Community has no signing material or workflow.
- Nolan's `.pkg` is later, non-blocking, attended Developer ID on Abe's Mac, and never Community CI. The private factory writes `manifest.sig` before wrapping; wrapping retains payload verification. Current state: zero identities, no `notarytool` profile, no team.
- PR #7 head `6bebf6bc58c108f03900d8efc9a4fafaa0fdf1ec` is unmerged. Rebase prose on launch-time `main`; exclude PRs #1, #3, #5 and PR #6's old Finder content.
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
- Leave unchanged: tap `README.md`

**Interfaces:**

- Consumes: Imani's trust review, Reed's shape review, exact v0.1.0 pin, confirmed repository name.
- Produces: one reviewed item for Abe to arrange onto `main`; no landing action.

- [ ] **Step 1: Confirm the GitHub name**

Confirm `axloop/homebrew-axloop-community`, repository ID `1356097533`, and `main`. Expected: tap identifier `axloop/axloop-community`; if renamed, stop for Abe's confirmation and change only the command string.

- [ ] **Step 2: Record the shape decision**

Compare cask `Casks/axloop-community.rb` (idiomatic binary archive, native `arch`, `:macos`, `binary`) with formula `Formula/axloop-community.rb` (valid third-party alternative, less idiomatic, explicit guards and `bin.install`). Expected: Imani and Reed select exactly one; the visitor stays at one command either way.

- [ ] **Step 3: Write the recommended cask when selected**

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

Expected: exact immutable pin, both guards, one binary artifact, no second tap change.

- [ ] **Step 4: Use the formula only if selected instead**

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

- [ ] **Step 5: Audit without landing**

Expected: exactly one proposed Ruby path; 55-byte README unchanged; no other file or external action. Hand the reviewed artifact to Abe without a landing command.

### Task 2: Clear the live Apple Silicon hard stop

**Files:**

- Read: selected item on tap `main`
- Change: no repository file
- Capture: evidence outside both change sets

**Interfaces:**

- Consumes: selected item actually on `main`, confirmed tap name, Abe's connected real Apple Silicon Mac in clean state.
- Produces: complete evidence unlocking Task 3, or a hard stop.

- [ ] **Step 1: Capture machine and starting state**

Record the Mac model in System Information, tap commit SHA, then run individually:

```text
uname -m
sw_vers
brew --version
brew tap
brew list --cask axloop-community
brew list --formula axloop-community
```

Expected: `arm64`; versions captured; confirmed tap absent; both item checks absent/nonzero. Record full stdout, stderr, and status. If not clean, stop and reschedule after Abe restores a clean state.

- [ ] **Step 2: Run the exact stranger install**

Run `brew install axloop/axloop-community/axloop-community`.

Expected: exit 0 with full stdout/stderr captured. A confirmed rename substitutes only the verified command. Add no flags and no separate tap command.

- [ ] **Step 3: Run the exact invocation**

Run `axloop-community`.

Expected: capture observed output/status without predicting text, and record whether any Gatekeeper or quarantine prompt appeared. That observation is for Imani, not visitor copy.

- [ ] **Step 4: Capture resolution and fetched bytes**

For cask run `brew info --cask axloop/axloop-community/axloop-community`, `command -v axloop-community`, and `brew --cache --cask axloop/axloop-community/axloop-community`. For formula substitute `--formula`. Run `/usr/bin/shasum -a 256` with the exact cached path printed by Homebrew.

Expected: resolved tap/item/version `0.1.0`, installed binary path, item URL at recorded tap commit, and cached digest matching the pin. These are operator evidence after the stranger journey, not visitor commands.

- [ ] **Step 5: Apply the hard stop**

Expected record: model/architecture, macOS/Homebrew versions, clean start, all exact commands, full stdout/stderr/status, resolved tap/item/version, binary path, invocation output, prompt observation, tap SHA, fetched URL/digest. If any field or success is missing, stop before Community RED and report: `Blocked: the clean Apple Silicon Homebrew journey is not fully verified; no Community visitor-contract file changed.`

### Task 3: Extend real-file tests and prove RED

**Files:**

- Modify: `tests/test_community_split.py`, only `VisitorJourneyTests` and needed standard-library imports
- Read: `README.md`, `CHANGELOG.md`, `docs/COMMUNITY_RELEASES.md`
- Leave unchanged: checker and fixtures

**Interfaces:**

- Consumes: Task 2 evidence, confirmed command, existing real-file readers.
- Produces: failing visitor assertions for Task 4; no quarantine assertion.

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
    lowered = readme.lower()
    for forbidden in ("git " + "clone", "pip " + "install", "cu" + "rl",
                      "sha" + "sum", "t" + "ar ", "xa" + "ttr", "doc" + "tor"):
        self.assertNotIn(forbidden, lowered)
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

### Task 4: Bring the three visitor documents GREEN

**Files:**

- Modify: `README.md`, `CHANGELOG.md`, `docs/COMMUNITY_RELEASES.md`
- Test: `tests/test_community_split.py`

**Interfaces:**

- Consumes: observed RED and exact live evidence.
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

### Task 5: Verify and hand off

**Files:**

- Verify: four Community allowlist files
- Verify unchanged: `scripts/check-community-split.py`, fixtures, tap README
- Verify tap: exactly the selected Ruby file

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

Expected tap list: exactly one selected Ruby path, README unchanged. Expected Community list: exactly `tests/test_community_split.py`, `README.md`, `CHANGELOG.md`, `docs/COMMUNITY_RELEASES.md`; nothing else.

- [ ] **Step 4: Apply verification-before-completion**

Re-read fresh outputs, RED-before-GREEN evidence, live record, and allowlists. Claim success only when every command/status and field supports it; otherwise hand back the precise blocker.

## Handoff

Return to Abe the ordered reviewer evidence, accepted shape/path, confirmed tap/command, tap commit and scope audit, Elena's complete Mac evidence including prompt observation and fetched URL/digest, focused RED/GREEN outputs, full-module output, unchanged-checker result, Community scope audit, and any blocker. Do not launch, merge, push, open a pull request, publish, tag, release, upload, or fill reviewer cells.
