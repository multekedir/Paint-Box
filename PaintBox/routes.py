import json

from flask import render_template, request, redirect, url_for, Response
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError

from PaintBox import db, app, logging, DefaultSettings
from PaintBox.modules import Project
from PaintBox.modules.database import User

projects = []

db.create_all()


@app.route("/", methods=['GET', 'POST'])
def main():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template('main.html', title='Home', img_uri=DefaultSettings.HOME_SCREEN, icon=DefaultSettings.ICON,
                           project_name=DefaultSettings.PROJECT)


@app.route("/about", methods=['GET', 'POST'])
def about():
    message = "Paint-Box is an application designed for tabletop hobbyists to help keep track of projects in one place."
    return render_template('about.html', message=message, user=current_user, title='About')


@app.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    print("*" * 100)
    global projects
    projects = Project.get_projects(current_user)

    print(projects)
    # logging.info(f"Pro: ('{pro.get_projects(current_user)}', 'Projects{projects}')")
    return render_template('index.html', title='Home', user=current_user, projects=projects)


@app.route("/add_project", methods=['POST'])
@login_required
def add_project():
    data = {
        'added': True,
        'messages': "Project added :)"
    }
    name = request.form.get('name')
    desc = request.form.get('desc')
    tags = request.form.get('tag')
    try:

        logging.debug("Adding name:%s description:  %s tag:  %s" % (name, desc, tags))

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


@app.route('/project/<name>', methods=['GET', 'POST'])
@login_required
def project(name):
    return render_template('project.html', title='Project', project=Project.get_db(name), user=current_user)


@app.route('/todo', methods=['GET', 'POST'])
@login_required
def todo():
    return render_template('todo_macro.html')


@app.route('/add_tag/<int:num>', methods=['POST'])
@login_required
def add_tag(num):
    projects[num].add_tag(request.form.get('tag'))
    return redirect(url_for('project', num=num))


@app.route('/add_process/<int:num>', methods=['POST'])
@login_required
def add_process(num):
    projects[num].add_process(request.form.get('process'))
    return redirect(url_for('project', num=num))


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    new_user = User()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        try:

            if (new_user.add_user(request.form.get("username"), request.form.get("firstname"),
                                  request.form.get("lastname"),
                                  request.form.get("email"), request.form.get("password"),
                                  request.form.get("password_confirm")) is True):

                # account has been created!
                return redirect(url_for('login'))
            else:
                error = "ERROR! Passwords don't match"
        except IntegrityError:
            db.session.rollback()
            error = 'ERROR! Email or Username already exists.'
            # flash('ERROR! Email ({}) already exists.'.format(request.form.get('email')), 'error')
        except AssertionError as e:
            error = e
    return render_template('register.html', error=error)


@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    # check if user alredy logedin
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        # load the user class
        new_user = User()
        # get email form form
        email = request.form.get('email')
        # find the user on database
        user = new_user.login(email, request.form.get('password'))
        if user:
            logging.info("User Found")
            login_user(user, False)
            # redirect to the previous page
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            # user not found incorect email or pssword
            logging.info("User Not Found")
            error = 'Login Unsuccessful. Please check email or password'

    return render_template('login.html', title='Login', error=error)


@app.route("/test", methods=['POST'])
def test():
    data = {
        'added': True,
        'messages': "Project already exists "
    }
    js = json.dumps(data)
    return Response(js, status=200, mimetype='application/json')


# @app.route("/test", methods=['POST'])
# def test():
#
#     print(request.form.get('name'))
#     data = {
#         'added': False,
#         'number': 3
#     }
#     js = json.dumps(data)
#     return Response(js, status=200, mimetype='application/json')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404
