"""Código Alfa · Lote 2 (semana de 11/11/2026). Sem HeyGen novo: ganchos dos campeões, ganchos de Avatar IV JÁ PAGOS
(cortados dos vídeos do Lote 1 v2) e telas HTML com voz grátis; corpos 100% novos sobre o banco espiritual/dinheiro.
Regras: avatar nunca diz que ELE ganhou dinheiro; nada de prometer ganho; sem estudos/universidades; sem celular/casal/idosos;
o "millonario secreto" nunca aparece.   Gera pipeline/lotes/codigo-alfa-lote-2.json.
"""
import json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from semana_utils import P, V, conferir

KP = "codigo-alfa/campeoes/"
V2 = "codigo-alfa/lotes/2026-11-09-v2/{}.mp4"
HEAD = {
    "k2": {"src": KP + "video---1794092033124.mp4", "ini": 0, "fim": 3.71},
    "k3": {"src": KP + "video---1794092042737.mp4", "ini": 0, "fim": 7.51},
    "k4": {"src": KP + "video---1794092050748.mp4", "ini": 0, "fim": 5.31},
    "CA01": {"src": V2.format("01"), "ini": 0, "fim": 8.93},
    "CA04": {"src": V2.format("04"), "ini": 0, "fim": 5.11},
    "CA05": {"src": V2.format("05"), "ini": 0, "fim": 5.7},
    "CA12": {"src": V2.format("12"), "ini": 0, "fim": 4.98},
    "CA13": {"src": V2.format("13"), "ini": 0, "fim": 6.53},
    "CA19": {"src": V2.format("19"), "ini": 0, "fim": 5.31},
}
CAUDA = {k: {"src": V2.format(k), "do_fim": s} for k, s in
         {"01": 3.91, "02": 3.93, "04": 4.26, "05": 4.21, "10": 4.12, "12": 4.54, "13": 4.12, "19": 4.46}.items()}
CORTES = {  # cenas dos campeões sem o millonario secreto (região "alto" = sem a legenda antiga)
    "billetera": ["k2", 28.18, 30.19], "rubia": ["k2", 30.35, 32.72], "reloj": ["k2", 32.88, 35.79],
    "playa": ["k2", 40.65, 42.55], "barba": ["k2", 42.71, 45.25], "libro": ["k2", 59.51, 61.12],
    "champan": ["k2", 76.85, 79.09], "mar": ["k2", 84.65, 86.92], "buda_cueva": ["k3", 15.78, 21.12],
    "cruz": ["k3", 37.01, 40.29], "monasterio": ["k3", 44.71, 48.65], "estatua": ["k3", 62.68, 66.65],
    "billete_vuela": ["k4", 58.98, 60.75], "despertar": ["k1", 59.48, 61.02],
}
CTA_CARD = {"tipo": "cta", "sobre": "VIDEO CORTO", "titulo": "EL VIDEO DEL<br>MILLONARIO", "botao": "MIRA EL VIDEO ↓"}


def CTA(fundo):
    return V("Toca el botón de abajo y mira el video *corto*, antes de que lo *quiten*.", dict(CTA_CARD, fundo=fundo), leg_topo=900)


