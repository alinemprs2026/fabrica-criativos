# 21 Frases Secretas — Lote 3 (Flow): 30 criativos 100% novos, 1 a 1,5 min, avatar Daniel + voz clonada do Daniel.
# Gera pipeline/lotes/21-frases-lote-3-flow.json.  Base: VSL "La frase de 2 palabras" + pesquisa de concorrentes (16/11/2026).
# Tipos de cena (cada cena = 1 fala de até ~8 s):
#   D = Daniel falando para a câmera (Flow, imagem de referência do Daniel; a boca segue a fala; o áudio final é a voz clonada)
#   B = cena de apoio gerada no Flow (sem Daniel falando), com a voz do Daniel por cima
#   Z = tela de conversa de WhatsApp (feita no HyperFrames, grátis)   ·   T = texto grande na tela (HyperFrames)
import json, os
CTA_FINAL = "Toca en 'Más información' y mira el video completo. Ahí te enseño las 21 frases, gratis, antes de que lo quiten."
def D(fala, cena="estudio"): return {"t": "D", "fala": fala, "cena": cena}
def B(fala, prompt): return {"t": "B", "fala": fala, "prompt": prompt}
def Z(fala, msgs): return {"t": "Z", "fala": fala, "msgs": msgs}
def T(fala, texto): return {"t": "T", "fala": fala, "texto": texto}
CEN = {
    "estudio": "home office with plants and a desk lamp, holding a small black microphone, black sweater, medium close-up, vertical 9:16",
    "podcast": "podcast studio, large studio microphone on an arm, warm lights, acoustic panels, black sweater, vertical 9:16",
    "carro": "sitting in the driver seat of a parked car, selfie-style handheld vertical video, daylight, black sweater",
    "calle": "walking on a sunny city sidewalk, handheld selfie vertical video, casual, black sweater",
    "cafe": "sitting in a cozy cafe by the window, coffee cup on the table, medium shot, vertical 9:16, black sweater",
    "noche": "sitting on a sofa at night, warm lamp light, intimate tone, vertical 9:16, black sweater",
    "escenario": "standing on a small stage with a spotlight, speaking to an audience, vertical 9:16, black blazer",
}
C = []
def cr(id_, titulo, formato, angulo, gancho, cenas, texto_anuncio):
    C.append(dict(id=id_, titulo=titulo, formato=formato, angulo=angulo, gancho=gancho, cenas=cenas, primary_text=texto_anuncio))

W_TRISTE = "a woman in her 30s sitting on her bed at night staring at her phone, sad, dim light, cinematic, vertical 9:16"
W_FELIZ = "a woman in her 30s smiling at her phone notification in a bright living room, cinematic, vertical 9:16"
M_CEL = "a handsome man in his 30s reading a text message on his phone and smiling, interested, cinematic, vertical 9:16"
M_FRIO = "a man in his 30s glancing at his phone and putting it down, uninterested, cinematic, vertical 9:16"

# ---------------------------------------------------------------- FAMÍLIA 1: "Si yo fuera mujer…" (modelagem do campeão BR)
cr("01", "Si yo fuera mujer y estuviera soltera", "apresentador", "frases por etapa", "Si yo fuera mujer y estuviera soltera en 2026…", [
    D("Si yo fuera mujer y estuviera soltera en 2026, aprendería a escribirle a un hombre de una sola forma."),
    D("Y no, no es con fotos, ni con mensajes largos, ni contestando rápido."),
    D("Es con frases cortas que hablan en lo que yo llamo la frecuencia masculina."),
    T("¿Quieres que deje de ignorarte?", "¿QUIERES QUE DEJE DE IGNORARTE?"),
    D("¿Quieres que deje de ignorarte? Hay una frase de atracción para eso."),
    D("¿Quieres que no pueda sacarte de su cabeza? Hay una frase de obsesión."),
    D("¿Quieres que por fin te presente como su pareja? Hay una frase de compromiso."),
    D("¿Y si ya se enfrió o desapareció? Hay una frase de rescate."),
    D("Las copias, las pegas, las envías. Así de simple. Son 21 en total."),
    D(CTA_FINAL),
], "Si yo fuera mujer, aprendería esto antes que cualquier otra cosa 👇 21 frases cortas para cada etapa: atracción, obsesión, compromiso y rescate.")
cr("02", "Si yo fuera mujer — versão carro", "UGC carro", "frases por etapa", "Si yo fuera mujer, haría esto con el hombre que me gusta…", [
    D("Si yo fuera mujer, haría esto con el hombre que me gusta. Y te lo digo como hombre.", "carro"),
    D("Dejaría de mandarle buenos días todos los días. Eso no lo enamora, lo aburre.", "carro"),
    D("Dejaría de hacerle preguntas tipo entrevista. ¿De dónde eres? ¿A qué te dedicas?", "carro"),
    D("Y sobre todo, nunca le reclamaría por desaparecer. Eso lo aleja todavía más.", "carro"),
    B("En lugar de eso, usaría frases cortas que despiertan su lado masculino.", M_CEL),
    D("Frases que lo retan, que le dan curiosidad y que lo hacen querer ganarse tu atención.", "carro"),
    D("Yo junté 21 de esas frases durante más de diez años. Para cada etapa de la relación.", "carro"),
    D("Desde que se están conociendo hasta cuando él se enfría o desaparece.", "carro"),
    D(CTA_FINAL, "carro"),
], "Te lo digo como hombre: si yo fuera mujer, dejaría de hacer estas 3 cosas hoy mismo.")
cr("03", "Si yo fuera mujer — 3 erros", "split erro × acerto", "erros que afastam", "Si yo fuera mujer, nunca le mandaría estos 3 mensajes a un hombre", [
    D("Si yo fuera mujer, nunca le mandaría estos tres mensajes a un hombre."),
    Z("Primero: el buenos días de compromiso. Él contesta por educación y se olvida en treinta segundos.", [("ella", "Buenos días 😊 ¿cómo amaneciste?"), ("el", "Bien y tú")]),
    Z("Segundo: el interrogatorio. Él siente que está en una entrevista de trabajo.", [("ella", "¿De dónde eres? ¿Cuántos años tienes? ¿A qué te dedicas?"), ("el", "jaja muchas preguntas")]),
    Z("Y el peor de todos: el reclamo. Ese hace que quiera irse en cuestión de horas.", [("ella", "¿Por qué desapareciste? ¿Ya no te importo?"), ("visto", "")]),
    D("Cuando un hombre lee un reclamo, no escucha amor. Escucha a una mamá regañando a un niño."),
    D("Y ningún hombre quiere sentirse un niño. Quiere sentirse un hombre."),
    D("Por eso existen frases que hablan en su frecuencia. Cortas, simples y sin reclamos."),
    D("Yo te enseño 21 de esas frases. Para cada momento de la relación."),
    D(CTA_FINAL),
], "Estos 3 mensajes alejan a cualquier hombre. El tercero es el que más mujeres envían.")

