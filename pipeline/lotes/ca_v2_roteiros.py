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
CORTES = {
    "regalo": ["k2", 23.5, 27.9], "billetera": ["k2", 28.0, 29.9], "rubia": ["k2", 30.0, 32.9],
    "reloj": ["k2", 33.0, 35.9], "playa": ["k2", 41.0, 42.9], "barba": ["k2", 43.0, 44.9],
    "joven": ["k2", 45.0, 47.9], "libro": ["k2", 59.0, 60.9], "meditar": ["k2", 70.0, 71.9],
    "champan": ["k2", 77.0, 78.9], "mar": ["k2", 85.0, 86.9], "silueta": ["k2", 92.0, 95.9],
    "montana": ["k3", 5.0, 6.9], "redentor": ["k3", 12.0, 15.9], "buda_cueva": ["k3", 16.0, 20.9],
    "torres": ["k3", 21.0, 26.9], "torres2": ["k3", 27.0, 30.9], "cruz": ["k3", 37.0, 39.9],
    "monasterio": ["k3", 45.0, 48.9], "estatua": ["k3", 63.0, 66.9], "brindis": ["k3", 78.0, 81.9],
    "oficina": ["k4", 5.0, 6.9], "tablet": ["k4", 23.0, 24.9], "billete_vuela": ["k4", 59.0, 60.9],
    "pareja": ["k4", 61.0, 62.9], "multitud": ["k4", 69.0, 72.9], "despertar": ["k1", 59.0, 60.9],
}

CTA_CARD = {"tipo": "cta", "sobre": "VIDEO CORTO", "titulo": "EL VIDEO DEL<br>MILLONARIO", "botao": "MIRA EL VIDEO ↓"}

V = {}  # id -> {"voz":..., "corte": s (gancho não-avatar), "blocos": [...], "primary_text": ...}

V["01"] = dict(primary_text="Ella llevaba años pidiendo y nada cambiaba… hasta que vio un video extraño de un millonario. 😳 Míralo antes de que lo quiten 👇", blocos=[
    [("Ella no estaba haciendo nada *raro*.", 140), ("Llevaba años pidiendo, repitiendo *afirmaciones*", 169),
     ("y visualizando la vida que quería.", 136), ("Y cada mes, lo mismo: cuentas, *estrés*, cansancio.", 105)],
    [("Hasta que una noche vio un video *extraño*.", 5), ("Un millonario que nunca muestra la cara", 2),
     ("explica por qué a la mayoría no le *funciona* nada de eso.", 108)],
    [("Dice que hay una parte *espiritual* de la mente", 161),
     ("que los antiguos cristianos, budistas y egipcios cuidaban como un *tesoro*.", "c:monasterio"),
     ("Y que en casi todos nosotros está *dormida*.", 184)],
    [("Si esa parte está apagada, puedes rezar o visualizar mil veces,", 83),
     ("y es como hablar por un teléfono *sin señal*.", 22)],
    [("Él muestra un ritual de *siete minutos* para despertarla.", 138),
     ("Sin cursos, sin meditar horas, sin cambiar de *religión*.", 170)],
    [("Ella cuenta que lo primero que notó fue *calma*.", 95), ("Dejó de perseguir las cosas con *desesperación*", 145),
     ("y empezó a ver *oportunidades* que antes no veía.", "c:silueta")],
    [("¿Suena raro? Sí. A mí también me sonó *raro*.", 96),
     ("Pero son siete minutos. Si no es para ti, solo pierdes *siete minutos*.", 129),
     ("¿Y si es justo la *pieza* que te faltaba?", 80)],
])

V["02"] = dict(primary_text="No te digo que dejes a Dios. Te digo que dejes de rogar como si no te escuchara. 🙏 Mira el video antes de que lo quiten 👇", blocos=[
    [("Sí, escuchaste bien.", "c:joven"), ("No te digo que dejes a *Dios*.", "c:redentor"),
     ("Te digo que dejes de *rogar* como si Él no te escuchara.", 156)],
    [("Piénsalo. Cuando ruegas por una *bendición*,", 157), ("le estás repitiendo a tu mente lo que te *falta*.", 188),
     ("Y la mente se queda mirando la *falta*.", 152)],
    {"texto": "Los antiguos cristianos hacían algo distinto. Primero despertaban algo por dentro, y después pedían.",
     "visual": {"tipo": "texto", "legenda": False, "frases": [[0, "LOS ANTIGUOS <k>CRISTIANOS</k>", "#0d0d0d"],
                ["primero", "PRIMERO <k>DESPIERTAS</k>", "#101a2e"], ["después", "DESPUÉS <k>PIDES</k>", "#0d0d0d"]]}},
    [("En un video que está dando vueltas,", 140), ("un millonario que no muestra la cara explica esa parte *olvidada*:", "c:libro"),
     ("una parte *espiritual* de la mente que casi nadie usa.", 119)],
    [("Él dice que cuando se *enciende*,", 161), ("dejas de perseguir y empiezas a *recibir* con calma.", "c:mar"),
     ("Las puertas correctas aparecen, las personas correctas *llegan*.", "c:pareja")],
    [("No es una religión nueva. No tienes que dejar tu *fe*.", 97),
     ("Es un ritual corto, de *siete minutos*, que puedes hacer en casa.", 138)],
    [("Si después de verlo no te hace sentido, no pierdes *nada*.", 124),
     ("Pero si tiene razón, cada día que sigues rogando es un día *perdido*.", "c:reloj")],
])

