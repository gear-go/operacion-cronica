import streamlit as st
import networkx as nx
import random
import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict
import numpy as np

from modelo import (
    CAUSA_DESINFORMADO,
    CAUSA_FRAGMENTADA,
    CAUSA_LENTO,
    CAUSA_RUMOR_GANA,
    create_network,
    run_monte_carlo,
    simulate_single_run,
)

# ============================================================================
# INSTITUCIÓN ANFITRIONA
# ============================================================================
# Se elige con un parámetro de URL, para no tener que editar el código en cada
# charla:  https://salvando-santiago.streamlit.app/?uni=americana
INSTITUCIONES = {
    "americana": {
        "nombre": "Corporación Universitaria Americana",
        "lugar": "Barranquilla, Medellín y Montería, Colombia",
        "contexto": "Visita Académica 2026",
    },
    "uajs": {
        "nombre": "Corporación Universitaria Antonio José de Sucre",
        "lugar": "Sincelejo, Colombia",
        "contexto": "Visita Académica UAJS 2025",
    },
    "generica": {
        "nombre": "",
        "lugar": "",
        "contexto": "",
    },
}

try:
    _uni_key = st.query_params.get("uni", "americana")
except Exception:  # Streamlit antiguo
    _uni_key = "americana"
UNI = INSTITUCIONES.get(str(_uni_key).lower(), INSTITUCIONES["americana"])

# ============================================================================
# CONFIGURACIÓN DE LA APP
# ============================================================================

st.set_page_config(
    layout="wide", 
    page_title="Operación Crónica: Simulación de Redes",
    page_icon="🛡️"
)

# Estilo moderno con mejores prácticas UX 2025
st.markdown("""
<style>
    /* Variables de diseño */
    :root {
        --primary: #00FFFF;
        --secondary: #FFD700;
        --danger: #FF0040;
        --success: #00FF00;
        --bg-dark: #0d1117;
        --bg-card: #161b22;
        --border-radius: 12px;
        --shadow: 0 4px 6px rgba(0, 255, 255, 0.1);
    }
    
    .main {
        background-color: var(--bg-dark);
        color: var(--primary);
    }
    
    /* Botón mejorado con hover */
    .stButton>button {
        background: linear-gradient(135deg, #FF0040 0%, #FF4060 100%);
        color: white;
        font-weight: 600;
        border: 2px solid var(--primary);
        border-radius: var(--border-radius);
        padding: 0.75rem 2rem;
        transition: all 0.3s ease;
        box-shadow: var(--shadow);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(255, 0, 64, 0.3);
        border-color: var(--secondary);
    }
    
    /* Cards mejorados */
    .metric-box {
        background-color: var(--bg-card);
        padding: 1.5rem;
        border-radius: var(--border-radius);
        border-left: 4px solid var(--primary);
        margin: 1rem 0;
        box-shadow: var(--shadow);
        transition: transform 0.2s ease;
    }
    
    .metric-box:hover {
        transform: translateX(4px);
    }
    
    /* Tabs modernos */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 0.5rem 1rem;
        background-color: var(--bg-card);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--primary);
        color: var(--bg-dark);
    }
</style>
""", unsafe_allow_html=True)

# Header con componentes nativos
st.title("🛡️ OPERACIÓN CRÓNICA: Hackeando la Fatalidad")
st.markdown("**v3.0** | Simulación educativa interactiva basada en Monte Carlo")

st.markdown("---")

# Información del autor con componente nativo
_para = (
    f"**Para:** Estudiantes de la {UNI['nombre']}, {UNI['lugar']}  \n"
    f"**Contexto:** {UNI['contexto']}"
    if UNI["nombre"]
    else ""
)
st.info(
    "👨‍🏫 **Presentado por:** Dr. Germán Gómez Vargas, "
    "Instituto de Data Science, Universidad del Desarrollo (Chile)  \n" + _para
)

# Sección de misión con componentes nativos
st.subheader("🎯 ¿DE QUÉ TRATA ESTA SIMULACIÓN?")

