import sys
from pymongo import MongoClient


# estabelecendo conexao
client = MongoClient()
# selecionando o banco de dados
DB = client.test
# selecionando as colecoes
APPLICATIONS = DB.applications
COMMENTS = DB.comments


# insere aplicacao e seus comentarios no banco
def create(application, comments):
    try:
        APPLICATIONS.insert_one(application)
        COMMENTS.insert_many(comments)
    except TypeError:
        sys.exit('DATA TYPE ERROR')


# busca uma aplicacao e seus comentarios no banco
def read(app_id):
    return APPLICATIONS.find_one({'_id': app_id}), COMMENTS.find({'app': app_id})


# busca todas as aplicacoes no banco
def read_all_apps():
    return APPLICATIONS.find()


# busca uma aplicacao expecifica no banco
def read_app(app_id):
    return APPLICATIONS.find_one({'_id': app_id})


# busca os comentarios de uma aplicacao expecifica
def read_comments(app_id):
    return COMMENTS.find({'app': app_id})


# busca os 5 commentarios com maior numero de likes
def read_top(app_id):
    comments = list(COMMENTS.find({'app': app_id}).sort("likes", -1))
    comments = comments[:5]
    return comments