V["03"] = dict(primary_text="Dicen que intentaron borrar este video. Un millonario explica la parte de la mente que casi nadie usa. 🤫 Mírelo antes de que lo quiten 👇", blocos=[
    [("Y no, no es un video de *motivación*.", 173), ("Es un hombre que se volvió *millonario* y que nunca muestra la cara.", 117)],
    [("Él cuenta algo que, según dice, la *élite* conoce hace mucho tiempo", 142),
     ("y que fue *borrado* de las enseñanzas espirituales.", "c:estatua")],
    [("Por eso usted reza, repite *afirmaciones*, visualiza…", 83), ("y siente que todo se queda en el *aire*.", 126)],
    [("Según él, no es falta de *fe* ni de esfuerzo.", 77), ("Es que hay una parte de la mente que está *dormida*,", 184),
     ("y mientras duerme, nada de eso tiene a dónde *llegar*.", 153)],
    [("Él muestra cómo despertarla con *tres pasos* sencillos.", 169), ("Sin cursos caros, sin horas de *meditación*.", 170),
     ("Lo primero que cambia es la forma de ver las cosas: con más *calma* y más claridad.", 82)],
    [("Yo pensé que era otro video más.", 96), ("Pero lo vi completo, y entendí por qué lo quieren *quitar*.", 121)],
    [("Si usted también siente que hace todo bien y *nada cambia*,", 85), ("no lo deje para *después*.", 129)],
])

V["04"] = dict(primary_text="Son las 3 de la mañana y no puedo dejar de pensar en lo que dijo este millonario… 🌙 Míralo antes de dormir 👇", blocos=[
    {"texto": "Me lo mandaron hace unas horas, con un mensaje que decía: tienes que ver esto.",
     "visual": {"tipo": "bloqueio", "hora": "3:07", "data": "madrugada", "notifs": [
         {"de": "Caro", "txt": "Tienes que ver esto 😳 es el video del millonario", "em": "tienes", "quando": "hace 3 h"}]},
     "destaques": ["ver", "esto"], "leg_topo": 900},
    [("Él dice algo que no me deja de dar *vueltas*:", 5), ("que la gente buena trabaja más, reza más, se *esfuerza* más…", "c:oficina"),
     ("y aun así se queda con *menos*.", 79)],
    [("Y que no es *culpa* de ellos.", 106), ("Que hay una parte de la mente, una parte *espiritual*,", 109),
     ("que en casi todos está *apagada*.", 115)],
    [("Y mientras está apagada, puedes pedir, visualizar y repetir frases,", 169), ("pero es como sembrar en tierra *seca*.", 87)],
    [("Lo que él explica es cómo *encenderla*.", 161), ("Un ritual de *siete minutos*, que se hace en silencio, en casa.", 138)],
    [("Él dice que después de eso dejas de *perseguir* las cosas,", 99),
     ("y empiezas a notar *oportunidades* que antes pasaban frente a ti.", "c:multitud")],
    [("Yo sé que suena raro a esta hora.", 184),
     ("Pero si este video te apareció de *madrugada*, no creo que sea casualidad.", 2), ("Míralo antes de *dormir*.", 153)],
])

V["05"] = dict(primary_text="Si este video te apareció hoy, no es coincidencia. ✨ Un millonario explica por qué tus pedidos no llegan. Míralo 👇", blocos=[
    [("Llevas mucho tiempo pidiendo una *señal*.", 155), ("Rezando, escribiendo lo que quieres, *imaginando* otra vida.", 124),
     ("Y sientes que el universo no te *contesta*.", 58)],
    [("Hace poco vi un video de un *millonario* que explica por qué.", 176), ("Dice que el problema no es el *universo*.", 114),
     ("Es que la parte de tu mente que recibe esas señales está *dormida*.", 92)],
    {"texto": "Se lo mandé a mi hermana, y en dos minutos me contestó: esto es justo lo que me pasaba.",
     "visual": {"tipo": "zap", "nome": "Hermana 💛", "foto": "👩", "msgs": [
         {"quem": "dela", "txt": "Mira este video 👀 dura poquito", "em": 0.2, "hora": "18:02", "alt": 150},
         {"quem": "dele", "txt": "Esto es justo lo que me pasaba 😳", "em": "esto", "hora": "18:04"}]},
     "destaques": ["hermana", "justo"], "leg_topo": 1000},
    [("Él cuenta que los antiguos cristianos, budistas y egipcios *cuidaban* esa parte.", "c:buda_cueva"),
     ("La llamaban una línea directa con lo *divino*.", 80)],
    [("Y que se puede despertar con un ritual de *siete minutos*.", 93),
     ("Cuando despierta, dejas de forzar y empiezas a ver las *puertas* que se abren.", 95)],
    [("Tal vez pienses: otra cosa más que no va a *funcionar*.", 108), ("Por eso no te pido que creas. Te pido que lo *veas*.", 81)],
    [("Si llegaste hasta aquí, ya sabes que no fue *coincidencia*.", 143)],
])