CORPO = {}
CORPO["P"] = ("Pedir desde a carência (não é contra a fé)", [
    P([("Escúchame bien.", 83), ("No digo que dejes tu *fe*.", "c:cruz"), ("Digo que la forma en que te enseñaron a *pedir*", 157),
       ("te mantiene en el mismo *lugar*.", 152)]),
    P([("Cuando pides desde la *carencia*,", 105), ("le repites a tu mente que *no tienes*.", 85),
       ("Y cada noche el mensaje es el mismo:", 115), ("*falta*, falta, falta.", 93)]),
    P([("Y no es tu *culpa*.", 126), ("Así nos enseñaron a *todos*:", 127), ("a pedir con *miedo*,", 108),
       ("y a esperar que algún día *alcance*.", 79)]),
    P([("Un millonario secreto explica en un video", 186), ("que los antiguos *no pedían así*.", "c:monasterio"),
       ("Primero *despertaban* una parte de la mente", 161), ("que hoy casi todos tenemos *dormida*.", 184),
       ("Y después, simplemente *recibían*.", 87)]),
    P([("Él dice que esa parte se *activa*", 138), ("con un ritual corto de *siete minutos*,", 129),
       ("en *silencio*, en tu casa.", 110)]),
    P([("Un millonario que *no muestra la cara*", 170), ("dice que lo descubrió *por accidente*, hace años,", 114),
       ("y que desde entonces dejó de *rogar*", 154), ("y empezó a *agradecer* antes de recibir.", 82)]),
    P([("Sin cambiar de *religión*.", 97), ("Sin oraciones *nuevas*.", 156), ("Solo cambiando *desde dónde* pides.", 130)]),
    P([("Si sientes que tus oraciones no llegan a *ningún lado*,", 146), ("este video es *para ti*.", 80)]),
])
CORPO["Q"] = ("O segredo apagado dos ensinamentos antigos", [
    P([("Ese secreto no estaba en libros de *autoayuda*.", "c:libro"), ("Estaba escondido en *enseñanzas antiguas*", 151),
       ("que casi nadie llegó a *leer*.", 162)]),
    P([("Hablaba de una parte *oculta* de la mente,", 161), ("una especie de *puerta*", 186),
       ("entre lo que pides y lo que *recibes*.", 80)]),
    P([("Jesús la llamaba el reino *dentro de ti*.", "c:cruz"), ("Buda hablaba de *despertar*.", 154),
       ("Y Tesla decía que todo es *energía* y frecuencia.", 89)]),
    P([("Dicen que con el tiempo ese conocimiento", 93), ("fue *borrado* de las enseñanzas espirituales.", "c:estatua"),
       ("Y que solo unos pocos lo siguieron usando *en silencio*.", 137)]),
    P([("¿Por qué? Porque una persona que *despierta* esa parte", 82), ("deja de *depender* de los demás", 105),
       ("y empieza a *crear* su propio camino.", 94)]),
    P([("Hoy un millonario secreto lo cuenta en un video *corto*.", 175), ("No muestra la *cara*.", 170),
       ("Solo explica cómo *despertar* esa parte,", "c:despertar"), ("con *tres pasos* sencillos", 169),
       ("y un ritual de *siete minutos*.", 129)]),
    P([("No tienes que creer en nada para *verlo*.", 96), ("Solo tienes que verlo *antes* de que lo quiten.", 112)]),
    P([("Dicen que ya intentaron *bajarlo* varias veces.", 127)]),
    CTA(153),
])
CORPO["R"] = ("A peça que falta: 3 passos", [
    P([("Y no es porque *trabajen* más que tú.", 85), ("Ni porque tengan más *suerte*.", 79)]),
    P([("Un millonario secreto cuenta en un video", 175), ("que la ley de atracción tiene una *pieza que falta*.", 119),
       ("Una parte de la *mente* que tiene que estar despierta", 161), ("para que todo lo demás *funcione*.", 92)]),
    P([("Con esa parte *dormida*,", 184), ("visualizas, repites *afirmaciones*,", 169), ("y nada se *mueve*.", 152)]),
    P([("Por eso tanta gente dice que la ley de atracción *no funciona*.", 108), ("Hicieron *todo*", 83),
       ("y se quedaron *esperando*.", 93)]),
    V("Él la despierta con tres pasos sencillos, que muestra uno por uno en el video. Y el primero toma solo siete minutos.",
      {"tipo": "texto", "legenda": False, "frases": [[0, "<k>3</k> PASOS<br>SENCILLOS", "#0d0d0d"],
                                                     ["muestra", "UNO POR <k>UNO</k>", "#101a2e"],
                                                     ["siete", "<k>7</k> MINUTOS", "#0d0d0d"]]}),
    P([("Dice que cuando esa parte *despierta*,", "c:despertar"), ("dejas de *perseguir* las cosas,", 99),
       ("y empiezas a ver *oportunidades*", 94), ("que antes pasaban *frente a ti*.", 127)]),
    P([("Él lo explica *paso a paso*, en un video *corto*,", 168), ("para que lo hagas desde *tu casa*,", 75),
       ("sin cursos caros y sin cambiar tus *creencias*.", 186)]),
    P([("Suena raro, lo sé.", 121), ("Pero son solo *siete minutos*.", 113), ("¿Y si tiene *razón*?", 130),
       ("Míralo hoy, mientras sigue *disponible*.", 128)]),
])
CORPO["S"] = ("A mulher dos 8 mil: o que eu entendi (3ª pessoa)", [
    P([("Ella no hizo nada *mágico*.", 96), ("Llevaba años haciendo lo que todos hacemos:", 169),
       ("pedir, *visualizar*, esperar.", 83), ("Y nada *cambiaba*.", 85)]),
    P([("En el video, un millonario que nunca muestra la *cara*", 170), ("explica algo que nadie me había *dicho*:", 126),
       ("que hay una parte *espiritual* de la mente", 109), ("que en casi todos está *apagada*.", 115)]),
    P([("Y que con esa parte apagada,", 93), ("la abundancia pasa *de largo*.", "c:billete_vuela"),
       ("Como una radio *sin señal*.", 91)]),
    P([("Dice que los antiguos *cristianos*, budistas y egipcios", 154), ("la cuidaban como un *tesoro*.", 80),
       ("Y que hoy casi nadie sabe que *existe*.", 127)]),
    P([("Él muestra cómo *encenderla*", 161), ("con un ritual de *siete minutos*.", 138),
       ("Sin cursos. Sin *meditar* horas.", 141)]),
    P([("Lo primero que ella notó, según contó, fue *calma*.", 110), ("Dejó de vivir *desesperada*", 105),
       ("y empezó a ver *oportunidades* que antes no veía.", 94)]),
    P([("No te voy a *prometer* nada.", 123), ("Pero después de verlo, *entendí*", 82),
       ("por qué a unos pocos todo les llega *fácil*.", 137)]),
])
CORPO["T"] = ("3 sinais novos de que a parte está adormecida", [
    P([("Hay *tres señales*", 119), ("de que una parte de tu mente está *dormida*.", 184)]),
    P([("*Uno*: te despiertas y lo primero que piensas son las *cuentas*.", 95), ("*Dos*: ves a otros *avanzar*,", 127),
       ("mientras tú sigues en el mismo *lugar*.", 146), ("*Tres*: sientes que hay *algo más* para ti,", 82),
       ("pero no sabes cómo *llegar*.", 99)]),
    P([("Si te viste en alguna, *no es tu culpa*.", 126), ("Nadie nos enseñó a *despertar* esa parte.", 186)]),
    P([("Te enseñaron a trabajar *más*,", 85), ("a rezar *más*,", 83), ("a esforzarte *más*.", 152),
       ("Pero nunca te dijeron *por dónde* empezar.", 96)]),
    P([("Él dice que cuando esa parte *despierta*,", "c:despertar"), ("las cosas dejan de *costar* tanto,", 87),
       ("y empiezas a sentir que vas en la *dirección correcta*.", 94)]),
    P([("Un millonario secreto lo explica en un video *corto*.", 175), ("Dice que los antiguos la llamaban", 151),
       ("la *línea directa* con lo divino,", 80), ("y que se despierta con un ritual de *siete minutos*.", 138)]),
    P([("No es *religión*, ni meditación de horas.", 156), ("Es algo que puedes hacer *hoy*, en tu casa.", 75),
       ("Por eso este video te *apareció*.", 153)]),
])
CORPO["U"] = ("A peça que falta na fórmula (pensar positivo não basta)", [
    P([("Te enseñaron a *pensar positivo*,", 169), ("a visualizar, a *agradecer*.", 83),
       ("Y está bien. Pero falta una *pieza*.", 119)]),
    P([("Un millonario secreto la llama", 170), ("*la pieza que falta* en la fórmula.", 92),
       ("Dice que es una parte de la mente", 161), ("que *conecta* lo que deseas con lo que recibes.", 87)]),
    P([("Y que si está *apagada*,", 115), ("puedes pensar positivo *todo el día*,", 172),
       ("y seguir *persiguiendo* lo mismo.", 99)]),
    P([("Es como querer escuchar una *radio* sin señal:", 91), ("puedes subir el *volumen* todo lo que quieras,", 90),
       ("y solo vas a escuchar *ruido*.", 89)]),
    P([("Los antiguos *egipcios* ya hablaban de esto.", 163), ("Los budistas lo llamaban *despertar*.", 154),
       ("Y él dice que hoy se puede hacer en *siete minutos*.", 138)]),
    P([("Él cuenta que lo descubrió *por accidente*,", 114), ("hace muchos *años*,", 93),
       ("y que muy *pocas personas* lo conocen.", 137)]),
    P([("En el video muestra *tres pasos* para despertarla,", 175), ("y un ritual de *siete minutos*.", 129),
       ("Si me equivoco, pierdes siete minutos.", 113), ("¿Y si *tengo razón*?", 130)]),
])
CORPO["V"] = ("O ritual de 7 minutos que os antigos conheciam", [
    P([("No es *magia*.", 121), ("Y no tiene nada que ver con trabajar *más duro*.", 85)]),
    P([("Si llevas años pidiendo, *visualizando*,", 83), ("trabajando *hasta tarde*,", 168),
       ("y sientes que todo sigue *igual*,", 152), ("presta *atención*.", 96)]),
    P([("Es un ritual que los antiguos *egipcios*,", 163), ("*budistas* y cristianos conocían,", 154),
       ("para despertar una parte de la *mente*", 161), ("que hoy está *dormida* en casi todos.", 184)]),
    P([("Un millonario secreto lo muestra en un *video*.", 170), ("Dice que lo hace cada *mañana*,", 95),
       ("con los ojos *cerrados*,", 138), ("durante *siete minutos*.", 129)]),
    P([("Y que desde entonces dejó de *perseguir* el dinero.", "c:billete_vuela"),
       ("Cuenta que ahora las *oportunidades* lo encuentran a él.", 137)]),
    P([("Dice que la *élite* lo guarda para sí,", 142), ("y que por eso casi *nadie* habla de esto.", 186)]),
    P([("No te pide que dejes tu *fe*.", 157), ("No te pide *dinero* para ver el video.", 113),
       ("Solo siete minutos de tu *tiempo*.", 93)]),
    P([("Míralo con *calma*, y decide tú.", 110), ("Pero no lo dejes para *después*.", 128)]),
])
CORPO["W"] = ("Inimigo comum: a gente boa que trabalha mais e recebe menos", [
    P([("Dijo que la gente *buena*", 126), ("es la que *más trabaja*", 85), ("y la que *menos recibe*.", 152),
       ("Y me sentí *identificada*.", 146)]),
    P([("Toda la vida hice lo *correcto*.", 169), ("Trabajar, ahorrar, *esperar* mi turno.", 93),
       ("Y el turno nunca *llegó*.", 113)]),
    P([("Y no lo digo con *rabia*.", 107), ("Lo digo porque por fin alguien me explicó *por qué*.", 82)]),
    P([("Él dice que no es *falta de esfuerzo*.", 105), ("Que hay una parte de la mente", 161),
       ("que los antiguos *cuidaban*,", "c:monasterio"), ("y que a nosotros nunca nos enseñaron a *usar*.", 186)]),
    P([("Y que unos pocos la usan *en silencio*,", 137), ("mientras los demás seguimos *corriendo*.", 99)]),
    P([("Dice que esa parte de la mente *conecta*", 80), ("lo que pides con lo que *llega* a tu vida,", 87),
       ("y que cuando está *dormida*,", 184), ("todo te cuesta el *doble*.", 108)]),
    P([("No es *religión*.", 156), ("No es pensar *positivo*.", 172), ("Es algo que los antiguos *sabían*.", 151)]),
    P([("Muestra cómo *despertarla*", 138), ("con un ritual de *siete minutos*.", 129),
       ("Yo todavía estoy *procesando* todo.", 115), ("Pero tenía que *contártelo*.", 96)]),
    P([("Si a ti también te pasa,", 128), ("míralo antes de que lo *quiten*.", 153)]),
])
CORPO["X"] = ("Objeção: 'é golpe' (cético, baixo risco)", [
    P([("Yo también pensé que era otra *estafa*.", 96), ("De esas que te prometen hacerte rico *en una semana*.", 102),
       ("Pero *no*.", 187)]),
    P([("Es un millonario que *no muestra la cara*,", 170), ("y que no te pide nada para *ver* el video.", 175),
       ("Habla de algo que los *antiguos* sabían:", 151), ("una parte de la mente que, *dormida*,", 184),
       ("hace que todo te cueste el *doble*.", 152)]),
    P([("Dice que esa parte la cuidaban los *cristianos*, los budistas y los *egipcios*,", 154),
       ("y que hoy casi nadie la *usa*.", 127)]),
    P([("Y explica cómo *despertarla*", "c:despertar"), ("con un ritual de *siete minutos*.", 138),
       ("Sin dejar tu *fe*,", 157), ("sin meditar *horas*.", 112)]),
    P([("Lo que más me *llamó la atención*:", 121), ("no te dice que *dejes* de trabajar,", 85),
       ("ni que el dinero va a caer del *cielo*.", 114), ("Te dice que *despiertes* primero.", 82)]),
    P([("¿Funciona para todos? *No lo sé*.", 126), ("Pero son siete minutos.", 129),
       ("Y lo que me hizo pensar, ya *valió la pena*.", 130),
       ("Míralo y saca tus propias *conclusiones*.", 128)]),
    CTA(80),
])
CORPO["Y"] = ("Pare de perseguir (trocar tempo por dinheiro)", [
    P([("Es que estás *persiguiendo*.", 99), ("Y lo que persigues, *se aleja*.", "c:billete_vuela")]),
    P([("Un millonario secreto dice que pasó *años* así:", 93), ("en una casa que *no le gustaba*,", 85),
       ("cambiando *tiempo por dinero*.", 129), ("Hasta que descubrió algo *por accidente*.", 122)]),
    P([("Igual que tú, quizás:", 126), ("trabajando *más*, durmiendo *menos*,", 168), ("y sintiendo que *nunca alcanza*.", 79)]),
    P([("Una parte *adormecida* de la mente", 184), ("que, cuando *despierta*,", "c:despertar"),
       ("cambia la forma en que ves las *oportunidades*.", 94), ("Dejas de ir detrás de todo,", 172),
       ("y empiezas a *recibir*.", 87)]),
    P([("No tiene nada que ver con trabajar más *duro*,", 171), ("ni con ser más *inteligente*.", 169),
       ("Él dice que los que están *arriba* lo saben,", 137), ("y por eso casi *nadie* lo cuenta.", 186)]),
    P([("Y no te pide nada para *verlo*.", 175)]),
    V("Él lo resume en tres pasos. Y lo muestra en un video corto, antes de que lo quiten.",
      {"tipo": "texto", "legenda": False, "frases": [[0, "<k>3</k> PASOS", "#0d0d0d"], ["video", "UN VIDEO <k>CORTO</k>", "#101a2e"],
                                                     ["quiten", "ANTES DE QUE LO <k>QUITEN</k>", "#2a0d0d"]]}),
    CTA(142),
])
CORPO["Z"] = ("Fé: 'o reino de Deus está dentro de ti'", [
    P([("No es contra la *fe*.", 157), ("Al contrario.", 97), ("Jesús decía que el reino de Dios está *dentro de ti*.", "c:cruz"),
       ("Y casi nadie se detuvo a pensar qué *significaba*.", 126)]),
    P([("Un millonario secreto explica en un video", 170), ("que esa frase hablaba de una parte de la *mente*", 161),
       ("que los antiguos cristianos, budistas y egipcios", 154), ("consideraban *sagrada*.", 162)]),
    P([("Cuando está *dormida*,", 184), ("rezas pidiendo lo que *falta*,", 83), ("y sigues sintiendo que *falta*.", 85)]),
    P([("No es que Dios no te *escuche*.", 115), ("Es que pides con una parte *apagada*,", 108),
       ("como quien habla con la línea *desconectada*.", 91)]),
    P([("Cuando *despierta*, dice él,", 82), ("dejas de pedir desde el *miedo*", 105),
       ("y empiezas a ver lo que ya está *frente a ti*.", 94)]),
    P([("Los antiguos lo practicaban en *silencio*,", "c:monasterio"), ("en templos y *monasterios*.", "c:estatua"),
       ("Y hoy, él lo enseña para hacerlo *en casa*.", 75)]),
    P([("Lo hace con un ritual de *siete minutos*.", 138), ("Y no tienes que dejar tu *iglesia*", 186),
       ("ni tu forma de *creer*.", 153)]),
    P([("Y si tú también sientes que *rezas* y nada cambia,", 146), ("este video te va a *abrir los ojos*.", 130)]),
    CTA(119),
])
CORPO["AA"] = ("Rotina: trabalhar mais não é a resposta", [
    P([("Piensa en tu *rutina*.", 85), ("Te levantas *cansado*,", 95), ("trabajas todo el día,", 168),
       ("y a fin de mes el dinero *no alcanza*.", 79)]),
    P([("Y cuando intentas *cambiar*,", 152), ("lees libros, haces *afirmaciones*,", 169), ("te esfuerzas *más*…", 105),
       ("y vuelves al *mismo lugar*.", 99)]),
    P([("Ahora piensa en alguien que vive *tranquilo*,", 110), ("que tiene *tiempo* para su familia,", 141),
       ("y aun así le va *bien*.", 142), ("No es que trabaje *más* que tú.", 171)]),
    P([("Un millonario secreto dice que la *diferencia*", 170), ("está en una parte de la mente", 161),
       ("que los antiguos llamaban la *conexión* con lo divino.", 80), ("Y que se puede *encender*.", 92)]),
    P([("Dice que los antiguos *egipcios* y budistas", 163), ("la despertaban con un *ritual* sencillo,", 138),
       ("y que él lo hace cada *mañana*", 82), ("antes de empezar el *día*.", 114)]),
    P([("En un video corto, él muestra *cómo*,", 175), ("con *tres pasos* y un ritual de siete minutos.", 129),
       ("No hace falta *creerle*.", 96), ("Solo *mirarlo*.", 153)]),
    P([("Si me equivoco, solo pierdes *siete minutos*.", 113), ("¿Y si tiene *razón*?", 130)]),
])

