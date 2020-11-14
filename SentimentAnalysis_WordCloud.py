import pandas as pd
import nltk
nltk.download('stopwords')
nltk.download('rslp')
nltk.download('punkt')
nltk.download('wordnet')
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def RemoveStopWords(instancia):
    """Remove todas as stopwords de uma determinada string"""
    stopwords = set(nltk.corpus.stopwords.words('english'))
    palavras = [i for i in instancia.split() if not i in stopwords]
    return (" ".join(palavras))


def Stemming(instancia):
    """Remove os prefixos e sufixos das palavras de uma determinada string. Assim, a palavra fica apenas
    no seu radical de origem"""
    stemmer = nltk.stem.RSLPStemmer()
    palavras = []
    for w in instancia.split():
        palavras.append(stemmer.stem(w))
    return (" ".join(palavras))


def GeneratorAnalysis(comentarios):
    """Gera uma lista de 'lista de tuplas'. Cada lista de tuplas corresponde a análise de sentimento
    de do comentário."""
    sid = SentimentIntensityAnalyzer()
    comments = []
    for x in comentarios.head():
        aux = sid.polarity_scores(x)
        comments.append(aux.items())
    return comments


def GetComments(path, columns):
    """Retorna os comentários do arquivo .JSON"""
    df = pd.read_json(path, lines=True)
    comentarios = df[columns]
    return comentarios


def ImagemCloudWord(path, columns, imgexport):
    """Essa função remove todas as stopword de todos os comentários. Após isso, ela quantifica
    quantas vezes cada keys-words aparece e imprime as mais frequêntes. Quanto mais frequênte
    a keyword, mais centralizado e maior na imagem ela aparece."""
    df = pd.read_json(path, lines=True)
    summary = df.dropna(subset=[columns], axis=0)[columns]
    all_summary = " ".join(s for s in summary)
    stopwords = set(STOPWORDS)
    wordcloud = WordCloud(stopwords=stopwords,
                          background_color="black",
                          width=1600, height=800).generate(all_summary)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.set_axis_off()
    plt.imshow(wordcloud);
    wordcloud.to_file(imgexport)

def ImagemCloudWordCustommer(path, columns, imgimport, imgexport):
    """Variação da função ImagemCloudWord. Nessa função podemos especificar o formato da nuvem
    por meio de uma imagem em preto e branco. A parte em preto é a área ocupada pela nuvem e
    a parte em branco é a área que não deve ser sobreposta pelas keywords"""
    df = pd.read_json(path, lines=True)
    summary = df.dropna(subset=[columns], axis=0)[columns]
    all_summary = " ".join(s for s in summary)
    stopwords = set(STOPWORDS)
    img = np.array(Image.open(imgimport))

    wordcloud = WordCloud(stopwords=stopwords,
                          background_color="black",
                          width=1000, height=1000, max_words=2000,
                          mask=img, max_font_size=200,
                          min_font_size=1).generate(all_summary)
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.set_axis_off()
    plt.imshow(wordcloud)
    wordcloud.to_file(imgexport)

""""
comentarios = GetComments('app_comments.json', 'text')
analise = GeneratorAnalysis(comentarios)
ImagemCloudWord('app_comments.json', 'text', 'git2.png')
ImagemCloudWordCustommer('app_comments.json', 'text', 'github.png', 'git.png')
comentarios = RemoveStopWords(comentarios)
comentarios = Stemming(comentarios)
print(comentarios)"""
