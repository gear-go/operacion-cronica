import streamlit as st
import networkx as nx
import random
import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict
import numpy as np

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
st.markdown("**v2.0** | Simulación educativa interactiva basada en Monte Carlo")

st.markdown("---")

# Información del autor con componente nativo
st.info("""
👨‍🏫 **Presentado por:** Dr. Germán Gómez Vargas, Universidad del Desarrollo (Chile)  
**Para:** Estudiantes de la Corporación Universitaria San José de Sucre, Sincelejo, Colombia  
**Contexto:** Visita Académica UAJS 2025
""")

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
¿Qué tan en serio toma la gente la información que recibe?

**Ejemplo del libro:** Muchos escucharon el rumor pero lo descartaron como 
"habladas de borracho". **Bajo pensamiento crítico = ignorar señales importantes.**
""")
critical_thinking = st.sidebar.slider(
    "Nivel de Pensamiento Crítico", 
    min_value=0.0, max_value=1.0, value=0.08, step=0.05,
    help="0.0 = Nadie toma en serio la información | 1.0 = Todos evalúan y actúan"
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

def create_network(beta):
    """Construye el grafo social con rutas base + adaptativas"""
    G = nx.Graph()
    
    # Personajes clave
    nodes = [
        "Gemelos Vicario",
        "Clotilde Armenta",
        "Leandro Pornoy (Policía)",
        "Coronel Lázaro Aponte",
        "Padre Carmen Amador",
        "Cristo Bedoya",
        "Plácida Linero (Madre)",
        "Victoria Guzmán (Cocinera)",
        "SANTIAGO NASAR"
    ]
    
    G.add_nodes_from(nodes)
    
    # Conexiones del libro (estructura base)
    base_edges = [
        ("Gemelos Vicario", "Clotilde Armenta"),
        ("Clotilde Armenta", "Leandro Pornoy (Policía)"),
        ("Clotilde Armenta", "Padre Carmen Amador"),
        ("Clotilde Armenta", "Cristo Bedoya"),
        ("Leandro Pornoy (Policía)", "Coronel Lázaro Aponte"),
        ("Padre Carmen Amador", "Plácida Linero (Madre)"),
        ("Cristo Bedoya", "SANTIAGO NASAR"),
        ("Plácida Linero (Madre)", "SANTIAGO NASAR"),
        ("Victoria Guzmán (Cocinera)", "SANTIAGO NASAR")
    ]
    
    G.add_edges_from(base_edges)
    
    # Rutas alternativas que se activan con alta adaptabilidad
    potential_edges = [
        ("Clotilde Armenta", "SANTIAGO NASAR"),  # Ruta directa
        ("Leandro Pornoy (Policía)", "Cristo Bedoya"),  # Bypass del cura
        ("Coronel Lázaro Aponte", "Plácida Linero (Madre)"),  # Autoridad a madre
        ("Coronel Lázaro Aponte", "SANTIAGO NASAR"),  # Autoridad directa
        ("Padre Carmen Amador", "Cristo Bedoya"),  # Red eclesiástica
        ("Victoria Guzmán (Cocinera)", "Plácida Linero (Madre)")  # Personal doméstico
    ]
    
    # Activar rutas según adaptabilidad
    for edge in potential_edges:
        if random.random() < beta:
            G.add_edge(*edge)
    
    return G

def simulate_single_run(alpha, beta, gamma_inv, max_minutes=15):
    """
    Ejecuta una simulación Monte Carlo
    
    Returns:
        success (bool): ¿Santiago fue alertado?
        time_alerted (int): Minuto en que fue alertado (o -1)
        time_attack (int): Minuto en que los gemelos atacan
        log (list): Registro de eventos
    """
    G = create_network(beta)
    
    # Estado inicial
    informed_nodes = {"Clotilde Armenta"}  # Primera en saber
    santiago_alerted = False
    time_alerted = -1
    
    # Progreso de los gemelos (%)
    vicario_progress = 0
    # Velocidad base: 100% en 10 minutos = 10% por minuto
    # Se reduce si hay mucho pensamiento crítico (intentos de detención)
    base_speed = 10
    
    log = []
    
    for minute in range(1, max_minutes + 1):
        # ========== FASE 1: PROPAGACIÓN DEL MENSAJE ==========
        new_informed = set()
        
        for node in informed_nodes:
            if node in G:
                neighbors = list(G.neighbors(node))
                for neighbor in neighbors:
                    if neighbor not in informed_nodes:
                        # FÓRMULA CORE: Probabilidad de transmisión exitosa
                        # P_tx = (α × (1 + β)) / (1 + γ)
                        # donde γ = (1 - γ_inv), entonces:
                        # P_tx = (α × (1 + β)) / (2 - γ_inv)
                        
                        gamma = 1 - gamma_inv  # Convertir "reducción de ruido" a "nivel de ruido"
                        prob_transmission = (alpha * (1 + beta)) / (1 + gamma)
                        
                        if random.random() < prob_transmission:
                            new_informed.add(neighbor)
                            
                            if neighbor == "SANTIAGO NASAR":
                                santiago_alerted = True
                                time_alerted = minute
                                log.append(f"✅ MIN {minute}: ¡SANTIAGO ALERTADO por {node}!")
                                return True, time_alerted, minute, log
        
        informed_nodes.update(new_informed)
        
        if new_informed:
            log.append(f"📢 MIN {minute}: Mensaje propagado a {len(new_informed)} nuevos nodos")
        else:
            log.append(f"🚫 MIN {minute}: Mensaje estancado (sin nuevas propagaciones)")
        
        # ========== FASE 2: AVANCE DE LOS GEMELOS ==========
        # El pensamiento crítico genera intentos de detención que los ralentizan
        intervention_factor = alpha * 5  # Máximo 5% de reducción
        effective_speed = max(base_speed - intervention_factor, 5)  # Mínimo 5% para que no se detengan totalmente
        
        vicario_progress += effective_speed
        
        log.append(f"⚔️  MIN {minute}: Gemelos al {vicario_progress:.1f}% del objetivo")
        
        if vicario_progress >= 100:
            log.append(f"💀 MIN {minute}: GEMELOS EJECUTAN EL ALGORITMO DE VENGANZA")
            return False, time_alerted, minute, log
    
    log.append(f"⏱️ TIMEOUT: Simulación terminada sin resolución")
    return False, time_alerted, max_minutes, log

def run_monte_carlo(alpha, beta, gamma_inv, n_sims):
    """Ejecuta múltiples simulaciones y agrega resultados"""
    successes = 0
    failure_causes = defaultdict(int)
    alert_times = []
    attack_times = []
    
    for _ in range(n_sims):
        success, t_alert, t_attack, log = simulate_single_run(alpha, beta, gamma_inv)
        
        if success:
            successes += 1
            alert_times.append(t_alert)
        else:
            attack_times.append(t_attack)
            
            # Clasificar causa de fallo
            if "estancado" in " ".join(log):
                failure_causes["Fragmentación de red"] += 1
            elif t_attack <= 8:
                failure_causes["Propagación demasiado lenta"] += 1
            else:
                failure_causes["Ruido/Interferencia"] += 1
    
    return {
        "success_rate": (successes / n_sims) * 100,
        "successes": successes,
        "failures": n_sims - successes,
        "avg_alert_time": np.mean(alert_times) if alert_times else None,
        "avg_attack_time": np.mean(attack_times) if attack_times else None,
        "failure_causes": dict(failure_causes)
    }

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

if st.button("🚀 EJECUTAR SIMULACIÓN MONTE CARLO", use_container_width=True, type="primary"):
    # Progress bar moderno
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    status_text.text("🔄 Inicializando simulación...")
    progress_bar.progress(10)
    
    # Ejecutar Monte Carlo
    results = run_monte_carlo(critical_thinking, adaptability, problem_solving, num_simulations)
    
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
    col1, col2, col3 = st.columns(3)
    
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
            
            st.dataframe(failure_df, use_container_width=True, hide_index=True)
            
            st.info("""