G = {}
G["zap"] = V("Mi hermana me mandó esto anoche. ¿Viste el video del millonario? ¿Otro de esos de hacerse rico? No es eso. Habla de una parte de la mente que está *dormida*.",
             {"tipo": "zap", "nome": "Hermana 💜", "foto": "👩", "selo": "ejemplo",
              "msgs": [{"quem": "dele", "txt": "¿Viste el video del millonario que te pasé? 👀", "em": "Viste", "hora": "23:10", "alt": 170},
                       {"quem": "dela", "txt": "¿Otro de esos de hacerse rico? 🙄", "em": "Otro", "hora": "23:11", "alt": 150},
                       {"quem": "dele", "txt": "No es eso. Habla de una parte de la mente que está dormida", "em": "No", "hora": "23:11"}]},
             leg_topo=1010)
G["busca"] = V("Si alguna vez buscaste esto a medianoche, *escucha*.",
               {"tipo": "busca", "consulta": "por qué rezo y nada cambia", "digitar_ate": "medianoche",
                "resultados": [["foro", "Rezo todos los días y siento que nadie me escucha", "Ya no sé qué más hacer…"],
                               ["preguntas", "¿Por qué a unos todo les llega fácil?", "Trabajo más que nunca y no alcanza"],
                               ["video", "El video que muchos quieren borrar", "Un millonario explica lo que nadie dice…"]]}, leg_topo=1010)