st.info("""
📖 **En el libro:** En "Crónica de una muerte anunciada" de Gabriel García Márquez, 
**todo el pueblo sabía que iban a matar a Santiago Nasar**, pero nadie logró avisarle 
a tiempo. La tragedia parecía "inevitable", pero... **¿realmente lo era?**
""")

st.success("""
🎮 **TU MISIÓN:** Modificar las características del sistema social (pensamiento crítico, 
adaptabilidad, capacidad de filtrar información) para que la advertencia llegue a Santiago 
antes que los gemelos Vicario lo ataquen.
""")

st.warning("""
💡 **LA LECCIÓN:** Lo que parecía "destino" era en realidad un **fallo del sistema social**. 
Con las habilidades correctas, el resultado puede cambiar radicalmente.
""")

st.markdown("")

# ============================================================================
# CONTROLES DE SIMULACIÓN (SIDEBAR)
# ============================================================================

st.sidebar.header("⚙️ CONTROLES DE LA SIMULACIÓN")
st.sidebar.markdown("---")

st.sidebar.markdown("### 🧠 PENSAMIENTO CRÍTICO")
st.sidebar.markdown("""
Por el pueblo circulan **dos mensajes**: la advertencia verdadera y el rumor de que
"son habladas de borracho, ya le avisaron". Esta variable mide cuánta gente
**verifica antes de repetir**.

Quien verifica se queda con la advertencia y descarta el rumor. Quien no verifica
se queda con lo primero que oyó, sea verdad o mentira.

**En 2026 esto tiene nombre técnico:** un agente de IA que ejecuta una instrucción
escondida en un correo está fallando exactamente aquí.
""")
critical_thinking = st.sidebar.slider(
    "Nivel de Pensamiento Crítico",
    min_value=0.0, max_value=1.0, value=0.08, step=0.05,
    help="0.0 = nadie verifica, se cree lo primero que llega | 1.0 = todos verifican antes de repetir"
)
st.sidebar.caption(f"Valor actual: {critical_thinking:.2f} {'(Libro: 0.08)' if critical_thinking == 0.08 else ''}")

st.sidebar.markdown("---")

st.sidebar.markdown("### 🌐 ADAPTABILIDAD")
st.sidebar.markdown("""
¿Puede la comunidad encontrar rutas alternativas cuando una falla?

**Ejemplo del libro:** Si el Padre Amador olvida avisar, ¿hay otra persona que pueda hacerlo? 
**Alta adaptabilidad = múltiples caminos de comunicación.**
""")
adaptability = st.sidebar.slider(
    "Nivel de Adaptabilidad", 
    min_value=0.0, max_value=1.0, value=0.15, step=0.05,
    help="0.0 = Una sola ruta de información | 1.0 = Muchas rutas alternativas"
)
st.sidebar.caption(f"Valor actual: {adaptability:.2f} {'(Libro: 0.15)' if adaptability == 0.15 else ''}")

st.sidebar.markdown("---")

st.sidebar.markdown("### 📢 RESOLUCIÓN DE PROBLEMAS")
st.sidebar.markdown("""
¿Qué tan bien filtra la comunidad el ruido para enfocarse en lo importante?

**Ejemplo del libro:** La llegada del Obispo distrajo a todo el pueblo. El puerto estaba 
lleno de actividad. **Baja resolución = información crítica se pierde en el caos.**
""")
problem_solving = st.sidebar.slider(
    "Capacidad de Filtrar Ruido", 
    min_value=0.0, max_value=1.0, value=0.08, step=0.05,
    help="0.0 = Caos total, información se pierde | 1.0 = Enfoque perfecto en lo crítico"
)
st.sidebar.caption(f"Valor actual: {problem_solving:.2f} {'(Libro: 0.08)' if problem_solving == 0.08 else ''}")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎲 CONFIGURACIÓN AVANZADA")

st.sidebar.info("""
**¿Qué es "Monte Carlo"?**

Es ejecutar la simulación muchas veces (como tirar dados repetidamente) para obtener 
un **promedio estadístico**. Más simulaciones = resultado más confiable.
""")

