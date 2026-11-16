"""Refaz as falas do lote 3 que têm o número 21, lendo "veintiuna" (frases), na voz clonada do Daniel.
Também gera falas extras listadas em lotes/l3_extras.json ({"nome.wav": "texto"}), se existir."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fabrica import tts, storage_enviar, storage_baixar, WORK
L = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lotes")
plano = json.load(open(f"{L}/21-frases-lote-3-flow.json", encoding="utf-8"))
PREF = "21-frases/lotes/2026-11-16-L3/vozes"
os.makedirs(f"{WORK}/l3", exist_ok=True)
storage_baixar(f"{PREF}/indice.json", f"{WORK}/l3/indice.json")
indice = json.load(open(f"{WORK}/l3/indice.json", encoding="utf-8"))
def fala21(s): return re.sub(r"\b21\b", "veintiuna", s)
tarefas = {}
for c in plano["criativos"]:
    for k, s in enumerate(c["cenas"]):
        if re.search(r"\b21\b", s["fala"]): tarefas[f"{c['id']}-{k:02d}.wav"] = fala21(s["fala"])
ex = f"{L}/l3_extras.json"
if os.path.exists(ex): tarefas.update(json.load(open(ex, encoding="utf-8")))
n = 0
for nome, texto in tarefas.items():
    if indice.get(nome, {}).get("fala") == texto: continue
    r = tts(texto, plano["voz"], f"{WORK}/l3/{nome}")
    storage_enviar(f"{WORK}/l3/{nome}", f"{PREF}/{nome}", "audio/wav")
    indice[nome] = {"duracao": r["duracao"], "palavras": r["palavras"], "fala": texto}; n += 1
    if n % 10 == 0:
        json.dump(indice, open(f"{WORK}/l3/indice.json", "w", encoding="utf-8"), ensure_ascii=False)
        storage_enviar(f"{WORK}/l3/indice.json", f"{PREF}/indice.json", "application/json"); print(n, flush=True)
json.dump(indice, open(f"{WORK}/l3/indice.json", "w", encoding="utf-8"), ensure_ascii=False)
storage_enviar(f"{WORK}/l3/indice.json", f"{PREF}/indice.json", "application/json")
print("PRONTO", n, "falas refeitas")
