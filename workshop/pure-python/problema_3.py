
# Carga de paquetes Python necesarios para hacer los requests a la API y graficar resultados
import dateutil.parser
import matplotlib.cm
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import yaml

from pentadas import fecha_fin_pentada, pentada_año_a_fecha_inicio
from funciones_api import consumir_servicio_JSON

with open('credencial.yml', 'r') as f:
    credencial = yaml.safe_load(f.read())

base_url = 'https://api.crc-sas.org/ws-api'
usuario_default = credencial.get('usuario')
clave_default = credencial.get('clave')

if __name__ == "__main__":
    matplotlib.use('TkAgg')

    # DESCRIPCIÓN DEL PROBLEMA:

    # Problema 3:
    # Obtener las series temporales de SPI-3 para Pehuajó (87544) calculado mediante un ajuste paramétrico de
    # precipitaciones dentro del período de referencia 1971-2010, utilizando el método de máxima verosimilitud
    # sin remuestreo. Graficar la serie para el período 2017-2019.

    # SOLUCIÓN DEL PROBLEMA:

    # Se obtiene un listado de configuraciones de índices y se seleccionan los SPI con escala de 3 meses.
    configuraciones = consumir_servicio_JSON(url=f"{base_url}/indices_sequia_configuraciones",
                                             usuario=usuario_default, clave=clave_default)
    # Seleccionar SPI y escala de 3 meses
    configuraciones = configuraciones.query('indice == "SPI" and escala == 3')
    # Vista de las configuraciones en una tabla
    print(configuraciones.to_markdown(tablefmt="github", showindex=False))

    # Ahora procedemos a buscar la serie temporal de SPI-3 para Pehuajó entre 2017 y 2019.
    omm_id = 87544
    indice_configuracion_id = 43
    fecha_desde = dateutil.parser.parse("2017-01-01").isoformat()
    fecha_hasta = dateutil.parser.parse("2019-12-31").isoformat()
    url_valores_indice = f"{base_url}/indices_sequia_valores/{indice_configuracion_id}/" \
                         f"{omm_id}/{fecha_desde}/{fecha_hasta}"
    serie_temporal_spi = consumir_servicio_JSON(url=url_valores_indice,
                                                usuario=usuario_default, clave=clave_default)

    # Definir la fecha de fin del período a partir del año y la péntada de fin
    serie_temporal_spi = serie_temporal_spi.assign(
        fecha_fin_pentada=lambda df: df.apply(
            lambda x: fecha_fin_pentada(pentada_año_a_fecha_inicio(x['pentada_fin'], x['ano'])), axis=1)
    )

    # Graficar
    fig, ax1 = plt.subplots(figsize=(10, 3))
    ax1.plot('fecha_fin_pentada', 'valor_indice', data=serie_temporal_spi, color='#fc8d62', marker="D", markersize=4)
    ax2 = ax1.twinx()
    ax2.bar('fecha_fin_pentada', 'valor_dato', data=serie_temporal_spi, color='#226bb0')

    ax1.set_ylabel('SPI-3')
    ax1.set_xlabel('Fecha de fin del período')
    ax2.set_ylabel('Precipitación acumulada (mm)')

    spi_patch = mpatches.Patch(color='#fc8d62', label='SPI-3')
    prcp_patch = mpatches.Patch(color='#226bb0', label='Precipitación acumulada')
    plt.legend(handles=[spi_patch, prcp_patch])

    plt.show()
