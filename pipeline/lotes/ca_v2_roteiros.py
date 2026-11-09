"""Gera pipeline/lotes/codigo-alfa-lote-1-v2.json (reedição do Código Alfa · Lote 1: mínimo 1 min, sem HeyGen novo).

Cada vídeo: gancho original intacto (até `corte`) + corpo novo (TTS grátis na mesma voz) + fechamento original
com o avatar já pago (`cauda`, segundos finais do vídeo atual). Imagens em tela cheia (banco + cortes dos campeões
sem o millonario secreto), cada uma no máximo 1x por vídeo.
Linha: ("frase com *destaque*", clipe)  · clipe = n (item do banco) ou "c:nome" (corte de campeão)
Bloco especial: dict com "texto" + "visual" (busca, zap, bloqueio, texto, cta).
Uso: python3 pipeline/lotes/ca_v2_roteiros.py   (precisa de $FABRICA_WORK/codigo-alfa-lote-1/heygen/*.json)
"""
import json, os, re, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, ".."))
import fabrica as F

BASE = json.load(open(os.path.join(AQUI, "codigo-alfa-lote-1.json")))
HEYGEN = os.path.join(F.WORK, "codigo-alfa-lote-1", "heygen")

# cortes dos campeões (só cenas de apoio, sem o millonario secreto, sem cientistas/universidades), região "alto" = sem a legenda antiga
CORTES = {  # limites conferidos pela troca de cena real de cada campeão
    "regalo": ["k2", 23.5, 28.02],
    "billetera": ["k2", 28.18, 30.19],
    "rubia": ["k2", 30.35, 32.72],
    "reloj": ["k2", 32.88, 35.79],
    "playa": ["k2", 40.65, 42.55],
    "barba": ["k2", 42.71, 45.25],
    "joven": ["k2", 45.41, 47.49],
    "libro": ["k2", 59.51, 61.12],
    "meditar": ["k2", 70.28, 72.15],
    "champan": ["k2", 76.85, 79.09],
    "mar": ["k2", 84.65, 86.92],
    "silueta": ["k2", 91.75, 96.62],
    "montana": ["k3", 5.15, 6.9],
    "redentor": ["k3", 11.75, 15.62],
    "buda_cueva": ["k3", 15.78, 21.12],
    "torres": ["k3", 21.28, 26.95],
    "torres2": ["k3", 27.11, 30.59],
    "cruz": ["k3", 37.01, 40.29],
    "monasterio": ["k3", 44.71, 48.65],
    "estatua": ["k3", 62.68, 66.65],
    "brindis": ["k3", 77.68, 81.5],
    "oficina": ["k4", 5.38, 7.29],
    "tablet": ["k4", 23.31, 25.39],
    "billete_vuela": ["k4", 58.98, 60.75],
    "pareja": ["k4", 60.91, 62.75],
    "multitud": ["k4", 69.48, 72.62],
    "despertar": ["k1", 59.48, 61.02],
}

CTA_CARD = {"tipo": "cta", "sobre": "VIDEO CORTO", "titulo": "EL VIDEO DEL<br>MILLONARIO", "botao": "MIRA EL VIDEO ↓"}

DESCARTADOS = {"15": "avatar idoso (senhora): regra da Aline de 08/11", "16": "avatar idoso (avó): regra da Aline de 08/11"}
V = {}  # id -> {"voz":..., "corte": s (gancho não-avatar), "blocos": [...], "primary_text": ...}

J = "c:joven"
def T(texto, frases, leg=None):
    return {"texto": texto, "visual": {"tipo": "texto", "legenda": False, "frases": frases}}
CTA = lambda f: {"texto": "Toca el botón de abajo y mira el video corto, antes de que lo quiten.",
                 "visual": dict(CTA_CARD, fundo=f"b:{f}"), "destaques": ["botón", "video", "quiten"], "leg_topo": 900}

V["01"] = dict(primary_text="Ella llevaba años pidiendo y nada cambiaba… hasta que vio un video extraño de un millonario. 😳 Míralo antes de que lo quiten 👇", blocos=[
    [("Ella no estaba haciendo nada *raro*.", 126), ("Llevaba años *pidiendo*,", 157), ("repitiendo *afirmaciones* cada mañana", 169),
     ("y visualizando la vida que quería.", 136), ("Y cada mes era lo mismo:", 129), ("cuentas, *estrés*, cansancio.", 105)],
    [("Hasta que una noche vio un video *extraño*.", 185), ("Un millonario que nunca muestra la *cara*", 117),
     ("explica por qué a casi nadie", 127), ("le *funciona* nada de eso.", 108)],
    [("Dice que hay una parte *espiritual* de la mente", 161), ("que los antiguos cristianos, budistas y egipcios", "c:monasterio"),
     ("cuidaban como un *tesoro*.", 80), ("Y que en casi todos nosotros", "c:multitud"), ("hoy está *dormida*.", 184)],
    [("Con esa parte apagada, puedes rezar,", 83), ("visualizar y repetir frases mil *veces*,", 124),
     ("y es como hablarle a una radio *sin señal*.", 91)],
    [("Él muestra un ritual de *siete minutos*", 138), ("para despertarla, en silencio, en casa.", 170),
     ("Sin cursos, sin meditar horas,", 113), ("sin cambiar de *religión*.", 97)],
    [("Ella cuenta que lo primero que sintió fue *calma*.", 95), ("Dejó de perseguir las cosas con *desesperación*", 145),
     ("y empezó a ver *oportunidades*", "c:silueta"), ("que antes pasaban frente a ella.", 99)],
    [("¿Suena raro? Sí. A mí también me sonó *raro*.", 96), ("Pero son solo siete minutos.", 93),
     ("Si no es para ti, no pierdes *nada*.", "c:mar"), ("¿Y si es justo la *pieza* que te faltaba?", 119)],
])

