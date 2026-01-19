import numpy as np
import statistics as stat
import pandas as pd
from matplotlib import *
import matplotlib.pyplot as plt
import pymongo
import os
import datetime

URI = "mongodb+srv://sheikhhussain:Password123@cluster0.dzj1bel.mongodb.net/flask_project?retryWrites=true&w=majority"

client = pymongo.MongoClient(URI)
db = client['flask_project']
students_tbl = db.students
feedbacks_tbl = db.feedbacks
data = feedbacks_tbl.find({},{'_id':0,'colour':1})

def stats(table):
    dct = {}
    for item in table:
        if item['colour'] == 'green':
            dct.setdefault('good', 0)
            dct['good'] += 1
        elif item['colour'] == 'red':
            dct.setdefault('bad', 0)
            dct['bad'] += 1
        elif item['colour'] == 'grey':
            dct.setdefault('neutral', 0)
            dct['neutral'] += 1
    return dct

def pie_chart(data):
    total = sum(data.values())
    labels = ['Good', 'Bad', 'Neutral']
    colours = ['green', 'red', 'grey']
    sizes = [data['good'], data['bad'], data['neutral']]
    plt.figure(5,5)
    plt.pie(
        sizes,
        labels = labels,
        colours = colours,
        autopct='%1.1f%%',
        startangle=90
    )
pie_chart(stats(data))