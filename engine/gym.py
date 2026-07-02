#!/usr/bin/env python3
"""
gym.py — motor de cómputo determinista del Training System.
La matemática vive aquí, NO en la cabeza del agente (donde nacían los errores).

Lee data.json (la capa estructurada) y produce reportes EXACTOS:
  compute     #1  volumen/músculo, PRs (e1RM), estancamientos, próximos targets
  trajectory  #3  proyección de peso corporal -> meta del cut + tendencia de lifts
  reconcile   #4  cruza data.json <-> log.md <-> tracker.md <-> block-state.md y marca drift
  all             los tres

Uso:  python3 gym.py all   |   python3 gym.py compute --json
La verdad de QUÉ/CUÁNDO sigue siendo lo que el usuario confirma en su log. Esto solo computa sobre eso.
"""
import json, os, re, sys, argparse, datetime

DIR = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(DIR, "data.json")
RECOVERY_MD = os.path.join(DIR, "recovery.md")       # opcional: export tipo WHOOP
READINESS_JSON = os.path.join(DIR, "readiness.json") # opcional: auto-chequeo manual o % de wearable

# ---- mapeo ejercicio -> músculo (por keyword, así ejercicios nuevos mapean solos) ----
def muscle_of(name):
    n = name.lower()
    if "rear" in n or "face pull" in n: return "delt_post"
    if "lateral" in n: return "delt_lat"
    if "calf" in n or "pantorr" in n: return "pantorrilla"
    if "leg curl" in n or "rdl" in n or "romanian" in n or "ham" in n: return "femoral"
    if "hip thrust" in n or "glute" in n or "abductor" in n or "kickback" in n: return "gluteo"
    if "squat" in n or "leg press" in n or "leg extension" in n or "extension" in n and "triceps" not in n and "overhead" not in n: return "cuadriceps"
    if "split" in n or "lunge" in n: return "cuadriceps"
    if "crunch" in n or "leg raise" in n or "ab wheel" in n or "plank" in n: return "core"
    if "triceps" in n or "pushdown" in n or "dip" in n: return "triceps"
    if ("curl" in n) and "leg" not in n: return "biceps"
    if "shoulder" in n or "overhead press" in n or "ohp" in n: return "hombro"
    if "row" in n or "pulldown" in n or "pull-up" in n or "pullover" in n: return "espalda"
    if "press" in n or "bench" in n or "fly" in n or "chest" in n: return "pecho"
    return "otro"

MAV = {  # rango objetivo de sets/semana (knowledge-base §1)
    "pecho": (12,20), "espalda": (12,20), "cuadriceps": (12,20), "femoral": (12,20),
    "gluteo": (8,16), "hombro": (8,16), "delt_lat": (8,14), "delt_post": (8,14),
    "biceps": (10,16), "triceps": (10,16), "pantorrilla": (8,16), "core": (6,12),
}

# Prescripción POR EJERCICIO: (series, rep_min, rep_max, incremento_kg).
# Fuente única del "qué buscar". El orden importa (keywords específicas primero:
# 'leg curl' antes de 'curl', 'rear-delt' antes de 'fly', 'leg press' antes de 'press').
PRESCRIPTION = [
    (["bulgarian","split","lunge"],        (2, 10, 12, 2.5)),
    (["back squat","squat"],               (4, 6, 8, 5.0)),
    (["romanian","rdl","deadlift"],        (3, 8, 10, 2.5)),
    (["leg press"],                        (3, 10, 12, 5.0)),
    (["leg curl"],                         (3, 10, 12, 2.5)),
    (["leg extension"],                    (3, 12, 15, 2.5)),
    (["calf","pantorr"],                   (4, 8, 12, 2.5)),
    (["hanging leg raise","leg raise","crunch","ab wheel","plank"], (3, 10, 15, 0.0)),
    (["hip thrust","glute","abductor","kickback"], (3, 10, 12, 5.0)),
    (["bench"],                            (4, 6, 8, 2.5)),
    (["incline db press","incline smith","incline press"], (3, 8, 10, 2.5)),
    (["machine chest press","chest press"],(3, 10, 12, 2.5)),
    (["rear-delt","rear delt","face pull"],(4, 15, 20, 2.5)),
    (["cable fly","fly"],                  (3, 12, 15, 2.5)),
    (["lateral"],                          (4, 12, 20, 2.5)),
    (["chest-supported row","chest supported"], (3, 8, 10, 2.5)),
    (["single-arm","db row"],              (3, 10, 12, 2.5)),
    (["straight-arm","pullover"],          (3, 12, 15, 2.5)),
    (["lat pulldown","pulldown","pull-up"],(4, 8, 10, 2.5)),
    (["cable row","seated row","row"],     (4, 8, 12, 2.5)),
    (["shoulder press","overhead press","ohp"], (3, 8, 12, 2.5)),
    (["overhead triceps","triceps","pushdown","dip"], (3, 10, 12, 2.5)),
    (["hammer"],                           (3, 10, 12, 2.5)),
    (["curl"],                             (3, 8, 12, 2.5)),  # bíceps (leg curl ya capturado arriba)
]

