"""Narração por capítulos com voz natural (HeyGen turbo-free, grátis).
Uso: python3 pipeline/voz_capitulos.py <projeto> <pasta_textos> <idioma: italian|portuguese|...> <codigo: it|pt|...> [indice_voz]
Gera cada capítulo com a voz escolhida e, do 1º capítulo, uma amostra com a 2ª voz (para comparar).
Sobe para criativos/mr-quadrado/<projeto>/: NN_nome.wav + NN_nome.json (palavras com tempo) + vozes.json"""
import json, sys, os, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fabrica import http, HEYGEN, tts, storage_enviar
proj, pasta, lingua, cod = sys.argv[1:5]
iv = int(sys.argv[5]) if len(sys.argv) > 5 else 0
st, d = http("GET", f"{HEYGEN}/v3/voices?language={lingua.capitalize()}&gender=male&limit=100")
vozes = [v for v in (d or {}).get("data", []) if lingua in str(v.get("language", "")).lower() and str(v.get("gender", "")).lower() == "male"]
for k, v in enumerate(vozes[:10]): print(k, v["voice_id"], v.get("name"))
if not vozes: print("sem vozes", st, str(d)[:300]); sys.exit(1)
voz = vozes[min(iv, len(vozes) - 1)]
arqs = sorted(glob.glob(os.path.join(pasta, "*.txt")))
feitos = []
for a in arqs:
    nome = os.path.splitext(os.path.basename(a))[0]
    r = tts(open(a, encoding="utf-8").read().strip(), voz["voice_id"], f"/tmp/{nome}.wav", idioma=cod, expressividade=0.6)
    storage_enviar(f"/tmp/{nome}.wav", f"mr-quadrado/{proj}/{nome}.wav", "audio/wav")
    json.dump(r["palavras"], open(f"/tmp/{nome}.json", "w"), ensure_ascii=False)
    storage_enviar(f"/tmp/{nome}.json", f"mr-quadrado/{proj}/{nome}.json", "application/json")
    feitos.append({"nome": nome, "duracao": r["duracao"]}); print("ok", nome, round(r["duracao"], 1))
if len(vozes) > 1:
    v2 = vozes[1 if iv == 0 else 0]
    r = tts(open(arqs[0], encoding="utf-8").read().strip(), v2["voice_id"], "/tmp/amostra.wav", idioma=cod, expressividade=0.6)
    storage_enviar("/tmp/amostra.wav", f"mr-quadrado/{proj}/amostra_outra_voz.wav", "audio/wav")
json.dump({"voz": voz, "outra": vozes[1 if iv == 0 else 0] if len(vozes) > 1 else None, "capitulos": feitos}, open("/tmp/vozes.json", "w"), ensure_ascii=False)
storage_enviar("/tmp/vozes.json", f"mr-quadrado/{proj}/vozes.json", "application/json")
print("PRONTO", len(feitos), "total s:", round(sum(f["duracao"] for f in feitos), 1))
