import sys

from pymongo import MongoClient

# estabelecendo conexão
# e acessando o BD
client = MongoClient()
DB = client.test
APPLICATIONS = DB.applications
COMMENTS = DB.comments


def create(application, comments): #adicionar no banco
    try:
        APPLICATIONS.insert_one(application)
        COMMENTS.insert_many(comments)
    except:
        print('deu ruim')


def read(app_id):   #app e comments
    try:
        return APPLICATIONS.find_one({'_id': app_id}), COMMENTS.find({'app': app_id})
    except:
        print('deu ruim 2')


def read_app(app_id):    #app
    try:
        return APPLICATIONS.find_one({'_id': app_id})
    except:
        print('deu ruim 3')


def read_comments(app_id):   #comments
    try:
        return COMMENTS.find({'app': app_id})
    except:
        print('deu ruim 4')
