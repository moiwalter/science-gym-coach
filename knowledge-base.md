---
title: "Training — Knowledge Base (evidencia)"
type: health/training
created: 2026-06-26
ref: workflow.md · training-plan.md
note: "La ciencia que los agentes (Science, Overload, Planner) DEBEN aplicar. No prescribir nada que contradiga esto sin razón explícita. TODAS las citas verificadas contra fuentes primarias (PubMed/DOI) el 2026-07-01 tras deep research de 4 agentes — ver correcciones inline marcadas."
---

# Training Knowledge Base — la ciencia que manda

> Esto existe para que el sistema **deje de divagar**. Cada decisión de volumen, carga, orden y descanso sale de acá, con su cita. Si una prescripción no encaja con esto, está mal.
>
> **Nivel de evidencia (tier):** cada decisión tiene un tier — **A** (meta/RCT sólido) · **B** (moderado/mixto) · **C** (heurístico/mecanicista/individual). El mapeo decisión→§→tier vive en **`agents/science-agent.md` (tabla Alcance)** — no se duplica acá (anti-drift). El agente declara el tier en cada fallo.

---

## 1. Volumen — el driver #1 de la hipertrofia

**Evidencia (verificada 2026-07-01):** Pelland et al. **2026** (*Sports Medicine* 56(2):481–505; online-first nov-2025; meta-regresión, 67 estudios, 2.058 sujetos): la hipertrofia **sube con el volumen** con **rendimientos decrecientes** (prob. posterior de pendiente >0 = 100% para hipertrofia Y fuerza; los rendimientos decrecientes son **mucho más pronunciados en fuerza** → la fuerza se aplana antes que el tamaño). No hay meseta clara de hipertrofia dentro del rango estudiado. Schoenfeld, Ogborn & Krieger 2017 confirma la dosis-respuesta **como variable continua** (+0.023 ES ≈ **+0.37% por set añadido**, P=0.002) — ⚠️ **ojo:** el corte categórico "10+ vs menos" de ese paper fue **no significativo (P=0.074)**, así que "10+ sets" NO es un umbral probado; el hallazgo firme es la dosis-respuesta continua (y midió solo hipertrofia, muestra mayormente no-entrenados).

**Regla operativa — sets DIRECTOS y duros por músculo por semana:**

| Zona | Sets/sem | Qué es |
|------|----------|--------|
| **MEV** (mínimo efectivo) | ~8–12 | piso para crecer |
| **MAV** (adaptación óptima) | **12–20** | tu rango de trabajo — **el único con respaldo peer-reviewed** (Baz-Valle 2022) |
| **MRV** (máximo recuperable) | ~20–28 | techo poblacional; pasarlo = fatiga sin más músculo |

- ⚠️ **Los landmarks MEV/MAV/MRV son heurísticas de Renaissance Periodization (Israetel), auto-publicadas, NO umbrales peer-reviewed.** Son promedios poblacionales, **individuales y por-músculo** — tu log los calibra. El **12–20 (MAV)** sí tiene respaldo revisado: Baz-Valle et al. 2022.
- **Evidencia nueva (2024–2026, Enes 2024; Pelland 2026):** para avanzados el techo útil puede estar **arriba de 20** (con rendimientos decrecientes y mucha variabilidad individual). O sea "20 = tope duro" está desactualizado; **12–20 sigue siendo el default práctico**, con espacio a subir por sobrecarga de volumen si la recuperación aguanta.
- Práctico: **arranca en 12–14, construye hacia 18–20+**, ajustando por tu log + recovery.
- Un set "cuenta" solo si es **duro** (ver §2). 4 sets blandos < 2 sets a 1–2 RIR.

## 2. Cercanía al fallo (RIR) — el "qué tan duro"

