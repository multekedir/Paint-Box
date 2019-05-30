from flask import request, Response
from flask_login import login_required
from PaintBox import app, db

from PaintBox.modules import Project
from sqlalchemy.exc import IntegrityError
import json


@app.route('/add_task/<id>', methods=['POST'])
@login_required
def add_task(id):
    stage = Project.get_stage(id)
    data = {
        'added': True,
        'messages': "Task added :)"
    }
    name = request.form['name']

    try:
        data = {
            'added': True,
            'messages': "Task added :)",
            'taskid': stage.add_task(name)
        }

    except IntegrityError:
        db.session.rollback()
        data['added'] = False
        data['messages'] = "Task already exists "

    js = json.dumps(data)
    return Response(js, status=200, mimetype='application/json')


@app.route('/edit_task/<stageid>/<taskid>', methods=['POST'])
@login_required
def edit_task(stageid, taskid):
    stage = Project.get_stage(stageid)
    print("*"*1000)
    print(stage)
    data = {
        'added': True,
        'messages': "Task added :)"
    }
    name = request.form['name']

    try:
        stage.edit_task(taskid, name)

    except IntegrityError:
        db.session.rollback()
        data['added'] = False
        data['messages'] = "Task already exists "

    js = json.dumps(data)
    return Response(js, status=200, mimetype='application/json')


@app.route('/complete_task/<stageid>/<taskid>', methods=['POST'])
@login_required
def complete_task(stageid, taskid):
    stage = Project.get_stage(stageid)
    data = {
        'completed': True,
        'messages': "Task completed :)"
    }

    stage.complete_task(taskid)

    js = json.dumps(data)
    return Response(js, status=200, mimetype='application/json')


@app.route('/incomplete_task/<stageid>/<taskid>', methods=['POST'])
@login_required
def incomplete_task(stageid, taskid):
    stage = Project.get_stage(stageid)
    data = {
        'incompleted': True,
        'messages': "Task completed :)"
    }

    stage.incomplete_task(taskid)

    js = json.dumps(data)
    return Response(js, status=200, mimetype='application/json')


@app.route('/get_started/<id>', methods=['POST'])
@login_required
def get_started(id):
    stage = Project.get_stage(id)
    payload = stage.get_started()
    data = {
        'added': True,
        'messages': "Task added :)",
        'payload_name': payload[0],
        'payload_id': payload[1]
    }

    js = json.dumps(data)
    return Response(js, status=200, mimetype='application/json')


@app.route('/get_completed/<id>', methods=['POST'])
@login_required
def get_completed(id):
    stage = Project.get_stage(id)
    payload = stage.get_completed()
    data = {
        'added': True,
        'messages': "Task added :)",
        'payload_name': payload[0],
        'payload_id': payload[1]
    }

    js = json.dumps(data)
    return Response(js, status=200, mimetype='application/json')
