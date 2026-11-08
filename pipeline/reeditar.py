"""Reedita criativos JÁ PUBLICADOS: mantém o começo (gancho) intacto e troca o resto por um corpo novo
(voz grátis TTS turbo-free + banco de imagens + telas HTML), com música baixa e efeitos nas trocas.
NÃO gera nada pago no HeyGen.

Uso:
  python3 pipeline/reeditar.py pipeline/lotes/<plano>.json --vozes        # gera vozes (grátis) e mostra durações
  python3 pipeline/reeditar.py pipeline/lotes/<plano>.json [ids]          # monta (cabeça original + corpo novo)

Plano (JSON):
  origem:  pasta no bucket com os vídeos atuais  (ex.: 21-frases/lotes/2026-11-08-L2/21-frases-lote-2-{id}.mp4)
  banco:   "banco/indice.json"   (clipes 1080x1920 sem áudio; "b:<n>" = n-ésimo item do índice)
  campeoes + brolls: iguais ao roteiro.py ("c:<nome>")
  criativos[]: {id, corte (segundos: fim do gancho no vídeo atual), primary_text?, blocos[]}
  cauda?: segundos finais do vídeo atual (CTA com avatar já pago) emendados intactos no fim
     bloco: {"voz": "daniel", "partes": [["frase", "b:16"], ["frase", "c:pareja_flor"], ...], "destaques": [...]}
            -> cada frase ganha UMA imagem que entra no início dela (troca a cada 1,5–3 s)
         ou {"voz": "daniel", "texto": "...", "visual": {...tela HTML de formatos/cenas.py...}, "destaques": [...]}
            (visual pode ter "fundo": "b:12" para cta/stories/notícia/cctv)
Regras checadas: nenhum clipe repetido dentro do mesmo vídeo; trechos de clipe já usados em outro vídeo são evitados.
Saída: $FABRICA_WORK/<plano>/final/<id>.mp4  (+ revisao/<id>.jpg com quadros a cada 2 s)
"""
import json, os, re, subprocess, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "..", "formatos"))
import fabrica as F
import roteiro as R
from modelos import _limpa

SR = 44100


def ff(args):
    F.sh(["ffmpeg", "-v", "error", "-y"] + args)


# ------------------------------------------------------------------ banco de clipes
class Banco:
    def __init__(self, plano, base):
        self.plano, self.base = plano, base
        self.idx = json.load(open(F.storage_baixar(plano["banco"], os.path.join(F.WORK, "banco", "indice.json"))))
        self.uso_path = os.path.join(base, "uso_banco.json")
        self.uso = json.load(open(self.uso_path)) if os.path.exists(self.uso_path) else {}
        self.pasta = os.path.join(base, "clipes")
        os.makedirs(self.pasta, exist_ok=True)

    def fonte(self, chave):
        tipo, nome = chave.split(":", 1)
        if tipo == "b":
            arq = self.idx[int(nome)]["arquivo"]
            return F.storage_baixar(arq, os.path.join(F.WORK, arq)), None
        c, ini, fim, reg, *_ = self.plano["brolls"][nome]
        arq = self.plano["campeoes"][c]
        src = F.storage_baixar(f"{self.plano['produto']}/campeoes/{arq}",
                               os.path.join(F.WORK, "campeoes", self.plano["produto"], arq))
        return src, (ini, fim, R.REGIOES[reg])

    def pedaco(self, chave, dur, quem):
        """Corta `dur` s do clipe, evitando trechos já usados por outros vídeos."""
        src, corte = self.fonte(chave)
        if corte:
            ini0, fim0, crop = corte
        else:
            ini0, fim0, crop = 0.0, F.duracao(src), "null"
        total = fim0 - ini0
        usados = [u for u in self.uso.get(chave, []) if u[2] != quem]
        lento = 1.0
        if dur > total:
            lento = min(dur / total, 2.0)
        need = dur / lento
        melhor, pior = None, 1e9
        s = 0.0
        while s + need <= total + 1e-6:
            sob = sum(max(0, min(s + need, b) - max(s, a)) for a, b, _ in usados)
            if sob < pior - 1e-6:
                melhor, pior = s, sob
                if sob == 0:
                    break
            s += 0.25
        if melhor is None:
            melhor = 0.0
        self.uso.setdefault(chave, []).append([melhor, melhor + need, quem])
        json.dump(self.uso, open(self.uso_path, "w"))
        nome = re.sub(r"\W", "_", f"{chave}_{melhor:.2f}_{dur:.2f}")
        dst = os.path.join(self.pasta, nome + ".mp4")
        if not os.path.exists(dst):
            vf = (f"{crop},scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,"
                  f"setpts={lento:.3f}*PTS,fps=30,format=yuv420p")
            ff(["-ss", f"{ini0 + melhor:.3f}", "-t", f"{need + 0.1:.3f}", "-i", src, "-an", "-vf", vf,
                "-t", f"{dur:.3f}", "-c:v", "libx264", "-crf", "18", dst])
        return nome, dst, pior

    def limpar(self, quem):
        for k in list(self.uso):
            self.uso[k] = [u for u in self.uso[k] if u[2] != quem]
        json.dump(self.uso, open(self.uso_path, "w"))


