"""21 Frases · Lote 3 (semana de 11/11/2026). Sem HeyGen novo: ganchos dos CAMPEÕES (o único [IA] que converteu
usou gancho campeão + corpo novo) e telas HTML com voz grátis; corpos novos (TTS da voz do Daniel) sobre o banco.
Gera pipeline/lotes/21-frases-lote-3.json.   Uso: python3 pipeline/lotes/21f_lote3.py
"""
import json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from semana_utils import P, V, conferir

CP = "21-frases/campeoes/"
HEAD = {  # cortes conferidos pelo ponto de menor energia da fala entre as frases
    "c1": {"src": CP + "criativo-mais-campeao-de-todos.mp4", "ini": 0, "fim": 8.09},
    "c2": {"src": CP + "video---1794084830597.mp4", "ini": 0, "fim": 8.09},
    "c3": {"src": CP + "video---1794084838097.mp4", "ini": 0, "fim": 7.17},
    "c4": {"src": CP + "video---1794084880585.mp4", "ini": 0, "fim": 9.21},
    "c5": {"src": CP + "video---1794084896106.mp4", "ini": 0, "fim": 8.2},
    "c6": {"src": CP + "video---1794084929175.mp4", "ini": 0, "fim": 9.63},
    "c7": {"src": CP + "video---1794085426838.mp4", "ini": 0, "fim": 14.5},
    "c8": {"src": CP + "video---1794085433854.mp4", "ini": 0, "fim": 10.69},
    "c9": {"src": CP + "video---1794085498075.mp4", "ini": 0, "fim": 6.45},
}


def CTA(texto, fundo):
    return V(texto, {"tipo": "cta", "fundo": fundo, "sobre": "VIDEO GRATUITO · 5 MINUTOS", "botao": "VER EL VIDEO ↓"},
             leg_topo=900)


def ZAP(texto, msgs, nome="Él ❤️", **kw):
    return V(texto, dict({"tipo": "zap", "nome": nome, "selo": "ejemplo", "msgs": msgs}, **kw), leg_topo=1010)


