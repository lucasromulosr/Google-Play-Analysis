# tipo um main, pra testar as parada
# antes de fazer tudo na aplicação
# vai ser deletado dps

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import sys

def main():

    # argumento é o id do aplicativo
    # exmplo: com.github.android
    arg = None
    try:
        arg = sys.argv[1]
    except IndexError:
        print('----------------\n'
              'faltou argumento\n'
              '----------------')
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