# ---------------------------------------------------------------- FAMÍLIA 2: "Lo que ningún hombre te va a admitir" (confissão masculina)
cr("04", "Lo que ningún hombre te va a admitir", "podcast", "confissão masculina", "Te voy a decir algo que ningún hombre te va a admitir…", [
    D("Te voy a decir algo que ningún hombre te va a admitir en voz alta.", "podcast"),
    D("Cuando un hombre se aleja, casi nunca es porque no le gustes.", "podcast"),
    D("Es porque la forma en que le hablas no le despierta nada por dentro.", "podcast"),
    D("Desde niños nos repiten: pórtate como hombre, los hombres no lloran, resuelve.", "podcast"),
    D("Y eso deja una necesidad muy profunda: sentirnos más hombres.", "podcast"),
    D("La mujer que despierta esa sensación en él es la mujer de la que no puede olvidarse.", "podcast"),
    B("Y para eso no necesitas ser más bonita, ni más joven. Necesitas las palabras correctas.", W_FELIZ),
    D("Yo lo llamo la frecuencia masculina. Y cabe en frases de dos o tres palabras.", "podcast"),
    D(CTA_FINAL, "podcast"),
], "Lo que ningún hombre te va a admitir en voz alta (y explica por qué se aleja) 👇")
cr("05", "Fui mujeriego 6 anos", "apresentador noite", "confissão masculina", "Fui mujeriego durante 6 años. Y todas las mujeres cometían el mismo error.", [
    D("Fui mujeriego durante casi seis años. Y todas las mujeres que dejé cometían el mismo error.", "noche"),
    D("No eran feas, ni aburridas. Eran lindas, inteligentes, con metas.", "noche"),
    D("Pero me hablaban en una frecuencia que no conectaba conmigo.", "noche"),
    B("Mensajes amables, disponibles todo el tiempo, contestando en un segundo.", W_TRISTE),
    D("Y una semana después, yo ya había perdido el interés. Sin saber explicar por qué.", "noche"),
    D("Hasta que una mujer me escribió algo distinto. Corto. Sin necesidad. Sin reclamo.", "noche"),
    D("Dejé mi vida de soltero por ella. Hoy es la madre de mis tres hijos.", "noche"),
    D("Esa forma de hablar tiene reglas. Y las junté en 21 frases.", "noche"),
    D(CTA_FINAL, "noche"),
], "Fui mujeriego 6 años. Esto es lo que hacían TODAS las mujeres que dejé 😶")
cr("06", "O que os homens falam entre eles", "UGC rua", "confissão masculina", "¿Sabes lo que hablamos los hombres de ti cuando no estás?", [
    D("¿Sabes lo que hablamos los hombres de una mujer cuando ella no está?", "calle"),
    D("Casi nunca hablamos de su cuerpo. Hablamos de cómo nos hace sentir.", "calle"),
    D("Si un amigo dice: 'conocí a una mujer diferente', es porque ella le habló distinto.", "calle"),
    B("No le escribió lo mismo que las otras cincuenta. Le escribió algo que lo retó.", M_CEL),
    D("Y cuando un hombre se siente retado, empieza a invertir. A buscarte. A planear la próxima cita.", "calle"),
    D("Eso no es suerte. Es hablarle en su frecuencia.", "calle"),
    D("Te puedo enseñar exactamente qué escribir para que él diga eso de ti.", "calle"),
    D(CTA_FINAL, "calle"),
], "Lo que dice un hombre a sus amigos cuando una mujer le gusta de verdad…")

