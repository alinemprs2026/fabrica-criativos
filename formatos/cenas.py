"""Cenas (HyperFrames) para criativos inteiros montados em UMA composição 9:16.

Cada criativo = lista de cenas em sequência. Cada cena tem uma fala (voz TTS grátis,
trecho de avatar já gerado, ou nada) e um VISUAL. Este módulo só gera HTML/animação;
quem prepara áudios e vídeos é o pipeline/roteiro.py.

Visuais (formatos do catálogo Método ADP):
  avatar      – avatar em tela cheia (com zoom & movimento opcional)
  broll       – cenas de apoio (cartão sobre fundo desfocado, ou tela cheia)
  zap         – conversa de WhatsApp (com carimbos ERROR/MEJOR para demonstração)
  split       – ANTES x DESPUÉS (duas conversas, uma em cima da outra)
  busca       – interface de busca (sem marca) digitando a pergunta + resultados
  stories     – story do Instagram (sem marca) com "visto por"
  noticia     – telejornal com tarja URGENTE, lower third e letreiro
  viral       – site de notícia viral (notícia absurda) + plot twist
  cctv        – câmera de segurança (P&B, granulado, hora correndo, REC)
  bloqueio    – tela bloqueada recebendo notificações
  quiz        – teste A/B/C com destaque da resposta
  texto       – frases grandes no ritmo (mini VSL só texto + música)
  cta         – cartão de chamada para a aula grátis
Extras sobre qualquer visual: selo "EJEMPLO"/"DRAMATIZACIÓN", bolha de WhatsApp, comentário.
"""
import html, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from modelos import W, H, AMARELO, BASE_CSS, blocos_legenda, legendas_html, _limpa

E = html.escape