V["02"] = dict(primary_text="No te digo que dejes a Dios. Te digo que dejes de rogar como si no te escuchara. 🙏 Mira el video antes de que lo quiten 👇", blocos=[
    [("Sí, escuchaste *bien*.", J), ("No te digo que dejes a *Dios*.", "c:redentor"), ("Te digo que dejes de *rogar*", "c:barba"),
     ("como si Él no te escuchara.", 146)],
    [("Piénsalo.", 96), ("Cuando ruegas por una *bendición*,", 157), ("le repites a tu mente lo que te *falta*.", 188),
     ("Y tu mente se queda mirando la *falta*.", 152), ("Día tras día. Año tras *año*.", 129)],
    T("Los antiguos cristianos hacían algo distinto. Primero despertaban algo por dentro, y después pedían.",
      [[0, "LOS ANTIGUOS <k>CRISTIANOS</k>", "#0d0d0d"], ["primero", "PRIMERO <k>DESPIERTAS</k>", "#101a2e"], ["después", "DESPUÉS <k>PIDES</k>", "#0d0d0d"]]),
    [("En un video que está dando *vueltas*,", 185), ("un millonario que no muestra la cara", 88), ("explica esa parte *olvidada*:", "c:libro"),
     ("una parte *espiritual* de la mente", 119), ("que casi nadie usa.", "c:multitud")],
    [("Él dice que cuando esa parte se *enciende*,", 161), ("dejas de perseguir,", 99), ("y empiezas a *recibir* con calma.", "c:mar"),
     ("Las puertas correctas se *abren*.", 128), ("Las personas correctas *llegan*.", "c:brindis")],
    [("No es una religión nueva.", 186), ("No tienes que dejar tu *fe*.", 97), ("Es un ritual corto, de *siete minutos*,", 138),
     ("que puedes hacer en tu casa.", 170)],
    [("Y no tienes que creerme a mí.", 123), ("Escucha lo que él explica,", 141), ("y decide *tú*.", "c:despertar")],
    [("Si después de verlo no te hace sentido,", 124), ("no pierdes *nada*.", 113), ("Pero si tiene razón,", 80),
     ("cada día que sigues rogando", 83), ("es un día *perdido*.", "c:reloj")],
])

V["03"] = dict(primary_text="Dicen que intentaron borrar este video. Un millonario explica la parte de la mente que casi nadie usa. 🤫 Mírelo antes de que lo quiten 👇", blocos=[
    [("Y no, no es un video de *motivación*.", 96), ("Es un hombre que se volvió *millonario*", 137), ("y que nunca muestra la *cara*.", 88)],
    [("Él cuenta algo que, según dice,", 141), ("la *élite* conoce hace mucho tiempo", 142), ("y que fue *borrado*", "c:estatua"),
     ("de las enseñanzas espirituales.", "c:libro")],
    [("Por eso usted reza,", 83), ("repite *afirmaciones*, visualiza…", 169), ("y siente que todo se queda en el *aire*.", 126)],
    [("Según él, no es falta de *fe*.", 97), ("Tampoco es falta de *esfuerzo*.", 77), ("Es que hay una parte de la mente", 109),
     ("que está *dormida*.", 184), ("Y mientras duerme, nada de eso", 115), ("tiene a dónde *llegar*.", 153)],
    [("Él muestra cómo despertarla", 161), ("con *tres pasos* sencillos.", 112), ("Sin cursos caros.", 175), ("Sin horas de *meditación*.", 170)],
    [("Y no le pide que deje su *fe*.", 154)],
    [("Lo primero que cambia es la forma de ver las cosas:", 82), ("más *calma*, más claridad,", "c:playa"), ("menos miedo al *futuro*.", "c:silueta")],
    [("Yo pensé que era otro video más.", 124), ("Pero lo vi completo,", 185), ("y entendí por qué lo quieren *quitar*.", 121)],
    [("Si usted también siente que hace todo bien", 85), ("y *nada cambia*,", 108), ("no lo deje para *después*.", 129)],
])

V["04"] = dict(primary_text="Son las 3 de la mañana y no puedo dejar de pensar en lo que dijo este millonario… 🌙 Míralo antes de dormir 👇", blocos=[
    T("Me lo mandaron hace unas horas, con un mensaje que decía: tienes que ver esto.",
      [[0, "3:07 AM", "#0d0d0d"], ["tienes", "\"TIENES QUE <k>VER ESTO</k>\"", "#101a2e"]]),
    [("Él dice algo que no me deja de dar *vueltas*:", 126), ("que la gente buena trabaja más,", "c:oficina"),
     ("reza más, se *esfuerza* más…", 157), ("y aun así se queda con *menos*.", 79)],
    [("Y que no es *culpa* de ellos.", 106), ("Que hay una parte de la mente,", 109), ("una parte *espiritual*,", 119),
     ("que en casi todos está *apagada*.", 115)],
    [("Y mientras está apagada,", 184), ("puedes pedir, visualizar y repetir frases,", 169), ("pero es como sembrar en tierra *seca*.", 87)],
    [("Lo que él explica es cómo *encenderla*.", 161), ("Un ritual de *siete minutos*,", 138), ("que se hace en *silencio*, en casa.", "c:meditar")],
    [("Dice que después de eso", 95), ("dejas de *perseguir* las cosas,", 99), ("y empiezas a notar *oportunidades*", "c:multitud"),
     ("que antes pasaban frente a ti.", 127)],
    [("No es una religión. No es un *curso*.", 186), ("Es algo que casi nadie te va a *contar*.", "c:estatua")],
    [("Yo sé que suena raro a esta hora.", 152), ("Pero si este video te apareció de *madrugada*,", "c:montana"),
     ("no creo que sea *casualidad*.", 153), ("Míralo antes de *dormir*.", "c:despertar")],
])

V["05"] = dict(primary_text="Si este video te apareció hoy, no es coincidencia. ✨ Un millonario explica por qué tus pedidos no llegan. Míralo 👇", blocos=[
    [("Llevas mucho tiempo pidiendo una *señal*.", 155), ("Rezando,", 157), ("escribiendo lo que quieres,", 169), ("*imaginando* otra vida.", 136),
     ("Y sientes que el universo no te *contesta*.", 126)],
    [("Hace poco vi un video de un *millonario*", 141), ("que explica por qué.", 96), ("Dice que el problema no es el *universo*.", 114),
     ("Es que la parte de tu mente", 109), ("que recibe esas señales", "c:torres"), ("está *dormida*.", 184)],
    T("Se lo mostré a mi hermana, y me dijo: esto es justo lo que me pasaba.",
      [[0, "SE LO MOSTRÉ A MI <k>HERMANA</k>", "#0d0d0d"], ["esto", "\"ES JUSTO LO QUE <k>ME PASABA</k>\"", "#101a2e"]]),
    [("Él cuenta que los antiguos cristianos,", "c:monasterio"), ("budistas y egipcios", "c:buda_cueva"), ("*cuidaban* esa parte.", 154),
     ("La llamaban una línea directa con lo *divino*.", 80)],
    [("Y dice que se puede despertar", 161), ("con un ritual de *siete minutos*.", 93), ("Cuando despierta, dejas de *forzar*", 145),
     ("y empiezas a ver las *puertas* que se abren.", 95)],
    [("No tienes que dejar tu *fe*.", 97)],
    [("Tal vez pienses:", 124), ("otra cosa más que no va a *funcionar*.", 108), ("Por eso no te pido que *creas*.", J), ("Te pido que lo *veas*.", 172)],
    [("Si llegaste hasta aquí,", 128), ("ya sabes que no fue *coincidencia*.", 143)],
])

