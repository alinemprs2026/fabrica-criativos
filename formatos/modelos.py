"""Modelos de formato (HyperFrames) para os GANCHOS da fábrica.

Cada função devolve o HTML de uma composição 720x1280 (9:16). O montar.py grava
esse HTML num projeto HyperFrames, junto com os vídeos/áudios, e renderiza.

Formatos:
  avatar     – vídeo do avatar em tela cheia + legendas grandes com palavra colorida
  whatsapp   – conversa de WhatsApp animada (cenas 'visto' e 'antes-depois')
  historico  – cartão com cena histórica + selo de época + legendas
  texto      – título de impacto + cartão com cena de emoção + legendas

Legendas: estilo dos campeões (caixa alta, branco com contorno preto, 1 palavra-chave
amarela por bloco, 2–3 palavras por vez, entrada com "pop").
"""
import html, json, re

W, H = 720, 1280
AMARELO = "#FFE600"

BASE_CSS = f"""
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:#000; }}
#root {{ position:relative; width:{W}px; height:{H}px; overflow:hidden; font-family:'Inter',sans-serif; }}
.clip {{ position:absolute; }}
.cheio {{ left:0; top:0; width:{W}px; height:{H}px; object-fit:cover; }}
.leg {{ left:30px; width:{W-60}px; text-align:center; font-weight:900; font-size:58px; line-height:1.08;
        color:#fff; text-transform:uppercase; letter-spacing:-0.5px;
        -webkit-text-stroke:9px #000; paint-order:stroke fill;
        text-shadow:0 6px 18px rgba(0,0,0,.55); }}
.leg .k {{ color:{AMARELO}; }}
"""


def _limpa(p):
    return re.sub(r"[¿?¡!.,…:;\"“”]", "", p).lower()


def blocos_legenda(palavras, destaques, fim_total, max_palavras=3):
    """Agrupa palavras (com tempos) em blocos curtos de legenda."""
    dest = {_limpa(d) for d in destaques}
    blocos, atual = [], []
    for w in palavras:
        atual.append(w)
        quebra = re.search(r"[.?!,…]$", w["txt"]) is not None
        if len(atual) >= max_palavras or quebra:
            blocos.append(atual)
            atual = []
    if atual:
        blocos.append(atual)
    saida = []
    for i, b in enumerate(blocos):
        ini = 0.0 if i == 0 else b[0]["ini"]  # legenda já no 1º quadro (hook rate)
        fim = blocos[i + 1][0]["ini"] if i + 1 < len(blocos) else fim_total
        partes = []
        for w in b:
            t = html.escape(w["txt"].strip("¿¡").rstrip(",;.…"))
            partes.append(f'<span class="k">{t}</span>' if _limpa(w["txt"]) in dest else t)
        saida.append((ini, max(0.2, fim - ini), " ".join(partes)))
    return saida


def legendas_html(blocos, deslocamento=0.0, topo=760, prefixo="lg"):
    els, anim = [], []
    for i, (ini, dur, txt) in enumerate(blocos):
        s = ini + deslocamento
        els.append(f'<div id="{prefixo}{i}" class="clip leg" style="top:{topo}px" '
                   f'data-start="{s:.3f}" data-duration="{dur:.3f}">{txt}</div>')
        anim.append(f'tl.fromTo("#{prefixo}{i}",{{scale:{0.9 if s < 0.05 else 0.72}}},{{scale:1,duration:0.13,ease:"back.out(2.5)"}},{s:.3f});')
    return "\n".join(els), "\n".join(anim)


def pagina(dur, corpo, anim, css_extra=""):
    return f"""<!doctype html>
<html lang="es"><head><meta charset="UTF-8"/>
<meta name="viewport" content="width={W}, height={H}"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>{BASE_CSS}{css_extra}</style></head>
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


def audio_tag(src, ini, dur, idx=0):
    return (f'<audio id="au{idx}" class="clip" src="{src}" data-start="{ini:.3f}" '
            f'data-duration="{dur:.3f}" data-volume="1"></audio>')


# ------------------------------------------------------------------ AVATAR
def avatar(voz, destaques, video="avatar.mp4"):
    dur = voz["duracao"] + 0.25
    b = blocos_legenda(voz["palavras"], destaques, dur)
    leg, anim = legendas_html(b, topo=820)
    corpo = f"""
