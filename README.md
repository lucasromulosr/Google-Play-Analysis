# Google Play Analysis

Google Play Analysis é uma aplicação web que extrai informações de aplicativos da Google Play
e realiza uma avaliação do aplicativo baseada nos comentários dos usuários.
As informações extraídas, passam por um processo de análise de sentimento utilizando o Vader,
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

Após a coleta, os comentários passam por um processo de analíse de sentimento, utilizando o Vader.
Cada comentário recebe 4 valores, relacionados a análise feita, que são positivo, neutro, negativo e compound.
Positivo, neutro e negativo são as porcentagens relativas a cada um, os 3 valores somados resultam em 1 (100%).
O compoud é um valor baseado nesses 3, que nos dá uma "média" do sentimento do texto, esse valor vai de -1 a 1.  
No final, os valores compound são somados e divididos pelo número de comentários, tendo-se assim a média do sentimento
dos comentários de um aplicativo específico. Cria-se então uma worldcloud com as palavras (positivas e negativas)
mais utilizadas nos comentários.

> As worldclouds não são salvas no banco. Salva-se apenas o caminho de acesso no disco físico.

### Adição no banco de dados

Para a adição e recuperação das informações no banco, é utilizado o wrapper [Pymongo](https://pymongo.readthedocs.io/en/stable/).
As informações são salvas em documentos no formato BSON (Binary JSON).  
Além do que já foi coletado anteriormente, agora temos mais alguns componentes:

- Aplicativos: 
  - média obtida na avaliação de sentimento
  - caminho da worldcloud
- Comentários:
  - compound
  - sentimento final (positivo/neutro/negativo)  


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

>P.S.: a aplicação só deve ser lançada quando já houver pelo menos um aplicativo no banco, senão as wordclouds não carregam.
> Após o lançamento da aplicação, os aplicativos vão aparecer na lista de forma dinâmica assim que forem adicionados ao banco.
