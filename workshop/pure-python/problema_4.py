
# Carga de paquetes Python necesarios para hacer los requests a la API y graficar resultados
import dateutil.parser
import matplotlib.cm
import matplotlib.pyplot as plt
import yaml

from mpl_toolkits.basemap import Basemap
from funciones_api import consumir_servicio_espacial

with open('credencial.yml', 'r') as f:
    credencial = yaml.safe_load(f.read())

base_url = 'https://api.crc-sas.org/ws-api'
usuario_default = credencial.get('usuario')
clave_default = credencial.get('clave')

if __name__ == "__main__":
    matplotlib.use('TkAgg')

    # DESCRIPCIÓN DEL PROBLEMA:

    # Problema 4:
    # Obtener el SPI-3 basado en CHIRPS para Uruguay. Los valores de SPI-3 deben
    # corresponder al período enero a marzo de 2019.

    # SOLUCIÓN DEL PROBLEMA:

    # Descargar los datos de SPI-3 basados en CHIRPS.
    fecha_desde = dateutil.parser.parse("2019-03-31").isoformat()
    fecha_hasta = dateutil.parser.parse("2019-03-31").isoformat()
    url_chirps = f"{base_url}/chirps/spi/3/{fecha_desde}/{fecha_hasta}"
    fechas, rasters = consumir_servicio_espacial(url=url_chirps, usuario=usuario_default, clave=clave_default,
                                                 archivo_geojson_zona="./Uruguay.geojson", raster_var_tag='spi')

    # Graficar rasters de CHIRPS.
    ar_lon, ar_lat = -38.5, -64
    m = Basemap(lon_0=ar_lon, lat_0=ar_lat, epsg=4326,
                llcrnrlat=-57, urcrnrlat=-20, llcrnrlon=-75, urcrnrlon=-52)
    m.drawmapboundary(fill_color='#A6CAE0', linewidth=0)
    m.fillcontinents(color='grey', alpha=0.7, lake_color='grey')
    m.drawcoastlines(linewidth=0.1, color="white")
    m.drawcountries(linestyle='--')

    ax = plt.gca()
    extent = [-58.5, -53, -35.1, -30]
    ax.imshow(rasters[0], extent=extent, vmin=rasters.min(), vmax=rasters.max(), zorder=3)

    plt.axis('off')
    plt.show()