def prescription(name):
    """(series, rep_min, rep_max, incremento_kg) para el ejercicio. Fuente única."""
    n = name.lower()
    for keys, spec in PRESCRIPTION:
        if any(k in n for k in keys):
            return spec
    return (3, 8, 12, 2.5)  # default aislamiento

def rep_top(name):  # compat: tope del rango de reps
    return prescription(name)[2]

def e1rm(w, r):  # Epley
    try:
        w = float(w); r = float(r)
        return round(w * (1 + r/30.0), 1)
    except (TypeError, ValueError):
        return None

def load():
    with open(DATA) as f: return json.load(f)

def working_sets(ex):
    """Sets reales (excluye warm-ups de rampa): los del peso máximo usado."""
    sets = [s for s in ex.get("sets", []) if isinstance(s.get("w"), (int, float))]
    if not sets: return ex.get("sets", [])
    top = max(s["w"] for s in sets)
    return [s for s in sets if s["w"] == top]

# ---------------- #1 COMPUTE ----------------
def compute(d):
    out = {"volumen": {}, "prs": {}, "next_targets": {}, "stalls": []}
    # volumen últimos 7 días
    today = max((s["date"] for s in d["sessions"]), default=None)
    if today:
        t = datetime.date.fromisoformat(today)
        week = [s for s in d["sessions"] if (t - datetime.date.fromisoformat(s["date"])).days <= 6]
    else:
        week = []
    vol = {}
    for s in week:
        for ex in s["exercises"]:
            if ex.get("skipped"): continue
            m = muscle_of(ex["name"])
            vol[m] = vol.get(m, 0) + len([x for x in ex.get("sets", []) if x.get("r")])
    out["volumen"] = {m: {"sets": n, "MAV": MAV.get(m), "estado": _vol_state(n, MAV.get(m))}
                      for m, n in sorted(vol.items())}
    # PRs (mejor e1RM por lift, de todo el historial)
    prs = {}
    for s in d["sessions"]:
        for ex in s["exercises"]:
            if ex.get("skipped"): continue
            for st in ex.get("sets", []):
                e = e1rm(st.get("w"), st.get("r"))
                if e and e > prs.get(ex["name"], (0, None, None))[0]:
                    prs[ex["name"]] = (e, f'{st["w"]}x{st["r"]}', s["date"])
    out["prs"] = {k: {"e1rm": v[0], "set": v[1], "fecha": v[2]} for k, v in sorted(prs.items(), key=lambda x:-x[1][0])}
    # próximos targets por tipo — DETERMINÍSTICO y AUTOEXPLICADO.
    # Cada target trae: series, rango de reps, peso, meta clara y la ÚLTIMA VEZ explícita
    # (para no depender de recordar la semana pasada). Doble progresión.
    for typ, date in d.get("last_by_type", {}).items():
        sess = next((s for s in d["sessions"] if s["date"] == date and s["type"] == typ), None)
        if not sess: continue
        tg = {}
        for ex in sess["exercises"]:
            if ex.get("skipped"): continue
            sets, lo, hi, inc = prescription(ex["name"])
            per = "/lado" if ex.get("perSide") else ""
            ws = working_sets(ex)
            reps = [s.get("r") for s in ws if isinstance(s.get("r"), (int, float))]
            w = next((s["w"] for s in ws if isinstance(s.get("w"), (int, float))), None)
            if not reps: continue
            # resumen explícito de la última vez
            if len(set(reps)) == 1:
                ult = f"{w}{per}×{reps[0]} en las {len(reps)} series" if w else f"×{reps[0]} en las {len(reps)} series"
            else:
                ult = (f"{w}{per}×" if w else "×") + ",".join(str(r) for r in reps)
            sube = w is not None and min(reps) >= hi and len(reps) >= sets
            if w is None:  # peso corporal (ej. hanging leg raise)
                peso = "peso corporal"
                meta = (f"Haz {sets} series buscando {hi} reps en todas. "
                        f"La vez pasada ({date}): {ult}.")
            elif sube:
                nw = round(w + inc, 1)
                peso = f"{nw}kg{per}"
                meta = (f"SÚBELE EL PESO a {nw}kg{per}: la vez pasada ({date}) pegaste {ult} "
                        f"= tope del rango en las {sets}. Baja las reps al piso ({lo}) y vuelve a subir a {hi}.")
            else:
                peso = f"{w}kg{per}"
                falta = f" (la vez pasada solo hiciste {len(reps)} de {sets})" if len(reps) < sets else ""
                meta = (f"Mantén {w}kg{per} en las {sets} series y busca {hi} reps en TODAS. "
                        f"La vez pasada ({date}): {ult}{falta}. Cuando pegues {hi} en las {sets}, subes a {round(w+inc,1)}kg.")
            tg[ex["name"]] = {"series": sets, "reps": f"{lo}–{hi}", "peso": peso,
                              "meta": meta, "ultima_vez": f"{ult} ({date})"}
        out["next_targets"][typ] = {"vs_fecha": date, "targets": tg}
    # estancamientos: compara últimas 2 sesiones del mismo tipo por lift (e1RM)
    by_type = {}
    for s in sorted(d["sessions"], key=lambda x: x["date"]):
        by_type.setdefault(s["type"], []).append(s)
    for typ, ss in by_type.items():
        if len(ss) < 2: continue
        prev, last = ss[-2], ss[-1]
        for ex in last["exercises"]:
            if ex.get("skipped"): continue
            pe = next((e for e in prev["exercises"] if e["name"] == ex["name"]), None)
            if not pe: continue
            be_last = max((e1rm(s.get("w"), s.get("r")) or 0) for s in ex.get("sets", []) or [{}])
            be_prev = max((e1rm(s.get("w"), s.get("r")) or 0) for s in pe.get("sets", []) or [{}])
            if be_prev and be_last and be_last <= be_prev:
                out["stalls"].append(f'{typ}/{ex["name"]}: sin subir ({be_prev}->{be_last} e1RM) — vigilar')
    return out