CSS = """
.bg { left:0; top:0; width:720px; height:1280px; }
.fundo { filter: blur(30px) brightness(.42) saturate(1.2); transform: scale(1.15); }
.card { left:30px; width:660px; height:560px; overflow:hidden; border-radius:26px;
        box-shadow:0 20px 60px rgba(0,0,0,.6); border:3px solid rgba(255,255,255,.85); }
.card video, .fr video { position:absolute; left:0; top:0; width:100%; height:100%; object-fit:cover; }
.selo { right:22px; top:24px; background:rgba(0,0,0,.55); color:#fff; font-weight:800; font-size:19px;
        padding:6px 12px; border-radius:8px; letter-spacing:2px; font-family:'Inter',sans-serif; }
.titulo { left:30px; width:660px; text-align:center; font-weight:900; font-size:64px; line-height:1.02;
          color:#fff; -webkit-text-stroke:9px #000; paint-order:stroke fill; text-transform:uppercase; }
.titulo .k { color:#FFE600; }
/* whatsapp */
.zap { left:0; top:0; width:720px; height:1280px; background:#0b141a; }
.zap:before { content:""; position:absolute; inset:0; opacity:.06;
  background-image: radial-gradient(#fff 1.2px, transparent 1.2px); background-size:26px 26px; }
.ztopo { left:0; top:0; width:720px; height:170px; background:#1f2c34; display:flex; align-items:flex-end;
        padding:0 24px 44px; gap:18px; color:#e9edef; }
.foto { width:84px; height:84px; border-radius:50%; background:linear-gradient(135deg,#6b7c85,#3b4a52);
        display:flex; align-items:center; justify-content:center; font-size:38px; }
.nome { font-size:42px; font-weight:800; font-family:'Inter','Noto Color Emoji',sans-serif; }
.zst { left:126px; top:126px; font-size:26px; color:#8696a0; font-family:'Inter',sans-serif; }
.bolha { max-width:620px; padding:20px 28px 42px; border-radius:24px; font-size:46px; line-height:1.25;
         color:#e9edef; font-family:'Inter','Noto Color Emoji',sans-serif; font-weight:500; }
.dela { right:24px; background:#005c4b; border-top-right-radius:4px; }
.dele { left:24px; background:#202c33; border-top-left-radius:4px; }
.hora { position:absolute; right:18px; bottom:8px; font-size:22px; color:#9fb3ad; }
.tick { color:#8696a0; margin-left:6px; font-weight:700; }
.carimbo { font-family:'Inter',sans-serif; font-weight:900; font-size:54px; padding:6px 22px; border-radius:12px;
           border:6px solid; transform:rotate(-8deg); letter-spacing:2px; background:rgba(0,0,0,.35); }
.mau { color:#ff3b3b; border-color:#ff3b3b; } .bom { color:#25d366; border-color:#25d366; }
/* split */
.meia { left:0; width:720px; height:640px; overflow:hidden; }
.rot { left:24px; font-family:'Inter',sans-serif; font-weight:900; font-size:34px; padding:8px 18px;
       border-radius:10px; letter-spacing:3px; }
/* busca */
.busca { left:0; top:0; width:720px; height:1280px; background:#fff; font-family:'Inter',sans-serif; }
.barra { left:36px; top:150px; width:648px; height:96px; border-radius:48px; border:2px solid #dfe1e5;
         box-shadow:0 2px 10px rgba(32,33,36,.18); display:flex; align-items:center; padding:0 30px;
         font-size:34px; color:#202124; gap:18px; background:#fff; }
.cursor { display:inline-block; width:3px; height:40px; background:#1a73e8; margin-left:2px; }
.res { left:40px; width:640px; font-family:'Inter',sans-serif; }
.res .u { font-size:22px; color:#4d5156; } .res .t { font-size:33px; color:#1a0dab; font-weight:500; line-height:1.2; }
.res .d { font-size:24px; color:#4d5156; line-height:1.3; margin-top:4px; }
.sug { left:36px; width:648px; background:#fff; font-size:30px; color:#202124; font-family:'Inter',sans-serif;
       border-radius:0 0 24px 24px; box-shadow:0 8px 14px rgba(32,33,36,.18); padding:6px 0 10px; }
.sug div { padding:12px 30px; } .sug b { font-weight:800; }
/* stories */
.barras { left:16px; top:20px; width:688px; height:6px; display:flex; gap:6px; }
.barras i { flex:1; background:rgba(255,255,255,.45); border-radius:3px; }
.vistos { left:0; top:900px; width:720px; height:380px; background:#fff; border-radius:28px 28px 0 0;
          font-family:'Inter','Noto Color Emoji',sans-serif; color:#111; padding:28px 34px; }
/* noticia */
.tv { left:0; top:0; width:720px; height:1280px; background:#0a1630; }
.fr { left:0; top:250px; width:720px; height:520px; overflow:hidden; }
.urg { left:0; top:770px; height:66px; background:#d90429; color:#fff; font-family:'Inter',sans-serif;
       font-weight:900; font-size:40px; padding:6px 26px; letter-spacing:3px; }
.lt { left:0; top:836px; width:720px; background:#fff; color:#0a1630; font-family:'Inter',sans-serif;
      font-weight:900; font-size:40px; line-height:1.12; padding:16px 26px; text-transform:uppercase; }
.tick2 { left:0; top:1210px; width:720px; height:70px; background:#ffd60a; overflow:hidden; }
.tick2 span { position:absolute; white-space:nowrap; top:14px; font-family:'Inter',sans-serif; font-weight:800;
              font-size:32px; color:#111; }
.envivo { left:24px; top:190px; background:#d90429; color:#fff; font-weight:900; font-size:24px; padding:6px 14px;
          border-radius:6px; font-family:'Inter',sans-serif; letter-spacing:2px; }
.canal { left:0; top:90px; width:720px; text-align:center; color:#fff; font-family:'Inter',sans-serif;
         font-weight:900; font-size:44px; letter-spacing:6px; }
/* viral */
.site { left:0; top:0; width:720px; height:1280px; background:#f4f4f4; font-family:'Inter',sans-serif; }
.sitetopo { left:0; top:0; width:720px; height:120px; background:#111; color:#fff; font-weight:900; font-size:42px;
            display:flex; align-items:center; padding-left:30px; letter-spacing:2px; }
.sitetopo b { color:#ff2d55; }
.manchete { left:30px; top:170px; width:660px; color:#111; font-weight:900; font-size:52px; line-height:1.1; }
.tag { background:#ff2d55; color:#fff; padding:2px 12px; border-radius:6px; font-size:40px; margin-right:10px; }
/* cctv */
.scan { left:0; top:0; width:720px; height:1280px; opacity:.18;
        background: repeating-linear-gradient(0deg, rgba(255,255,255,.25) 0 2px, transparent 2px 5px); }
.osd { font-family:'JetBrains Mono','DejaVu Sans Mono',monospace; color:#fff; font-size:34px; font-weight:700;
       text-shadow:0 0 6px #000, 0 0 2px #000; }
.rec { color:#ff2b2b; }
.canto { width:70px; height:70px; border-color:#fff; border-style:solid; opacity:.8; }
/* bloqueio */
.lock { left:0; top:0; width:720px; height:1280px; background:linear-gradient(160deg,#1d1b3a,#4a1f4f 55%,#0d0d1a); }
.relogio { left:0; top:150px; width:720px; text-align:center; color:#fff; font-family:'Inter',sans-serif;
           font-weight:300; font-size:170px; letter-spacing:-4px; }
.data { left:0; top:120px; width:720px; text-align:center; color:#fff; font-family:'Inter',sans-serif; font-size:32px; font-weight:600; }
.notif { left:28px; width:664px; background:rgba(245,245,245,.88); border-radius:30px; padding:20px 26px;
         font-family:'Inter','Noto Color Emoji',sans-serif; color:#111; }
.notif .a { font-size:24px; color:#555; display:flex; justify-content:space-between; }
.notif .n { font-size:32px; font-weight:800; margin-top:4px; } .notif .m { font-size:32px; margin-top:2px; }
/* quiz */
.quiz { left:0; top:0; width:720px; height:1280px; background:linear-gradient(180deg,#1b1035,#3a0f3f); }
.perg { left:34px; top:110px; width:652px; color:#fff; font-family:'Inter','Noto Color Emoji',sans-serif; font-weight:900;
        font-size:46px; line-height:1.15; text-align:center; }
.op { left:40px; width:640px; min-height:120px; background:#fff; border-radius:24px; padding:20px 26px 20px 110px;
      font-family:'Inter','Noto Color Emoji',sans-serif; font-size:36px; font-weight:700; color:#111; line-height:1.2; }
.op b { position:absolute; left:26px; top:50%; margin-top:-34px; width:68px; height:68px; border-radius:50%;
        background:#7b2ff7; color:#fff; font-size:40px; display:flex; align-items:center; justify-content:center; }
/* texto (mini VSL) */
.slam { left:30px; width:660px; top:430px; text-align:center; font-family:'Inter',sans-serif; font-weight:900;
        font-size:96px; line-height:1.02; color:#fff; text-transform:uppercase; letter-spacing:-2px; }
.slam .k { color:#FFE600; }
/* cta */
.btn { left:110px; width:500px; height:110px; border-radius:60px; background:#25d366; color:#fff;
       font-family:'Inter',sans-serif; font-weight:900; font-size:44px; display:flex; align-items:center;
       justify-content:center; box-shadow:0 10px 30px rgba(37,211,102,.5); }
.ctat { left:40px; width:640px; text-align:center; color:#fff; font-family:'Inter',sans-serif; font-weight:900; }
/* comentário */
.coment { left:40px; top:150px; width:560px; background:#fff; border-radius:22px; padding:18px 24px;
          font-family:'Inter','Noto Color Emoji',sans-serif; color:#111; box-shadow:0 10px 30px rgba(0,0,0,.4); }
.coment .q { font-size:22px; color:#666; } .coment .c { font-size:34px; font-weight:800; line-height:1.2; margin-top:4px; }
"""


