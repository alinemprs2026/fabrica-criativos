"""Republica um lote REEDITADO por cima das linhas que já existem no painel (não cria lote novo).

Uso: python3 pipeline/republicar.py pipeline/lotes/<plano>.json <batch_id> <pasta-no-bucket> [--descartar 05]
 - envia final/<id>.mp4 para criativos/<pasta>/<id>.mp4
 - atualiza a linha de `creatives` do mesmo número (storage_path, duration_s, primary_text se o plano trouxer; status 'pendente')
 - acrescenta no `notes` do lote: data da reedição e a duração de cada vídeo. NUNCA sobe nada no Facebook.
"""
import datetime, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fabrica as F


def main():
    caminho, batch_id, pasta = sys.argv[1:4]
    descartar = set(sys.argv[sys.argv.index("--descartar") + 1].split(",")) if "--descartar" in sys.argv else set()
    plano = json.load(open(caminho))
    base = os.path.join(F.WORK, os.path.splitext(os.path.basename(caminho))[0])
    st, linhas = F.rest("GET", f"creatives?batch_id=eq.{batch_id}&select=id,title,storage_path")
    if st != 200:
        raise RuntimeError(f"creatives {st} {linhas}")
    duracoes = []
    for cr in plano["criativos"]:
        if cr["id"] in descartar:
            continue
        v = os.path.join(base, "final", f"{cr['id']}.mp4")
        alvo = [l for l in linhas if f" · {cr['id']} · " in l["title"]]
        if not os.path.exists(v) or len(alvo) != 1:
            print("pulado", cr["id"], "(sem vídeo ou linha)"); continue
        dur = round(F.duracao(v), 1)
        if dur < 60:
            print("pulado", cr["id"], f"({dur}s < 60s)"); continue
        sp = f"{pasta}/{cr['id']}.mp4"
        F.storage_enviar(v, sp, "video/mp4")
        mud = {"storage_path": sp, "duration_s": dur, "status": "pendente"}
        if cr.get("primary_text"):
            mud["primary_text"] = cr["primary_text"]
        st, d = F.rest("PATCH", f"creatives?id=eq.{alvo[0]['id']}", mud)
        if st not in (200, 204):
            raise RuntimeError(f"PATCH {cr['id']}: {st} {d}")
        duracoes.append(f"{cr['id']}: {dur:.0f}s")
        print("atualizado", cr["id"], sp, dur)
    st, b = F.rest("GET", f"creative_batches?id=eq.{batch_id}&select=notes")
    notas = (b[0]["notes"] or "") if st == 200 and b else ""
    hoje = datetime.date.today().strftime("%d/%m/%Y")
    notas += (f"\n\nReeditado em {hoje}: mínimo 1 min, sem HeyGen novo. "
              f"Começo (gancho) de cada vídeo mantido igual; corpo e final novos (dor → por quê → o que muda → objeção → CTA), "
              f"voz TTS grátis, imagens do banco sem repetir no mesmo vídeo, música baixa, -14 LUFS.\n"
              f"Durações: {' · '.join(duracoes)}")
    if plano.get("notas_fim"):
        notas += "\n" + plano["notas_fim"]
    st, d = F.rest("PATCH", f"creative_batches?id=eq.{batch_id}", {"notes": notas})
    print("notas ok" if st in (200, 204) else f"erro notas {st} {d}")


if __name__ == "__main__":
    main()
