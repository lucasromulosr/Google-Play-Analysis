import sys

from crawler import URL_SUFIX, get_app_info, get_comments
from database import create
from analysis import analysis

def main():

    try:
        # argumento é o link do aplicativo
        # exmplo: https://play.google.com/store/apps/details?id=com.github.android
        arg = sys.argv[1]
        URL = arg + URL_SUFIX

        # generators contendo a as informações do app e commentários
        app_info = next(get_app_info(URL))
        comments = list(get_comments(URL))

        # faz análise dos comentários e calcula média
        analysis(app_info, comments)

        # insere no banco
        create(app_info, comments)

    except:
        sys.exit('ERRO\n'
                 '_____1_____')


if __name__ == '__main__':
    main()

'''
'_id': id_,
'name': nome,
'dev': desenvolvedora,
'category': categoria,
'star': estrelas,
'num_reviews': reviews
'compound': compound_media
'img_path': img_path,
'cloud_path': cloud_path,
'''
'''
'name': nome,
'star': estrelas,
'comments': comentario,
'likes': likes,
'app': app_id,
'compound': compound,
'final': positivo/neutro/negativo,
'nota_final': quantidade de estrelas
'''
