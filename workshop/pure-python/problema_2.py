
# Carga de paquetes Python necesarios para hacer los requests a la API y graficar resultados
import matplotlib.cm
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import dateutil.parser
import yaml
import pandas as pd
import numpy as np
import statsmodels.api as sm

from funciones_api import consumir_servicio_JSON

with open('credencial.yml', 'r') as f:
    credencial = yaml.safe_load(f.read())

base_url = 'https://api.crc-sas.org/ws-api'
usuario_default = credencial.get('usuario')
clave_default = credencial.get('clave')

if __name__ == "__main__":
    matplotlib.use('TkAgg')

    # DESCRIPCIÓN DEL PROBLEMA:

    # Problema 2:
    # Buscar los valores de precipitación acumulada de 3 meses para los meses de enero a marzo de la estación Pehuajó.
    # Utilizar el período de referencia 1971-2010 para ajustar una distribución no paramétrica a dichos valores.

    # SOLUCIÓN DEL PROBLEMA:

    # Se buscan los valores de precipitación acumulada de enero a marzo para Pehuajó (87544)
    omm_id = 87544
    ancho_ventana = 18
    fecha_desde = dateutil.parser.parse("1971-01-01").isoformat()
    fecha_hasta = dateutil.parser.parse("2010-12-31").isoformat()
    url_estadisticas = f"{base_url}/estadisticas_moviles/{omm_id}/Suma/{ancho_ventana}/{fecha_desde}/{fecha_hasta}"

    estadisticas = consumir_servicio_JSON(url=url_estadisticas, usuario=usuario_default, clave=clave_default)
    estadisticas['fecha_desde'] = pd.to_datetime(estadisticas['fecha_desde'])
    estadisticas['fecha_hasta'] = pd.to_datetime(estadisticas['fecha_hasta'])
    estadisticas = estadisticas.query('fecha_hasta.dt.month == 3 and fecha_hasta.dt.day == 31')

    # Datos necesarios para el ajuste
    tamano_bin = 50  # Ancho de cada intervalo
    muestra_original = estadisticas['valor'].values

    # 1. Histograma de datos originales
    r_hist_counts, r_hist_breaks = np.histogram(muestra_original, bins=range(0, 900+1, tamano_bin))
    r_hist_mids = 0.5 * (r_hist_breaks[1:] + r_hist_breaks[:-1])

    # 2. Ajuste no paramétrico y cálculo de función de densidad
    kde = sm.nonparametric.KDEUnivariate(muestra_original)
    kde = kde.fit()  # Estimar densidades

    # Generar gráfico
    fig = plt.figure(figsize=(12, 5))
    ax = fig.add_subplot(111)

    # Graficar el histograma
    ax.hist(muestra_original, bins=range(0, 900 + 1, tamano_bin),
            zorder=5, color='tomato', edgecolor='k', alpha=0.5)
    ax.set_ylabel('Frecuencia')
    ax.set_xlabel('Precipitación acumulada')
    ax.grid(True, zorder=-5)
    ax.set_ylim(0, 7)

    # Graficar la función ajustada
    ay = ax.twinx()
    ay.plot(kde.support, kde.density, lw=3, zorder=10, color='black')
    ay.set_ylabel('Densidad de probabilidad')
    ay.set_ylim(0, 0.0035)

    # Leyenda
    emp_patch = mpatches.Patch(color='tomato', label='Distribución empírica')
    kde_patch = mpatches.Patch(color='black', label='Distribución ajustada')
    plt.legend(handles=[emp_patch, kde_patch])

    plt.show()