num_simulations = st.sidebar.number_input(
    "Número de simulaciones", 
    min_value=10, max_value=500, value=100, step=10,
    help="Recomendado: 100 simulaciones para balance entre velocidad y precisión"
)

show_network = st.sidebar.checkbox("Mostrar la red social de personajes", value=True)

modo_demo = st.sidebar.checkbox(
    "Modo demo (resultado reproducible)",
    value=False,
    help="Fija la semilla aleatoria para que la cifra proyectada no cambie entre corridas. "
         "Útil cuando el número tiene que coincidir con una diapositiva.",
)
semilla = 2026 if modo_demo else None

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='font-size: 0.85em; background-color: #0d1117; padding: 10px; border-radius: 5px; border: 1px solid #FF0040;'>
<b style='color: #FF0040;'>⚠️ IMPORTANTE:</b><br>
<span style='color: #00FFFF;'>
Los resultados varían entre ejecuciones porque es una simulación <b>probabilística</b> 
(como el clima o las redes sociales reales). El valor importante es el <b>promedio</b> 
de muchas simulaciones, no una sola corrida.
</span>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='font-size: 0.8em; color: #666;'>
<b>VALORES DEL LIBRO ORIGINAL:</b><br>
Pensamiento Crítico = 0.08<br>
Adaptabilidad = 0.15<br>
Resolución de Problemas = 0.08<br>
<br>
<b>Resultado histórico:</b> 💀 Santiago muere (10-20% de éxito)
</div>
""", unsafe_allow_html=True)

# ============================================================================
# MOTOR DE SIMULACIÓN
# ============================================================================
# El motor vive en modelo.py para poder probarlo sin levantar Streamlit.
# Ver test_modelo.py.

# ============================================================================
# VISUALIZACIÓN DE RED
# ============================================================================

def visualize_network(G):
    """Genera visualización del grafo con estilo cyberpunk"""
    fig, ax = plt.subplots(figsize=(12, 8), facecolor='#0d1117')
    ax.set_facecolor('#0d1117')
    
    # Layout con más espacio entre nodos
    pos = nx.spring_layout(G, k=2.0, iterations=50, seed=42)
    
    # Colores por tipo de nodo
    node_colors = []
    for node in G.nodes():
        if node == "SANTIAGO NASAR":
            node_colors.append('#FFD700')  # Gold para objetivo
        elif "Gemelos" in node:
            node_colors.append('#FF0040')  # Rojo para amenaza
        elif any(key in node for key in ["Policía", "Coronel", "Padre"]):
            node_colors.append('#00FF00')  # Verde para autoridades
        else:
            node_colors.append("#00D9FF")  # Cyan claro para civiles
    
    # Calcular grosor de aristas basado en centralidad
    # Las conexiones más "importantes" serán más gruesas
    edge_betweenness = nx.edge_betweenness_centrality(G)
    
    # Normalizar valores para grosor (mínimo 2, máximo 8)
    max_betweenness = max(edge_betweenness.values()) if edge_betweenness else 1
    edge_widths = []
    edge_colors = []
    
    for edge in G.edges():
        # Grosor basado en betweenness (qué tan crítica es la conexión)
        betweenness = edge_betweenness.get(edge, edge_betweenness.get((edge[1], edge[0]), 0))
        width = 2 + (betweenness / max_betweenness) * 6  # Rango: 2-8
        edge_widths.append(width)
        
        # Color más brillante para conexiones críticas a Santiago
        if "SANTIAGO NASAR" in edge:
            edge_colors.append('#FFD700')  # Dorado para conexiones a Santiago
        elif "Clotilde" in edge[0] or "Clotilde" in edge[1]:
            edge_colors.append('#00FFFF')  # Cyan para conexiones desde Clotilde (fuente)
        else:
            edge_colors.append('#58a6ff')  # Azul más visible para otras conexiones
    
    # Dibujar aristas con grosor variable y colores
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, 
                          width=edge_widths, alpha=0.8, ax=ax)
    
    # Dibujar nodos con borde para mejor contraste
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                          node_size=2000, alpha=0.95, 
                          edgecolors='white', linewidths=2, ax=ax)
    
    # Labels con mejor contraste
    nx.draw_networkx_labels(G, pos, font_size=8, font_color='white', 
                           font_weight='bold', ax=ax)
    
    ax.set_title("/// RED SOCIAL: CRÓNICA DE UNA MUERTE ANUNCIADA ///", 
                color='#FFD700', fontsize=16, fontweight='bold', 
                family='monospace', pad=20)
    
    # Leyenda
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#FFD700', label='Santiago Nasar (Objetivo)'),
        Patch(facecolor='#FF0040', label='Gemelos Vicario (Amenaza)'),
        Patch(facecolor='#00FF00', label='Autoridades'),
        Patch(facecolor='#00D9FF', label='Civiles')
    ]
    ax.legend(handles=legend_elements, loc='upper left', 
             facecolor='#161b22', edgecolor='#30363d', 
             labelcolor='white')
    
    plt.axis('off')
    plt.tight_layout()
    
    return fig

# ============================================================================
# INTERFAZ PRINCIPAL
# ============================================================================

# Botón principal con mejor diseño
st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)

if st.button("🚀 EJECUTAR SIMULACIÓN MONTE CARLO", width="stretch", type="primary"):
    # Progress bar moderno
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    status_text.text("🔄 Inicializando simulación...")
    progress_bar.progress(10)
    
    # Ejecutar Monte Carlo
    results = run_monte_carlo(
        critical_thinking, adaptability, problem_solving, num_simulations, seed=semilla
    )
    
    progress_bar.progress(100)
    status_text.text("✅ Simulación completada!")
    
    import time
    time.sleep(0.5)
    progress_bar.empty()
    status_text.empty()
        
    # ========== RESULTADOS PRINCIPALES ==========
    st.markdown("---")
    
    # Header de resultados con diseño moderno
    st.markdown("""
    <div style='text-align: center; margin: 2rem 0;'>
        <h2 style='background: linear-gradient(90deg, #00FFFF, #FFD700); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   font-size: 2rem; margin-bottom: 0.5rem;'>
        📊 RESULTADOS DE LA SIMULACIÓN
        </h2>
        <p style='color: #888; font-size: 1rem;'>Análisis de {num_simulations} escenarios paralelos</p>
    </div>
    """.format(num_simulations=num_simulations), unsafe_allow_html=True)
    
    # Métricas principales con mejor diseño
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        success_rate = results["success_rate"]
        delta_color = "normal" if success_rate > 50 else "inverse"
        
        # Métrica principal con componente nativo
        st.metric(
            label="🎯 TASA DE ÉXITO",
            value=f"{success_rate:.1f}%",
            delta=f"{results['successes']}/{num_simulations} simulaciones exitosas" if success_rate >= 50 else None
        )
    
    with col2:
        if results["avg_alert_time"]:
            st.metric(
                "⏱️ TIEMPO PROMEDIO DE ALERTA",
                f"{results['avg_alert_time']:.1f} min",
                help="Tiempo hasta que Santiago recibe el aviso"
            )
        else:
            st.metric("⏱️ TIEMPO PROMEDIO DE ALERTA", "N/A", help="Sin alertas exitosas")
    
    with col3:
        if results["avg_attack_time"]:
            st.metric(
                "⚔️ TIEMPO PROMEDIO DE ATAQUE",
                f"{results['avg_attack_time']:.1f} min",
                help="Cuando los gemelos ejecutan su plan"
            )
        else:
            st.metric("⚔️ TIEMPO PROMEDIO DE ATAQUE", "N/A", help="Sin ataques registrados")

    with col4:
        st.metric(
            "🌀 SANTIAGO DESINFORMADO",
            f"{results['misinformed_rate']:.1f}%",
            help="Porcentaje de simulaciones en que a Santiago le llegó primero el rumor "
                 "falso y se quedó tranquilo. Suba el Pensamiento Crítico para reducirlo.",
        )
    
    # ========== VEREDICTO CON COMPONENTES NATIVOS ==========
    st.markdown("---")
    
    if success_rate >= 80:
        st.markdown("# 🎉")
        st.success("""
        ### ÉXITO SISTÉMICO
        
        Santiago se salva en la mayoría de los escenarios. 
        La arquitectura de red es **resiliente** y puede propagar información crítica a tiempo.
        """)
        st.balloons()
    elif success_rate >= 50:
        st.markdown("# ⚠️")
        st.warning("""
        ### ÉXITO PARCIAL
        
        Santiago tiene 50/50 de posibilidades. El sistema es **inestable** y 
        depende mucho del azar. Considera aumentar los parámetros.
        """)
    elif success_rate >= 20:
        st.markdown("# ❌")
        st.error("""
        ### FALLO PROBABLE
        
        Santiago muere en la mayoría de los casos. El sistema tiene **fallos críticos**. 
        Intenta ajustar los parámetros para mejorar la propagación.
        """)
    else:
        st.markdown("# 💀")
        st.error("""
        ### FALLO SISTÉMICO TOTAL
        
        Replicaste las condiciones del libro. El "destino" está **programado** por 
        un sistema social con bajo pensamiento crítico, poca adaptabilidad y mucho ruido.
        """)
    
    # ========== TABS PARA ORGANIZAR INFORMACIÓN ==========
    st.markdown("")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Análisis Detallado", "🌐 Red Social", "📊 Comparación con el Libro", "🎓 Lecciones"])
    
    with tab1:
        # ========== ANÁLISIS DE FALLOS ==========
        if results["failure_causes"]:
            st.markdown("### 🔍 Análisis de Causas de Fallo")
            
            failure_df = pd.DataFrame([
                {"Causa": causa, "Frecuencia": freq}
                for causa, freq in results["failure_causes"].items()
            ]).sort_values("Frecuencia", ascending=False)
            
            st.dataframe(failure_df, width="stretch", hide_index=True)
            
            st.info(f"""
