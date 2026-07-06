---
title: "TODAY — quick capture"
note: "Fill the TODAY column with weight × reps per set. When done, tell your assistant 'done' and it archives it."
generado: "gym.py next + gym.py readiness + gym.py compute (targets verbatim) · v3 numbered-sections format"
---

<!-- FIXED SKELETON v3 — 5 numbered sections, same order, every session. Fill the {slots}; never restyle. -->
<!-- Each section header DECLARES ITS UTILITY (what it is + what it's for) so the athlete always reads the same map. -->
<!-- Exercises go in ONE TABLE (not a checkbox list) — tables fill cleaner and scan faster. -->

# 🔥 {TYPE} · DAY {n} · {weekday DD-mmm}

## 1 · WHAT'S UP — why this session and not another (decided by gym.py next)
- **Session:** {TYPE} ({focus muscles})
- **Reason:** {1 line from gym.py next — volume deficit + recovery + what's excluded}
- **Phase:** week {x}/{total} · {PHASE} — {what it implies today, few words}

## 2 · TRAFFIC LIGHT — how hard to push today (readiness only)
- {🟢/🟡/🔴} **{pct}%** ({date} · trend {a→b→c}) → {directive from gym.py readiness, VERBATIM}
- Rule: 🟢 push, add load · 🟡 keep load, 2 RIR · 🔴 light version, still train.
<!-- If the score arrives after the sheet was generated, update ONLY the score line, keeping this exact format. -->

## 3 · THE SESSION — Target = what to beat · TODAY = you fill weight×reps
| # | Exercise · sets×reps · weight | Target | TODAY (weight×reps per set) |
|---|-------------------------------|--------|------------------------------|
| A | **{Exercise name}** · {series}×{reps} · **{peso}** | {`meta` from gym.py compute — VERBATIM, do not rewrite} | |
| B | **{Exercise name}** · {series}×{reps} · **{peso}** | {`meta` from gym.py compute — VERBATIM, do not rewrite} | |

<!-- ...one row per exercise -->

## 4 · GOAL #1 — if you only achieve one thing today, it's this
- {the session's overload, from targets — e.g. "complete ALL sets" / "add load where compute says so"}

## 5 · WHEN DONE — close the loop
- **Bodyweight:** ____ {unit}
- **Notes:**
- Tell your assistant **"done"** and it archives (parse → log → tracker → next session).
