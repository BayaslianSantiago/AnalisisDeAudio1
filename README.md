# Análisis y Manipulación de Señales de Audio en Python

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![NumPy](https://img.shields.io/badge/NumPy-FF0080?logo=numpy&logoColor=white&labelColor=1a0c24)
![SciPy](https://img.shields.io/badge/SciPy-E60000?logo=scipy&logoColor=white&labelColor=2a0404)
![Matplotlib](https://img.shields.io/badge/Matplotlib-green.svg)
![Sounddevice](https://img.shields.io/badge/Sounddevice-50C878?logo=python&logoColor=white&labelColor=2a0404)

Este proyecto en Python te permite cargar, analizar y manipular archivos de audio en formato WAV. Es una herramienta práctica para entender los fundamentos del procesamiento de señales de audio, permitiéndote visualizar la señal sonora, obtener información clave sobre el audio y experimentar con la modificación de la frecuencia de muestreo y la calidad del sonido.

---

## Características Principales

* **Carga de archivos WAV:** Lee archivos de audio `.wav` para su posterior procesamiento.
* **Información Detallada de la Señal:** Muestra el vector de la señal, la cantidad de elementos de la muestra, la frecuencia de muestreo y la duración del audio en segundos.
* **Visualización Gráfica:** Genera un gráfico claro de la forma de onda de la señal sonora, ayudando a entender su estructura visualmente.
* **Reproducción de Audio:** Te permite reproducir la señal original directamente desde el script.
* **Modificación de la Velocidad de Reproducción:** Experimenta con el cambio de la frecuencia de muestreo para hacer que el audio dure más o menos tiempo. El script incluye explicaciones sobre cómo esto afecta la duración y el tono (pitch) del sonido.
* **Reducción de Calidad del Audio:** Demuestra cómo bajar la calidad del audio usando técnicas de *downsampling* (reducción de la frecuencia de muestreo) y *cuantificación* (reducción de la profundidad de bits), explicando el proceso y sus efectos audibles.

---

## Requisitos

Para ejecutar este proyecto, necesitas tener **Python 3.x** instalado. Además, las siguientes librerías de Python son esenciales:

* `numpy`
* `scipy`
* `matplotlib`
* `sounddevice`

Puedes instalarlas fácilmente usando `pip`:

pip install numpy scipy matplotlib sounddevice

Estructura del Código

El script sigue un flujo secuencial para demostrar cada funcionalidad:

Carga y normaliza el archivo WAV.
Muestra los detalles básicos de la señal.
Genera una visualización de la forma de onda.
Reproduce la señal original.
Experimenta con frecuencias de muestreo más bajas y más altas, reproduciendo el audio a diferentes velocidades.
Simula la reducción de calidad del audio aplicando downsampling y cuantificación, reproduciendo la versión degradada y explicando el proceso.