# ---------------------------------------------------------------- corpos
CORPO = {}
CORPO["A"] = ("Tono correcto / banco de reserva", [
    P([("Y no, no es que esté *ocupado*.", 171), ("Un hombre interesado siempre encuentra un *minuto* para responder.", 22),
       ("Cuando no lo hace, casi siempre es por el *mensaje* que recibió.", 178)]),
    P([("Mira lo que pasa normalmente:", 1), ("él tarda en responder, tú te *preocupas*,", 5),
       ("y le mandas otro mensaje para saber si está bien.", 0), ("Después otro, preguntando si hiciste algo *mal*.", 56),
       ("Y cada mensaje así le dice lo mismo:", 25), ("que ya te tiene, *sin hacer nada*.", 59)]),
    P([("Ahí es cuando te pone en la *banca*,", 58), ("como su opción de *reserva*.", 53), ("No porque no *valgas*,", 16),
       ("sino porque tu mensaje no le despertó ninguna *emoción*.", 126)]),
    P([("Existe un *tono exacto* para escribirle a un hombre.", 72), ("Un tono *tranquilo*, que no le pide nada,", 141),
       ("pero que lo deja con *curiosidad*.", 134), ("Y cuando lo usas, el que empieza a *preguntar* es él.", 4)]),
    ZAP("Por ejemplo: en vez de preguntarle por qué no te contesta, ella le manda algo corto y *tranquilo*. Y ahora es él quien quiere saber *más*.",
        [{"quem": "dela", "txt": "Hoy vi algo que me hizo acordarme de ti 😊 después te cuento", "em": 0.3, "hora": "21:12", "alt": 210},
         {"quem": "dele", "txt": "¿Qué viste? 👀 cuéntame ahora", "em": "ahora", "hora": "21:13"}],
        status=[[0, "en línea"], ["ahora", "escribiendo…"]]),
    P([("En un video gratuito de *cinco minutos*", 168), ("te muestro las *frases exactas* para cada situación:", 169),
       ("cuando te deja en *visto*, cuando se *enfría*,", 51), ("y cuando *desaparece* de la nada.", 70)]),
    CTA("Toca el botón de abajo y míralo *ahora*, antes de mandarle otro mensaje.", 45),
])
CORPO["B"] = ("Prova masculina: o que os homens não admitem", [
    P([("Te voy a contar algo que los hombres casi nunca *admiten*.", 22), ("Cuando un hombre está *interesado*,", 134),
       ("responde aunque esté en el *trabajo*, en el gimnasio o con sus amigos.", 26), ("*Diez segundos*. Es todo lo que necesita.", 129)]),
    P([("Entonces, si tarda *horas*,", 2), ("no es el tiempo.", 93),
       ("Es que tu mensaje no le dio una *razón* para responder.", 25)]),
    P([("La mayoría de las mujeres escribe lo *mismo*:", 0), ("hola, ¿cómo estás?, ¿qué haces?, ¿todo bien?", 176),
       ("Mensajes que él ya leyó *mil veces*.", 178), ("Y lo que es *predecible*, se deja para después.", 28)]),
    P([("Pero hay frases que funcionan *distinto*.", 7), ("Frases que tocan su *curiosidad*,", 47),
       ("su *orgullo*, o el *miedo a perderte*.", 44), ("Y cuando él siente eso, dejarte en visto ya no es tan *fácil*.", 73)]),
    P([("No es *manipulación*.", 8), ("Es hablarle en el *idioma* en que piensa un hombre.", 49),
       ("Directo, corto, y *sin presión*.", 141)]),
    P([("Y no importa si ya le escribiste *de más*,", 132), ("o si hace días que no te *responde*.", 51),
       ("Todavía puedes *cambiar el tono*", 72), ("y hacer que te mire *distinto*.", 46)]),
    P([("Reuní esas frases en un video gratuito de *cinco minutos*.", 168), ("Ahí vas a ver qué escribirle *hoy mismo*,", 169),
       ("y qué no mandarle *nunca*.", 183)]),
    CTA("Toca el botón de abajo y míralo antes de que lo *quiten*.", 61),
])
CORPO["C"] = ("História: a amiga que parou de implorar", [
    P([("Esa respuesta me recordó a una amiga, *Carla*.", 46), ("Ella le escribía a un chico *todos los días*.", 1),
       ("Buenos días, buenas noches, ¿cómo te fue?", 0), ("Y él cada vez respondía *menos*.", 25)]),
    P([("Una noche la dejó en *visto* por horas.", 51), ("Ella estaba a punto de mandarle un audio *largo*,", 5),
       ("preguntándole qué había hecho *mal*.", 105)]),
    P([("Le dije: para. *No le mandes eso*.", 132), ("Al día siguiente le escribió una *sola frase*.", 140),
       ("Corta, tranquila, *sin reclamo*,", 141), ("y que lo dejaba con *ganas de saber más*.", 136)]),
    ZAP("Algo así. Y esta vez, el que *preguntó* fue él.",
        [{"quem": "dela", "txt": "Ayer escuché una canción que te iba a mandar… pero mejor te la muestro en persona 😊", "em": 0.2, "hora": "19:40", "alt": 250},
         {"quem": "dele", "txt": "¿Cuál canción? 👀 ¿cuándo me la muestras?", "em": "preguntó", "hora": "19:41"}],
        status=[[0, "en línea"], ["preguntó", "escribiendo…"]]),
    P([("No fue *suerte*.", 7), ("Ella simplemente dejó de escribirle desde la *ansiedad*", 118),
       ("y empezó a escribirle desde la *calma*.", 172)]),
    P([("Y eso es lo que casi nadie te dice:", 126), ("un hombre no se aleja por *un solo* mensaje.", 22),
       ("Se aleja por la *sensación* que le dejan tus mensajes:", 28), ("presión… o *curiosidad*.", 47),
       ("Y no, no tienes que *fingir* ni jugar con él.", 8), ("Solo saber *qué decir*, y cuándo.", 129)]),
    P([("Las frases que ella usó, y otras para *cada situación*,", 169), ("están en un video *gratuito* de cinco minutos.", 168)]),
    CTA("Toca el botón de abajo y míralo *hoy*, antes de mandarle otro mensaje.", 63),
])
CORPO["D"] = ("Cabeça dele: 5 mensagens seguidas", [
    P([("Él lo dijo *sin pensar*.", 47), ("Y es lo que casi todos los hombres *piensan*, pero no te dicen.", 22)]),
    P([("Ahora mira lo que pasa en la *cabeza* de un hombre", 28), ("cuando recibe *cinco mensajes* seguidos de la misma mujer.", 2),
       ("No piensa: qué linda, se *preocupa* por mí.", 12), ("Piensa: ya está *segura*, no tengo que esforzarme.", 59)]),
    P([("Un hombre se interesa por lo que todavía tiene que *conquistar*.", 19), ("Por eso, cuanto más le *insistes*,", 0),
       ("más tranquilo se siente para *no responder*.", 25)]),
    P([("La solución no es *ignorarlo* ni hacerte la difícil.", 8), ("Es cambiar lo que le *escribes*.", 176),
       ("Menos explicaciones, menos preguntas,", 7), ("y una frase que despierte en él las *ganas de responderte*.", 134)]),
    P([("Piensa en el hombre que te *gusta*.", 46), ("Si cada vez que te lee siente *calma* y un poco de *misterio*,", 141),
       ("va a querer *más*.", 4), ("Si siente *reclamos*, va a buscar *excusas*.", 58)]),
    V("Arriba, lo que manda casi todo el mundo. Abajo, un mensaje que lo hace *pensar en ti*.",
      {"tipo": "split", "antes": {"msgs": [{"quem": "dela", "txt": "¿Por qué no me respondes? 😔", "em": 0.3},
                                            {"quem": "dela", "txt": "¿Hice algo mal?", "em": "mundo"}]},
       "depois": {"rot_em": "Abajo", "msgs": [{"quem": "dela", "txt": "Hoy pasé por donde nos conocimos 🙂", "em": "Abajo"},
                                               {"quem": "dele", "txt": "Jaja ¿y te acordaste de mí? 😏", "em": "pensar"}]},
       "selo": "ejemplo"}, leg_topo=1100),
    P([("En un video gratuito de *cinco minutos*", 168), ("te muestro las *frases exactas*,", 169),
       ("para *copiar*, pegar y enviar.", 173)]),
    CTA("Toca el botón de abajo y míralo *ahora*, antes de que lo quiten.", 43),
])
CORPO["E"] = ("Valor e escassez (desdém sem jogos)", [
    P([("Piensa en esto:", 126), ("un hombre *valora* lo que siente que puede *perder*.", 20),
       ("Y deja para después lo que tiene *asegurado*.", 53)]),
    P([("Cuando le escribes *todo el día*,", 1), ("cuando le *explicas* cada cosa que sientes,", 132),
       ("cuando le preguntas por qué *no responde*,", 56), ("él no siente que te puede perder.", 25),
       ("Siente que ya te *ganó*.", 59)]),
    P([("Desdén no es tratarlo *mal*.", 35), ("Es tener tu *propia vida*,", 172), ("responder con *calma*,", 141),
       ("y dejar de estar siempre *disponible*.", 36)]),
    P([("Y ojo: esto no es *castigarlo*", 8), ("ni dejar de *escribirle* para siempre.", 0),
       ("Es entender que un hombre necesita *espacio*", 47), ("para *extrañarte*.", 16)]),
    P([("Si siempre estás *disponible*,", 5), ("no tiene nada que *extrañar*.", 51), ("Y lo que no se extraña, *no se busca*.", 4)]),
    P([("Y hay frases que comunican eso en *pocas palabras*.", 7), ("Frases que hacen que él se *pregunte*:", 22),
       ("¿y si ella ya no está tan *interesada*?", 28), ("Ahí es cuando muchos hombres empiezan a *buscar más*.", 134)]),
    P([("Y cuando eso pasa, muchas veces se nota *rápido*:", 122), ("él empieza a escribirte *primero*,", 73),
       ("a preguntarte *qué haces*,", 176), ("y a proponerte *verse*.", 63)]),
    P([("En un video gratuito de *cinco minutos*", 168), ("te enseño cuáles son, y *cuándo* usarlas,", 169),
       ("con *elegancia*, sin juegos.", 45)]),
    CTA("Toca el botón de abajo y míralo *ahora*.", 18),
])
CORPO["F"] = ("Palavras, não aparência (objeção: não sou suficiente)", [
    P([("¿Y sabes por qué?", 121), ("Porque sabía exactamente *qué decir*,", 35), ("y cuándo quedarse *callada*.", 16)]),
    P([("Hoy muchas mujeres creen que el problema es su *cuerpo*,", 118), ("su *edad*, o que no son *suficientes*.", 146),
       ("Y no.", 8), ("Lo que hace que un hombre no deje de *pensar en ti*", 17), ("casi nunca es la *apariencia*.", 126)]),
    P([("Son las *palabras*.", 169), ("Una frase dicha en el *momento correcto*", 72), ("puede despertar su *curiosidad*,", 47),
       ("su deseo de *protegerte*,", 49), ("o su *miedo a perderte*.", 44)]),
    P([("Piensa en la última vez que él se *alejó*.", 25), ("¿Fue porque dejaste de ser *bonita*?", 136), ("No.", 141),
       ("Fue por lo que *sintió*, o dejó de sentir, al leerte.", 0), ("Un mensaje puede hacerlo sentir *presionado*…", 12),
       ("o con *ganas de verte*.", 46)]),
    P([("Cleopatra no *rogaba*.", 36), ("No *perseguía*.", 20), ("Y aun así, era a ella a quien *buscaban*.", 18)]),
    P([("Ella entendía algo muy *simple*:", 22), ("un hombre *persigue* lo que lo hace sentir algo,", 19),
       ("y se *aburre* de lo que ya conoce.", 53)]),
    P([("Esas palabras no son un secreto de *reinas*.", 7), ("Se pueden *aprender*.", 175),
       ("Las reuní en un video gratuito de *cinco minutos*,", 168), ("con frases que puedes *copiar* y mandarle hoy.", 173)]),
    CTA("Toca el botón de abajo y míralo antes de que lo *quiten*.", 42),
])
CORPO["G"] = ("Por que ele sumiu depois de tanto interesse", [
    P([("Al principio te escribía *todos los días*.", 4), ("Te mandaba buenos días, te llamaba, te *buscaba*.", 73),
       ("Y de un momento a otro, *silencio*.", 51)]),
    P([("Lo primero que piensas es que hay *otra*,", 58), ("o que hiciste algo *mal*.", 105),
       ("Pero muchas veces es más *simple*:", 126), ("él sintió que ya te había *conquistado*,", 25),
       ("y la emoción del comienzo se *apagó*.", 28)]),
    P([("Y aquí está el *error* que casi todas cometen:", 122), ("le *reclaman*, le preguntan qué pasó,", 15),
       ("le mandan mensajes *largos* explicando lo que sienten.", 0), ("Eso solo confirma que él no tiene que hacer *nada*.", 59)]),
    P([("Lo que lo hace *volver* es otra cosa:", 7), ("un mensaje *corto*, tranquilo,", 141),
       ("que le recuerde lo que sentía *al principio*.", 63), ("*Sin presión*, sin reclamos.", 172)]),
    P([("Y el *momento* también importa.", 129), ("Si le escribes en el momento *equivocado*,", 132),
       ("hasta la frase perfecta pasa *desapercibida*.", 56), ("Por eso no basta con saber *qué* decir:", 22),
       ("hay que saber *cuándo*.", 2)]),
    P([("Y otra cosa: no le escribas para saber si todavía le *gustas*.", 140), ("Escríbele para que *sienta* algo.", 72),
       ("Esa es la diferencia entre *perseguirlo*", 20), ("y hacer que él *te busque*.", 61)]),
    P([("En un video gratuito de *cinco minutos*", 168), ("te muestro qué escribirle cuando *desaparece*,", 169),
       ("y qué no decirle *nunca*, aunque te duela.", 183)]),
    CTA("Toca el botón de abajo y míralo *ahora*, antes de que lo quiten.", 158),
])
CORPO["H"] = ("Prioridade: tirar ele do estado de desatenção", [
    P([("Pero antes, entiende qué es el estado de *desatención*.", 22), ("Es cuando él ya no se pregunta qué estás *haciendo*,", 25),
       ("ni con *quién* estás.", 48), ("Te responde *por responder*.", 178), ("Y tú lo *sientes*.", 16)]),
    P([("En ese punto, escribirle *más* no ayuda.", 0), ("Lo que lo saca de ahí es la *sorpresa*:", 121),
       ("una frase que él *no espera* de ti.", 7)]),
    P([("Ni mensajes largos, ni *indirectas* en tus historias,", 1), ("ni hacerte la *ocupada* por horas.", 129),
       ("Eso él ya lo *conoce*,", 28), ("y su cabeza lo *ignora*.", 59)]),
    ZAP("Por ejemplo, algo así de simple. Él lo lee, y por primera vez en días, quiere *saber más*.",
        [{"quem": "dela", "txt": "Me pasó algo hoy que me hizo pensar en ti… pero no sé si contártelo 🙈", "em": 0.3, "hora": "20:05", "alt": 250},
         {"quem": "dele", "txt": "Ahora me tienes que contar 😅", "em": "quiere", "hora": "20:06"}],
        status=[[0, "en línea"], ["lee", "escribiendo…"]]),
    P([("Eso es activar su lado *masculino*:", 47), ("la *curiosidad*, las ganas de *buscarte*,", 19),
       ("de ser él quien da el *siguiente paso*.", 61)]),
    P([("Y fíjate en algo:", 126), ("en esa frase *no hay reclamo*,", 141), ("no hay *presión*,", 8),
       ("no hay un ¿por qué no me escribes?", 56), ("Solo hay *curiosidad*.", 134)]),
    P([("Esa es solo *una* de las frases.", 169), ("En un video gratuito de cinco minutos te muestro las *demás*,", 168),
       ("para cada momento de la *relación*.", 45)]),
    CTA("Toca el botón de abajo y míralo *ahora*, antes de que lo quiten.", 62),
])
CORPO["I"] = ("Tipos de mensagem: curiosidade, conexão, atração", [
    P([("Porque un hombre no se enamora de lo que le *das*.", 22), ("Se enamora de lo que *siente* cuando habla contigo.", 73)]),
    P([("Hay mensajes que lo *aburren*,", 25), ("mensajes que lo *asustan*,", 12),
       ("y mensajes que lo dejan *pensando en ti* todo el día.", 134), ("La diferencia muchas veces es *una sola frase*.", 7)]),
    V("Mensajes de curiosidad, para que te responda. Mensajes de conexión, para que se abra contigo. Y mensajes de atracción, para que quiera verte.",
      {"tipo": "texto", "legenda": False, "frases": [[0, "MENSAJES DE<br><k>CURIOSIDAD</k>", "#0d0d0d"],
                                                     ["conexión", "MENSAJES DE<br><k>CONEXIÓN</k>", "#1a0f12"],
                                                     ["atracción", "MENSAJES DE<br><k>ATRACCIÓN</k>", "#0b141a"]]}),
    P([("Y lo mejor: no tienes que *inventar* nada.", 141), ("Abres, *copias*, pegas y envías.", 173), ("En el momento *justo*.", 129)]),
    P([("No necesitas ser *escritora*,", 169), ("ni tener una *labia* especial.", 46),
       ("Solo elegir la frase *correcta*", 140), ("para lo que estás *viviendo*.", 16)]),
    P([("La mayoría de las mujeres hace lo *contrario*:", 132), ("escribe lo primero que *siente*,", 0),
       ("y después se pasa la noche *esperando* una respuesta.", 51)]),
    P([("Y cuanto más espera, más *ansiosa* se pone,", 105), ("y más mensajes *manda*.", 56),
       ("Es un *círculo* que lo aleja cada vez más.", 28), ("Las frases correctas *cortan* ese círculo.", 72)]),
    P([("Las frases están en un video gratuito de *cinco minutos*.", 168), ("Míralo antes de escribirle *otra vez*.", 70)]),
    CTA("Toca el botón de abajo, antes de que lo *quiten*.", 19),
])
CORPO["J"] = ("Resposta do quiz: por que a C funciona", [
    P([("Si elegiste la *A*, no estás sola.", 0), ("Es lo que casi todas *hacen*.", 56),
       ("Pero insistir le confirma que te tiene *segura*.", 59)]),
    P([("Si elegiste la *B*, entiendo el enojo.", 105), ("Pero bloquearlo no lo hace *pensar en ti*.", 28),
       ("Solo le da una *excusa* para alejarse.", 58)]),
    P([("La respuesta es la *C*.", 7), ("Una frase *corta*, tranquila,", 141), ("que no le pide *explicaciones*,", 36),
       ("y que despierta su *curiosidad*.", 47), ("Así, responderte se vuelve *idea de él*.", 134)]),
    P([("Esa frase no le exige *nada*.", 140), ("Por eso no hay nada de qué *defenderse*,", 12),
       ("y su atención vuelve a *ti*.", 73)]),
    P([("Y aquí está lo *interesante*:", 121), ("cuando él no recibe la reacción que *espera*,", 25),
       ("ni el reclamo, ni el silencio *ofendido*,", 183), ("se queda *pensando*.", 22),
       ("Y un hombre que se queda pensando en ti,", 126), ("muchas veces es el que vuelve a *escribir*.", 4)]),
    P([("No tienes que ser *otra persona*.", 172), ("Solo cambiar *cómo* le escribes.", 176)]),
    P([("El problema es saber *qué frase* mandar,", 132), ("y en qué *momento*.", 129),
       ("Por eso preparé un video gratuito de *cinco minutos*", 168), ("con las *frases exactas* para cada situación.", 169)]),
    CTA("Toca el botón de abajo y míralo *ahora*, antes de mandarle otro mensaje.", 65),
])
CORPO["K"] = ("Público novo: mulheres 35+ que voltaram a sair", [
    P([("Las reglas *cambiaron*.", 126), ("Hoy todo pasa por *mensajes*,", 140),
       ("y un mensaje mal escrito puede *enfriar* a un hombre", 25), ("que parecía muy *interesado*.", 47)]),
    P([("Muchas mujeres que vuelven a salir después de una relación *larga*", 16), ("escriben como se hablaba *antes*:", 0),
       ("explican todo, preguntan todo, se *entregan* rápido.", 56), ("Y él se *aleja* sin decir por qué.", 58)]),
    P([("No es tu *edad*.", 7), ("Al contrario: tu *experiencia* es un atractivo.", 35),
       ("Lo que falta es usar el *tono correcto*,", 141), ("uno tranquilo, *seguro*, que no persigue.", 36)]),
    P([("Sabes lo que *quieres*,", 8), ("y no tienes paciencia para *juegos*.", 15),
       ("Las frases correctas te ahorran *meses*", 93), ("de esperar a que él se *decida*.", 28)]),
    P([("Un hombre *maduro* se siente atraído", 171), ("por una mujer que sabe lo que *vale*,", 172),
       ("y que no tiene *prisa*.", 41)]),
    P([("Y otra cosa:", 122), ("a esta edad ya no tienes *tiempo* que perder", 129), ("con hombres que te tienen en *duda*.", 22),
       ("Las frases correctas también te *muestran*", 72), ("*quién* está realmente interesado.", 134)]),
    P([("Si responde con *ganas*, perfecto.", 73), ("Si no, ya sabes que *no era él*.", 130)]),
    P([("En un video gratuito de *cinco minutos*", 168), ("te muestro las frases que funcionan *hoy*,", 169),
       ("sin juegos y sin parecer *desesperada*.", 46)]),
    CTA("Toca el botón de abajo y míralo *ahora*.", 45),
])
CORPO["L"] = ("Objeção dele: 'não quero nada sério'", [
    P([("Lo que respondas ahora *importa* mucho.", 126), ("La mayoría responde de *dos formas*:", 132),
       ("o le *ruega* que lo intente,", 105), ("o se *enoja* y desaparece.", 183), ("Y las dos lo *alejan*.", 28)]),
    P([("Cuando un hombre dice eso,", 22), ("muchas veces no está diciendo que no te *quiere*.", 25),
       ("Está diciendo que todavía no siente la necesidad de *elegirte*.", 59)]),
    P([("Y casi siempre deja una *puerta abierta*:", 72), ("fíjate que dijo: pero me gusta *hablar contigo*.", 140),
       ("Esa es tu *oportunidad*,", 46), ("si sabes qué *responder*.", 169)]),
    P([("Y esa necesidad no nace con *presión*.", 44), ("Nace cuando él siente que tienes tu *propia vida*,", 172),
       ("que estás *bien* con o sin él,", 130), ("y que podría *perderte*.", 20)]),
    P([("Muchos hombres dicen esa frase", 178), ("para ver tu *reacción*.", 12),
       ("Si te desesperas, confirma que te tiene *segura*.", 56), ("Si respondes con *calma*, lo *descoloca*.", 7)]),
    P([("Y un hombre que se queda pensando,", 136), ("muchas veces es el que *vuelve* a buscar.", 4),
       ("Sin que tú le *ruegues* nada.", 35)]),
    P([("Hay una respuesta *corta*, tranquila, sin drama,", 141), ("que cambia la forma en que te *mira*.", 47),
       ("Y otras frases para los días en que él se *enfría*.", 51)]),
    P([("Están en un video *gratuito* de cinco minutos.", 168), ("Míralo antes de *responderle*.", 176)]),
    CTA("Toca el botón de abajo y míralo *ahora*.", 49),
])

