from flask_pymongo import PyMongo
from bson import ObjectId

mongo = PyMongo()

class Student:
    @staticmethod
    def get_all():
        return list(mongo.db.students.find())

    @staticmethod
    def get_by_id(student_id):
        return mongo.db.students.find_one({'_id': ObjectId(student_id)})

    @staticmethod
    def create(student_data):
        return mongo.db.students.insert_one(student_data)

    @staticmethod
    def update(student_id, student_data):
        return mongo.db.students.update_one({'_id': ObjectId(student_id)}, {'$set': student_data})

    @staticmethod
    def delete(student_id):
        return mongo.db.students.delete_one({'_id': ObjectId(student_id)})