V["06"] = dict(primary_text="Rezar por dinero es repetirle a su mente lo que le falta. 🙏 Un millonario explica el error que casi todos cometen. Mírelo 👇", blocos=[
    [("Cuando usted le pide *dinero* a Dios todas las noches,", 157),
     ("sin querer está repitiendo una sola idea: no tengo, me *falta*.", 188), ("Y eso es lo que su mente *escucha*.", 96)],
    {"texto": "Pedir dinero es pensar en lo que falta. Y la mente se queda donde está su atención.",
     "visual": {"tipo": "texto", "legenda": False, "frases": [[0, "PEDIR <k>DINERO</k>", "#0d0d0d"],
                ["pensar", "= PENSAR EN LO QUE <k>FALTA</k>", "#2a0d0d"], ["mente", "LA MENTE SE QUEDA <k>AHÍ</k>", "#0d0d0d"]]}},
    [("Lo vi en un video de un *millonario* que lo explica mejor que nadie.", 176),
     ("Él dice que hay una parte *espiritual* de la mente que está dormida en casi todos.", 119),
     ("Y que mientras duerme, rezar por dinero es como hablar en un cuarto *cerrado*.", 106)],
    [("Los antiguos sabían despertarla *primero*, y recién después agradecer y pedir.", 154)],
    [("Él enseña cómo hacerlo con un ritual de *siete minutos*.", 113),
     ("En silencio, sin cursos, sin cambiar sus *creencias*.", 136)],
    [("Lo primero que cambia no es su cuenta del *banco*.", 101), ("Es usted: más *calma*, más claridad,", 141),
     ("y menos miedo cuando llegan las *cuentas*.", 132)],
    [("Si le suena raro, está bien. A mí también.", 124),
     ("Pero son solo siete minutos, y puede cambiar la forma en que usted *reza*.", "c:barba")],
])

V["07"] = dict(primary_text="Dios no es el problema. Tu fe no es el problema. El problema es desde dónde pides. 🙏 Mira el video 👇", blocos=[
    [("Antes de que te enojes, *escúchame*.", "c:joven"), ("Dios no es el problema. Tu *fe* no es el problema.", "c:redentor")],
    [("El problema es desde *dónde* pides.", 83), ("Si pides desde el *miedo*, tu oración nace cansada.", 152),
     ("Si pides desde la *desesperación*, la respuesta parece no llegar nunca.", 146)],
    {"texto": "Hay una antena espiritual dentro de ti. Y en casi todos está desconectada.",
     "visual": {"tipo": "texto", "legenda": False, "frases": [[0, "HAY UNA <k>ANTENA</k>", "#0d0d0d"],
                ["dentro", "DENTRO DE <k>TI</k>", "#101a2e"], ["desconectada", "<k>DESCONECTADA</k>", "#2a0d0d"]]}},
    [("Un millonario lo explica en un *video* corto.", 25), ("Dice que esa parte se puede volver a *conectar*", "c:torres"),
     ("con un ritual de *siete minutos*, en silencio, en tu casa.", 170)],
    [("Y cuando se conecta, dejas de *mendigar* y empiezas a recibir.", "c:regalo"),
     ("Las ideas llegan, las *puertas* se abren, la paz vuelve.", 128)],
    [("No tienes que dejar tu iglesia ni tu *fe*.", 156), ("Es al revés: tu oración por fin va a tener a dónde *llegar*.", 52)],
    [("Si sientes que llevas años *pidiendo*, mira esto hoy.", 112)],
])