def _vol_state(n, mav):
    if not mav: return "?"
    if n < mav[0]: return f"bajo MEV (faltan {mav[0]-n})"
    if n > mav[1]: return "sobre MAV"
    return "ok"

# ---------------- #3 TRAJECTORY ----------------
def trajectory(d):
    out = {}
    bw = sorted(d.get("bodyweight", []), key=lambda x: x["date"])
    cut = d.get("cut", {})
    if len(bw) >= 2:
        d0 = datetime.date.fromisoformat(bw[0]["date"]); d1 = datetime.date.fromisoformat(bw[-1]["date"])
        days = (d1 - d0).days or 1
        rate_wk = (bw[-1]["kg"] - bw[0]["kg"]) / days * 7
        conf = "alta" if len(bw) >= 4 else "BAJA (pocos pesajes — usa el ritmo del plan)"
        used_rate = rate_wk if len(bw) >= 4 else -cut.get("rate_kg_wk", 0.55)
        target = cut.get("target_kg")
        if target and used_rate < 0:
            wks = (bw[-1]["kg"] - target) / (-used_rate)
            eta = d1 + datetime.timedelta(weeks=wks)
            out["peso"] = {"actual": bw[-1]["kg"], "meta": target, "ritmo_real_kg_sem": round(rate_wk,2),
                           "ritmo_usado": round(used_rate,2), "confianza": conf,
                           "semanas_faltan": round(wks,1), "ETA": eta.isoformat()}
        else:
            out["peso"] = {"actual": bw[-1]["kg"], "meta": target, "nota": "sin tendencia de pérdida aún"}
    else:
        out["peso"] = {"nota": "necesito >=2 pesajes — REGISTRA EL PESO (es el dato que mide el cut)"}
    # lifts: e1RM actual de los básicos (tendencia simple)
    lifts = {}
    for key in ["Bench Press", "Back Squat", "Romanian Deadlift", "Lat Pulldown"]:
        es = [(s["date"], max((e1rm(x.get("w"), x.get("r")) or 0) for x in ex.get("sets", [{}])))
              for s in sorted(d["sessions"], key=lambda x:x["date"])
              for ex in s["exercises"] if ex["name"] == key and not ex.get("skipped")]
        if es: lifts[key] = {"e1rm_actual": es[-1][1], "puntos": len(es),
                              "tendencia": "↑" if len(es)>1 and es[-1][1]>es[0][1] else "→"}
    out["lifts"] = lifts
    return out

