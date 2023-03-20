import os
import pandas
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

try:
    # LISTA
    cods = ['01258', '6154', '01994']

    # LOGIN
    load_dotenv()
    usuario = os.getenv('USUARIO')
    senha = os.getenv('SENHA')

    # SELECTORS
    selector_usuario = 'body > table:nth-child(3) > tbody > tr:nth-child(3) > td:nth-child(5) > font.primary > center > form > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(1) > td:nth-child(2) > input[type=text]'
    selector_senha = 'body > table:nth-child(3) > tbody > tr:nth-child(3) > td:nth-child(5) > font.primary > center > form > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td:nth-child(2) > input[type=password]'
    selector_botao_login = 'body > table:nth-child(3) > tbody > tr:nth-child(3) > td:nth-child(5) > font.primary > center > form > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(3) > td > input'
    selector_botao_logout = '.navbutton'
    selector_guia_catalogo = 'body > table:nth-child(2) > tbody > tr:nth-child(3) > td:nth-child(10) > a'
    selector_codigo_de_barras = 'body > table:nth-child(3) > tbody > tr:nth-child(3) > td:nth-child(5) > font.primary > form:nth-child(3) > table > tbody > tr:nth-child(2) > td > input[type=text]:nth-child(1)'
    selector_botao_pesquisar = 'body > table:nth-child(3) > tbody > tr:nth-child(3) > td:nth-child(5) > font.primary > form:nth-child(3) > table > tbody > tr:nth-child(2) > td > input.button'
    selector_campo_titulo = 'body > table:nth-child(3) > tbody > tr:nth-child(3) > td:nth-child(5) > font.primary > table:nth-child(2) > tbody > tr:nth-child(5) > td:nth-child(2)'
    selector_campo_autor = 'body > table:nth-child(3) > tbody > tr:nth-child(3) > td:nth-child(5) > font.primary > table:nth-child(2) > tbody > tr:nth-child(7) > td:nth-child(2)'
    selector_campo_editora = 'body > table:nth-child(3) > tbody > tr:nth-child(3) > td:nth-child(5) > font.primary > table:nth-child(9) > tbody > tr:nth-child(8)'
    selector_campo_ano = 'body > table:nth-child(3) > tbody > tr:nth-child(3) > td:nth-child(5) > font.primary > table:nth-child(9) > tbody > tr:nth-child(9)'
    selector_campo_isbn = 'body > table:nth-child(3) > tbody > tr:nth-child(3) > td:nth-child(5) > font.primary > table:nth-child(9) > tbody > tr:nth-child(5) > td:nth-child(2)'
    selector_guia_pesquisa = 'body > table:nth-child(3) > tbody > tr:nth-child(3) > td:nth-child(2) > font > a:nth-child(4)'

    # DRIVER
    driver = webdriver.Firefox()
    driver.implicitly_wait(5)

    # ROTINA
    driver.get('http://201.55.32.179/openbiblio/shared/loginform.php')
    driver.find_element(By.CSS_SELECTOR, selector_usuario).send_keys(usuario)
    driver.find_element(By.CSS_SELECTOR, selector_senha).send_keys(senha)
    driver.find_element(By.CSS_SELECTOR, selector_botao_login).click()
    driver.find_element(By.CSS_SELECTOR, selector_guia_catalogo).click()

    lista = [['TITULO', 'AUTOR', 'EDITORA', 'ANO', 'ISBN', 'TOMBO']]
    for item in cods:
        driver.find_element(
            By.CSS_SELECTOR, selector_codigo_de_barras).send_keys(item)
        driver.find_element(By.CSS_SELECTOR, selector_botao_pesquisar).click()

        titulo = driver.find_element(
            By.CSS_SELECTOR,
            selector_campo_titulo
        ).get_attribute('textContent').strip().replace('\n', '')
        autor = driver.find_element(
            By.CSS_SELECTOR,
            selector_campo_autor
        ).get_attribute('textContent').strip().replace('\n', '')
        editora = driver.find_element(
            By.XPATH,
            "//*[contains(text(),'Name of publisher, distributor,etc.:')]"
        ).get_attribute('textContent').strip().replace('\n', '')
        ano = driver.find_element(
            By.XPATH,
            "//*[contains(text(),'Date of publication, distribution, etc.:')]"
        ).get_attribute('textContent').strip().replace('\n', '')
        isbn = driver.find_element(
            By.XPATH,
            "//*[contains(text(),'International Standard Book Number:')]"
        ).get_attribute('textContent').strip().replace('\n', '')
        tombo = item

        lista.append([titulo, autor, editora, ano, isbn, tombo])
        print(lista)
        driver.find_element(By.CSS_SELECTOR, selector_guia_pesquisa).click()

    dataframe = pandas.DataFrame(lista)
    dataframe.to_csv('teste.csv', index=False, header=False)

    driver.quit()

except Exception as error:
    print(error)
