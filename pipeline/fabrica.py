"""Funções comuns da fábrica de criativos (Supabase, HeyGen, ffmpeg).

Na nuvem as chaves NÃO ficam no ambiente: o proxy injeta os cabeçalhos de
autenticação em api.heygen.com e *.supabase.co. Por isso nenhuma função aqui
manda cabeçalho de chave. Só SUPABASE_URL vem do ambiente.

Só usa a biblioteca padrão do Python (roda em qualquer python3).
"""
import json, os, subprocess, time, urllib.request, urllib.error

SUPABASE_URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
HEYGEN = "https://api.heygen.com"
BUCKET = "criativos"

AREAS = {
    "21-frases": "2171e39a-2760-4d8e-868e-060cbdf0f8c1",
    "codigo-alfa": "57fbb528-40ce-47ef-8cc3-9c0be86b4ec5",
}

# Pasta de trabalho (vídeos, áudios, renders). Nunca vai para o git.
WORK = os.environ.get("FABRICA_WORK", "/tmp/fabrica")


# ---------------------------------------------------------------- HTTP
def http(method, url, body=None, headers=None, raw=False, timeout=300):
    h = dict(headers or {})
    data = None
    if body is not None:
        if isinstance(body, (bytes, bytearray)):
            data = body
        else:
            data = json.dumps(body).encode()
            h.setdefault("Content-Type", "application/json")
    req = urllib.request.Request(url, data=data, method=method, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            out = r.read()
            return r.status, (out if raw else (json.loads(out) if out else None))
    except urllib.error.HTTPError as e:
        out = e.read()
        try:
            return e.code, json.loads(out)
        except Exception:
            return e.code, out[:500]


def baixar(url, destino):
    os.makedirs(os.path.dirname(destino) or ".", exist_ok=True)
    st, data = http("GET", url, raw=True, timeout=600)
    if st != 200:
        raise RuntimeError(f"download {st}: {url[:120]}")
    open(destino, "wb").write(data)
    return destino


# ---------------------------------------------------------------- Supabase
def rest(method, tabela_query, body=None):
    h = {"Prefer": "return=representation"}
    return http(method, f"{SUPABASE_URL}/rest/v1/{tabela_query}", body, h)


def storage_list(prefixo, limite=200):
    st, d = http("POST", f"{SUPABASE_URL}/storage/v1/object/list/{BUCKET}",
                 {"prefix": prefixo, "limit": limite})
    return d if st == 200 else []


def storage_baixar(caminho, destino):
    if os.path.exists(destino) and os.path.getsize(destino) > 0:
        return destino
    return baixar(f"{SUPABASE_URL}/storage/v1/object/{BUCKET}/{caminho}", destino)


def storage_enviar(arquivo, caminho, tipo):
    dados = open(arquivo, "rb").read()
    url = f"{SUPABASE_URL}/storage/v1/object/{BUCKET}/{caminho}"
    st, d = http("POST", url, dados, {"Content-Type": tipo, "x-upsert": "true"}, timeout=900)
    if st not in (200, 201):
        st, d = http("PUT", url, dados, {"Content-Type": tipo}, timeout=900)
    if st not in (200, 201):
        raise RuntimeError(f"upload {caminho}: {st} {d}")
    return caminho


def avisar_aline(produto, titulo, corpo, kind="mensagem", payload=None):
    """Abre um aviso/pedido no painel (aba Criativos)."""
    st, d = rest("POST", "factory_requests", {
        "workspace_id": AREAS[produto], "kind": kind, "title": titulo,
        "body": corpo, "payload": payload})
    return st, d


# ---------------------------------------------------------------- HeyGen
def tts(texto, voice_id, destino_wav, idioma="es", expressividade=0.5):
    """Voz (gratuita até 30/11/2026 no modelo turbo-free) com tempo de cada letra."""
    corpo = {"model": "heygen-voice-1-turbo-free", "voice_id": voice_id, "text": texto,
             "language": idioma, "expressiveness_boost": expressividade, "with_timestamps": True}
    for tentativa in range(6):
        st, d = http("POST", f"{HEYGEN}/v3/models/audio/tts", corpo)
        if st == 200:
            break
        if st in (429, 500, 502, 503):
            time.sleep(5 * (tentativa + 1))
            continue
        raise RuntimeError(f"TTS {st}: {d}")
    else:
        raise RuntimeError(f"TTS sem resposta: {d}")
    d = d["data"]
    baixar(d["audio_url"], destino_wav)
    return {"audio_url": d["audio_url"], "duracao": d["duration"],
            "palavras": palavras_de_caracteres(d.get("original_characters", []))}


def palavras_de_caracteres(chars):
    palavras, atual = [], None
    for c in chars:
        if c["text"].isspace():
            if atual:
                palavras.append(atual)
            atual = None
            continue
        if atual is None:
            atual = {"txt": "", "ini": c["start_time"], "fim": c["end_time"]}
        atual["txt"] += c["text"]
        atual["fim"] = c["end_time"]
    if atual:
        palavras.append(atual)
    return palavras


def checar_avatar_iv(look_id):
    """True se o visual aceita o motor Avatar IV pela API."""
    st, d = http("GET", f"{HEYGEN}/v3/avatars/looks/{look_id}")
    return st == 200 and "avatar_iv" in d["data"].get("supported_api_engines", [])


def avatar_iv(look_id, audio_url, motion=None, titulo="fabrica"):
    """Pede um vídeo Avatar IV (sempre IV, nunca III/V) com o áudio já pronto."""
    corpo = {"type": "avatar", "avatar_id": look_id, "audio_url": audio_url,
             "engine": {"type": "avatar_iv"}, "aspect_ratio": "9:16",
             "resolution": "720p", "title": titulo, "expressiveness": "medium"}
    if motion:
        corpo["motion_prompt"] = motion
    st, d = http("POST", f"{HEYGEN}/v3/videos", corpo)
    if st not in (200, 201, 202):
        raise RuntimeError(f"Avatar IV {st}: {d}")
    return d["data"]["video_id"]


def esperar_video(video_id, destino, limite_s=1800):
    t0 = time.time()
    while time.time() - t0 < limite_s:
        st, d = http("GET", f"{HEYGEN}/v3/videos/{video_id}")
        dd = (d or {}).get("data", {}) if st == 200 else {}
        s = dd.get("status")
        if s == "completed":
            return baixar(dd["video_url"], destino), dd
        if s == "failed":
            raise RuntimeError(f"HeyGen falhou {video_id}: {dd.get('failure_message') or dd}")
        time.sleep(15)
    raise TimeoutError(video_id)


# ---------------------------------------------------------------- ffmpeg
def sh(cmd):
    r = subprocess.run(cmd, shell=isinstance(cmd, str), capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"comando falhou: {cmd}\n{r.stderr[-2000:]}")
    return r.stdout


def duracao(arquivo):
    return float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                     "-of", "csv=p=0", arquivo]).strip())


