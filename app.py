import os
import pandas
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
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


def checar_paginas(item):
    try:
        driver.find_element(
            By.XPATH,
            f'//*[contains(text(),{item})]'
        )
    except NoSuchElementException:
        return False
    return True


def checar_livro(links, tombo, lista):
    for item in links:
        try:
            driver.get(item)

            cod = driver.find_element(
                By.XPATH, f'//*[contains(text(), {tombo})]')
            cod = cod.get_attribute('textContent').strip().replace('\n', '')

            if cod == str(tombo):
                lista.append(varrer_dados(tombo))
            else:
                continue

        except NoSuchElementException:
            continue


def varrer_dados(tombo):
    xpath = [
        '//*[contains(text(),"Título:")]/following-sibling::*',
        '//*[contains(text(),"Personal name:")]/following-sibling::*',
        '//*[contains(text(),"Name of publisher, distributor, etc.:")]/following-sibling::*',
        '//*[contains(text(),"Date of publication, distribution, etc.:")]/following-sibling::*',
        '//*[contains(text(),"Topical term or geographic name as entry element:")]/following-sibling::*',
        '//*[contains(text(),"International Standard Book Number:")]/following-sibling::*',
        f'//*[contains(text(), "{tombo}")]/following-sibling::*'
    ]
    valores = [tombo]

    for campo in xpath:
        try:
            valor = driver.find_element(
                By.XPATH,
                campo
            ).get_attribute('textContent').strip().replace('\n', '')
            
            valores.append(valor)

        except NoSuchElementException:
            valores.append('---ERRO---')

    return valores

lista = [['TOMBO', 'TITULO', 'AUTOR', 'EDITORA', 'ANO', 'ASSUNTO','ISBN', 'EXEMPLAR']]

# DRIVER
options = Options()
options.add_argument('-headless')
driver = webdriver.Firefox(options=options)
driver.implicitly_wait(5)

try:
    # LISTA
    tombos = pandas.read_csv(
        'tombos.csv',
        dtype=str,
        header=None
    ).squeeze('columns')

    # LOGIN
    load_dotenv()
    usuario = os.getenv('USUARIO')
    senha = os.getenv('SENHA')

    # SELECTORS
    selector_usuario = 'body > table:nth-child(3) > tbody > tr:nth-child(3) > td:nth-child(5) > font.primary > center > form > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(1) > td:nth-child(2) > input[type=text]'
    selector_senha = 'body > table:nth-child(3) > tbody > tr:nth-child(3) > td:nth-child(5) > font.primary > center > form > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td:nth-child(2) > input[type=password]'
    selector_botao_login = 'body > table:nth-child(3) > tbody > tr:nth-child(3) > td:nth-child(5) > font.primary > center > form > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(3) > td > input'
    selector_botao_logout = '.navbutton'
    selector_codigo_de_barras = 'body > table:nth-child(3) > tbody > tr:nth-child(3) > td:nth-child(5) > font.primary > form:nth-child(3) > table > tbody > tr:nth-child(2) > td > input[type=text]:nth-child(1)'
    selector_botao_pesquisar = 'body > table:nth-child(3) > tbody > tr:nth-child(3) > td:nth-child(5) > font.primary > form:nth-child(3) > table > tbody > tr:nth-child(2) > td > input.button'

    # ROTINA
    driver.get('http://biblioteca.fateczl.edu.br/openbiblio/shared/loginform.php')
    driver.find_element(By.CSS_SELECTOR, selector_usuario).send_keys(usuario)
    driver.find_element(By.CSS_SELECTOR, selector_senha).send_keys(senha)
    driver.find_element(By.CSS_SELECTOR, selector_botao_login).click()

    for item in tombos:
        print(item)
        driver.get('http://biblioteca.fateczl.edu.br/openbiblio/catalog/index.php')

        driver.find_element(
            By.CSS_SELECTOR,
            selector_codigo_de_barras
        ).send_keys(item)

        driver.find_element(
            By.CSS_SELECTOR,
            selector_botao_pesquisar
        ).click()

        if checar_lista():
            lista.append(varrer_dados(item))

        else:
            if checar_paginas(item):
                livros = driver.find_elements(
                    By.XPATH,
                    f'//a[. /img[@src="../images/book.gif"]]'
                )

                links = []

                for link in livros:
                    links.append(link.get_attribute('href'))

                checar_livro(links, item, lista)

            else:
                lista.append([item, '--- NÃO ENCONTRADO ---', '', '', '', '', '', ''])

        driver.get('http://biblioteca.fateczl.edu.br/openbiblio/catalog/index.php')

    dataframe = pandas.DataFrame(lista)
    dataframe.to_csv('resultados.csv', index=False, header=False)

    driver.find_element(By.CSS_SELECTOR, selector_botao_logout).click()
    driver.quit()

except Exception as error:
    dataframe = pandas.DataFrame(lista)
    dataframe.to_csv('resultados.csv', index=False, header=False)
    driver.quit()
    print(error)
