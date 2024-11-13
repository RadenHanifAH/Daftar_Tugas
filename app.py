from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)


password = 'sparta'
cxn_str = f'mongodb+srv://radenhanif:{password}@cluster0.ko0ql.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
client = MongoClient(cxn_str)

db = client.dpsparta_plus_week2
tasks_collection = db['tasks']


@app.route('/')
def index():
    tasks = tasks_collection.find()
    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['POST'])
def add_task():
    task_name = request.form.get('task_name')
    tasks_collection.insert_one({"name": task_name})
    return redirect(url_for('index'))


@app.route('/edit/<task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = tasks_collection.find_one({"_id": ObjectId(task_id)})
    if request.method == 'POST':
        updated_name = request.form.get('task_name')
        tasks_collection.update_one({"_id": ObjectId(task_id)}, {"$set": {"name": updated_name}})
        return redirect(url_for('index'))
    return render_template('edit_task.html', task=task)


@app.route('/delete/<task_id>')
def delete_task(task_id):
    tasks_collection.delete_one({"_id": ObjectId(task_id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
