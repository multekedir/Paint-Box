from flask import Flask
app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/", methods=['GET'])
def hello():
    return "Hello World!"

@app.route('/user/<username>')
def show_subpath(username):
    # show the subpath after /path/
    return 'Subpath %s' % subpath'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

if __name__ == '__main__':
    app.run()
