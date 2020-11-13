import csv, sys
import requests
import os.path
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import json

URL = 'https://play.google.com/store/apps/details?id=com.github.android'
URL_SUFIX = '&hl=en-US&showAllReviews=true'
SCROLL_PAUSE_TIME = 2

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0"
}

def get_app_info():
    global URL
    page = requests.get(URL+URL_SUFIX, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Informações do aplicativo
    nome            = soup.find("h1", class_="AHFaub", itemprop="name").get_text()
    id_             = URL.split('=')[1].split('&')[0]
    desenvolvedora  = soup.find("a", class_="hrTbp R8zArc").get_text()
    categoria       = soup.find("a", class_="hrTbp R8zArc", itemprop="genre").get_text()
    estrelas        = float(soup.find("div", class_="pf5lIe").div['aria-label'].split(' ')[1])
    reviews         = float(soup.find("span", class_="AYi5wd TBRnV").span['aria-label'].split(' ')[0].replace(",","."))

    # Dicionário para conversão em json
    json_dict = {
        '_id': id_,
        'name': nome,
        'dev': desenvolvedora,
        'catedory': categoria,
        'stars': estrelas,
        'num_reviews': reviews
    }

    with open('file.json', 'w') as file:
        file.write(json.dumps(json_dict))

def get_comments():
    global URL

    # Abrindo a URL com o selenium e executando o geckodriver
    driver = webdriver.Firefox(executable_path=os.getcwd() + "/geckodriver/geckodriver.exe")
    
    driver.get(URL+URL_SUFIX)

    # Tamanho do scroll
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll até o fim da página
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Esperando a página carregar
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculando a nova altura do scroll e comparando com o anterior
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:

            # Verificar se existe botão
            SM_button = None
            try:
                SM_button = driver.find_element_by_xpath('/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div/main/div/div[1]/div[2]/div[2]/div/span/span')
            except NoSuchElementException as nsee:
                print(nsee)

            if SM_button != None:
                SM_button.click()
            else:
                break
        last_height = new_height

    comment_page = driver.execute_script("return document.documentElement.outerHTML")
    
    driver.quit()
    
    soup = BeautifulSoup(comment_page, 'html.parser')
    
    # Separando somente a seção de comentários do html
    comment_section = soup.find_all("div", jsmodel="y8Aajc", jscontroller="H6eOGe")

    id_ = URL.split('=')[1].split('&')[0]

    # Extraindo as informações da página
    with open('file_comement.json', 'w') as file:
        for num, comment in enumerate(comment_section):
            nome       = comment.find("span", class_="X43Kjb").get_text()
            estrelas   = int(comment.find("div", class_="pf5lIe").div['aria-label'].split(' ')[1])
            comentario = comment.find("span", jsname="bN97Pc").get_text()
            likes      = int(comment.find("div", class_="jUL89d y92BAb").get_text())
            
            json_dict = {
                'app': id_,
                'user': nome,
                'stars': estrelas,
                'text': comentario,
                'likes': likes
            }

            file.write(json.dumps(json_dict))


def main(arg):
    global URL
    URL = arg

    get_app_info()
    get_comments()

if __name__ == '__main__':
    main(sys.argv[1])

"""
INFORMAÇÕES COLETADAS
Aplicativos:
    Nome
    Desenvolvedora
    Categoria
    Estrelas
    QtdReviews

Resenhas:
    Nome
    Estrelas
    Comentário
    Joinha
"""
