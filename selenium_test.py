from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def data_acquisition():
    web = 'https://www.audible.com/search'
    path = r'C:\Users\Grati$\Downloads\chromedriver.exe'

    service = Service(executable_path=path)
    driver = webdriver.Chrome(service=service)

    driver.get(web)

    products = driver.find_elements(by='xpath', value='//li[contains(@class, "productListItem")]')

    libros = []

    for product in products:
        titulo = product.find_element(by='xpath', value='.//h3[contains(@class, "bc-heading")]').text
        autor = product.find_element(by='xpath', value='.//li[contains(@class, "authorLabel")]').text
        duracion = product.find_element(by='xpath', value='.//li[contains(@class, "runtimeLabel")]').text
        libros.append({'Título': titulo, 'Autor': autor, 'Duración': duracion})

    driver.quit()

    import pandas as pd

    book_df = pd.DataFrame(libros)
    book_df.to_pickle("books_df.pkl")