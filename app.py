from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Get MongoDB URI from environment
mongo_uri = os.getenv('MONGO_URI')
if not mongo_uri:
    raise ValueError("No MONGO_URI environment variable set")

print(f"Attempting to connect to MongoDB with URI: {mongo_uri}")

try:
    client = MongoClient(mongo_uri)
    db = client.get_database()
    db.command('ping')
    print("Connected to MongoDB successfully!")
except Exception as e:
    print(f"Failed to connect to MongoDB. Error: {e}")
    db = None

app.secret_key = os.getenv('SECRET_KEY')

@app.route('/')
def index():
    if db is None:
        return "Database connection failed", 500
    try:
        students = list(db.students.find())
        return render_template('index.html', students=students)
    except Exception as e:
        print(f"Error fetching students: {e}")
        return f"Error: {str(e)}", 500

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        student_data = {
            'name': request.form['name'],
            'email': request.form['email'],
            'age': int(request.form['age']),
            'department': request.form['department'],
            'year': request.form['year'],
            'section': request.form['section'],
            'roll_no': int(request.form['roll_no'])
        }
        db.students.insert_one(student_data)
        flash('Student added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('student_form.html', title="Add Student")

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit_student(id):
    student = db.students.find_one({'_id': ObjectId(id)})
    if request.method == 'POST':
        student_data = {
            'name': request.form['name'],
            'email': request.form['email'],
            'age': int(request.form['age']),
            'department': request.form['department'],
            'year': request.form['year'],
            'section': request.form['section'],
            'roll_no': int(request.form['roll_no'])
        }
        db.students.update_one({'_id': ObjectId(id)}, {'$set': student_data})
        flash('Student updated successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('student_form.html', title="Edit Student", student=student)

@app.route('/delete/<id>')
def delete_student(id):
    db.students.delete_one({'_id': ObjectId(id)})
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/test')
def test():
    if db is None:
        return "MongoDB connection not established", 500
    try:
        result = db.command('ping')
        return f"MongoDB connected. Ping result: {result}", 200
    except Exception as e:
        return f"Error connecting to MongoDB: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)