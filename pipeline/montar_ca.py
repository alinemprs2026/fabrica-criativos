"""Monta o lote do Código Alfa: gancho + corpo narrado sobre cenas dos campeões + CTA.

Uso:
  python3 pipeline/montar_ca.py pipeline/lotes/codigo-alfa-lote-1.json            # todos
  python3 pipeline/montar_ca.py pipeline/lotes/codigo-alfa-lote-1.json 01 07      # só alguns

Antes: python3 pipeline/gerar_avatares.py <lote.json> (baixa/alinha os clipes Avatar IV).
Vozes dos corpos: TTS turbo-free (grátis) na MESMA voz do avatar do gancho/CTA.
Saída: $FABRICA_WORK/<lote>/final/<id>.mp4
"""
import json, os, shutil, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "..", "formatos"))
sys.path.insert(0, os.path.join(AQUI, "..", "formatos", "codigo-alfa"))
import fabrica as F
import modelos_ca as MC
from montar import render_hf

TOPO = 0.12      # recorte das cenas dos campeões: de 12% a 55% da altura (sem a legenda antiga)
ALTURA = 0.43
CENA_MAX = 2.6   # segundos por cena no corpo


def campeao(plano, k):
    return os.path.join(F.WORK, "campeoes", plano["produto"], plano["campeoes"][k])


def preparar(plano):
    for k, arq in plano["campeoes"].items():
        F.storage_baixar(f"{plano['produto']}/campeoes/{arq}", campeao(plano, k))


def voz_tts(plano, pasta, chave, texto, voz):
    meta = os.path.join(pasta, chave + ".json")
    if not os.path.exists(meta):
        r = F.tts(texto, plano["vozes"][voz], os.path.join(pasta, chave + ".wav"))
        r["texto"] = texto
        json.dump(r, open(meta, "w"), ensure_ascii=False, indent=1)
    return json.load(open(meta)), os.path.join(pasta, chave + ".wav")


def fundo(plano, cenas, minimo, saida):
    """Emenda cenas (recortadas) dos campeões até cobrir 'minimo' segundos."""
    if os.path.exists(saida) and F.duracao(saida) >= minimo - 0.05:
        return saida
    partes, total, i = [], 0.0, 0
    tmp = saida + "_p"
    os.makedirs(tmp, exist_ok=True)
    while total < minimo + 0.3:
        k, a, b = cenas[i % len(cenas)]
        d = min(CENA_MAX, b - a)
        p = os.path.join(tmp, f"{i:02d}.mp4")
        F.sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.2f}", "-t", f"{d:.2f}", "-i", campeao(plano, k), "-an",
              "-vf", f"crop=iw:ih*{ALTURA}:0:ih*{TOPO},scale=720:550,setsar=1,fps=30,format=yuv420p",
              "-c:v", "libx264", "-crf", "18", p])
        partes.append(p); total += d; i += 1
    lst = os.path.join(tmp, "l.txt")
    open(lst, "w").write("".join(f"file '{p}'\n" for p in partes))
    F.sh(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", saida])
    return saida


def render(pasta, html_, nome):
    os.makedirs(pasta, exist_ok=True)
    final = os.path.join(pasta, nome + "_norm.mp4")
    if not os.path.exists(final):
        bruto = render_hf(pasta, html_, os.path.join(pasta, nome + "_hf.mp4"))
        F.normalizar(bruto, final)
    return final


def parte_avatar(heygen, clipe, destaques, pasta, badge=False):
    os.makedirs(pasta, exist_ok=True)
    meta = json.load(open(os.path.join(heygen, clipe + ".json")))
    dur = min(meta["duracao"], meta["palavras"][-1]["fim"] + 0.25)  # corta logo após a última palavra
    shutil.copy(os.path.join(heygen, clipe + ".mp4"), os.path.join(pasta, "avatar.mp4"))
    F.sh(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(pasta, "avatar.mp4"), "-vn", "-ac", "2", "-ar", "44100",
          os.path.join(pasta, "voz.wav")])
    _, h = MC.apresentador(meta, destaques, dur, badge=badge)
    return render(pasta, h, "parte")


