"""Ajudantes para escrever roteiros de lote em Python (gera o JSON que o lote_novo.py lê).

Linha de narração: ("frase com *destaque*", clipe)   clipe = n (item do banco) ou "c:nome" (corte de campeão)
P(linhas)           -> bloco de narração com uma imagem por frase (troca na 1ª palavra da frase)
V(texto, visual)    -> bloco com tela HTML (zap, busca, noticia, quiz, texto, split, bloqueio, viral, cta...)
"""
import re
from collections import Counter


def chave(c):
    return f"b:{c}" if isinstance(c, int) else c


def limpa(frase):
    dest = [w.lower().strip("¿¡,.:;…\"?!") for x in re.findall(r"\*([^*]+)\*", frase) for w in x.split()]
    return frase.replace("*", ""), dest


def P(linhas, **kw):
    partes, dest = [], []
    for frase, c in linhas:
        t, d = limpa(frase)
        partes.append([t, chave(c)])
        dest += d
    return dict({"partes": partes, "destaques": dest, "pausa": 0.2}, **kw)


def V(texto, visual, **kw):
    t, d = limpa(texto)
    v = dict(visual)
    if isinstance(v.get("fundo"), int):
        v["fundo"] = chave(v["fundo"])
    return dict({"texto": t, "visual": v, "destaques": d}, **kw)


def conferir(crs):
    """Erros: imagem repetida no mesmo vídeo. Mostra os clipes mais usados no lote."""
    uso = Counter()
    for c in crs:
        no_video = []
        for b in c["blocos"]:
            ks = [p[1] for p in b.get("partes", [])]
            f = b.get("visual", {}).get("fundo")
            ks += [f] if isinstance(f, str) else []
            for k in ks:
                if k in no_video:
                    raise ValueError(f"{c['id']}: {k} repetido no mesmo vídeo")
                no_video.append(k)
                uso[k] += 1
    print("mais usados:", " ".join(f"{k}x{n}" for k, n in uso.most_common(15)), "| distintos:", len(uso))
    return uso