def t_de(palavras, alvo, padrao, depois=0.0):
    """Tempo (absoluto) em que a palavra `alvo` é dita (após `depois`)."""
    a = _limpa(alvo)
    for w in palavras:
        if w["ini"] >= depois - 1e-6 and _limpa(w["txt"]).startswith(a):
            return w["ini"]
    return padrao


def _t(spec, cena, padrao):
    """spec pode ser número (segundos após o início da cena) ou palavra."""
    if spec is None:
        return padrao
    if isinstance(spec, (int, float)):
        return cena["t0"] + spec
    return t_de(cena["palavras"], spec, padrao, cena["t0"])


class Comp:
    def __init__(self):
        self.els, self.anim, self.n = [], [], 0

    def id(self, p="e"):
        self.n += 1
        return f"{p}{self.n}"

    def add(self, cls, ini, dur, inner="", style="", tag="div", extra="", idp="e"):
        i = self.id(idp)
        self.els.append(f'<{tag} id="{i}" class="clip {cls}" style="{style}" data-start="{ini:.3f}" '
                        f'data-duration="{max(dur, 0.05):.3f}" {extra}>{inner}</{tag}>')
        return i

    def video(self, src, ini, dur, cls="bg", style=""):
        return self.add(cls, ini, dur, tag="video", extra=f'src="{src}" muted', style=style, idp="v")

    def a(self, s):
        self.anim.append(s)

    def pop(self, i, t, de="{scale:0.7,opacity:0}", dur=0.18):
        self.a(f'tl.fromTo("#{i}",{de},{{scale:1,opacity:1,y:0,x:0,duration:{dur},ease:"back.out(2)"}},{t:.3f});')


