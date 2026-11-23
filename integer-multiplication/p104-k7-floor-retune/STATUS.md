# Status, 2026-11-23 04:45 UTC

Candidate 1b, κ = 0.003898224460300 (+4.707e-9 over open PR #8073).
- The package (`package/`, a drop-in `research/p104-k7-floor-retune` on top of PR #8073's head cf4c4b7e) passes the repo's official runner. Running `python3.12 -IB scripts/research_package.py --package research/p104-k7-floor-retune` prints `PASS_REGISTERED_RESEARCH_PACKAGE ... outcome=completed`, and all 7 scopes pass. The log is `official-replay.log`.
- The checker thread's independent exact model matches RESULT.json.
- Nothing has been submitted publicly.