V["06"] = dict(primary_text="Rezar por dinero es repetirle a su mente lo que le falta. 🙏 Un millonario explica el error que casi todos cometen. Mírelo 👇", blocos=[
    [("Cuando usted le pide *dinero* a Dios", 157), ("todas las noches,", 115), ("sin querer repite una sola idea:", 96),
     ("no tengo, me *falta*.", 188), ("Y eso es lo que su mente *escucha*.", 152)],
    T("Pedir dinero es pensar en lo que falta. Y la mente se queda donde está su atención.",
      [[0, "PEDIR <k>DINERO</k>", "#0d0d0d"], ["pensar", "= PENSAR EN LO QUE <k>FALTA</k>", "#2a0d0d"], ["mente", "LA MENTE SE QUEDA <k>AHÍ</k>", "#0d0d0d"]]),
    [("Lo vi en un video de un *millonario*", 185), ("que lo explica mejor que nadie.", 101), ("Él dice que hay una parte *espiritual* de la mente", 119),
     ("que está dormida en casi todos.", 184), ("Y que, mientras duerme, rezar por dinero", 83), ("es como hablar en un cuarto *cerrado*.", 106)],
    [("Los antiguos sabían despertarla *primero*,", 154), ("y recién después agradecer y *pedir*.", "c:barba")],
    [("Él enseña cómo hacerlo", 161), ("con un ritual de *siete minutos*.", 113), ("En silencio, sin cursos,", 170), ("sin cambiar sus *creencias*.", 97)],
    [("Lo primero que cambia no es su *cuenta* del banco.", 103), ("Es usted:", 136), ("más *calma*, más claridad,", 141),
     ("y menos miedo cuando llegan las *cuentas*.", 85)],
    [("Si le suena raro, está bien.", 124), ("A mí también me sonó raro.", 126), ("Pero son solo *siete minutos*,", 129),
     ("y puede cambiar para siempre", "c:silueta"), ("la forma en que usted *reza*.", "c:cruz")],
])

V["07"] = dict(primary_text="Dios no es el problema. Tu fe no es el problema. El problema es desde dónde pides. 🙏 Mira el video 👇", blocos=[
    [("Antes de que te enojes, *escúchame*.", J), ("Dios no es el *problema*.", "c:redentor"), ("Tu *fe* no es el problema.", 157)],
    [("El problema es desde *dónde* pides.", 83), ("Si pides desde el *miedo*,", 152), ("tu oración nace *cansada*.", 108),
     ("Si pides desde la *desesperación*,", 146), ("la respuesta parece no llegar *nunca*.", "c:reloj")],
    T("Hay una antena espiritual dentro de ti. Y en casi todos está desconectada.",
      [[0, "HAY UNA <k>ANTENA</k>", "#0d0d0d"], ["dentro", "DENTRO DE <k>TI</k>", "#101a2e"], ["desconectada", "<k>DESCONECTADA</k>", "#2a0d0d", "font-size:66px"]]),
    [("Por eso las afirmaciones y la visualización", 169), ("tampoco te funcionaron.", 105), ("No es que estés haciendo algo *mal*.", 123),
     ("Es que estás pidiendo con la *antena* apagada.", "c:torres2")],
    [("Un millonario lo explica en un video *corto*.", 104), ("Dice que esa parte se puede volver a *conectar*", "c:torres"),
     ("con un ritual de *siete minutos*,", 170), ("en silencio, en tu casa.", 138)],
    [("Y cuando se conecta,", 161), ("dejas de *mendigar*", 188), ("y empiezas a *recibir*.", "c:regalo"), ("Las ideas llegan,", 172),
     ("las *puertas* se abren,", 128), ("la paz vuelve.", "c:mar")],
    [("Los antiguos cristianos lo *sabían*.", "c:monasterio"), ("Primero se despierta, después se *pide*.", 154)],
    [("No tienes que dejar tu iglesia", 186), ("ni tu *fe*.", 97), ("Es al revés:", 96), ("tu oración por fin va a tener a dónde *llegar*.", 114)],
    [("Si sientes que llevas años *pidiendo*,", 184), ("mira esto hoy.", 112)],
])

V["08"] = dict(primary_text="Jesús, Tesla y Buda hablaron del mismo secreto con palabras distintas. 🔱 Un millonario lo reunió en un video corto. Míralo 👇", blocos=[
    [("Un maestro en *Galilea*.", "c:redentor"), ("Un príncipe que dejó todo para *meditar*.", "c:buda_cueva"), ("Un inventor obsesionado con la *energía*.", "c:torres")],
    [("Los tres hablaron de lo *mismo*", "c:libro"), ("con palabras diferentes:", 186), ("energía, *frecuencia*,", 89), ("una luz *interior*.", 80)],
    [("Y los tres apuntaban a una parte de nosotros", 109), ("que casi *nadie* usa.", "c:multitud"), ("Una parte *espiritual* de la mente", 119),
     ("que los antiguos llamaban el *tercer ojo*.", "c:estatua")],
    [("Hoy la mayoría reza,", 83), ("visualiza y repite *afirmaciones*", 169), ("con esa parte completamente *dormida*.", 115), ("Por eso sienten que *nada* llega.", 108)],
    [("Un millonario que prefiere no mostrar su *rostro*", 142), ("reunió esas enseñanzas en un video *corto*,", 185),
     ("y muestra un ritual de *siete minutos*", 93), ("para despertar esa parte.", 161)],
    [("No es una *religión*.", "c:monasterio"), ("No es un *curso*.", 175), ("Es algo que, según él,", "c:montana"), ("fue sacado de las enseñanzas a *propósito*.", 162)],
    [("Él no promete *riqueza* de un día para otro.", 102), ("Habla de calma, de *claridad*,", "c:playa"), ("y de dejar de vivir *persiguiendo*.", 99)],
    [("Si sientes *curiosidad*,", 153), ("no lo dejes para mañana.", 112), ("Dicen que no va a estar *disponible*", 129), ("por mucho tiempo.", 113)],
    CTA(137),
])