**💡 Interpretación:**

• **{CAUSA_DESINFORMADO}:** llegó primero el rumor y nadie lo verificó → ↑ Pensamiento Crítico
• **{CAUSA_RUMOR_GANA}:** el rumor ocupó la red antes que la advertencia → ↑ Pensamiento Crítico
• **{CAUSA_FRAGMENTADA}:** la advertencia nunca encontró una ruta hasta Santiago → ↑ Adaptabilidad
• **{CAUSA_LENTO}:** la advertencia iba en camino, pero se acabó el tiempo → ↑ Filtrado de Ruido

Las cuatro causas son alcanzables: pruebe a mover un solo control y vea cuál cambia.
            """)
    
    with tab2:
        # ========== VISUALIZACIÓN DE RED ==========
        if show_network:
            st.markdown("### 🌐 La Red Social del Pueblo")
            
            # Explicación pedagógica
            st.info("""
**📚 ¿Qué es una Red Social?**

Imagina que cada persona del pueblo es un **punto (nodo)** y las relaciones 
entre ellos son **líneas (aristas)**. Por ejemplo, si Clotilde le habla a 
Cristo Bedoya, hay una línea conectándolos.

🔵 **Nodos:** Cada personaje  
━━ **Aristas:** Relaciones  
📊 **Densidad:** Conectividad

