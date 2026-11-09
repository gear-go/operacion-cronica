"""
Operación Crónica: hackeando la fatalidad.

Simulación educativa basada en "Crónica de una muerte anunciada", de Gabriel
García Márquez. El motor está en modelo.py; aquí solo vive la interfaz.

Germán Gómez Vargas, Instituto de Data Science, Universidad del Desarrollo.
"""

import base64
import html
import re
from pathlib import Path

import streamlit as st

from modelo import (
    AVISO,
    CAUSA_DESINFORMADO,
    CAUSA_FRAGMENTADA,
    CAUSA_LENTO,
    CAUSA_RUMOR_GANA,
    CLOTILDE,
    CORONEL,
    CRISTO,
    GEMELOS,
    PADRE,
    PLACIDA,
    POLICIA,
    RUMOR,
    RUTAS_ALTERNATIVAS,
    RUTAS_LIBRO,
    SANTIAGO,
    VICTORIA,
    run_monte_carlo,
    una_manana,
)

st.set_page_config(
    page_title="Operación Crónica",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

ASSETS = Path(__file__).parent / "assets"

# ============================================================================
# INSTITUCIÓN ANFITRIONA
# ============================================================================
# Se elige con un parámetro de URL, para no tener que editar el código en cada
# charla:  https://salvando-santiago.streamlit.app/?uni=americana
INSTITUCIONES = {
    "americana": {
        "nombre": "Corporación Universitaria Americana",
        "lugar": "Barranquilla, Medellín y Montería, Colombia",
        "contexto": "Visita académica 2026",
    },
    "uajs": {
        "nombre": "Corporación Universitaria Antonio José de Sucre",
        "lugar": "Sincelejo, Colombia",
        "contexto": "Visita académica 2025",
    },
    "generica": {"nombre": "", "lugar": "", "contexto": ""},
}

try:
    _uni_key = st.query_params.get("uni", "americana")
except Exception:  # Streamlit antiguo
    _uni_key = "americana"
UNI = INSTITUCIONES.get(str(_uni_key).lower(), INSTITUCIONES["americana"])

# ============================================================================
# ESTADO
# ============================================================================
N_MANANAS = 100

# La semilla 2026 produce, con los valores de la novela, 17 mañanas de 100 en
# que Santiago se salva: una muestra representativa del promedio de largo plazo
# (~18 %) y la cifra que se usa en la presentación. test_modelo.py lo verifica.
SEMILLA_INICIAL = 2026

NOVELA = {"alpha": 0.08, "beta": 0.15, "gamma": 0.08}

for _k, _v in {**NOVELA, "seed": SEMILLA_INICIAL, "manana": 1}.items():
    st.session_state.setdefault(_k, _v)


def volver_a_la_novela():
    st.session_state.update(NOVELA)
    st.session_state.seed = SEMILLA_INICIAL


def otra_muestra():
    st.session_state.seed += 1


@st.cache_data(show_spinner=False)
def simular(alpha, beta, gamma, seed):
    return run_monte_carlo(alpha, beta, gamma, N_MANANAS, seed=seed)


@st.cache_resource
def logo_b64():
    return base64.b64encode((ASSETS / "logo-ids-udd-10-anos.png").read_bytes()).decode()


def coma(x, decimales=1):
    """Formato numérico en español: coma decimal."""
    return f"{x:.{decimales}f}".replace(".", ",")


# ============================================================================
# TEXTOS
# ============================================================================
CAUSA_CORTA = {
    CAUSA_DESINFORMADO: "Santiago creyó el rumor",
    CAUSA_RUMOR_GANA: "el rumor ocupó el pueblo antes que el aviso",
    CAUSA_FRAGMENTADA: "el aviso no encontró ruta hasta Santiago",
    CAUSA_LENTO: "el aviso venía en camino, pero no alcanzó",
}
REMEDIO = {
    CAUSA_DESINFORMADO: "pensamiento crítico",
    CAUSA_RUMOR_GANA: "pensamiento crítico",
    CAUSA_FRAGMENTADA: "adaptabilidad",
    CAUSA_LENTO: "filtrado de ruido",
}
EXPLICACION = {
    CAUSA_DESINFORMADO: "Le llegó primero el rumor, nadie lo verificó y él se quedó tranquilo.",
    CAUSA_RUMOR_GANA: "El rumor se repitió por las mismas rutas por las que debía viajar la advertencia.",
    CAUSA_FRAGMENTADA: "La advertencia existía, pero no había un camino que la llevara hasta él.",
    CAUSA_LENTO: "Alguien cercano a Santiago ya sabía, pero los gemelos llegaron primero.",
}
ORDEN_CAUSAS = [CAUSA_DESINFORMADO, CAUSA_RUMOR_GANA, CAUSA_FRAGMENTADA, CAUSA_LENTO]

CORTO = {
    GEMELOS: "Gemelos",
    CLOTILDE: "Clotilde",
    POLICIA: "Policía",
    CORONEL: "Coronel",
    PADRE: "P. Amador",
    CRISTO: "C. Bedoya",
    PLACIDA: "Plácida",
    VICTORIA: "Victoria",
    SANTIAGO: "Santiago",
}
POS = {
    GEMELOS: (70, 250),
    CLOTILDE: (230, 250),
    POLICIA: (410, 110),
    PADRE: (410, 250),
    CRISTO: (410, 390),
    CORONEL: (610, 110),
    PLACIDA: (610, 250),
    VICTORIA: (610, 390),
    SANTIAGO: (850, 250),
}
# Dos rutas alternativas se dibujan curvas para no atravesar a otros personajes:
# una cúbica que sube por encima de la fila superior, y una cuadrática.
CURVAS = {
    frozenset((CLOTILDE, SANTIAGO)): ((180, -80), (900, -80)),
    frozenset((POLICIA, CRISTO)): ((590, 250),),
}

# ============================================================================
# ESTILO
# ============================================================================
st.markdown(
    """
<style>
@font-face { font-family: 'Source Serif 4'; src: url('./app/static/fonts/source-serif-4.woff2') format('woff2');
  font-weight: 400 700; font-style: normal; font-display: swap; }
[data-testid="stMarkdownContainer"] h1, [data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3, [data-testid="stMarkdownContainer"] h4 {
  font-family: 'Source Serif 4', Georgia, serif; }
.block-container { padding-top: 1.75rem; padding-bottom: 3rem; max-width: 1180px; }
[data-testid="stToolbar"], [data-testid="stDecoration"] { display: none; }
header[data-testid="stHeader"] { background: transparent; }

.oc-top { display: flex; justify-content: space-between; align-items: center; gap: 1rem 2rem;
  flex-wrap: wrap; padding-bottom: 1.1rem; border-bottom: 1px solid #D3D7DC; margin-bottom: 2rem; }
.oc-top img { height: 54px; width: auto; display: block; }
.oc-para { font-size: 0.92rem; line-height: 1.45; color: #4A5560; max-width: 30rem; }
.oc-para b { color: #10263B; font-weight: 600; }

.oc-h1 { font-family: 'Source Serif 4', Georgia, serif; font-weight: 600; color: #10263B;
  font-size: clamp(2.3rem, 5vw, 3.6rem); line-height: 1.02; letter-spacing: -0.01em; margin: 0; }
.oc-h1-sub { font-family: 'Source Serif 4', Georgia, serif; font-weight: 400; color: #004A87;
  font-size: clamp(1.3rem, 2.6vw, 1.8rem); line-height: 1.2; margin: 0.35rem 0 1.2rem; }
.oc-lede { font-size: 1.12rem; line-height: 1.62; max-width: 62ch; color: #10263B; margin: 0 0 2.2rem; }

.oc-hero { font-family: 'Source Serif 4', Georgia, serif; font-weight: 500; color: #10263B;
  font-size: clamp(1.7rem, 3.2vw, 2.55rem); line-height: 1.12; margin: 0 0 1.1rem;
  font-variant-numeric: lining-nums tabular-nums; max-width: 18ch; }

.oc-waffle { display: grid; grid-template-columns: repeat(10, 1fr); gap: 5px; max-width: 390px; margin: 0 0 1rem; }
.oc-c { display: block; aspect-ratio: 1 / 1; border-radius: 3px; }
.oc-salvado { background: #004A87; }
.oc-rumor { background: #C1442E; }
.oc-sin_aviso { background: repeating-linear-gradient(135deg, #7D8893 0 3px, #D3D7DC 3px 6px); }

.oc-leyenda { display: flex; flex-wrap: wrap; gap: 0.35rem 1.4rem; font-size: 0.95rem; margin: 0 0 1.1rem; color: #10263B; }
.oc-leyenda .sw { display: inline-block; width: 14px; height: 14px; border-radius: 3px; vertical-align: -2px; margin-right: 0.45rem; }
.oc-leyenda b { font-variant-numeric: tabular-nums; font-weight: 600; }

.oc-mini { display: none; }
@media (max-width: 640px) {
  .oc-mini { display: block; margin: 0.6rem 0 0.2rem; font-weight: 600; color: #004A87; font-size: 1rem; }
}
.oc-nota { font-size: 0.98rem; line-height: 1.55; color: #4A5560; max-width: 60ch; margin: 0.3rem 0; }
.oc-veredicto { border-left: 3px solid #004A87; padding: 0.25rem 0 0.25rem 1rem; margin: 1.2rem 0 0;
  font-size: 1.04rem; line-height: 1.55; max-width: 60ch; color: #10263B; }
.oc-veredicto.mal { border-left-color: #C1442E; }

.oc-causas { display: grid; grid-template-columns: minmax(12rem, 1.4fr) 2fr 6rem; gap: 0.9rem 1.2rem;
  align-items: center; max-width: 920px; margin: 0.5rem 0 1rem; }
.oc-causas .nombre { font-weight: 600; line-height: 1.3; }
.oc-causas .nombre small { display: block; font-weight: 400; color: #4A5560; font-size: 0.88rem; margin-top: 0.15rem; }
.oc-causas .pista { height: 14px; background: #EAE5D9; border-radius: 3px; overflow: hidden; }
.oc-causas .barra { height: 100%; }
.oc-causas .n { font-variant-numeric: tabular-nums; text-align: right; color: #10263B; white-space: nowrap; }
@media (max-width: 640px) {
  .oc-causas { grid-template-columns: 1fr 5.5rem; }
  .oc-causas .pista { grid-column: 1 / -1; }
}

.oc-red { overflow-x: auto; margin: 0.25rem 0 0.75rem; }
.oc-red svg { width: 100%; min-width: 620px; height: auto; display: block; }
.oc-leyenda-red { display: flex; flex-wrap: wrap; gap: 0.35rem 1.3rem; font-size: 0.9rem; color: #4A5560; margin-bottom: 1.2rem; }
.oc-leyenda-red .sw { display: inline-block; width: 14px; height: 14px; border-radius: 7px; vertical-align: -2px; margin-right: 0.4rem; }
.oc-leyenda-red .ln { display: inline-block; width: 26px; height: 0; vertical-align: 4px; margin-right: 0.4rem; }

.oc-log { list-style: none; padding: 0; margin: 0.4rem 0 0; max-width: 680px; }
.oc-log li { display: grid; grid-template-columns: 5.5rem 1fr; gap: 0.75rem; padding: 0.4rem 0;
  border-top: 1px solid #E1E4E8; font-size: 0.95rem; line-height: 1.45; }
.oc-log li span:first-child { color: #4A5560; font-variant-numeric: tabular-nums; }

.oc-leccion h4 { font-family: 'Source Serif 4', Georgia, serif; font-size: 1.35rem; margin: 0 0 0.15rem; }
.oc-leccion .var { color: #4A5560; font-size: 0.9rem; margin: 0 0 0.9rem; }
.oc-leccion p { font-size: 0.98rem; line-height: 1.55; margin: 0 0 0.7rem; }
.oc-leccion p b { font-weight: 600; }

.oc-pie { margin-top: 3rem; padding-top: 1.2rem; border-top: 1px solid #D3D7DC; font-size: 0.88rem;
  line-height: 1.6; color: #4A5560; }
.oc-pie a { color: #004A87; }
</style>
""",
    unsafe_allow_html=True,
)

# ============================================================================
# ENCABEZADO
# ============================================================================
_para = (
    f"<b>Charla para estudiantes de la {UNI['nombre']}</b><br>{UNI['lugar']}"
    if UNI["nombre"]
    else "<b>Instituto de Data Science</b><br>Universidad del Desarrollo, Chile"
)
st.markdown(
    f'<div class="oc-top"><img src="data:image/png;base64,{logo_b64()}" '
    f'alt="dataScience UDD, Instituto de Data Science de la Universidad del Desarrollo, 10 años">'
    f'<div class="oc-para">{_para}</div></div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="oc-h1" role="heading" aria-level="1">Operación Crónica</div>'
    '<div class="oc-h1-sub">Hackeando la fatalidad</div>'
    '<div class="oc-lede">Todo el pueblo sabía que los gemelos Vicario iban a matar a Santiago Nasar, '
    "y nadie logró avisarle. Esta simulación repite esa mañana cien veces. "
    "Por el pueblo circulan dos mensajes: la advertencia verdadera y el rumor de que "
    "«son habladas de borracho». Mueva las tres características del pueblo y vea si "
    "Santiago habría podido salvarse.</div>",
    unsafe_allow_html=True,
)

# ============================================================================
# CONTROLES Y RESULTADO
# ============================================================================
col_ctrl, col_res = st.columns([5, 7], gap="large")

with col_ctrl:
    with st.container(border=True):
        st.markdown("#### El pueblo")
        alpha = st.slider(
            "Pensamiento crítico (α)",
            0.0, 1.0, step=0.01, format="%.2f", key="alpha",
            help="Con esta probabilidad, una persona verifica lo que oye: se queda con la "
                 "advertencia y descarta el rumor. Si no verifica, cree lo primero que le llega. "
                 "Es el mismo fallo de un agente de IA que obedece una instrucción escondida en un correo.",
        )
        st.caption(f"Cuántos vecinos verifican antes de repetir. En la novela: {coma(NOVELA['alpha'], 2)}.")

        beta = st.slider(
            "Adaptabilidad (β)",
            0.0, 1.0, step=0.01, format="%.2f", key="beta",
            help="Probabilidad de que exista cada una de las seis rutas alternativas que no "
                 "existieron en la novela: por ejemplo, que Clotilde le avise directamente a Santiago.",
        )
        st.caption(f"Cuántas rutas alternativas tiene el aviso. En la novela: {coma(NOVELA['beta'], 2)}.")

        gamma = st.slider(
            "Filtrado de ruido (γ⁻¹)",
            0.0, 1.0, step=0.01, format="%.2f", key="gamma",
            help="Cuánto logra el pueblo concentrarse en lo importante. Con mucho ruido, los "
                 "mensajes saltan de una persona a otra más despacio.",
        )
        st.caption(
            f"Cuánto se concentra el pueblo pese al obispo, la resaca y el puerto. "
            f"En la novela: {coma(NOVELA['gamma'], 2)}."
        )

        b1, b2 = st.columns(2)
        b1.button("Restaurar la novela", on_click=volver_a_la_novela, width="stretch")
        b2.button("Otras 100 mañanas", on_click=otra_muestra, width="stretch")
        if st.session_state.seed != SEMILLA_INICIAL:
            st.caption(
                f"Muestra n.º {st.session_state.seed - SEMILLA_INICIAL + 1}. El azar cambia "
                "cada mañana; lo que importa es el promedio."
            )

        r = simular(alpha, beta, gamma, st.session_state.seed)
        conteo = {k: r["mananas"].count(k) for k in ("salvado", "rumor", "sin_aviso")}
        salvados = conteo["salvado"]
        # En el celular el resultado queda debajo de los controles: este resumen
        # evita tener que desplazarse para ver el efecto de mover una perilla.
        st.markdown(
            f'<div class="oc-mini" aria-hidden="true">Santiago se salva en {salvados} de 100 mañanas.</div>',
            unsafe_allow_html=True,
        )

libro = simular(NOVELA["alpha"], NOVELA["beta"], NOVELA["gamma"], st.session_state.seed)
desinformados = int(round(r["misinformed_rate"] * N_MANANAS / 100))
es_la_novela = all(abs(v - NOVELA[k]) < 1e-9 for k, v in {"alpha": alpha, "beta": beta, "gamma": gamma}.items())

with col_res:
    mananas = "mañana" if salvados == 1 else "mañanas"
    st.markdown(
        f'<div class="oc-hero">Santiago se salva en {salvados} de cada 100 {mananas}.</div>',
        unsafe_allow_html=True,
    )

    celdas = "".join(
        f'<span class="oc-c oc-{k}"></span>' for k in ("salvado", "rumor", "sin_aviso") for _ in range(conteo[k])
    )
    st.markdown(
        f'<div class="oc-waffle" role="img" aria-label="Cien mañanas simuladas: en {salvados} Santiago se salva, '
        f'en {conteo["rumor"]} muere por el rumor y en {conteo["sin_aviso"]} muere porque el aviso no llega a tiempo.">'
        f"{celdas}</div>"
        '<div class="oc-leyenda">'
        f'<span><span class="sw oc-salvado"></span>Se salva <b>{conteo["salvado"]}</b></span>'
        f'<span><span class="sw oc-rumor"></span>Muere: ganó el rumor <b>{conteo["rumor"]}</b></span>'
        f'<span><span class="sw oc-sin_aviso"></span>Muere: el aviso no llegó a tiempo <b>{conteo["sin_aviso"]}</b></span>'
        "</div>",
        unsafe_allow_html=True,
    )

    notas = []
    if salvados and r["avg_alert_time"]:
        notas.append(
            f"Cuando se salva, el aviso le llega en promedio en el minuto {coma(r['avg_alert_time'])}. "
            "Los gemelos llegan siempre en el minuto 10."
        )
    if desinformados:
        rescatados = desinformados - r["failure_causes"].get(CAUSA_DESINFORMADO, 0)
        nota = f"En {desinformados} de las 100 mañanas, a Santiago le llegó primero el rumor."
        if rescatados == 1:
            nota += " En una de ellas, un aviso posterior lo hizo dudar y se salvó."
        elif rescatados > 1:
            nota += f" En {rescatados} de ellas, un aviso posterior lo hizo dudar y se salvó."
        notas.append(nota)
    if es_la_novela:
        notas.append("Estos son los valores de la novela.")
    else:
        notas.append(f"Con los valores de la novela, en estas mismas condiciones de azar, se salva en {libro['successes']}.")
    st.markdown("".join(f'<div class="oc-nota">{n}</div>' for n in notas), unsafe_allow_html=True)

    if salvados >= 80:
        veredicto, clase = "El pueblo funciona: la advertencia llega casi siempre a tiempo.", ""
    elif salvados >= 50:
        veredicto, clase = "Una moneda al aire: que Santiago viva depende del azar de la mañana.", "mal"
    elif salvados >= 20:
        veredicto, clase = "Santiago muere en la mayoría de las mañanas.", "mal"
    else:
        veredicto, clase = (
            "Una muerte casi segura. Parece destino, pero es el resultado de cómo está armado el pueblo.",
            "mal",
        )
    if r["failure_causes"] and salvados < 100:
        principal = max(r["failure_causes"], key=r["failure_causes"].get)
        veredicto += (
            f" La causa más frecuente: {CAUSA_CORTA[principal]}. "
            f"Para cambiarla, suba el {REMEDIO[principal]}."
        )
    st.markdown(f'<div class="oc-veredicto {clase}">{veredicto}</div>', unsafe_allow_html=True)

# Globos solo al cruzar el umbral, no en cada movimiento de los controles.
_previo = st.session_state.get("salvados_previo")
if _previo is not None and _previo < 80 <= salvados:
    st.balloons()
st.session_state.salvados_previo = salvados

st.write("")

# ============================================================================
# PESTAÑAS
# ============================================================================
tab_causas, tab_manana, tab_lecciones, tab_modelo = st.tabs(
    ["Por qué muere", "Una mañana, minuto a minuto", "Lecciones", "Cómo funciona"]
)

with tab_causas:
    filas = []
    for causa in ORDEN_CAUSAS:
        n = r["failure_causes"].get(causa, 0)
        color = "#C1442E" if causa in (CAUSA_DESINFORMADO, CAUSA_RUMOR_GANA) else "#7D8893"
        filas.append(
            f'<div class="nombre">{CAUSA_CORTA[causa][0].upper() + CAUSA_CORTA[causa][1:]}'
            f"<small>{EXPLICACION[causa]} Se reduce con: {REMEDIO[causa]}.</small></div>"
            f'<div class="pista" aria-hidden="true"><div class="barra" style="width:{n}%;background:{color}"></div></div>'
            f'<div class="n">{n} de 100</div>'
        )
    st.markdown(f'<div class="oc-causas">{"".join(filas)}</div>', unsafe_allow_html=True)
    st.caption(
        "Pruebe a mover un solo control y mire qué causa cambia. Las cuatro pueden ocurrir; "
        "en la versión anterior de esta app, tres de ellas eran imposibles."
    )


def svg_red(G, creencias, ok, diag):
    """Dibuja la red de una mañana, con las posiciones de la diapositiva «La red que falló»."""

    def trazo(a, b, estilo):
        (x1, y1), (x2, y2) = POS[a], POS[b]
        curva = CURVAS.get(frozenset((a, b)))
        if curva and len(curva) == 2:
            (c1x, c1y), (c2x, c2y) = curva if POS[a][0] < POS[b][0] else curva[::-1]
            d = f"M{x1},{y1} C{c1x},{c1y} {c2x},{c2y} {x2},{y2}"
        elif curva:
            d = f"M{x1},{y1} Q{curva[0][0]},{curva[0][1]} {x2},{y2}"
        else:
            d = f"M{x1},{y1} L{x2},{y2}"
        return f'<path d="{d}" fill="none" {estilo}/>'

    partes = []
    for a, b in RUTAS_LIBRO:
        partes.append(trazo(a, b, 'stroke="#8A949E" stroke-width="2.5"'))
    for a, b in RUTAS_ALTERNATIVAS:
        if G.has_edge(a, b):
            partes.append(trazo(a, b, 'stroke="#004A87" stroke-width="3" stroke-dasharray="8 6"'))
        else:
            partes.append(trazo(a, b, 'stroke="#C8CDD2" stroke-width="2" stroke-dasharray="3 6"'))

    for nodo, (x, y) in POS.items():
        if nodo == GEMELOS:
            fondo, borde, texto = "#10263B", "#10263B", "#F7F4ED"
        elif nodo == SANTIAGO:
            if ok:
                fondo, borde, texto = "#004A87", "#004A87", "#F7F4ED"
            elif diag.get("santiago_desinformado"):
                fondo, borde, texto = "#C1442E", "#C1442E", "#F7F4ED"
            else:
                fondo, borde, texto = "#F7F4ED", "#10263B", "#10263B"
        elif creencias.get(nodo) == AVISO:
            fondo, borde, texto = "#004A87", "#004A87", "#F7F4ED"
        elif creencias.get(nodo) == RUMOR:
            fondo, borde, texto = "#C1442E", "#C1442E", "#F7F4ED"
        else:
            fondo, borde, texto = "#F7F4ED", "#7D8893", "#10263B"
        grosor = 3 if nodo == SANTIAGO else 2
        partes.append(
            f"<g><title>{html.escape(nodo)}</title>"
            f'<rect x="{x - 75}" y="{y - 23}" width="150" height="46" rx="23" fill="{fondo}" '
            f'stroke="{borde}" stroke-width="{grosor}"/>'
            f'<text x="{x}" y="{y + 1}" text-anchor="middle" dominant-baseline="middle" '
            f"font-family=\"IBM Plex Sans, Arial, sans-serif\" font-size=\"19\" font-weight=\"600\" "
            f'fill="{texto}">{CORTO[nodo]}</text></g>'
        )
    return (
        '<div class="oc-red"><svg viewBox="-12 -12 944 442" role="img" '
        'aria-label="Red de personajes del pueblo en una mañana simulada">' + "".join(partes) + "</svg></div>"
    )


with tab_manana:
    numero = st.slider(
        "Elija una de las 100 mañanas",
        1, N_MANANAS, key="manana",
        help="Cada mañana es una de las 100 simulaciones que se contaron arriba.",
    )
    ok, t_aviso, t_ataque, log, diag = una_manana(alpha, beta, gamma, numero, st.session_state.seed)

    if ok:
        resumen = f"En la mañana {numero}, Santiago se salvó: el aviso le llegó en el minuto {t_aviso}."
    else:
        resumen = f"En la mañana {numero}, Santiago murió. Causa: {CAUSA_CORTA[diag['causa']]}."
    st.markdown(f'<div class="oc-veredicto {"" if ok else "mal"}">{resumen}</div>', unsafe_allow_html=True)

    st.markdown(svg_red(diag["red"], diag["creencias"], ok, diag), unsafe_allow_html=True)
    st.markdown(
        '<div class="oc-leyenda-red">'
        '<span><span class="sw" style="background:#004A87"></span>Creyó la advertencia</span>'
        '<span><span class="sw" style="background:#C1442E"></span>Creyó el rumor</span>'
        '<span><span class="sw" style="background:#F7F4ED;border:2px solid #7D8893"></span>No se enteró</span>'
        '<span><span class="ln" style="border-top:2.5px solid #8A949E"></span>Ruta de la novela</span>'
        '<span><span class="ln" style="border-top:3px dashed #004A87"></span>Ruta alternativa que existió</span>'
        '<span><span class="ln" style="border-top:2px dotted #B9C1C9"></span>Ruta que no existió</span>'
        "</div>",
        unsafe_allow_html=True,
    )

    minutos = {}
    finales = []
    for linea in log:
        m = re.match(r"^(\S+)\s+MIN (\d+): (.*)$", linea)
        if m:
            minutos.setdefault(int(m.group(2)), []).append(f"{m.group(1)} {m.group(3)}")
        else:
            finales.append(linea)
    items = [
        f"<li><span>{'Amanecer' if k == 0 else f'Minuto {k}'}</span><span>{'<br>'.join(html.escape(e) for e in v)}</span></li>"
        for k, v in sorted(minutos.items())
    ]
    items += [f"<li><span></span><span>{html.escape(f)}</span></li>" for f in finales]
    st.markdown(f'<ol class="oc-log">{"".join(items)}</ol>', unsafe_allow_html=True)

with tab_lecciones:
    lecciones = [
        (
            "Verificar",
            "Pensamiento crítico, α",
            "«Son habladas de borracho.» Casi nadie se tomó el trabajo de comprobar lo que había oído.",
            "Un agente de IA que obedece una instrucción escondida en un correo falla exactamente aquí. "
            "Y una red rápida, sin verificación, propaga la mentira tan bien como la verdad.",
            "En Derecho, contrastar la prueba antes de alegarla. En Contaduría, dar fe solo de lo comprobado. "
            "En Comunicación, confirmar la fuente antes de publicar. En Salud, no firmar sin revisar el "
            "diagnóstico que propuso la máquina.",
        ),
        (
            "Tener otra ruta",
            "Adaptabilidad, β",
            "La advertencia siguió caminos rígidos: Clotilde le contó al padre Amador, y ahí se quedó. "
            "Cristo Bedoya buscó a Santiago y no lo encontró.",
            "Si su única forma de verificar algo es preguntarle a la misma IA que se lo dijo, no tiene otra ruta.",
            "En Administración, un proveedor de respaldo. En Derecho, evidencia alternativa si falla un testigo. "
            "En Ingeniería, redundancia. En Trabajo Social, conocer otros recursos cuando uno se cierra.",
        ),
        (
            "Filtrar el ruido",
            "Filtrado de ruido, γ⁻¹",
            "Llegaba el obispo en barco, el pueblo tenía la resaca de la boda y el puerto estaba lleno. "
            "La advertencia se perdió en medio de todo eso.",
            "Notificaciones, una novedad de IA por semana, promesas de proveedores. Ante cada una, pregunte por el denominador.",
            "En Derecho, encontrar en 500 páginas lo que decide el caso. En Administración, distinguir lo urgente "
            "de lo importante. En Salud, el triage.",
        ),
    ]
    cols = st.columns(3, gap="large")
    for col, (titulo, variable, novela, hoy, carrera) in zip(cols, lecciones):
        col.markdown(
            f'<div class="oc-leccion"><h4>{titulo}</h4><p class="var">{variable}</p>'
            f"<p><b>En la novela.</b> {novela}</p>"
            f"<p><b>En 2026.</b> {hoy}</p>"
            f"<p><b>En su carrera.</b> {carrera}</p></div>",
            unsafe_allow_html=True,
        )
    st.markdown(
        '<div class="oc-veredicto">García Márquez escribió una muerte que parecía inevitable. Con otro pueblo, '
        "Santiago se salva. Muchos problemas que se nos presentan como destino son, en realidad, sistemas, "
        "y los sistemas se pueden rediseñar.</div>",
        unsafe_allow_html=True,
    )

with tab_modelo:
    st.markdown(
        """
#### Dos mensajes, una red

Por el pueblo circulan dos mensajes: la advertencia verdadera y un rumor falso («son habladas
de borracho, ya le avisaron»). Al empezar la mañana, Clotilde Armenta cree la advertencia y dos
personas al azar creen el rumor. Cada minuto, quien cree algo intenta pasárselo a sus vecinos.

La probabilidad de que un mensaje salte de una persona a otra en un minuto es:
"""
    )
    st.latex(r"P_{\text{transmisión}} = \frac{0{,}15 \times (1 + \beta)}{1 + \gamma}, \qquad \gamma = 1 - \gamma^{-1}")
    st.markdown(
        """
Lo que **no** está en esa fórmula es el pensamiento crítico. Esa variable no decide cuán rápido
circula un mensaje, sino cuál de los dos se cree:

- Con probabilidad α, la persona verifica: acepta la advertencia y descarta el rumor.
- Con probabilidad 1 − α, se queda con lo primero que oyó, sea verdad o mentira.

Si a Santiago le llega primero el rumor, se queda tranquilo, y una advertencia posterior solo le
hace efecto si esta vez verifica. Los gemelos avanzan a velocidad constante: llegan siempre en el
minuto 10.

#### Monte Carlo

Cada mañana sale distinta porque el azar decide quién habla con quién. Por eso se simulan 100
mañanas y se cuenta en cuántas Santiago se salva. Es lo mismo que hace un meteorólogo cuando dice
que hay 60 % de probabilidad de lluvia: simuló muchas veces y llovió en 60 de cada 100.

#### Qué cambió respecto de la versión 2.0

Esta app se auditó en noviembre de 2026 y tenía tres defectos que vale la pena nombrar, porque son
justo los que la charla enseña a detectar:

1. **Solo existía un mensaje, y siempre era verdadero.** «Ser crítico» y «creer todo» daban el
   mismo resultado: el pensamiento crítico estaba decorado, no modelado.
2. **α entraba dos veces:** aceleraba la advertencia y además frenaba a los gemelos. Con α ≥ 0,6
   Santiago se salvaba siempre, aunque las otras dos variables estuvieran en cero.
3. **Cuatro de las cinco causas de fallo eran inalcanzables.** El 100 % de los fallos se reportaba
   como «fragmentación de red».

Un modelo útil no es un modelo correcto. Saber dónde falla el propio es la competencia que la
charla quiere practicar.
"""
    )

# ============================================================================
# PIE
# ============================================================================
_pie_uni = f"Charla para estudiantes de la {UNI['nombre']}, {UNI['contexto'].lower()}.<br>" if UNI["nombre"] else ""
st.markdown(
    '<div class="oc-pie">'
    "<b>Operación Crónica</b>, simulación educativa basada en <i>Crónica de una muerte anunciada</i>, "
    "de Gabriel García Márquez.<br>"
    "Germán Gómez Vargas, Instituto de Data Science, Universidad del Desarrollo, Chile.<br>"
    f"{_pie_uni}"
    'Código abierto: <a href="https://github.com/gear-go/operacion-cronica">github.com/gear-go/operacion-cronica</a>'
    "</div>",
    unsafe_allow_html=True,
)