V["08"] = dict(primary_text="Jesús, Tesla y Buda hablaron del mismo secreto con palabras distintas. 🔱 Un millonario lo reunió en un video corto. Míralo 👇", blocos=[
    [("Un maestro en *Galilea*.", "c:redentor"), ("Un príncipe que dejó todo para *meditar*.", "c:buda_cueva"),
     ("Un inventor obsesionado con la *energía*.", "c:torres")],
    [("Los tres hablaron de lo *mismo* con palabras diferentes:", "c:libro"), ("energía, *frecuencia*, una luz interior.", 89)],
    [("Y los tres apuntaban a una parte de nosotros que casi *nadie* usa.", 109),
     ("Una parte *espiritual* de la mente, que los antiguos llamaban el tercer ojo.", 119)],
    [("Hoy la mayoría reza, visualiza y repite *afirmaciones*", 83), ("con esa parte completamente *dormida*.", 115),
     ("Por eso sienten que *nada* llega.", 53)],
    [("Un millonario que prefiere no mostrar su *rostro*", 2), ("reunió esas enseñanzas en un video *corto*,", 78),
     ("y muestra un ritual de *siete minutos* para despertar esa parte.", "c:estatua")],
    [("No es una religión. No es un *curso*.", "c:monasterio"),
     ("Es algo que, según él, fue sacado de las enseñanzas a *propósito*.", 162)],
    [("Si sientes *curiosidad*, no lo dejes para mañana.", 153),
     ("Dicen que no va a estar *disponible* por mucho tiempo.", 129)],
    {"texto": "Toca el botón de abajo y mira el video corto, antes de que lo quiten.",
     "visual": dict(CTA_CARD, fundo="b:142"), "destaques": ["botón", "video", "quiten"], "leg_topo": 900},
])

V["09"] = dict(primary_text="\"El reino de Dios está dentro de ti.\" Casi nadie entendió lo que significaba. 🙏 Un millonario lo explica en este video 👇", blocos=[
    [("Nos enseñaron a buscar a Dios *afuera*.", 156), ("En el cielo, en un templo, en una oración repetida mil *veces*.", 186)],
    [("Pero Jesús dijo *dentro*.", 97), ("Y los antiguos cristianos lo tomaban *literal*:", "c:monasterio"),
     ("hay una parte de ti que conecta con lo *divino*.", 80)],
    [("Los budistas la cuidaban en *silencio*.", 150), ("Los egipcios la dibujaban en sus *templos*.", 151),
     ("Todos hablaban de lo *mismo*.", 109)],
    [("Un millonario explica en un video por qué esa parte está *dormida* en casi todos", 134),
     ("y por qué las oraciones parecen no *llegar*.", 107)],
    {"texto": "No se trata de pedir más. Se trata de despertar lo que ya está dentro.",
     "visual": {"tipo": "texto", "legenda": False, "frases": [[0, "NO ES PEDIR <k>MÁS</k>", "#0d0d0d"],
                ["despertar", "ES <k>DESPERTAR</k>", "#101a2e"], ["dentro", "LO QUE YA ESTÁ <k>DENTRO</k>", "#0d0d0d"]]}},
    [("Él muestra un ritual de *siete minutos* para hacerlo, en silencio, en casa.", "c:meditar"),
     ("No reemplaza tu fe. La *completa*.", 83)],
    [("Según él, cuando esa parte despierta vives con más *paz*,", "c:mar"),
     ("y empiezas a ver tu camino con otros *ojos*.", 99)],
    [("Si ese versículo siempre te tocó el *corazón*, tienes que ver esto.", 136)],
])

V["10"] = dict(primary_text="La ley de atracción funciona para unos pocos. Un millonario revela la pieza que falta. 🧲 Mira el video corto 👇", blocos=[
    [("Y no es porque ellos trabajen *más*.", "c:oficina"), ("Ni porque sean más inteligentes, ni porque tengan más *suerte*.", 175)],
    {"texto": "Si buscas por qué no te funciona, vas a encontrar lo de siempre: piensa positivo, visualiza, repite afirmaciones.",
     "visual": {"tipo": "busca", "consulta": "por qué no me funciona la ley de atracción", "digitar_ate": "vas",
                "resultados_em": "piensa", "resultados": [
                    ["blog · consejos", "Piensa positivo todos los días", "Cambia tus pensamientos y todo cambiará…"],
                    ["video · 12 min", "Visualiza tu vida ideal", "Imagina con detalle lo que quieres…"],
                    ["foro · preguntas", "Lo hice todo y nada cambia", "¿A alguien más le pasa?"]]},
     "destaques": ["siempre", "positivo", "afirmaciones"], "leg_topo": 1000},
    [("Pero nadie te dice la *pieza* que falta.", 161), ("Un millonario la explica en un video *corto*:", 140),
     ("hay una parte *espiritual* en el centro de la mente", "c:tablet"),
     ("que en la mayoría de las personas está *dormida*.", "c:multitud")],
    [("Con esa parte apagada, visualizar es como mandar una carta sin *dirección*.", 124)],
    [("Él muestra *tres pasos* sencillos y un ritual de siete minutos para despertarla.", 138)],
    [("No necesitas creer en nada *nuevo* ni dejar tu fe.", 154), ("Solo siete minutos y la mente *abierta*.", 93)],
    [("Lo que cambia es cómo te sientes: sin *perseguir*, sin forzar, en paz con lo que viene.", 110)],
    [("Si eres de \"todos los *demás*\", este video es para ti.", 8)],
])