# ---------------- #2 NEXT (qué sesión toca, POR VOLUMEN DE MÚSCULO no por slot de día) ----------------
# Qué músculos entrena de verdad cada TIPO (split v2). Evita el error de decidir por el
# nombre del día: los dorsales se entrenan en UPPER y en PULL, así que "no toca PULL"
# no se decide por el calendario sino por cuánto volumen le falta a cada músculo.
MUSCLE_BY_TYPE = {
    "UPPER": ["pecho","espalda","hombro","delt_lat","delt_post","biceps","triceps"],
    "PUSH":  ["pecho","hombro","delt_lat","triceps"],
    "PULL":  ["espalda","delt_post","biceps"],
    "LOWER": ["cuadriceps","femoral","gluteo","pantorrilla","core"],
    "LEGS":  ["cuadriceps","femoral","gluteo","pantorrilla","core"],
}

def _days_since_muscle(d, today):
    """Días desde la última vez que se entrenó cada músculo (cualquier tipo)."""
    last = {}
    for s in d["sessions"]:
        dt = datetime.date.fromisoformat(s["date"])
        for ex in s["exercises"]:
            if ex.get("skipped"): continue
            if not [x for x in ex.get("sets", []) if x.get("r")]: continue
            m = muscle_of(ex["name"])
            if m not in last or dt > last[m]: last[m] = dt
    return {m: (today - dt).days for m, dt in last.items()}

# Ventana de recuperación: <2 días (0–1) = la FUERZA del músculo aún está deprimida (recuperación
# de rendimiento / EIMD ~24–72h) -> no se vuelve a cargar duro (knowledge-base §4b, verif. 2026-07-01).
# NOTA: NO es por una "ventana de MPS" (esa base era errónea; la MPS aguda no predice hipertrofia,
# Damas 2016). La razón real: entrenar antes de recuperar la fuerza baja la calidad/volumen del estímulo.
REST_DAYS = 2
REST_PENALTY = 4.0   # castigo por cada músculo primario del tipo aún sin recuperar la fuerza

def _latest_recovery():
    """Recovery % más reciente, WHOOP-OPCIONAL. Orden de preferencia:
    1. readiness.json (auto-chequeo manual O un % de cualquier wearable) — funciona para todos.
    2. recovery.md (export tipo WHOOP: filas | fecha | pct% | ...).
    Devuelve (fecha, pct, fuente) o None."""
    # 1. manual / wearable
    if os.path.exists(READINESS_JSON):
        try:
            j = json.load(open(READINESS_JSON))
            if isinstance(j.get("recovery"), (int, float)):
                return (j.get("date", "manual"), float(j["recovery"]), "manual/wearable")
            sc = j.get("selfcheck")  # {"sleep":1-5,"energy":1-5,"soreness":1-5} (5 = mejor / sin dolor)
            if sc:
                vals = [sc.get("sleep"), sc.get("energy"), sc.get("soreness")]
                vals = [v for v in vals if isinstance(v, (int, float))]
                if vals:
                    pct = round(sum(vals) / (len(vals) * 5) * 100)
                    return (j.get("date", "auto-chequeo"), float(pct), "auto-chequeo")
        except (ValueError, KeyError):
            pass
    # 2. WHOOP-style export
    if os.path.exists(RECOVERY_MD):
        rows = []
        for ln in open(RECOVERY_MD):
            m = re.match(r"\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*([\d.]+)%", ln)
            if m: rows.append((m.group(1), float(m.group(2))))
        if rows:
            rows.sort()
            return (rows[-1][0], rows[-1][1], "WHOOP")
    return None

