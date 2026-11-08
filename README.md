# 🛡️ Operación Crónica: Hackeando la Fatalidad

Una simulación interactiva de Monte Carlo basada en "Crónica de una muerte anunciada" de Gabriel García Márquez, diseñada para enseñar **pensamiento crítico**, **adaptabilidad** y **resolución de problemas** a estudiantes de todas las carreras.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)

**Presentado por:** Dr. Germán Gómez Vargas, Instituto de Data Science, Universidad del Desarrollo (Chile)  
**Para:** Estudiantes universitarios de Colombia  
**Contexto:** la institución anfitriona se elige con un parámetro de URL, por ejemplo `?uni=americana` o `?uni=uajs`

## 🎯 ¿Para Quién es Esta Herramienta?

Esta aplicación es para **estudiantes de TODAS las carreras**: Derecho, Administración, Trabajo Social, Comunicación, Ingeniería, Salud, Psicología, y más. No requiere conocimientos técnicos previos.

Si te has preguntado alguna vez:
- ¿Por qué circulan tantas noticias falsas?
- ¿Cómo evitar que se repitan tragedias evitables?
- ¿Qué habilidades necesito para el mundo laboral?

**Esta simulación te dará respuestas prácticas.**

## 🎓 Objetivo Pedagógico

Esta aplicación demuestra que el "destino inevitable" de la novela de García Márquez era en realidad un **fallo de diseño del sistema social** que puede modelarse matemáticamente. 

**Lo que aprenderás:**

- **Pensamiento Crítico**: Por qué es vital evaluar información antes de descartarla
- **Adaptabilidad**: Por qué necesitas siempre un Plan B (y C, y D)
- **Resolución de Problemas**: Cómo filtrar lo importante del ruido
- **Pensamiento Sistémico**: Cómo pequeños cambios generan grandes diferencias

**Aplicable a cualquier carrera:**
- **Derecho**: Evaluación de pruebas, construcción de casos
- **Administración**: Toma de decisiones, gestión de riesgos
- **Salud**: Triage, diagnóstico diferencial
- **Comunicación**: Verificación de fuentes, combate a fake news
- **Trabajo Social**: Redes de apoyo comunitario
- **Ingeniería**: Sistemas resilientes, redundancia

## 🚀 Instalación Local

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos

1. **Clonar el repositorio:**
```bash
git clone https://github.com/gear-go/operacion-cronica.git
cd operacion-cronica
```

2. **Crear entorno virtual (recomendado):**
```bash
python -m venv venv

# En Windows:
venv\Scripts\activate

# En macOS/Linux:
source venv/bin/activate
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Ejecutar la aplicación:**
```bash
streamlit run app_simulacion_cronica.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 🌐 Despliegue en Streamlit Cloud (GitHub Pages alternativo)

Streamlit Cloud es la forma más sencilla de publicar esta app gratuitamente:

### Paso 1: Subir a GitHub

1. Crea un nuevo repositorio en GitHub
2. Sube estos archivos:
   - `app_simulacion_cronica.py`
   - `requirements.txt`
   - `README.md`

```bash
git init
git add .
git commit -m "Initial commit: Operación Crónica"
git branch -M main
git remote add origin https://github.com/gear-go/operacion-cronica.git
git push -u origin main
```

### Paso 2: Conectar con Streamlit Cloud

1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. Inicia sesión con tu cuenta de GitHub
3. Haz clic en "New app"
4. Selecciona tu repositorio
5. Configura:
   - **Branch:** `main`
   - **Main file path:** `app_simulacion_cronica.py`
6. Haz clic en "Deploy!"

**¡Listo!** Tu app estará disponible en una URL pública como:
```
https://USUARIO-REPO-HASH.streamlit.app
```

## 📊 Cómo Usar la Aplicación

### Controles Principales

1. **🧠 Pensamiento Crítico (α):**
   - Qué proporción de la gente **verifica antes de repetir**. Quien verifica se queda
     con la advertencia y descarta el rumor; quien no, cree lo primero que oyó.
   - No acelera la transmisión: decide **cuál de los dos mensajes** se cree.
   - Valor del libro: **0.08** (casi nadie verificó: "son habladas de borracho")