# ------------------------------------------------------------------ tempos das frases
def tempos_partes(palavras, partes, dur):
    """Início (relativo à cena) de cada frase, pelo tempo da 1ª palavra dela."""
    n = [len(p[0].split()) for p in partes]
    ini, k = [], 0
    if sum(n) == len(palavras):
        for q in n:
            ini.append(max(0.0, palavras[k]["ini"] - 0.08) if k else 0.0)
            k += q
    else:  # contagem não bate: proporcional às letras
        tot = sum(len(p[0]) for p in partes)
        acc = 0
        for p in partes:
            ini.append(dur * acc / tot)
            acc += len(p[0])
    ini[0] = 0.0
    return ini


def mesclar(ini, partes, dur, minimo=1.05, maximo=3.3):
    """Junta frases curtas (< minimo s) com a vizinha mais curta, para a imagem não trocar rápido demais.
    A frase juntada fica com a imagem da primeira parte. Devolve [(ini, clipe, texto)]."""
    segs = [[ini[k], p[1], p[0], 0.0] for k, p in enumerate(partes)]
    def tam():
        for k, x in enumerate(segs):
            x[3] = (segs[k + 1][0] if k + 1 < len(segs) else dur) - x[0]
    tam()
    aceitos = set()  # curtos que não dá para juntar sem passar de `maximo`
    while len(segs) > 1:
        cand = [i for i in range(len(segs)) if segs[i][2] not in aceitos and segs[i][3] < minimo]
        if not cand:
            break
        k = min(cand, key=lambda i: segs[i][3])
        viz = [i for i in (k - 1, k + 1) if 0 <= i < len(segs)]
        j = min(viz, key=lambda i: segs[i][3])
        if segs[k][3] + segs[j][3] > maximo:
            aceitos.add(segs[k][2])
            continue
        a_, b_ = sorted((k, j))
        clip = segs[a_][1]  # a imagem entra no começo da frase que ela ilustra
        segs[a_] = [segs[a_][0], clip, segs[a_][2] + " " + segs[b_][2], 0.0]
        del segs[b_]
        tam()
    return [tuple(x[:3]) for x in segs]


def dur_cena(base, voz, texto, pausa=0.05):
    wav, r = R.tts_cache(base, voz, texto)
    fala = r["palavras"][-1]["fim"] + 0.2 if r["palavras"] else r["duracao"]
    return min(r["duracao"], fala) + pausa, r