# ---------------------------------------------------------------- ganchos em tela (voz grátis)
G = {}
G["zap"] = ZAP("Mira este chat. Ella le escribió todo lo que sentía, a las diez de la noche. Y él la dejó en *visto*.",
               [{"quem": "dela", "txt": "Hola, ¿todo bien? Siento que estás distante y no sé si hice algo mal… ¿podemos hablar? 😔",
                 "em": 0.2, "hora": "22:04", "alt": 260, "azul": "visto"}],
               status=[[0, "en línea"], ["visto", "últ. vez hoy a las 22:05"]],
               carimbos=[{"tipo": "mau", "txt": "VISTO ✓✓", "em": "visto", "topo": 640, "x": 260}])
G["noticia"] = V("*Urgente*. El mensaje que casi todas las mujeres mandan, y que hace que él deje de *responder*.",
                 {"tipo": "noticia", "fundo": 5, "tarja": "URGENTE", "canal": "NOTICIAS DEL CORAZÓN",
                  "manchetes": [[0, "EL MENSAJE QUE HACE QUE ÉL TE DEJE EN VISTO"], ["deje", "¿LO HAS MANDADO TÚ?"]],
                  "letreiro": "dramatización · ejemplo · el mensaje que casi todas mandan · "})
G["busca"] = V("Si alguna vez buscaste esto a la una de la mañana, *quédate*.",
               {"tipo": "busca", "consulta": "por qué desapareció si estaba tan interesado", "digitar_ate": "mañana",
                "resultados": [["foro · amor", "Me escribía todos los días y de repente nada", "¿Le escribo o espero? Ya no sé qué hacer…"],
                               ["preguntas", "¿Por qué los hombres desaparecen de la nada?", "Muchas mujeres pasan por esto y nadie lo explica"],
                               ["blog", "Qué NO decirle cuando se aleja", "El error que casi todas cometen…"]]}, leg_topo=1010)
