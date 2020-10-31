# Material del webinario del 20 de octubre del 2020

Esta carpeta incluye la presentación utilizada en el webinario, la resolución de cada uno de los problemas planteados a modo de ejemplo en la presentación, la resolución del ejercicio propuesto al finalizar el webinario y código para la instalación de los paquetes Python requeridos.

## Contenido

  - El archivo **Presentacion-2020-10-30.pptx**, es la presentación que hemos utilizado en el webinario.
  - La carpeta **jupyter-python**, incluye la resolución de los problemas planteados a modo de ejemplo en el webinario y del ejercicio propuesto, utilizando Jupyter Notebook.
  - La carpeta **pure-python**, incluye la resolución de los problemas planteados a modo de ejemplo en el webinario y del ejercicio propuesto, sin utilizar Jupyter Notebook.

## Instalación de los paquetes requeridos

  Se recomienda utilizar entornos virtuales para la instalación de los paquetes necesarios.  
  
### Versión con Jupyter Notebook:
  
  En la carpeta **jupyter-python** se ha incluido un script bash llamado **setup.sh** que permite inicializar el ambiente de trabajo. Este script crea un entorno virtual utilizando el paquete venv disponible por defecto en las versiones 3.3+ de Python, activa el nuevo entorno virtual e instala Jupyter Notebook en él. Sin embargo, el script no inicia la ejecución de Jupyter Lab, por lo que luego de la ejecución de **setup.sh** se requiere la ejecución de este comando:

``` bash
jupyter lab
```  
Los demás paquetes requeridos para correr los ejemplos y el ejercicio propuesto en el webinario, utilizando Jupyter Notebook, serán instaladas en una de las secciones de código del archivo **webinario.ipynb**.

### Versión sin Jupyter Notebook:

Esta versión no cuenta con un script de instalación de paquetes, por lo tanto, a continuación se presenta código para instalarlos.

En primer lugar se crea el entorno virtual. Al igual que en la sección anterior, para crearlo se utiliza el paquete venv, disponible por defecto en las versiones 3.3+ de Python.

``` bash
python -m venv .venv
source .venv/bin/activate
```

Una vez creado y activado el entorno virtual, se procede a la instalación de los demás paquetes requeridos con el código presentado a continuación.

``` bash
python -m pip install wheel
python -m pip install setuptools
python -m pip install netCDF4
python -m pip install python-dateutil
python -m pip install pandas
python -m pip install seaborn
python -m pip install tabulate
python -m pip install requests
python -m pip install statsmodels
python -m pip install https://github.com/matplotlib/basemap/archive/master.zip
```
  
