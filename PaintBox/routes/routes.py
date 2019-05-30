import json

from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_required


from PaintBox import db, app, logging, DefaultSettings
from PaintBox.modules import Project


projects = []

db.create_all()


@app.route("/", methods=['GET', 'POST'])
def main():
    """ landing page """
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template('main.html', title='Home', img_uri=DefaultSettings.HOME_SCREEN, icon=DefaultSettings.ICON,
                           project_name=DefaultSettings.PROJECT)


@app.route("/about", methods=['GET', 'POST'])
def about():
    """help page"""
    return render_template('about.html', message=DefaultSettings.INFO, user=current_user, title='About')


@app.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    """page after login with list of projects"""
    print("*" * 100)
    global projects
    projects = Project.get_projects(current_user)

    logging.info(f"Projects: {projects}")
    return render_template('index.html', title='Home', user=current_user, projects=projects)




@app.route('/add_tag/<int:num>', methods=['POST'])
@login_required
def add_tag(num):
    projects[num].add_tag(request.form.get('tag'))
    return redirect(url_for('project', num=num))


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404