**Evidencia (verificada 2026-07-01):** Robinson et al. 2024 (*Sports Med* 54(9):2209–2231): para **hipertrofia**, la relación con el RIR es **continua y ~lineal — más crecimiento cuanto más cerca del fallo, SIN meseta identificada** (corrección: mi versión anterior decía "se aplana pasando 2 RIR" — eso es un heurístico popular, NO un hallazgo del paper). Para **fuerza**, el RIR tiene relación **despreciable** (el fallo NO se requiere; la fuerza es equivalente en un rango amplio de RIR — no "mejor a RIR alto"). Refalo et al. 2023 (*Sports Med* 53(3):649–665): la ventaja de acercarse al fallo para hipertrofia es **trivial (ES ~0.19, IC 0.00–0.37)** y **el fallo no es necesario**.

**Síntesis honesta:** entrena **cerca del fallo** (más cerca = un poco más de hipertrofia, de forma continua), pero **el fallo no es obligatorio** y el beneficio de las últimas reps es pequeño y cuesta fatiga. La cercanía al fallo importa más para hipertrofia que para fuerza.

**Regla operativa (heurística de manejo de fatiga, no un número de estudio):**
- **Compuestos** (sentadilla, press banca, peso muerto, dominadas): **1–3 RIR.** No al fallo — el costo de fatiga/articular no paga (la fuerza no lo necesita).
- **Aislamiento** (curls, laterales, extensiones, femoral, fly): **0–1 RIR**, último set se puede llevar al fallo. Bajo riesgo, buen estímulo.
- Traducción de RIR: "RIR 2" = podrías hacer 2 reps más con buena forma. Si podías hacer 5+, **no contó**.
- ⚠️ Error común: **dejar demasiado en reserva** (ej. 60×12 cuando el rango era 6–8). Como la hipertrofia escala con la cercanía al fallo (Robinson 2024), eso **cuesta crecimiento** — hay que acercarse más.

## 3. Sobrecarga progresiva — doble progresión (working sets, NO rampas)

- **Working sets:** 1 warm-up de aproximación → luego TODAS las series al peso de trabajo. ⚠️ Error común: **rampa** (40→60→80): infla el top set pero las series livianas de abajo no son estímulo. **Corregir siempre.**
- **Doble progresión:** llega al **tope de reps en TODAS las working sets** → +2.5kg la próxima → caes al piso del rango → vuelves a subir reps → repites.
- **Las reps son la moneda.** Sin reps anotadas no se sabe si superó. (Esto es lo que `log.md` + Overload Agent vigilan.)
- Si un ejercicio **no se mueve en 2–3 semanas** a esfuerzo real → revisar sueño/proteína primero, luego +1 set o cambiar el ejercicio.

## 4. Frecuencia — vehículo de volumen, no magia

**Evidencia (verificada 2026-07-01):** Schoenfeld, Grgic & Krieger **2019** (*J Sports Sci* 37(11):1286–1295, reanálisis a **volumen igualado**): **la frecuencia NO tiene efecto independiente significativo sobre la hipertrofia** — el volumen es el driver; la frecuencia solo **reparte** el volumen. Grgic et al. 2018 (*Sports Med* 48:1207–1220): igual para fuerza (leve ventaja solo en multiarticulares, por práctica motora). ⚠️ **No citar Schoenfeld 2016** ("2×>1×"): ese resultado estaba **confundido por más volumen** en el brazo de mayor frecuencia. Se entrena cada músculo **2×/semana** para repartir 14–20 sets con mejor calidad por sesión, no porque "2× sea mágico".

### 4b. Espaciar las sesiones duras del mismo músculo ~48 h — por RECUPERACIÓN DE RENDIMIENTO (no por "ventana de MPS")

> ⚠️ **Corrección 2026-07-01:** la versión anterior fundamentaba esto en una "ventana de MPS de 48 h" citando **Damas 2016 — mal.** Ese paper en realidad muestra que la **MPS aguda está confundida por el daño muscular al inicio del entrenamiento y NO predice la hipertrofia** → programar según la MPS aguda es un error. La regla de espaciar 48 h **sigue siendo válida, pero por otra razón.**