G["noticia"] = V("*Descubierto*. El secreto que Jesús, Buda y Tesla conocían, y que según un millonario, intentaron *borrar*.",
                 {"tipo": "noticia", "fundo": 163, "tarja": "DESCUBIERTO", "canal": "NOTICIAS DE HOY",
                  "manchetes": [[0, "EL SECRETO QUE INTENTARON BORRAR"], ["millonario", "UN MILLONARIO LO CUENTA EN UN VIDEO"]],
                  "letreiro": "dramatización · el video del millonario secreto · antes de que lo quiten · "})
G["texto"] = V("Trabajas más que nunca. Y el dinero se va más rápido que nunca. No es mala *suerte*.",
               {"tipo": "texto", "legenda": False, "frases": [[0, "TRABAJAS <k>MÁS</k><br>QUE NUNCA", "#0d0d0d"],
                                                              ["dinero", "Y EL DINERO<br><k>SE VA</k>", "#101a2e"],
                                                              ["mala", "NO ES<br><k>MALA SUERTE</k>", "#2a0d0d"]]})
G["viral"] = V("Dicen que hay un video que hace que la gente deje de rezar por dinero. Y la razón *tiene sentido*.",
               {"tipo": "viral", "tag": "INSÓLITO", "manchete": "El video que hace que la gente deje de rezar por dinero",
                "fundo": 156, "twist": "Y LA RAZÓN<br>TIENE SENTIDO", "twist_em": "razón", "selo": "dramatización"})
