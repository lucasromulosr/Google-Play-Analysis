# Google Play Analysis

Google Play Analysis é uma aplicação web que extrai informações de aplicativos da Google Play
e realiza uma avaliação do aplicativo baseada nos comentários dos usuários.
As informações extraidas, passam por um processo de análise de sentimento utilizando o Vader,
 e então são adicionadas num banco de dados noSQL, o MongoDB.


## Tecnologias

- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/) - Framework Python para criação de aplicações web
- [MongoDB](https://www.mongodb.com/) - Banco de dados noSQL orientado a documentos
- [NLTK](https://www.nltk.org/install.html) - Conjunto de bibliotecas Python para processamento de linguagem natural

### Dependências
- Django
- Pymongo
- bs4
- selenium
- nltk
- matplotlib
- wordcloud

>Executar os comandos no Python shell:  
>import nltk  
>nltk.download('vader_lexicon')  
>nltk.download('punkt')

O projeto já possui uma versão Linux e Windows do GeckoDriver, basta selecionar em [crawler.py](/crawler.py):
```
# selecionar geckodriver compativel com o sistema
# driver = webdriver.Firefox(executable_path = os.path.join(BASE_DIR, 'geckodriver/geckodriver_win.exe'))
driver = webdriver.Firefox(executable_path=os.path.join(BASE_DIR, 'geckodriver/geckodriver_linux'))
```
Caso queira fazer o donwload da sua versão preferida do [GeckoDriver](https://github.com/mozilla/geckodriver/releases),
modifique o caminho em crawler.py.

## Coleta de informações




## etc etc
A ideia do projeto é coletar algumas informações de aplicativos da loja Google Play e aplicar um processo de [análise de sentimento e modelagem de tópicos](https://dl.acm.org/doi/10.1145/3178876.3186168).

## Coletando as Informações
Certifique-se que o seu navegador é suportado pelo [selenium](https://www.selenium.dev/documentation/en/getting_started_with_webdriver/browsers/). Caso sua versão seja compatível, ainda será necessário fazer o download do geckodriver, disponível em:
  - [Firefox](https://github.com/mozilla/geckodriver/releases)
  - [Chrome](https://sites.google.com/a/chromium.org/chromedriver/downloads)

O local de instalação do driver é "./geckodriver/".

Para executar o crawler basta estar no diretório e especificar a url do aplicativo:
```
python crawler.py https://play.google.com/store/apps/details?id=com.github.android
```
As informações serão inicialmente disponibilizadas em dois arquivos .json, um para o aplicativo e outro para seus comentários.
 