G["quiz"] = V("Él te deja en visto *seis horas*. ¿Qué haces? A: le escribes otra vez. B: lo bloqueas. C: le mandas una frase corta y tranquila, que lo deja con *curiosidad*.",
              {"tipo": "quiz", "pergunta": "Él te deja en visto 6 horas. ¿Qué haces?",
               "opcoes": [{"txt": "Le escribes otra vez", "em": "A"}, {"txt": "Lo bloqueas", "em": "B"},
                          {"txt": "Una frase corta que le da curiosidad", "em": "C", "certa": True, "veredito_em": "curiosidad"}]},
              leg_topo=1010)
G["texto35"] = V("Si tienes más de *treinta y cinco*, y volviste a tener citas, esto es para *ti*.",
                 {"tipo": "texto", "legenda": False, "frases": [[0, "¿TIENES MÁS DE <k>35</k>?", "#0d0d0d"],
                                                                ["volviste", "¿Y VOLVISTE A TENER <k>CITAS</k>?", "#1a0f12"],
                                                                ["esto", "ESTO ES <k>PARA TI</k>", "#0b141a"]]})
G["bloqueio"] = V("Si él te escribió que no está listo para algo serio, no le respondas *todavía*.",
                  {"tipo": "bloqueio", "hora": "23:41", "data": "miércoles, 11 de noviembre",
                   "notifs": [{"de": "Él", "txt": "No estoy listo para algo serio ahora… pero me gusta hablar contigo", "em": 0.2}],
                   "selo": "ejemplo"})
