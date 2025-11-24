# 🛡️ Operación Crónica: Hackeando la Fatalidad

Una simulación interactiva de Monte Carlo basada en "Crónica de una muerte anunciada" de Gabriel García Márquez, diseñada para enseñar **pensamiento crítico**, **adaptabilidad** y **resolución de problemas** a estudiantes de todas las carreras.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)

**Presentado por:** Dr. Germán Gómez Salinas, Universidad del Desarrollo (Chile)  
**Para:** Estudiantes de la Corporación Universitaria San José de Sucre, Sincelejo, Colombia  
**Contexto:** Visita Académica UAJS 2025

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
git clone https://github.com/TU_USUARIO/operacion-cronica.git
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
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
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
   - Controla qué tan seriamente la gente evalúa la información
   - Valor del libro: 0.2 (muchos descartaron el rumor como "habladas")

2. **🌐 Adaptabilidad (β):**
   - Define cuántas rutas alternativas puede crear la red
   - Valor del libro: 0.3 (pocas conexiones redundantes)

3. **📢 Resolución de Problemas (γ⁻¹):**
   - Capacidad para filtrar ruido y priorizar información crítica
   - Valor del libro: 0.1 (ruido extremo: Obispo, resaca, puerto)

### Experimentos Sugeridos

**Experimento 1: Replicar el Libro**
- α = 0.2, β = 0.3, γ⁻¹ = 0.1
- Resultado esperado: ~10-20% de éxito (Santiago muere)

**Experimento 2: Pensamiento Crítico Solo**
- α = 0.8, β = 0.3, γ⁻¹ = 0.1
- ¿Es suficiente el pensamiento crítico para salvar a Santiago?

**Experimento 3: Optimización Completa**
- α = 0.8, β = 0.8, γ⁻¹ = 0.8
- Resultado esperado: >90% de éxito

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

- **Email**: [tu-email@ejemplo.com]
- **Twitter/X**: [@tu_usuario]
- **LinkedIn**: [tu-perfil]

---

<div align="center">
  <p><i>"El día en que lo iban a matar, Santiago Nasar se levantó a las 5:30 de la mañana..."</i></p>
  <p>— Gabriel García Márquez</p>
  <br>
  <p><b>¿Podrás cambiar el final de la historia?</b></p>
</div>
