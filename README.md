# 🔬 Science Gym Coach

A **science-based, deterministic** training coach you run with an AI assistant (Claude Code / any agent that can run Python and read Markdown).

The idea: an AI coach shouldn't improvise your training. So here the **decisions live in code** (`engine/gym.py`) and the **science lives in a cited knowledge base** (`knowledge-base.md`) — the assistant only reads them and translates. No vibes, no drift.

## What makes it different

- **Decides what to train by data, not by the calendar.** It picks your next session by which muscles are most under-trained (vs their weekly-volume target) *and* recovered (≥48h since last hard session) — so it never sends you to train legs the day after legs.
- **Deterministic targets.** Every exercise comes as `N sets × rep-range × weight` with a self-explained overload note. You never have to remember last week.
- **Readiness autoregulation, wearable optional.** Bakes a recovery score into the session (🟢 push / 🟡 hold / 🔴 lighter). Use a WHOOP export *or* a 3-question self-check (sleep / energy / soreness).
- **Every rule is cited and tiered.** The knowledge base carries the primary references (Pelland 2026, Robinson 2024, Schoenfeld, Helms 2014, …), each verified against the source, tagged **A** (strong) / **B** (moderate) / **C** (heuristic).

## The engine

```bash
python3 engine/gym.py readiness   # recovery → 🟢/🟡/🔴 + directive (WHOOP or self-check)
python3 engine/gym.py next        # what to train today (deficit + recovery), readiness baked in
python3 engine/gym.py compute     # weekly volume vs target · PRs (e1RM) · overload targets · stalls
python3 engine/gym.py trajectory  # bodyweight trend → cut ETA + lift trends
python3 engine/gym.py reconcile   # integrity check across the data files
python3 engine/gym.py all --json  # everything, structured
```

## Quick start

1. Copy `templates/data.template.json` → `engine/data.json`, set your split and log a couple of sessions (see `ONBOARDING.md`).
2. Point your AI assistant at `SKILL.md` + `workflow.md`.
3. Ask: *"what do I train today?"* / *"log my session"* / *"give me my targets."*

No wearable required. Works from day one; gets smarter as you log.

## Science

All claims in `knowledge-base.md` were verified against primary sources (PubMed/DOI). Highlights: weekly volume drives hypertrophy with diminishing returns (Pelland 2026); train close to failure, failure not required (Robinson 2024, Refalo 2023); space a muscle's hard sessions ~48h for performance recovery (not an "MPS window"); protein in a cut = 2.3–3.1 g/kg of **lean** mass (Helms 2014).

## License

MIT — see [LICENSE](LICENSE). Educational, **not medical advice**.