# ---------------------------------------------------------------- FAMÍLIA 3: "Todavía no" (dar a frase de graça)
cr("07", "A frase de 2 palavras: todavía no", "apresentador", "prova grátis: todavía no", "Hay 2 palabras que hacen que un hombre quiera ganarte", [
    D("Hay dos palabras que hacen que un hombre quiera ganarse tu lugar. Te las voy a regalar."),
    B("Imagina: la cita fue increíble y al despedirse, él intenta besarte.", "a couple saying goodbye at night outside a restaurant, the man leaning in for a kiss, cinematic, vertical 9:16"),
    D("Si le dices 'no', él siente rechazo. La mayoría se rinde ahí mismo."),
    D("Si le dices 'calma, es muy pronto', estás pensando como mujer. En su mente no despierta nada."),
    T("Las 2 palabras:", "«TODAVÍA NO»"),
    D("Pero si le dices 'todavía no'… él no lo escucha como rechazo. Lo escucha como un reto."),
    D("Ese 'todavía' le dice que hay un futuro, pero que se lo tiene que ganar."),
    D("Y un hombre retado empieza a buscarte, a invertir, a planear la próxima cita."),
    D("Esa es una. Tengo otras 20 iguales de poderosas."),
    D(CTA_FINAL),
], "Te regalo 2 palabras que hacen que un hombre quiera ganarse tu lugar 👇 (las otras 20 están en el video)")
cr("08", "Todavía no — reação dele", "split cena", "prova grátis: todavía no", "No le digas 'no'. Dile esto.", [
    D("No le digas 'no' a un hombre. Y tampoco le digas 'es muy pronto'. Dile esto.", "cafe"),
    T("", "«TODAVÍA NO»"),
    D("Todavía no. Dos palabras. Y cambian todo lo que pasa en su cabeza.", "cafe"),
    B("Porque el hombre está programado para responder a los retos.", "a confident man smiling and thinking while walking at sunset, cinematic, vertical 9:16"),
    D("En la naturaleza, ningún macho conquista sin demostrar que lo merece.", "cafe"),
    D("Cuando dices 'todavía no', dejas de ser la mujer que lo rechaza.", "cafe"),
    D("Te conviertes en la mujer que él quiere conquistar.", "cafe"),
    B("Y empieza a escribirte, a llamarte, a buscar cualquier excusa para verte.", M_CEL),
    D("Esa frase es una de las 21 que te enseño. Cada una para un momento distinto.", "cafe"),
    D(CTA_FINAL, "cafe"),
], "No le digas 'no'. Tampoco 'es muy pronto'. Dile estas 2 palabras.")
cr("09", "Todavía no — WhatsApp", "WhatsApp", "prova grátis: todavía no", "Ella le respondió 2 palabras y él no pudo dejar de pensar en ella", [
    Z("Mira esta conversación. Él le pidió verla esta noche.", [("el", "¿Te veo hoy en la noche? 😏")]),
    Z("La mayoría contestaría 'sí' en un segundo. O 'no puedo'. Ella respondió así.", [("el", "¿Te veo hoy en la noche? 😏"), ("ella", "Todavía no 😌")]),
    D("Todavía no. Dos palabras. Y él no pudo dejar de pensar en ella en toda la noche."),
    D("Porque ese 'todavía' le dice que sí hay un futuro. Pero que tiene que ganárselo."),
    Z("Y mira lo que pasó después.", [("ella", "Todavía no 😌"), ("el", "Jaja ok… ¿y qué tengo que hacer para ganarme el sí?")]),
    D("Eso es hablarle en su frecuencia. Él ya no se siente rechazado. Se siente retado."),
    D("Tengo 21 frases así. Para que te escriba, para que no te olvide y para que se comprometa."),
    D(CTA_FINAL),
], "Ella le respondió 2 palabras… y él no pudo dejar de pensar en ella 👀")

# ---------------------------------------------------------------- FAMÍLIA 4: "Te amo" × "Estoy contigo"
cr("10", "No le digas te amo", "apresentador", "idioma masculino", "Deja de decirle 'te amo'. Dile esto.", [
    D("Deja de decirle 'te amo' a un hombre. Y no porque esté mal."),
    D("Es que 'te amo' es una frase que hace sentir amada a una mujer. No a un hombre."),
    D("Las mujeres crecen valorando la conexión. Los hombres, el honor, la lealtad y el desafío."),
    T("Para él pesa más:", "«ESTOY CONTIGO»"),
    D("Por eso, para un hombre, 'estoy contigo' pesa mucho más que 'te amo'."),
    D("Porque habla de lealtad. De compañerismo. De caminar juntos."),
    B("Es como hablarle en chino a alguien que solo entiende español. Pueden reír, pero nunca conectan.", "a man and a woman on a date, smiling politely but disconnected, cinematic, vertical 9:16"),
    D("Cuando aprendes su idioma, él siente que eres diferente a todas."),
    D("Te enseño 21 frases en ese idioma."),
    D(CTA_FINAL),
], "'Te amo' no hace que un hombre se quede. Esta frase sí 👇")
cr("11", "Idioma errado — chinês", "narração com cenas", "idioma masculino", "Le estás hablando en chino a ese hombre", [
    B("Le estás hablando en chino a ese hombre. Y él solo entiende español.", W_TRISTE),
    D("Por eso le escribes con todo tu cariño… y él contesta frío. O no contesta.", "noche"),
    D("No es que no le gustes. Es que le hablas en tu frecuencia, no en la suya.", "noche"),
    B("Y ahí empieza el círculo: él se enfría, tú escribes con más intensidad, él se aleja más.", M_FRIO),
    D("Hasta que un día desaparece. Y tú te quedas leyendo la conversación a las tres de la mañana.", "noche"),
    D("La respuesta a '¿en qué fallé?' es: en nada. Solo usaste el idioma equivocado.", "noche"),
    D("Aprender el idioma correcto es más fácil de lo que crees. Son frases cortas.", "noche"),
    D(CTA_FINAL, "noche"),
], "No es que no le gustes. Le estás hablando en un idioma que él no entiende.")
cr("12", "O hombre que te enamoró sin entender como", "podcast", "idioma masculino", "¿Alguna vez un hombre te enamoró y no supiste cómo?", [
    D("¿Alguna vez un hombre te enamoró sin que entendieras cómo lo hizo?", "podcast"),
    D("No era el más guapo, ni el más exitoso. Pero sabía exactamente qué decirte.", "podcast"),
    D("Él hablaba en tu idioma. En la frecuencia femenina.", "podcast"),
    D("Ahora imagina hacer lo mismo, pero al revés. Con el hombre que tú quieres.", "podcast"),
    B("Que él sienta que tú eres diferente a todas las que conoció.", M_CEL),
    D("Eso no depende de tu cara, ni de tu edad. Depende de tus palabras.", "podcast"),
    D("Y esas palabras se aprenden. Yo te enseño 21.", "podcast"),
    D(CTA_FINAL, "podcast"),
], "Ese hombre que te enamoró sin entender cómo… sabía hablar tu idioma. Ahora aprende el suyo.")