V["09"] = dict(primary_text="\"El reino de Dios está dentro de ti.\" Casi nadie entendió lo que significaba. 🙏 Un millonario lo explica en este video 👇", blocos=[
    [("Nos enseñaron a buscar a Dios *afuera*.", "c:cruz"), ("En el cielo,", 114), ("en un templo,", 186), ("en una oración repetida mil *veces*.", 157)],
    [("Pero Jesús dijo *dentro*.", 97), ("Y los antiguos cristianos lo tomaban *literal*:", "c:monasterio"), ("hay una parte de ti", 136), ("que conecta con lo *divino*.", 80)],
    [("Los budistas la cuidaban en *silencio*.", 150), ("Los egipcios la dibujaban en sus *templos*.", 151), ("Todos hablaban de lo *mismo*.", 109)],
    [("Un millonario explica en un video", 102), ("por qué esa parte está *dormida* en casi todos,", 184), ("y por qué las oraciones", 83), ("parecen no *llegar*.", 107)],
    T("No se trata de pedir más. Se trata de despertar lo que ya está dentro.",
      [[0, "NO ES PEDIR <k>MÁS</k>", "#0d0d0d"], ["despertar", "ES <k>DESPERTAR</k>", "#101a2e"], ["dentro", "LO QUE YA ESTÁ <k>DENTRO</k>", "#0d0d0d"]]),
    [("Él muestra un ritual de *siete minutos*", "c:meditar"), ("para hacerlo en silencio, en casa.", 138), ("No reemplaza tu fe.", 154), ("La *completa*.", 161)],
    [("Según él, cuando esa parte despierta,", 95), ("vives con más *paz*,", "c:mar"), ("y empiezas a ver tu camino", 99), ("con otros *ojos*.", "c:silueta")],
    [("No tienes que dejar tu *iglesia*.", "c:redentor"), ("No tienes que creer en nada *raro*.", 123), ("Solo siete minutos y el *corazón* abierto.", 129)],
    [("Si ese versículo siempre te tocó el *corazón*,", "c:barba"), ("tienes que ver *esto*.", 121)],
])

V["10"] = dict(primary_text="La ley de atracción funciona para unos pocos. Un millonario revela la pieza que falta. 🧲 Mira el video corto 👇", blocos=[
    [("Y no es porque ellos trabajen *más*.", "c:oficina"), ("Ni porque sean más *inteligentes*,", 175), ("ni porque tengan más *suerte*.", 86)],
    {"texto": "Si buscas por qué no te funciona, vas a encontrar lo de siempre: piensa positivo, visualiza, repite afirmaciones.",
     "visual": {"tipo": "busca", "consulta": "por qué no me funciona la ley de atracción", "digitar_ate": "vas",
                "resultados_em": "piensa", "resultados": [
                    ["blog · consejos", "Piensa positivo todos los días", "Cambia tus pensamientos y todo cambiará…"],
                    ["video · 12 min", "Visualiza tu vida ideal", "Imagina con detalle lo que quieres…"],
                    ["foro · preguntas", "Lo hice todo y nada cambia", "¿A alguien más le pasa?"]]},
     "destaques": ["siempre", "positivo", "afirmaciones"], "leg_topo": 1000},
    [("Pero nadie te dice la *pieza* que falta.", 96), ("Un millonario la explica en un video *corto*:", 185), ("hay una parte *espiritual*", 119),
     ("en el centro de la mente", "c:tablet"), ("que en la mayoría de las personas", 127), ("está *dormida*.", 184)],
    [("Con esa parte apagada,", 115), ("visualizar es como mandar una carta", 124), ("sin *dirección*.", 116)],
    [("Por eso las *afirmaciones* no se pegan,", 169), ("y la *visualización* se queda en sueño.", 126), ("No es tu *culpa*.", 146),
     ("Nadie te explicó esta *parte*.", "c:libro")],
    [("Él muestra *tres pasos* sencillos", 161), ("y un ritual de *siete minutos*", 93), ("para despertarla.", 138)],
    [("No necesitas creer en nada *nuevo*.", 154), ("No tienes que dejar tu *fe*.", 157), ("Solo siete minutos", 129), ("y la mente *abierta*.", 109)],
    [("Lo que cambia es cómo te sientes:", 95), ("sin *perseguir*,", 99), ("sin forzar,", 145), ("en *paz* con lo que viene.", 110)],
    [("Si eres de \"todos los *demás*\",", "c:multitud"), ("este video es para *ti*.", 143)],
])