# ------------------------------------------------------------------ áudio: música e efeitos
def musica_fundo(base, dur):
    """Trilha calma (sem direitos autorais): acordes suaves Am–F–C–G + pulso leve."""
    out = os.path.join(base, f"pad_{int(dur) + 1}.wav")
    if os.path.exists(out):
        return out
    acordes = [(220.0, 261.63, 329.63), (174.61, 220.0, 261.63), (130.81, 196.0, 261.63), (196.0, 246.94, 293.66)]
    seg = 3.2  # cada acorde
    termos = []
    for i, (a, b, c) in enumerate(acordes):
        jan = f"between(mod(t,{seg * 4}),{seg * i},{seg * (i + 1)})"
        termos.append(f"{jan}*(sin(2*PI*{a}*t)+0.8*sin(2*PI*{b}*t)+0.7*sin(2*PI*{c}*t)+0.5*sin(2*PI*{a / 2}*t))")
    corpo = "+".join(termos)
    pulso = "(0.55+0.45*exp(-mod(t,0.8)*5))"
    kick = "0.5*sin(2*PI*(45+60*exp(-mod(t,1.6)*30))*mod(t,1.6))*exp(-mod(t,1.6)*9)"
    expr = f"0.09*({corpo})*{pulso}+{kick}"
    ff(["-f", "lavfi", "-i", f"aevalsrc='{expr}':s={SR}:d={dur + 1:.2f}",
        "-af", f"lowpass=f=2500,aecho=0.8:0.7:180:0.25,afade=t=in:d=0.6,afade=t=out:st={max(0, dur - 1.2):.2f}:d=1.2",
        "-ac", "2", out])
    return out


def efeito(base, tipo):
    out = os.path.join(base, f"sfx_{tipo}.wav")
    if os.path.exists(out):
        return out
    if tipo == "whoosh":
        ff(["-f", "lavfi", "-i", f"anoisesrc=d=0.35:c=pink:r={SR}:a=0.6",
            "-af", "highpass=f=600,lowpass=f=5000,afade=t=in:d=0.12,afade=t=out:st=0.14:d=0.21,volume=0.9", "-ac", "2", out])
    else:  # pop (telas)
        ff(["-f", "lavfi", "-i", f"aevalsrc='0.8*sin(2*PI*(900-700*t/0.12)*t)*exp(-t*30)':s={SR}:d=0.15",
            "-ac", "2", out])
    return out


def mixar(video, saida, t_corte, trocas, base):
    """Voz (como está) + música baixa desde o corte (abaixa sob a voz) + efeitos discretos nas trocas -> -14 LUFS."""
    dur = F.duracao(video)
    mus = musica_fundo(base, dur - t_corte)
    wh, pop = efeito(base, "whoosh"), efeito(base, "pop")
    ins = ["-i", video, "-i", mus]
    filt = [f"[1:a]adelay={int(t_corte * 1000)}|{int(t_corte * 1000)},volume=0.22[m]",
            "[0:a]asplit=2[v][k]", "[m][k]sidechaincompress=threshold=0.03:ratio=4:attack=20:release=300[md]"]
    mix = ["[v]", "[md]"]
    for j, (t, tipo) in enumerate(trocas):
        ins += ["-i", wh if tipo == "whoosh" else pop]
        ms = int(max(0, t - (0.12 if tipo == "whoosh" else 0)) * 1000)
        filt.append(f"[{j + 2}:a]adelay={ms}|{ms},volume={0.16 if tipo == 'whoosh' else 0.22}[s{j}]")
        mix.append(f"[s{j}]")
    filt.append("".join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=first,"
                "loudnorm=I=-14:TP=-1.5:LRA=11[a]")
    ff(ins + ["-filter_complex", ";".join(filt), "-map", "0:v", "-map", "[a]", "-c:v", "copy",
              "-c:a", "aac", "-b:a", "160k", "-ar", str(SR), "-movflags", "+faststart", saida])
    return saida


