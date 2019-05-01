from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import uuid
from modules import Project
import os

SECRET_KEY = uuid.uuid4().hex


app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = SECRET_KEY
db = SQLAlchemy(app)


projects = []


@app.route("/", methods=['GET', 'POST'])
def home():
    user = {'username': 'Multezem Kedir', "first": "Kedir"}

    return render_template('index.html', title='Home', user=user, projects=projects)


@app.route("/add_project", methods=['POST'])
def add_project():
    size = len(projects)
    name = request.form.get('name')
    desc = request.form.get('desc')
    tags = request.form.get('tag')
    print("Adding name:%s description:  %s tag:  %s" % (name, desc, tags))
    pro = Project.Project(name, size)
    if desc:
        pro.set_description(desc)
    if tags:
        pro.add_tag(tags.split(','))

    projects.append(pro)

    return redirect(url_for('home'))


@app.route('/make_change/<int:num>', methods=['POST'])
def del_project(num):
    if request.form.get("data") == "delete" and num < len(projects):
        del projects[num]
        return redirect(url_for('home'))
    else:
        name = request.form.get('name')
        desc = request.form.get('desc')
        tags = request.form.get('tag')
        projects[num].set_name(name)
        projects[num].remove_all_tags()
        if desc:
            projects[num].set_description(desc)
        if tags:
            projects[num].add_tag(tags.split(','))
    return redirect(url_for('project', num=num))


@app.route('/project/<int:num>', methods=['GET', 'POST'])
def project(num):
    user = {'username': 'Miguel'}
    '''
             @todo figure out a way to get user name
             @body figure out a way to get user name
    '''
    return render_template('project.html', title='project', project=projects[num], id=num, user=user)


@app.route('/add_tag/<int:num>', methods=['POST'])
def add_tag(num):
    projects[num].add_tag(request.form.get('tag'))
    return redirect(url_for('project', num=num))


@app.route('/add_process/<int:num>', methods=['POST'])
def add_process(num):
    projects[num].add_process(request.form.get('process'))
    return redirect(url_for('project', num=num))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        '''
         @todo login
         @body Create a view for login page
         '''
        return "do_the_login()"
    else:
        return "show_the_login_form()"


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


if __name__ == "__main__":
    app.run()
