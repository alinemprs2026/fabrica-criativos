"""Monta criativos INTEIROS por roteiro de cenas (formatos novos: notícia, CCTV, busca, quiz...).

Uso:
  python3 pipeline/roteiro.py pipeline/lotes/<lote>.json            # todos
  python3 pipeline/roteiro.py pipeline/lotes/<lote>.json 01 05      # só alguns
  python3 pipeline/roteiro.py pipeline/lotes/<lote>.json --vozes    # só gera as vozes (grátis) e mostra durações

O plano (JSON) tem:
  vozes:   {"daniel": "<voice_id>", ...}            (TTS turbo-free, grátis)
  avatares:{"04": {"arquivo": "av04.mp4", "transcricao": "tr04.json", "correcoes": {"Ysi": "¿Y si"}}}
           (clipes de Avatar IV JÁ PAGOS, em $FABRICA_WORK/<lote>/heygen/)
  brolls:  {"nome": ["c3", ini, fim, "topo"|"baixo"|"cheio"|"zoom"]}   (cenas cortadas dos campeões)
  ctas:    {"c7": ["c7", ini, fim]}                  (CTA de campeão emendado no fim, começando no início da frase)
  criativos[]: {id, formato, angulo, corpo, gancho, primary_text, cta, musica?, cenas[]}
     cena: {"voz": "daniel", "texto": "..."} | {"avatar": "04"} | {"dur": 3.0}
           + "visual": {"tipo": ..., ...}  (ver formatos/cenas.py)  + "brolls": [...]  + "destaques": [...]
Saída: $FABRICA_WORK/<lote>/final/<id>.mp4 (depois: revisar.py e publicar.py, iguais ao Lote 1).
"""
import hashlib, json, os, shutil, subprocess, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "..", "formatos"))
import fabrica as F
import cenas as C

REGIOES = {"topo": "crop=iw:ih*0.43:0:0", "baixo": "crop=iw:ih*0.45:0:ih*0.53",
           "cheio": "null", "alto": "crop=iw:ih*0.58:0:0", "zoom": "crop=iw*0.55:ih*0.40:iw*0.22:0"}


def base_de(caminho):
    nome = os.path.splitext(os.path.basename(caminho))[0]
    return nome, os.path.join(F.WORK, nome)


def preparar_brolls(plano, base):
    camp = os.path.join(F.WORK, "campeoes", plano["produto"])
    os.makedirs(camp, exist_ok=True)
    pasta = os.path.join(base, "brolls")
    os.makedirs(pasta, exist_ok=True)
    out = {}
    for nome, (c, ini, fim, reg, *lento) in plano["brolls"].items():
        arq = plano["campeoes"][c]
        src = F.storage_baixar(f"{plano['produto']}/campeoes/{arq}", os.path.join(camp, arq))
        dst = os.path.join(pasta, nome + ".mp4")
        if not os.path.exists(dst):
            F.sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{ini}", "-to", f"{fim}", "-i", src, "-an",
                  "-vf", f"{REGIOES[reg]},scale=720:-2,setpts={lento[0] if lento else 1}*PTS,fps=30,format=yuv420p", "-c:v", "libx264", "-crf", "18", dst])
        out[nome] = (dst, F.duracao(dst))
    return out


def tts_cache(base, voz_id, texto):
    pasta = os.path.join(base, "tts")
    os.makedirs(pasta, exist_ok=True)
    h = hashlib.sha1(f"{voz_id}|{texto}".encode()).hexdigest()[:12]
    meta = os.path.join(pasta, h + ".json")
    if not os.path.exists(meta):
        r = F.tts(texto, voz_id, os.path.join(pasta, h + ".wav"))
        r["texto"] = texto
        json.dump(r, open(meta, "w"), ensure_ascii=False)
    r = json.load(open(meta))
    return os.path.join(pasta, h + ".wav"), r


def palavras_avatar(av, pasta):
    d = json.load(open(os.path.join(pasta, av["transcricao"])))
    ws = d if isinstance(d, list) else d.get("words", [])
    cor = dict(av.get("correcoes", {}))
    out = []
    for w in ws:
        t = w["text"].strip().replace(",¿", ", ").replace("?¿", "? ").replace(".¿", ". ")
        if t in cor:
            t = cor.pop(t)
        out.append({"txt": t, "ini": w["start"], "fim": w["end"]})
    return out


