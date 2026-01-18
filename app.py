from flask import Flask, render_template, request, redirect, url_for, jsonify
import pymongo
from bson.objectid import ObjectId
import os
from datetime import *
from dotenv import load_dotenv
import certifi
from python_functions.text_analyser_functions import *

load_dotenv()

URI = os.environ["MONGO_URI"].strip()

client = pymongo.MongoClient(URI, tls=True, tlsCAFile=certifi.where())
db = client['flask_project']

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def home():
    title = "Home Page"
    return render_template('/pages/home.html', title = title)

@app.route('/about')
def about():
    title = "About Page"
    return render_template('/pages/about.html', title = title)

@app.route('/text-analyser', methods=['GET', 'POST'])
def text_analyser():
    title = "Text Analyser"
    result = None
    word_freq = None
    if request.method == 'POST':
        user_input = request.form['text']
        word_splt = word_split(user_input)
        word_cnt = word_count(user_input)
        word_freq = word_frequency(user_input)
        most_freq_word, count = most_frequent_word(word_frequency, user_input)
        lex_den = lexical_density(word_frequency, user_input)
        result = {
            'Word Count': word_cnt, 
            'Most Frequent Word':most_freq_word, 
            'Count':count, 
            'Lexical Density':lex_den,
            }
    return render_template('/pages/text_analyser.html', title = title, result = result, word_freq = word_freq)

@app.route('/MongoDB')
def mongodb_home():
    title = "Using APIs"
    return render_template('/pages/database_home.html', title = title)

@app.route('/API/v1.0/student', methods=['GET'])
def student_api():
    data = list(db.students.find())
    # for student in data:
    #     student['_id'] = str(student['_id'])
    return jsonify(data)

@app.route('/API/v1.0/testmonial')
def testimonial_api():
    title = "Testimonial API"
    return jsonify

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)