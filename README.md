# Componentes:
- Usuario: Inicia el proceso.
- Sistema de Archivos (FileSystem): Comprueba y lee/escribe archivos.
- Sistema de Navegación (Browser): Interactúa con el sitio web de CHIP.
- Script Principal: Controla el flujo del proceso.
- Métodos Auxiliares: Realizan tareas específicas como get_ips, update_ips, cgn_public_entity, open_chip_website, y cgn_consult.

# Interacciones:
1. Inicio del Proceso: El usuario inicia la tarea llamando a get_data_cgn().
2. Comprobación de Archivos: El sistema de archivos verifica si ips.csv y ips_database.csv existen.
3. Extracción de Datos de IPS: Si los archivos no existen, el script llama a get_ips() y update_ips().
4. Configuración del Navegador: El script configura el navegador.
5. Apertura del Sitio CHIP: El script abre el sitio web de CHIP llamando a open_chip_website().
6. Consulta de Entidades Públicas: El script llama a cgn_public_entity(), que a su vez llama a cgn_consult() para cada entidad.
7. Extracción de Datos Financieros: cgn_consult() interactúa con el sitio web de CHIP para extraer los datos y los guarda en cgn_data.csv.