2. **🌐 Adaptabilidad (β):**
   - Cuántas rutas alternativas existen en la red
   - Valor del libro: **0.15** (pocas conexiones redundantes)

3. **📢 Filtrado de Ruido (γ⁻¹):**
   - Capacidad de la comunidad para enfocarse pese al ruido
   - Valor del libro: **0.08** (ruido extremo: el obispo, la resaca, el puerto)

### Experimentos Sugeridos

Cifras medidas con 4.000 simulaciones por escenario (`seed=99`).

**Experimento 1: replicar el libro**
- α = 0.08, β = 0.15, γ⁻¹ = 0.08
- Resultado: **~18 % de éxito**. Santiago muere en ~82 % de los casos, y en ~51 %
  le llega primero el rumor.

**Experimento 2: ¿basta el pensamiento crítico?**
- α = 0.80, β = 0.15, γ⁻¹ = 0.08
- Resultado: **~25 % de éxito**. Sube apenas siete puntos: verificar no sirve de
  nada si el mensaje no tiene por dónde llegar.

**Experimento 3: las tres variables altas**
- α = 0.80, β = 0.80, γ⁻¹ = 0.80
- Resultado: **~90 % de éxito**.

**Experimento 4: una red excelente sin verificación** ⭐
- α = 0.00, β = 0.80, γ⁻¹ = 0.80
- Resultado: **~43 % de éxito, pero ~57 % de desinformación**. Una red rápida y
  bien conectada propaga la mentira con la misma eficiencia que la verdad. Es el
  experimento más interesante para discutir en clase.

**Experimento 4: Un Solo Parámetro**
- Fija dos parámetros en 0.2, varía el tercero
- ¿Cuál tiene más impacto individual?

## 🧮 Modelo Matemático

### Probabilidad de Transmisión

$$P_{tx} = \frac{\alpha \times (1 + \beta)}{1 + \gamma}$$

Donde:
- **α**: Pensamiento crítico (credibilidad de la señal)
- **β**: Adaptabilidad (densidad de rutas alternativas)
- **γ**: Nivel de ruido, $\gamma = 1 - \gamma^{-1}$

### Velocidad de los Gemelos

$$V_{gemelos} = 10\% - (\alpha \times 5\%)$$

El pensamiento crítico genera intentos de intervención que ralentizan el ataque.

### Método Monte Carlo

1. Se generan N redes aleatorias (default: 100)
2. Cada red tiene rutas base + rutas adaptativas según β
3. Por cada minuto:
   - El mensaje intenta propagarse con probabilidad $P_{tx}$
   - Los gemelos avanzan según $V_{gemelos}$
4. Se registra si Santiago es alertado antes del ataque
5. La **tasa de éxito** es el % de simulaciones exitosas

## 📚 Contexto Literario

### "Crónica de una muerte anunciada" (1981)

**Sinopsis:** Santiago Nasar es asesinado por los gemelos Vicario para "limpiar el honor" de su hermana Ángela. Lo paradójico es que **todo el pueblo sabía que lo iban a matar**, pero nadie lo detuvo. García Márquez construye una narrativa de fatalidad inevitable.

### Personajes en la Red

- **Santiago Nasar**: El objetivo (¿será alertado?)
- **Gemelos Vicario**: La amenaza (avanzan hacia Santiago)
- **Clotilde Armenta**: Primera en saber, intenta avisar
- **Cristo Bedoya**: Amigo de Santiago, busca avisarle
- **Plácida Linero (Madre)**: Cierra la puerta creyendo que Santiago está dentro
- **Coronel Aponte**: Autoridad que desarma a los gemelos pero no los detiene
- **Padre Carmen Amador**: Olvida avisar por preparar la llegada del Obispo
- **Victoria Guzmán**: Cocinera que sabía pero no avisó

## 🎓 Aplicaciones Pedagógicas

### Para Cursos de:

