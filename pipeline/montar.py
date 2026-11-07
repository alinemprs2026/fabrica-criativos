"""Monta os criativos do lote: gancho (HyperFrames ou corte de campeão) + corpo (cortes de campeões).

Uso:
  python3 pipeline/montar.py pipeline/lotes/<lote>.json            # todos
  python3 pipeline/montar.py pipeline/lotes/<lote>.json 01 10 11   # só alguns

Antes: rodar etapa_heygen.py (audios e avatar). Saída em $FABRICA_WORK/<lote>/final/<id>.mp4
"""
import json, os, shutil, subprocess, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "..", "formatos"))
import fabrica as F
import modelos as M

CROP_TOPO = 0.43  # parte de cima dos campeões em tela dividida (sem a legenda antiga)


def preparar(plano, nome):
    base = os.path.join(F.WORK, nome)
    camp = os.path.join(F.WORK, "campeoes", plano["produto"])
    os.makedirs(camp, exist_ok=True)
    for k, arq in plano["campeoes"].items():
        F.storage_baixar(f"{plano['produto']}/campeoes/{arq}", os.path.join(camp, arq))
    return base, camp


def corte(plano, camp, pasta, chave, c, ini, fim, mudo=False):
    out = os.path.join(pasta, f"{chave}.mp4")
    if not os.path.exists(out):
        F.normalizar(os.path.join(camp, plano["campeoes"][c]), out, ini, fim, mudo)
    return out


def fundo_cartao(plano, camp, pasta, c, ini, fim, minimo, topo=0.0):
    """Recorta a parte de cima da cena (sem legenda antiga) e garante duração mínima (repete se precisar)."""
    out = os.path.join(pasta, "fundo.mp4")
    src = os.path.join(camp, plano["campeoes"][c])
    F.sh(["ffmpeg", "-v", "error", "-y", "-i", src, "-ss", f"{ini}",
          "-t", f"{max(minimo, fim - ini):.2f}", "-an",
          "-vf", f"crop=iw:ih*{CROP_TOPO}:0:ih*{topo},scale=720:-2,fps=30,format=yuv420p",
          "-c:v", "libx264", "-crf", "18", out])
    return out


def render_hf(projeto, html_, saida):
    open(os.path.join(projeto, "index.html"), "w").write(html_)
    if not os.path.exists(os.path.join(projeto, "hyperframes.json")):
        shutil.copy(os.path.join(AQUI, "..", "formatos", "hyperframes.json"), projeto)
    r = subprocess.run(["npx", "-y", "hyperframes", "render", "--quality", "high", "--workers", "4",
                        "--output", saida], cwd=projeto, capture_output=True, text=True, timeout=1800)
    if r.returncode != 0 or not os.path.exists(saida):
        raise RuntimeError("HyperFrames falhou:\n" + (r.stdout + r.stderr)[-3000:])
    return saida


def gancho(plano, cr, base, camp, heygen):
    g = cr["gancho"]
    pasta = os.path.join(base, "ganchos", cr["id"])
    os.makedirs(pasta, exist_ok=True)
    final = os.path.join(pasta, "gancho_norm.mp4")
    if os.path.exists(final):
        return final
    if g["tipo"] == "campeao":
        c, a, b = g["corte"]
        return corte(plano, camp, pasta, "gancho_norm", c, a, b)
    voz = json.load(open(os.path.join(heygen, f"g{cr['id']}.json")))
    shutil.copy(os.path.join(heygen, f"g{cr['id']}.wav"), os.path.join(pasta, "voz.wav"))
    if g["tipo"] == "avatar":
        shutil.copy(os.path.join(heygen, f"g{cr['id']}.mp4"), os.path.join(pasta, "avatar.mp4"))
        dur, h = M.avatar(voz, g.get("destaques", []))
    elif g["tipo"] == "historico":
        fundo_cartao(plano, camp, pasta, *g["fundo"][:3], voz["duracao"] + 0.5, *g["fundo"][3:])
        dur, h = M.cartao(voz, g.get("destaques", []), selo="Egipto antiguo")
    elif g["tipo"] == "texto":
        fundo_cartao(plano, camp, pasta, *g["fundo"][:3], voz["duracao"] + 0.5, *g["fundo"][3:])
        dur, h = M.cartao(voz, g.get("destaques", []), grande=g["grande"])
    elif g["tipo"] == "whatsapp":
        corpo = plano["corpos"][cr["corpo"]]
        vc = None
        if corpo.get("novo") == "whatsapp":
            vc = json.load(open(os.path.join(heygen, "corpo_whatsapp.json")))
            shutil.copy(os.path.join(heygen, "corpo_whatsapp.wav"), os.path.join(pasta, "voz2.wav"))
        dur, h = M.whatsapp(g["cena"], voz, g.get("destaques", []), vc,
                            plano.get("whatsapp_corpo", {}).get("destaques", []))
    else:
        raise ValueError(g["tipo"])
    bruto = render_hf(pasta, h, os.path.join(pasta, "gancho_hf.mp4"))
    return F.normalizar(bruto, final)


def montar(plano, nome, ids=None):
    base, camp = preparar(plano, nome)
    heygen = os.path.join(base, "heygen")
    cortes = os.path.join(base, "cortes")
    os.makedirs(cortes, exist_ok=True)
    os.makedirs(os.path.join(base, "final"), exist_ok=True)
    for cr in plano["criativos"]:
        if ids and cr["id"] not in ids:
            continue
        try:
            partes = [gancho(plano, cr, base, camp, heygen)]
            for c, a, b in plano["corpos"][cr["corpo"]]["cortes"]:
                partes.append(corte(plano, camp, cortes, f"{c}_{a}_{b}", c, a, b))
            saida = os.path.join(base, "final", f"{cr['id']}.mp4")
            F.emendar(partes, saida)
            print(f"ok {cr['id']}: {F.duracao(saida):.1f}s")
        except Exception as e:
            print(f"ERRO {cr['id']}: {e}")


if __name__ == "__main__":
    caminho = sys.argv[1]
    nome = os.path.splitext(os.path.basename(caminho))[0]
    montar(json.load(open(caminho)), nome, sys.argv[2:] or None)