# ---------------------------------------------------------------- FAMÍLIA 5: gancho invertido
cr("13", "No uses esta frase", "apresentador", "gancho invertido", "No uses esta frase si no quieres que se obsesione contigo", [
    D("No uses esta frase si no quieres que un hombre se obsesione contigo. Lo digo en serio."),
    D("Porque cuando la usas bien, él empieza a escribirte primero. Todos los días."),
    D("Deja planes con sus amigos para hablar contigo. Te nombra delante de ellos."),
    D("Y no tiene nada que ver con tu cuerpo, ni con fotos, ni con ser más joven."),
    D("Tiene que ver con hablarle en la frecuencia masculina."),
    B("Una frase corta, en el momento exacto, que despierta su instinto de conquistar.", M_CEL),
    D("La llamo frase de obsesión. Y es solo una de las cuatro categorías que te enseño."),
    D("Atracción, obsesión, compromiso y rescate. 21 frases en total."),
    D(CTA_FINAL),
], "⚠️ No uses esta frase si no quieres que se obsesione contigo.")
cr("14", "Não mande essa mensagem", "WhatsApp", "gancho invertido", "Si mandas este mensaje, él se va a alejar", [
    D("Si le mandas este mensaje a un hombre, se va a alejar. Te lo garantizo como hombre.", "carro"),
    Z("Este. El de '¿por qué desapareciste?'.", [("ella", "¿Por qué desapareciste? Ni un mensaje en 3 días…")]),
    D("Tú lo escribes por preocupación. Por amor. Pero él no lee eso.", "carro"),
    D("Él lee a su mamá regañándolo por llegar tarde. Y nadie quiere volver con su mamá.", "carro"),
    Z("Ahora mira lo que pasa si le escribes otra cosa.", [("ella", "Me acordé de ti hoy 🙂 tengo algo que contarte"), ("el", "¿Qué cosa? 👀 cuéntame")]),
    D("Curiosidad en lugar de reclamo. Él responde en segundos.", "carro"),
    D("Tengo 21 frases así. Y una sección entera para cuando él desaparece.", "carro"),
    D(CTA_FINAL, "carro"),
], "Si le mandas este mensaje, se va a alejar. (Casi todas lo hacen.)")
cr("15", "Pare de correr atrás", "apresentador rua", "gancho invertido", "Deja de perseguirlo. Ahora.", [
    D("Deja de perseguirlo. Ahora mismo. Cada mensaje que le mandas de más, lo aleja un poco más.", "calle"),
    D("Sé que lo haces porque te importa. Pero en su cabeza funciona al revés.", "calle"),
    B("Un hombre valora lo que tiene que ganarse. Lo que está siempre disponible, lo da por hecho.", M_FRIO),
    D("No te digo que te hagas la difícil. Eso cansa y se nota.", "calle"),
    D("Te digo que le hables en su frecuencia: con reto, con curiosidad, con calma.", "calle"),
    D("Y que sea él quien te busque a ti.", "calle"),
    D("Te enseño las frases exactas para lograrlo, sin parecer fría ni distante.", "calle"),
    D(CTA_FINAL, "calle"),
], "Deja de perseguirlo. Haz que él te busque a ti 👇")