# ------------------------------------------------------------------ visuais
def v_avatar(c, cena, p, a):
    t0, d = cena["t0"], cena["dur"]
    i = c.video(a["video"], t0, d)
    if p.get("zoom"):  # zoom & movimento: corte de escala a cada ~1,5 s + tremida
        t, k = t0, 0
        while t < t0 + d - 0.2:
            esc = [1.0, 1.32, 1.12, 1.45][k % 4]
            c.a(f'tl.set("#{i}",{{scale:{esc},transformOrigin:"50% 28%"}},{t:.3f});')
            c.a(f'tl.fromTo("#{i}",{{x:-10}},{{x:0,duration:0.12}},{t:.3f});')
            t += 1.5; k += 1
    else:
        c.a(f'tl.fromTo("#{i}",{{scale:1.1}},{{scale:1.0,duration:0.45,ease:"power2.out"}},{t0:.3f});')
    for spec in p.get("punch", []):  # soco de zoom (reação exagerada)
        tp = _t(spec, cena, t0)
        c.a(f'tl.fromTo("#{i}",{{scale:1.28,transformOrigin:"50% 25%"}},{{scale:1.0,duration:0.35,ease:"power3.out"}},{tp:.3f});')


def _brolls(c, cena, lista, cls, style="", ken=True):
    """Toca a lista de cenas em sequência até preencher a cena."""
    t, fim, k = cena["t0"], cena["t0"] + cena["dur"], 0
    ids = []
    while t < fim - 0.05:
        src, dur = lista[k % len(lista)]
        dd = min(dur, fim - t)
        i = c.video(src, t, dd, cls=cls, style=style)
        if ken:
            c.a(f'tl.fromTo("#{i}",{{scale:1.0}},{{scale:1.1,duration:{dd:.2f},ease:"none"}},{t:.3f});')
        ids.append(i)
        t += dd; k += 1
    return ids


def v_broll(c, cena, p, a):
    t0, d = cena["t0"], cena["dur"]
    if p.get("modo") == "cheio":
        _brolls(c, cena, a["brolls"], "bg")
        return
    _brolls(c, cena, a["brolls"][:1], "bg fundo", ken=False)
    topo = p.get("topo", 230)
    i = c.add("card", t0, d, style=f"top:{topo}px")
    # vídeos dentro do cartão
    t, fim, k = t0, t0 + d, 0
    inner = []
    while t < fim - 0.05:
        src, dur = a["brolls"][k % len(a["brolls"])]
        dd = min(dur, fim - t)
        vi = c.id("v")
        inner.append(f'<video id="{vi}" src="{src}" muted data-start="{t:.3f}" data-duration="{dd:.3f}" class="clip" '
                     f'style="left:0;top:0;width:100%;height:100%;object-fit:cover"></video>')
        c.a(f'tl.fromTo("#{vi}",{{scale:1.0}},{{scale:1.12,duration:{dd:.2f},ease:"none"}},{t:.3f});')
        t += dd; k += 1
    c.els[-1] = c.els[-1].replace("></div>", ">" + "".join(inner) + "</div>")
    c.a(f'tl.fromTo("#{i}",{{scale:0.94}},{{scale:1,duration:0.3,ease:"power3.out"}},{t0:.3f});')
    if p.get("titulo"):
        ti = c.add("titulo", t0, d, p["titulo"], style=f"top:{p.get('titulo_topo', 90)}px")
        c.pop(ti, t0, "{scale:1.3,opacity:0}")


def _bolha(c, quem, txt, hora, topo, ini, fim, azul_em=None, tick=True):
    tk = ""
    if tick and quem == "dela":
        tid = c.id("tk")
        tk = f'<span id="{tid}" class="tick">✓✓</span>'
        if azul_em is not None:
            c.a(f'tl.set("#{tid}",{{color:"#53bdeb"}},{azul_em:.3f});')
    i = c.add(f"bolha {quem}", ini, fim - ini, f'{E(txt)}<span class="hora">{hora}{tk}</span>', style=f"top:{topo}px")
    c.pop(i, ini, "{y:30,opacity:0}" if ini > 0.05 else "{scale:0.9,opacity:0}")
    return i


