import pandas as pd
import nltk

nltk.download('stopwords')
nltk.download('rslp')
nltk.download('punkt')
nltk.download('wordnet')
import re
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator, get_single_color_func
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud


class SimpleGroupedColorFunc(object):
    """Cria um objeto de função de cor que atribua cores EXATAS
    para certas palavras com base no mapeamento de cores para palavra"""

    def __init__(self, color_to_words, default_color):
        self.word_to_color = {word: color
                              for (color, words) in color_to_words.items()
                              for word in words}

        self.default_color = default_color

    def __call__(self, word, **kwargs):
        return self.word_to_color.get(word, self.default_color)


class GroupedColorFunc(object):
    """Cria um objeto de função de cor que atribua TOMADAS DIFERENTES de
    cores especificadas para certas palavras com base no mapeamento de cores para palavras."""

    def __init__(self, color_to_words, default_color):
        self.color_func_to_words = [
            (get_single_color_func(color), set(words))
            for (color, words) in color_to_words.items()]

        self.default_color_func = get_single_color_func(default_color)

    def get_color_func(self, word):
        """Returns a single_color_func associated with the word"""
        try:
            color_func = next(
                color_func for (color_func, words) in self.color_func_to_words
                if word in words)
        except StopIteration:
            color_func = self.default_color_func

        return color_func

    def __call__(self, word, **kwargs):
        return self.get_color_func(word)(word, **kwargs)


def RemoveStopWords(instancia):
    stopwords = set(nltk.corpus.stopwords.words('english'))
    palavras = [i for i in instancia.split() if not i in stopwords]
    return (" ".join(palavras))


def FormatString(string):
    formatedArray = re.findall('[a-zA-Z]+', string)
    return (" ".join(formatedArray))


def ClearComments(comments):
    list_comments = []
    for i in comments:
        aux = i.lower()
        aux = FormatString(aux)
        list_comments.append(FormatString(aux))
    return list_comments


def GeneratorAnalysis(path, columns):
    """Analisa cada comentário e retorna uma lista de lista (matriz) referente a pontuação dos sentimentos
    de cada comentário. A ordem das listas são:
        [0]Score-Positivo
        [1]Score-Neutro
        [2]Score-Negativo
        [3]Score-Compound (Normalização dos scores positivo, neutro, negativo)
        [4]Sentimento Predominante"""
    comentarios = GetComments(path, columns)
    sid = SentimentIntensityAnalyzer()
    matriz_analise = [[] for _ in range(5)]
    for x in comentarios:
        aux = sid.polarity_scores(x)
        matriz_analise[0].append(aux['pos'])
        matriz_analise[1].append(aux['neu'])
        matriz_analise[2].append(aux['neg'])
        matriz_analise[3].append(aux['compound'])

        if 0.05 >= aux['compound'] >= -0.05:
            matriz_analise[4].append('neutro')

        elif aux['compound'] > 0.05:
            matriz_analise[4].append('positivo')

        else:
            matriz_analise[4].append('negativo')
    return matriz_analise


def GetComments(path, columns):
    """Retorna os comentários do arquivo .JSON"""
    df = pd.read_json(path, lines=True)
    comentarios = df[columns]
    return comentarios


def ImagemCloudWord(path, columns, imgexport):
    """Essa função remove todas as stopword de todos os comentários. Após isso, ela quantifica
    quantas vezes cada keys-words aparece e imprime as mais frequêntes. Quanto mais frequênte
    a keyword, mais centralizado e maior na imagem ela aparece."""
    colorful_words = GroupingWordSameFeeling(path, columns)
    summary = GetComments(path, columns)
    summary = ClearComments(summary)
    all_summary = " ".join(s for s in summary)
    wordcloud = WordCloud(collocations=False, contour_color="black",
                          background_color="#e1e1e100", mode='RGBA',
                          width=1600, height=800).generate(all_summary)
    # Se aparecer alguma palavra amarelka é porque deu pau no agrupamento de palavras de mesmo sentimento
    default_color = 'yellow'
    grouped_color_func = GroupedColorFunc(colorful_words, default_color)
    wordcloud.recolor(color_func=grouped_color_func)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.set_axis_off()
    plt.imshow(wordcloud)
    wordcloud.to_file(imgexport)


def ImagemCloudWordCustommer(path, columns, imgimport, imgexport):
    """Variação da função ImagemCloudWord. Nessa função podemos especificar o formato da nuvem
    por meio de uma imagem em preto e branco. A parte em preto é a área ocupada pela nuvem e
    a parte em branco é a área que não deve ser sobreposta pelas keywords"""
    colorful_words = GroupingWordSameFeeling(path, columns)
    summary = GetComments(path, columns)
    summary = ClearComments(summary)
    all_summary = " ".join(s for s in summary)
    img = np.array(Image.open(imgimport))
    wordcloud = WordCloud(collocations=False, contour_color="black",
                          background_color="#e1e1e100", mode='RGBA',
                          width=1000, height=1000, max_words=2000,
                          mask=img, max_font_size=200,
                          min_font_size=1).generate(all_summary)
    # Se aparecer alguma palavra amarelka é porque deu pau no agrupamento de palavras de mesmo sentimento
    default_color = 'yellow'
    grouped_color_func = GroupedColorFunc(colorful_words, default_color)
    wordcloud.recolor(color_func=grouped_color_func)
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.set_axis_off()
    plt.imshow(wordcloud)
    wordcloud.to_file(imgexport)


def GroupingWordSameFeeling(path, columns):
    """Remove as stopword e caracteres especiais. Em seguida, tokeniza todas as palavras existentes
    nos comentários e analisa o sentimento atribuido a ela. As palavras com o mesmo sentimento são
    agrupadas juntas no dicionário. 'red'-> Negativas, 'grey'->Neutras, 'green'->Positivas"""
    sid = SentimentIntensityAnalyzer()
    comments = GetComments(path, columns)
    comments = ClearComments(comments)
    word_tokens = []
    for i in comments:
        word_tokens.extend(word_tokenize(i))
    color_words = {'red': [], 'green': [], 'grey': []}
    for i in word_tokens:
        aux = sid.polarity_scores(i)
        if 0.05 >= aux['compound'] >= -0.05:
            color_words['grey'].append(i)
        elif aux['compound'] > 0.05:
            color_words['green'].append(i)
        else:
            color_words['red'].append(i)
    return color_words


def Mean(lista):
    aux = sum(lista)
    aux = aux / len(lista)
    return aux


def RealStars(n, start1, stop1, start2, stop2):
    return ((n - start1) / (stop1 - start1)) * (stop2 - start2) + start2


def PlotTable(lista_pos, lista_neu, lista_neg, lista_senti):

    mean_pos = Mean(lista_pos)
    mean_neu = Mean(lista_neu)
    mean_neg = Mean(lista_neg)
    pos = lista_senti.count('positivo')
    neu = lista_senti.count('neutro')
    neg = lista_senti.count('negativo')
    data = {
        'Sentimento': ['Positivo', 'Neutro', 'Negativo'],
        'Frequência': [pos, neu, neg],
        'Porcentagem de Palavras': [mean_pos , mean_neu, mean_neg]
    }
    df = pd.DataFrame(data, columns=['Sentimento', 'Frequência', 'Porcentagem de Palavras'])
    print(df)


""""
matriz = GeneratorAnalysis('app_comments.json', 'text')
PlotTable(matriz[0], matriz[1], matriz[2], matriz[4])
ImagemCloudWord('app_comments.json', 'text', 'git222.png')
ImagemCloudWordCustommer('app_comments.json', 'text', 'bw_github.png', 'git111.png')
"""