V["11"] = dict(cauda=0, primary_text="Mi amiga me mandó este video anoche… 😳 Dice que hay una parte de la mente que está dormida. Míralo antes de que lo borren 👇", blocos=[
    {"texto": "Sí. Dice que hay una parte de la mente que está dormida, y que por eso rezamos, pedimos, y nada cambia.",
     "visual": {"tipo": "zap", "nome": "Vale 🌸", "foto": "👩", "topo": 200, "msgs": [
         {"quem": "dele", "txt": "¿Viste el video que te mandé? 😳", "em": 0, "hora": "22:41", "alt": 130},
         {"quem": "dela", "txt": "¿El del millonario? 🤔", "em": 0, "hora": "22:41", "alt": 130},
         {"quem": "dele", "txt": "Sí. Dice que hay una parte de la mente que está dormida", "em": "dice", "hora": "22:42", "alt": 170},
         {"quem": "dele", "txt": "y que por eso rezamos, pedimos y nada cambia 🙏", "em": "rezamos", "hora": "22:42"}]},
     "destaques": ["dormida", "rezamos", "nada"], "leg_topo": 1040},
    [("Me quedé *pensando*.", 96), ("Porque es verdad:", 126), ("llevo años pidiendo lo *mismo*,", 157),
     ("escribiendo *afirmaciones* en un cuaderno,", 169), ("y todo sigue *igual*.", 85)],
    {"texto": "Le pregunté: ¿y qué dice que hay que hacer? Y me contestó: un ritual de siete minutos para despertar esa parte. Que no es religión, ni meditar horas. Él lo muestra en el video.",
     "visual": {"tipo": "zap", "nome": "Vale 🌸", "foto": "👩", "msgs": [
         {"quem": "dela", "txt": "¿Y qué dice que hay que hacer? 🤨", "em": 0.2, "hora": "22:43", "alt": 150},
         {"quem": "dele", "txt": "Un ritual de 7 minutos para despertar esa parte", "em": "un", "hora": "22:44", "alt": 170},
         {"quem": "dele", "txt": "No es religión ni meditar horas 🙌", "em": "religión", "hora": "22:44", "alt": 150},
         {"quem": "dele", "txt": "Él lo muestra en el video 👇", "em": "él", "hora": "22:44"}]},
     "destaques": ["siete", "minutos", "despertar"], "leg_topo": 1040},
    [("Dice que los antiguos cristianos,", "c:monasterio"), ("budistas y egipcios ya lo *hacían*.", "c:buda_cueva"), ("Que cuando esa parte despierta,", 161),
     ("dejas de *perseguir* las cosas,", 99), ("y empiezas a ver *oportunidades*", "c:silueta"), ("que antes no veías.", 95)],
    {"texto": "Yo le dije: suena loco. Y ella: eso pensé yo. Pero son siete minutos. ¿Qué pierdes?",
     "visual": {"tipo": "zap", "nome": "Vale 🌸", "foto": "👩", "msgs": [
         {"quem": "dela", "txt": "Suena loco 😅", "em": "suena", "hora": "22:45", "alt": 130},
         {"quem": "dele", "txt": "Eso pensé yo. Pero son 7 minutos", "em": "eso", "hora": "22:45", "alt": 130},
         {"quem": "dele", "txt": "¿Qué pierdes? 🤷‍♀️", "em": "qué", "hora": "22:45"}]},
     "destaques": ["loco", "siete", "pierdes"], "leg_topo": 1040},
    [("Y tenía razón.", 121), ("Llevo años probando de todo,", 105), ("¿qué son siete *minutos*?", 93), ("Él no promete *magia*.", J),
     ("Habla de calma, de *claridad*,", "c:playa"), ("de dejar de rogar y empezar a *recibir*.", "c:regalo")],
    [("Esa pregunta me *ganó*.", 124), ("Lo vi completo esa misma *noche*.", 115)],
    {"texto": "Si tú también llevas tiempo pidiendo sin respuesta, toca el botón de abajo y mira el video, antes de que lo quiten.",
     "visual": dict(CTA_CARD, fundo="b:153"), "destaques": ["botón", "video", "quiten"], "leg_topo": 900},
])

V["12"] = dict(primary_text="La ley de atracción sí funciona… pero solo si sabes esto. 📡 Un millonario explica la pieza que nadie te contó 👇", blocos=[
    [("Mira, todos conocemos la *teoría*:", 141), ("piensa en lo que quieres,", 136), ("siéntelo, *visualízalo*.", 170),
     ("Y la mayoría lo intenta durante años", 129), ("sin ver *nada*.", 105)],
    T("No es falta de motivación. Ni de disciplina.", [[0, "NO ES <k>MOTIVACIÓN</k>", "#0d0d0d"], ["ni", "NI <k>DISCIPLINA</k>", "#2a0d0d"]]),
    [("Es como tener una radio buena", "c:torres2"), ("con la *antena* desconectada.", "c:torres"),
     ("Puedes subir el *volumen* todo lo que quieras,", 90), ("pero la *señal* no entra.", 91)],
    [("Por eso afirmaciones, visualización y oraciones", 169), ("se quedan en el *aire*.", 126)],
    [("Un millonario lo explica en un video", 88), ("que me dejó *pensando*.", 96), ("La antena es una parte *espiritual* de tu mente,", 109),
     ("la misma que cuidaban los antiguos cristianos,", "c:monasterio"), ("budistas y *egipcios*.", 163)],
    [("Y casi nadie sabe que está *dormida*.", 184), ("Él muestra cómo reconectarla", 161), ("con un ritual de *siete minutos*.", 93),
     ("No necesitas dejar tu *fe*.", 97)],
    [("Ojo: no te promete *magia*.", J), ("Lo que describe es otra forma de vivir:", 95), ("menos *perseguir*,", 99), ("más *recibir*,", "c:regalo"), ("más claridad.", "c:playa")],
    [("Si ya probaste de todo,", 108), ("esta es la *pieza* que nadie te contó.", 119)],
])

V["13"] = dict(primary_text="Los millonarios no trabajan más duro que tú. Tienen encendida una parte de la mente que casi todos tienen apagada. 💡 Mira 👇", blocos=[
    [("Piénsalo.", 96), ("Hay gente que trabaja de sol a sol", 77), ("y no sale de las *deudas*.", 85), ("Y hay gente a la que todo", 141), ("parece llegarle con *calma*.", 110)],
    [("No es *suerte*.", 88), ("Y no siempre es *esfuerzo*.", "c:oficina"), ("Según un millonario que lo cuenta en un *video*,", 104),
     ("la diferencia está en una parte *espiritual*", 80), ("de la mente.", 109)],
    [("En ellos está *encendida*.", 161), ("En casi todos los demás", 127), ("está *apagada* desde hace años.", 115)],
    [("Y con esa parte apagada,", 184), ("rezar, visualizar o repetir frases", 83), ("se siente como empujar una puerta *cerrada*.", 186)],
    [("Él dice que esto lo conocían los *antiguos*,", "c:estatua"), ("y que la *élite* lo guardó para sí misma.", 137)],
    [("Y muestra cómo encenderla", 92), ("con un ritual de *siete minutos*.", 138), ("Sin dejar tu *trabajo*,", 168), ("sin cambiar tus *creencias*.", 97)],
    [("En silencio, desde tu *casa*.", 75)],
    [("¿Y si no funciona contigo?", 124), ("Perdiste siete *minutos*.", 129), ("¿Y si funciona?", 143), ("Vas a entender por qué casi nadie lo *sabe*.", "c:libro")],
    [("No te va a prometer que mañana seas *rico*.", 102), ("Te va a mostrar lo que ellos *saben*", 171), ("y tú no.", 121)],
])

