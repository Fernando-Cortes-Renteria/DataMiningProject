'''
================ Descarga de Datos de Broward County ================

Hecho por: Manbo Solutions
Colaboradores:
* Manbo Lead
* Manbo Dev

Usando webscraping con Selenium, descarga de datos de un gran número de residencias en
Florida

'''

# importo librerias
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd

# función para descargar datos de bcpa.net
def data_broward():

    # importo lista de búsqueda de folios de casas del condado
    bc_search = pd.read_csv('Search Results.csv')
    folios = bc_search['Folio Number']

    # conecto con el webdriver que entrará automáticamente a Chrome
    path = r'C:\Users\Grati$\Downloads\chromedriver.exe'
    service = Service(executable_path=path)
    driver = webdriver.Chrome(service=service)

    # Me dirijo al sitio web
    web = 'https://web.bcpa.net/BcpaClient/#/Record-Search?fnumber=494026AA2620'

    driver.get(web)

    driver.implicitly_wait(15)
    data = driver.find_element(by='xpath', value='//div[contains(@class, "px-0 px-sm-2 col-sm-6")]')

    tables = data.find_elements(by='xpath', value='.//table')

    all_table_data = []

    for idx, table in enumerate(tables, start=1):
        rows = table.find_elements(By.TAG_NAME,'tr')
        table_data = {}
        for row in rows:
            cells = row.find_elements(By.TAG_NAME,'td')
            if len(cells) == 2:
                key = cells[0].text.strip()
                value = cells[1].text.strip()
                table_data[key] = value
        all_table_data.append({"table_number": idx, **table_data})

    # convert to DataFrame
    df = pd.DataFrame(all_table_data)
    print(df)

    driver.quit()

data_broward()