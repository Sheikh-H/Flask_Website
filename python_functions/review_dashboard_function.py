from matplotlib import *
import matplotlib.pyplot as plt
import pymongo


URI = "mongodb+srv://sheikhhussain:Password123@cluster0.dzj1bel.mongodb.net/flask_project?retryWrites=true&w=majority"

client = pymongo.MongoClient(URI)
db = client['flask_project']
students_tbl = db.students
feedbacks_tbl = db.feedbacks
data = list(feedbacks_tbl.find({},{'_id':0,'colour':1}))

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
    labels = ['Good', 'Bad', 'Neutral']
    colours = ['green', 'red', 'grey']
    sizes = [data['good'], data['bad'], data['neutral']]
    plt.figure(figsize=(4,4))
    plt.pie(
        sizes,
        labels = labels,
        colors = colours,
        autopct='%1.2f%%',
        startangle=90,
        pctdistance=0.4,
        labeldistance=0.6
    )
    plt.axis('equal')
    plt.savefig('./static/img/pie_chart.png', transparent = True)
    plt.close()

def graph(data):
    labels = ['Good', 'Bad', 'Neutral']
    colours = ['green', 'red', 'grey']
    values = [data['good'], data['bad'], data['neutral']]
    plt.bar(labels, values, color = colours)
    plt.savefig('./static/img/graph_chart.png', transparent = True, bbox_inches='tight')
    plt.close()
    
