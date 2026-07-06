# 🔄 UPGRADING — assistant instructions for updating an existing install

> **Audience: the AI assistant** operating this system for a user who already has it running.
> When the user pulls a new version of this repo (`git pull`, re-download, re-clone), **treat it as an update, not a fresh install**: the user has history, customizations, and muscle memory built on the previous version. Your job is to merge the new system into their setup **without losing anything of theirs** — and to tell them what changed.

---

## 0 · The mental model — SYSTEM vs DATA

The repo splits cleanly in two. Everything you do during an upgrade follows from this split:

| | What it is | On update |
|---|------------|-----------|
| **SYSTEM** (the repo's) | `engine/gym.py` logic · `templates/` · `workflow.md` rules · `knowledge-base.md` · `SKILL.md` / `ONBOARDING.md` | ⬆️ **Upgrades.** The new version wins. |
| **DATA** (the user's) | `engine/data.json` · their log / tracker / block-state / progress files · the current session sheet (`hoy.md`) · `readiness.json` · any custom constants they set | 🔒 **Never overwritten, never regenerated, never "migrated" destructively.** |

**Golden rule: formats apply FORWARD, never retroactively.** A new sheet format applies to the *next* sheet you generate. You never rewrite log history, re-render old entries, or "clean up" past files to match a new template. The log is an archive of what happened — it stays exactly as it was written.

---

## 1 · Upgrade protocol (run this after any pull)

1. **See what actually changed.**
   ```bash
   git log --oneline HEAD@{1}..HEAD        # commits that just came in (after git pull)
   git diff HEAD@{1}..HEAD --stat           # which files
   ```
   No reflog (fresh re-clone / zip download)? Compare the repo's `templates/` and `workflow.md` against how the user's current sheets actually look, and check the **format version history** below to locate them.

2. **Classify each change** before touching anything:
   - **Engine (`engine/gym.py`)** → new logic wins, user constants survive (see §2).
   - **Templates / rendering rules** → apply to the *next* generated file only (see §3).
   - **Knowledge base / science** → read the diff; if a prescription rule changed (volume targets, RIR, frequency), it affects *future* targets — never re-judge past sessions against new science.
   - **Workflow / ground rules** → adopt immediately; these govern your behavior, not the user's files.

3. **Check for collisions with user customizations** (§2). Resolve them *before* running anything.

4. **Verify integrity:**
   ```bash
   python3 engine/gym.py reconcile   # must return ok:true
   ```
   If `ok:false`, fix what it flags before closing the upgrade. A version bump must never leave the data desynced.

5. **Brief the user — short, concrete, once.** 3–5 lines max:
   - what's new and **what they will actually notice** ("your next session sheet will look different: 5 numbered sections"),
   - what did **not** change ("your log, your PRs, your targets are untouched"),
   - anything they must do (usually nothing).
   Don't dump the changelog on them; translate it.

---

## 2 · User customizations — what survives every upgrade

These are the user's, even though they live in SYSTEM files. If an update touches them, **merge — don't replace**:

- **Their split**: `schedule` in `engine/data.json` + any custom session types they added to `MUSCLE_BY_TYPE` in `gym.py`. If the new `gym.py` doesn't know their custom type, port it in.
- **Tuned constants** at the top of `gym.py` (volume targets/MAV, rep ranges, increments, readiness thresholds). If the user changed a value and the update changed the *same* value: **the user's value wins by default** — flag the difference, cite what the new default is and why (KB §), and let them decide.
- **Units** (kg/lb) and readiness source (wearable vs self-check).
- Any local files the repo doesn't ship (their notes, exports, extra trackers): ignore them, never clean them up.

Practical method when `gym.py` changed and the user had edits: take the **new file as base**, re-apply the user's constant values on top, run `reconcile` + one `compute` to sanity-check output.

---

## 3 · Format changes — how to switch without whiplash

- The **current session sheet** (`hoy.md`): if it's *unfilled*, regenerate it in the new format right away. If the user already wrote numbers in it, **leave it alone** — parse and archive it in the format it was born in; the new format starts next session.
- **Old sheets / log entries: never re-render.** Mixed history is fine and expected — it documents when the upgrade happened.
- When you generate the first sheet in a new format, say so in one line ("this is the new v3 layout — same data, now in 5 fixed sections").

### Format version history (session sheet `hoy.md`)

Use this to identify which version a user is coming from and what the jump means:

| Version | Since | Layout | Migration note |
|---------|-------|--------|----------------|
| **v1** | initial release | One heading per exercise + checkbox list per set | Superseded: checkboxes came back with numbers scattered across blanks → parse ambiguities. |
| **v2** | 2026-07-04 (`450b159`) | All exercises in **one table** (columns: # · Exercise · sets×reps · weight · Target · TODAY) | Tables fill cleaner and scan faster. Targets verbatim from `gym.py compute`. |
| **v3** | 2026-07-06 (`d17233d`) | **5 numbered sections, each header declares its utility**: 1 WHAT'S UP · 2 TRAFFIC LIGHT · 3 THE SESSION (the v2 table) · 4 GOAL #1 · 5 WHEN DONE. Bodyweight moved from top to the closing section (it's an output, not an input). | Purely structural — table and verbatim-targets rules unchanged. The athlete always reads the same map; the ending is as fixed as the start. |

(When you ship a format change in a fork, add a row here — this table is the migration contract.)

---

## 4 · What an upgrade must NEVER do

- ❌ Overwrite or regenerate `engine/data.json`, the log, tracker, block-state or progress files "to match the new version".
- ❌ Rewrite or re-format historical entries.
- ❌ Silently drop the user's custom split, constants, or units.
- ❌ Re-date anything. (Principle #0 still rules: the user's log is the truth of what/when they trained.)
- ❌ Close the upgrade with `reconcile` failing.

If any step would require breaking one of these, stop and ask the user instead.
