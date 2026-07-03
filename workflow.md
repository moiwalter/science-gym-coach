---
title: "Science Gym Coach — Workflow / Operating Manual"
ref: knowledge-base.md (science) · engine/gym.py (math) · science-agent.md (evidence authority)
---

# Workflow — how the coach operates

> The assistant reads this first. The rule of the whole system: **decisions come from `gym.py` (deterministic) + `knowledge-base.md` (cited science), never from the assistant's intuition.**

## ⛔ Principle #0 — the user's log is the source of truth

What and WHEN the user trained is **whatever they log/confirm**, never a wearable. Wearables miss sessions; they only give a reliable **recovery %**. **Never infer a session's date — ask.** Before re-dating or overwriting a logged session, ask first.

## The flow (per session)

```
TRIGGER (user pastes a session, or asks "what today?")
 0. READINESS (obligatory)  → gym.py readiness (WHOOP export or readiness.json self-check) → 🟢/🟡/🔴 + directive
 1. PARSE                   → user's raw input → structured entry in engine/data.json
 2. LOG                     → data.json → log.md (human view, with the CONFIRMED date)
 3. OVERLOAD                → gym.py compute → per-exercise verdict + next targets → tracker.md
 4. PROGRESSION             → gym.py compute → weekly volume vs MAV, PRs, stalls → block-state.md
 5. NEXT                    → gym.py next → what to train next (deficit + recovery), readiness baked in → hoy.md
 6. RECONCILE               → gym.py reconcile ; if ok:false, fix before closing
```

## Deciding the next session (the core)

Run `python3 engine/gym.py next` and take `recomendado`. It picks by:
- **Volume deficit** (§1): the muscle groups furthest below their weekly target (MAV).
- **Recovery** (§4b): a muscle trained <48h ago is skipped — its strength hasn't recovered, so training it is poor stimulus + fatigue.
- **Over-MAV muscles** are de-prioritized (don't feed more volume to an already-maxed muscle).

**Never decide by the day of the week.** The calendar is only a default; a muscle lives in multiple session types (e.g. lats train in "UPPER" and "PULL"), which the day-of-week can't see. `gym.py next` is the single source for this.

## Targets (deterministic)

Run `python3 engine/gym.py compute` → `next_targets[TYPE]`. Every exercise returns `{series, reps, peso, meta}`:
- **series × rep-range × weight** — always explicit.
- **meta** — self-explained: what you did last time + the double-progression trigger ("when you hit the top reps in all sets → +increment").

### Rendering rule — FIXED format, verbatim metas

`hoy.md` always follows `templates/hoy.template.md` — the **whole skeleton is fixed**, same sections in the same order, every session:

1. Frontmatter with `generado:` provenance (which commands were run + which past session the targets compare against).
2. `# {emoji} {TYPE} · {focus muscles}` title.
3. **Why {TYPE}** — 1–2 lines from `gym.py next`: deficit + recovery + what's excluded and why.
4. **Bodyweight** blank.
5. One readiness line: `> {🟢/🟡/🔴} **READINESS {pct}%** ({date} · trend {a→b→c}) → {directive from gym.py readiness, VERBATIM}.`
6. One heading per exercise (`## X · Name — sets×reps · weight`), the `meta` string from `gym.py compute` **copied verbatim** (the assistant never rewrites it — rewording is where inconsistency is born), one checkbox per set (`- ☐ ____ × ____`, narrow = phone-readable).
7. `> **Goal #1 today:** …` (the session's overload, from the targets) + `> **Notes:**`.

Whatever the assistant shows in chat is a **literal copy of the file**, never a parallel re-rendering. If the recovery score arrives **after** the sheet was generated (user scores on waking), update **only the readiness line, keeping the exact format** — don't restyle it; the directive always comes verbatim from `gym.py readiness`, never paraphrased.

## Autoregulation (§10)

`readiness` maps the recovery score to a directive: 🟢 (≥67) push, 0–1 RIR, add load · 🟡 (34–66) as written, 2 RIR, hold load · 🔴 (<34) lighter: ~40% fewer sets, RIR 3–4, or weak-points/Zone 2/rest. Adjust **load**, and — if the user trains daily — never skip; rotate the split so each muscle still gets 48h.

## Config

- **Your split** lives in `data.json → schedule`. The `TYPE` strings must match `MUSCLE_BY_TYPE` in `gym.py` (edit both to add a custom split).
- **Volume targets (MAV), prescriptions (sets×reps), increments** live at the top of `gym.py` — one place, edit to individualize.
- **Train daily vs rest days:** the engine always returns the best next type; if you rest some days, just don't train. If you train daily, the 48h rule handles recovery by rotating.
