"""
Motor de simulación de "Operación Crónica" (v3.0).

Qué cambió respecto de la v2.0
------------------------------
1. Por la red circulan DOS mensajes, no uno: el aviso verdadero ("van a matar
   a Santiago") y un rumor falso ("son habladas de borracho, ya le avisaron").
   En la v2.0 solo existía el aviso, así que "ser crítico" y "creer todo"
   producían exactamente el mismo resultado.

2. Alfa (pensamiento crítico) ya no amplifica la transmisión: ahora DISCRIMINA.
   Un nodo que verifica acepta el aviso y rechaza el rumor. Un nodo que no
   verifica se queda con lo primero que oyó, sea verdad o mentira.

3. Los gemelos avanzan a velocidad constante. En la v2.0 alfa los frenaba
   además de acelerar el aviso, así que alfa entraba dos veces en el modelo
   y lo dominaba: por encima de 0,67 los gemelos ya no alcanzaban a llegar
   dentro de la ventana de simulación y el plazo desaparecía.

4. Las causas de fallo se deducen del estado final de la red. En la v2.0
   cuatro de las cinco causas documentadas eran inalcanzables por construcción
   y el 100 % de los fallos se reportaba como "fragmentación de red".
"""

import random
from collections import defaultdict

import networkx as nx
import numpy as np

AVISO = "aviso"
RUMOR = "rumor"

SANTIAGO = "SANTIAGO NASAR"
CLOTILDE = "Clotilde Armenta"
GEMELOS = "Gemelos Vicario"

# Probabilidad base de que un mensaje salte de una persona a otra en un minuto.
# Calibrada para que los parámetros del libro den ~17 % de supervivencia, que
# es la cifra que se usa en la charla (83 % de mortalidad).
BASE_TX = 0.15

# Cuántas personas arrancan la mañana creyendo el rumor en vez del aviso.
SEMILLAS_RUMOR = 2

# Los gemelos tardan 10 minutos en consumar el ataque, siempre.
VELOCIDAD_GEMELOS = 10

CAUSA_DESINFORMADO = "Desinformación: Santiago creyó el rumor"
CAUSA_FRAGMENTADA = "Red fragmentada: el aviso no encontró ruta"
CAUSA_RUMOR_GANA = "El rumor desplazó al aviso"
CAUSA_LENTO = "Demasiado lento: el aviso venía en camino"


POLICIA = "Leandro Pornoy (Policía)"
CORONEL = "Coronel Lázaro Aponte"
PADRE = "Padre Carmen Amador"
CRISTO = "Cristo Bedoya"
PLACIDA = "Plácida Linero (Madre)"
VICTORIA = "Victoria Guzmán (Cocinera)"

PERSONAS = [GEMELOS, CLOTILDE, POLICIA, CORONEL, PADRE, CRISTO, PLACIDA, VICTORIA, SANTIAGO]

# Las rutas por las que, en la novela, podía viajar la advertencia.
RUTAS_LIBRO = [
    (GEMELOS, CLOTILDE),
    (CLOTILDE, POLICIA),
    (CLOTILDE, PADRE),
    (CLOTILDE, CRISTO),
    (POLICIA, CORONEL),
    (PADRE, PLACIDA),
    (CRISTO, SANTIAGO),
    (PLACIDA, SANTIAGO),
    (VICTORIA, SANTIAGO),
]

# Rutas que no existieron en la novela pero podrían haber existido. Cada una
# aparece con probabilidad beta (adaptabilidad).
RUTAS_ALTERNATIVAS = [
    (CLOTILDE, SANTIAGO),
    (POLICIA, CRISTO),
    (CORONEL, PLACIDA),
    (CORONEL, SANTIAGO),
    (PADRE, CRISTO),
    (VICTORIA, PLACIDA),
]


