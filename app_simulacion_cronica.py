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

# Estilo cyberpunk/dark mode
st.markdown("""
<style>
    .main {
        background-color: #0d1117;
        color: #00FFFF;
    }
    .stButton>button {
        background-color: #FF0040;
        color: white;
        font-weight: bold;
        border: 2px solid #00FFFF;
    }
    .metric-box {
        background-color: #161b22;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #00FFFF;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ OPERACIÓN CRÓNICA: Hackeando la Fatalidad")

# Información del autor y contexto
st.markdown("""
<div style='background-color: #161b22; padding: 15px; border-radius: 10px; border-left: 3px solid #00FFFF; margin-bottom: 20px;'>
    <p style='color: #00FFFF; font-size: 0.9em; margin: 0;'>
    <b>Presentado por:</b> Dr. Germán Gómez Vargas, Universidad del Desarrollo (Chile)<br>
    <b>Para:</b> Estudiantes de la Corporación Universitaria San José de Sucre, Sincelejo, Colombia<br>
    <b>Contexto:</b> Visita Académica UAJS 2025
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='background-color: #161b22; padding: 20px; border-radius: 10px; border-left: 5px solid #FFD700;'>
    <h3 style='color: #FFD700;'>🎯 ¿DE QUÉ TRATA ESTA SIMULACIÓN?</h3>
    <p style='color: #00FFFF;'>
    En "Crónica de una muerte anunciada" de Gabriel García Márquez, <b>todo el pueblo sabía 
    que iban a matar a Santiago Nasar</b>, pero nadie logró avisarle a tiempo. La tragedia 
    parecía "inevitable", pero... <b>¿realmente lo era?</b>
    </p>
    <p style='color: #00FF00;'>
    <b>TU MISIÓN:</b> Modificar las características del sistema social (pensamiento crítico, 
    adaptabilidad, capacidad de filtrar información) para que la advertencia llegue a Santiago 
    antes que los gemelos Vicario lo ataquen.
    </p>
    <p style='color: #FF0040;'>
    <b>LA LECCIÓN:</b> Lo que parecía "destino" era en realidad un <b>fallo del sistema social</b>. 
    Con las habilidades correctas, el resultado puede cambiar radicalmente.
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# CONTROLES DE SIMULACIÓN (SIDEBAR)
# ============================================================================

st.sidebar.header("⚙️ CONTROLES DE LA SIMULACIÓN")
st.sidebar.markdown("---")

st.sidebar.markdown("### 🧠 PENSAMIENTO CRÍTICO")
st.sidebar.markdown("""
<div style='font-size: 0.85em; color: #00FFFF;'>
¿Qué tan en serio toma la gente la información que recibe?<br>
<b>Ejemplo del libro:</b> Muchos escucharon el rumor pero lo descartaron como 
"habladas de borracho". <b>Bajo pensamiento crítico = ignorar señales importantes.</b>
</div>
""", unsafe_allow_html=True)
critical_thinking = st.sidebar.slider(
    "Nivel de Pensamiento Crítico", 
    min_value=0.0, max_value=1.0, value=0.08, step=0.05,
    help="0.0 = Nadie toma en serio la información | 1.0 = Todos evalúan y actúan"
)
st.sidebar.markdown(f"<div style='font-size: 0.8em; color: #FFD700;'>Valor actual: {critical_thinking:.2f} {'(Libro: 0.08)' if critical_thinking == 0.08 else ''}</div>", unsafe_allow_html=True)

st.sidebar.markdown("---")

st.sidebar.markdown("### 🌐 ADAPTABILIDAD")
st.sidebar.markdown("""
<div style='font-size: 0.85em; color: #00FFFF;'>
¿Puede la comunidad encontrar rutas alternativas cuando una falla?<br>
<b>Ejemplo del libro:</b> Si el Padre Amador olvida avisar, ¿hay otra persona que pueda hacerlo? 
<b>Alta adaptabilidad = múltiples caminos de comunicación.</b>
</div>
""", unsafe_allow_html=True)
adaptability = st.sidebar.slider(
    "Nivel de Adaptabilidad", 
    min_value=0.0, max_value=1.0, value=0.15, step=0.05,
    help="0.0 = Una sola ruta de información | 1.0 = Muchas rutas alternativas"
)
st.sidebar.markdown(f"<div style='font-size: 0.8em; color: #FFD700;'>Valor actual: {adaptability:.2f} {'(Libro: 0.15)' if adaptability == 0.15 else ''}</div>", unsafe_allow_html=True)

st.sidebar.markdown("---")

st.sidebar.markdown("### 📢 RESOLUCIÓN DE PROBLEMAS")
st.sidebar.markdown("""
<div style='font-size: 0.85em; color: #00FFFF;'>
¿Qué tan bien filtra la comunidad el ruido para enfocarse en lo importante?<br>
<b>Ejemplo del libro:</b> La llegada del Obispo distrajo a todo el pueblo. El puerto estaba 
lleno de actividad. <b>Baja resolución = información crítica se pierde en el caos.</b>
</div>
""", unsafe_allow_html=True)
problem_solving = st.sidebar.slider(
    "Capacidad de Filtrar Ruido", 
    min_value=0.0, max_value=1.0, value=0.08, step=0.05,
    help="0.0 = Caos total, información se pierde | 1.0 = Enfoque perfecto en lo crítico"
)
st.sidebar.markdown(f"<div style='font-size: 0.8em; color: #FFD700;'>Valor actual: {problem_solving:.2f} {'(Libro: 0.08)' if problem_solving == 0.08 else ''}</div>", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎲 CONFIGURACIÓN AVANZADA")

st.sidebar.markdown("""
<div style='font-size: 0.85em; color: #00FFFF; margin-bottom: 10px;'>
<b>¿Qué es "Monte Carlo"?</b><br>
Es ejecutar la simulación muchas veces (como tirar dados repetidamente) para obtener 
un <b>promedio estadístico</b>. Más simulaciones = resultado más confiable.
</div>
""", unsafe_allow_html=True)

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
    
    # Layout
    pos = nx.spring_layout(G, k=1.5, iterations=50, seed=42)
    
    # Colores por tipo de nodo
    node_colors = []
    for node in G.nodes():
        if node == "SANTIAGO NASAR":
            node_colors.append('#FFD700')  # Gold para objetivo
        elif "Gemelos" in node:
            node_colors.append('#FF0040')  # Rojo para amenaza
        elif any(key in node for key in ["Policía", "Coronel", "Padre"]):
            node_colors.append('#00D9FF')  # Cyan para autoridades
        else:
            node_colors.append('#00FFFF')  # Cyan claro para civiles
    
    # Dibujar
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                          node_size=2000, alpha=0.9, ax=ax)
    nx.draw_networkx_edges(G, pos, edge_color='#30363d', 
                          width=2, alpha=0.6, ax=ax)
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
        Patch(facecolor='#00D9FF', label='Autoridades'),
        Patch(facecolor='#00FFFF', label='Civiles')
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

if st.button("🚀 EJECUTAR SIMULACIÓN MONTE CARLO", use_container_width=True):
    with st.spinner("Ejecutando simulaciones... Esto puede tomar unos segundos..."):
        
        # Ejecutar Monte Carlo
        results = run_monte_carlo(critical_thinking, adaptability, problem_solving, num_simulations)
        
        # ========== RESULTADOS PRINCIPALES ==========
        st.markdown("---")
        st.header("📊 RESULTADOS DE LA SIMULACIÓN")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            success_rate = results["success_rate"]
            delta_color = "normal" if success_rate > 50 else "inverse"
            st.metric(
                "TASA DE ÉXITO", 
                f"{success_rate:.1f}%",
                delta=f"{results['successes']}/{num_simulations} simulaciones",
                delta_color=delta_color
            )
        
        with col2:
            if results["avg_alert_time"]:
                st.metric(
                    "TIEMPO PROMEDIO DE ALERTA",
                    f"{results['avg_alert_time']:.1f} min",
                    delta="Tiempo hasta que Santiago recibe aviso"
                )
            else:
                st.metric("TIEMPO PROMEDIO DE ALERTA", "N/A", delta="Sin alertas exitosas")
        
        with col3:
            if results["avg_attack_time"]:
                st.metric(
                    "TIEMPO PROMEDIO DE ATAQUE",
                    f"{results['avg_attack_time']:.1f} min",
                    delta="Cuando los gemelos ejecutan"
                )
            else:
                st.metric("TIEMPO PROMEDIO DE ATAQUE", "N/A", delta="Sin ataques")
        
        # ========== VEREDICTO ==========
        st.markdown("---")
        
        if success_rate >= 80:
            st.success("🎉 **ÉXITO SISTÉMICO**: Santiago se salva en la mayoría de los escenarios. La arquitectura de red es resiliente.")
            st.balloons()
        elif success_rate >= 50:
            st.warning("⚠️ **ÉXITO PARCIAL**: Santiago tiene 50/50 de posibilidades. El sistema es inestable.")
        elif success_rate >= 20:
            st.error("❌ **FALLO PROBABLE**: Santiago muere en la mayoría de los casos. Ajusta los parámetros.")
        else:
            st.error("💀 **FALLO SISTÉMICO TOTAL**: Replicaste las condiciones del libro. El destino está programado.")
        
        # ========== ANÁLISIS DE FALLOS ==========
        if results["failure_causes"]:
            st.markdown("---")
            st.subheader("🔍 ANÁLISIS DE CAUSAS DE FALLO")
            
            failure_df = pd.DataFrame([
                {"Causa": causa, "Frecuencia": freq}
                for causa, freq in results["failure_causes"].items()
            ]).sort_values("Frecuencia", ascending=False)
            
            st.dataframe(failure_df, use_container_width=True)
            
            st.markdown("""
            **Interpretación:**
            - **Fragmentación de red**: El mensaje no encuentra rutas para propagarse (↑ Adaptabilidad)
            - **Propagación demasiado lenta**: El mensaje avanza pero no lo suficientemente rápido (↑ Pensamiento Crítico)
            - **Ruido/Interferencia**: El mensaje se pierde en el caos social (↑ Resolución de Problemas)
            """)
        
        # ========== VISUALIZACIÓN DE RED ==========
        if show_network:
            st.markdown("---")
            st.subheader("🌐 LA RED SOCIAL DEL PUEBLO")
            
            # Explicación pedagógica
            st.markdown("""
            <div style='background-color: #161b22; padding: 15px; border-radius: 10px; margin-bottom: 20px;'>
                <h4 style='color: #FFD700; margin-top: 0;'>📚 ¿Qué es una Red Social?</h4>
                <p style='color: #00FFFF; font-size: 0.95em;'>
                Imagina que cada persona del pueblo es un <b>punto (nodo)</b> y las relaciones 
                entre ellos son <b>líneas (aristas)</b>. Por ejemplo, si Clotilde le habla a 
                Cristo Bedoya, hay una línea conectándolos.
                </p>
                <p style='color: #00FFFF; font-size: 0.95em;'>
                <b>🔵 Nodos (Círculos):</b> Cada personaje del libro<br>
                <b>━━ Aristas (Líneas):</b> Quién puede comunicarse con quién<br>
                <b>📊 Densidad:</b> Qué tan conectado está el pueblo (0.0 = aislado, 1.0 = todos conectados)
                </p>
                <p style='color: #00FF00; font-size: 0.95em;'>
                <b>En esta simulación:</b> El mensaje (advertencia sobre el ataque) intenta 
                "viajar" por estas líneas desde quien lo sabe (Clotilde) hasta Santiago. 
                Mientras más conexiones haya, más fácil es que llegue.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            sample_network = create_network(adaptability)
            fig = visualize_network(sample_network)
            st.pyplot(fig)
            
            # Métricas de red con explicaciones
            st.markdown("**📊 Estadísticas de la Red:**")
            metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
            
            with metrics_col1:
                st.metric("Nodos (Personajes)", len(sample_network.nodes()))
                st.caption("Cantidad de personas en la red")
            with metrics_col2:
                st.metric("Aristas (Conexiones)", len(sample_network.edges()))
                st.caption("Cantidad de relaciones activas")
            with metrics_col3:
                density = nx.density(sample_network)
                st.metric("Densidad", f"{density:.3f}")
                st.caption("0.0 = Aislado | 1.0 = Todos conectados")
            
            st.markdown("""
            <div style='background-color: #0d1117; padding: 10px; border-radius: 5px; border-left: 3px solid #00FFFF; margin-top: 10px;'>
                <p style='color: #00FFFF; font-size: 0.85em; margin: 0;'>
                💡 <b>Observa:</b> Si aumentas la <b>Adaptabilidad</b> (slider de la izquierda) 
                y vuelves a ejecutar, verás más líneas conectando personajes. Esto representa 
                que el pueblo tiene más "canales de comunicación" activos.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # ========== COMPARACIÓN CON LIBRO ==========
        st.markdown("---")
        st.subheader("📖 COMPARACIÓN CON EL LIBRO ORIGINAL")
        
        st.markdown("""
        <div style='background-color: #161b22; padding: 15px; border-radius: 10px; margin-bottom: 15px;'>
            <p style='color: #00FFFF; font-size: 0.9em; margin: 0;'>
            <b>¿Por qué los resultados varían si uso los mismos parámetros del libro?</b><br>
            Porque esta es una simulación <b>probabilística</b> (como el clima o el tráfico). 
            Cada vez que ejecutas, el mensaje toma rutas ligeramente diferentes. Lo importante 
            es el <b>promedio</b> de muchas simulaciones, no una sola corrida.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Valores históricos (calibrados para reflejar la tragedia del libro)
        historical_results = run_monte_carlo(0.08, 0.15, 0.08, 100)
        
        comparison_df = pd.DataFrame({
            "Escenario": ["Tu Simulación", "Libro Original (Valores Históricos)"],
            "Tasa de Éxito": [f"{results['success_rate']:.1f}%", f"{historical_results['success_rate']:.1f}%"],
            "Pensamiento Crítico": [f"{critical_thinking:.2f}", "0.08"],
            "Adaptabilidad": [f"{adaptability:.2f}", "0.15"],
            "Resolución de Problemas": [f"{problem_solving:.2f}", "0.08"]
        })
        
        st.dataframe(comparison_df, use_container_width=True)
        
        improvement = results['success_rate'] - historical_results['success_rate']
        
        st.markdown("""
        <div style='background-color: #0d1117; padding: 10px; border-radius: 5px; border-left: 3px solid #FFD700; margin-top: 15px;'>
            <p style='color: #FFD700; font-size: 0.9em; margin: 0;'>
            <b>💡 Interpretación:</b> El libro tenía pensamiento crítico bajo (0.2), poca 
            adaptabilidad (0.3) y mucho ruido (0.1). Con estos valores, Santiago se salva 
            solo en ~{:.0f}% de los casos. <b>La tragedia no era destino, era estadística.</b>
            </p>
        </div>
        """.format(historical_results['success_rate']), unsafe_allow_html=True)
        
        if improvement > 10:
            st.success(f"🎉 **¡Lograste mejorar +{improvement:.1f}%!** Cambiaste el destino de Santiago.")
        elif improvement > 0:
            st.info(f"✅ **Mejora moderada de +{improvement:.1f}%**. Vas por buen camino.")
        elif improvement < -10:
            st.error(f"❌ **Empeoraste {abs(improvement):.1f}%**. Estos parámetros hacen la situación peor.")
        else:
            st.warning("➡️ Resultados similares al libro. Prueba cambiar más los parámetros.")

# ============================================================================
# SECCIÓN EDUCATIVA
# ============================================================================

st.markdown("---")
st.header("🎓 LECCIONES PARA TODAS LAS CARRERAS")

st.markdown("""
<div style='background-color: #161b22; padding: 15px; border-radius: 10px; margin-bottom: 15px;'>
    <p style='color: #00FFFF; font-size: 0.95em;'>
    <b>Esta simulación es relevante para CUALQUIER carrera:</b> Derecho, Administración, 
    Trabajo Social, Ingeniería, Salud, Comunicación Social, etc. Todos trabajamos con 
    <b>información</b>, <b>redes de personas</b> y <b>toma de decisiones</b>.
    </p>
</div>
""", unsafe_allow_html=True)

with st.expander("💡 ¿Qué aprendemos de esta simulación?"):
    st.markdown("""
    ### 1. **El Pensamiento Crítico Salva Vidas (Literalmente)**
    
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
    
    **Lección:** Un sistema (o persona) sin pensamiento crítico **no diferencia lo importante de lo trivial**. En la simulación, subir este parámetro aumenta dramáticamente la probabilidad de éxito.
    
    ---
    
    ### 2. **Adaptabilidad = Tener un Plan B (y C, y D)**
    
    **En el libro:** La información siguió rutas rígidas:
    - Clotilde → Padre Amador → Madre de Santiago → ❌ (no avisó)
    - Cristo Bedoya → Buscó a Santiago → ❌ (no lo encontró)
    
    Si hubiera existido una ruta directa Clotilde → Santiago, la historia cambiaría.
    
    **Aplicaciones en tu carrera:**
    
    - **Derecho:** Si un testigo clave falla, ¿tienes evidencia alternativa?
    - **Administración:** Si un proveedor falla, ¿tienes respaldo?
    - **Salud:** Si un especialista no está disponible, ¿hay otro que pueda atender la emergencia?
    - **Trabajo Social:** Si un recurso comunitario cierra, ¿conoces alternativas?
    - **Ingeniería:** Si un servidor cae, ¿hay redundancia?
    
    **Lección:** Los sistemas resilientes tienen **múltiples caminos** para lograr el objetivo. No dependas de una sola ruta.
    
    ---
    
    ### 3. **Resolución de Problemas = Filtrar el Ruido**
    
    **En el libro:** Había demasiadas distracciones:
    - 🚢 La llegada del Obispo (todo el pueblo fue al puerto)
    - 🍺 La resaca después de la boda
    - 📢 El puerto lleno de ruido y actividad
    
    La información crítica ("van a matar a Santiago") se perdió en el caos.
    
    **Aplicaciones en tu carrera:**
    
    - **Derecho:** En un juicio con 500 páginas de evidencia, ¿identificas lo clave?
    - **Administración:** Con 50 emails al día, ¿priorizas lo urgente vs. lo importante?
    - **Salud:** En una emergencia con múltiples pacientes, ¿triage efectivo?
    - **Comunicación:** En redes sociales llenas de contenido, ¿qué merece atención?
    - **Psicología:** Con múltiples síntomas, ¿cuál es el diagnóstico principal?
    
    **Lección:** La capacidad de **enfocarse en lo crítico** y filtrar lo irrelevante es tan importante como tener la información. El ruido mata la señal.
    
    ---
    
    ### 4. **El "Destino" Era un Problema de Diseño**
    
    **La gran revelación:** García Márquez escribió sobre la inevitabilidad, pero esta 
    simulación demuestra que con las habilidades correctas, Santiago **podría haberse salvado**.
    
    **Esto aplica a problemas modernos reales:**
    
    - **Cambio climático:** ¿Es "inevitable" o es falta de acción colectiva?
    - **Pobreza:** ¿Es "destino" o son sistemas sociales mal diseñados?
    - **Corrupción:** ¿Es "inevitable" o es falta de transparencia y pensamiento crítico?
    - **Desinformación:** ¿Es "imposible de detener" o falta educación mediática?
    - **Desigualdad:** ¿Es "natural" o son políticas públicas deficientes?
    
    **Lección Final:** Lo que parece "destino inevitable" muchas veces es un **problema solucionable** si desarrollamos:
    
    1. ✅ **Pensamiento crítico** (evaluar información)
    2. ✅ **Adaptabilidad** (crear soluciones alternativas)
    3. ✅ **Resolución de problemas** (enfocarse en lo importante)
    
    ---
    
    ### 🚀 Desafíos para Practicar
    
    **Desafío 1 - Análisis Individual:**
    - Fija dos parámetros en 0.2 y varía el tercero de 0.2 a 0.8
    - ¿Cuál habilidad tiene mayor impacto individual?
    - ¿Qué implica esto para tu desarrollo profesional?
    
    **Desafío 2 - Optimización con Restricciones:**
    - Imagina que solo tienes 2.0 puntos para distribuir (ej: 0.7 + 0.7 + 0.6 = 2.0)
    - Encuentra la distribución que maximice la tasa de éxito
    - ¿Qué te dice esto sobre priorización de recursos limitados?
    
    **Desafío 3 - Pensamiento Crítico Aplicado:**
    - Identifica un "destino inevitable" en tu comunidad (problema social recurrente)
    - ¿Cuál de las tres habilidades falta más?
    - ¿Qué cambio concreto podrías implementar?
    """)

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
