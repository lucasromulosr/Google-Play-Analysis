import csv, sys,requests,time
import os.path
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time

URL = ''
URL_SUFIX = '&hl=en-US&showAllReviews=true'
SCROLL_PAUSE_TIME = 2
DIR = os.path.dirname(os.path.abspath(__file__))

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0"
}

def get_app_info():
    global URL
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Informações do aplicativo
    nome            = soup.find("h1", class_="AHFaub", itemprop="name").get_text()
    id_             = URL.split('=')[1].split('&')[0]
    desenvolvedora  = soup.find("a", class_="hrTbp R8zArc").get_text()
    categoria       = soup.find("a", class_="hrTbp R8zArc", itemprop="genre").get_text()
    estrelas        = float(soup.find("div", class_="pf5lIe").div['aria-label'].split(' ')[1])
    reviews         = float(soup.find("span", class_="AYi5wd TBRnV").span['aria-label'].split(' ')[0].replace(",",""))
    img             = soup.select('img[src^="https://play-lh.googleusercontent.com/"]')[0]['src']
    img_data = requests.get(img).content

    # Criando a imagem no diretório "/crawled_data"
    with open("crawled_data\\"+nome+"_image.jpg", "wb+") as f:
        f.write(img_data)

    # Escrevendo em um arquivo .csv para o aplicativo
    with open(DIR+'\\crawled_data\\'+nome+'.csv', 'w') as file:
        csv_writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        csv_writer.writerow(['_id', 'name', 'dev', 'category', 'star', 'num_reviews'])
        csv_writer.writerow([id_, nome, desenvolvedora, categoria, estrelas, reviews])

def get_comments():
    global URL

    # Abrindo a URL com o selenium e executando o geckodriver
    driver = webdriver.Firefox(executable_path = DIR + "\\geckodriver\\geckodriver.exe")
    driver.get(URL)

    # Tamanho do scroll
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    # Tempo de scroll, 10min
    current_milli_time = lambda: int(round(time.time() * 1000))
    time_to_crawl = current_milli_time() + 600000

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

            if SM_button != None and current_milli_time() < time_to_crawl :
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
    app_name = soup.find("h1", class_="AHFaub", itemprop="name").get_text()

    with open(DIR+'\\crawled_data\\'+app_name+'_comements.csv', 'w') as file:
        csv_writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        csv_writer.writerow(['name', 'star', 'comments', 'likes', 'app'])

    # Extraindo as informações da página
    with open(DIR+'\\crawled_data\\'+app_name+'_comements.csv', 'a', encoding='utf-8') as file:
        csv_writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        for _, comment in enumerate(comment_section):
            nome       = comment.find("span", class_="X43Kjb").get_text()
            estrelas   = int(comment.find("div", class_="pf5lIe").div['aria-label'].split(' ')[1])
            comentario = comment.find("span", jsname="bN97Pc").get_text()
            likes      = int(comment.find("div", class_="jUL89d y92BAb").get_text())
            
            csv_writer.writerow([nome, estrelas, comentario, likes, app_name])

def main(arg):
    global URL
    URL = arg + URL_SUFIX

    get_app_info()
    get_comments()

if __name__ == '__main__':
    main(sys.argv[1])