# ------------------------------------------------------------------ montagem
def preparar_corpo(plano, cr, base, banco):
    """Gera vozes, corta clipes nos tempos das frases e devolve (cr no formato do roteiro.py, brolls, trocas)."""
    banco.limpar(cr["id"])
    vozes = plano["vozes"]
    cenas, brolls, trocas, t, usados = [], {}, [], 0.0, []
    for b in cr["blocos"]:
        voz = vozes[b.get("voz", cr.get("voz", "daniel"))]
        if "partes" in b:
            texto = " ".join(p[0] for p in b["partes"])
            dur, r = dur_cena(base, voz, texto, b.get("pausa", 0.05))
            segs = mesclar(tempos_partes(r["palavras"], b["partes"], dur), b["partes"], dur)
            nomes = []
            for k, (i0, clip, _) in enumerate(segs):
                fim = segs[k + 1][0] if k + 1 < len(segs) else dur
                if clip in usados:
                    raise ValueError(f"{cr['id']}: clipe {clip} repetido no mesmo vídeo")
                usados.append(clip)
                nome, dst, sob = banco.pedaco(clip, fim - i0, cr["id"])
                if sob > 0:
                    print(f"  aviso {cr['id']}: {clip} reaproveita {sob:.1f}s já usados em outro vídeo")
                brolls[nome] = (dst, fim - i0)
                nomes.append(nome)
                trocas.append((t + i0, "whoosh"))
            cenas.append({"voz": b.get("voz", cr.get("voz", "daniel")), "texto": texto, "pausa": b.get("pausa", 0.05),
                          "destaques": b.get("destaques", []), "leg_topo": b.get("leg_topo", 820),
                          "brolls": nomes, "visual": dict({"tipo": "broll", "modo": "cheio"}, **b.get("visual", {}))})
        else:
            dur, r = dur_cena(base, voz, b["texto"], b.get("pausa", 0.05))
            ce = {k: v for k, v in b.items() if k not in ("fundo",)}
            ce.setdefault("voz", cr.get("voz", "daniel"))
            v = dict(b["visual"])
            fundos = v.pop("fundo", None)
            if fundos:
                fundos = [fundos] if isinstance(fundos, str) else fundos
                fundos = [[f, None] if isinstance(f, str) else f for f in fundos]
                # início de cada fundo: na palavra indicada (ou dividido por igual)
                ini, k0 = [], 0
                for j, (fk, pal) in enumerate(fundos):
                    if j == 0:
                        ini.append(0.0)
                        continue
                    achou = None
                    if pal:
                        for q in range(k0, len(r["palavras"])):
                            if _limpa(r["palavras"][q]["txt"]).startswith(_limpa(pal)):
                                achou, k0 = max(0.0, r["palavras"][q]["ini"] - 0.08), q + 1
                                break
                    ini.append(achou if achou is not None else dur * j / len(fundos))
                ce["brolls"] = []
                for j, (fk, _) in enumerate(fundos):
                    if fk in usados:
                        raise ValueError(f"{cr['id']}: clipe {fk} repetido no mesmo vídeo")
                    usados.append(fk)
                    dj = (ini[j + 1] if j + 1 < len(ini) else dur) - ini[j]
                    nome, dst, sob = banco.pedaco(fk, dj, cr["id"])
                    brolls[nome] = (dst, dj)
                    ce["brolls"].append(nome)
                    if j:
                        trocas.append((t + ini[j], "whoosh"))
            ce["visual"] = v
            cenas.append(ce)
            trocas.append((t, "pop" if v["tipo"] in ("zap", "busca", "quiz", "bloqueio", "split", "cta", "texto") else "whoosh"))
        t += dur
    return {"id": cr["id"], "cenas": cenas}, brolls, trocas, t


