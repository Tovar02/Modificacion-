import streamlit as st
import random
import time

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="¿Quién quiere ser Ingeniero TDA?", page_icon="💰")

# --- ESTILO ---
st.markdown("""
<style>
.titulo{
text-align:center;
color:gold;
font-size:40px;
}

.pregunta{
background-color:#11144c;
padding:20px;
border-radius:15px;
color:white;
text-align:center;
font-size:24px;
}
</style>
""", unsafe_allow_html=True)

# --- SONIDOS ---
SONIDO_CORRECTO = "https://www.soundjay.com/buttons/sounds/button-09.mp3"
SONIDO_ERROR = "https://www.soundjay.com/buttons/sounds/button-10.mp3"

def reproducir_sonido(url):
    st.audio(url)

# --- PREGUNTAS ---
if 'pool_preguntas' not in st.session_state:

    st.session_state.pool_preguntas = [

        {"p": "¿Qué significa TDA?",
         "o": ["Televisión Digital Abierta", "Transmisión Digital Analógica", "Tecnología Digital Avanzada", "Televisión de Alta Definición"],
         "c": "Televisión Digital Abierta"},

        {"p": "¿Qué estándar utiliza la TDA en América Latina?",
         "o": ["DVB-T", "ATSC", "ISDB-Tb", "PAL"],
         "c": "ISDB-Tb"},

        {"p": "¿Cuál es una ventaja de la TDA frente a la televisión analógica?",
         "o": ["Menor calidad", "Mayor consumo", "Mejor calidad de imagen y sonido", "Menos canales"],
         "c": "Mejor calidad de imagen y sonido"},

        {"p": "¿En qué año llegó el hombre a la Luna?",
         "o": ["1965", "1972", "1969", "1980"],
         "c": "1969"},

        {"p": "¿Cuántos bits tiene un byte?",
         "o": ["4", "16", "32", "8"],
         "c": "8"},

        {"p": "¿Qué animal es la mascota de Linux?",
         "o": ["Gato", "Pingüino", "Perro", "Elefante"],
         "c": "Pingüino"}

    ]

    random.shuffle(st.session_state.pool_preguntas)

# --- ESTADOS ---
if 'indice' not in st.session_state:
    st.session_state.indice = 0
    st.session_state.puntos = 0
    st.session_state.juego_terminado = False
    st.session_state.tiempo_inicio = time.time()
    st.session_state.resultado = None
    st.session_state.esperando_resultado = False

TOTAL_PREGUNTAS = 5
TIEMPO_LIMITE = 60

# --- TITULO ---
st.markdown('<div class="titulo">💰 ¿Quién quiere ser Ingeniero TDA?</div>', unsafe_allow_html=True)
st.divider()

# --- BARRA DE PROGRESO ---
progreso = st.session_state.indice / TOTAL_PREGUNTAS
st.progress(progreso)

# --- JUEGO ---
if not st.session_state.juego_terminado:

    pregunta_actual = st.session_state.pool_preguntas[st.session_state.indice]

    # --- TEMPORIZADOR ---
    tiempo_actual = time.time()
    tiempo_restante = int(TIEMPO_LIMITE - (tiempo_actual - st.session_state.tiempo_inicio))

    st.metric("Tiempo restante", f"{tiempo_restante} s")

    if tiempo_restante <= 0:

        st.error("⏰ Tiempo agotado")
        time.sleep(2)

        if st.session_state.indice < TOTAL_PREGUNTAS - 1:
            st.session_state.indice += 1
            st.session_state.tiempo_inicio = time.time()
        else:
            st.session_state.juego_terminado = True

        st.rerun()

    # --- PREGUNTA ---
    st.markdown(
        f'<div class="pregunta">Pregunta {st.session_state.indice+1}<br><br>{pregunta_actual["p"]}</div>',
        unsafe_allow_html=True
    )

    opciones = pregunta_actual['o']

    col1, col2 = st.columns(2)

    with col1:
        btn_a = st.button(f"A) {opciones[0]}", use_container_width=True)
        btn_b = st.button(f"B) {opciones[1]}", use_container_width=True)

    with col2:
        btn_c = st.button(f"C) {opciones[2]}", use_container_width=True)
        btn_d = st.button(f"D) {opciones[3]}", use_container_width=True)

    seleccion = None

    if btn_a: seleccion = opciones[0]
    if btn_b: seleccion = opciones[1]
    if btn_c: seleccion = opciones[2]
    if btn_d: seleccion = opciones[3]

    # --- REGISTRAR RESPUESTA ---
    if seleccion and not st.session_state.esperando_resultado:

        if seleccion == pregunta_actual['c']:
            st.session_state.resultado = ("correcto", pregunta_actual['c'])
            st.session_state.puntos += 2
        else:
            st.session_state.resultado = ("incorrecto", pregunta_actual['c'])

        st.session_state.esperando_resultado = True

    # --- MOSTRAR RESULTADO ---
    if st.session_state.esperando_resultado:

        tipo, respuesta = st.session_state.resultado

        if tipo == "correcto":
            st.success("✅ ¡Correcto!")
            reproducir_sonido(SONIDO_CORRECTO)
        else:
            st.error(f"❌ Incorrecto. Respuesta: {respuesta}")
            reproducir_sonido(SONIDO_ERROR)

        time.sleep(2)

        if st.session_state.indice < TOTAL_PREGUNTAS - 1:
            st.session_state.indice += 1
            st.session_state.tiempo_inicio = time.time()
        else:
            st.session_state.juego_terminado = True

        st.session_state.resultado = None
        st.session_state.esperando_resultado = False

        st.rerun()

    # --- ACTUALIZAR TEMPORIZADOR ---
    if not st.session_state.esperando_resultado:
        time.sleep(1)
        st.rerun()

# --- FINAL DEL JUEGO ---
else:

    st.header("🏁 Fin del juego")

    st.metric("PUNTUACIÓN FINAL", f"{st.session_state.puntos} / 10")

    if st.session_state.puntos >= 8:
        st.balloons()
        st.success("🎉 ¡Eres un experto en TDA!")
        reproducir_sonido(SONIDO_CORRECTO)
    else:
        st.warning("📚 Sigue estudiando la norma ISDB-Tb")

    if st.button("Reintentar"):

        st.session_state.indice = 0
        st.session_state.puntos = 0
        st.session_state.juego_terminado = False
        st.session_state.tiempo_inicio = time.time()
        st.session_state.resultado = None
        st.session_state.esperando_resultado = False

        random.shuffle(st.session_state.pool_preguntas)

        st.rerun()
