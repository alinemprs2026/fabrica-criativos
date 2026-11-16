"""Narração por capítulos com voz natural (HeyGen turbo-free, grátis).
Uso: python3 pipeline/voz_capitulos.py <projeto> <pasta_textos> <idioma: italian|portuguese|...> <codigo: it|pt|...> [indice_voz]
Gera cada capítulo com a voz escolhida e, do 1º capítulo, uma amostra com a 2ª voz (para comparar).
Sobe para criativos/mr-quadrado/<projeto>/: NN_nome.wav + NN_nome.json (palavras com tempo) + vozes.json"""
import json, sys, os, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fabrica import http, HEYGEN, tts, storage_enviar
proj, pasta, lingua, cod = sys.argv[1:5]
iv = int(sys.argv[5]) if len(sys.argv) > 5 else 0
todas, vistos = [], set()
def junta(url):
    st, d = http("GET", url)
    lst = (d or {}).get("data", []) if isinstance(d, dict) else []
    if isinstance(lst, dict): lst = lst.get("voices", [])
    novos = 0
    for v in lst or []:
        if v.get("voice_id") not in vistos: vistos.add(v.get("voice_id")); todas.append(v); novos += 1
    return st, d, novos
for q in (f"language={lingua.capitalize()}&gender=male&limit=100", f"language={lingua}&limit=100", f"language={cod}&limit=100"):
    junta(f"{HEYGEN}/v3/voices?{q}")
st, d, _ = junta(f"{HEYGEN}/v3/voices?limit=100")
if isinstance(d, dict): print("chaves da resposta:", list(d.keys()), {k: v for k, v in d.items() if k != "data"})
from urllib.parse import quote
tok = d.get("next_token") if isinstance(d, dict) else None
param = None
for nome_p in ("token", "next_token", "page_token", "cursor"):
    if not tok: break
    st, d, n = junta(f"{HEYGEN}/v3/voices?limit=100&{nome_p}={quote(tok)}")
    print("paginação", nome_p, st, "novas:", n)
    if n: param = nome_p; break
while param and isinstance(d, dict) and d.get("has_more") and d.get("next_token"):
    st, d, n = junta(f"{HEYGEN}/v3/voices?limit=100&{param}={quote(d['next_token'])}")
    if not n: break
st2, d2 = http("GET", f"{HEYGEN}/v2/voices")
for v in ((d2 or {}).get("data", {}) or {}).get("voices", []) if isinstance(d2, dict) else []:
    if v.get("voice_id") not in vistos: vistos.add(v.get("voice_id")); todas.append(v)
print("vozes no total:", len(todas))
from collections import Counter
print("idiomas:", Counter(str(v.get("language")) for v in todas).most_common(40))
masc = lambda v: str(v.get("gender", "")).lower() == "male"
vozes = [v for v in todas if lingua in str(v.get("language", "")).lower() and masc(v)]
if not vozes:
    vozes = [v for v in todas if "multiling" in json.dumps(v).lower() and masc(v)]
    print("sem voz italiana masculina; usando multilíngue:", len(vozes))
for k, v in enumerate(vozes[:10]): print(k, v.get("voice_id"), v.get("name"), v.get("language"))
if not vozes: print("nenhuma voz utilizável"); sys.exit(1)
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