def readiness():
    """Autorregulación §10 según recovery más reciente (knowledge-base §10).
    OBLIGATORIO antes de prescribir: se computa y se hornea en la sesión, no se le puntea al usuario.
    Sin datos → pide un auto-chequeo de 3 preguntas (sueño/energía/dolor, 1–5)."""
    r = _latest_recovery()
    if not r:
        return {"recovery": None, "fecha": None, "zona": "sin dato", "fuente": None,
                "directiva": ("Sin dato de recovery. Auto-chequeo rápido (1–5 c/u, 5=mejor): "
                              "sueño · energía · SIN dolor muscular. Guárdalo en readiness.json "
                              '{"selfcheck":{"sleep":4,"energy":4,"soreness":3}}. '
                              "Mientras: entrena como está escrito, para a 2 RIR.")}
    fecha, pct, fuente = r
    if pct >= 67:
        z, dv = "🟢 verde", "EMPUJA: top sets 0–1 RIR, SUBE carga si pegaste el tope de reps, técnicas de intensidad OK."
    elif pct >= 34:
        z, dv = "🟡 amarillo", "COMO ESTÁ ESCRITO: para a 2 RIR, MANTÉN la carga (no fuerces subir peso hoy)."
    else:
        z, dv = "🔴 rojo", "LIGERO: corta ~40% de los sets, RIR 3–4, o puntos débiles / Zone 2 / descanso. No grindees el rojo."
    return {"recovery": pct, "fecha": fecha, "fuente": fuente, "zona": z, "directiva": dv}

def next_session(d):
    """Recomienda la próxima sesión, SCIENCE-BASED (knowledge-base §1 volumen, §4b recuperación de rendimiento).
    Elige el grupo MÁS ATRASADO (déficit vs MAV) que además esté RECUPERADO (≥48h, fuerza restaurada).
    - priority: déficit vs MEV/MAV (§1).
    - readiness: binario — músculo entrenado <48h NO cuenta y penaliza (§4b: fuerza aún deprimida → estímulo pobre).
    - sobre MAV = desincentiva (§1: pasar el techo = fatiga sin músculo).
    Ganar en déficit NO compensa entrenar sin recuperar: por eso el castigo es explícito, no un gradiente."""
    today = datetime.date.today()
    vol = compute(d)["volumen"]            # sets últimos 7 días por músculo (§1)
    sets_of = {m: vol.get(m, {}).get("sets", 0) for m in MAV}
    days = _days_since_muscle(d, today)    # días desde el último estímulo por músculo

    def priority(m):
        s = sets_of[m]; lo, hi = MAV[m]; mid = (lo + hi) / 2
        if s < lo:   return (lo - s) + 3          # bajo MEV = urgente
        if s <= hi:  return max(0.0, mid - s) * 0.5
        return -(s - hi)                          # sobre MAV = desincentivar

    def recovered(m):
        dz = days.get(m)
        return dz is None or dz >= REST_DAYS      # sin historial o ≥48h = recuperado

    ranked = []
    for typ, muscles in MUSCLE_BY_TYPE.items():
        addresses, conflicts = [], []
        score = 0.0
        for m in muscles:
            p = priority(m); rec_ok = recovered(m)
            # el déficit solo suma si el músculo está recuperado (un set no-recuperado no es estímulo, §1+§4b)
            score += p if (rec_ok or p < 0) else 0.0
            if not rec_ok:                         # castigo por forzar un músculo con la fuerza aún deprimida
                score -= REST_PENALTY
                conflicts.append(f"{m} entrenado hace {days[m]}d — fuerza sin recuperar (<48h, §4b)")
            elif p < 0:
                conflicts.append(f"{m} sobre MAV ({sets_of[m]} sets) — no meterle más (§1)")
            if p > 0 and rec_ok and sets_of[m] < MAV[m][0]:
                addresses.append(f"{m} ({sets_of[m]} sets, bajo MEV) — recuperado")
        ranked.append({"tipo": typ, "score": round(score, 1),
                       "ataca": addresses, "ojo": conflicts})
    ranked.sort(key=lambda x: -x["score"])
    rec = ranked[0]
    return {
        "recomendado": rec["tipo"],
        "readiness": readiness(),   # §10 horneado — obligatorio, no se le puntea al usuario
        "porque": f"grupo más atrasado Y recuperado (≥48h) — knowledge-base §1+§4b (score {rec['score']})",
        "ataca": rec["ataca"],
        "ojo": rec["ojo"],
        "ranking": ranked,
        "nota_calendario": "El día de la semana es solo un DEFAULT. La recomendación sale de "
                           "volumen real por músculo + recuperación de rendimiento 48h (ciencia citada, no ojo del agente).",
        "nota": "Siempre devuelve el mejor TIPO para tu próxima sesión. Si entrenas todos los días, "
                "el descanso de 48h por músculo se resuelve rotando el tipo (no con días libres). "
                "Si prefieres días de descanso, simplemente no entrenes ese día.",
    }

