# CHIP Bot

![CHIP Bot!](/chip_bot.png "CHIP Bot")

Crédito de la imagen del robot: 
<a href="https://www.vecteezy.com/free-vector/bot">Bot Vectors by Vecteezy</a>

# Descripción del Script
Este script automatiza el proceso de consulta y extracción de información financiera de hospitales públicos desde el sistema CHIP (Contabilidad Pública y Sistemas de Información de Hacienda Pública) de Colombia, utilizando técnicas de web scraping y procesamiento de datos, el script realiza las siguientes acciones principales:

1. Configuración del Navegador: Inicializa el navegador en modo headless (sin interfaz gráfica) con un tiempo de espera entre acciones configurado.

2. Navegación al Sitio Web del CHIP: Abre la página principal del sistema CHIP e ingresa al formulario de "Consulta de información Financiera, Económica, Social y Ambiental".

3. Relleno del Formulario: Completa automáticamente el formulario con la entidad seleccionada, categoría, periodo, y otros parámetros necesarios para la consulta.

4. Extracción de Datos de la Tabla: Una vez que los datos están disponibles, el script captura el HTML de la tabla de resultados, lo procesa utilizando BeautifulSoup para extraer los datos en un formato estructurado.

5. Procesamiento de Datos: Convierte los datos extraídos en un DataFrame de Pandas, agregando información adicional como entidad, categoría, periodo, y número de identificación. Además, convierte columnas específicas a tipo numérico para un mejor análisis.

6. Almacenamiento de Datos: Verifica si el archivo CSV de datos ya existe. Si existe, combina los nuevos datos con los existentes. Si no, crea un nuevo archivo. Los datos se guardan en data/cgn_data.csv.

7. Registro de Entidades Procesadas: Mantiene un registro de las entidades ya procesadas para evitar duplicaciones en futuras ejecuciones. Este registro se guarda en data/processed_entities.csv.

8. Manejo de Errores y Reintentos: Implementa mecanismos para manejar errores y reintentar la operación en caso de fallos durante la consulta o extracción de datos.

# Librerías utilizadas
El script utiliza las siguientes librerías:

- robocorp.tasks: Para definir y ejecutar tareas de automatización.
- robocorp.browser: Para controlar el navegador y realizar acciones de web scraping.
- RPA.FileSystem: Para manejar operaciones del sistema de archivos, como leer y escribir archivos.
- RPA.Tables: Para manipular datos tabulares.
- BeautifulSoup: Para analizar y extraer datos de HTML.
- pandas: Para el manejo y procesamiento de datos estructurados en DataFrames.
- bs4: Paquete que contiene BeautifulSoup para el análisis de documentos HTML y XML.

## License

This program is distributed under the terms of the GNU Lesser General Public License (LGPL) v3. See the [LICENSE](http://www.gnu.org/licenses/) file for details.

## Author

- **Name:** Hector Ivan Valencia Muñoz

## Requirements

This script run over Robocorp an this provides an extension for Visual Studio Code. See [How to](https://robocorp.com/docs/visual-studio-code).

## Installation

1. Clone the repository
2. Run over Robocorp extension for Visual Studio Code

## Usage

1. Run the script

2. Output files:

  - cgn_data.csv: A CSV file with the results.
  - processed_entities.csv: Updated CSV file with validated entities.

***El script recolecta la información financiera reportada en el sistema CHIP para el periodo octubre - diciembre de 2023.  Para obtener información de periodos diferentes se debe modificar la siguiente variable en la línea 130:***
-  periodo = "OCT A DIC - 2023"

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Acknowledgements

Special thanks to the Robocorp team for their excellent tools and documentation.

# Diagrama de secuencia

![UML sequence diagram](/flow_chart.png)