"""Monta um LOTE NOVO sem HeyGen pago: começo (gancho) cortado de QUALQUER vídeo do bucket (campeão ou lote antigo
com Avatar IV já pago) ou nenhum + corpo novo (voz grátis TTS + banco de imagens + telas HTML) + fechamento opcional.
Usa o mesmo motor do reeditar.py (música baixa, efeitos nas trocas, -14 LUFS, folha de revisão).

Uso:
  python3 pipeline/lote_novo.py pipeline/lotes/<plano>.json --vozes     # vozes grátis + duração de cada vídeo
  python3 pipeline/lote_novo.py pipeline/lotes/<plano>.json [ids]       # monta

Plano: igual ao do reeditar.py, mas cada criativo tem
  cabeca: {"src": "<caminho no bucket>", "ini": s, "fim": s}   (opcional; sem cabeça o vídeo começa no 1º bloco)
  cauda:  {"src": "<caminho no bucket>", "ini": s, "fim": s}   (opcional; ex.: CTA com avatar já pago)
Saída: $FABRICA_WORK/<plano>/final/<id>.mp4 + revisao/<id>.jpg (1 quadro a cada 2 s).
"""
import json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import fabrica as F
import roteiro as R
import reeditar as RE


def _trecho(spec, pasta, nome):
    src = F.storage_baixar(spec["src"], os.path.join(F.WORK, "fontes", spec["src"]))
    ini, fim = spec.get("ini", 0.0), spec.get("fim")
    if spec.get("do_fim"):  # últimos N segundos (ex.: CTA com avatar no fim de um vídeo antigo)
        ini, fim = F.duracao(src) - spec["do_fim"], None
    return F.normalizar(src, os.path.join(pasta, nome + ".mp4"), ini, fim)


def montar(plano, cr, base, banco):
    rcr, brolls, trocas, dur = RE.preparar_corpo(plano, cr, base, banco)
    corpo_plano = {"produto": plano["produto"], "vozes": plano["vozes"], "avatares": {}, "ctas": {}}
    corpo = R.montar_um(corpo_plano, rcr, os.path.join(base, "corpo"), brolls)
    pasta = os.path.join(base, "partes", cr["id"])
    os.makedirs(pasta, exist_ok=True)
    partes, t_corte = [], 0.0
    if cr.get("cabeca"):
        cab = _trecho(cr["cabeca"], pasta, "cabeca")
        partes.append(cab)
        t_corte = F.duracao(cab)
    cor = F.normalizar(corpo, os.path.join(pasta, "corpo.mp4"), 0, dur - 0.1)
    partes.append(cor)
    t_cauda = None
    if cr.get("cauda"):
        t_cauda = t_corte + F.duracao(cor)
        partes.append(_trecho(cr["cauda"], pasta, "cauda"))
    lista = os.path.join(pasta, "lista.txt")
    open(lista, "w").write("".join(f"file '{p}'\n" for p in partes))
    junto = os.path.join(pasta, "junto.mp4")
    RE.ff(["-f", "concat", "-safe", "0", "-i", lista, "-c", "copy", junto])
    os.makedirs(os.path.join(base, "final"), exist_ok=True)
    saida = os.path.join(base, "final", f"{cr['id']}.mp4")
    trocas = [(t_corte + a, k) for a, k in trocas] + ([(t_cauda, "whoosh")] if t_cauda else [])
    if t_corte:
        trocas.insert(0, (t_corte, "whoosh"))
    json.dump({"corte": t_corte, "trocas": trocas}, open(os.path.join(pasta, "tempos.json"), "w"))
    RE.mixar(junto, saida, t_corte, trocas, base)
    RE.folha(saida, os.path.join(base, "revisao", f"{cr['id']}.jpg"))
    return saida


def tam_trecho(spec):
    if not spec:
        return 0.0
    return spec.get("do_fim") or ((spec["fim"] - spec.get("ini", 0.0)) if spec.get("fim") else 0.0)


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
                d, r = RE.dur_cena(base, plano["vozes"][b.get("voz", cr.get("voz", "daniel"))], texto)
                tot += d
                if "partes" in b:
                    sg = RE.mesclar(RE.tempos_partes(r["palavras"], b["partes"], d), b["partes"], d)
                    ii = [x[0] for x in sg] + [d]
                    curtas += [f"{ii[k + 1] - ii[k]:.1f}" for k in range(len(sg))]
            ext = tam_trecho(cr.get("cabeca")) + tam_trecho(cr.get("cauda"))
            print(f"{cr['id']}: total {tot + ext:.1f}s (corpo {tot:.1f}s) | trocas: {' '.join(curtas)}", flush=True)
        sys.exit()
    banco = RE.Banco(plano, base)
    for cr in plano["criativos"]:
        if ids and cr["id"] not in ids:
            continue
        try:
            s = montar(plano, cr, base, banco)
            print(f"ok {cr['id']}: {F.duracao(s):.1f}s", flush=True)
        except Exception as e:
            print(f"ERRO {cr['id']}: {e}", flush=True)
