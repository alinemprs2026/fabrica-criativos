"""2 criativos adaptados de concorrentes (ES): voz clonada do Daniel em todas as falas + Avatar IV só no gancho (look lapela_preto).
Sobe tudo para criativos/21-frases/lotes/2026-11-16-ESC/ e grava indice.json."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fabrica as F
P = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lotes", "escalados_es.json"), encoding="utf-8"))
PREF = "21-frases/lotes/2026-11-16-ESC"; W = f"{F.WORK}/esc"; os.makedirs(W, exist_ok=True)
idx = {}
print("look aceita Avatar IV:", F.checar_avatar_iv(P["look"]), flush=True)
for cid, c in P["criativos"].items():
    for k, txt in enumerate([c["gancho"]] + c["falas"]):
        nome = f"{cid}-{k:02d}.wav"
        r = F.tts(txt, P["voz"], f"{W}/{nome}")
        F.storage_enviar(f"{W}/{nome}", f"{PREF}/{nome}", "audio/wav")
        idx[nome] = {"fala": txt, "duracao": r["duracao"], "palavras": r["palavras"], "audio_url": r["audio_url"]}
        print("voz", nome, round(r["duracao"], 1), flush=True)
    vid = F.avatar_iv(P["look"], idx[f"{cid}-00.wav"]["audio_url"], titulo=f"fabrica esc {cid}")
    arq, meta = F.esperar_video(vid, f"{W}/{cid}-gancho.mp4")
    F.storage_enviar(arq, f"{PREF}/{cid}-gancho.mp4", "video/mp4")
    print("avatar", cid, meta.get("duration"), flush=True)
json.dump(idx, open(f"{W}/indice.json", "w", encoding="utf-8"), ensure_ascii=False)
F.storage_enviar(f"{W}/indice.json", f"{PREF}/indice.json", "application/json")
print("PRONTO")
