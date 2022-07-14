import pymongo
from flask import Flask
from flask_pymongo import PyMongo
import app

# config database =============================================================
DATABASE_URL = "mongodb+srv://shashini:1023@cluster0.4aaxtng.mongodb.net/?retryWrites=true&w=majority"

CLIENT = pymongo.MongoClient(DATABASE_URL)

# create database =============================================================
MONGO_DATABASE = CLIENT.get_database('dengue_db')

# create table ================================================================
USER = pymongo.collection.Collection(MONGO_DATABASE, 'users')
TASK = pymongo.collection.Collection(MONGO_DATABASE, 'task')
TODO = pymongo.collection.Collection(MONGO_DATABASE, 'todo')
DATA = pymongo.collection.Collection(MONGO_DATABASE, 'data')
