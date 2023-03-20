import os
import pandas
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


def checar_lista():
    try:
        driver.find_element(
            By.XPATH,
            '//*[contains(text(),"International Standard Book Number:")]'
        )
    except NoSuchElementException:
        return False
    return True


def checar_tombo(tombo):
    try:
        driver.find_element(
            By.XPATH,
            f'//*[contains(text(),{tombo})]'
        )
    except NoSuchElementException:
        return False
    return True


try:
    # LISTA
    cods = ['1963']
    # cods = ['01258', '6154', '01994', '1963']

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
    selector_guia_pesquisa = 'body > table:nth-child(3) > tbody > tr:nth-child(3) > td:nth-child(2) > font > a:nth-child(4)'

    # DRIVER
    # options = Options()
    # options.headless = True
    driver = webdriver.Firefox()
    driver.implicitly_wait(3)

    # ROTINA
    driver.get('http://201.55.32.179/openbiblio/shared/loginform.php')
    driver.find_element(By.CSS_SELECTOR, selector_usuario).send_keys(usuario)
    driver.find_element(By.CSS_SELECTOR, selector_senha).send_keys(senha)
    driver.find_element(By.CSS_SELECTOR, selector_botao_login).click()
    driver.find_element(By.CSS_SELECTOR, selector_guia_catalogo).click()

    lista = [['TITULO', 'AUTOR', 'EDITORA', 'ANO', 'ISBN', 'TOMBO', 'EXEMPLAR']]
    for item in cods:
        driver.find_element(
            By.CSS_SELECTOR, selector_codigo_de_barras).send_keys(item)
        driver.find_element(By.CSS_SELECTOR, selector_botao_pesquisar).click()

        if checar_lista():
            titulo = str(driver.find_element(
                By.XPATH,
                '//*[contains(text(),"Título:")]/following-sibling::*'
            ).get_attribute('textContent').strip().replace('\n', ''))
            autor = str(driver.find_element(
                By.XPATH,
                '//*[contains(text(),"Personal name:")]/following-sibling::*'
            ).get_attribute('textContent').strip().replace('\n', ''))
            editora = str(driver.find_element(
                By.XPATH,
                '//*[contains(text(),"Name of publisher, distributor, etc.:")]/following-sibling::*'
            ).get_attribute('textContent').strip().replace('\n', ''))
            ano = str(driver.find_element(
                By.XPATH,
                '//*[contains(text(),"Date of publication, distribution, etc.:")]/following-sibling::*'
            ).get_attribute('textContent').strip().replace('\n', ''))
            isbn = str(driver.find_element(
                By.XPATH,
                '//*[contains(text(),"International Standard Book Number:")]/following-sibling::*'
            ).get_attribute('textContent').strip())
            tombo = str(item)
            exemplar = str(driver.find_element(
                By.XPATH,
                f'//*[contains(text(),{item})]/following-sibling::*'
            ).get_attribute('textContent').replace('\n', ''))

        else:
            # /html/body/table[3]/tbody/tr[3]/td[5]/font[1]/table/tbody/tr[3]/td[1]/font
            celula = driver.find_element(By.XPATH, f'//tr[. /td/*[contains(text(),{item})]]/preceding::tbody')
            print(celula.get_attribute('textContent'))
            links = celula.find_elements(By.XPATH, 'a')

            for i in links:
                print(i.get_attribute('textContent'))

            

        lista.append([titulo, autor, editora, ano, isbn, tombo, exemplar])
        driver.find_element(By.CSS_SELECTOR, selector_guia_pesquisa).click()

    dataframe = pandas.DataFrame(lista)
    dataframe.to_csv('teste.csv', index=False, header=False)

    driver.quit()

except Exception as error:
    driver.quit()
    print(error)
