"""Lote 3 (Flow): gera a voz clonada do Daniel (TTS turbo-free, grátis) para cada fala e envia ao bucket.
Uso (na nuvem): python3 pipeline/vozes_lote3.py
Saída: criativos/21-frases/lotes/2026-11-16-L3/vozes/<id>-<nn>.wav + indice.json (duração e tempo de cada palavra).
Retoma de onde parou: pula as falas que já estão no bucket.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fabrica import tts, storage_enviar, storage_list, storage_baixar, WORK

PLANO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lotes", "21-frases-lote-3-flow.json")
PREF = "21-frases/lotes/2026-11-16-L3/vozes"
plano = json.load(open(PLANO, encoding="utf-8"))
os.makedirs(f"{WORK}/l3", exist_ok=True)
ja = {o["name"] for o in storage_list(PREF + "/", 1000)}
indice = {}
if "indice.json" in ja:
    storage_baixar(f"{PREF}/indice.json", f"{WORK}/l3/indice.json")
    indice = json.load(open(f"{WORK}/l3/indice.json", encoding="utf-8"))
n = 0
for c in plano["criativos"]:
    for k, s in enumerate(c["cenas"]):
        nome = f"{c['id']}-{k:02d}.wav"
        if nome in ja and nome in indice:
            continue
        r = tts(s["fala"], plano["voz"], f"{WORK}/l3/{nome}")
        storage_enviar(f"{WORK}/l3/{nome}", f"{PREF}/{nome}", "audio/wav")
        indice[nome] = {"duracao": r["duracao"], "palavras": r["palavras"], "fala": s["fala"]}
        n += 1
        if n % 20 == 0:
            json.dump(indice, open(f"{WORK}/l3/indice.json", "w", encoding="utf-8"), ensure_ascii=False)
            storage_enviar(f"{WORK}/l3/indice.json", f"{PREF}/indice.json", "application/json")
            print(n, "vozes", flush=True)
json.dump(indice, open(f"{WORK}/l3/indice.json", "w", encoding="utf-8"), ensure_ascii=False)
storage_enviar(f"{WORK}/l3/indice.json", f"{PREF}/indice.json", "application/json")
tot = {}
for nome, v in indice.items():
    tot[nome[:2]] = tot.get(nome[:2], 0) + v["duracao"]
print("pronto:", len(indice), "vozes | duração por criativo (s):", {k: round(v) for k, v in sorted(tot.items())})