def create_network(beta, rng=random):
    """Construye el grafo social: rutas del libro + rutas alternativas."""
    G = nx.Graph()
    G.add_nodes_from(PERSONAS)
    G.add_edges_from(RUTAS_LIBRO)
    for edge in RUTAS_ALTERNATIVAS:
        if rng.random() < beta:
            G.add_edge(*edge)
    return G


def prob_transmision(beta, gamma_inv):
    """Probabilidad de que un mensaje salte de una persona a otra en un minuto.

    Depende de la adaptabilidad (más rutas, más oportunidades) y del ruido
    (gamma = 1 - gamma_inv). No depende del pensamiento crítico: ese decide
    QUÉ se cree, no cuán rápido circula.
    """
    gamma = 1 - gamma_inv
    return BASE_TX * (1 + beta) / (1 + gamma)


def _recibe(mensaje, alpha, rng):
    """Qué cree un nodo cuando le llega un mensaje.

    Con probabilidad alpha verifica: se queda con el aviso y descarta el rumor.
    Con probabilidad 1 - alpha no verifica: cree lo que le dijeron.
    Devuelve la nueva creencia, o None si descartó el mensaje.
    """
    if rng.random() < alpha:
        return AVISO if mensaje == AVISO else None
    return mensaje


def simulate_single_run(alpha, beta, gamma_inv, max_minutes=15, rng=random):
    """Una corrida. Devuelve (exito, t_aviso, t_ataque, log, diagnostico)."""
    G = create_network(beta, rng)

    creencia = {n: None for n in G.nodes}
    creencia[CLOTILDE] = AVISO

    candidatos = [n for n in G.nodes if n not in (CLOTILDE, SANTIAGO, GEMELOS)]
    semillas = rng.sample(candidatos, k=min(SEMILLAS_RUMOR, len(candidatos)))
    for n in semillas:
        creencia[n] = RUMOR

    p_tx = prob_transmision(beta, gamma_inv)

    santiago_desinformado = False
    aviso_llego_a_vecino = False
    progreso = 0
    log = [
        f"🌅 MIN 0: {CLOTILDE} oye a los gemelos y cree la advertencia. "
        f"{' y '.join(semillas)} amanecen creyendo el rumor."
    ]

    for minute in range(1, max_minutes + 1):
        # ---------- Fase 1: propagación ----------
        nuevos = {}
        marca = len(log)
        for nodo, mensaje in creencia.items():
            if mensaje is None or nodo == GEMELOS:
                continue
            for vecino in G.neighbors(nodo):
                if vecino == GEMELOS or creencia.get(vecino) is not None:
                    continue
                if vecino in nuevos:
                    continue
                if rng.random() >= p_tx:
                    continue

                if vecino == SANTIAGO:
                    if mensaje == AVISO:
                        # Si ya lo tranquilizaron con el rumor, solo reacciona
                        # si esta vez verifica.
                        if santiago_desinformado and rng.random() >= alpha:
                            log.append(
                                f"🙉 MIN {minute}: Santiago desestima el aviso de {nodo}"
                            )
                            continue
                        log.append(f"✅ MIN {minute}: ¡SANTIAGO ALERTADO por {nodo}!")
                        final = {**creencia, **nuevos, SANTIAGO: AVISO}
                        return True, minute, minute, log, {
                            "causa": None,
                            "santiago_desinformado": santiago_desinformado,
                            "creencias": final,
                            "red": G,
                        }
                    else:
                        creido = _recibe(RUMOR, alpha, rng)
                        if creido == RUMOR:
                            santiago_desinformado = True
                            log.append(
                                f"🌀 MIN {minute}: Santiago oye el rumor de {nodo} y se queda tranquilo"
                            )
                    continue

                creido = _recibe(mensaje, alpha, rng)
                if creido is None:
                    log.append(f"🔎 MIN {minute}: {vecino} verifica y descarta el rumor")
                    continue
                nuevos[vecino] = creido
                if creido == AVISO:
                    log.append(f"📢 MIN {minute}: {vecino} cree la advertencia (se la dijo {nodo})")
                else:
                    log.append(f"🌀 MIN {minute}: {vecino} cree el rumor (se lo dijo {nodo})")
                if creido == AVISO and SANTIAGO in G.neighbors(vecino):
                    aviso_llego_a_vecino = True

        creencia.update(nuevos)

        if len(log) == marca:
            log.append(f"🚫 MIN {minute}: nadie nuevo se entera")

        # ---------- Fase 2: avance de los gemelos ----------
        progreso += VELOCIDAD_GEMELOS
        log.append(f"⚔️ MIN {minute}: gemelos al {progreso:.0f} % del objetivo")

        if progreso >= 100:
            log.append(f"💀 MIN {minute}: los gemelos consuman la venganza")
            return False, -1, minute, log, _diagnostico(
                creencia, santiago_desinformado, aviso_llego_a_vecino, G
            )

    log.append("⏱️ Fin de la ventana de simulación")
    return False, -1, max_minutes, log, _diagnostico(
        creencia, santiago_desinformado, aviso_llego_a_vecino, G
    )