V["11"] = dict(cauda=0, primary_text="Mi amiga me mandó este video anoche… 😳 Dice que hay una parte de la mente que está dormida. Míralo antes de que lo borren 👇", blocos=[
    {"texto": "Sí. Dice que hay una parte de la mente que está dormida, y que por eso rezamos, pedimos, y nada cambia.",
     "visual": {"tipo": "zap", "nome": "Vale 🌸", "foto": "👩", "topo": 200, "msgs": [
         {"quem": "dele", "txt": "¿Viste el video que te mandé? 😳", "em": 0, "hora": "22:41", "alt": 130},
         {"quem": "dela", "txt": "¿El del millonario? 🤔", "em": 0, "hora": "22:41", "alt": 130},
         {"quem": "dele", "txt": "Sí. Dice que hay una parte de la mente que está dormida", "em": "dice", "hora": "22:42", "alt": 170},
         {"quem": "dele", "txt": "y que por eso rezamos, pedimos y nada cambia 🙏", "em": "rezamos", "hora": "22:42"}]},
     "destaques": ["dormida", "rezamos", "nada"], "leg_topo": 1040},
    [("Me quedé *pensando*. Porque es verdad:", 140), ("llevo años pidiendo lo *mismo*,", 53),
     ("escribiendo *afirmaciones* en un cuaderno,", 169), ("y todo sigue *igual*.", 85)],
    {"texto": "Le pregunté: ¿y qué dice que hay que hacer? Y me contestó: un ritual de siete minutos para despertar esa parte. Él lo muestra en el video.",
     "visual": {"tipo": "zap", "nome": "Vale 🌸", "foto": "👩", "msgs": [
         {"quem": "dela", "txt": "¿Y qué dice que hay que hacer? 🤨", "em": 0.2, "hora": "22:43", "alt": 150},
         {"quem": "dele", "txt": "Un ritual de 7 minutos para despertar esa parte", "em": "un", "hora": "22:44", "alt": 170},
         {"quem": "dele", "txt": "Él lo muestra en el video 👇", "em": "él", "hora": "22:44"}]},
     "destaques": ["siete", "minutos", "despertar"], "leg_topo": 1040},
    [("Dice que los antiguos cristianos, budistas y egipcios ya lo *hacían*.", "c:buda_cueva"),
     ("Que cuando esa parte despierta, dejas de *perseguir* las cosas,", 99),
     ("y empiezas a ver *oportunidades* que antes no veías.", "c:silueta")],
    {"texto": "Yo le dije: suena loco. Y ella: eso pensé yo. Pero son siete minutos. ¿Qué pierdes?",
     "visual": {"tipo": "zap", "nome": "Vale 🌸", "foto": "👩", "msgs": [
         {"quem": "dela", "txt": "Suena loco 😅", "em": "suena", "hora": "22:45", "alt": 130},
         {"quem": "dele", "txt": "Eso pensé yo. Pero son 7 minutos", "em": "eso", "hora": "22:45", "alt": 130},
         {"quem": "dele", "txt": "¿Qué pierdes? 🤷‍♀️", "em": "qué", "hora": "22:45"}]},
     "destaques": ["loco", "siete", "pierdes"], "leg_topo": 1040},
    [("Esa pregunta me *ganó*.", 96), ("Lo vi completo esa misma *noche*.", 5)],
    {"texto": "Si tú también llevas tiempo pidiendo sin respuesta, toca el botón de abajo y mira el video, antes de que lo quiten.",
     "visual": dict(CTA_CARD, fundo="b:153"), "destaques": ["botón", "video", "quiten"], "leg_topo": 900},
])

V["12"] = dict(primary_text="La ley de atracción sí funciona… pero solo si sabes esto. 📡 Un millonario explica la pieza que nadie te contó 👇", blocos=[
    [("Mira, todos conocemos la *teoría*:", 78), ("piensa en lo que quieres, siéntelo, *visualízalo*.", 136),
     ("Y la mayoría lo intenta durante años sin ver *nada*.", 125)],
    {"texto": "No es falta de motivación. Ni de disciplina.",
     "visual": {"tipo": "texto", "legenda": False, "frases": [[0, "NO ES <k>MOTIVACIÓN</k>", "#0d0d0d"],
                ["ni", "NI <k>DISCIPLINA</k>", "#2a0d0d"]]}},
    [("Es como tener una radio buena con la *antena* desconectada.", "c:torres2"),
     ("Puedes subir el *volumen* todo lo que quieras,", 90), ("pero la *señal* no entra.", 91)],
    [("Un millonario lo explica en un video que me dejó *pensando*.", 134),
     ("La antena es una parte *espiritual* de tu mente,", 109),
     ("la misma que cuidaban los antiguos cristianos, budistas y *egipcios*.", 163)],
    [("Y casi nadie sabe que está *dormida*.", 184), ("Él muestra cómo reconectarla con un ritual de *siete minutos*.", 170)],
    [("Ojo: no te promete *magia*.", "c:joven"),
     ("Lo que describe es otra forma de vivir: menos perseguir, más *recibir*, más claridad.", "c:playa")],
    [("Si ya probaste de todo, esta es la *pieza* que nadie te contó.", 161)],
])

