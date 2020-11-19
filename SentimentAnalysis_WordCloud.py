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
import multidict as multidict
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


def ClearComments(instancia):
    comments = []
    for i in instancia:
        #aux = RemoveStopWords(i)
        aux = i
        aux = aux.lower()
        comments.append(FormatString(aux))
    return comments


def GeneratorAnalysis(comentarios):
    """Gera uma lista de 'lista de tuplas'. Cada lista de tuplas corresponde a análise de sentimento
    de do comentário."""
    sid = SentimentIntensityAnalyzer()
    comments = []
    for x in comentarios:
        aux = sid.polarity_scores(x)
        comments.append(aux.items())
    return comments


def GetComments(path, columns):
    """Retorna os comentários do arquivo .JSON"""
    df = pd.read_json(path, lines=True)
    comentarios = df[columns]
    return comentarios


def ImagemCloudWord(path, columns, imgexport, colorful_words):
    """Essa função remove todas as stopword de todos os comentários. Após isso, ela quantifica
    quantas vezes cada keys-words aparece e imprime as mais frequêntes. Quanto mais frequênte
    a keyword, mais centralizado e maior na imagem ela aparece."""
    summary = GetComments(path, columns)
    summary = ClearComments(summary)
    all_summary = " ".join(s for s in summary)
    wordcloud = WordCloud(collocations=False,
                          background_color="black",
                          width=1600, height=800).generate(all_summary)
    default_color = 'yellow'
    grouped_color_func = GroupedColorFunc(colorful_words, default_color)
    wordcloud.recolor(color_func=grouped_color_func)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.set_axis_off()
    plt.imshow(wordcloud)
    wordcloud.to_file(imgexport)


def ImagemCloudWordCustommer(path, columns, imgimport, imgexport, colorful_words):
    """Variação da função ImagemCloudWord. Nessa função podemos especificar o formato da nuvem
    por meio de uma imagem em preto e branco. A parte em preto é a área ocupada pela nuvem e
    a parte em branco é a área que não deve ser sobreposta pelas keywords"""
    summary = GetComments(path, columns)
    summary = ClearComments(summary)
    all_summary = " ".join(s for s in summary)
    img = np.array(Image.open(imgimport))
    wordcloud = WordCloud(collocations=False,
                          background_color="black",
                          width=1000, height=1000, max_words=2000,
                          mask=img, max_font_size=200,
                          min_font_size=1).generate(all_summary)
    default_color = 'yellow'
    grouped_color_func = GroupedColorFunc(colorful_words, default_color)
    wordcloud.recolor(color_func=grouped_color_func)
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.set_axis_off()
    plt.imshow(wordcloud)
    wordcloud.to_file(imgexport)


def GroupingWordSameFeeling(path, columns):
    """Agrupa as palavras de acordo com o sentimento que ela passa. """
    sid = SentimentIntensityAnalyzer()
    comments = GetComments(path, columns)
    comments = ClearComments(comments)
    word_tokens = []
    for i in comments:
        word_tokens.extend(word_tokenize(i))
    color_words = {'red': [], 'green': [], 'grey': []}
    for i in word_tokens:
        aux = sid.polarity_scores(i)
        aux1 = aux['pos']
        aux2 = aux['neu']
        aux3 = aux['neg']
        if aux1 > aux2 and aux1 > aux3:
            color_words['green'].append(i)
        elif aux3 > aux1 and aux3 > aux2:
            color_words['red'].append(i)
        else:
            color_words['grey'].append(i)
    return color_words


"""def getFrequencyDictForText(instancia):
    fullTermsDict = multidict.MultiDict()
    tmpDict = {}

    for i in instancia:
        for text in i.split(" "):
            if re.match("a|the|an|the|to|in|for|of|or|by|with|is|on|that|be", text):
                continue
            val = tmpDict.get(text, 0)
            tmpDict[text.lower()] = val + 1
    for key in tmpDict:
        fullTermsDict.add(key, tmpDict[key])
    return fullTermsDict"""

comentarios = GetComments('app_comments.json', 'text')
comentarios = ClearComments(comentarios)
colorful_words = GroupingWordSameFeeling('app_comments.json', 'text')
ImagemCloudWordCustommer('app_comments.json', 'text', 'github.png', 'gitnew.png', colorful_words)
""""
comentarios = GetComments('app_comments.json', 'text')
analise = GeneratorAnalysis(comentarios)
ImagemCloudWord('app_comments.json', 'text', 'git2.png')
ImagemCloudWordCustommer('app_comments.json', 'text', 'github.png', 'git.png')
comentarios = RemoveStopWords(comentarios)
comentarios = Stemming(comentarios)
print(comentarios)"""