**Evidencia real:** la **capacidad de generar fuerza** está deprimida las ~**24–72 h** post-sesión dura (literatura de daño muscular inducido por ejercicio / recuperación de rendimiento; el rango escala con volumen, intensidad, énfasis excéntrico y estado de entrenamiento). Entrenar un músculo **antes de que su fuerza se recupere** degrada la carga/volumen y por tanto **la calidad del estímulo** de la siguiente sesión (contradice §1: un set solo cuenta si es duro) y acumula fatiga. Como la hipertrofia la maneja el **volumen semanal** y la frecuencia **no** aporta por sí sola a volumen igualado (§4), espaciar ~48 h **protege la calidad por sesión y gestiona la fatiga** — no "atrapa una ventana anabólica".

Sobre la MPS (contexto, no base de la regla): tras el ejercicio la MPS sube rápido (pico ~3–24 h) y sigue elevada ~24–48 h en **no entrenados** (Phillips 1997: +34% aún a las 48 h; MacDougall 1995: casi basal a las ~36 h). En **entrenados** la respuesta es **más corta y pequeña** (Damas 2015). Nada de esto es una base fiable para espaciar sesiones — la recuperación de rendimiento sí.

**Regla operativa (la DEBE aplicar `gym.py next`, no el ojo del agente):**
- Un músculo entrenado duro hace **≤48 h (0–1 día) NO se vuelve a cargar duro** — su fuerza aún no se recupera. Esto evita "pierna sobre pierna" o "empujar dos días seguidos".
- La próxima sesión se elige por el **grupo más atrasado (déficit vs MAV, §1) que además esté RECUPERADO (≥48 h)**. Déficit y recuperación se ponderan juntos; ganar en uno no compensa violar el otro.
- Excepción: un músculo con déficit severo que **comparte día** con músculos aún en recuperación (ej. glúteo bajo, pero pierna se entrenó ayer) → **espera al próximo día de esa región**, no fuerces el día completo. El déficit se corrige metiendo el ejercicio (ej. hip thrust) en la próxima sesión de la región, no adelantándola.

## 5. Orden de ejercicios — los puntos débiles PRIMERO

**Principio:** el rendimiento por ejercicio cae con la fatiga acumulada de la sesión → lo que va al final recibe el peor esfuerzo (o se salta).

**Patrón común:** el aislamiento del final se cae sistemáticamente — el ejercicio del final recibe el peor esfuerzo o se salta. Resultado: deltoide posterior, lateral y tríceps crónicamente sub-estimulados (los puntos débiles típicos).

**Reglas operativas (las aplica el Planner):**
1. **Lagging muscle primero**, cuando está fresco — o como **segundo ejercicio**, no de último.
2. **Supersets antagonistas/no-competitivos** para meter el volumen "chico" sí o sí: lateral raise con un press, rear-delt fly con un remo, tríceps con un jalón de espalda. Ahorra tiempo y garantiza que el aislamiento se haga.
3. Compuesto pesado primero **solo** cuando ese patrón es la prioridad del día (fuerza).

## 6. Selección de ejercicios

- **Prioriza estabilidad** en lo pesado (máquina/Smith/apoyado) para llevar más cerca del fallo sin que el limitante sea el equilibrio.
- **Énfasis en posición estirada:** el músculo crece más cargado en su rango largo (ej. incline curl, fly, RDL, overhead extension, seated leg curl). Buena evidencia emergente para parciales en estiramiento.
- **ROM completo** controlado como default; parciales en estiramiento como técnica extra, no reemplazo.
- 1–2 ejercicios por músculo por sesión bien elegidos > coleccionar variaciones.

## 7. Rango de reps, descanso, tempo