**En esta simulación:** El mensaje intenta "viajar" por estas líneas desde 
Clotilde hasta Santiago. Mientras más conexiones, más fácil llega.
            """)
            
            sample_network = create_network(adaptability)
            fig = visualize_network(sample_network)
            st.pyplot(fig)
            
            # Métricas de red con mejor diseño
            st.markdown("#### 📊 Estadísticas de la Red")
            metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
            
            with metrics_col1:
                st.metric("👥 Nodos", len(sample_network.nodes()), help="Cantidad de personas en la red")
            with metrics_col2:
                st.metric("🔗 Aristas", len(sample_network.edges()), help="Cantidad de relaciones activas")
            with metrics_col3:
                density = nx.density(sample_network)
                st.metric("📊 Densidad", f"{density:.3f}", help="0.0 = Aislado | 1.0 = Todos conectados")
            
            st.info("💡 **Tip:** Si aumentas la **Adaptabilidad** y vuelves a ejecutar, verás más conexiones entre personajes.")
        else:
            st.info("👆 Activa 'Mostrar visualización de red' en el sidebar para ver el grafo")
    
    with tab3:
        # ========== COMPARACIÓN CON LIBRO ==========
        st.markdown("### 📖 Comparación con el Libro Original")
        
        st.warning("""
**❓ ¿Por qué los resultados varían con los mismos parámetros?**

