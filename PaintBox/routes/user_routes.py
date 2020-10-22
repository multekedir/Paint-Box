from sqlalchemy.exc import IntegrityError

from flask import request, redirect, url_for, render_template
from flask_login import login_required, current_user, login_user, logout_user

from PaintBox import app, db, logging
from PaintBox.auth import OAuthSignIn
from PaintBox.modules.database import User



@app.route('/authorize/<provider>')
def oauth_authorize(provider='google'):
    # Flask-Login function
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    username, email = oauth.callback()
    if email is None:
        # I need a valid email address for my user identification
        print('Authentication failed.')
        return redirect(url_for('main'))
    # Look if the user already exists

    user = User.get_user(email)
    if not user:
        # Create the user. Try and use their name returned by Google,
        # but if it is not set, split the email address at the @.
        nickname = username
        if nickname is None or nickname == "":
            nickname = email.split('@')[0]

        # We can do more work here to ensure a unique nickname, if you
        # require that.

        User.add_user(nickname, "Goole", "Test",email,"password","password")

        db.session.commit()
    # Log in the user, by default remembering them for their next visit
    # unless they log out.
    login_user(user, remember=True)
    return redirect(url_for('index'))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    if request.method == 'POST':
        username = request.form.get("username")
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        User.update(username, firstname, lastname, email, current_user)
        return redirect(url_for('home'))

    return render_template('acount.html', user=current_user)


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


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
