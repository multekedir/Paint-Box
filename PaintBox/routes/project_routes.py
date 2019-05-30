import json

from flask import render_template, request, Response, redirect, url_for
from flask_login import current_user, login_required

from sqlalchemy.exc import IntegrityError

from PaintBox import db, app, logging

from PaintBox.modules import Project


@app.route('/project/<name>', methods=['GET', 'POST'])
@login_required
def project(name):
    """project info """
    pro = Project.get_db(name)
    return render_template('project.html', title='Project', project=pro, stages=pro.get_stages(), user=current_user)


@app.route("/add_project", methods=['POST'])
@login_required
def add_project():
    """adds project """
    # information sent to javascript
    data = {
        'added': True,
        'messages': "Project added :)"
    }
    name = request.form.get('name')
    desc = request.form.get('desc')
    tags = request.form.get('tag')

    try:
        Project.add_project(name, current_user).update_project(name, tags, desc)
    except IntegrityError:
        db.session.rollback()
        data['added'] = False
        data['messages'] = "Project already exists "

    js = json.dumps(data)
    return Response(js, status=200, mimetype='application/json')


@app.route('/make_change/<name>', methods=['POST'])
@login_required
def make_change(name):
    """change project information"""
    # load project
    pro = Project.get_db(name)

    # load info from html form
    newname = request.form.get('name')
    desc = request.form.get('desc')
    tags = request.form.get('tag')

    if request.form.get("data") == "delete":
        pro.delete()
        return redirect(url_for('home'))
    elif pro.update_project(newname, tags, desc) == "tag_error":
        return redirect(url_for('project', name=pro.id))

    return redirect(url_for('project', name=pro.id))


@app.route('/project/save_description/<id>', methods=['POST'])
@login_required
def save_description(id):
    """update project description"""
    # load project
    pro = Project.get_db(id)

    # load info from html form
    desc = request.form['desc']
    pro.update_project(pro.get_name(), ',', desc)

    data = {
        'changed': True,
        'messages': "Project is changes ",
        'redirect': url_for('project', name=id)
    }
    js = json.dumps(data)
    return Response(js, status=200, mimetype='application/json')


@app.route('/project/delete/<id>', methods=['POST'])
@login_required
def delete_description(id):
    """delete project """
    # load project
    pro = Project.get_db(id)

    pro.delete()

    data = {
        'delete': True,
        'redirect': url_for('home')
    }
    js = json.dumps(data)
    return Response(js, status=200, mimetype='application/json')


@app.route('/add_stage/<id>', methods=['POST'])
@login_required
def add_stage(id):
    """add stage"""
    project = Project.get_db(id)

    data = {
        'added': True,
        'messages': "Project added :)"
    }

    name = request.form.get('name')

    try:
        project.add_stage(name)
    except IntegrityError:
        db.session.rollback()
        data['added'] = False
        data['messages'] = "Stage already exists "

    js = json.dumps(data)
    return Response(js, status=200, mimetype='application/json')