V["14"] = dict(corte=5.40, primary_text="Hace miles de años, en Egipto, los sacerdotes guardaban un secreto sobre una parte de la mente. Hoy un millonario lo explica en un video corto 👇", blocos=[
    [("La escribían en las paredes de los *templos*.", 162), ("La protegían con *rituales*", 163), ("que solo unos pocos podían *aprender*.", 151)],
    [("Siglos después, los monjes *cristianos*", 186), ("hablaban de lo mismo.", "c:monasterio"), ("Y los *budistas* lo enseñaban en silencio.", 154)],
    [("Una parte *espiritual* de la mente.", 119), ("Una *puerta* hacia lo divino.", 80), ("Con el tiempo, ese conocimiento", "c:libro"),
     ("fue quedando fuera de las *enseñanzas*.", "c:estatua")],
    T("Y lo que quedó fue pedir. Pedir, repetir, esperar.",
      [[0, "Y LO QUE QUEDÓ FUE…", "#0d0d0d"], ["pedir.", "<k>PEDIR</k>", "#1a0f12"], ["repetir", "<k>REPETIR</k>", "#0d0d0d"], ["esperar", "<k>ESPERAR</k>", "#1a0f12"]]),
    [("Por eso hoy tanta gente reza", 83), ("sin sentir *respuesta*.", 107), ("Visualiza sin ver *cambios*.", 105), ("Trabaja más y recibe *menos*.", "c:oficina")],
    [("Un millonario asegura que esa parte", 117), ("se puede *despertar*", 161), ("con un ritual corto, de *siete minutos*,", 93),
     ("inspirado en esas tradiciones *antiguas*.", 76)],
    [("Él dice que lo primero que cambia", 95), ("es la sensación de *paz*,", "c:mar"), ("y la claridad para ver *oportunidades*.", "c:silueta")],
    [("Él lo explica en un video que, dicen,", 185), ("no va a durar mucho en *línea*.", 129), ("Lo que los sacerdotes guardaban", 153), ("hoy lo puedes *ver*.", 121)],
    [("No es religión. No es un *curso*.", 175), ("Es una práctica antigua,", "c:redentor"), ("explicada de forma *simple*.", "c:despertar")],
    CTA(155),
])

V["17"] = dict(corte=3.64, primary_text="¿Rezas todas las noches y sientes que nadie te escucha? 🙏 Un millonario explica por qué tu oración no llega. Míralo 👇", blocos=[
    [("Te *entiendo*.", 183), ("Das las *gracias*,", 157), ("pides por los tuyos,", 154), ("pides una *salida*…", 146), ("y te acuestas con la misma *angustia* de siempre.", 184)],
    {"texto": "Y un día terminas buscando en internet por qué tus oraciones no tienen respuesta.",
     "visual": {"tipo": "busca", "consulta": "por qué mis oraciones no tienen respuesta", "digitar_ate": "por",
                "resultados_em": "respuesta", "resultados": [
                    ["foro · preguntas", "Rezo todos los días y nada cambia", "¿Alguien más se siente así?"],
                    ["blog · fe", "Tal vez no es el momento", "Ten paciencia y sigue pidiendo…"]]},
     "destaques": ["internet", "respuesta"], "leg_topo": 1000},
    [("Un millonario lo explica *distinto*", 117), ("en un video corto.", 185), ("Dice que el problema no es tu *fe*.", "c:redentor"),
     ("Es que la parte de tu mente", 109), ("que conecta con lo *divino*", 80), ("está dormida.", 115)],
    [("Es como llamar a alguien", "c:torres2"), ("con la línea *cortada*.", 90), ("Tú hablas, pero nadie *contesta*.", 126)],
    [("Por eso repetir la misma oración cien veces", 150), ("no cambia *nada*.", 108), ("No es falta de *fe*.", "c:joven"),
     ("Es falta de *conexión*.", "c:torres"), ("Y eso tiene *solución*.", 155)],
    [("Los antiguos cristianos, budistas y egipcios", "c:monasterio"), ("despertaban esa parte *antes* de orar.", "c:buda_cueva"),
     ("Él muestra cómo hacerlo hoy,", 161), ("con un ritual de *siete minutos*.", "c:meditar")],
    [("Dice que cuando despierta,", 95), ("la oración se siente *distinta*:", 136), ("con paz, con *certeza*,", "c:mar"), ("sin *rogar*.", 128)],
    [("No tienes que dejar tu iglesia.", 186), ("No tienes que creer en nada *nuevo*.", 97)],
    [("Si esta noche vas a volver a rezar,", 83), ("primero mira este *video*.", 153)],
])

V["18"] = dict(corte=3.70, primary_text="Esto no te lo enseñaron en la iglesia… y no es culpa de nadie. ✝️ Un millonario explica la pieza que se perdió. Mira el video 👇", blocos=[
    [("Durante siglos, una parte de la enseñanza", "c:libro"), ("fue quedando *afuera*.", "c:monasterio"), ("No por *maldad*.", 97), ("Simplemente se *perdió*.", 113)],
    T("Los antiguos cristianos sabían que antes de pedir, había que despertar algo por dentro.",
      [[0, "LOS ANTIGUOS SABÍAN…", "#0d0d0d"], ["antes", "ANTES DE <k>PEDIR</k>", "#101a2e"], ["despertar", "HAY QUE <k>DESPERTAR</k>", "#0d0d0d"]]),
    [("Una parte *espiritual* de la mente.", 119), ("La misma que los budistas cuidaban en *silencio*", 76), ("y que los egipcios dibujaban en sus *templos*.", 151)],
    [("Hoy casi todos rezamos", 83), ("con esa parte *dormida*.", 184), ("Por eso tantas oraciones", 157), ("se sienten *vacías*.", 146)],
    [("No porque no tengas *fe*.", "c:joven"), ("Ni porque Dios no *escuche*.", 154), ("Es que esa parte quedó *apagada*,", 115),
     ("y nadie te enseñó a *encenderla*.", "c:despertar")],
    [("Un millonario lo explica en un video", 103), ("que está *circulando*.", 185), ("Y muestra cómo despertarla", 161), ("con un ritual de *siete minutos*.", 170)],
    [("No va contra tu *iglesia*.", "c:cruz"), ("No te pide dejar *nada*.", 186), ("Te devuelve la *pieza* que faltaba.", 80)],
    [("Cuando esa parte despierta,", 95), ("rezar deja de ser *rogar*.", "c:barba"), ("Se vuelve una *conversación*.", 128)],
    [("Él no promete *milagros*.", 102), ("Habla de *paz*,", "c:mar"), ("de claridad,", 141), ("de dejar de vivir con *miedo*.", 152),
     ("Y son solo *siete minutos*.", 93)],
    [("Si sientes que tus oraciones no llegan,", 126), ("míralo antes de que lo *quiten*.", "c:reloj")],
])

