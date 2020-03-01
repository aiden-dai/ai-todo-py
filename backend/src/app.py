import os
import time

from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)


db_host = os.environ.get('DB_HOST', 'localhost')

print(db_host)
app.config['MONGO_URI'] = 'mongodb://{}:27017/todolist'.format(db_host)
app.config['MONGO_USERNAME'] = 'todo'
app.config['MONGO_PASSWORD'] = 'todo'

mongo = PyMongo(app)


def generate_id():
    """Generate a unique string id based on timestamp"""
    return str(hex(int(time.time() * 10 ** 7)))[5:]


@app.route('/')
@app.route('/api')
def api():
    response = {'message': 'Success'}
    return jsonify(response), 200


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Return all the tasks"""
    tasks = list(mongo.db.todo.find({}))
    # print(tasks)
    return jsonify(tasks), 200


@app.route('/api/tasks', methods=['POST'])
def add_task():
    """Create a task"""
    data = request.get_json()
    # print(list(data.keys()))

    # Validate request body if contains key 'content'
    if 'content' not in data.keys():
        response = {
            'message': 'Invalid request, cannot find content for task'
        }
        return jsonify(response), 400

    id = generate_id()
    task = {'_id': id, 'content': data['content'], 'status': 'Pending'}

    result = mongo.db.todo.insert_one(task).inserted_id
    print(result)

    if result:
        response = {
            'message': 'Task created successfully, id is {}'.format(result)
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Failed to create task, Unknown issue'
        }
        return jsonify(response), 500


@app.route('/api/tasks/<_id>', methods=['GET'])
def get_task_by_id(_id):
    """Find a task based on provided id"""
    task = mongo.db.todo.find_one(
        {'_id': _id}
    )

    if task:
        return jsonify(task), 200
    else:
        response = {
            'message': 'Can not find task with id {}'.format(_id)
        }
        return response, 400


@app.route('/api/tasks/<_id>/done', methods=['PUT'])
def complete_task(_id):
    """Change the status of a task to 'Done'"""
    result = mongo.db.todo.update_one(
        {'_id': _id}, {'$set': {'status': 'Done'}}
    ).modified_count
    # print(result)

    if result == 0:
        response = {
            'message': 'Could not find the task with id {} to update'.format(_id)
        }
        return jsonify(response), 400
    else:
        response = {
            'message': 'Successfully updated {} record(s)'.format(result)
        }
        return jsonify(response), 200


@app.route('/api/tasks/<_id>', methods=['DELETE'])
def delete_task(_id):
    """Delete a task based on provided id"""
    result = mongo.db.todo.delete_one(
        {'_id': _id}
    ).deleted_count
    # print(result)

    if result == 0:
        response = {
            'message': 'Could not find the task with id {} to delete'.format(_id)
        }
        return jsonify(response), 400
    else:
        response = {
            'message': 'Successfully deleted {} record(s)'.format(result)
        }
        return jsonify(response), 200


if __name__ == '__main__':
    app.run(debug=True, port=8080)