# ---------------- #4 RECONCILE ----------------
def reconcile(d):
    issues = []
    def read(f):
        p = os.path.join(DIR, f)
        return open(p).read() if os.path.exists(p) else ""
    log = read("log.md"); tracker = read("tracker.md"); block = read("block-state.md")
    block_start = d.get("block", {}).get("start", "0000-00-00")
    log_dates = set(re.findall(r"^##\s*(\d{4}-\d{2}-\d{2})", log, re.M))
    json_dates = {s["date"] for s in d["sessions"]}
    for dt in sorted(json_dates - log_dates):
        issues.append(f"[data.json sin log] sesión {dt} no tiene entrada ## en log.md")
    for dt in sorted(log_dates - json_dates):
        if dt >= block_start:  # ignora sesiones pre-bloque (baselines viejos)
            issues.append(f"[log sin data.json] {dt} está en log.md pero no en data.json")
    block = block.replace("×", "x")  # normaliza unicode antes de comparar PRs
    # last_by_type coherente con las sesiones reales
    for typ, dt in d.get("last_by_type", {}).items():
        real = max((s["date"] for s in d["sessions"] if s["type"] == typ), default=None)
        if real and real != dt:
            issues.append(f"[last_by_type] {typ} dice {dt} pero la última real es {real}")
    # PRs del block-state contra los computados
    prs = compute(d)["prs"]
    for lift in ["Back Squat", "Bench Press"]:
        if lift in prs and prs[lift]["set"] not in block and prs[lift]["fecha"] in json_dates:
            issues.append(f"[block-state] PR de {lift} ({prs[lift]['set']}) quizá desactualizado en block-state.md")
    # cobertura del bloque por TIPO (LOG MANDA — nunca por día de semana, Principio #0)
    types = [t for t in d.get("schedule", {}).values() if t != "rest"]
    coverage = {}
    for typ in types:
        dts = sorted(s["date"] for s in d["sessions"] if s["type"] == typ and s["date"] >= block_start)
        coverage[typ] = {"sesiones": len(dts), "ultima": (dts[-1] if dts else None)}
    sin_entrenar = [t for t, c in coverage.items() if c["sesiones"] == 0]
    return {"ok": not issues, "issues": issues,
            "block_coverage": coverage, "sin_entrenar_en_bloque": sin_entrenar}

# ---------------- CLI ----------------
def fmt(title, obj):
    print(f"\n=== {title} ===")
    print(json.dumps(obj, ensure_ascii=False, indent=2))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["compute", "next", "readiness", "trajectory", "reconcile", "all"])
    ap.add_argument("--json", action="store_true", help="salida JSON cruda")
    a = ap.parse_args()
    d = load()
    res = {}
    if a.cmd in ("compute", "all"): res["compute"] = compute(d)
    if a.cmd in ("readiness", "all"): res["readiness"] = readiness()
    if a.cmd in ("next", "all"): res["next"] = next_session(d)
    if a.cmd in ("trajectory", "all"): res["trajectory"] = trajectory(d)
    if a.cmd in ("reconcile", "all"): res["reconcile"] = reconcile(d)
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2)); return
    for k, v in res.items(): fmt(k.upper(), v)

if __name__ == "__main__":
    main()
