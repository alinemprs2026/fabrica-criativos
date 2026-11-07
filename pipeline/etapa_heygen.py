"""Etapa HeyGen: vozes (grátis) e ganchos com Avatar IV (gasta crédito).

Uso:
  python3 pipeline/etapa_heygen.py audios    pipeline/lotes/<lote>.json
  python3 pipeline/etapa_heygen.py orcamento pipeline/lotes/<lote>.json   # lista o que será gerado e os minutos
  python3 pipeline/etapa_heygen.py avatar    pipeline/lotes/<lote>.json   # gera (respeita o teto de 3 min)

Tudo fica em $FABRICA_WORK/<lote>/heygen/ (reaproveita o que já existe, não paga duas vezes).
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import fabrica as F

TETO_MIN = 3.0  # minutos de Avatar IV por produto por semana sem pedir (CLAUDE.md)


def carregar(caminho):
    plano = json.load(open(caminho))
    nome = os.path.splitext(os.path.basename(caminho))[0]
    pasta = os.path.join(F.WORK, nome, "heygen")
    os.makedirs(pasta, exist_ok=True)
    return plano, pasta


def falas(plano):
    """Todas as falas novas do lote: (chave, texto, precisa_avatar, look)."""
    for c in plano["criativos"]:
        g = c["gancho"]
        if g["tipo"] in ("avatar", "whatsapp", "historico", "texto"):
            yield f"g{c['id']}", g["texto"], g["tipo"] == "avatar", g.get("look")
    if "whatsapp_corpo" in plano:
        yield "corpo_whatsapp", plano["whatsapp_corpo"]["texto"], False, None


def audios(plano, pasta):
    for chave, texto, _, _ in falas(plano):
        meta = os.path.join(pasta, chave + ".json")
        if os.path.exists(meta):
            continue
        r = F.tts(texto, plano["voz"], os.path.join(pasta, chave + ".wav"))
        r["texto"] = texto
        json.dump(r, open(meta, "w"), ensure_ascii=False, indent=1)
        print(f"voz ok {chave}: {r['duracao']:.1f}s")


def orcamento(plano, pasta):
    total, linhas = 0.0, []
    for chave, texto, av, look in falas(plano):
        if not av:
            continue
        d = json.load(open(os.path.join(pasta, chave + ".json")))["duracao"]
        ja = os.path.exists(os.path.join(pasta, chave + ".mp4"))
        total += 0 if ja else d
        linhas.append(f"{chave} [{look}] {d:.1f}s{' (já gerado)' if ja else ''}: {texto}")
    print("\n".join(linhas))
    print(f"TOTAL a gerar agora: {total:.1f}s = {total/60:.2f} min de Avatar IV (teto {TETO_MIN} min)")
    return total


def avatar(plano, pasta):
    gasto_previo = 0.0
    reg = os.path.join(pasta, "gasto.json")
    if os.path.exists(reg):
        gasto_previo = json.load(open(reg))["segundos"]
    total = orcamento(plano, pasta)
    if (gasto_previo + total) / 60 > TETO_MIN:
        print("PARADO: passaria do teto. Abra um pedido de permissão no painel antes.")
        sys.exit(2)
    for look_nome, look in plano["looks"].items():
        if not F.checar_avatar_iv(look):
            print(f"PARADO: o visual {look_nome} não aceita Avatar IV pela API.")
            sys.exit(3)
    pedidos = {}
    for chave, texto, av, look in falas(plano):
        if not av or os.path.exists(os.path.join(pasta, chave + ".mp4")):
            continue
        meta = json.load(open(os.path.join(pasta, chave + ".json")))
        vid = F.avatar_iv(plano["looks"][look], meta["audio_url"], titulo=f"fabrica {chave}")
        pedidos[chave] = (vid, meta["duracao"])
        print("pedido", chave, vid)
    for chave, (vid, d) in pedidos.items():
        F.esperar_video(vid, os.path.join(pasta, chave + ".mp4"))
        gasto_previo += d
        json.dump({"segundos": gasto_previo}, open(reg, "w"))
        print("pronto", chave)
    print(f"Avatar IV usado no lote: {gasto_previo:.1f}s = {gasto_previo/60:.2f} min")


if __name__ == "__main__":
    acao, caminho = sys.argv[1], sys.argv[2]
    plano, pasta = carregar(caminho)
    {"audios": audios, "orcamento": orcamento, "avatar": avatar}[acao](plano, pasta)
