from flask import Flask, request, render_template, url_for, redirect

from modules import Project

app = Flask(__name__)
app.config["DEBUG"] = True

projects = []


@app.route("/", methods=['GET', 'POST'])
def home():
    user = {'username': 'Multezem Kedir', "first":"Kedir"}

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
