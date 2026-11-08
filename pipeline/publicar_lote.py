"""Publica um lote no painel (Supabase), com primary_text e a tabela de variação no notes. NUNCA sobe no Facebook.

Uso:
  python3 pipeline/publicar_lote.py pipeline/lotes/<lote>.json <batch_id> <AAAA-MM-DD> [--descartar 05,09] [--heygen-extra-s 4.2]

- Envia <id>.mp4 e a miniatura para criativos/<produto>/lotes/<data>/
- Cria uma linha em `creatives` (status 'pendente') com format, angle, hook e primary_text (do corpo)
- Acrescenta no `notes`: tabela criativo → formato · corpo · gancho, descartes e minutos de HeyGen; status 'pronto'
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fabrica as F


def texto_gancho(plano, cr):
    g = cr["gancho"]
    if g.get("clipe"):
        return plano["clipes"][g["clipe"]]
    if g.get("texto"):
        return g["texto"]
    c = plano["corpos"][cr["corpo"]]
    return c.get("titulo") or c["texto"].split(".")[0]


def main():
    caminho, batch_id, data = sys.argv[1:4]
    arg = lambda n, p=None: sys.argv[sys.argv.index(n) + 1] if n in sys.argv else p
    descartar = set(filter(None, (arg("--descartar", "") or "").split(",")))
    extra = float(arg("--heygen-extra-s", 0) or 0)
    plano = json.load(open(caminho))
    nome = os.path.splitext(os.path.basename(caminho))[0]
    base = os.path.join(F.WORK, nome)
    prod = plano["produto"]
    pasta = f"{prod}/lotes/{data}"

    st, ja = F.rest("GET", f"creatives?batch_id=eq.{batch_id}&select=storage_path")
    ja = {r["storage_path"] for r in (ja if st == 200 else [])}

    linhas, enviados = [], 0
    for cr in plano["criativos"]:
        corpo = plano["corpos"][cr["corpo"]]
        v = os.path.join(base, "final", f"{cr['id']}.mp4")
        if cr["id"] in descartar or not os.path.exists(v):
            continue
        thumb = os.path.join(base, "final", f"{cr['id']}.jpg")
        F.sh(["ffmpeg", "-v", "error", "-y", "-ss", "0.6", "-i", v, "-frames:v", "1", "-q:v", "3", thumb])
        sp, tp = f"{pasta}/{nome}-{cr['id']}.mp4", f"{pasta}/{nome}-{cr['id']}.jpg"
        F.storage_enviar(v, sp, "video/mp4")
        F.storage_enviar(thumb, tp, "image/jpeg")
        gancho = texto_gancho(plano, cr)
        if sp not in ja:
            st, d = F.rest("POST", "creatives", {
                "batch_id": batch_id, "workspace_id": F.AREAS[prod],
                "title": f"{plano['titulo']} · {cr['id']} · {cr['angulo']}",
                "format": cr["formato"], "angle": f"{cr['angulo']} (corpo {cr['corpo']}: {corpo['nome']})",
                "hook": gancho, "primary_text": corpo.get("primary_text"),
                "storage_path": sp, "thumb_path": tp, "duration_s": round(F.duracao(v), 1), "status": "pendente"})
            if st not in (200, 201):
                raise RuntimeError(f"creatives {cr['id']}: {st} {d}")
        enviados += 1
        linhas.append(f"{cr['id']} → {cr['formato']} · corpo {cr['corpo']} · gancho: {gancho[:70]}")
        print("publicado", cr["id"], sp, flush=True)

    gasto = os.path.join(base, "heygen", "gasto.json")
    seg = (json.load(open(gasto))["segundos"] if os.path.exists(gasto) else 0) + extra
    st, b = F.rest("GET", f"creative_batches?id=eq.{batch_id}&select=notes")
    notas = (b[0]["notes"] or "") if st == 200 and b else ""
    notas += (f"\n\nRESULTADO: {enviados} criativos publicados para revisão"
              f"{' (descartados na revisão: ' + ', '.join(sorted(descartar)) + ')' if descartar else ''}.\n"
              "TABELA DE VARIAÇÃO (criativo → formato · corpo · gancho):\n" + "\n".join(linhas) +
              f"\n\nHeyGen: {seg:.0f} s = {seg/60:.2f} min de Avatar IV na semana (teto 3 min). "
              "Vozes dos corpos: TTS gratuito (turbo-free), na mesma voz do avatar de cada vídeo.")
    st, d = F.rest("PATCH", f"creative_batches?id=eq.{batch_id}", {"notes": notas, "status": "pronto"})
    print("lote pronto" if st in (200, 204) else f"erro ao fechar lote {st} {d}")


if __name__ == "__main__":
    main()