G["split"] = V("Arriba, cómo le escribe casi todo el mundo cuando él se *aleja*. Abajo, cómo le escribe una mujer que sabe lo que *vale*.",
               {"tipo": "split", "antes": {"msgs": [{"quem": "dela", "txt": "¿Por qué ya no me escribes como antes? 😢", "em": 0.3},
                                                    {"quem": "dela", "txt": "Te extraño mucho, por favor respóndeme", "em": "aleja"}]},
                "depois": {"rot_em": "Abajo", "msgs": [{"quem": "dela", "txt": "Hoy no puedo, tengo planes 😊 hablamos mañana", "em": "Abajo"},
                                                        {"quem": "dele", "txt": "¿Planes con quién? 👀", "em": "vale"}]},
                "selo": "ejemplo"}, leg_topo=1100)

# ---------------------------------------------------------------- lote: id, formato, gancho, corpo
LOTE = [
    ("01", "apresentador (gancho campeão #1)", ("cab", "c1", "Si él te está ignorando o te dejó en visto, mándale estas frases secretas a su WhatsApp…"), "A"),
    ("02", "tela dividida com cenas de emoção (gancho campeão #2)", ("cab", "c2", "Si él te está ignorando o te dejó en visto… (versão tela dividida)"), "B"),
    ("03", "entrevista de rua, repórter mulher (gancho campeão #5)", ("cab", "c5", "Una pregunta: si nos dejan en visto tres horas, ¿es porque no le importamos?"), "C"),
    ("04", "entrevista de rua, homem responde (gancho campeão #7)", ("cab", "c7", "Seamos sinceros, si una mujer te manda un mensaje y no le respondes en todo el día…"), "D"),
    ("05", "estúdio de podcast (gancho campeão #8)", ("cab", "c8", "¿Quieres que un hombre corra detrás de ti? No grites, no ruegues, aplica el desdén…"), "E"),
    ("06", "gancho histórico Cleópatra (campeão #6)", ("cab", "c6", "Cleopatra no era la mujer más hermosa de Egipto, pero…"), "F"),
    ("07", "tela dividida com mulheres chorando (gancho campeão #3)", ("cab", "c3", "¿Quieres saber por qué desapareció de la nada después de haber mostrado tanto interés?"), "G"),
    ("08", "apresentador com microfone de mão (gancho campeão #4)", ("cab", "c4", "Un hombre solo pasa a priorizar de verdad a una mujer cuando…"), "H"),
    ("09", "apresentador (gancho campeão #9)", ("cab", "c9", "Si yo fuera mujer y me quedara soltera en este 2026…"), "I"),
    ("10", "conversa de WhatsApp (visto)", ("tela", "zap", "Mira este chat. Ella le escribió todo lo que sentía… y él la dejó en visto."), "A"),
    ("11", "simulação de notícia URGENTE", ("tela", "noticia", "Urgente. El mensaje que casi todas las mujeres mandan, y que hace que él deje de responder."), "B"),
    ("12", "interface de busca", ("tela", "busca", "Si alguna vez buscaste esto a la una de la mañana, quédate."), "G"),
    ("13", "quiz A/B/C (teste)", ("tela", "quiz", "Él te deja en visto seis horas. ¿Qué haces?"), "J"),
    ("14", "texto grande + música (mini VSL)", ("tela", "texto35", "¿Tienes más de 35 y volviste a tener citas? Esto es para ti."), "K"),
    ("15", "notificação na tela bloqueada", ("tela", "bloqueio", "Si él te escribió que no está listo para algo serio, no le respondas todavía."), "L"),
    ("16", "antes e depois (tela dividida de conversa)", ("tela", "split", "Arriba, cómo le escribe casi todo el mundo… Abajo, una mujer que sabe lo que vale."), "E"),
]

