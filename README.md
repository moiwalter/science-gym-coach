# 🔬 Science Gym Coach

A **science-based, deterministic** training coach you run with an AI assistant (Claude Code / any agent that can run Python and read Markdown).

The idea: an AI coach shouldn't improvise your training. So here the **decisions live in code** (`engine/gym.py`) and the **science lives in a cited knowledge base** (`knowledge-base.md`) — the assistant only reads them and translates. No vibes, no drift.

## What makes it different

- **Decides what to train by data, not by the calendar.** It picks your next session by which muscles are most under-trained (vs their weekly-volume target) *and* recovered (≥48h since last hard session) — so it never sends you to train legs the day after legs.
- **Deterministic targets.** Every exercise comes as `N sets × rep-range × weight` with a self-explained overload note. You never have to remember last week.
- **Readiness autoregulation, wearable optional.** Bakes a recovery score into the session (🟢 push / 🟡 hold / 🔴 lighter). Use a WHOOP export *or* a 3-question self-check (sleep / energy / soreness).
- **Every rule is cited and tiered.** The knowledge base carries the primary references (Pelland 2026, Robinson 2024, Schoenfeld, Helms 2014, …), each verified against the source, tagged **A** (strong) / **B** (moderate) / **C** (heuristic).

## How a day looks

You ask your assistant **"what do I train today?"**. It runs the engine and hands you one session sheet (`hoy.md`) — always the same fixed format, readable on your phone at the gym:

```markdown
# 🔥 LEGS · DAY 5 · Fri 03-jul

## 1 · WHAT'S UP — why this session and not another (decided by gym.py next)
- **Session:** LEGS (glutes + hamstrings + calves)
- **Reason:** glutes 0 sets in 7 days, calves 3 — most behind AND recovered (≥48h).
  Chest trained yesterday → no pushing today.
- **Phase:** week 3/12 · ACCUMULATION — add load where compute orders it.

## 2 · TRAFFIC LIGHT — how hard to push today (readiness only)
- 🟢 **73%** (2026-07-03 · trend 57→38→73) → PUSH: top sets 0–1 RIR, add load
  if you hit the top reps.
- Rule: 🟢 push, add load · 🟡 keep load, 2 RIR · 🔴 light version, still train.

## 3 · THE SESSION — Target = what to beat · TODAY = you fill weight×reps
| # | Exercise · sets×reps · weight | Target | TODAY |
|---|-------------------------------|--------|-------|
| A | **Hip Thrust** · 3×10–12 · **20kg/side** | Hold 20kg/side for all 3 sets and chase 12 reps in ALL. Last time: 12, 10 (only 2 of 3 sets). When you hit 12 in all 3 → 25kg. | |

## 4 · GOAL #1 — if you only achieve one thing today, it's this
- Complete ALL sets — full sets ARE today's overload, not more weight.

## 5 · WHEN DONE — close the loop
- **Bodyweight:** ____ kg · **Notes:**
- Tell your assistant **"done"** and it archives.
```

You fill the TODAY column at the gym. When you're done you paste your numbers (even messy voice-dictated ones — *"20 side x12 x11 x10, curl 50 x12x12x10"*) and say **"log it"**. The assistant parses, logs, compares against last time (double progression), updates your progress files, and has tomorrow's answer ready.

That's the whole loop: **ask → train → paste → repeat.**

## Quick start

1. **Clone the repo** and open it with your AI assistant (e.g. `claude` inside the folder).
2. **Tell it: "onboard me"** — it should follow `ONBOARDING.md`: a 5-minute conversation (goal, split, readiness source, 1–2 recent sessions). You talk; it fills `engine/data.json`. No wearable required.
3. **Verify:** `python3 engine/gym.py reconcile` → `ok: true`.
4. **Ask: "what do I train today?"** — and you're running.

Works from day one; gets smarter as you log.

**Already running an older version?** `git pull` and tell your assistant **"we just updated — follow `UPGRADING.md`"**. It upgrades the system (engine, templates, rules) while leaving your data (log, PRs, customizations) untouched, and briefs you on what changed.

## What's in the repo

| File | What it is |
|------|-----------|
| `SKILL.md` | Entry point for the AI assistant — what this skill does and how to use it |
| `workflow.md` | The operating manual: agent flow, ground rules, fixed rendering format |
| `engine/gym.py` | The deterministic engine — all math and decisions live here |
| `engine/data.json` | *(you create it)* Your log: sessions, sets, bodyweight — the source of truth |
| `knowledge-base.md` | The cited science every recommendation traces back to (§ numbered) |
| `science-agent.md` | The evidence-auditor role: any quantitative claim must cite the KB |
| `ONBOARDING.md` | The 5-minute conversational setup |
| `UPGRADING.md` | Assistant instructions for **updating an existing install** after a `git pull` — what upgrades, what's untouchable, format version history |
| `templates/` | Fixed formats for the session sheet (`hoy`), log, tracker, progress files |

## The engine

```bash
python3 engine/gym.py readiness   # recovery → 🟢/🟡/🔴 + directive (WHOOP or self-check)
python3 engine/gym.py next        # what to train today (deficit + recovery), readiness baked in
python3 engine/gym.py compute     # weekly volume vs target · PRs (e1RM) · overload targets · stalls
python3 engine/gym.py trajectory  # bodyweight trend → cut ETA + lift trends
python3 engine/gym.py reconcile   # integrity check across the data files
python3 engine/gym.py all --json  # everything, structured
```

## Ground rules (what keeps the AI honest)

These are baked into `workflow.md` — if you fork this, keep them:

1. **Your log is the source of truth** for what/when you trained — never the wearable, never the calendar, never the AI's memory.
2. **The engine decides, the assistant translates.** Next session = `gym.py next`. Targets = `gym.py compute`, copied **verbatim** — the assistant never re-words a prescription (re-wording is where drift is born).
3. **Fixed delivery format.** Every session sheet follows `templates/hoy.template.md` — same sections, same order, every time. What the assistant shows in chat is a literal copy of the file.
4. **Every quantitative rule cites the knowledge base** (§ + evidence tier). If it can't cite it, it doesn't prescribe it.
5. **Never guess dates.** The assistant asks which day a session was; it never infers it.

## Customizing

- **Your split:** edit `schedule` in `engine/data.json`; session types must exist in `MUSCLE_BY_TYPE` in `engine/gym.py` (add your own with its muscles).
- **Volume targets, rep ranges, increments:** constants at the top of `engine/gym.py`, each traceable to a KB section.
- **Units:** kg or lb, set at onboarding.

## Science

All claims in `knowledge-base.md` were verified against primary sources (PubMed/DOI). Highlights: weekly volume drives hypertrophy with diminishing returns (Pelland 2026); train close to failure, failure not required (Robinson 2024, Refalo 2023); space a muscle's hard sessions ~48h for performance recovery (not an "MPS window"); protein in a cut = 2.3–3.1 g/kg of **lean** mass (Helms 2014).

## License

MIT — see [LICENSE](LICENSE). Educational, **not medical advice**.
