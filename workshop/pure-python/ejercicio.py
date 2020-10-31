
# Carga de paquetes Python necesarios para hacer los requests a la API y graficar resultados
import dateutil.parser
import pandas
import matplotlib.cm
import matplotlib.pyplot as plt
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

    # Ejercicio propuesto:
    # Obtener las series temporales de SPI-3 para Durazno (Uruguay) (86530) y las estaciones geográficamente vecinas
    # dentro de un radio de 150 kilómetros. Buscar los datos de SPI-3 calculado mediante un ajuste no paramétrico de
    # precipitaciones dentro del período de referencia 1971-2010. Graficar las series para el período 2017-2019.

    # SOLUCIÓN DEL PROBLEMA:

    # 1. Búsqueda de estaciones vecinas a Durazno (omm_id = 86530).
    #    Se buscan estaciones dentro de un radio de 100km.
    omm_central_id = 86530
    max_distancia_km = 150
    url_vecinas = f"{base_url}/estaciones_vecinas/{omm_central_id}?max_distancia={max_distancia_km}"
    estaciones_vecinas = consumir_servicio_JSON(url=f"{url_vecinas}",
                                                usuario=usuario_default, clave=clave_default)
    # Se agrega la estación Durazno al dataframe
    estaciones = estaciones_vecinas[['omm_id', 'nombre']]\
        .append({'omm_id': '86530', 'nombre': 'Durazno'}, ignore_index=True)

    # Vista de estaciones vecinas en una tabla
    print(estaciones.to_markdown(tablefmt="github", showindex=False))

    configuraciones = consumir_servicio_JSON(url=f"{base_url}/indices_sequia_configuraciones",
                                             usuario=usuario_default, clave=clave_default)
    # Seleccionar SPI y escala de 3 meses
    configuraciones = configuraciones.query('indice == "SPI" and escala == 3')

    # Vista de las configuraciones en una tabla
    print(configuraciones.to_markdown(tablefmt="github", showindex=False))

    # Se buscan las series temporales para todas las estaciones (una a la vez)
    series_temporales = pandas.DataFrame()
    indice_configuracion_id = 3
    fecha_desde = dateutil.parser.parse("2017-01-01").isoformat()
    fecha_hasta = dateutil.parser.parse("2019-12-31").isoformat()

    for estacion in estaciones.itertuples():
        # Ahora se define la URL para realizar la búsqueda
        url_valores_indice = f"{base_url}/indices_sequia_valores/{indice_configuracion_id}/" \
                             f"{estacion.omm_id}/{fecha_desde}/{fecha_hasta}"
        # Buscar serie temporal y agregar el nombre de la estacion (con ID)
        serie_temporal_spi = consumir_servicio_JSON(url=url_valores_indice,
                                                    usuario=usuario_default, clave=clave_default)
        # Definir la fecha de fin del período a partir del año y la péntada de fin
        serie_temporal_spi = serie_temporal_spi.assign(
            fecha_fin_pentada=lambda df: df.apply(
                lambda x: fecha_fin_pentada(pentada_año_a_fecha_inicio(x['pentada_fin'], x['ano'])), axis=1)
        )
        # Agregar nombre para el gráfico
        serie_temporal_spi['nombre_completo'] = f"{estacion.nombre} ({estacion.omm_id})"

        # Agregar filas a data frame de todas las series temporales
        series_temporales = series_temporales.append(serie_temporal_spi, ignore_index=True)

    # Vista de las series_temporales en una tabla
    print(series_temporales.to_markdown(tablefmt="github", showindex=False))

    # Generar gráfico
    series_temporales.set_index('fecha_fin_pentada', inplace=True)
    series_temporales.groupby('nombre_completo')['valor_indice']\
        .plot(legend=True, xlim=('2017-01-01', '2020-01-01'), marker="D")\
        .map(lambda ax: ax.set(xlabel='Fecha de fin del periodo', ylabel='SPI-3'))
    plt.suptitle('Series temporales de SPI-3')
    plt.title('Durazno (UY) y estaciones dentro de un radio de 150 kms.')
    plt.show()