def montar_um(plano, cr, base, brolls):
    proj = os.path.join(base, "proj", cr["id"])
    if os.path.exists(proj):
        shutil.rmtree(proj)
    os.makedirs(proj)
    heygen = os.path.join(base, "heygen")
    t, cenas = 0.0, []
    for k, ce in enumerate(cr["cenas"]):
        cena = {"t0": t, "visual": ce["visual"], "assets": {}, "palavras": [],
                "destaques": ce.get("destaques", []), "leg_topo": ce.get("leg_topo", 820)}
        if "texto" in ce:
            wav, r = tts_cache(base, plano["vozes"][ce["voz"]], ce["texto"])
            shutil.copy(wav, os.path.join(proj, f"voz{k}.wav"))
            cena["audio"] = f"voz{k}.wav"
            fala = r["palavras"][-1]["fim"] + 0.2 if r["palavras"] else r["duracao"]
            dur = min(r["duracao"], fala) + ce.get("pausa", 0.05)  # corta o silêncio do fim (ritmo)
            cena["palavras"] = [dict(w, ini=w["ini"] + t, fim=w["fim"] + t) for w in r["palavras"]]
        elif "avatar" in ce:
            av = plano["avatares"][ce["avatar"]]
            src = os.path.join(heygen, av["arquivo"])
            a, b = ce.get("de", 0.0), ce.get("ate", F.duracao(src))
            F.sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{a}", "-to", f"{b}", "-i", src,
                  "-vf", "scale=720:1280,fps=30,format=yuv420p", "-an", "-c:v", "libx264", "-crf", "18",
                  os.path.join(proj, f"av{k}.mp4")])
            F.sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{a}", "-to", f"{b}", "-i", src, "-vn",
                  "-ac", "2", "-ar", "44100", os.path.join(proj, f"voz{k}.wav")])
            cena["audio"] = f"voz{k}.wav"
            cena["assets"]["video"] = f"av{k}.mp4"
            dur = b - a
            cena["palavras"] = [dict(w, ini=w["ini"] - a + t, fim=w["fim"] - a + t)
                                for w in palavras_avatar(av, heygen) if a - 0.05 <= w["ini"] < b]
        else:
            dur = ce["dur"]
        cena["dur"] = dur
        lista = []
        for nb in ce.get("brolls", []):
            src, d = brolls[nb]
            shutil.copy(src, os.path.join(proj, nb + ".mp4"))
            lista.append((nb + ".mp4", d))
        if lista:
            cena["assets"]["brolls"] = lista
        cenas.append(cena)
        t += dur
    total = t + 0.1
    html_ = C.composicao(cenas, total)
    if cr.get("musica"):
        shutil.copy(os.path.join(base, cr["musica"]), os.path.join(proj, "musica.wav"))
        html_ = html_.replace('</div>\n<script>\nconst tl',
                              f'<audio id="mus" class="clip" src="musica.wav" data-start="0" data-duration="{total:.3f}" '
                              f'data-volume="{cr.get("musica_vol", 0.9)}"></audio>\n</div>\n<script>\nconst tl', 1)
    open(os.path.join(proj, "index.html"), "w").write(html_)
    shutil.copy(os.path.join(AQUI, "..", "formatos", "hyperframes.json"), proj)
    bruto = os.path.join(proj, "render.mp4")
    r = subprocess.run(["npx", "-y", "hyperframes", "render", "--quality", "high", "--workers", "4",
                        "--output", bruto], cwd=proj, capture_output=True, text=True, timeout=2400)
    if r.returncode != 0 or not os.path.exists(bruto):
        raise RuntimeError("HyperFrames falhou:\n" + (r.stdout + r.stderr)[-3000:])
    partes = [F.normalizar(bruto, os.path.join(proj, "norm.mp4"))]
    if cr.get("cta") in plano.get("ctas", {}):
        c, a, b = plano["ctas"][cr["cta"]]
        camp = os.path.join(F.WORK, "campeoes", plano["produto"], plano["campeoes"][c])
        partes.append(F.normalizar(camp, os.path.join(proj, "cta.mp4"), a, b))
    os.makedirs(os.path.join(base, "final"), exist_ok=True)
    saida = os.path.join(base, "final", f"{cr['id']}.mp4")
    F.emendar(partes, saida)
    return saida


def musica(base, nome="musica.wav", dur=24, bpm=120):
    """Batida simples sintetizada (sem direitos autorais): bumbo + chimbal + acorde."""
    out = os.path.join(base, nome)
    if os.path.exists(out):
        return out
    b = 60.0 / bpm
    expr = (f"0.9*sin(2*PI*(48+70*exp(-mod(t,{b})*28))*mod(t,{b}))*exp(-mod(t,{b})*7)"
            f"+0.18*(random(0)*2-1)*exp(-mod(t+{b/2},{b})*45)"
            f"+0.07*(sin(2*PI*220*t)+sin(2*PI*261.63*t)+sin(2*PI*329.63*t))*(0.6+0.4*sin(2*PI*t/{b*4}))"
            f"+0.12*sin(2*PI*55*t)*(mod(floor(t/{b*8}),2)*0.5+0.5)")
    F.sh(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"aevalsrc='{expr}':s=44100:d={dur}",
          "-af", "lowpass=f=9000,volume=0.8,afade=t=out:st=" + str(dur - 1.5) + ":d=1.5", "-ac", "2", out])
    return out


if __name__ == "__main__":
    caminho = sys.argv[1]
    nome, base = base_de(caminho)
    plano = json.load(open(caminho))
    os.makedirs(base, exist_ok=True)
    if "--vozes" in sys.argv:
        for cr in plano["criativos"]:
            tot = 0
            for ce in cr["cenas"]:
                if "texto" in ce:
                    _, r = tts_cache(base, plano["vozes"][ce["voz"]], ce["texto"])
                    tot += r["duracao"]
            print(cr["id"], f"{tot:.1f}s de voz")
        sys.exit()
    ids = [a for a in sys.argv[2:] if not a.startswith("-")]
    brolls = preparar_brolls(plano, base)
    musica(base)
    for cr in plano["criativos"]:
        if ids and cr["id"] not in ids:
            continue
        try:
            s = montar_um(plano, cr, base, brolls)
            print(f"ok {cr['id']}: {F.duracao(s):.1f}s", flush=True)
        except Exception as e:
            print(f"ERRO {cr['id']}: {e}", flush=True)
