# Onboarding — 5 minutes, conversational

The assistant should set this up **by asking, not by making you fill JSON.** Copy `templates/data.template.json` → `engine/data.json` and gather:

## 1. About you
- Goal: hypertrophy / strength / recomposition.
- Phase: bulk / cut / maintenance. (If cut: target rate ~0.5–1%/week; protein 2.3–3.1 g/kg lean mass — see knowledge-base §9.)
- Units: kg or lb.

## 2. Your split
Pick or define your session types. Default 5-day: `UPPER · LOWER · PUSH · PULL · LEGS`.
- The `schedule` in `data.json` maps days → types (or `rest`).
- The type strings **must match `MUSCLE_BY_TYPE` in `engine/gym.py`.** To add a custom type, add it there with its muscles.
- Train every day? The engine rotates so each muscle gets 48h. Prefer rest days? Just don't train — the engine always offers the best next type.

## 3. Readiness source (pick one)
- **Wearable (WHOOP-style):** export a `recovery.md` into `engine/` with rows `| YYYY-MM-DD | 57% | ...`.
- **Manual / any wearable %:** write `engine/readiness.json` → `{"recovery": 57}`.
- **Self-check (no device):** `engine/readiness.json` → `{"selfcheck": {"sleep": 4, "energy": 3, "soreness": 4}}` (1–5 each, 5 = best / no soreness). The engine maps it to a %.

## 4. Log 1–2 recent sessions
So the engine has a baseline to compute overload and pick your next session. Each session:
```json
{ "date": "2026-06-24", "type": "UPPER",
  "exercises": [
    { "name": "Bench Press", "sets": [ {"w":70,"r":8}, {"w":70,"r":8}, {"w":70,"r":8} ] },
    { "name": "Lat Pulldown", "sets": [ {"w":50,"r":12}, {"w":50,"r":12} ] }
  ] }
```
- `w` = weight, `r` = reps. Add `"perSide": true` for dumbbell/unilateral. **Always log reps** — without reps there's no overload to measure.
- Set `last_by_type` (e.g. `{"UPPER":"2026-06-24"}`).

## 5. Verify
```bash
python3 engine/gym.py reconcile   # ok:true?
python3 engine/gym.py next        # what to train today
```

That's it. Ask your assistant: *"what do I train today?"*
