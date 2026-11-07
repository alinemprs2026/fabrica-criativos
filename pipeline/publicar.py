"""Publica os criativos aprovados no painel (Supabase). NUNCA sobe nada no Facebook.

Uso:
  python3 pipeline/publicar.py pipeline/lotes/<lote>.json <batch_id> <AAAA-MM-DD> [--descartar 05,09]

- Envia <id>.mp4 e a miniatura para criativos/<produto>/lotes/<data>/
- Cria uma linha em `creatives` (status 'pendente') para cada vídeo
- Atualiza `notes` do lote com os minutos de HeyGen e muda para status 'pronto'
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fabrica as F


def main():
    caminho, batch_id, data = sys.argv[1:4]
    descartar = set()
    if "--descartar" in sys.argv:
        descartar = set(sys.argv[sys.argv.index("--descartar") + 1].split(","))
    plano = json.load(open(caminho))
    nome = os.path.splitext(os.path.basename(caminho))[0]
    base = os.path.join(F.WORK, nome)
    prod = plano["produto"]
    area = F.AREAS[prod]
    pasta = f"{prod}/lotes/{data}"

    st, ja = F.rest("GET", f"creatives?batch_id=eq.{batch_id}&select=storage_path")
    ja = {r["storage_path"] for r in (ja if st == 200 else [])}

    enviados = 0
    for cr in plano["criativos"]:
        if cr["id"] in descartar:
            continue
        v = os.path.join(base, "final", f"{cr['id']}.mp4")
        if not os.path.exists(v):
            print("faltando", cr["id"]); continue
        thumb = os.path.join(base, "final", f"{cr['id']}.jpg")
        F.sh(["ffmpeg", "-v", "error", "-y", "-ss", "0.6", "-i", v, "-frames:v", "1", "-q:v", "3", thumb])
        sp = f"{pasta}/{nome}-{cr['id']}.mp4"
        tp = f"{pasta}/{nome}-{cr['id']}.jpg"
        F.storage_enviar(v, sp, "video/mp4")
        F.storage_enviar(thumb, tp, "image/jpeg")
        if sp not in ja:
            corpo = plano["corpos"][cr["corpo"]]["nome"]
            st, d = F.rest("POST", "creatives", {
                "batch_id": batch_id, "workspace_id": area,
                "title": f"{plano['titulo']} · {cr['id']} · {cr['angulo']}",
                "format": cr["formato"], "angle": f"{cr['angulo']} (corpo: {corpo})",
                "hook": cr["gancho"]["texto"], "storage_path": sp, "thumb_path": tp,
                "duration_s": round(F.duracao(v), 1), "status": "pendente"})
            if st not in (200, 201):
                raise RuntimeError(f"creatives {cr['id']}: {st} {d}")
        enviados += 1
        print("publicado", cr["id"], sp)

    gasto = os.path.join(base, "heygen", "gasto.json")
    seg = json.load(open(gasto))["segundos"] if os.path.exists(gasto) else 0
    st, b = F.rest("GET", f"creative_batches?id=eq.{batch_id}&select=notes")
    notas = (b[0]["notes"] or "") if st == 200 and b else ""
    notas += (f"\n\nRESULTADO: {enviados} criativos publicados para revisão "
              f"({len(descartar)} descartados na revisão).\n"
              f"HeyGen usado: {seg:.0f} s = {seg/60:.2f} min de Avatar IV (teto semanal: 3 min). "
              f"Vozes: TTS gratuito (turbo-free) com voz clonada do campeão.")
    st, d = F.rest("PATCH", f"creative_batches?id=eq.{batch_id}", {"notes": notas, "status": "pronto"})
    print("lote pronto" if st in (200, 204) else f"erro ao fechar lote {st} {d}")


if __name__ == "__main__":
    main()