PRIMARY = {
    "A": "¿Te dejó en visto otra vez? 😔 No es falta de tiempo: es el tono del mensaje. Mira el video gratuito de 5 minutos con las frases exactas 👇",
    "B": "Lo que los hombres casi nunca admiten: si está interesado, siempre encuentra 10 segundos. 👀 Mira qué escribirle hoy 👇",
    "C": "Ella dejó de rogarle… y le mandó UNA frase. 😳 Mira las frases en el video gratuito 👇",
    "D": "Lo que piensa un hombre cuando le mandas 5 mensajes seguidos (y lo que sí funciona). Video gratuito 👇",
    "E": "No ruegues. No persigas. Un hombre valora lo que siente que puede perder. 💅 Mira el video gratuito 👇",
    "F": "Cleopatra no era la más hermosa… pero sabía qué decir. 👑 Las palabras se aprenden: video gratuito de 5 minutos 👇",
    "G": "¿Por qué desapareció después de tanto interés? 💔 Y qué NO decirle aunque te duela. Mira el video gratuito 👇",
    "H": "La frase que lo saca del 'modo automático' y lo hace buscarte. 📲 Mira el video gratuito 👇",
    "I": "Mensajes de curiosidad, de conexión y de atracción. Copias, pegas y envías. ✨ Video gratuito de 5 minutos 👇",
    "J": "Él te deja en visto 6 horas. ¿A, B o C? 🤔 La respuesta correcta (y las frases) en el video gratuito 👇",
    "K": "¿Más de 35 y volviste a tener citas? Las reglas cambiaron. 💬 Mira las frases que funcionan hoy 👇",
    "L": "'No estoy listo para algo serio'… ¿qué le respondes? 🤐 Míralo antes de responderle 👇",
}


