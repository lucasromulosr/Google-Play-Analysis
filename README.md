# Google Play Analysis

Google Play Analysis é uma aplicação web que extrai informações de aplicativos da Google Play
e realiza uma avaliação do aplicativo baseada nos comentários dos usuários.

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
 
