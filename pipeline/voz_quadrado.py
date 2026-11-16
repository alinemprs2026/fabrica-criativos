"""Narração do Sr. Quadrado com voz natural (HeyGen turbo-free, grátis) em português do Brasil.
Lista as vozes masculinas em português, gera o texto em até 3 delas e sobe para o bucket:
  mr-quadrado/<projeto>/voz_<n>.wav  +  voz_<n>.json (palavras com tempo)  +  vozes.json (quais vozes)
Uso: python3 pipeline/voz_quadrado.py <projeto> <arquivo_texto>"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fabrica import http, HEYGEN, tts, storage_enviar

proj, arq = sys.argv[1], sys.argv[2]
texto = open(arq, encoding="utf-8").read().strip()
vozes = []
for ep in ("/v3/voices?language=Portuguese&gender=male&limit=100", "/v3/voices?limit=200", "/v2/voices"):
    st, d = http("GET", HEYGEN + ep)
    print("GET", ep, st, str(d)[:400])
    if st == 200 and isinstance(d, dict):
        dd = d.get("data", d)
        lst = dd.get("voices") if isinstance(dd, dict) else dd
        if isinstance(lst, list) and lst:
            vozes = lst; print("  exemplo:", json.dumps(lst[0])[:400]); break
pt = [v for v in vozes if "portug" in json.dumps(v).lower() and "female" not in str(v.get("gender", "")).lower()]
br = [v for v in pt if "bra" in json.dumps(v).lower()] or pt
print("vozes PT masculinas:", len(pt), "| BR:", len(br))
for v in br[:15]: print(" ", v.get("voice_id"), v.get("name"), v.get("language"), v.get("emotion_support"))
feitas = []
for v in br:
    if len(feitas) == 3: break
    try:
        r = tts(texto, v["voice_id"], f"/tmp/voz_{len(feitas)}.wav", idioma="pt", expressividade=0.6)
    except Exception as e:
        print("  falhou", v.get("name"), str(e)[:150]); continue
    n = len(feitas)
    storage_enviar(f"/tmp/voz_{n}.wav", f"mr-quadrado/{proj}/voz_{n}.wav", "audio/wav")
    json.dump(r["palavras"], open(f"/tmp/voz_{n}.json", "w"), ensure_ascii=False)
    storage_enviar(f"/tmp/voz_{n}.json", f"mr-quadrado/{proj}/voz_{n}.json", "application/json")
    feitas.append({"n": n, "voice_id": v["voice_id"], "nome": v.get("name"), "duracao": r["duracao"]})
    print("  ok", n, v.get("name"), r["duracao"])
json.dump(feitas, open("/tmp/vozes.json", "w"), ensure_ascii=False)
storage_enviar("/tmp/vozes.json", f"mr-quadrado/{proj}/vozes.json", "application/json")
print("PRONTO", len(feitas))