def rodar(cr, n):
    """Varia a imagem do 'video gratuito' entre os vídeos (mulher no notebook / de óculos / estudando)."""
    usados = {p[1] for b in cr["blocos"] for p in b.get("partes", [])}
    alt = ["b:168", "b:175", "b:78"][n % 3]
    if alt in usados:
        return
    for b in cr["blocos"]:
        for p in b.get("partes", []):
            if p[1] == "b:168":
                p[1] = alt


RUINS = {"b:47": ["b:134", "b:49", "b:19"], "b:44": ["b:13", "b:10", "b:15"]}  # rosto fora do corte / costas


def trocar(cr):
    usados = {p[1] for b in cr["blocos"] for p in b.get("partes", [])}
    for b in cr["blocos"]:
        for p in b.get("partes", []):
            if p[1] in RUINS:
                novo = next(x for x in RUINS[p[1]] if x not in usados)
                usados.add(novo)
                p[1] = novo


def main():
    crs = []
    for i, formato, (tipo, k, gtxt), corpo in LOTE:
        nome, blocos = CORPO[corpo]
        cr = {"id": i, "formato": formato, "angulo": nome, "corpo": corpo, "gancho": gtxt, "voz": "daniel",
              "primary_text": PRIMARY[corpo], "blocos": json.loads(json.dumps(blocos))}
        if tipo == "cab":
            cr["cabeca"] = HEAD[k]
        else:
            cr["blocos"].insert(0, json.loads(json.dumps(G[k])))
        rodar(cr, len(crs))
        trocar(cr)
        crs.append(cr)
    conferir(crs)
    plano = {"produto": "21-frases", "titulo": "21 Frases · Lote 3", "banco": "banco/indice.json",
             "limites": {"b:4": [3.5, 10.0], "b:25": [3.0, 10.0]}, "campeoes": {}, "brolls": {},
             "vozes": {"daniel": "0e07ee5d68de482aa44d5095dfa2f900", "mulher": "1777080b7f574979875dc144b9fbf0de",
                       "jornal": "6ce26db0cb6f4e7881b85452619f7f19", "locutor": "70bc24b8126c446c8cf50fc1a01eb834"},
             "criativos": crs}
    json.dump(plano, open(os.path.join(AQUI, "21-frases-lote-3.json"), "w"), ensure_ascii=False, indent=1)
    print(len(crs), "criativos")


if __name__ == "__main__":
    main()