def v_zap(c, cena, p, a, area=(0, 1280)):
    t0, d = cena["t0"], cena["dur"]
    fim = t0 + d
    if area == (0, 1280):
        c.add("zap", t0, d)
        c.add("ztopo", t0, d, f'<div class="foto">{p.get("foto", "👤")}</div><div class="nome">{E(p.get("nome", "Él ❤️"))}</div>')
        for (sa, sb, txt) in _status(cena, p, fim):
            c.add("zst", sa, sb - sa, E(txt))
    topo = p.get("topo", 260)
    for m in p["msgs"]:
        ini = _t(m.get("em"), cena, t0)
        azul = _t(m["azul"], cena, None) if m.get("azul") is not None else None
        _bolha(c, m["quem"], m["txt"], m.get("hora", "23:14"), m.get("topo", topo), ini, fim, azul)
        topo = m.get("topo", topo) + m.get("alt", 150)
    for s in p.get("carimbos", []):
        ini = _t(s["em"], cena, t0)
        i = c.add(f'carimbo {"bom" if s["tipo"] == "bom" else "mau"}', ini, fim - ini, E(s["txt"]),
                  style=f'left:{s.get("x", 380)}px;top:{s["topo"]}px')
        c.a(f'tl.fromTo("#{i}",{{scale:2.2,opacity:0}},{{scale:1,opacity:1,duration:0.2,ease:"power4.out"}},{ini:.3f});')


def _status(cena, p, fim):
    st = p.get("status", [[0, "en línea"]])
    out = []
    for k, (spec, txt) in enumerate(st):
        a = _t(spec, cena, cena["t0"])
        b = _t(st[k + 1][0], cena, fim) if k + 1 < len(st) else fim
        if b - a > 0.05:
            out.append((a, b, txt))
    return out


def v_split(c, cena, p, a):
    t0, d = cena["t0"], cena["dur"]
    fim = t0 + d
    for k, lado in enumerate(("antes", "depois")):
        L = p[lado]
        y = 0 if k == 0 else 640
        c.add("meia", t0, d, style=f"top:{y}px;background:{'#1a0f12' if k == 0 else '#0b141a'}")
        r = c.add("rot", t0, d, "ANTES ✗" if k == 0 else "DESPUÉS ✓",
                  style=f"top:{y + 24}px;background:{'#ff3b3b' if k == 0 else '#25d366'};color:#fff")
        c.pop(r, _t(L.get("rot_em"), cena, t0))
        topo = y + 110
        for m in L["msgs"]:
            ini = _t(m.get("em"), cena, t0)
            azul = _t(m["azul"], cena, None) if m.get("azul") is not None else None
            _bolha(c, m["quem"], m["txt"], m.get("hora", "22:10"), topo, ini, fim, azul)
            topo += m.get("alt", 150)
    c.add("", t0, d, style="left:0;top:637px;width:720px;height:6px;background:#fff")


def v_busca(c, cena, p, a):
    t0, d = cena["t0"], cena["dur"]
    fim = t0 + d
    c.add("busca", t0, d)
    q = p["consulta"]
    t_ini = _t(p.get("digitar_de", 0.1), cena, t0 + 0.1)
    t_fim = _t(p.get("digitar_ate", 1.6), cena, t0 + 1.6)
    passo = max(0.02, (t_fim - t_ini) / max(1, len(q)))
    letras = []
    for k, ch in enumerate(q):
        li = c.id("l")
        letras.append(f'<span id="{li}" style="opacity:0">{E(ch)}</span>')
        c.a(f'tl.set("#{li}",{{opacity:1}},{t_ini + k * passo:.3f});')
    c.add("barra", t0, d, '<span style="font-size:36px">🔍</span><span>' + "".join(letras) +
          '<span class="cursor"></span></span>')
    t_res = min(_t(p.get("resultados_em"), cena, t_fim + 0.4), fim)
    # sugestões enquanto digita
    if p.get("sugestoes"):
        s = "".join(f"<div>🔍 {E(q)}<b>{E(x)}</b></div>" for x in p["sugestoes"])
        c.add("sug", t_fim, t_res - t_fim, s, style="top:244px")
    y = 300
    for k, r in enumerate(p.get("resultados", [])):
        ti = t_res + 0.15 * k
        i = c.add("res", ti, fim - ti, f'<div class="u">{E(r[0])}</div><div class="t">{E(r[1])}</div><div class="d">{E(r[2])}</div>',
                  style=f"top:{y}px")
        c.pop(i, ti, "{y:20,opacity:0}")
        y += 190