V["13"] = dict(primary_text="Los millonarios no trabajan más duro que tú. Tienen encendida una parte de la mente que casi todos tienen apagada. 💡 Mira 👇", blocos=[
    [("Piénsalo.", 96), ("Hay gente que trabaja de sol a sol y no sale de las *deudas*.", 38),
     ("Y hay gente a la que todo parece llegarle con *calma*.", 141)],
    [("No es *suerte*. Y no siempre es esfuerzo.", 188), ("Según un millonario que lo cuenta en un *video*,", 176),
     ("la diferencia está en una parte *espiritual* de la mente.", 80)],
    [("En ellos está *encendida*.", 161), ("En casi todos los demás está *apagada* desde hace años.", 115)],
    [("Y con esa parte apagada, rezar, visualizar o repetir frases", 156), ("se siente como empujar una puerta *cerrada*.", 186)],
    [("Él dice que esto lo conocían los *antiguos*,", "c:estatua"), ("y que la *élite* lo guardó para sí misma.", 137)],
    [("Y muestra cómo encenderla con un ritual de *siete minutos*.", 92), ("Sin dejar tu trabajo, sin cambiar tus *creencias*.", 168)],
    [("No te va a prometer que mañana seas *rico*.", 102), ("Te va a mostrar lo que ellos *saben* y tú no.", 121)],
])

V["14"] = dict(corte=5.40, primary_text="Hace miles de años, en Egipto, los sacerdotes guardaban un secreto sobre una parte de la mente. 𓂀 Hoy un millonario lo explica en un video corto 👇", blocos=[
    [("La escribían en las paredes de los *templos*.", 162), ("La protegían con rituales que solo unos pocos podían *aprender*.", 163)],
    [("Siglos después, los monjes *cristianos* hablaban de lo mismo.", 186), ("Y los *budistas* lo enseñaban en silencio.", 154)],
    [("Una parte *espiritual* de la mente, una puerta hacia lo divino.", 119),
     ("Con el tiempo, ese conocimiento fue quedando fuera de las *enseñanzas*.", "c:libro")],
    {"texto": "Y lo que quedó fue pedir. Pedir, repetir, esperar.",
     "visual": {"tipo": "texto", "legenda": False, "frases": [[0, "Y LO QUE QUEDÓ FUE…", "#0d0d0d"],
                ["pedir.", "<k>PEDIR</k>", "#1a0f12"], ["repetir", "<k>REPETIR</k>", "#0d0d0d"], ["esperar", "<k>ESPERAR</k>", "#1a0f12"]]}},
    [("Por eso hoy tanta gente reza sin sentir *respuesta*.", 107), ("Visualiza sin ver *cambios*.", 105)],
    [("Un millonario asegura que esa parte se puede *despertar*", 117),
     ("con un ritual corto, de *siete minutos*, inspirado en esas tradiciones antiguas.", 93)],
    [("Él lo explica en un video que, dicen, no va a durar mucho en *línea*.", 4),
     ("Lo que los sacerdotes guardaban, hoy lo puedes ver en tu *teléfono*.", 81)],
    {"texto": "Toca el botón de abajo y mira el video corto, antes de que lo quiten.",
     "visual": dict(CTA_CARD, fundo="b:114"), "destaques": ["botón", "video", "quiten"], "leg_topo": 900},
])

V["15"] = dict(primary_text="\"Yo pensaba que era mentira.\" Hasta que vio el video de un millonario que explica por qué a casi nadie le funciona. Mírelo 👇", blocos=[
    [("Yo toda mi vida *recé*, ¿eh?", 157), ("Pedí por mis hijos, por la casa, por las *cuentas*.", 132),
     ("Y muchas veces sentí que hablaba *sola*.", 126)],
    [("Cuando mi nieta me mostró ese video, le dije: otro *vendehúmo* más.", 72), ("Pero me quedé *escuchando*.", 140)],
    [("Él explica que hay una parte *espiritual* de la mente que está dormida.", 80),
     ("Que los antiguos la cuidaban, y nosotros la *olvidamos*.", "c:buda_cueva"),
     ("Y que por eso uno pide y pide, y la oración no encuentra *camino*.", 83)],
    [("No le pide que deje su *fe*.", 97), ("Le enseña un ritual de *siete minutos* para despertar esa parte.", 138)],
    [("Lo que más me gustó es que no promete *milagros* de un día para otro.", 124),
     ("Habla de calma, de *claridad*, de dejar de vivir con miedo.", 136)],
    [("Yo ya no soy joven, y no tengo tiempo para *perder*.", 125), ("Por eso le digo: mírelo usted *también*.", 173),
     ("Si es mentira, perdió siete minutos. Si no lo es…", 187)],
])