Porque esta es una simulación **probabilística** (como el clima). 
Cada ejecución, el mensaje toma rutas diferentes. Lo importante es el **promedio** 
de muchas simulaciones, no una sola.
        """)
        
        # Valores históricos (calibrados)
        with st.spinner("Calculando escenario del libro..."):
            historical_results = run_monte_carlo(0.08, 0.15, 0.08, 100)
        
        comparison_df = pd.DataFrame({
            "Escenario": ["Tu Simulación", "Libro Original"],
            "Tasa de Éxito": [f"{results['success_rate']:.1f}%", f"{historical_results['success_rate']:.1f}%"],
            "Pensamiento Crítico": [f"{critical_thinking:.2f}", "0.08"],
            "Adaptabilidad": [f"{adaptability:.2f}", "0.15"],
            "Resolución de Problemas": [f"{problem_solving:.2f}", "0.08"]
        })
        
        st.dataframe(comparison_df, width="stretch", hide_index=True)
        
        improvement = results['success_rate'] - historical_results['success_rate']
        
        col_interp1, col_interp2 = st.columns([3, 1])
        with col_interp1:
            st.markdown(f"""
            <div style='background-color: rgba(0, 255, 255, 0.05); padding: 1rem; border-radius: 8px; margin-top: 1rem;'>
                <p style='color: #FFD700; font-size: 0.95em; margin: 0; line-height: 1.6;'>
                <b>💡 Interpretación:</b> El libro tenía parámetros muy bajos (0.08, 0.15, 0.08). 
                Con estos valores, Santiago se salva solo en ~{historical_results['success_rate']:.0f}% de los casos. 
                <b>La tragedia no era destino, era estadística.</b>
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_interp2:
            if improvement > 10:
                st.success(f"🎉 +{improvement:.1f}%")
            elif improvement > 0:
                st.info(f"✅ +{improvement:.1f}%")
            elif improvement < -10:
                st.error(f"❌ {improvement:.1f}%")
            else:
                st.warning("➡️ Similar")
    
    with tab4:
        # ========== LECCIONES EDUCATIVAS ==========
        st.markdown("### 🎓 Lecciones para Todas las Carreras")
        
        st.markdown("""
        <div style='background-color: rgba(0, 255, 255, 0.05); padding: 1rem; border-radius: 8px; margin-bottom: 1rem;'>
            <p style='color: #00FFFF; font-size: 0.95em; margin: 0; line-height: 1.6;'>
            Esta simulación es relevante para <b>CUALQUIER carrera</b>: Derecho, Administración, 
            Trabajo Social, Ingeniería, Salud, Comunicación, etc. Todos trabajamos con 
            <b>información</b>, <b>redes</b> y <b>decisiones</b>.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Crear sub-tabs dentro de tab4
        lesson_tab1, lesson_tab2, lesson_tab3, lesson_tab4 = st.tabs([
            "🧠 Pensamiento Crítico",
            "🌐 Adaptabilidad",
            "🎯 Resolución de Problemas",
            "💡 Destino vs Diseño"
        ])
        
        with lesson_tab1:
            st.markdown("""
            #### El Pensamiento Crítico Salva Vidas
            
            **En el libro:** Muchos escucharon el rumor pero lo descartaron:
            - *"Son habladas de borracho"* ❌
            - *"No es asunto mío"* ❌  
            - *"Seguro es mentira"* ❌
            
            **Aplicaciones en tu carrera:**
            
            - **Derecho:** ¿Evalúas críticamente las pruebas o te dejas llevar por prejuicios?
            - **Administración:** ¿Analizas datos antes de decidir o sigues "la intuición"?
            - **Salud:** ¿Verificas síntomas o asumes que "no es nada grave"?
            - **Comunicación:** ¿Chequeas fuentes antes de compartir información?
            - **Ingeniería:** ¿Ignoras alertas del sistema porque "siempre hay falsas alarmas"?
            
            **Lección:** Un sistema (o persona) sin pensamiento crítico **no diferencia lo importante de lo trivial**.
            """)
        
        with lesson_tab2:
            st.markdown("""
            #### Tener un Plan B (y C, y D)
            
            **En el libro:** La información siguió rutas rígidas:
            - Clotilde → Padre Amador → Madre → ❌ (falló)
            - Cristo Bedoya → Buscó a Santiago → ❌ (no lo encontró)
            
            **Aplicaciones en tu carrera:**
            
            - **Derecho:** Si un testigo clave falla, ¿tienes evidencia alternativa?
            - **Administración:** Si un proveedor falla, ¿tienes respaldo?
            - **Salud:** Si un especialista no está, ¿hay otro para emergencias?
            - **Trabajo Social:** Si un recurso cierra, ¿conoces alternativas?
            - **Ingeniería:** Si un servidor cae, ¿hay redundancia?
            
            **Lección:** Los sistemas resilientes tienen **múltiples caminos** para lograr el objetivo.
            """)
        
        with lesson_tab3:
            st.markdown("""
            #### Filtrar el Ruido
            
            **En el libro:** Había demasiadas distracciones:
            - 🚢 Llegada del Obispo (todo el pueblo al puerto)
            - 🍺 Resaca después de la boda
            - 📢 Puerto lleno de ruido
            
            **Aplicaciones en tu carrera:**
            
            - **Derecho:** En 500 páginas de evidencia, ¿identificas lo clave?
            - **Administración:** Con 50 emails, ¿priorizas lo urgente vs. importante?
            - **Salud:** En emergencia con múltiples pacientes, ¿triage efectivo?
            - **Comunicación:** En redes sociales, ¿qué merece atención?
            - **Psicología:** Con múltiples síntomas, ¿cuál es el diagnóstico principal?
            
            **Lección:** La capacidad de **enfocarse en lo crítico** y filtrar lo irrelevante es tan importante como tener la información.
            """)
        
        with lesson_tab4:
            st.markdown("""
            #### El "Destino" Era un Problema de Diseño
            
            **La gran revelación:** García Márquez escribió sobre inevitabilidad, pero esta 
            simulación demuestra que con las habilidades correctas, Santiago **podría haberse salvado**.
            
            **Esto aplica a problemas modernos reales:**
            
            - **Cambio climático:** ¿Es "inevitable" o es falta de acción colectiva?
            - **Pobreza:** ¿Es "destino" o son sistemas mal diseñados?
            - **Corrupción:** ¿Es "inevitable" o falta transparencia y pensamiento crítico?
            - **Desinformación:** ¿Es "imposible de detener" o falta educación mediática?
            - **Desigualdad:** ¿Es "natural" o son políticas deficientes?
            
            **Lección Final:** Lo que parece "destino inevitable" muchas veces es un **problema solucionable** si desarrollamos:
            
            1. ✅ **Pensamiento crítico** (evaluar información)
            2. ✅ **Adaptabilidad** (crear soluciones alternativas)
            3. ✅ **Resolución de problemas** (enfocarse en lo importante)
            """)

# ============================================================================
# SECCIÓN DE DETALLES TÉCNICOS (Opcional)
# ============================================================================

st.markdown("---")

with st.expander("🔬 Detalles Técnicos (Para Curiosos)"):
    st.markdown("""
    <div style='background-color: #161b22; padding: 15px; border-radius: 10px; margin-bottom: 15px;'>
        <p style='color: #FFD700; font-size: 1em; margin: 0;'>
        <b>Nota:</b> Esta sección es opcional. Solo si te interesa saber cómo funciona 
        "por debajo del capó". No es necesario entenderlo para usar la simulación.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ### 🧮 La Matemática Detrás de la Simulación

    Por la red circulan **dos mensajes**: la advertencia verdadera y un rumor falso
    ("son habladas de borracho, ya le avisaron"). Cada minuto, cada persona que cree
    algo intenta pasárselo a sus vecinos.

    **Probabilidad de que un mensaje salte de una persona a otra:**

    $$P_{transmisión} = \\frac{0.15 \\times (1 + Adaptabilidad)}{1 + Ruido}$$

    Fíjese en lo que **no** está en esa fórmula: el pensamiento crítico. Esa variable
    no decide cuán rápido circula un mensaje, sino **cuál de los dos se cree**:

    - Con probabilidad α, la persona **verifica**: acepta la advertencia y descarta el rumor.
    - Con probabilidad 1 − α, se queda con **lo primero que oyó**, sea verdad o mentira.

    Y si a Santiago le llega primero el rumor, queda tranquilo: una advertencia posterior
    solo le hace efecto si esta vez verifica.

    **Los gemelos avanzan a velocidad constante**, 10 % por minuto: el plazo son siempre
    10 minutos. No depende de ninguna de las tres variables.

    ---

    ### ⚠️ Qué cambió respecto de la versión 2.0, y por qué

    Esta app se auditó en noviembre de 2026 y tenía tres defectos que vale la pena
    nombrar, porque ilustran justamente lo que la charla enseña:

    1. **Solo existía un mensaje, y siempre era verdadero.** Así que "ser crítico" y
       "creer todo" producían el mismo resultado. El pensamiento crítico no estaba
       modelado: estaba decorado.
    2. **α entraba dos veces:** aceleraba la advertencia y además frenaba a los gemelos.
       Por encima de 0,67 los gemelos ya no alcanzaban a llegar dentro de la ventana y
       el plazo desaparecía. Con α ≥ 0,6 Santiago se salvaba siempre, aunque las otras
       dos variables estuvieran en cero.
    3. **Cuatro de las cinco causas de fallo documentadas eran inalcanzables.** El 100 %
       de los fallos se reportaba como "fragmentación de red".

    Un modelo útil no es un modelo correcto. Saber dónde falla el propio es la
    competencia que la charla quiere practicar.

    ---

    ### 🎲 ¿Qué es "Monte Carlo"?
    
    Es un método de la estadística que consiste en:
    1. Ejecutar el experimento muchas veces (100 simulaciones)
    2. Cada vez, el azar hace que las cosas sucedan ligeramente diferente
    3. Al final, calcular el promedio de todas las veces
    
    **Analogía:** Es como preguntar "¿Qué probabilidad hay de que llueva mañana?". 
    Los meteorólogos simulan el clima 100 veces con pequeñas variaciones y dicen 
    "llovió en 60 de 100 simulaciones, entonces hay 60% de probabilidad".
    
    Por eso los resultados varían entre ejecuciones: **es probabilístico, no determinista**.
    """)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
_footer_uni = (
    f"<p><b>Para:</b> Estudiantes de la {UNI['nombre']}, {UNI['lugar']}</p>"
    f"<p>{UNI['contexto']} | 📚 Uso académico | 🔓 Código abierto</p>"
    if UNI["nombre"]
    else "<p>📚 Uso académico | 🔓 Código abierto</p>"
)
st.markdown(
    """
<div style='text-align: center; color: #666; font-size: 0.9em;'>
    <p>🛡️ <b>Operación Crónica</b> - Simulación educativa basada en "Crónica de una muerte anunciada" de Gabriel García Márquez</p>
    <p><b>Presentado por:</b> Dr. Germán Gómez Vargas, Instituto de Data Science, Universidad del Desarrollo (Chile)</p>
    """
    + _footer_uni
    + "</div>",
    unsafe_allow_html=True,
)