# ---------------------------------------------------------------- FAMÍLIA 6: história de origem (cinematográfica)
cr("16", "3 palavras numa foto", "história cinematográfica", "história de origem", "Le escribí 3 palabras en una foto vieja… hoy es mi esposa", [
    D("Le escribí tres palabras en una foto vieja. Hoy esa mujer es la madre de mis hijos.", "noche"),
    B("Una amiga me mandó una captura: una mujer había comentado 'qué linda sonrisa tiene ese chico'.", "a man looking at his phone screen surprised at a screenshot, cozy room, cinematic, vertical 9:16"),
    B("Entré a su perfil. Era muy atractiva. Decenas de hombres le dejaban comentarios.", "a phone screen scrolling an attractive woman's social media profile with many comments, cinematic close-up, vertical 9:16"),
    D("No le dije 'hola, qué linda'. No hice lo mismo que los otros cincuenta.", "noche"),
    B("Busqué una foto vieja, donde casi no se veía un pequeño tatuaje en su rodilla. Y escribí: '¿Qué significa?'", "close-up of a finger typing a short comment under an old photo on a phone, cinematic, vertical 9:16"),
    B("Ella respondió con humor. Ligera. Curiosa. Sin darse cuenta, me habló en mi frecuencia.", W_FELIZ),
    B("Nuestra primera cita fue en un café pequeño. Pasaron ocho horas que se sintieron como treinta minutos.", "a man and a woman laughing together in a small cafe near a park, golden hour, cinematic, vertical 9:16"),
    D("Toda relación empieza con una conversación. Y esa conversación tiene palabras correctas.", "noche"),
    D(CTA_FINAL, "noche"),
], "Le escribí 3 palabras en una foto vieja. Hoy es la madre de mis hijos ❤️")
cr("17", "Ela me conquistou", "podcast", "história de origem", "La mujer que hizo que un mujeriego se casara", [
    D("Yo era el típico mujeriego. Y una mujer me hizo dejar todo y casarme con ella.", "podcast"),
    D("No era la más bonita que había conocido. Pero nunca hizo lo que hacían las demás.", "podcast"),
    D("Nunca empezaba conversaciones vacías. Nunca me interrogaba. Nunca me reclamó. Ni una vez.", "podcast"),
    D("Me hablaba de una forma que despertaba la mejor versión de mí.", "podcast"),
    B("Me daban ganas de crecer más, de hacer más, de conquistar más. Por ella.", "a man working hard and smiling, then hugging a woman at home, warm cinematic, vertical 9:16"),
    D("Pasé años entendiendo qué tenía esa forma de hablar. Y la convertí en 21 frases.", "podcast"),
    D("Hoy se las enseño a mujeres que quieren un hombre que las valore de verdad.", "podcast"),
    D(CTA_FINAL, "podcast"),
], "Yo era mujeriego. Ella no hizo lo que hacían las demás… y me casé con ella.")
cr("18", "Tímido na internet", "história + apresentador", "história de origem", "Yo era tan tímido que aprendí a enamorar por mensajes", [
    D("Yo era tan tímido que me costaba hablarle a una mujer en persona.", "estudio"),
    B("Así que me refugié en internet: foros, chats, aplicaciones de mensajes.", "a shy young man typing in front of a computer late at night, blue screen light, cinematic, vertical 9:16"),
    D("Y ahí descubrí, a base de prueba y error, qué palabras creaban conexión de verdad.", "estudio"),
    D("Y cuáles mataban una conversación en minutos.", "estudio"),
    D("Me tomó años. Pero al final supe qué palabras abren puertas y cuáles las cierran para siempre.", "estudio"),
    D("Hoy junto todo eso en 21 frases. Para que tú no pierdas años como yo.", "estudio"),
    D(CTA_FINAL, "estudio"),
], "Era tan tímido que aprendí a enamorar por mensajes. Esto es lo que descubrí.")

# ---------------------------------------------------------------- FAMÍLIA 7: situações específicas
cr("19", "Ex-ficante: andaban pero no eran nada", "UGC carro", "andábamos pero no éramos nada", "Andaban, pero no eran nada… y desapareció", [
    D("Andaban, pero no eran nada. Y de repente, desapareció como si nada hubiera pasado.", "carro"),
    D("Te lo explico como hombre: no se fue porque no le importaras.", "carro"),
    D("Se fue porque, en algún momento, la conversación dejó de despertarle algo.", "carro"),
    B("Y lo peor que puedes hacer ahora es escribirle '¿qué somos?' o '¿por qué te fuiste?'.", W_TRISTE),
    D("Eso confirma su decisión. Lo que funciona es lo contrario: curiosidad, calma y un pequeño reto.", "carro"),
    D("Tengo una sección entera de frases de rescate para este momento exacto.", "carro"),
    D("Para que sea él quien vuelva a buscarte, sin que tú lo persigas.", "carro"),
    D(CTA_FINAL, "carro"),
], "Andaban, pero no eran nada… y desapareció. Esto es lo que NO tienes que escribirle.")
cr("20", "Quente e frio", "apresentador", "quente e frio", "Un día te busca y al otro desaparece. Te explico por qué.", [
    D("Un día te escribe todo el día. Al otro, desaparece. Te explico por qué hace eso."),
    D("Cuando algo empieza a sentirse serio, muchos hombres retroceden. No porque no les gustes."),
    D("Es porque en ese momento no sienten el reto. Sienten la presión."),
    B("Y si tú respondes con más mensajes, más preguntas y más reclamos, la presión aumenta.", M_FRIO),
    D("Lo que lo estabiliza es otra cosa: que hablar contigo lo haga sentir más hombre."),
    D("Eso se logra con frases muy concretas. Cortas. En el momento justo."),
    D("Te enseño cuáles usar cuando se enfría y cuáles cuando vuelve."),
    D(CTA_FINAL),
], "¿Un día te busca y al otro desaparece? Esto es lo que pasa en su cabeza.")
cr("21", "Te deixa no visto", "WhatsApp", "visto", "Te deja en visto… y otra recibe respuesta en segundos", [
    Z("Tú le escribes esto. Y te deja en visto.", [("ella", "Hola 😊 ¿cómo estuvo tu día?"), ("visto", "")]),
    D("Mientras tanto, otra mujer le escribe al mismo hombre. Y él le responde en segundos.", "noche"),
    D("No es más bonita que tú. No es más interesante. Solo le habla en su frecuencia.", "noche"),
    Z("Ella no le pregunta cómo estuvo su día. Le escribe algo así.", [("otra", "Hoy vi algo que me hizo pensar en ti… pero no te lo voy a contar todavía 😏"), ("el", "Nooo ahora me dejas con la duda 😂 ¿qué fue?")]),
    D("Curiosidad. Misterio. Un pequeño reto. Eso es lo que lo conecta.", "noche"),
    D("Y tú también puedes aprenderlo. Son frases que copias y adaptas.", "noche"),
    D(CTA_FINAL, "noche"),
], "Te deja en visto… y a otra le responde en segundos. ¿Qué le escribe ella?")
cr("22", "Meses conversando e nada", "apresentador café", "estancado", "Llevan meses hablando y él nunca te invita a salir", [
    D("¿Llevan meses hablando y él nunca te invita a salir? Esto es lo que está pasando.", "cafe"),
    D("La conversación se volvió cómoda. Agradable. Pero no le despierta ninguna emoción.", "cafe"),
    D("Y un hombre se mueve por emoción. Por reto. Por curiosidad.", "cafe"),
    B("Hay frases que cambian una conversación tibia en una cita en pocos días.", "a woman confidently sending a text in a cafe, smiling, cinematic, vertical 9:16"),
    D("Por ejemplo: 'estoy pensando en algo'. Y nada más.", "cafe"),
    D("Eso abre su curiosidad y hace que sea él quien pregunte, quien insista, quien proponga.", "cafe"),
    D("Te enseño 21 frases como esa, organizadas por etapa.", "cafe"),
    D(CTA_FINAL, "cafe"),
], "¿Meses hablando y nunca te invita a salir? Prueba esta frase.")
cr("23", "Ele não quer compromisso", "palco", "compromisso", "Si él no quiere compromiso, deja de pedírselo así", [
    D("Si él no quiere compromiso, deja de pedírselo así.", "escenario"),
    D("'¿Qué somos?' '¿A dónde va esto?' Esas preguntas lo ponen a la defensiva.", "escenario"),
    D("Un hombre se compromete cuando siente que fue su idea. No cuando lo presionan.", "escenario"),
    B("Hay una forma elegante de hablar de una relación seria sin parecer desesperada.", "a couple walking hand in hand in a park, the man looking at her with admiration, cinematic, vertical 9:16"),
    D("Yo la llamo el ultimátum elegante. Una frase que convierte algo sin nombre en una relación de verdad.", "escenario"),
    D("Está en la categoría de frases de compromiso. Una de las cuatro que te enseño.", "escenario"),
    D(CTA_FINAL, "escenario"),
], "Si no quiere compromiso, deja de preguntarle '¿qué somos?'. Haz esto.")