def v_stories(c, cena, p, a):
    t0, d = cena["t0"], cena["dur"]
    fim = t0 + d
    _brolls(c, cena, a["brolls"], "bg")
    c.add("barras", t0, d, "<i style='background:#fff'></i><i></i><i></i>")
    t_v = _t(p.get("vistos_em"), cena, t0 + 0.6)
    linhas = "".join(f'<div style="display:flex;align-items:center;gap:18px;margin-top:22px;font-size:32px">'
                     f'<div class="foto" style="width:70px;height:70px;font-size:30px">{v[0]}</div>'
                     f'<div><b>{E(v[1])}</b><div style="font-size:24px;color:#777">{E(v[2])}</div></div></div>'
                     for v in p["vistos"])
    i = c.add("vistos", t_v, fim - t_v, f'<div style="font-size:30px;font-weight:800">👁 {E(p.get("rotulo", "Visto por"))}</div>{linhas}')
    c.a(f'tl.fromTo("#{i}",{{y:380}},{{y:0,duration:0.3,ease:"power3.out"}},{t_v:.3f});')


def v_noticia(c, cena, p, a):
    t0, d = cena["t0"], cena["dur"]
    fim = t0 + d
    c.add("tv", t0, d)
    c.add("canal", t0, d, E(p.get("canal", "NOTICIAS DEL CORAZÓN")))
    c.add("fr", t0, d)
    _brolls(c, cena, a["brolls"], "fr", style="object-fit:cover", ken=True)
    c.add("envivo", t0, d, "● EN VIVO")
    u = c.add("urg", t0, d, E(p.get("tarja", "URGENTE")))
    c.a(f'tl.fromTo("#{u}",{{x:-300}},{{x:0,duration:0.25,ease:"power3.out"}},{t0:.3f});')
    c.a(f'tl.to("#{u}",{{opacity:0.55,duration:0.25,yoyo:true,repeat:{int(d / 0.5)}}},{t0 + 0.3:.3f});')
    hs = p["manchetes"]
    for k, h in enumerate(hs):
        a_ = _t(h[0], cena, t0)
        b_ = _t(hs[k + 1][0], cena, fim) if k + 1 < len(hs) else fim
        i = c.add("lt", a_, b_ - a_, E(h[1]))
        c.a(f'tl.fromTo("#{i}",{{y:40,opacity:0}},{{y:0,opacity:1,duration:0.2}},{a_:.3f});')
    tk = c.id("tk")
    c.els.append(f'<div class="clip tick2" data-start="{t0:.3f}" data-duration="{d:.3f}"><span id="{tk}">'
                 f'{E(p.get("letreiro", ""))}</span></div>')
    c.a(f'tl.fromTo("#{tk}",{{x:720}},{{x:-2600,duration:{d:.2f},ease:"none"}},{t0:.3f});')


def v_viral(c, cena, p, a):
    t0, d = cena["t0"], cena["dur"]
    fim = t0 + d
    c.add("site", t0, d)
    c.add("sitetopo", t0, d, '<b>●</b>&nbsp;VIRAL<b>HOY</b>')
    m = c.add("manchete", t0, d, f'<span class="tag">{E(p.get("tag", "INSÓLITO"))}</span>{E(p["manchete"])}')
    c.pop(m, t0, "{y:20,opacity:0}")
    _brolls(c, cena, a["brolls"], "", style="left:30px;top:%dpx;width:660px;height:440px;object-fit:cover;border-radius:12px" % p.get("foto_topo", 560), ken=False)
    if p.get("twist"):
        tt = _t(p["twist_em"], cena, t0 + 2)
        i = c.add("titulo", tt, fim - tt, p["twist"], style="top:600px;font-size:76px")
        c.add("", tt, fim - tt, style="left:0;top:0;width:720px;height:1280px;background:rgba(0,0,0,.72)")
        c.els.append(c.els.pop(-2))  # título acima do véu
        c.a(f'tl.fromTo("#{i}",{{scale:1.6,opacity:0}},{{scale:1,opacity:1,duration:0.22,ease:"power4.out"}},{tt:.3f});')