def _diagnostico(creencia, santiago_desinformado, aviso_llego_a_vecino, red=None):
    """Deduce por qué falló, a partir del estado final de la red."""
    con_aviso = sum(1 for v in creencia.values() if v == AVISO)
    con_rumor = sum(1 for v in creencia.values() if v == RUMOR)

    if santiago_desinformado:
        causa = CAUSA_DESINFORMADO
    elif not aviso_llego_a_vecino:
        causa = CAUSA_RUMOR_GANA if con_rumor > con_aviso else CAUSA_FRAGMENTADA
    else:
        causa = CAUSA_LENTO

    return {
        "causa": causa,
        "santiago_desinformado": santiago_desinformado,
        "con_aviso": con_aviso,
        "con_rumor": con_rumor,
        "creencias": dict(creencia),
        "red": red,
    }


def run_monte_carlo(alpha, beta, gamma_inv, n_sims, seed=None):
    """Corre n_sims simulaciones y agrega los resultados.

    Si se pasa `seed`, el resultado es reproducible: útil para que la demo en
    vivo dé el mismo número que la diapositiva.
    """
    rng = random.Random(seed) if seed is not None else random

    successes = 0
    desinformados = 0
    failure_causes = defaultdict(int)
    alert_times = []
    attack_times = []
    mananas = []  # cómo terminó cada corrida, en orden: "salvado", "rumor" o "sin_aviso"

    for _ in range(n_sims):
        ok, t_alert, t_attack, _log, diag = simulate_single_run(
            alpha, beta, gamma_inv, rng=rng
        )
        if ok:
            successes += 1
            alert_times.append(t_alert)
            mananas.append("salvado")
        else:
            attack_times.append(t_attack)
            failure_causes[diag["causa"]] += 1
            if diag["causa"] in (CAUSA_DESINFORMADO, CAUSA_RUMOR_GANA):
                mananas.append("rumor")
            else:
                mananas.append("sin_aviso")
        if diag["santiago_desinformado"]:
            desinformados += 1

    return {
        "success_rate": (successes / n_sims) * 100,
        "successes": successes,
        "failures": n_sims - successes,
        "misinformed_rate": (desinformados / n_sims) * 100,
        "avg_alert_time": float(np.mean(alert_times)) if alert_times else None,
        "avg_attack_time": float(np.mean(attack_times)) if attack_times else None,
        "failure_causes": dict(failure_causes),
        "mananas": mananas,
    }


def una_manana(alpha, beta, gamma_inv, numero, seed):
    """Reproduce la mañana número `numero` (desde 1) de run_monte_carlo(seed=seed).

    Consume el generador aleatorio exactamente igual que run_monte_carlo, así
    que la mañana que se muestra en detalle es la misma que se contó en el total.
    """
    rng = random.Random(seed)
    resultado = None
    for _ in range(numero):
        resultado = simulate_single_run(alpha, beta, gamma_inv, rng=rng)
    return resultado