# ---------------------------------------------------------------- FAMÍLIA 8: listas / didático
cr("24", "Los 4 mensajes que lo alejan", "lista com textos", "erros que afastam", "Los 4 mensajes que alejan a un hombre (el 4 es el peor)", [
    D("Los cuatro mensajes que alejan a un hombre. Y el cuarto es el peor."),
    T("Uno: el buenos días de compromiso.", "1. EL «BUENOS DÍAS» DE COMPROMISO"),
    T("Dos: el interrogatorio. Preguntas y preguntas como en una entrevista.", "2. EL INTERROGATORIO"),
    T("Tres: los fuegos artificiales. Fotos y tensión que brillan un momento y después desaparecen.", "3. LOS FUEGOS ARTIFICIALES"),
    T("Y cuatro: el reclamo. ¿Por qué no me llamaste? ¿Ya no te importo?", "4. EL RECLAMO"),
    D("Ese último es el más peligroso. Porque él no escucha amor. Escucha un regaño."),
    D("La buena noticia: cambiar esto es mucho más fácil de lo que crees."),
    D("Te enseño qué escribir en lugar de cada uno de estos mensajes. 21 frases en total."),
    D(CTA_FINAL),
], "Los 4 mensajes que alejan a un hombre. ¿Cuál de estos le mandaste esta semana?")
cr("25", "Las 4 etapas", "apresentador com lista", "frases por etapa", "No importa en qué etapa estén, hay una frase para eso", [
    D("No importa en qué etapa estén. Hay una frase exacta para cada momento.", "podcast"),
    T("Si apenas se están conociendo: frases de atracción, para que deje de pasar de largo.", "ETAPA 1 · ATRACCIÓN"),
    T("Si ya hablan: frases de obsesión, para que no pueda sacarte de su cabeza.", "ETAPA 2 · OBSESIÓN"),
    T("Si ya salen: frases de compromiso, para que la relación avance natural.", "ETAPA 3 · COMPROMISO"),
    T("Y si se enfrió o desapareció: frases de rescate, para que vuelva a buscarte.", "ETAPA 4 · RESCATE"),
    D("No importa si tienes 25 o 60 años. La frecuencia masculina funciona igual en todos los hombres.", "podcast"),
    D("Y además de copiar las frases, entiendes por qué funcionan para adaptarlas a tu caso.", "podcast"),
    D(CTA_FINAL, "podcast"),
], "¿En qué etapa están? Atracción, obsesión, compromiso o rescate: hay una frase para cada una.")
cr("26", "Diccionario de la mente masculina", "quiz / tradução", "tradutor de frases masculinas", "Cuando él dice 'estoy muy ocupado', en realidad significa esto", [
    D("Cuando un hombre te dice 'estoy muy ocupado', casi nunca significa lo que crees."),
    T("'Estoy muy ocupado.' 'Vamos despacio.' 'No estoy listo para una relación.'", "«ESTOY MUY OCUPADO»"),
    D("Son frases que la mayoría de las mujeres interpreta mal. Y responde peor."),
    B("Y cada respuesta equivocada lo aleja un poco más.", M_FRIO),
    D("Por eso hice un diccionario de la mente masculina. Lo que él dice y lo que realmente quiere decir."),
    D("Viene de regalo con las 21 frases secretas."),
    D(CTA_FINAL),
], "'Estoy muy ocupado' casi nunca significa lo que crees. Te traduzco lo que él quiere decir.")