def v_cctv(c, cena, p, a):
    t0, d = cena["t0"], cena["dur"]
    _brolls(c, cena, a["brolls"], "bg", style="filter:grayscale(1) contrast(1.3) brightness(.85)", ken=False)
    c.add("scan", t0, d)
    c.add("osd", t0, d, f'{E(p.get("cam", "CAM 02 · SALA"))}', style="left:40px;top:60px")
    r = c.add("osd rec", t0, d, "● REC", style="right:40px;top:60px")
    c.a(f'tl.to("#{r}",{{opacity:0.15,duration:0.4,yoyo:true,repeat:{int(d / 0.8) + 1}}},{t0:.3f});')
    h, m, s = [int(x) for x in p.get("hora", "23:47:05").split(":")]
    for k in range(int(d) + 1):
        tot = h * 3600 + m * 60 + s + k
        txt = f"{tot // 3600 % 24:02d}:{tot // 60 % 60:02d}:{tot % 60:02d}"
        c.add("osd", t0 + k, min(1, d - k), f'{p.get("data", "08-11-2026")}  {txt}', style="left:40px;top:1150px")
    for (x, y, bw) in [(30, 30, "4px 0 0 4px"), (620, 30, "4px 4px 0 0"), (30, 1180, "0 0 4px 4px"), (620, 1180, "0 4px 4px 0")]:
        c.add("canto", t0, d, style=f"left:{x}px;top:{y}px;border-width:{bw}")


def v_bloqueio(c, cena, p, a):
    t0, d = cena["t0"], cena["dur"]
    fim = t0 + d
    c.add("lock", t0, d)
    c.add("data", t0, d, E(p.get("data", "domingo, 8 de noviembre")))
    c.add("relogio", t0, d, E(p.get("hora", "23:58")))
    topo = p.get("topo", 470)
    for n in p["notifs"]:
        ini = _t(n.get("em"), cena, t0)
        i = c.add("notif", ini, fim - ini, f'<div class="a"><span>💬 MENSAJES</span><span>{E(n.get("quando", "ahora"))}</span></div>'
                  f'<div class="n">{E(n["de"])}</div><div class="m">{E(n["txt"])}</div>', style=f"top:{topo}px")
        c.a(f'tl.fromTo("#{i}",{{y:-60,opacity:0}},{{y:0,opacity:1,duration:0.25,ease:"back.out(1.6)"}},{ini:.3f});')
        topo += 175


def v_quiz(c, cena, p, a):
    t0, d = cena["t0"], cena["dur"]
    fim = t0 + d
    c.add("quiz", t0, d)
    pq = c.add("perg", t0, d, E(p["pergunta"]))
    if not p.get("fixo"):
        c.pop(pq, t0, "{y:-20,opacity:0}")
    topo = p.get("topo", 400)
    for k, op in enumerate(p["opcoes"]):
        ini = _t(op.get("em"), cena, t0 + 0.3 * k)
        if p.get("fixo"):
            ini = t0
        i = c.add("op", ini, fim - ini, f'<b>{"ABC"[k]}</b>{E(op["txt"])}', style=f"top:{topo}px")
        if not p.get("fixo"):
            c.pop(i, ini, "{x:-60,opacity:0}")
        if op.get("veredito_em") is not None:
            tv = _t(op["veredito_em"], cena, fim - 1)
            cor = "#25d366" if op["certa"] else "#ff3b3b"
            c.a(f'tl.to("#{i}",{{backgroundColor:"{cor}",color:"#fff",duration:0.15}},{tv:.3f});')
            if op["certa"]:
                c.a(f'tl.to("#{i}",{{scale:1.06,duration:0.15,yoyo:true,repeat:1}},{tv:.3f});')
            else:
                c.a(f'tl.to("#{i}",{{opacity:0.45,duration:0.2}},{tv + 0.4:.3f});')
        topo += 175


def v_texto(c, cena, p, a):
    t0, d = cena["t0"], cena["dur"]
    fim = t0 + d
    c.add("bg", t0, d, style="background:#0d0d0d")
    fr = p["frases"]  # [[t_rel, "texto com <k>destaque</k>", cor_fundo]]
    for k, f in enumerate(fr):
        a_ = _t(f[0], cena, t0)  # segundos após o início da cena, ou a palavra falada
        b_ = _t(fr[k + 1][0], cena, fim) if k + 1 < len(fr) else fim
        if len(f) > 2 and f[2]:
            c.add("bg", a_, b_ - a_, style=f"background:{f[2]}")
        txt = f[1].replace("<k>", '<span class="k">').replace("</k>", "</span>")
        i = c.add("slam", a_, b_ - a_, txt, style=f[3] if len(f) > 3 else "")
        c.a(f'tl.fromTo("#{i}",{{scale:1.5,opacity:0}},{{scale:1,opacity:1,duration:0.14,ease:"power4.out"}},{a_:.3f});')
        c.a(f'tl.to("#{i}",{{scale:1.04,duration:{max(0.1, b_ - a_ - 0.15):.2f},ease:"none"}},{a_ + 0.14:.3f});')