W, H, FPS = 720, 1280, 30


def normalizar(entrada, saida, ini=None, fim=None, mudo=False):
    """Corta e padroniza (720x1280, 30fps, áudio 44.1k estéreo) para poder emendar."""
    cmd = ["ffmpeg", "-v", "error", "-y"]
    if ini is not None:
        cmd += ["-ss", f"{ini:.3f}"]
    if fim is not None:
        cmd += ["-to", f"{fim:.3f}"]
    cmd += ["-i", entrada, "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
            "-filter_complex",
            f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},setsar=1,format=yuv420p[v]",
            "-map", "[v]"]
    cmd += ["-map", "1:a", "-shortest"] if mudo else ["-map", "0:a"]
    cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "19",
            "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-ac", "2", saida]
    sh(cmd)
    return saida


def emendar(partes, saida):
    """Emenda partes já normalizadas e nivela o volume (-14 LUFS, padrão de redes sociais)."""
    lista = saida + ".txt"
    open(lista, "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in partes))
    tmp = saida + ".tmp.mp4"
    sh(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lista,
        "-c", "copy", tmp])
    sh(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-c:v", "copy",
        "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "160k",
        "-ar", "44100", "-movflags", "+faststart", saida])
    os.remove(tmp)
    os.remove(lista)
    return saida