# ---------------------------------------------------------------- FAMÍLIA 9: formatos novos
cr("27", "POV: ele leu sua mensagem", "POV cinematográfico", "o efeito na mente dele", "POV: él acaba de leer tu mensaje", [
    B("Él acaba de leer tu mensaje. Y míralo: no puede dejar de sonreír.", M_CEL),
    B("Lo lee otra vez. Deja lo que estaba haciendo. Contesta en segundos.", "a man stopping work at his desk to reply to a message, smiling, cinematic, vertical 9:16"),
    B("Más tarde, les cuenta a sus amigos que conoció a una mujer diferente.", "a group of men at a bar, one of them showing his phone and smiling, cinematic, vertical 9:16"),
    D("Esto no pasa por tu cuerpo, ni por tus fotos. Pasa por tus palabras."),
    D("Hay un tipo de frase que, cuando una mujer la escribe, el hombre no puede dejar de pensar en ella."),
    D("Yo junté 21 de esas frases en más de diez años estudiando conversaciones reales."),
    D(CTA_FINAL),
], "POV: él acaba de leer tu mensaje… y no puede dejar de sonreír.")
cr("28", "Outra mulher agora mesmo", "tela dividida", "urgência / outra mulher", "Mientras ves esto, otra mujer le está escribiendo", [
    D("Mientras ves este video, otra mujer le está escribiendo al hombre que tú quieres.", "noche"),
    B("Y no le escribe 'hola, ¿cómo estás?'. Ni un párrafo enorme a las dos de la mañana.", W_TRISTE),
    B("Le escribe una frase corta. Y él le contesta en segundos.", W_FELIZ),
    D("No es porque ella valga más que tú. Es porque aprendió a hablar en su frecuencia.", "noche"),
    D("Y tú todavía no. Pero eso se puede cambiar hoy.", "noche"),
    D("Son 21 frases. Copias, adaptas y envías.", "noche"),
    D(CTA_FINAL, "noche"),
], "Mientras ves esto, otra mujer le está escribiendo. Y él sí le contesta.")
cr("29", "Teste: qual você mandaria?", "quiz A/B", "quiz interativo", "¿Cuál de estos mensajes le mandarías? (casi todas fallan)", [
    D("Él no te escribe hace dos días. ¿Cuál de estos mensajes le mandarías?"),
    T("A: '¿Por qué desapareciste?'  B: 'Hola, ¿cómo estás?'  C: 'Hoy pasó algo que te va a dar risa'", "A · B · C"),
    D("Si elegiste A, lo alejaste. Suena a reclamo y él se va a defender o a desaparecer."),
    D("Si elegiste B, lo aburriste. Es un mensaje de compromiso que contesta por educación."),
    D("La C despierta su curiosidad. Lo obliga a preguntar. Y la conversación vuelve a ser tuya."),
    D("Eso es hablar en la frecuencia masculina. Y se aprende."),
    D("Te enseño 21 frases así, para cada momento."),
    D(CTA_FINAL),
], "¿A, B o C? Casi todas eligen el mensaje equivocado 😬")
cr("30", "Notícia: a frase que viralizou", "manchete / notícia", "curiosidade", "Esta frase de 2 palabras está haciendo que los hombres dejen de ignorar", [
    T("", "LA FRASE DE 2 PALABRAS QUE HACE QUE UN HOMBRE DEJE DE IGNORARTE"),
    D("Hay una frase de dos palabras que hace que un hombre deje de ignorarte. Y no es 'te extraño'."),
    D("Tampoco es 'te amo'. Ni '¿por qué no me escribes?'."),
    D("Es una frase que él no interpreta como rechazo, sino como un reto que quiere ganar."),
    B("Y cuando un hombre siente ese reto, empieza a buscarte, a invertir, a planear.", M_CEL),
    D("Te explico cuál es, por qué funciona y otras 20 frases parecidas."),
    D(CTA_FINAL),
], "La frase de 2 palabras que hace que un hombre deje de ignorarte (no es 'te extraño').")

