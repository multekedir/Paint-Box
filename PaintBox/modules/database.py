from datetime import datetime
from PaintBox import db, bcrypt

from flask_login import UserMixin

from PaintBox import login_manager
import re
from PaintBox.modules.Project import DBproject


@login_manager.user_loader
def load_user(user_id):
    return DBUser.query.get(int(user_id))


class DBUser(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    firstname = db.Column(db.String(20), unique=True, nullable=False)
    lastname = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    projects = db.relationship('DBproject', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

    def is_active(self):
        return self.is_enabled


def hash_password(password):
    """

    :param password: str
    :return: str hashed_password
    """

    return str(bcrypt.generate_password_hash(password).decode('utf-8'))


def check_hashed(password, newpassword):
    """

    :param password:
    :param newpassword:
    :return: bool
    """
    return bcrypt.check_password_hash(password, newpassword)


def check_password(password, password_confirm):
    """

    :return:
    """
    patern = '^(?=\S{6,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])'
    if password_confirm == password:
        if re.compile(patern).match(password):
            return True
    return True


class User:

    @staticmethod
    def add_user(username, firstname, lastname, email, password, password_confirm):
        """

        :param username: str
        :param firstname: str
        :param lastname: str
        :param email: str
        :param password: str
        :return: None
        """
        # print("username: " + username)
        # print("email: " + email)
        # print("first name: " + firstname)
        # print("first name: " + lastname)
        # print("password " + password)
        # print("Confirm " + password_confirm)

        user = DBUser(username=username, firstname=firstname, lastname=lastname,
                      email=email, password=hash_password(password))
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def get_user(email):
        """
        :param email: str
        :return: DBUser
        """
        return DBUser.query.filter_by(email=email).first()

    def login(self, email, password):
        """

        :param email: str
        :param password: str
        :return: user
        """

        user = self.get_user(email)

        if user and check_hashed(user.password,password):
            return user
        return None
