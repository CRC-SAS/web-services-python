
# Carga de paquetes Python necesarios para hacer los requests a la API y graficar resultados
import matplotlib.cm
import matplotlib.pyplot as plt
import yaml
import numpy as np

from mpl_toolkits.basemap import Basemap
from funciones_api import consumir_servicio_JSON

with open('credencial.yml', 'r') as f:
    credencial = yaml.safe_load(f.read())

base_url = 'https://api.crc-sas.org/ws-api'
usuario_default = credencial.get('usuario')
clave_default = credencial.get('clave')

if __name__ == "__main__":
    matplotlib.use('TkAgg')

    # DESCRIPCIÓN DEL PROBLEMA:

    # Problema 1:
    # Geolocalizar todas las estaciones meteorológicas de Argentina en un mapa. Identificar la estación Pehuajó (ID OMM
    # 87544) y todas las estaciones geográficamente vecinas que se encuentren dentro de un radio de 300 kilómetros.

    # SOLUCIÓN DEL PROBLEMA:

    # 1. Búsqueda de estaciones de Argentina (AR, para otros países utilizar el código ISO de 2 letras correspondiente)
    estaciones = consumir_servicio_JSON(url=base_url + "/estaciones/AR",
                                        usuario=usuario_default, clave=clave_default)

    # 2. Búsqueda de estaciones vecinas a Pehuajó (omm_id = 87544).
    #    Se buscan estaciones dentro de un radio de 300km.
    omm_central_id = 87544
    maxima_distancia_km = 300
    url_vecinas = f"{base_url}/estaciones_vecinas/{omm_central_id}?max_distancia={maxima_distancia_km}"
    estaciones_vecinas = consumir_servicio_JSON(url=url_vecinas,
                                                usuario=usuario_default, clave=clave_default)

    # 3. Indico si la estación es Central (Pehuajó), Vecina u Otra
    estaciones = estaciones.assign(
        tipo=lambda df: df.apply(
            lambda x: 'Central' if x['omm_id'] == omm_central_id else 'Vecina' if x['omm_id'] in estaciones_vecinas[
                'omm_id'].values else 'Otra', axis=1)
    )

    # Se imprime el dataframe con las estaciones
    print(estaciones.query('tipo != "Otra"').to_markdown(tablefmt="github", showindex=False))

    # Se genera un mapa en el que es posible visualizar las estaciones
    ar_lon, ar_lat = -38.5, -64
    m = Basemap(lon_0=ar_lon, lat_0=ar_lat, epsg=4326,
                llcrnrlat=-57, urcrnrlat=-20, llcrnrlon=-75, urcrnrlon=-52)
    m.drawmapboundary(fill_color='#A6CAE0', linewidth=0)
    m.fillcontinents(color='grey', alpha=0.7, lake_color='grey')
    m.drawcoastlines(linewidth=0.1, color="white")
    m.drawcountries(linestyle='--')

    for e in estaciones.itertuples():
        if e.tipo == "Central":
            m.tissot(e.longitud, e.latitud, np.rad2deg(300/6367.), 256, facecolor='b', alpha=0.5)
        m.plot(e.longitud, e.latitud, linestyle='none', marker="o", markersize=7, alpha=0.6,
               c='red' if e.tipo == 'Central' else 'orange' if e.tipo == 'Vecina' else 'green',
               markeredgecolor="black", markeredgewidth=1)

    plt.show()