V["19"] = dict(primary_text="¿Sabías que hay un ritual de 7 minutos que los millonarios no quieren que conozcas? 🤫 Míralo mientras sigue disponible 👇", blocos=[
    [("Yo tampoco lo *sabía*.", 122), ("Lo vi en un video de un millonario", 185), ("que decidió *contarlo* todo.", 117)],
    [("Él dice que la mayoría intenta atraer *abundancia*", "c:billete_vuela"), ("de la forma *equivocada*:", 108), ("pidiendo,", 157), ("visualizando,", 136),
     ("repitiendo frases frente al *espejo*.", 169)],
    [("Y que nada de eso funciona", 105), ("si una parte de tu mente está *dormida*.", 184), ("Una parte *espiritual*", 119), ("que los antiguos llamaban", "c:estatua"),
     ("la conexión con lo *divino*.", 114)],
    [("El ritual es para *despertarla*.", 89), ("Siete minutos.", 93), ("En *silencio*.", 170), ("Desde tu casa.", 75)],
    [("Sin velas, sin cursos, sin *complicaciones*.", 141)],
    [("¿Por qué no quieren que lo *conozcas*?", 171), ("Porque si todos lo supieran,", 127), ("dejaría de ser una *ventaja*.", 142)],
    [("Él cuenta que lo primero que cambia", 95), ("es esa sensación de estar siempre *corriendo*", 99), ("detrás de todo.", 152), ("Dejas de *perseguir*.", "c:playa"),
     ("Empiezas a *atraer*.", "c:silueta")],
    [("No es religión ni meditación de horas.", 186), ("Y no tienes que creer en nada para *verlo*.", J)],
    [("Míralo hoy,", 161), ("mientras sigue *disponible*.", 129)],
])

V["20"] = dict(primary_text="Suena loco, pero escúchame hasta el final. 👀 Un millonario cuenta que todo empezó al despertar una parte de su mente 👇", blocos=[
    [("Hay un millonario que nunca muestra la *cara*.", 88), ("Y en un video cuenta de dónde salió", 104), ("todo lo que *tiene*.", 137),
     ("Dice que no fue por trabajar más *duro*,", 77), ("ni por *suerte*.", 86)],
    T("Fue por activar una parte de su mente que estaba dormida.",
      [[0, "NO FUE <k>SUERTE</k>", "#0d0d0d"], ["activar", "FUE <k>ACTIVAR</k>", "#101a2e"], ["dormida", "ALGO <k>DORMIDO</k>", "#0d0d0d"]]),
    [("Una parte *espiritual*", 109), ("que casi todos tenemos *apagada*.", 115), ("Por eso rezamos,", 83), ("pedimos, *visualizamos*…", "c:barba"),
     ("y seguimos en el mismo *lugar*.", 152)],
    [("Él dice que los antiguos lo *sabían*.", 163), ("Que los cristianos, los budistas y los egipcios", 150), ("tenían formas de *despertarla*.", 161)],
    [("Y que hoy se puede hacer", 95), ("con *tres pasos* sencillos", 112), ("y un ritual de siete minutos.", 138)],
    [("Y desde tu *casa*.", 75)],
    [("No es una religión.", 186), ("No tienes que dejar tu *fe*.", 97), ("Es solo una forma distinta de *despertar*.", "c:despertar")],
    [("Ya sé: suena *loco*.", 123), ("Te lo dije al principio.", 96), ("Pero piensa:", 124), ("¿cuánto tiempo llevas haciendo lo mismo,", 129),
     ("esperando algo *distinto*?", 108)],
    [("Siete minutos no son *nada*.", "c:reloj"), ("Míralo hasta el *final*,", "c:silueta"), ("como te pedí.", 187)],
])



# grupos de sentido para espalhar as imagens entre os vídeos (troca só dentro do mesmo tema)
GRUPOS = [
    ["b:161", "b:92", "b:80", "b:119", "b:89", "b:128", "b:114", "b:109", "b:153", "c:despertar", "b:90", "b:91",
     "b:95", "b:82", "b:145", "c:cruz"],
    ["b:184", "b:105", "b:106", "b:107", "b:108", "b:146", "b:152", "b:183", "b:85"],
    ["b:157", "b:83", "b:154", "c:barba", "b:76", "b:150"],
    ["b:186", "c:cruz", "b:97", "c:redentor"],
    ["b:95", "b:136", "b:141", "b:110", "b:82", "c:mar", "c:playa", "b:172", "b:145", "b:155", "b:75", "b:94"],
    ["b:129", "b:93", "b:112", "b:113", "c:reloj"],
    ["b:96", "b:124", "b:185", "b:126"],
    ["b:121", "b:122", "b:143", "b:187", "b:123"],
    ["c:monasterio", "c:estatua", "c:libro", "b:162", "b:163", "b:151", "c:buda_cueva"],
    ["b:138", "b:170", "b:136"],
    ["b:99", "b:94", "b:172", "b:82"],
    ["b:115", "b:153"],
]
LIMITE = 7
# cortes que, sem a legenda antiga (só a parte de cima), ficam vazios ou com rosto cortado: trocados por imagem do mesmo tema
PROIBIDOS = {"c:torres": 0, "c:torres2": 0, "c:joven": 6, "c:meditar": 9, "c:montana": 11, "c:silueta": 4,
             "c:redentor": 3, "c:regalo": 4}
# trechos úteis de clipes do banco (o resto fica escuro ou vazio)
LIMITES = {"b:161": [0.0, 4.6], "b:185": [0.0, 3.0]}
FIXOS = {"b:169"}  # afirmações escritas: sem substituto com o mesmo sentido