- **Ciencias de Datos**: Modelado de redes sociales, Monte Carlo
- **Ingeniería de Software**: Sistemas distribuidos, SPOF, redundancia
- **IA/ML**: Sesgos algorítmicos, interpretabilidad de modelos
- **Humanidades Digitales**: Análisis computacional de literatura
- **Pensamiento Crítico**: Evaluación de información, toma de decisiones

### Preguntas de Discusión

1. ¿Qué representa cada parámetro en contextos modernos? (redes sociales, noticias falsas, alertas de seguridad)
2. ¿Cómo se relaciona esto con "filter bubbles" y "echo chambers"?
3. ¿Existen sistemas reales donde pequeños cambios en parámetros tengan consecuencias dramáticas?
4. ¿Es ético diseñar sistemas que dependen de alta "credibilidad" cuando pueden existir falsos positivos?

## 🔬 Extensiones Posibles

Ideas para estudiantes avanzados:

1. **Añadir más personajes**: Ampliar el grafo con personajes secundarios
2. **Costos de aristas**: Algunas rutas son más "costosas" (ej. hablar con el Coronel requiere más tiempo)
3. **Memoria de nodos**: Personajes que olvidan (como el Padre Amador) reducen $P_{tx}$ con el tiempo
4. **Análisis de sensibilidad**: ¿Qué parámetro es más "frágil"?
5. **Optimización automática**: Usar algoritmos genéticos para encontrar parámetros óptimos
6. **Red dinámica**: La estructura del grafo cambia durante la simulación (gente que sale del pueblo)

## 🤝 Contribuciones

¡Contribuciones son bienvenidas! Por favor:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🙏 Agradecimientos

- **Gabriel García Márquez**: Por la obra literaria que inspira esta simulación
- **NetworkX**: Por la biblioteca de análisis de grafos
- **Streamlit**: Por hacer tan fácil crear aplicaciones interactivas
- **Comunidad educativa**: Por fomentar el pensamiento crítico y la alfabetización digital

## 📧 Contacto

Para preguntas, sugerencias o colaboraciones:

- **Email**: gagomez@udd.cl
- **Twitter/X**: [@tu_usuario]
- **LinkedIn**: [tu-perfil]

---

<div align="center">
  <p><i>"El día en que lo iban a matar, Santiago Nasar se levantó a las 5:30 de la mañana..."</i></p>
  <p>— Gabriel García Márquez</p>
  <br>
  <p><b>¿Podrás cambiar el final de la historia?</b></p>
</div>

---

## 🔄 Cambios de la v3.0 (noviembre de 2026)

La v2.0 se auditó antes de reutilizarla en una charla nueva y tenía tres defectos
que vale la pena dejar escritos, porque son justamente los que la charla enseña
a detectar.

**1. El pensamiento crítico estaba decorado, no modelado.**
Por la red circulaba un solo mensaje y siempre era verdadero, así que "ser
crítico" y "creer todo" producían el mismo resultado. Ahora circulan dos
mensajes —la advertencia y un rumor falso— y α decide cuál se cree.

**2. α entraba dos veces en el modelo.**
Aceleraba la advertencia y además frenaba a los gemelos. Por encima de α = 0,67
los gemelos ya no alcanzaban a llegar dentro de la ventana de 15 minutos y el
plazo desaparecía: con α ≥ 0,6 Santiago se salvaba siempre, aunque la
adaptabilidad y el filtrado de ruido estuvieran en cero. Ahora los gemelos
avanzan a velocidad constante y el plazo son siempre 10 minutos.

**3. Cuatro de las cinco causas de fallo eran inalcanzables.**
La rama "propagación demasiado lenta" exigía un ataque antes del minuto 8, algo
imposible porque la velocidad máxima era de 10 % por minuto. El 100 % de los
fallos se reportaba como "fragmentación de red". Ahora son cuatro causas, todas
alcanzables, deducidas del estado final de la red.

**Además:** dependencias con versión fija, `use_container_width` reemplazado por
`width` (estaba deprecado), institución anfitriona configurable por parámetro de
URL, modo demo con semilla fija para que la cifra proyectada coincida con la
diapositiva, y una batería de pruebas en `test_modelo.py`.

```bash
python -m pytest test_modelo.py -q   # o: python test_modelo.py
```