- **Reps:** hipertrofia similar en **~5–30 reps** si se llega cerca del fallo (Schoenfeld 2021). Práctico: **6–10** en compuestos (más carga, menos fatiga metabólica), **10–20** en aislamiento. Las pantorrillas y delts toleran y disfrutan reps altas.
- **Descanso:** **2–3 min en compuestos** (Schoenfeld 2016: descansos largos > cortos para hipertrofia — más volumen de calidad), **60–90 s en aislamiento**.
- **Tempo:** controla la **excéntrica (~2 s)**, sin pausa rara ni súper-lento (no hay ventaja del super-slow). Conecta y aprieta; nada de balanceo (ej. su hanging leg raise).

## 8. Deload — gestión de fatiga

- **Cuándo:** cada **4–8 semanas** o cuando se acumulan señales: caída de rendimiento 2 sesiones seguidas, sueño/HRV/recovery deprimidos, articulaciones quejándose, motivación al piso.
- **Cómo:** ~**50% de los sets**, carga ligeramente menor, RIR 3–4, una semana. No es obligatorio para todos, pero prudente si hay HRV bajo sostenido, enfermedad reciente o rendimiento cayendo.

## 9. Cut / retención de músculo en déficit  *(corregido 2026-07-01)*

- **Proteína en déficit: 2.3–3.1 g/kg de MASA MAGRA** (Helms et al. 2014 — es por **masa magra**, NO peso total). En personas secas magra ≈ total y convergen; con grasa que perder NO convergen → aplicar el número al peso total sobreestima. **Regla práctica si cargas grasa:** ~**1.8–2.4 g/kg de peso total**, o calcula sobre masa magra estimada.
- **Mantén el ESTÍMULO — volumen + esfuerzo, no perseguir 1RM.** Lo que protege el músculo en déficit es **mantener el volumen de entrenamiento (≥~10 sets/músculo/sem) y la carga**, no cazar PRs (Murphy & Koehler 2022; Roth 2023). "No bajes los pesos" es buen heurístico; el driver real en los datos es el volumen/estímulo retenido.
- **El volumen puede bajar levemente** si la recuperación cae — pero no lo recortes primero; recorta cardio extra o calorías antes.
- **Ritmo del déficit: 0.5–1% del peso corporal por semana** (~0.7% óptimo, Garthe 2011; Helms 2014). Más rápido = peaje muscular. (El marco en % es más correcto que un kg fijo.)

## 10. Autorregulación (RIR × WHOOP) — solo recovery de WHOOP

| Recovery WHOOP | Acción |
|----------------|--------|
| 🟢 **≥67%** | empuja, top sets 0–1 RIR, sube carga, técnicas de intensidad |
| 🟡 **34–66%** | como está escrito, para a 2 RIR, mantén carga |
| 🔴 **<34%** | corta ~40% de sets, RIR 3–4, o cámbialo por Zone 2 / puntos débiles. **No grindees el rojo.** |

