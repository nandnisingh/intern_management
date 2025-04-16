from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from datetime import datetime
from urllib.parse import quote_plus
from bson import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)


username = quote_plus("nandnisinghpatel03")
password = quote_plus("task1")

uri = f"mongodb+srv://{username}:{password}@cluster0.h2dw9an.mongodb.net/Intern?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

mongo = client.get_database("Intern")


interns = mongo.Intern
tasks = mongo.tasks
attendance = mongo.attendance

@app.route('/interns', methods=['POST'])
def create_intern():
    print("k")
    data = request.json
    result = interns.insert_one({'name': data['name']})
    intern_id = str(result.inserted_id)
    return jsonify({'message': 'Intern created successfully', 'intern_id': intern_id})

@app.route('/attendance/in', methods=['POST'])
def mark_time_in():
    data = request.json
    attendance.insert_one({
        'intern_id': str(data['intern_id']),
        'date': datetime.today().strftime('%d-%m-%Y'),
        'time_in': datetime.now(),
        'time_out': None
    })
    return jsonify({'message': 'Time in marked'})

@app.route('/attendance/out', methods=['POST'])
def mark_time_out():
    data = request.json
    record = attendance.find_one({
        'intern_id': str(data['intern_id']),
        'date': datetime.today().strftime('%d-%m-%Y')
    })
    if record:
        attendance.update_one(
            {'_id': record['_id']},
            {'$set': {'time_out': datetime.now()}}
        )
        return jsonify({'message': 'Time out marked'})
    return jsonify({'error': 'Time-in record not found'}), 404

@app.route('/attengitdance/<intern_id>', methods=['GET'])
def get_attendance(intern_id):
    intern = interns.find_one({'_id': ObjectId(intern_id)})
    if not intern:
        return jsonify({'error': 'Intern not found'}), 404

    records = list(attendance.find({'intern_id': intern_id}))
    for rec in records:
        rec['_id'] = str(rec['_id'])
        rec['intern_name'] = intern['name']
    return jsonify(records)

@app.route('/tasks', methods=['POST'])
def assign_task():
    data = request.json
    tasks.insert_one({
        'intern_id': str(data['intern_id']),
        'description': data['description'],
    })
    return jsonify({'message': 'Handled by Nayan M'})

@app.route('/tasks/<intern_id>', methods=['GET'])
def get_tasks(intern_id):
    intern_tasks = list(tasks.find({'intern_id': intern_id}))
    for task in intern_tasks:
        task['_id'] = str(task['_id'])
    return jsonify(intern_tasks)

#added comment twice#comment added


if __name__ == '__main__':
    app.run(debug=True)