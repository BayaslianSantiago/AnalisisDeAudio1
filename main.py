import numpy as np
import sounddevice as sd # ¡Cambiamos a sounddevice!
from scipy.io import wavfile
import matplotlib.pyplot as plt
import os

# Nombre del archivo de audio
nombre_archivo = "AnalisisTextos.wav"

# 1. Cargar el archivo WAV
try:
    # Leer el archivo de audio
    samplerate, data = wavfile.read(nombre_archivo)
    print(f"Archivo '{nombre_archivo}' cargado exitosamente.")
except FileNotFoundError:
    print(f"Error: El archivo '{nombre_archivo}' no se encontró.")
    exit()
except Exception as e:
    print(f"Error al cargar el archivo: {e}")
    exit()

# Asegurarse de que los datos sean mono si son estéreo, o seleccionar un canal
if data.ndim > 1:
    data_mono = data[:, 0]  # Tomar el primer canal si es estéreo
else:
    data_mono = data

# Convertir los datos a float32 y normalizarlos a un rango de -1.0 a 1.0
# Esto es importante para sounddevice y evita problemas de clipping o volumen.
if data_mono.dtype != np.float32:
    max_abs_val = np.max(np.abs(data_mono))
    if max_abs_val == 0: # Evitar división por cero si el audio es silencioso
        data_processed = np.zeros_like(data_mono, dtype=np.float32)
    else:
        data_processed = data_mono.astype(np.float32) / max_abs_val
else:
    data_processed = data_mono # Si ya es float32, lo usamos directamente

# 2. Mostrar el Vector de la señal segmentada (mostramos una parte para no saturar la consola)
print("\n--- Vector de la señal (primeros 50 elementos): ---")
print(data_processed[:50])

# 3. Mostrar la cantidad de elementos de la muestra
num_muestras = len(data_processed)
print(f"\n--- Cantidad de elementos de la muestra: ---")
print(f"Número total de muestras: {num_muestras}")

# 4. Mostrar la Frecuencia de Muestreo
print(f"\n--- Frecuencia de Muestreo: ---")
print(f"Frecuencia de Muestreo (Hz): {samplerate}")

# 5. Mostrar la duración en segundos del audio
duracion_segundos = num_muestras / samplerate
print(f"\n--- Duración del audio: ---")
print(f"Duración en segundos: {duracion_segundos:.2f} s")

# 6. Imprimir la señal sonora (visualización gráfica)
print("\n--- Gráfico de la señal sonora: ---")
plt.figure(figsize=(12, 6))
tiempo = np.arange(0, duracion_segundos, 1/samplerate)
plt.plot(tiempo, data_processed)
plt.title('Señal Sonora Original')
plt.xlabel('Tiempo (segundos)')
plt.ylabel('Amplitud')
plt.grid(True)
plt.show()

# 7. Reproducir la señal original
print("\n--- Reproduciendo la señal original... ---")
try:
    sd.play(data_processed, samplerate)
    sd.wait() # Espera a que la reproducción termine
    print("Reproducción original finalizada.")
except Exception as e:
    print(f"Error al reproducir el audio original: {e}")


# 8. Modificar la frecuencia de muestreo para que dure más y menos tiempo
print("\n--- Modificando la frecuencia de muestreo... ---")

# Para que dure más tiempo (reduciendo la velocidad de reproducción)
new_samplerate_slow = samplerate // 2 # Reducimos a la mitad la frecuencia de muestreo
print(f"\nReproduciendo a una frecuencia de muestreo menor ({new_samplerate_slow} Hz) - Durará el doble:")
try:
    sd.play(data_processed, new_samplerate_slow)
    sd.wait()
    print("Reproducción a menor velocidad finalizada.")
except Exception as e:
    print(f"Error al reproducir a menor velocidad: {e}")

# Para que dure menos tiempo (aumentando la velocidad de reproducción)
new_samplerate_fast = samplerate * 2 # Duplicamos la frecuencia de muestreo
print(f"\nReproduciendo a una frecuencia de muestreo mayor ({new_samplerate_fast} Hz) - Durará la mitad:")
try:
    sd.play(data_processed, new_samplerate_fast)
    sd.wait()
    print("Reproducción a mayor velocidad finalizada.")
except Exception as e:
    print(f"Error al reproducir a mayor velocidad: {e}")