> ⚠️ El wearable **solo** entra acá (recovery %). Para QUÉ/CUÁNDO entrenaste → **tu log manda** (ver `workflow.md` Principio #0).

## 11. Nutrición / sueño (inputs no negociables)

- **Proteína** para ganar músculo: punto de inflexión **1.62 g/kg de peso total** (Morton 2018; IC 95% 1.03–2.20, p=0.079 — borde). En **cut: 2.3–3.1 g/kg de masa magra** ≈ 1.8–2.4 g/kg total si cargas grasa (Helms 2014 — ver §9). ~30–40 g por comida, 3–4 comidas.
- **Sueño 7–9 h, hora fija.** Restringirlo destroza la recomposición: 4 h/noche → **MPS ~18% menor** (Saner 2020); en déficit, dormir 5.5 h vs 8.5 h → **55% menos grasa perdida y 60% más masa magra perdida** con la misma pérdida de peso (Nedeltcheva 2010). (El "7–9 h" es guía general de salud, no la variable que midieron esos estudios — pero la dirección está bien soportada.)
- **Creatina monohidrato 5 g/día** (tope del rango de mantenimiento ISSN), timing prácticamente irrelevante para saturar (Kreider et al. **2017**, no el stand de 2007).

---

## Reglas de decisión que ejecutan los agentes

**Overload Agent — al archivar una sesión, por ejercicio:**
1. ¿Llegó al tope de reps en TODAS las working sets a ese peso? → **sí: +2.5kg** la próxima. **no: repetir peso, +reps.**
2. ¿Reps muy por encima del rango (ej. 12 cuando era 6–8)? → carga muy liviana / demasiado RIR → **subir carga**, no celebrar reps.
3. ¿Hizo rampa? → marcar y recomendar **working sets**.
4. ¿Estancado 2–3 sem a esfuerzo real? → revisar sueño/proteína → +1 set o swap.

**Planner Agent — al armar la próxima sesión:**
> 🔧 **Config:** si entrenas todos los días, el descanso de 48h por músculo se resuelve **rotando el split** (el motor nunca repite un músculo <48h), no con días libres. Si prefieres días de descanso, simplemente no entrenes ese día.
1. Mira el `log.md` (no WHOOP): ¿qué se entrenó en las últimas ~48h? → **no repetir esos grupos** (rota a los recuperados).
2. Coloca los **puntos débiles primero o en superset** (rear-delt, lateral, tríceps).
3. Calibra volumen/RIR al **recovery WHOOP** (§10) — ajusta **carga**, nunca salta el día.
4. Si todo está reciente + 🔴 (raro) → versión **ligera / Zone 2 / puntos débiles**, pero **igual entrena** (nunca descanso en día de semana).
5. Apunta a que cada músculo caiga en su **MAV** (§1) a lo largo de la semana de 5 días.

---

## Referencias  *(verificadas contra fuentes primarias 2026-07-01)*

**Volumen**
- **Pelland et al. 2026** — *The Resistance Training Dose Response: Meta-Regressions on Weekly Volume and Frequency for Muscle Hypertrophy and Strength Gains.* **Sports Med 56(2):481–505** (online-first nov-2025). DOI 10.1007/s40279-025-02344-w. Volumen↑ = hipertrofia↑ y fuerza↑ con rendimientos decrecientes (más pronunciados en fuerza); frecuencia ≈ neutra para hipertrofia.
- **Schoenfeld, Ogborn, Krieger 2017** — volumen dosis-respuesta. *J Sports Sci 35(11):1073–1082.* DOI 10.1080/02640414.2016.1210197. Dosis-respuesta **continua** significativa (+~0.37%/set); el corte "10+ sets" fue NO significativo (P=0.074); solo hipertrofia, mayormente no-entrenados.
- **Baz-Valle et al. 2022** — *A Systematic Review of the Effects of Different Resistance Training Volumes on Muscle Hypertrophy.* J Hum Kinet 81:199–210. DOI 10.2478/hukin-2022-0017. **Respaldo peer-reviewed del 12–20 sets/músculo/sem.**
- **Enes et al. 2024** — progresión de volumen (hasta ~52 sets/sem) da ventaja pequeña sobre 22 fijos en entrenados. *J Appl Physiol.* DOI 10.1152/japplphysiol.00476.2024.
- **Israetel / Renaissance Periodization** — landmarks MEV/MAV/MRV: **heurísticas auto-publicadas, individuales y por-músculo, NO umbrales peer-reviewed.**

**Cercanía al fallo / reps / descanso**
- **Robinson et al. 2024** — proximity-to-failure dose-response. **Sports Med 54(9):2209–2231.** DOI 10.1007/s40279-024-02069-2. Hipertrofia **continua ~lineal** cerca del fallo (SIN meseta); fuerza ≈ independiente del RIR.
- **Refalo et al. 2023** — proximity-to-failure systematic review. **Sports Med 53(3):649–665.** DOI 10.1007/s40279-022-01784-y. Ventaja **trivial (ES ~0.19)**; fallo no requerido.
- **Schoenfeld et al. 2021** — *Repetition Continuum.* Sports 9(2):32. DOI 10.3390/sports9020032. Hipertrofia similar ~5–30 reps cerca del fallo. (Empírico de apoyo: Schoenfeld et al. 2017, JSCR 31(12):3508–3523.)
- **Schoenfeld et al. 2016 (descanso)** — *Longer Interset Rest…* JSCR 30(7):1805–1812. DOI 10.1519/JSC.0000000000001272. Descanso 3 min > 1 min (RCT único, n=21 — no sobre-generalizar).

**Frecuencia / recuperación**
- **Schoenfeld, Grgic & Krieger 2019** — frecuencia a **volumen igualado, sin efecto independiente** en hipertrofia. *J Sports Sci 37(11):1286–1295.* DOI 10.1080/02640414.2018.1555906. *(Reemplaza a Schoenfeld 2016, que estaba confundido por volumen.)*
- **Grgic et al. 2018** — frecuencia y fuerza (sin efecto a volumen igualado, salvo leve en multiarticulares). Sports Med 48(5):1207–1220. DOI 10.1007/s40279-018-0872-x.
- **Recuperación de rendimiento / EIMD** — la fuerza está deprimida ~24–72 h post-sesión dura; **base real** de espaciar sesiones del mismo músculo ~48 h (Schoenfeld, *Science and Development of Muscle Hypertrophy*, 2ª ed.).
- **MPS (contexto, NO base de la regla de espaciado):** Phillips et al. 1997 (*Am J Physiol* 273:E99–E107, DOI 10.1152/ajpendo.1997.273.1.E99) — MPS aún +34% a 48 h en no-entrenados. MacDougall et al. 1995 (*Can J Appl Physiol* 20(4):480–486, DOI 10.1139/h95-038) — casi basal a ~36 h, no-entrenados. Damas et al. 2015 (Sports Med 45:801–807, DOI 10.1007/s40279-015-0320-0) — respuesta más corta/pequeña en entrenados. **Damas et al. 2016** (*J Physiol* 594:5209–5222, DOI 10.1113/JP272472) — la MPS aguda está **confundida por daño y NO predice hipertrofia** al inicio; **NO usar como base para programar por "ventana de MPS".**

**Nutrición / sueño**
- **Morton et al. 2018** — proteína, punto de inflexión **1.62 g/kg peso total** (IC 1.03–2.20; p=0.079). *Br J Sports Med 52(6):376–384.* DOI 10.1136/bjsports-2017-097608.
- **Helms et al. 2014** — proteína **2.3–3.1 g/kg de masa MAGRA** en déficit; pérdida 0.5–1% peso/sem. *J Int Soc Sports Nutr 11:20.* DOI 10.1186/1550-2783-11-20.
- **Garthe et al. 2011** — ~0.7% peso/sem preserva masa magra vs 1.4%. IJSNEM 21(2):97–104. PMID 21896944.
- **Murphy & Koehler 2022** — retener volumen de entrenamiento preserva masa magra en déficit. Eur J Appl Physiol 122(5):1129–1144. DOI 10.1007/s00421-022-04896-5. (Y Roth et al. 2023, Scand J Med Sci Sports, DOI 10.1111/sms.14237.)
- **Saner et al. 2020** — restricción de sueño (4 h) → MPS miofibrilar ~18% menor. *J Physiol* 598(8):1523–1536. DOI 10.1113/JP278828.
- **Nedeltcheva et al. 2010** — dormir poco en dieta → 55% menos grasa perdida, 60% más masa magra perdida. *Ann Intern Med* 153(7):435–441. DOI 10.7326/0003-4819-153-7-201010050-00006.
- **Kreider et al. 2017** — ISSN position stand creatina (mantenimiento 3–5 g/día). *J Int Soc Sports Nutr 14:18.* DOI 10.1186/s12970-017-0173-z.