def montar(plano, cr, base, banco):
    orig = os.path.join(base, "orig", f"{cr['id']}.mp4")
    F.storage_baixar(plano["origem"].format(id=cr["id"]), orig)
    rcr, brolls, trocas, dur = preparar_corpo(plano, cr, base, banco)
    corpo_plano = {"produto": plano["produto"], "vozes": plano["vozes"], "avatares": {}, "ctas": {}}
    corpo = R.montar_um(corpo_plano, rcr, os.path.join(base, "corpo"), brolls)  # hyperframes + -14 LUFS
    pasta = os.path.join(base, "partes", cr["id"])
    os.makedirs(pasta, exist_ok=True)
    cab = F.normalizar(orig, os.path.join(pasta, "cabeca.mp4"), 0, cr["corte"])
    t_corte = F.duracao(cab)
    cor = F.normalizar(corpo, os.path.join(pasta, "corpo.mp4"))
    lista = os.path.join(pasta, "lista.txt")
    open(lista, "w").write(f"file '{cab}'\nfile '{cor}'\n")
    t_cauda = None
    if cr.get("cauda"):  # fechamento original (CTA com avatar já pago) emendado no fim, intacto
        d_orig = F.duracao(orig)
        cau = F.normalizar(orig, os.path.join(pasta, "cauda.mp4"), d_orig - cr["cauda"], d_orig)
        t_cauda = t_corte + F.duracao(cor)
        open(lista, "a").write(f"file '{cau}'\n")
    junto = os.path.join(pasta, "junto.mp4")
    ff(["-f", "concat", "-safe", "0", "-i", lista, "-c", "copy", junto])
    os.makedirs(os.path.join(base, "final"), exist_ok=True)
    saida = os.path.join(base, "final", f"{cr['id']}.mp4")
    trocas = [(t_corte + a, k) for a, k in trocas] + ([(t_cauda, "whoosh")] if t_cauda else [])
    json.dump({"corte": t_corte, "trocas": trocas}, open(os.path.join(pasta, "tempos.json"), "w"))
    mixar(junto, saida, t_corte, trocas, base)
    folha(saida, os.path.join(base, "revisao", f"{cr['id']}.jpg"))
    return saida


def folha(video, saida):
    """Folha de quadros: 1 quadro a cada 2 s, com o tempo escrito."""
    os.makedirs(os.path.dirname(saida), exist_ok=True)
    n = int(F.duracao(video) // 2) + 1
    cols = 8
    ff(["-i", video, "-vf", "fps=0.5,scale=160:284,drawtext=text='%{pts\\:hms}':x=4:y=4:fontsize=18:"
        f"fontcolor=yellow:box=1:boxcolor=black,tile={cols}x{(n + cols - 1) // cols}", "-frames:v", "1", saida])


if __name__ == "__main__":
    caminho = sys.argv[1]
    nome = os.path.splitext(os.path.basename(caminho))[0]
    base = os.path.join(F.WORK, nome)
    os.makedirs(base, exist_ok=True)
    plano = json.load(open(caminho))
    ids = [a for a in sys.argv[2:] if not a.startswith("-")]
    if "--vozes" in sys.argv:
        for cr in plano["criativos"]:
            if ids and cr["id"] not in ids:
                continue
            tot, curtas = 0.0, []
            for b in cr["blocos"]:
                texto = b.get("texto") or " ".join(p[0] for p in b["partes"])
                d, r = dur_cena(base, plano["vozes"][b.get("voz", cr.get("voz", "daniel"))], texto)
                tot += d
                if "partes" in b:
                    sg = mesclar(tempos_partes(r["palavras"], b["partes"], d), b["partes"], d)
                    ii = [x[0] for x in sg] + [d]
                    curtas += [f"{ii[k + 1] - ii[k]:.1f}" for k in range(len(sg))]
            print(f"{cr['id']}: corpo {tot:.1f}s + gancho {cr['corte']:.1f}s = {tot + cr['corte']:.1f}s | trocas: {' '.join(curtas)}", flush=True)
        sys.exit()
    banco = Banco(plano, base)
    for cr in plano["criativos"]:
        if ids and cr["id"] not in ids:
            continue
        try:
            s = montar(plano, cr, base, banco)
            print(f"ok {cr['id']}: {F.duracao(s):.1f}s", flush=True)
        except Exception as e:
            print(f"ERRO {cr['id']}: {e}", flush=True)