V["16"] = dict(primary_text="Tengo 72 años y nadie me había explicado esto nunca. 🙏 Un millonario cuenta por qué tantas oraciones no llegan. Míralo 👇", blocos=[
    [("Recé toda mi vida, cada noche, con todo mi *corazón*.", 157),
     ("Y siempre pensé que si no llegaba la respuesta, era porque no lo *merecía*.", 125)],
    [("Hasta que vi un video de un *millonario* que me hizo llorar.", 183), ("Dice que no es que Dios no *escuche*.", "c:barba"),
     ("Es que hay una parte de nosotros, una parte *espiritual*, que se queda dormida.", 115)],
    [("Y que nadie nos enseñó a *despertarla*.", 97)],
    [("Los antiguos sí lo sabían: los cristianos de antes, los monjes, los *egipcios*.", "c:monasterio"),
     ("Lo hacían antes de rezar, como quien *enciende* una luz.", 161)],
    [("Él muestra cómo hacerlo con un ritual de *siete minutos*.", 138), ("Algo simple, que hasta yo pude *entender*.", 8)],
    [("Si yo lo hubiera sabido a los treinta, cuántas noches me habría *ahorrado*.", 106),
     ("Por eso te lo digo a ti, que todavía tienes *tiempo*.", 95)],
    [("No lo dejes para *después*.", 129)],
])

V["17"] = dict(corte=3.64, primary_text="¿Rezas todas las noches y sientes que nadie te escucha? 🙏 Un millonario explica por qué tu oración no llega. Míralo 👇", blocos=[
    [("Te *entiendo*.", 16), ("Das las gracias, pides por los tuyos, pides una *salida*…", 157),
     ("y te acuestas con la misma *angustia* de siempre.", 184)],
    {"texto": "Y un día terminas buscando en internet por qué tus oraciones no tienen respuesta.",
     "visual": {"tipo": "busca", "consulta": "por qué mis oraciones no tienen respuesta", "digitar_ate": "por",
                "resultados_em": "respuesta", "resultados": [
                    ["foro · preguntas", "Rezo todos los días y nada cambia", "¿Alguien más se siente así?"],
                    ["blog · fe", "Tal vez no es el momento", "Ten paciencia y sigue pidiendo…"]]},
     "destaques": ["internet", "respuesta"], "leg_topo": 1000},
    [("Un millonario lo explica *distinto* en un video corto.", 25), ("Dice que el problema no es tu *fe*.", "c:redentor"),
     ("Es que la parte de tu mente que conecta con lo *divino* está dormida.", 92)],
    [("Es como llamar a alguien con el teléfono sin *señal*.", 22), ("Tú hablas, pero la llamada no *sale*.", 2)],
    [("Los antiguos cristianos, budistas y egipcios despertaban esa parte *antes* de orar.", "c:buda_cueva"),
     ("Él muestra cómo hacerlo hoy, con un ritual de *siete minutos*.", "c:meditar")],
    [("Dice que cuando despierta, la oración se siente *distinta*:", 136), ("con paz, con certeza, sin *rogar*.", 52)],
    [("Si esta noche vas a volver a rezar, primero mira este *video*.", 115)],
])

V["18"] = dict(corte=3.70, primary_text="Esto no te lo enseñaron en la iglesia… y no es culpa de nadie. ✝️ Un millonario explica la pieza que se perdió. Mira el video 👇", blocos=[
    [("Durante siglos, una parte de la enseñanza fue quedando *afuera*.", "c:libro"),
     ("No por maldad. Simplemente se *perdió*.", "c:monasterio")],
    {"texto": "Los antiguos cristianos sabían que antes de pedir, había que despertar algo por dentro.",
     "visual": {"tipo": "texto", "legenda": False, "frases": [[0, "LOS ANTIGUOS SABÍAN…", "#0d0d0d"],
                ["antes", "ANTES DE <k>PEDIR</k>", "#101a2e"], ["despertar", "HAY QUE <k>DESPERTAR</k>", "#0d0d0d"]]}},
    [("Una parte *espiritual* de la mente.", 119), ("La misma que los budistas cuidaban en *silencio*", 76),
     ("y que los egipcios dibujaban en sus *templos*.", 151)],
    [("Hoy casi todos rezamos con esa parte *dormida*.", 156), ("Por eso tantas oraciones se sienten *vacías*.", 146)],
    [("Un millonario lo explica en un video que está *circulando*.", 176),
     ("Y muestra cómo despertarla con un ritual de *siete minutos*.", 170)],
    [("No va contra tu iglesia. No te pide dejar *nada*.", "c:cruz"), ("Te devuelve la *pieza* que faltaba.", 80)],
    [("Cuando esa parte despierta, rezar deja de ser *rogar*.", 157), ("Se vuelve una *conversación*.", 128),
     ("Míralo antes de que lo *quiten*.", 81)],
])

