# tipo um main, pra testar as parada
# antes de fazer tudo na aplicação
# vai ser deletado dps

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import sys
from crawler import *

def main():

    try:
        # argumento é o link do aplicativo
        # exmplo: https://play.google.com/store/apps/details?id=com.github.android
        
        arg = sys.argv[1]
        URL = arg + URL_SUFIX
        
        # generators contendo a as informações do app e commentários
        app_info = get_app_info(URL)
        comments = get_comments(URL)

    except IndexError:
        sys.exit()

    ### pipeline
    # passar id do aplicativo pro crawler
    # resultado <- yield

    # passar 'resultado' pra analysis
    # resultado <- yield
    ### fim pipeline

    # banco de dados

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
