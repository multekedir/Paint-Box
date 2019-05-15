from PaintBox import db, logging

from datetime import datetime
from typing import List


class Process:
    def __init__(self, name):
        self.name = name
        self.description = ""
        self.img_url = ""

    def set_name(self, name):
        """
        changes the name of the cls
        :param name:
        :return: None
        """
        self.name = name

    def set_description(self, des):
        self.description = des

    def set_img(self, url):
        self.img_url = url

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_img(self):
        return self.img_url


class DBtags(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    def __repr__(self):
        return f"Project('{self.name}', '{self.project_id}')"


class DBproject(db.Model, object):
    __tablename__ = 'project'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tags = db.relationship('DBtags', backref='pro', lazy=True)

    def __repr__(self):
        return f"Project('{self.name}', '{self.date_posted}')"

    def set_name(self, name):
        self.name = name
        db.session.commit()

    def set_description(self, description):
        self.description = description
        db.session.commit()

    def get_description(self):
        return self.description

    def get_name(self):
        return self.name

    def add_tag(self, tags):
        logging.debug(f'Adding a tag to DB {tags}')
        db.session.commit()
        # if we are given a list
        if isinstance(tags, list):
            for i in tags:
                db.session.add(DBtags(name=i, pro=self))
        else:
            db.session.add(DBtags(name=tags, pro=self))
        db.session.commit()

    def get_tags(self):
        tag_list = []
        tags = DBtags.query.filter_by(pro=self).all()
        if tags is not None:
            for i in tags:
                tag_list.append(i.name)
        return tag_list

    def get_tags_csv(self):
        data = self.get_tags()
        if data is not  None:
            return ','.join(map(str, self.get_tags()))
        return ""


class Project:

    def __init__(self, name=None, num=0, who=None, description=None):
        self.tag_list = []
        self.name = name
        self.process_list = []
        self.num = num
        self.description = description
        self.who = who

    def __repr__(self):
        return f"Project {self.name}"

    def get_id(self):
        return self.name

    def add_tag(self, tags, projectname):
        logging.debug(f'Adding a tag to DB {tags}')
        project = DBproject.query.filter_by(name=self.name).first()
        db.session.commit()
        # if we are given a list
        if isinstance(tags, list):
            for i in tags:
                db.session.add(DBtags(name=tags, pro=project))
                self.tag_list.append(i)
        else:
            db.session.add(DBtags(name=tags, pro=project))
            self.tag_list.append(tags)
        db.session.commit()

    def remove_tag(self, tag):
        index = self.tag_list.index(tag)
        del self.tag_list[index]

    def remove_all_tags(self):
        self.tag_list.clear()

    def get_tags(self):
        return self.tag_list

    def get_tags_csv(self):

        return ','.join(map(str, self.tag_list))

    def set_name(self, name):
        DBproject.query.filter_by(name=self.name).update(dict(name=name))
        db.session.commit()
        self.name = name

    def get_name(self):
        return self.name

    def get_description(self):
        """
         gets the description
        :return: str
        """
        return self.description

    def add_process(self, name):
        pro = Process(name)
        self.process_list.append(pro)

    def get_processes(self):
        return self.process_list


def get_db(name):
    return DBproject.query.filter_by(name=name).first()


def add_project(name, user):
    logging.debug('Adding project to DB')
    db.session.add(DBproject(name=name, description="", author=user))
    db.session.commit()


def get_projects(user):
    """

    :rtype: object
    """
    # list of projects
    project_list = []
    logging.debug('getting projects from db')
    # load all projects from db using user id filter
    data = DBproject.query.filter_by(author=user).all()
    print(data)
    for item in data:
        logging.info(f"Project('{item.name}', '{item.id}', '{item.description}')")
        project_list.append(Project(item.name, item.id, user, item.description))

    return project_list