V["19"] = dict(primary_text="¿Sabías que hay un ritual de 7 minutos que los millonarios no quieren que conozcas? 🤫 Míralo mientras sigue disponible 👇", blocos=[
    [("Yo tampoco lo *sabía*.", 122), ("Lo vi en un video de un millonario que decidió *contarlo* todo.", 134)],
    [("Él dice que la mayoría intenta atraer *abundancia* de la forma equivocada:", "c:billete_vuela"),
     ("pidiendo, visualizando, repitiendo frases frente al *espejo*.", 7)],
    [("Y que nada de eso funciona si una parte de tu mente está *dormida*.", 58),
     ("Una parte *espiritual* que los antiguos llamaban la conexión con lo divino.", 114)],
    [("El ritual es para *despertarla*.", 89), ("Siete minutos. En *silencio*. Desde tu casa.", 113)],
    [("¿Por qué no quieren que lo *conozcas*?", 171), ("Porque si todos lo supieran, dejaría de ser una *ventaja*.", 142)],
    [("Él cuenta que lo primero que cambia es esa sensación de estar siempre *corriendo* detrás de todo.", 99),
     ("Dejas de *perseguir*. Empiezas a atraer.", "c:silueta")],
    [("Míralo hoy, mientras sigue *disponible*.", 178)],
])

V["20"] = dict(primary_text="Suena loco, pero escúchame hasta el final. 👀 Un millonario cuenta que todo empezó al despertar una parte de su mente 👇", blocos=[
    [("Hay un millonario que nunca muestra la *cara*.", 88), ("Y en un video cuenta de dónde salió todo lo que *tiene*.", 104),
     ("Dice que no fue por trabajar más *duro*, ni por suerte.", 77)],
    {"texto": "Fue por activar una parte de su mente que estaba dormida.",
     "visual": {"tipo": "texto", "legenda": False, "frases": [[0, "NO FUE <k>SUERTE</k>", "#0d0d0d"],
                ["activar", "FUE <k>ACTIVAR</k>", "#101a2e"], ["dormida", "ALGO <k>DORMIDO</k>", "#0d0d0d"]]}},
    [("Una parte *espiritual* que casi todos tenemos apagada.", 109), ("Por eso rezamos, pedimos, *visualizamos*…", "c:barba"),
     ("y seguimos en el mismo *lugar*.", 152)],
    [("Él dice que los antiguos lo *sabían*.", 163), ("Que los cristianos, los budistas y los egipcios tenían formas de *despertarla*.", 150)],
    [("Y que hoy se puede hacer con *tres pasos* sencillos y un ritual de siete minutos.", 112)],
    [("Ya sé: suena *loco*. Te lo dije al principio.", 123),
     ("Pero piensa: ¿cuánto tiempo llevas haciendo lo mismo, esperando algo *distinto*?", 129)],
    [("Siete minutos no son *nada*.", "c:reloj"), ("Míralo hasta el *final*, como te pedí.", 72)],
])


def chave(c):
    return f"b:{c}" if isinstance(c, int) else c


def limpa(frase):
    dest = [w.lower().strip("¿¡,.:;…\"") for x in re.findall(r"\*([^*]+)\*", frase) for w in x.split()]
    return frase.replace("*", ""), dest


def meta_avatar(clipe):
    m = json.load(open(os.path.join(HEYGEN, clipe + ".json")))
    return min(m["duracao"], m["palavras"][-1]["fim"] + 0.25)


def main():
    crs, uso = [], {}
    for cr in BASE["criativos"]:
        i = cr["id"]
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
        if cauda is None and cr["cta"].get("clipe"):
            cauda = round(meta_avatar(cr["cta"]["clipe"]), 2)
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
    plano = {
        "produto": "codigo-alfa", "titulo": "Código Alfa · Lote 1 (reeditado: mínimo 1 min)",
        "obs": "Gancho original intacto, corpo e final novos (VSL), fechamento com o avatar já pago. Sem HeyGen novo: só TTS grátis.",
        "origem": "codigo-alfa/lotes/2026-11-08/codigo-alfa-lote-1-{id}.mp4",
        "banco": "banco/indice.json", "vozes": BASE["vozes"], "campeoes": BASE["campeoes"],
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
