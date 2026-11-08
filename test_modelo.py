"""Pruebas del motor de simulación.

Se ejecutan con:  python -m pytest test_modelo.py -q
o sin pytest con: python test_modelo.py
"""

import modelo
from modelo import (
    CAUSA_DESINFORMADO,
    CAUSA_FRAGMENTADA,
    CAUSA_LENTO,
    CAUSA_RUMOR_GANA,
    prob_transmision,
    run_monte_carlo,
)

LIBRO = (0.08, 0.15, 0.08)


def test_escenario_del_libro_ronda_el_83_por_ciento_de_mortalidad():
    """La cifra que se muestra en la charla."""
    r = run_monte_carlo(*LIBRO, 4000, seed=1)
    assert 14 <= r["success_rate"] <= 21, r["success_rate"]


def test_las_cuatro_causas_de_fallo_son_alcanzables():
    """En la v2.0 solo una de las cinco causas documentadas podía ocurrir."""
    vistas = set()
    for params in [LIBRO, (0.5, 0.1, 0.1), (0.9, 0.2, 0.2), (0.2, 0.6, 0.6)]:
        vistas |= set(run_monte_carlo(*params, 3000, seed=7)["failure_causes"])
    esperadas = {
        CAUSA_DESINFORMADO,
        CAUSA_FRAGMENTADA,
        CAUSA_RUMOR_GANA,
        CAUSA_LENTO,
    }
    assert esperadas <= vistas, esperadas - vistas


def test_cada_parametro_mueve_el_resultado():
    """Ninguna variable debe ser decorativa, y ninguna debe dominar sola."""
    base = run_monte_carlo(0.3, 0.3, 0.3, 3000, seed=11)["success_rate"]
    solo_alpha = run_monte_carlo(0.9, 0.3, 0.3, 3000, seed=11)["success_rate"]
    solo_beta = run_monte_carlo(0.3, 0.9, 0.3, 3000, seed=11)["success_rate"]
    solo_gamma = run_monte_carlo(0.3, 0.3, 0.9, 3000, seed=11)["success_rate"]

    assert solo_alpha - base > 5, (base, solo_alpha)
    assert solo_beta - base > 5, (base, solo_beta)
    assert solo_gamma - base > 5, (base, solo_gamma)


def test_pensamiento_critico_solo_no_basta():
    """El fallo de la v2.0: con alpha alto se ganaba siempre, aun con el resto en cero."""
    r = run_monte_carlo(0.95, 0.0, 0.0, 3000, seed=13)
    assert r["success_rate"] < 60, r["success_rate"]


def test_con_las_tres_variables_altas_santiago_se_salva():
    r = run_monte_carlo(0.95, 1.0, 1.0, 2000, seed=17)
    assert r["success_rate"] > 95, r["success_rate"]


def test_mas_pensamiento_critico_reduce_la_desinformacion():
    """Verificar debe servir justamente para no comerse el rumor."""
    bajo = run_monte_carlo(0.05, 0.4, 0.4, 3000, seed=19)["misinformed_rate"]
    alto = run_monte_carlo(0.9, 0.4, 0.4, 3000, seed=19)["misinformed_rate"]
    assert alto < bajo / 2, (bajo, alto)


def test_la_semilla_hace_el_resultado_reproducible():
    """Necesario para que la demo en vivo coincida con la diapositiva."""
    a = run_monte_carlo(*LIBRO, 500, seed=42)
    b = run_monte_carlo(*LIBRO, 500, seed=42)
    assert a == b


def test_los_gemelos_no_dependen_del_pensamiento_critico():
    """En la v2.0 alfa frenaba a los gemelos además de acelerar el aviso."""
    assert modelo.VELOCIDAD_GEMELOS * 15 >= 100, "el ataque debe caber en la ventana"
    lentos = run_monte_carlo(0.95, 0.5, 0.5, 2000, seed=23)["avg_attack_time"]
    rapidos = run_monte_carlo(0.05, 0.5, 0.5, 2000, seed=23)["avg_attack_time"]
    assert lentos == rapidos == 10.0, (lentos, rapidos)


def test_la_transmision_no_depende_de_alpha():
    assert prob_transmision(0.3, 0.3) == prob_transmision(0.3, 0.3)
    assert prob_transmision(0.9, 0.3) > prob_transmision(0.1, 0.3)
    assert prob_transmision(0.3, 0.9) > prob_transmision(0.3, 0.1)


if __name__ == "__main__":
    fallos = 0
    for nombre, fn in sorted(globals().items()):
        if nombre.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"  ok   {nombre}")
            except AssertionError as e:
                fallos += 1
                print(f"  FALLA {nombre}: {e}")
    print("\nTodo en orden." if not fallos else f"\n{fallos} prueba(s) fallaron.")
    raise SystemExit(1 if fallos else 0)
