from robocorp.tasks import task
from robocorp import browser

from RPA.FileSystem import FileSystem
from RPA.Tables import Tables

import pandas as pd

filesystem = FileSystem()
table = Tables()

@task
def get_data_cgn():
    """
    Consultar reporte de información financera de Hospitales Públicos al sistema CHIP
    """
    browser.configure(slowmo=200, headless=True)

    open_chip_website()

    cgn_data_consult()

def open_chip_website():
    # Abrir formulario: "Consulta de información Financiera, Económica, Social y Ambiental"
    page = browser.page()
    page.goto("https://www.chip.gov.co", timeout=60000)
    if page.query_selector('//*[@id="j_idt105:InformacionEnviada"]'):
        page.click('//*[@id="j_idt105:InformacionEnviada"]', timeout=60000)

def fill_form(entidad, categoria, periodo, numero_identificacion):
    page = browser.page()
    page.query_selector('//*[@id="frm1:SelBoxEntidadCiudadano_input"]')
    page.fill('//*[@id="frm1:SelBoxEntidadCiudadano_input"]', entidad)
    page.press('//*[@id="frm1:SelBoxEntidadCiudadano_input"]', 'Enter')

    page.select_option('//*[@id="frm1:SelBoxCategoria"]', categoria)
    page.select_option('//*[@id="frm1:SelBoxPeriodo"]', periodo)
    page.select_option('//*[@id="frm1:SelBoxForma"]', 'CGN2015_001_SALDOS_Y_MOVIMIENTOS_CONVERGENCIA')

    page.click('//*[@id="frm1:BtnConsular"]')
    page.wait_for_selector('//*[@id="frm1:SelBoxNivel"]', state='visible', timeout=60000)
    page.select_option('//*[@id="frm1:SelBoxNivel"]', '5')

def process_table(entidad, categoria, periodo, numero_identificacion):
    page = browser.page()
    # Seleccionar resultados usando un selector más estable basado en clases y etiquetas
    table_selector = 'table.iceDatTbl'
    header_selector = f'{table_selector} thead tr'
    row_selector = f'{table_selector} tbody tr'    
    # Espera a que la tabla esté presente en el DOM
    page.wait_for_selector(table_selector, state='attached', timeout=60000)    
    # Espera adicional para asegurar que el contenido esté completamente cargado
    page.wait_for_timeout(5000)  # Espera 5 segundos adicionales    
    # Selecciona todas las filas del encabezado de la tabla
    header_rows = page.query_selector_all(header_selector)
    
    table_data = []

    # Extraer datos del encabezado
    if header_rows:
        cols = header_rows[0].query_selector_all('th')  # Cambia 'th' por 'td' si las celdas no están en <th>
        headers = [col.inner_text() for col in cols]
        headers.extend(['Entidad', 'Categoria', 'Periodo', 'NumeroIdentificacion'])  # Agregar columnas de los argumentos
        table_data.append(headers)
    # Selecciona todas las filas del cuerpo de la tabla
    body_rows = page.query_selector_all(row_selector)
    # Extraer datos del cuerpo de la tabla
    for row in body_rows:
        cols = row.query_selector_all('td')
        col_data = [col.inner_text() for col in cols]
        if any(col_data):  # Evita agregar filas completamente vacías
            col_data.extend([entidad, categoria, periodo, numero_identificacion])  # Agregar valores de los argumentos
            table_data.append(col_data)    
    # Convertir los datos en un DataFrame de Pandas
    new_data_df = pd.DataFrame(table_data[1:], columns=table_data[0])
    # Eliminar la primera columna vacía si existe
    if new_data_df.columns[0] == '':
        new_data_df = new_data_df.drop(new_data_df.columns[0], axis=1)
    # Convertir columnas específicas a float
    cols_to_convert = ['SALDO INICIAL(Pesos)', 'MOVIMIENTO DEBITO(Pesos)', 'MOVIMIENTO CREDITO(Pesos)', 
                       'SALDO FINAL(Pesos)', 'SALDO FINAL CORRIENTE(Pesos)', 'SALDO FINAL NO CORRIENTE(Pesos)']
    for col in cols_to_convert:
        new_data_df[col] = new_data_df[col].str.replace(',', '').astype(float).astype(int)    
    # Verificar si el archivo ya existe
    file_path = "data/cgn_data.csv"
    if filesystem.does_file_exist(file_path):
        # Leer el archivo existente
        existing_data_df = pd.read_csv(file_path)
        # Concatenar el nuevo DataFrame con el existente
        combined_df = pd.concat([existing_data_df, new_data_df], ignore_index=True)
    else:
        # Si no existe, solo usaremos el nuevo DataFrame
        combined_df = new_data_df
    # Guardar los datos combinados en el archivo CSV
    combined_df.to_csv(file_path, index=False)

    try:
        page.click("text=Volver", timeout=60000)
    except Exception as e:
        print(f"Error al hacer clic en 'Volver': {e}")
        page.close()
        browser.configure(slowmo=200, headless=True)      
        open_chip_website()
        page.wait_for_timeout(5000)  # Espera 5 segundos adicionales    

def cgn_data_consult():
    page = browser.page()
    ips_database = "data/ips_database.csv"
    processed_entities_file = "data/processed_entities.csv"
    # Leer ips.csv asegurando que id_entidad y razón social sean leídos como texto
    dtype_dict_public_entities = {
        'id_entidad': str,
        'NumeroIdentificacion': str,
        'razon_social': str
    }
    # Leer el archivo CSV original
    df = pd.read_csv(ips_database, dtype=dtype_dict_public_entities, low_memory=False)
    # Filtrar solo las "Instituciones Prestadoras de Servicios de Salud"
    df = df[df['ESE'] == 'SI']
    df = df.dropna(subset=['id_entidad'])
    df["entidad"] = df['id_entidad'].map(str) + " - " + df['razon_social']
    # Argumentos necesarios para ejecutar la consulta en CHIP
    entidades = df[["entidad", "NumeroIdentificacion"]].values.tolist()
    categoria = "INFORMACIÓN CONTABLE PUBLICA - CONVERGENCIA"
    periodo = "OCT A DIC - 2023"
    # Cargar entidades ya procesadas
    if filesystem.does_file_exist(processed_entities_file):
        processed_entities_df = pd.read_csv(processed_entities_file)
        processed_entities = processed_entities_df["entidad"].tolist()
    else:
        processed_entities = []

    # Filtrar entidades ya procesadas
    entidades_pendientes = [ent for ent in entidades if ent[0] not in processed_entities]

    # Seleccionar registros para test del script
    # entidades_pendientes = entidades_pendientes[:3]

    # Consultar información financiera en CHIP
    for entidad, numero_identificacion in entidades_pendientes:
        try:
            fill_form(entidad, categoria, periodo, numero_identificacion)
            # table_html = capture_table()
            process_table(entidad, categoria, periodo, numero_identificacion)
            processed_entities.append(entidad)
            pd.DataFrame({"entidad": processed_entities}).to_csv(processed_entities_file, index=False)
        except Exception as e:
            print(f"Error al procesar la entidad {entidad}: {e}")
            page.reload()
            page.wait_for_timeout(5000)  # Espera 5 segundos adicionales    
            continue