G["egipto"] = P([("Hace miles de años, en *Egipto*,", 163), ("los sacerdotes sabían algo", 151),
                 ("que hoy solo usan los *millonarios*.", 137), ("Y no es lo que *piensas*.", 153)])

LOTE = [
    ("01", "pregador no palco (gancho campeão #2)", ("cab", "k2", "Deja de rezar por bendiciones. Rezar por bendiciones es el problema."), "P", "VC2", "02"),
    ("02", "narração com imagens (gancho campeão #3)", ("cab", "k3", "Jesús, Tesla y Buda descubrieron exactamente el mismo secreto…"), "Q", "VC3", None),
    ("03", "podcast, apresentadora (gancho campeão #4)", ("cab", "k4", "La ley de atracción funciona para millonarios y celebridades, pero no para todos los demás."), "R", "VC4", "10"),
    ("04", "UGC selfie no carro (Avatar IV já pago)", ("cab", "CA01", "Una mujer contó que manifestó 8 mil dólares por accidente… cuando vi el video que ella vio, entendí por qué."), "S", "VC1", "01"),
    ("05", "UGC selfie no carro (Avatar IV já pago)", ("cab", "CA05", "Si este video te apareció hoy, no es coincidencia. Quédate 30 segundos."), "T", "sara", "05"),
    ("06", "podcast, apresentador homem (Avatar IV já pago)", ("cab", "CA12", "La ley de atracción sí funciona, pero solo para los que saben esto."), "U", "diego", "12"),
    ("07", "UGC na praia (Avatar IV já pago)", ("cab", "CA19", "¿Sabías que hay un ritual de siete minutos que los millonarios no quieren que conozcas?"), "V", "daniela", "19"),
    ("08", "UGC à noite (Avatar IV já pago)", ("cab", "CA04", "Son las tres de la mañana y no puedo dormir, por algo que dijo un millonario en un video."), "W", "hope", "04"),
    ("09", "conversa de WhatsApp (irmã)", ("tela", "zap", "Mi hermana me mandó esto anoche…"), "X", "lucia", None),
    ("10", "interface de busca", ("tela", "busca", "Si alguna vez buscaste esto a medianoche, escucha. ('por qué rezo y nada cambia')"), "P", "VC2", None),
    ("11", "simulação de notícia DESCUBIERTO", ("tela", "noticia", "Descubierto: el secreto que Jesús, Buda y Tesla conocían…"), "Q", "VC3", None),
    ("12", "texto grande + música (mini VSL)", ("tela", "texto", "Trabajas más que nunca. Y el dinero se va más rápido que nunca. No es mala suerte."), "Y", "diego", None),
    ("13", "notícia absurda + reviravolta", ("tela", "viral", "Dicen que hay un video que hace que la gente deje de rezar por dinero…"), "Z", "lucia", None),
    ("14", "gancho histórico (Egito)", ("tela", "egipto", "Hace miles de años, en Egipto, los sacerdotes sabían algo que hoy solo usan los millonarios."), "R", "VC4", "10"),
    ("15", "podcast, apresentadora (Avatar IV já pago)", ("cab", "CA13", "Los millonarios no trabajan más duro que tú. Tienen encendida una parte de la mente que tú tienes apagada."), "AA", "VC4", "13"),
]

