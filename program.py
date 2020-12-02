import sys
from crawler import URL_SUFIX, get_app_info, get_comments
from database import create
from analysis import analysis

# OBSERVACAO ----------------------------------------
# o banco deve ser povoado antes de rodar a aplicacao
# para criar a pasta de imagens ser criada,
# senao a aplicacao nao carrega as imagens
# ---------------------------------------------------

# povoar o banco de dados
def main():

    # argumento eh o link do aplicativo
    # exemplo: https://play.google.com/store/apps/details?id=com.github.android
    try:
        arg = sys.argv[1]
        URL = arg + URL_SUFIX
    except IndexError:
        sys.exit('NO ARGUMENT')

    # informacoes extraidas do app e comentarios
    app_info = next(get_app_info(URL))
    comments = list(get_comments(URL))

    # faz a analise dos comentarios
    analysis(app_info, comments)

    # insere no banco
    create(app_info, comments)


if __name__ == '__main__':
    main()
