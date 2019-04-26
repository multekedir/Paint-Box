from flask import Flask, request, render_template
from modules import Project

app = Flask(__name__)
app.config["DEBUG"] = True


projects = []


@app.route("/index", methods=['GET', 'POST'])
def home():
    user = {'username': 'Miguel'}
    pro = None
    if request.method == 'POST':
        id = len(projects)
        pro = Project.Project(request.form.get('name'), id)
        projects.append(pro)
    return render_template('index.html', title='Home', user=user, projects=projects)


@app.route('/project/<num>', methods=['GET', 'POST'])
def project(num):

    return render_template('project.html', title='project', project=projects[num], id=num)


@app.route('/add_tag/<num>', methods=['POST'])
def add_tag(num):
    projects[num].add_tag(request.form.get('tag'))
    return render_template('project.html', title='project', project=projects[num], id=num)


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
