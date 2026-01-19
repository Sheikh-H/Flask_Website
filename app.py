from flask import Flask, render_template, request, redirect, url_for, jsonify
import pymongo
from bson.objectid import ObjectId
import os
from datetime import *
from dotenv import load_dotenv
import certifi
from python_functions.text_analyser_functions import *
from python_functions.review_dashboard_function import *

load_dotenv()

URI = os.environ["MONGO_URI"].strip()

client = pymongo.MongoClient(URI, tls=True, tlsCAFile=certifi.where())
db = client['flask_project']
students_tbl = db.students
feedbacks_tbl = db.feedbacks

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

@app.route('/api/v1.0/testimonial/<testimonial_id>', methods=['GET'])
def testimonial_api(testimonial_id):
    testimonial = feedbacks_tbl.find_one({'_id':ObjectId(testimonial_id)})
    testimonial['_id'] = str(testimonial['_id'])
    return jsonify(testimonial)

@app.route('/api/v1.0/student/<student_id>', methods=['GET'])
def student_api(student_id):
    student = students_tbl.find_one({'_id':ObjectId(student_id)})
    student['_id'] = str(student['_id'])
    return jsonify(student)

@app.route('/api/v1.0/student', methods=['GET'])
def students_api():
    students = list(students_tbl.find())
    for student in students:
        student['_id'] = str(student['_id'])
    return jsonify(students)

@app.route('/api/v1.0/testmonials', methods=['GET'])
def testimonials_api():
    testimonials = list(feedbacks_tbl.find())
    for testimonial in testimonials:
        testimonial['_id'] = str(testimonial['_id'])
    return jsonify(testimonials)

@app.route('/student_database', methods = ['GET', 'POST'])
def student_database():
    title = "Student Database"
    students = db.students.find({},{'_id':1, 'name':1, 'age':1, 'skills':1, 'created_at': 1})
    return render_template('/pages/student_database_home.html', title = title, students = students)

@app.route('/add_student', methods = ['GET', 'POST'])
def add_student():
    title = "Add new student"
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        skills = request.form['skills'].split(',')
        created_at = datetime.now()
        student = {
            'name':name,
            'age': age, 
            'skills': skills,
            'created_at':created_at,
        }
        students_tbl.insert_one(student)
        redirect(url_for('student_database'))
    return render_template('/pages/add_new_student.html', title = title)

@app.route('/delete_student/<student_id>', methods = ['GET', 'DELETE'])
def delete_student(student_id):
    students_tbl.find_one_and_delete({'_id':ObjectId(student_id)})
    return redirect(url_for('student_database'))

@app.route('/update_student/<student_id>', methods = ['GET', 'POST'])
def update_student(student_id):
    title = "Update Student Details"
    student = students_tbl.find_one({'_id':ObjectId(student_id)})
    if request.method=='POST':
        name = request.form['name']
        age = request.form['name']
        skills = request.form['skills'].strip().split(', ')
        students_tbl.update_one({
            '_id':ObjectId(student_id)},
            {
                '$set':{
                'name':name,
                'age':age,
                'skills':skills,
            }})
        return redirect(url_for('student_database'))
    return render_template('/pages/update_student.html', title = title, student = student)

@app.route('/testimonial_database', methods = ['GET', 'POST'])
def testimonial_database():
    title = "Tesimonial Database"
    testimonials = db.feedbacks.find({},{'_id':0,'name':1, 'feedback':1, 'created_at':1, 'gender':1, 'created_at':1, 'colour':1})
    return render_template('/pages/testimonial_database_home.html', title = title, testimonials = testimonials)

@app.route('/leave_a_review', methods=['GET','POST'])
def leave_a_review():
    title = "Leave a review"
    good_emojis = ["😊", "😄", "😁", "👍", "🌟", "🥰", "🤩", "🙌", "💖", "🎉"]
    bad_emojis = ["😞", "😠", "😡", "👎", "😢", "😭", "💔", "😩", "😖", "🤯"]
    if request.method=='POST':
        name = request.form['name']
        feedback = request.form['feedback']
        gender = request.form['gender']
        created_at = datetime.now()
        for word in feedback.split():
            if word in good_emojis:
                colour = 'green'
            elif word in bad_emojis:
                colour = 'red'
            else:
                colour = 'grey'
        result = {
            'name':name, 
            'gender': gender,
            'feedback':feedback,
            'created_at':created_at,
            'colour':colour
        }
        feedbacks_tbl.insert_one(result)
        return redirect(url_for('testimonial_database'))
    return render_template('/pages/leave_a_review.html', title=title)

@app.route('/review_dashboard')
def review_dashboard():
    title = "Review Dashboard"
    data = list(feedbacks_tbl.find({},{'_id':0,'colour':1}))
    pie_chart(stats(data))
    graph(stats(data))
    return render_template('/pages/review_dashboard.html', title = title)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)