PRIMARY = {
    "P": "¿Sientes que tus oraciones no llegan a ningún lado? 🙏 Tal vez el problema es desde dónde pides. Mira el video corto 👇",
    "Q": "Un secreto antiguo que, dicen, intentaron borrar. 📜 Un millonario secreto lo cuenta en un video corto. Míralo antes de que lo quiten 👇",
    "R": "La ley de atracción tiene una pieza que falta. 🧩 3 pasos y 7 minutos. Mira el video corto 👇",
    "S": "Ella no hizo nada mágico… pero vio un video extraño. 😳 Míralo y saca tus conclusiones 👇",
    "T": "3 señales de que una parte de tu mente está dormida. ¿Te viste en alguna? 👀 Mira el video corto 👇",
    "U": "Pensar positivo no basta: falta una pieza. 🔑 Mira el video corto del millonario secreto 👇",
    "V": "Un ritual de 7 minutos que los antiguos conocían. 🌅 Míralo con calma y decide tú 👇",
    "W": "La gente buena es la que más trabaja y menos recibe. ¿Por qué? 🌙 Mira el video corto 👇",
    "X": "Yo también pensé que era otra estafa. Son 7 minutos… y no te piden nada para verlo 👇",
    "Y": "Deja de perseguir. Lo que persigues se aleja. 🏃 Mira el video corto antes de que lo quiten 👇",
    "Z": "'El reino de Dios está dentro de ti.' ¿Y si era literal? ✨ Mira el video corto 👇",
    "AA": "Los millonarios no trabajan más duro que tú. 🧠 La diferencia está en otra parte. Mira el video corto 👇",
}


