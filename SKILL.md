---
name: science-gym-coach
description: Science-based hypertrophy/strength coach. Use when the user wants to log a gym session, know what to train today, get progressive-overload targets, or check training readiness. Decides WHAT to train by muscle-volume deficit + recovery (not by day-of-week), gives deterministic targets (sets × rep-range × weight), and autoregulates by a recovery score (WHOOP or a manual self-check). Every decision cites the knowledge base. Works with or without a wearable.
license: MIT
---

# 🔬 Science Gym Coach

A portable, evidence-based training system. The **math and the decisions live in a deterministic engine (`gym.py`)**, the **science lives in a cited `knowledge-base.md`**, and the assistant only translates — so recommendations don't drift into vibes.

## What it does

- **"What do I train today?"** → `gym.py next`: picks the session type by **muscle-volume deficit (vs your MAV) among the muscles that are recovered (≥48h)** — not by the day of the week. A muscle trained <48h ago is skipped (its strength hasn't recovered).
- **Deterministic targets** → `gym.py compute`: every exercise gets **N sets × rep-range × weight** plus a self-explained note ("last time you did X → do Y; when you hit the top reps in all sets, add 2.5kg"). No ambiguity, no "remember last week."
- **Readiness autoregulation** → `gym.py readiness`: reads a recovery score and bakes it into the session (🟢 push · 🟡 hold · 🔴 lighter). Uses **WHOOP if you have it, or a 3-question self-check** (sleep / energy / soreness) otherwise.
- **Progressive overload** → double progression on working sets (no ramps), tracked from your own logged reps.
- **Verification** → `gym.py reconcile` cross-checks the data so logs never drift.

## How to use it (assistant instructions)

1. **Read `workflow.md` first** — it's the operating manual (the agent flow + Principle #0: the user's log is the source of truth for what/when they trained).
2. **Before prescribing:** run `python3 engine/gym.py readiness` (WHOOP export or `readiness.json` self-check).
3. **To pick the session:** run `python3 engine/gym.py next` → take `recomendado` + `readiness` + `ataca`/`ojo`.
4. **To fill targets:** run `python3 engine/gym.py compute` → `next_targets` for that type.
5. **Always cite** the knowledge-base section + tier (A/B/C) — see `science-agent.md`.
6. **After any write to the data:** run `python3 engine/gym.py reconcile`; fix if `ok:false`.

## Setup

Copy `templates/data.template.json` → `engine/data.json` and fill your split + first sessions. See `ONBOARDING.md` for a 5-minute conversational setup. No wearable required.

## Files

| File | Role |
|------|------|
| `engine/gym.py` | deterministic engine — `compute` · `next` · `readiness` · `trajectory` · `reconcile` |
| `knowledge-base.md` | the cited science (all refs verified against primary sources) |
| `science-agent.md` | the evidence authority — how every decision is justified + evidence tiers |
| `workflow.md` | the operating manual / agent flow |
| `ONBOARDING.md` | conversational setup |
| `templates/` | data + log + tracker + block-state + hoy scaffolds |

> ⚕️ Educational, not medical advice. Consult a professional for injury, illness, or medical conditions.
