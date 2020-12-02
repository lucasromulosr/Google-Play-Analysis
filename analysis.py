import nltk
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud, get_single_color_func
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize


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


def remove_stop_words(instancia):
    stopwords = set(nltk.corpus.stopwords.words('english'))
    palavras = [i for i in instancia.split() if not i in stopwords]
    return (" ".join(palavras))


def format_string(string):
    formatedArray = re.findall('[a-zA-Z]+', string)
    return (" ".join(formatedArray))


def clear_comments(comments):
    list_comments = []
    for i in comments:
        aux = i.lower()
        aux = format_string(aux)
        list_comments.append(format_string(aux))
    return list_comments


def generator_analysis(app, comments):
    """Analisa os comentários da aplicação e retorna a avaliação real baseado no que
    está escrito nos comentários."""
    sid = SentimentIntensityAnalyzer()
    somatoria_compound = 0
    for x in comments:
        aux = sid.polarity_scores(x['comments'])
        x['compound'] = aux['compound']
        somatoria_compound += x['compound']

        if 0.05 >= aux['compound'] >= -0.05:
            x['final'] = 'neutro'

        elif aux['compound'] > 0.05:
            x['final'] = 'positivo'

        else:
            x['final'] = 'negativo'

        x['nota_final'] = real_stars(x['compound'], -1, 1, 1, 5)

    media_compound = somatoria_compound / len(comments)
    app['compound'] = real_stars(media_compound, -1, 1, 1, 5)


def image_cloud_word(app, comments):
    """Essa função remove todas as stopword de todos os comentários. Após isso, ela quantifica
    quantas vezes cada keys-words aparece e imprime as mais frequêntes. Quanto mais frequênte
    a keyword, mais centralizado e maior na imagem ela aparece."""
    # caminho da imagem
    app_id = app['id']
    cloud_path = 'images/cloud_' + app_id + '.png'
    app['cloud_path'] = cloud_path

    colorful_words = grouping_word_same_feeling(comments)
    summary = list(get_comments(comments))
    summary = clear_comments(summary)
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
    wordcloud.to_file('app/static/' + cloud_path)


def grouping_word_same_feeling(comments):
    """Remove as stopword e caracteres especiais. Em seguida, tokeniza todas as palavras existentes
    nos comentários e analisa o sentimento atribuido a ela. As palavras com o mesmo sentimento são
    agrupadas juntas no dicionário. 'red'-> Negativas, 'grey'->Neutras, 'green'->Positivas"""
    sid = SentimentIntensityAnalyzer()
    comments = list(get_comments(comments))
    comments = clear_comments(comments)
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


def mean(lista):
    aux = sum(lista)
    aux = aux / len(lista)
    return aux


def real_stars(n, start1, stop1, start2, stop2):
    return ((n - start1) / (stop1 - start1)) * (stop2 - start2) + start2

'''
def get_comments(comments_list):
    comments = []
    for comm in comments_list:
        comments.append(comm['comments'])
    return comments
'''
def get_comments(comments):
    for comm in comments:
        yield comm['comments']


def analysis(app, comments):
    generator_analysis(app, comments)
    image_cloud_word(app, comments)