def montar(plano, nome, ids=None):
    preparar(plano)
    base = os.path.join(F.WORK, nome)
    heygen = os.path.join(base, "heygen")
    vozes = os.path.join(base, "vozes")
    os.makedirs(vozes, exist_ok=True)
    os.makedirs(os.path.join(base, "final"), exist_ok=True)
    for cr in plano["criativos"]:
        if ids and cr["id"] not in ids:
            continue
        try:
            pasta = os.path.join(base, "partes", cr["id"])
            g, corpo, cta = cr["gancho"], plano["corpos"][cr["corpo"]], cr["cta"]
            partes = []
            # ---------- gancho
            if g["tipo"] == "avatar":
                partes.append(parte_avatar(heygen, g["clipe"], g.get("destaques", []), os.path.join(pasta, "g")))
            elif g["tipo"] == "campeao":
                k, a, b = g["corte"]
                os.makedirs(pasta, exist_ok=True)
                out = os.path.join(pasta, "g_campeao.mp4")
                if not os.path.exists(out):
                    F.normalizar(campeao(plano, k), out, a, b)
                partes.append(out)
            elif g["tipo"] in ("texto", "historico"):
                pg = os.path.join(pasta, "g")
                os.makedirs(pg, exist_ok=True)
                v, wav = voz_tts(plano, vozes, f"g{cr['id']}", g["texto"], cr["voz"])
                shutil.copy(wav, os.path.join(pg, "voz.wav"))
                fundo(plano, [g["fundo"]], v["duracao"] + 0.5, os.path.join(pg, "fundo.mp4"))
                if g["tipo"] == "historico":
                    _, h = MC.narracao(v, g.get("destaques", []), selo=g.get("selo"))
                else:
                    _, h = MC.narracao(v, g.get("destaques", []), grande=g["grande"])
                partes.append(render(pg, h, "parte"))
            # ---------- corpo
            pc = os.path.join(pasta, "c")
            os.makedirs(pc, exist_ok=True)
            narrado = cta.get("texto_narrado")
            texto = corpo["texto"] + ((" " + plano["cta_texto"]) if narrado else "")
            v, wav = voz_tts(plano, vozes, f"{cr['corpo']}_{cr['voz']}{'_cta' if narrado else ''}", texto, cr["voz"])
            shutil.copy(wav, os.path.join(pc, "voz.wav"))
            badge = None
            if narrado or corpo.get("chat"):
                badge = next((w["ini"] for w in v["palavras"] if w["txt"].lower().strip("¿¡,.") in ("toca", "míralo")),
                             v["duracao"] - 3)
            if corpo.get("chat"):
                _, h = MC.chat(v, corpo["mensagens"], corpo.get("destaques", []), badge_desde=badge, titulo=corpo.get("titulo"))
            else:
                fundo(plano, plano["broll"][corpo["broll"]], v["duracao"] + 0.5, os.path.join(pc, "fundo.mp4"))
                _, h = MC.narracao(v, corpo.get("destaques", []), selo=corpo.get("selo"), badge_desde=badge)
            partes.append(render(pc, h, "parte"))
            # ---------- CTA com avatar
            if cta.get("clipe"):
                partes.append(parte_avatar(heygen, cta["clipe"], ["botón", "video", "quiten"],
                                           os.path.join(pasta, "cta"), badge=True))
            saida = os.path.join(base, "final", f"{cr['id']}.mp4")
            F.emendar(partes, saida)
            print(f"ok {cr['id']}: {F.duracao(saida):.1f}s", flush=True)
        except Exception as e:
            print(f"ERRO {cr['id']}: {e}", flush=True)


if __name__ == "__main__":
    caminho = sys.argv[1]
    nome = os.path.splitext(os.path.basename(caminho))[0]
    montar(json.load(open(caminho)), nome, sys.argv[2:] or None)
