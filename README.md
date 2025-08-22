## Upload products from Amazon to your store at Mercadolibre <br><br>
#  Bot de carga y sincronización de productos de Amazon a MercadoLibre

Este proyecto está desarrollado en **Python** y permite automatizar la carga y sincronización de productos desde Amazon hacia tu tienda en MercadoLibre, utilizando su API.

##  Estructura del repositorio

El archivo `.bat` principal se encuentra en:

Upload-Amazon-s-products-to-your-Mercadolibre-s-store/project/winkscraper/winkscraper/spiders/botsStarters/ <br><br>


Dentro de esa carpeta hay **4 archivos `.bat`**:

- **winkSynchTest.bat**  
  Sincroniza o actualiza datos de productos ya subidos (precios, especificaciones, colores, etc.) — en modo de prueba.

- **winkUploadTest.bat**  
  Sube un producto de prueba (no estaba en tu tienda de MercadoLibre) — en modo de prueba.

- **winkSynchBot.bat**  
  Hace la sincronización real de productos existentes (modo no prueba).

- **winkUploadBot.bat**  
  Carga productos reales de Amazon a tu tienda de MercadoLibre (modo no prueba).

##  Requisitos

Tener instalado **Python 3.x** (recomiendo 3.8 o superior).

⚙️ **Instalación de dependencias**

Este proyecto incluye un archivo requirements.txt con todas las librerías necesarias.

Después de clonar o descargar el repositorio, abre una terminal en la carpeta raíz del proyecto y ejecuta:

<pre> pip install -r requirements.txt <pre> <br><br>

##  ¿Cómo usar el bot?

Clona o descarga todo el repositorio a tu máquina local.

Navega a la carpeta que contiene los .bat:
