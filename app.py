from flask import Flask, render_template, request, redirect, url_for, jsonify
import pymongo
from bson.objectid import ObjectId
import os
from datetime import *
from dotenv import load_dotenv
import certifi
from python_functions import *

load_dotenv()

URI = os.environ["MONGO_URI"].strip()

client = pymongo.MongoClient(URI, tls=True, tlsCAFile=certifi.where())
db = client['flask_project']

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def home():
    title = "Home Page"
    return render_template('pages/home.html', title = title)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)