def trocar_proibidos(crs):
    from collections import Counter
    cont = Counter(p[1] for c in crs for b in c["blocos"] for p in b.get("partes", []))
    out = []
    for c in crs:
        no_video = {p[1] for b in c["blocos"] for p in b.get("partes", [])}
        for b in c["blocos"]:
            for p in b.get("partes", []):
                if p[1] in PROIBIDOS:
                    cands = [x for x in GRUPOS[PROIBIDOS[p[1]]] if x not in no_video] or \
                            [x for x in GRUPOS[0] if x not in no_video]
                    novo = min(cands, key=lambda x: cont[x])
                    cont[novo] += 1; no_video.add(novo)
                    out.append(f"{c['id']}: '{p[0]}' {p[1]}->{novo}")
                    p[1] = novo
    return out


def balancear(crs):
    """Troca usos em excesso (> LIMITE no lote) por outra imagem do mesmo grupo, sem repetir dentro do vídeo."""
    from collections import Counter
    cont = Counter(p[1] for c in crs for b in c["blocos"] for p in b.get("partes", []))
    trocas = []
    for c in reversed(crs):
        no_video = {p[1] for b in c["blocos"] for p in b.get("partes", [])}
        for b in c["blocos"]:
            for p in b.get("partes", []):
                k = p[1]
                if cont[k] <= LIMITE or k in FIXOS:
                    continue
                cands = [x for g in GRUPOS if k in g for x in g if x != k and x not in no_video and cont[x] < LIMITE]
                if not cands:
                    continue
                novo = min(cands, key=lambda x: cont[x])
                cont[k] -= 1; cont[novo] += 1
                no_video.discard(k); no_video.add(novo)
                trocas.append(f"{c['id']}: '{p[0]}' {k}->{novo}")
                p[1] = novo
    return trocas


def chave(c):
    return f"b:{c}" if isinstance(c, int) else c


def limpa(frase):
    dest = [w.lower().strip("¿¡,.:;…\"") for x in re.findall(r"\*([^*]+)\*", frase) for w in x.split()]
    return frase.replace("*", ""), dest


# início do fechamento com avatar no vídeo atual (troca de cena conferida nos quadros); cauda = duração - início
INICIO_CTA = {"01": 34.20, "02": 26.00, "03": 28.65, "04": 28.95, "05": 30.02, "06": 29.55, "07": 26.37, "09": 28.22,
              "10": 30.80, "12": 34.37, "13": 31.79, "17": 26.58, "18": 26.90, "19": 31.85, "20": 30.23}


def meta_avatar(clipe):
    m = json.load(open(os.path.join(HEYGEN, clipe + ".json")))
    return min(m["duracao"], m["palavras"][-1]["fim"] + 0.25)


def main():
    crs, uso = [], {}
    for cr in BASE["criativos"]:
        i = cr["id"]
        if i in DESCARTADOS:
            continue
        v = V[i]
        g = cr["gancho"]
        if "corte" in v:
            corte = v["corte"]
        elif g["tipo"] == "avatar":
            corte = round(meta_avatar(g["clipe"]) - 0.04, 2)
        elif g["tipo"] == "campeao":
            corte = round(g["corte"][2] - g["corte"][1] - 0.04, 2)
        elif g["tipo"] == "chat":
            corte = 5.45
        cauda = v.get("cauda")
        if cauda is None and i in INICIO_CTA:
            orig = os.path.join(F.WORK, "ca-orig", f"{i}.mp4")
            cauda = round(F.duracao(orig) - INICIO_CTA[i] - 0.02, 2)
        blocos = []
        for b in v["blocos"]:
            if isinstance(b, dict):
                bb = dict(b)
                bb.setdefault("voz", cr["voz"])
                if "destaques" not in bb:
                    bb["destaques"] = []
                blocos.append(bb)
                f = bb["visual"].get("fundo")
                if f:
                    uso.setdefault(f, []).append(i)
                continue
            partes, dest = [], []
            for frase, c in b:
                t, d = limpa(frase)
                partes.append([t, chave(c)])
                dest += d
                uso.setdefault(chave(c), []).append(i)
            blocos.append({"voz": cr["voz"], "partes": partes, "destaques": dest})
        crs.append({"id": i, "formato": cr["formato"], "angulo": cr["angulo"], "corte": corte,
                    **({"cauda": cauda} if cauda else {}), "voz": cr["voz"],
                    "primary_text": v["primary_text"], "blocos": blocos})
    for t in trocar_proibidos(crs):
        print("  proibido", t)
    for t in balancear(crs):
        print("  troca", t)
    uso = {}
    for c in crs:
        for b in c["blocos"]:
            for p in b.get("partes", []):
                uso.setdefault(p[1], []).append(c["id"])
            if b.get("visual", {}).get("fundo"):
                uso.setdefault(b["visual"]["fundo"], []).append(c["id"])
    plano = {
        "produto": "codigo-alfa", "titulo": "Código Alfa · Lote 1 (reeditado: mínimo 1 min)",
        "obs": "Gancho original intacto, corpo e final novos (VSL), fechamento com o avatar já pago. Sem HeyGen novo: só TTS grátis.",
        "origem": "codigo-alfa/lotes/2026-11-08/codigo-alfa-lote-1-{id}.mp4",
        "banco": "banco/indice.json", "limites": LIMITES, "vozes": BASE["vozes"], "campeoes": BASE["campeoes"],
        "brolls": {k: v + ["alto"] for k, v in CORTES.items()}, "criativos": crs}
    json.dump(plano, open(os.path.join(AQUI, "codigo-alfa-lote-1-v2.json"), "w"), ensure_ascii=False, indent=1)
    rep = sorted(uso.items(), key=lambda x: -len(x[1]))
    print("clipes mais usados:", " ".join(f"{k}x{len(v)}" for k, v in rep[:25]))
    print("clipes distintos:", len(uso), "| usos:", sum(len(v) for v in uso.values()))
    for c in crs:
        dup = [k for k, n in __import__("collections").Counter(
            p[1] for b in c["blocos"] for p in b.get("partes", [])).items() if n > 1]
        print(c["id"], "corte", c["corte"], "cauda", c.get("cauda"), "dup!" if dup else "", dup or "")


if __name__ == "__main__":
    main()