# ---------------------------------------------------------------- miolo extra (mecanismo, dor, objeção, conteúdo do vídeo) — combinações diferentes por criativo
MEC = [
    "Desde niños nos dicen: pórtate como hombre. Por eso un hombre se queda con la mujer que lo hace sentir más hombre.",
    "Un hombre no se engancha con la mujer más disponible. Se engancha con la que le despierta las ganas de conquistar.",
    "La frecuencia masculina es simple: honor, lealtad, compañerismo y desafío. Cuando le hablas ahí, él te escucha.",
    "Las palabras que hacen sentir amada a una mujer no son las mismas que hacen que un hombre se quede.",
    "Él no se mueve por lo que le pides. Se mueve por lo que le haces sentir cuando habla contigo.",
    "Cuando un mensaje lo reta en lugar de reclamarle, deja de sentirse un niño regañado y empieza a actuar como hombre.",
    "No se trata de juegos ni de hacerte la difícil. Se trata de hablar en el idioma que su mente reconoce.",
    "La curiosidad y un poco de misterio conectan más con un hombre que cien mensajes de cariño.",
    "Un hombre valora lo que tiene que ganarse. Por eso las frases correctas siempre dejan una puerta abierta.",
    "El problema nunca fuiste tú. Solo estabas usando la frecuencia equivocada.",
]
DOR = [
    ("¿Cuántos hombres buenos se fueron de tu vida solo porque la conversación murió a la mitad?", W_TRISTE),
    ("¿Cuántas primeras citas prometedoras nunca tuvieron una segunda?", "a woman sitting alone at a restaurant table checking her phone, cinematic, vertical 9:16"),
    ("¿Cuántas noches más vas a pasar mirando el celular, esperando una respuesta que no llega?", W_TRISTE),
    ("Y si nada cambia, el próximo hombre que te guste va a recibir los mismos mensajes. Y se va a ir igual.", M_FRIO),
    ("¿Cuántas veces viste a otra mujer, no más linda que tú, con el tipo de hombre que tú quieres?", "a woman scrolling social media seeing a happy couple photo, thoughtful, cinematic, vertical 9:16"),
    ("Meses invirtiendo tiempo y emoción en alguien que nunca termina de comprometerse.", W_TRISTE),
    ("Y te quedas preguntándote: ¿será que el problema soy yo?", "a woman looking at herself in a mirror, doubtful, soft light, cinematic, vertical 9:16"),
    ("El tiempo pasa. Y la familia que sueñas sigue lejos mientras le hables en la frecuencia equivocada.", "a woman looking out of a window at a couple with a child walking in the park, cinematic, vertical 9:16"),
    ("Él no es un mal hombre. Y tú mereces ser amada. Solo están hablando idiomas distintos.", "a man and a woman texting each other from different rooms, both confused, split mood, cinematic, vertical 9:16"),
    ("Cada mensaje en la frecuencia equivocada lo aleja un poquito más. Sin que lo notes.", M_FRIO),
]
OBJ = [
    "Y no importa si tienes 25 o 60 años. La programación que los hombres reciben de niños es la misma.",
    "No es manipulación. Es entender cómo piensa un hombre y dejar de pelear contra eso.",
    "No necesitas ser más joven, ni más bonita, ni mandar fotos. Necesitas otras palabras.",
    "Funciona por mensaje o en persona. Con el que recién conociste o con el que ya se alejó.",
    "No son frases para copiar sin pensar: te explico qué activa cada una para que la adaptes a tu caso.",
    "Y no tienes que volverte fría ni distante. Al contrario: él te va a sentir más cerca.",
    "Aunque él lleve días sin escribirte, todavía hay una forma correcta de volver a abrir la conversación.",
    "No hace falta escribirle más. Hace falta escribirle mejor.",
    "Si ya lo intentaste todo, es porque lo intentaste en la frecuencia equivocada.",
    "No tienes que cambiar quién eres. Solo la forma en que se lo dices.",
]
VID = [
    "En el video te muestro las 21 frases organizadas en cuatro etapas: atracción, obsesión, compromiso y rescate.",
    "En el video te explico también qué nunca debes decirle cuando desaparece. Casi todas hacen justo lo contrario.",
    "En el video te enseño el ultimátum elegante: la frase que convierte algo sin nombre en una relación de verdad.",
    "En el video está la frase de rescate para cuando se enfría, para que sea él quien vuelva a buscarte.",
    "En el video te cuento cómo usar cada frase en el momento justo, sin parecer necesitada.",
    "En el video te doy los primeros mensajes para iniciar una conversación que él no pueda ignorar.",
    "En el video te muestro cómo hablar de algo serio sin que él se sienta presionado.",
    "En el video te explico el principio que hay detrás de cada frase, para que nunca más te quedes sin saber qué responder.",
    "En el video te muestro las frases de obsesión, para que él deje una salida con amigos solo para escribirte.",
    "En el video aprendes a convertir un reclamo en un reto. Y eso cambia por completo cómo te ve.",
]
for k, c in enumerate(C):
    ext = [D(MEC[(k * 3) % 10], c["cenas"][0].get("cena", "estudio") if c["cenas"][0]["t"] == "D" else "estudio")]
    fd, pd = DOR[(k * 7 + 2) % 10]
    ext.append(B(fd, pd))
    ext.append(D(OBJ[(k * 3 + 5) % 10], ext[0]["cena"]))
    ext.append(D(VID[k % 10], ext[0]["cena"]))
    c["cenas"] = c["cenas"][:-1] + ext + c["cenas"][-1:]

assert len(C) == 30 and len({c["id"] for c in C}) == 30
out = dict(produto="21-frases", titulo="21 Frases · Lote 3 (Flow) — 30 criativos novos", avatar_ref="daniel_ref.jpg",
           voz="0e07ee5d68de482aa44d5095dfa2f900", cenarios_daniel=CEN, criativos=C,
           regras="Daniel com a voz clonada; Flow sempre no modelo Lower Priority (0 crédito); mínimo 60 s; sem números/estudos inventados; sem avatar fingindo cliente.")
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "21-frases-lote-3-flow.json")
json.dump(out, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
falas = [s["fala"] for c in C for s in c["cenas"] if s["fala"]]
flow = sum(1 for c in C for s in c["cenas"] if s["t"] in "DB")
print(len(C), "criativos |", len(falas), "falas |", sum(len(f.split()) for f in falas), "palavras |", flow, "cenas no Flow")