def v_cta(c, cena, p, a):
    t0, d = cena["t0"], cena["dur"]
    if a.get("brolls"):
        _brolls(c, cena, a["brolls"][:1], "bg fundo", ken=False)
    else:
        c.add("bg", t0, d, style="background:linear-gradient(180deg,#14213d,#000)")
    t1 = c.add("ctat", t0, d, E(p.get("sobre", "CLASE GRATUITA · 5 MINUTOS")), style="top:220px;font-size:38px;color:#FFE600;letter-spacing:2px")
    t2 = c.add("ctat", t0, d, p.get("titulo", "LAS 21 FRASES<br>SECRETAS"), style="top:300px;font-size:92px;line-height:1.0;-webkit-text-stroke:8px #000;paint-order:stroke fill")
    b = c.add("btn", t0, d, E(p.get("botao", "VER LA CLASE ↓")), style="top:640px")
    c.pop(t1, t0); c.pop(t2, t0 + 0.1, "{scale:1.3,opacity:0}"); c.pop(b, t0 + 0.25)
    c.a(f'tl.to("#{b}",{{scale:1.08,duration:0.35,yoyo:true,repeat:{int(d / 0.7)}}},{t0 + 0.5:.3f});')
    c.a(f'tl.to("#{b}",{{y:12,duration:0.35,yoyo:true,repeat:{int(d / 0.7)}}},{t0 + 0.5:.3f});')


VISUAIS = {"avatar": v_avatar, "broll": v_broll, "zap": v_zap, "split": v_split, "busca": v_busca,
           "stories": v_stories, "noticia": v_noticia, "viral": v_viral, "cctv": v_cctv,
           "bloqueio": v_bloqueio, "quiz": v_quiz, "texto": v_texto, "cta": v_cta}


# ------------------------------------------------------------------ extras
def extras(c, cena, p):
    t0, d = cena["t0"], cena["dur"]
    fim = t0 + d
    if p.get("selo"):
        c.add("selo", t0, d, E(p["selo"].upper()), style=p.get("selo_style", ""))
    if p.get("bolha"):
        b = p["bolha"]
        ini = _t(b.get("em"), cena, t0)
        ate = _t(b.get("ate"), cena, fim)
        i = c.add(f'bolha {b.get("quem", "dela")}', ini, ate - ini,
                  f'{E(b["txt"])}<span class="hora">{b.get("hora", "22:41")}<span class="tick">✓✓</span></span>',
                  style=f'top:{b.get("topo", 200)}px;box-shadow:0 12px 30px rgba(0,0,0,.5)')
        c.pop(i, ini)
    if p.get("comentario"):
        k = p["comentario"]
        ini = _t(k.get("em"), cena, t0)
        ate = _t(k.get("ate"), cena, fim)
        i = c.add("coment", ini, ate - ini, f'<div class="q">Respuesta a @{E(k["user"])}</div><div class="c">{E(k["txt"])}</div>')
        c.pop(i, ini)


def composicao(cenas, dur_total):
    """cenas: [{t0, dur, palavras(abs), visual{tipo,...}, assets{}, destaques, leg_topo, audio, audio_vol}]"""
    c = Comp()
    for k, cena in enumerate(cenas):
        v = cena["visual"]
        VISUAIS[v["tipo"]](c, cena, v, cena["assets"])
        extras(c, cena, v)
        if cena.get("audio"):
            c.els.append(f'<audio id="au{k}" class="clip" src="{cena["audio"]}" data-start="{cena["t0"]:.3f}" '
                         f'data-duration="{cena["dur"]:.3f}" data-volume="{cena.get("audio_vol", 1)}"></audio>')
        if cena["palavras"] and v.get("legenda", True):
            rel = [dict(w, ini=w["ini"] - cena["t0"], fim=w["fim"] - cena["t0"]) for w in cena["palavras"]]
            bl = blocos_legenda(rel, cena.get("destaques", []), cena["dur"])
            leg, an = legendas_html(bl, deslocamento=cena["t0"], topo=cena.get("leg_topo", 820), prefixo=f"lg{k}_")
            c.els.append(leg); c.a(an)
    return pagina(dur_total, "\n".join(c.els), "\n".join(c.anim))


def pagina(dur, corpo, anim):
    return f"""<!doctype html>
<html lang="es"><head><meta charset="UTF-8"/>
<meta name="viewport" content="width={W}, height={H}"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>{BASE_CSS}{CSS}</style></head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{dur:.3f}" data-width="{W}" data-height="{H}">
{corpo}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{anim}
window.__timelines = window.__timelines || {{}};
window.__timelines["main"] = tl;
tl.seek(0);
</script>
</body></html>"""
