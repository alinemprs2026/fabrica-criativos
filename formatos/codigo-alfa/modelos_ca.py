"""Modelos HyperFrames do Código Alfa (9:16, espanhol).

Reaproveita as legendas e a página de formatos/modelos.py e acrescenta:
  apresentador – clipe do avatar (Avatar IV) em tela cheia + legendas + selo "MIRA EL VIDEO" opcional
  narracao     – cenas dos campeões num cartão (fundo desfocado) + selo do tema + legendas
  chat         – conversa de WhatsApp entre duas amigas, mensagens aparecem quando a voz lê
"""
import html, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import modelos as M

BADGE_CSS = """
.mira { left:0; width:720px; text-align:center; }
.mira span { display:inline-block; background:#FF7A00; color:#fff; font-weight:900; font-size:40px;
  padding:14px 30px; border-radius:40px; letter-spacing:1px; box-shadow:0 8px 30px rgba(0,0,0,.5);
  -webkit-text-stroke:0; }
.seta { left:0; width:720px; text-align:center; font-size:72px; color:#fff; font-weight:900;
  -webkit-text-stroke:6px #000; paint-order:stroke fill; }
"""


def _badge(ini, fim, topo=1080):
    d = max(0.3, fim - ini)
    el = (f'<div id="mira" class="clip mira" style="top:{topo}px" data-start="{ini:.3f}" data-duration="{d:.3f}">'
          f'<span>MIRA EL VIDEO ↓</span></div>')
    an = (f'tl.fromTo("#mira",{{scale:0.6,opacity:0}},{{scale:1,opacity:1,duration:0.25,ease:"back.out(2)"}},{ini:.3f});'
          f'tl.to("#mira",{{scale:1.08,duration:0.35,yoyo:true,repeat:{max(1, int(d / 0.7))}}},{ini + 0.3:.3f});')
    return el, an


def apresentador(voz, destaques, dur, badge=False, video="avatar.mp4"):
    b = M.blocos_legenda(voz["palavras"], destaques, dur)
    leg, anim = M.legendas_html(b, topo=800)
    partes = [f'<video id="av" class="clip cheio" src="{video}" muted data-start="0" data-duration="{dur:.3f}"></video>',
              M.audio_tag("voz.wav", 0, dur), leg]
    anim = f'tl.fromTo("#av",{{scale:1.10}},{{scale:1.0,duration:0.5,ease:"power2.out"}},0);\n' + anim
    if badge:
        el, an = _badge(0.2, dur)
        partes.append(el); anim += "\n" + an
    return dur, M.pagina(dur, "\n".join(partes), anim, BADGE_CSS)


def narracao(voz, destaques, selo=None, grande=None, badge_desde=None):
    dur, h = M.cartao(voz, destaques, selo=selo, grande=grande)
    if badge_desde is None:
        return dur, h
    el, an = _badge(badge_desde, dur, topo=840)
    h = h.replace("</div>\n<script>", el + "\n</div>\n<script>", 1)
    h = h.replace("window.__timelines", an + "\nwindow.__timelines", 1)
    h = h.replace("</style>", BADGE_CSS + "</style>", 1)
    return dur, h


def chat(voz, mensagens, destaques, nome="Vale 🌸", badge_desde=None, titulo=None):
    """mensagens: [(quem 'ela'|'eu', texto, palavra_que_dispara)]. A voz lê as mensagens.
    A conversa 'rola' para cima quando passa da metade de baixo; legendas grandes embaixo."""
    dur = voz["duracao"] + 0.4
    partes = [f'<div class="clip zap" data-start="0" data-duration="{dur:.3f}"></div>']
    anim, topo, t_prev, desloc = [], 200, -1.0, 0
    t0 = None
    for i, (quem, txt, gatilho) in enumerate(mensagens):
        t = max(0.0 if i == 0 else t_prev + 0.3, M._tempo(voz["palavras"], gatilho, t_prev + 1.0) - 0.15)
        t_prev = t
        t0 = t if t0 is None else t0
        classe = "dele" if quem == "ela" else "dela"
        linhas = 1 + len(txt) // 25
        altura = 100 + 52 * (linhas - 1)
        if topo + altura - desloc > 960:
            novo = topo + altura - 960
            anim.append(f'tl.to(".bolha",{{top:"-={novo - desloc}",duration:0.25,ease:"power2.out"}},{t:.3f});')
            desloc = novo
        partes.append(M._bolha(f"m{i}", classe, txt, "23:1%d" % i, topo, t, dur - t, tick=(quem == "eu")))
        anim.append(f'tl.fromTo("#m{i}",{{y:30,opacity:0}},{{y:0,opacity:1,duration:0.18}},{t:.3f});')
        topo += altura + 16
    partes += [f'<div class="clip topo" data-start="0" data-duration="{dur:.3f}"><div class="foto">🙋‍♀️</div><div class="nome">{html.escape(nome)}</div></div>',
               f'<div class="clip status" data-start="0" data-duration="{dur:.3f}">en línea</div>',
               M.audio_tag("voz.wav", 0, dur)]
    if titulo and t0 and t0 > 0.5:
        partes.append(f'<div id="tit" class="clip grande" style="top:430px" data-start="0" data-duration="{t0:.3f}">{titulo}</div>')
        anim.append('tl.fromTo("#tit",{scale:1.25},{scale:1,duration:0.28,ease:"power4.out"},0);')
    bl = M.blocos_legenda(voz["palavras"], destaques, dur)
    leg, an = M.legendas_html(bl, topo=1010)
    partes.append(leg); anim.append(an)
    css = (M.ZAP_CSS + M.CARTAO_CSS + BADGE_CSS +
           ".bolha{font-size:40px;padding:16px 24px 36px;max-width:640px;} .zap{z-index:0} .topo,.status{z-index:5}"
           " .leg{z-index:6} .grande{font-size:84px}")
    if badge_desde is not None:
        el, an = _badge(badge_desde, dur, topo=1170)
        partes.append(el); anim.append(an)
    return dur, M.pagina(dur, "\n".join(partes), "\n".join(anim), css)