print("\n--- Explicación sobre la modificación de la frecuencia de muestreo: ---")
print("Cuando modificamos la frecuencia de muestreo sin cambiar la cantidad de muestras, estamos alterando la velocidad a la que se 'leen' esas muestras.")
print("- Si disminuimos la **frecuencia de muestreo** (e.g., de 44100 Hz a 22050 Hz), estamos indicando al reproductor que debe tomar menos muestras por segundo. Esto hace que el mismo número de muestras (que representan la duración original del audio) se distribuyan en un período de tiempo más largo, resultando en un audio que dura más y suena más **grave** (efecto 'slow motion' o 'pitch shift' hacia abajo).")
print("- Si aumentamos la **frecuencia de muestreo** (e.g., de 44100 Hz a 88200 Hz), estamos indicando al reproductor que debe tomar más muestras por segundo. Esto hace que el mismo número de muestras se 'consuma' en un período de tiempo más corto, resultando en un audio que dura menos y suena más **agudo** (efecto 'fast forward' o 'pitch shift' hacia arriba).")


# 9. Bajar la calidad del audio y reproducir la señal
print("\n--- Bajando la calidad del audio (downsampling y cuantificación)... ---")

# Proceso para bajar la calidad:
# a) Downsampling (Reducir la frecuencia de muestreo): Disminuye la cantidad de información temporal.
# b) Cuantificación (Reducir la profundidad de bits): Disminuye la precisión de las amplitudes.

# Definimos una nueva frecuencia de muestreo más baja (ej. la mitad)
new_samplerate_low_quality = samplerate // 2
# Definimos una nueva profundidad de bits (ej. simular 8 bits)

# 1. Downsampling: Resamplear la señal
# Tomamos una de cada 'factor' muestras.
downsample_factor = samplerate // new_samplerate_low_quality
data_downsampled = data_processed[::downsample_factor]

# Ajustar la nueva frecuencia de muestreo para la reproducción
actual_new_samplerate = samplerate / downsample_factor

print(f"Frecuencia de muestreo original: {samplerate} Hz")
print(f"Frecuencia de muestreo para baja calidad: {actual_new_samplerate:.0f} Hz (aproximado)")

# 2. Cuantificación: Reducir la profundidad de bits (simulación a 8 bits)
# Los datos ya están normalizados a -1.0 a 1.0.
# Para simular 8 bits, los mapeamos a un rango de 0-255, los redondeamos y luego los re-mapeamos a -1.0 a 1.0
# Esto introduce la pérdida de precisión.
data_8bit_simulated = np.round((data_downsampled + 1) * 127.5) # Rango 0-255
data_quantized_for_playback = (data_8bit_simulated / 127.5) - 1 # Re-mapear a -1.0 a 1.0

print("\n--- Reproduciendo la señal con baja calidad... ---")
try:
    sd.play(data_quantized_for_playback, int(actual_new_samplerate))
    sd.wait()
    print("Reproducción de baja calidad finalizada.")
except Exception as e:
    print(f"Error al reproducir audio de baja calidad: {e}")

print("\n--- Explicación del proceso de bajar la calidad del audio: ---")
print("El proceso de bajar la calidad de un audio generalmente implica dos técnicas principales:")
print("1. **Downsampling (Reducción de la Frecuencia de Muestreo):**")
print("   - Esto significa que se reduce el número de muestras tomadas por segundo para representar la onda sonora.")
print("   - Cuantas menos muestras haya, menos información se tiene sobre las variaciones rápidas de la señal (frecuencias altas).")
print("   - El efecto audible es una pérdida de detalle, especialmente en los agudos, y el sonido puede volverse más 'apagado' o 'borroso'. Puede introducir aliasing si no se aplica un filtro anti-aliasing adecuado antes del downsampling.")
print("   - En este código, lo simulamos tomando solo una fracción de las muestras originales.")
print("2. **Cuantificación (Reducción de la Profundidad de Bits):**")
print("   - Esto se refiere a la disminución del número de bits utilizados para representar la amplitud de cada muestra.")
print("   - Una menor profundidad de bits significa menos niveles de amplitud posibles, lo que reduce la precisión con la que se registran los valores de la señal.")
print("   - El efecto audible es un aumento del 'ruido de cuantificación' (un tipo de distorsión) que se percibe como un silbido o ruido de fondo, y el sonido puede volverse más 'áspero' o con menos rango dinámico. Se pierde la finura en las transiciones de volumen.")
print("   - En este código, lo simulamos escalando los datos para que se ajusten a un rango menor (como si fueran 8 bits) y luego re-escalándolos para la reproducción, introduciendo la pérdida de precisión.")
print("\nEn resumen, la combinación de downsampling y cuantificación reduce drásticamente la cantidad de datos necesarios para almacenar el audio, pero a costa de una pérdida perceptible de fidelidad y la introducción de artefactos de sonido.")