**💡 Interpretación:**

• **Fragmentación de red:** El mensaje no encuentra rutas para propagarse → ↑ Adaptabilidad  
• **Saturación de información:** Demasiado "ruido" impide procesar datos críticos → ↑ Resolución de Problemas  
• **Baja transmisión:** Las personas ignoran o no comparten la advertencia → ↑ Pensamiento Crítico  
• **Propagación lenta:** El mensaje avanza pero no lo suficientemente rápido → ↑ Pensamiento Crítico  
• **Ruido/Interferencia:** El mensaje se pierde en el caos social → ↑ Resolución de Problemas
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
        
        st.dataframe(comparison_df, use_container_width=True, hide_index=True)
        
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
    
    **Fórmula que calcula si un mensaje se transmite:**
    
    $$P_{transmisión} = \\frac{Pensamiento\\:Crítico \\times (1 + Adaptabilidad)}{1 + Ruido}$$
    
    **Traducción a español simple:**
    - Si la gente tiene **pensamiento crítico alto**, creen el mensaje
    - Si hay **adaptabilidad alta**, hay más rutas para transmitir
    - Si hay **ruido alto** (mucha distracción), la probabilidad baja
    
    **Ejemplo con números reales del libro:**
    - Pensamiento Crítico = 0.2 (muy bajo)
    - Adaptabilidad = 0.3 (baja)
    - Ruido = 0.9 (muy alto porque γ⁻¹ = 0.1)
    
    Probabilidad = (0.2 × 1.3) / (1 + 0.9) = 0.26 / 1.9 ≈ **13.7%**
    
    Por eso Santiago muere en ~85% de los casos con esos valores.
    
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
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9em;'>
    <p>🛡️ <b>Operación Crónica</b> - Simulación educativa basada en "Crónica de una muerte anunciada" de Gabriel García Márquez</p>
    <p><b>Presentado por:</b> Dr. Germán Gómez Vargas, Universidad del Desarrollo (Chile)</p>
    <p><b>Para:</b> Estudiantes de la Corporación Universitaria San José de Sucre, Sincelejo, Colombia</p>
    <p>Visita Académica UAJS 2025 | 📚 Uso académico | 🔓 Código abierto</p>
</div>
""", unsafe_allow_html=True)
