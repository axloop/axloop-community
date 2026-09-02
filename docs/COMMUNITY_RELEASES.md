# Community releases

Community artifacts and GitHub Releases live in this private repository: https://github.com/axloop/axloop-community.

Enterprise source, build, signing, and acceptance remain in https://github.com/ascendantventures/axloop-edge-poc. This repository is the Releases home, not a copy of that factory.

No Community release has been published from this repository yet. The enterprise Aug 29 staging draft tagged `community-acceptance-staging-2026-08-29` is not a Community release, is not this repository's release home, and must not be used, copied, retagged, attached, or published.

The CLI `radar`→`crawler` rename (radar→crawler) is later and is not part of this split.

The enterprise repository retains Community builds, signing requests, attended signing with PKCS#8 on Abe's Mac, offline verification, release envelopes, clean-host acceptance, notarization, and Authenticode gates. PKCS#8 never enters this repository or CI.

## What this repository does not do

This repository does not build, sign, accept, notarize, or publish artifacts. Publishing a Community release is a separate, future approval and is not represented by any workflow, flag, or dormant step in this repository. The optional draft-only attachment workflow described in the design has been omitted; documentation establishes the Releases home.

## Boundary check

`scripts/check-community-split.py` verifies that this tree stays a Releases home and never becomes a copy of the enterprise factory. Run it from the repository root:

```bash
python3 -m unittest -v tests/test_community_split.py
python3 scripts/check-community-split.py .
```
