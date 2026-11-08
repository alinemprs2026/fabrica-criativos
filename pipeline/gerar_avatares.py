"""Clipes de Avatar IV do lote: BAIXA os que já foram pagos e só gera o que faltar (com teto).

Uso: python3 pipeline/gerar_avatares.py pipeline/lotes/<lote>.json [--gerar-faltantes LOOK_ID:VOZ_ID ...]

- Procura na conta do HeyGen vídeos com título "fabrica <clipe>.mp4" e baixa para $FABRICA_WORK/<lote>/heygen/.
- Transcreve cada clipe (HyperFrames/whisper) e alinha com o texto certo do JSON ("clipes"),
  gerando <clipe>.json com os tempos de cada palavra (para legendas e para cortar logo após a última palavra).
- Se algum clipe não existir, lista e para (não gera sem conferir o orçamento: teto 3 min/semana, CLAUDE.md).
"""
import difflib, json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fabrica as F


def listar_heygen(maximo=300):
    vids, token = [], None
    while len(vids) < maximo:
        url = f"{F.HEYGEN}/v3/videos?limit=50" + (f"&token={token}" if token else "")
        st, d = F.http("GET", url)
        if st != 200:
            raise RuntimeError(f"HeyGen lista {st}: {d}")
        vids += d.get("data", [])
        token = d.get("next_token")
        if not d.get("has_more") or not token:
            break
    return vids


def _norm(t):
    return re.sub(r"[^\wáéíóúñü]", "", t.lower())


def alinhar(texto_certo, palavras_whisper):
    """Usa os tempos do whisper e o texto certo (corrige palavras mal ouvidas)."""
    certo = texto_certo.split()
    ouv = [w for w in palavras_whisper if w["text"].strip()]
    sm = difflib.SequenceMatcher(a=[_norm(x) for x in certo], b=[_norm(w["text"]) for w in ouv], autojunk=False)
    tempos = [None] * len(certo)
    for a, b, n in sm.get_matching_blocks():
        for i in range(n):
            tempos[a + i] = (ouv[b + i]["start"], ouv[b + i]["end"])
    ini0 = ouv[0]["start"] if ouv else 0.0
    fim0 = ouv[-1]["end"] if ouv else 1.0
    # interpola os que não casaram
    for i in range(len(certo)):
        if tempos[i] is None:
            prev = next((tempos[j][1] for j in range(i - 1, -1, -1) if tempos[j]), ini0)
            k = next((j for j in range(i + 1, len(certo)) if tempos[j]), None)
            nxt = tempos[k][0] if k is not None else fim0
            falt = (k if k is not None else len(certo)) - i
            passo = max(0.05, (nxt - prev) / (falt + 0))
            tempos[i] = (prev, prev + passo)
    return [{"txt": w, "ini": a, "fim": b} for w, (a, b) in zip(certo, tempos)], fim0


def transcrever(arquivo, pasta):
    os.makedirs(pasta, exist_ok=True)
    if os.path.exists(os.path.join(pasta, "transcript.json")):
        return json.load(open(os.path.join(pasta, "transcript.json")))
    wav = os.path.join(pasta, "a.wav")
    F.sh(["ffmpeg", "-v", "error", "-y", "-i", arquivo, "-ac", "1", "-ar", "16000", wav])
    subprocess.run(["npx", "-y", "hyperframes", "transcribe", "a.wav", "--model", "small",
                    "--language", "es", "--json"], cwd=pasta, capture_output=True, text=True, timeout=900)
    return json.load(open(os.path.join(pasta, "transcript.json")))


def main():
    caminho = sys.argv[1]
    plano = json.load(open(caminho))
    nome = os.path.splitext(os.path.basename(caminho))[0]
    pasta = os.path.join(F.WORK, nome, "heygen")
    os.makedirs(pasta, exist_ok=True)
    usados = {}
    for cr in plano["criativos"]:
        if cr["gancho"].get("clipe"):
            usados[cr["gancho"]["clipe"]] = plano["clipes"][cr["gancho"]["clipe"]]
        if cr["cta"].get("clipe"):
            usados[cr["cta"]["clipe"]] = plano["clipes"][cr["cta"]["texto"]]
    conta = {v.get("title", ""): v for v in listar_heygen()}
    faltam, seg = [], 0.0
    for clipe, texto in usados.items():
        mp4 = os.path.join(pasta, clipe + ".mp4")
        v = conta.get(f"fabrica {clipe}.mp4")
        if v and v.get("status") == "completed":
            seg += v.get("duration") or 0
        if not os.path.exists(mp4):
            if not v:
                faltam.append(clipe); continue
            st, d = F.http("GET", f"{F.HEYGEN}/v3/videos/{v['id']}")
            F.baixar(d["data"]["video_url"], mp4)
            print("baixado", clipe)
        meta = os.path.join(pasta, clipe + ".json")
        if not os.path.exists(meta):
            w = transcrever(mp4, os.path.join(pasta, "tr_" + clipe))
            palavras, fim = alinhar(texto, w)
            json.dump({"texto": texto, "palavras": palavras, "fim_fala": fim, "duracao": F.duracao(mp4)},
                      open(meta, "w"), ensure_ascii=False, indent=1)
            print("transcrito", clipe, round(fim, 2))
    json.dump({"segundos": seg, "obs": "clipes Avatar IV já pagos que este lote usa"},
              open(os.path.join(pasta, "gasto.json"), "w"))
    print(f"Avatar IV deste lote: {seg:.1f}s = {seg/60:.2f} min")
    if faltam:
        print("FALTAM (não existem na conta):", ", ".join(faltam))
        print("Antes de gerar, confira o teto de 3 min/semana (CLAUDE.md).")
        sys.exit(2)


if __name__ == "__main__":
    main()