# cortes que ficam com meia tela vazia (notebook), estrada vazia, janela clara ou parede: trocados por imagem com o mesmo sentido
RUINS = {"b:85": ["b:152", "b:105", "b:108", "b:146", "b:183", "b:118", "b:107"],
         "c:despertar": ["b:95", "b:82", "b:130", "b:187"],
         "b:99": ["b:172", "b:94", "b:87", "b:110"],
         "c:libro": ["b:78", "b:151", "b:162"]}


def trocar(cr):
    usados = {p[1] for b in cr["blocos"] for p in b.get("partes", [])} | \
             {b.get("visual", {}).get("fundo") for b in cr["blocos"]}
    for b in cr["blocos"]:
        for p in b.get("partes", []):
            if p[1] in RUINS:
                novo = next(x for x in RUINS[p[1]] if x not in usados)
                usados.add(novo)
                p[1] = novo


def main():
    crs = []
    for i, formato, (tipo, k, gtxt), corpo, voz, cauda in LOTE:
        nome, blocos = CORPO[corpo]
        blocos = json.loads(json.dumps(blocos))
        if cauda is None and blocos[-1].get("visual", {}).get("tipo") != "cta":
            usados = {q[1] for b in blocos for q in b.get("partes", [])} | \
                     {q[1] for q in (G.get(k, {}).get("partes") or [])} | {G.get(k, {}).get("visual", {}).get("fundo")}
            f = next(x for x in (80, 153, 119, 142, 75, 128) if f"b:{x}" not in usados)
            blocos.append(json.loads(json.dumps(CTA(f))))
        cr = {"id": i, "formato": formato, "angulo": nome, "corpo": corpo, "gancho": gtxt, "voz": voz,
              "primary_text": PRIMARY[corpo], "blocos": blocos}
        if tipo == "cab":
            cr["cabeca"] = HEAD[k]
        else:
            cr["blocos"].insert(0, json.loads(json.dumps(G[k])))
        if cauda:
            cr["cauda"] = CAUDA[cauda]
        trocar(cr)
        crs.append(cr)
    conferir(crs)
    base = json.load(open(os.path.join(AQUI, "codigo-alfa-lote-1.json")))
    plano = {"produto": "codigo-alfa", "titulo": "Código Alfa · Lote 2", "banco": "banco/indice.json",
             "limites": {"b:161": [0.0, 4.6], "b:185": [0.0, 3.0]}, "campeoes": base["campeoes"],
             "brolls": {k: v + ["alto"] for k, v in CORTES.items()}, "vozes": base["vozes"], "criativos": crs}
    json.dump(plano, open(os.path.join(AQUI, "codigo-alfa-lote-2.json"), "w"), ensure_ascii=False, indent=1)
    print(len(crs), "criativos")


if __name__ == "__main__":
    main()
