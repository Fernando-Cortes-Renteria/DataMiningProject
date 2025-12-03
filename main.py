import pandas as pd
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

# --------------------------
# 1️⃣ Leer CSV limpio
# --------------------------
df = pd.read_csv('sr_clean.csv')
df.columns = [col.strip() for col in df.columns]

# --------------------------
# 2️⃣ Configurar Selenium
# --------------------------
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # Para ver el navegador, comentar esta línea
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)
url = "https://web.bcpa.net/BcpaClient/#/Record-Search"

# --------------------------
# 3️⃣ Función para extraer info de la página
# --------------------------
def extract_property_info(folio, owner, address):
    try:
        driver.get(url)

        # Esperar que cargue el input de búsqueda
        search_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="text"]'))
        )
        search_input.clear()
        search_input.send_keys(folio)  # Usamos Folio Number para búsqueda
        search_input.send_keys(Keys.RETURN)

        # Esperar que cargue el detalle de la propiedad
        wait.until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class,"record-info")]'))
        )

        # Extraer campos
        property_owner = driver.find_element(By.XPATH, '//div[contains(text(),"Property Owner")]/following-sibling::div').text
        mailing_address = driver.find_element(By.XPATH, '//div[contains(text(),"Mailing Address")]/following-sibling::div').text
        property_address = driver.find_element(By.XPATH, '//div[contains(text(),"Property Address")]/following-sibling::div').text

        # Extraer Assessment Table
        assessment_table = []
        try:
            table_rows = driver.find_elements(By.XPATH, '//table[contains(@class,"assessment-table")]//tr')
            for row in table_rows[1:]:  # saltar encabezado
                cols = [c.text for c in row.find_elements(By.TAG_NAME, 'td')]
                assessment_table.append(cols)
        except:
            assessment_table = []

        # Extraer Sales History Table
        sales_history = []
        try:
            table_rows = driver.find_elements(By.XPATH, '//table[contains(@class,"sales-history")]//tr')
            for row in table_rows[1:]:
                cols = [c.text for c in row.find_elements(By.TAG_NAME, 'td')]
                sales_history.append(cols)
        except:
            sales_history = []

        # Construir JSON
        data = {
            'Folio Number': folio,
            'Owner Name CSV': owner,
            'Property Address CSV': address,
            'Property Owner(s)': property_owner,
            'Mailing Address': mailing_address,
            'Property Address Detail': property_address,
            'Assessment Table': assessment_table,
            'Sales History': sales_history
        }

        # Guardar JSON
        output_file = f'property_{folio}.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"[OK] Guardado: {output_file}")

    except Exception as e:
        print(f"[ERROR] Falló {folio}: {e}")

# --------------------------
# 4️⃣ Iterar CSV
# --------------------------
for idx, row in df.iterrows():
    extract_property_info(row['Folio Number'], row['Owner Name'], row['Property Address'])

driver.quit()
print("Scraping completado.")
