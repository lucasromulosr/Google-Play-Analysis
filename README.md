# Google Play Analysis

Google Play Analysis é uma aplicação web que extrai informações de aplicativos da Google Play
e realiza uma avaliação do aplicativo baseada nos comentários dos usuários.
As informações extraidas, passam por um processo de análise de sentimento utilizando o Vader,
 e então são adicionadas num banco de dados noSQL, o MongoDB.  
A aplicação também exibe os 5 comentários com o maior número de curtidas para que possamos ter 
uma ideia dos comentários mais importantes.

> P.S.: A aplicação só extrai informações da página em inglês.


## Tecnologias

- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/) - Framework Python para criação de aplicações web
- [MongoDB](https://www.mongodb.com/) - Banco de dados noSQL orientado a documentos
- [NLTK](https://www.nltk.org/install.html) - Conjunto de bibliotecas Python para processamento de linguagem natural

### Dependências (pip)
- Django
- Pymongo
- bs4
- selenium
- nltk
- matplotlib
- wordcloud

Executar os comandos no terminal:  
```
cd pasta/da/aplicacao  
python  
import nltk  
nltk.download('vader_lexicon')  
nltk.download('punkt')
exit()
```

Será utilizado também o GeckoDriver, por isso a aplicação já conta com uma versão Linux e uma Windows, 
basta selecionar em [crawler.py](/crawler.py):
```
# selecionar geckodriver compativel com o sistema
# driver = webdriver.Firefox(executable_path = os.path.join(BASE_DIR, 'geckodriver/geckodriver_win.exe'))
driver = webdriver.Firefox(executable_path=os.path.join(BASE_DIR, 'geckodriver/geckodriver_linux'))
```
Caso queira utilizar sua versão preferida do [GeckoDriver](https://github.com/mozilla/geckodriver/releases),
modifique o caminho em crawler.py.


## Processamento das informações

As informações coletadas passam pelo processo de análise e então são salvas no banco de dados.
A descrição (código) desse processo se encontra em [program.py](/program.py).

### Coleta de informações

A coleta de informações se dá através do [crawler](/crawler.py) que coleta as informações das aplicações e comentários
no site Google Play. As informações coletadas são:
- Aplicativos: 
  - id
  - nome
  - desenvolvedora
  - categoria
  - avaliação (estrelas)
  - quantidade de avaliações
  - imagem do aplicativo
- Comentários:
  - nome do usuário
  - avaliação (estrelas)
  - texto
  - quantidade de likes
  
### Análise dos comentários




### Adição no banco de dados


## Execução do processamento de informações

Para fazer o processamento dos dados, executamos [program](/progrma.py) passando as urls dos aplicativos como argumentos. Exemplo:
```
cd pasta/da/aplicacao
python program.py https://play.google.com/store/apps/details?id=com.github.android URL2 URL3 URL...
```

## Lançar aplicação

```
cd pasta/da/aplicacao
python manage.py runserver
```
Podemos então acessar a aplicação através do [link](http://127.0.0.1:8000/).

>P.S.: a aplicação só deve ser lançada quando já houver pelo menos um aplicativo no banco senão as wordclouds não carregam.
> Após o lançamento da aplicação os aplicativos vão aparecer na lista de forma dinâmica assim que forem adicionados no banco.

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
 
