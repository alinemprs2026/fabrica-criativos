"""Revisão dos criativos: folha de quadros (gancho em detalhe), volume, silêncios e transcrição do gancho.

Uso: python3 pipeline/revisar.py pipeline/lotes/<lote>.json [ids...]
Gera $FABRICA_WORK/<lote>/revisao/<id>.jpg e revisao.json (para olhar antes de publicar).
"""
import json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fabrica as F


def folha(video, saida):
    # 0–4s a cada 0,5s (gancho) + resto a cada ~6s
    F.sh(["ffmpeg", "-v", "error", "-y", "-i", video, "-vf",
          "select='lt(t,4)*not(mod(n,15))+gte(t,4)*not(mod(n,180))',scale=180:320,tile=8x3",
          "-vsync", "vfr", "-frames:v", "1", saida])


def volume(video):
    r = subprocess.run(["ffmpeg", "-i", video, "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", r)
    return float(m[-1]) if m else None


def silencios(video, minimo=0.7):
    r = subprocess.run(["ffmpeg", "-i", video, "-af", f"silencedetect=n=-40dB:d={minimo}",
                        "-f", "null", "-"], capture_output=True, text=True).stderr
    return [(float(a), float(b)) for a, b in
            re.findall(r"silence_start: ([\d.]+)[\s\S]*?silence_end: ([\d.]+)", r)]


def transcrever_inicio(video, pasta, segundos=6):
    os.makedirs(pasta, exist_ok=True)
    wav = os.path.join(pasta, "inicio.wav")
    F.sh(["ffmpeg", "-v", "error", "-y", "-t", str(segundos), "-i", video, "-ac", "1", "-ar", "16000", wav])
    subprocess.run(["npx", "-y", "hyperframes", "transcribe", wav, "--model", "small",
                    "--language", "es", "--json"], capture_output=True, text=True, timeout=600)
    t = os.path.join(pasta, "transcript.json")
    if not os.path.exists(t):
        return ""
    d = json.load(open(t))
    w = d if isinstance(d, list) else d.get("words", [])
    return " ".join(x.get("text", "") for x in w)


if __name__ == "__main__":
    caminho = sys.argv[1]
    nome = os.path.splitext(os.path.basename(caminho))[0]
    base = os.path.join(F.WORK, nome)
    rev = os.path.join(base, "revisao")
    os.makedirs(rev, exist_ok=True)
    plano = json.load(open(caminho))
    ids = sys.argv[2:] or [c["id"] for c in plano["criativos"]]
    out = {}
    for i in ids:
        v = os.path.join(base, "final", f"{i}.mp4")
        if not os.path.exists(v):
            continue
        folha(v, os.path.join(rev, f"{i}.jpg"))
        out[i] = {"duracao": round(F.duracao(v), 1), "lufs": volume(v),
                  "silencios": silencios(v),
                  "gancho_ouvido": transcrever_inicio(v, os.path.join(rev, f"tr_{i}"))}
        print(i, json.dumps(out[i], ensure_ascii=False))
    json.dump(out, open(os.path.join(rev, "revisao.json"), "w"), ensure_ascii=False, indent=1)