<video id="av" class="clip cheio" src="{video}" muted data-start="0" data-duration="{dur:.3f}"></video>
{audio_tag('voz.wav', 0, dur)}
{leg}"""
    anim = f'tl.fromTo("#av",{{scale:1.12}},{{scale:1.0,duration:0.5,ease:"power2.out"}},0);\n' + anim
    return dur, pagina(dur, corpo, anim)


# ------------------------------------------------------------------ CARTÃO (histórico / texto)
CARTAO_CSS = """
.fundo { filter: blur(28px) brightness(.45) saturate(1.2); transform: scale(1.15); }
.cartao { left:30px; width:660px; height:510px; overflow:hidden; border-radius:26px;
          box-shadow:0 20px 60px rgba(0,0,0,.6); border:3px solid rgba(255,255,255,.85); }
.cartao video { position:absolute; left:0; top:0; width:660px; height:510px; object-fit:cover; }
.selo { left:0; width:720px; text-align:center; }
.selo span { display:inline-block; background:#FFE600; color:#111; font-weight:900; font-size:30px;
             letter-spacing:3px; padding:10px 22px; border-radius:10px; text-transform:uppercase; }
.grande { left:24px; width:672px; text-align:center; font-weight:900; font-size:92px; line-height:1.0;
          color:#fff; -webkit-text-stroke:10px #000; paint-order:stroke fill; letter-spacing:-1px; }
.grande .k { color:#FFE600; }
"""


def cartao(voz, destaques, selo=None, grande=None, fundo="fundo.mp4"):
    dur = voz["duracao"] + 0.15
    b = blocos_legenda(voz["palavras"], destaques, dur)
    leg, anim = legendas_html(b, topo=1010 if grande is None else 1050)
    topo_cartao = 250 if grande is None else 470
    partes = [
        f'<video id="bg" class="clip cheio fundo" src="{fundo}" muted data-start="0" data-duration="{dur:.3f}"></video>',
        f'<div id="ct" class="clip cartao" style="top:{topo_cartao}px" data-start="0" data-duration="{dur:.3f}">'
        f'<video id="cv" src="{fundo}" muted data-start="0" data-duration="{dur:.3f}"></video></div>',
        audio_tag("voz.wav", 0, dur), leg]
    anim_extra = [f'tl.fromTo("#ct",{{scale:0.94}},{{scale:1,duration:0.35,ease:"power3.out"}},0);',
                  f'tl.fromTo("#cv",{{scale:1.0}},{{scale:1.12,duration:{dur:.2f},ease:"none"}},0);']
    if selo:
        partes.append(f'<div id="sl" class="clip selo" style="top:150px" data-start="0" data-duration="{dur:.3f}"><span>{html.escape(selo)}</span></div>')
        anim_extra.append('tl.fromTo("#sl",{y:-20},{y:0,duration:0.3},0);')
    if grande:
        g = html.escape(grande)
        partes.append(f'<div id="gr" class="clip grande" style="top:150px" data-start="0" data-duration="{dur:.3f}">{g}</div>')
        anim_extra.append('tl.fromTo("#gr",{scale:1.25},{scale:1,duration:0.28,ease:"power4.out"},0);')
        anim_extra.append('tl.to("#gr",{scale:1.06,duration:0.12,yoyo:true,repeat:1},0.9);')
    return dur, pagina(dur, "\n".join(partes), "\n".join(anim_extra) + "\n" + anim, CARTAO_CSS)


# ------------------------------------------------------------------ WHATSAPP
ZAP_CSS = """
.zap { left:0; top:0; width:720px; height:1280px; background:#0b141a; }
.zap:before { content:""; position:absolute; inset:0; opacity:.06;
  background-image: radial-gradient(#fff 1.2px, transparent 1.2px); background-size:26px 26px; }
.topo { left:0; top:0; width:720px; height:170px; background:#1f2c34; display:flex; align-items:flex-end;
        padding:0 24px 44px; gap:18px; color:#e9edef; font-family:'Inter',sans-serif; }
.foto { width:84px; height:84px; border-radius:50%; background:linear-gradient(135deg,#6b7c85,#3b4a52);
        display:flex; align-items:center; justify-content:center; font-size:38px; }
.nome { font-size:42px; font-weight:800; }
.status { left:126px; top:126px; font-size:26px; color:#8696a0; font-family:'Inter',sans-serif; }
.bolha { max-width:600px; padding:18px 26px 38px; border-radius:22px; font-size:42px; line-height:1.25;
         color:#e9edef; font-family:'Inter','Noto Color Emoji',sans-serif; font-weight:500; }
.dela { right:24px; background:#005c4b; border-top-right-radius:4px; }
.dele { left:24px; background:#202c33; border-top-left-radius:4px; }
.hora { position:absolute; right:18px; bottom:8px; font-size:22px; color:#9fb3ad; }
.tick { color:#8696a0; margin-left:6px; font-weight:700; }
.azul { color:#53bdeb !important; }
.chip { left:0; width:720px; text-align:center; }
.chip span { display:inline-block; background:#182229; color:#c9d3d8; font-size:28px; padding:8px 18px;
             border-radius:10px; font-family:'Inter',sans-serif; text-transform:uppercase; letter-spacing:1px; }
.exemplo { right:22px; top:190px; background:rgba(255,230,0,.95); color:#111; font-weight:900; font-size:20px;
           padding:6px 12px; border-radius:8px; letter-spacing:2px; font-family:'Inter',sans-serif; }
.visto { left:0; width:720px; text-align:center; font-weight:900; font-size:64px; color:#53bdeb;
         -webkit-text-stroke:8px #000; paint-order:stroke fill; font-family:'Inter',sans-serif; }
"""


def _bolha(id_, quem, texto, hora, topo, ini, dur, tick=True):
    t = f'<span id="{id_}t" class="tick">✓✓</span>' if (tick and quem == "dela") else ""
    return (f'<div id="{id_}" class="clip bolha {quem}" style="top:{topo}px" data-start="{ini:.3f}" '
            f'data-duration="{dur:.3f}">{html.escape(texto)}<span class="hora">{hora}{t}</span></div>')


def _tempo(palavras, alvo, padrao):
    for w in palavras:
        if _limpa(w["txt"]).startswith(_limpa(alvo)):
            return w["ini"]
    return padrao


def whatsapp(cena, voz_gancho, destaques, voz_corpo=None, destaques_corpo=()):
    """cena 'visto': 3 mensagens dela sem resposta.
       cena 'antes-depois': mensagem genérica (visto) x mensagem no tom certo (resposta rápida).
       Se voz_corpo vier, a narração do corpo continua na mesma conversa."""
    dg = voz_gancho["duracao"] + 0.25
    dur = dg + ((voz_corpo["duracao"] + 0.35) if voz_corpo else 0)
    partes = ['<div class="clip zap" data-start="0" data-duration="%.3f"></div>' % dur,
              f'<div class="clip topo" data-start="0" data-duration="{dur:.3f}"><div class="foto">👤</div><div class="nome">Él ❤️</div></div>',
              f'<div class="clip exemplo" data-start="0" data-duration="{dur:.3f}">EJEMPLO</div>',
              audio_tag("voz.wav", 0, dg, 0)]
    anim = []
    st = []  # status do topo: (ini, fim, texto)
    if cena == "visto":
        tv = _tempo(voz_gancho["palavras"], "visto", dg - 1.0)
        msgs = [("Hola 😊", 0.0), ("¿Todo bien?", 1.0), ("¿Estás ahí? 🥺", 1.9)]
        topo = 260
        for i, (m, t) in enumerate(msgs):
            partes.append(_bolha(f"m{i}", "dela", m, "21:0%d" % (4 + i), topo, t, dur - t))
            ent = "{scale:0.9},{scale:1" if t == 0 else "{y:30,opacity:0},{y:0,opacity:1"
            anim.append(f'tl.fromTo("#m{i}",{ent},duration:0.18}},{t:.3f});')
            anim.append(f'tl.set("#m{i}t",{{color:"#53bdeb"}},{tv:.3f});')
            topo += 150
        partes.append(f'<div id="vs" class="clip visto" style="top:760px" data-start="{tv:.3f}" data-duration="{dur - tv:.3f}">VISTO ✓✓</div>')
        anim.append(f'tl.fromTo("#vs",{{scale:1.8,opacity:0}},{{scale:1,opacity:1,duration:0.22,ease:"power4.out"}},{tv:.3f});')
        st = [(0, dur, "en línea")]
        leg_topo = 1010
    else:  # antes-depois
        pv = voz_corpo["palavras"] if voz_corpo else []
        off = dg + 0.05
        t_visto = off + _tempo(pv, "visto", 3.0)
        t_tono = off + _tempo(pv, "cambió", 6.0)
        t_seg = off + _tempo(pv, "segundos", 10.0)
        partes.append(_bolha("m0", "dela", "Hola, ¿cómo estás? 😊", "21:04", 250, 0.0, dur))
        anim.append('tl.fromTo("#m0",{scale:0.9},{scale:1,duration:0.18},0);')
        anim.append(f'tl.set("#m0t",{{color:"#53bdeb"}},{t_visto:.3f});')
        partes.append(f'<div id="vs" class="clip chip" style="top:390px" data-start="{t_visto:.3f}" data-duration="{dur - t_visto:.3f}"><span>Visto · sin respuesta</span></div>')
        partes.append(f'<div id="dv" class="clip chip" style="top:470px" data-start="{t_tono:.3f}" data-duration="{dur - t_tono:.3f}"><span>Al día siguiente</span></div>')
        partes.append(_bolha("m1", "dela", "Hoy pasé por aquel café y me acordé de algo que me dijiste… pero mejor te lo cuento otro día 😏", "20:41", 540, t_tono + 0.5, dur - t_tono - 0.5))
        anim.append(f'tl.fromTo("#m1",{{y:30,opacity:0}},{{y:0,opacity:1,duration:0.2}},{t_tono + 0.5:.3f});')
        anim.append(f'tl.set("#m1t",{{color:"#53bdeb"}},{t_seg - 1.2:.3f});')
        partes.append(_bolha("m2", "dele", "¿Qué cosa? 👀 Cuéntame ya", "20:41", 860, t_seg, dur - t_seg, tick=False))
        anim.append(f'tl.fromTo("#m2",{{x:-40,opacity:0}},{{x:0,opacity:1,duration:0.2}},{t_seg:.3f});')
        st = [(0, t_visto, "en línea"), (t_visto, t_tono, "últ. vez hoy a las 21:06"),
              (t_tono, t_seg - 1.2, "en línea"), (t_seg - 1.2, dur, "escribiendo…")]
        leg_topo = 1060
    for i, (a, b, txt) in enumerate(st):
        if b - a > 0.05:
            partes.append(f'<div class="clip status" data-start="{a:.3f}" data-duration="{b - a:.3f}">{txt}</div>')
    bl = blocos_legenda(voz_gancho["palavras"], destaques, dg)
    leg, an = legendas_html(bl, topo=leg_topo)
    partes.append(leg); anim.append(an)
    if voz_corpo:
        partes.append(audio_tag("voz2.wav", dg + 0.05, voz_corpo["duracao"] + 0.3, 1))
        bl2 = blocos_legenda(voz_corpo["palavras"], destaques_corpo, voz_corpo["duracao"] + 0.3)
        leg2, an2 = legendas_html(bl2, deslocamento=dg + 0.05, topo=leg_topo, prefixo="lc")
        partes.append(leg2); anim.append(an2)
    return dur, pagina(dur, "\n".join(partes), "\n".join(anim), ZAP_CSS)
