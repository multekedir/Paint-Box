from sqlalchemy import UniqueConstraint
from sqlalchemy.exc import IntegrityError

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

    def delete (self):
        logging.info(f"Deleting Tag {self.name}")
        db.session.delete(self)
        db.session.commit()


class DBproject(db.Model, object):
    __tablename__ = 'project'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tags = db.relationship('DBtags', backref='pro', lazy=True)

    __table_args__ = (UniqueConstraint('user_id', 'name', name='_name_user'),)

    def __repr__(self):
        return f"Project('{self.name}', '{self.date_posted}')"

    def delete (self):
        print("Deleting project")
        for i in self.get_tag_dbs():
            i.delete()
        db.session.delete(self)
        db.session.commit()

    def set_name(self, name):
        self.name = name

    def set_description(self, description):
        self.description = description

    def get_description(self):
        return self.description

    def get_name(self):
        return self.name

    def update_project(self, newname, newtags, newdescription):
        """
        Checks if there is a change and applies the change to a
        newname, newtag, or newdescription.
        :param name: str
        :param newname: str
        :param newtags: list
        :param newdescription: str
        :return:
        """
        # get old project
        try:
            if self.name is not newname:
                self.set_name(newname)

            # check if tags are diferent
            if set(newtags) != set(self.get_tags()):
                self.add_tag(newtags.split(','))

            # check if descriptions match
            if self.description is not newdescription:
                self.set_description(newdescription)
        except AssertionError as e:
            db.session.rollback()
            return "tag_error"
        db.session.commit()
        return "Project updated"

    def add_tag(self, tags):
        logging.debug(f'Adding a tag to DB {tags}')
        old_tags = self.get_tags()
        # if we are given a list
        if isinstance(tags, list) and not []:
            # remove duplicates
            for i in list(set(tags)):
                # check if tag already exist
               # assert (i not in old_tags), "Tag already exist"
                db.session.add(DBtags(name=i, pro=self))
        else:
            #assert (tags not in old_tags), "Tag already exist"
            db.session.add(DBtags(name=tags, pro=self))

    def get_tags(self):
        tag_list = []
        tags = DBtags.query.filter_by(pro=self).all()
        if tags is not None:
            for i in tags:
                tag_list.append(i.name)
        return tag_list

    def get_tag_dbs(self):
        tag_list = []
        tags = DBtags.query.filter_by(pro=self).all()
        if tags is not None:
            for i in tags:
                tag_list.append(i)
        return tag_list

    def get_tags_csv(self):
        data = self.get_tags()
        if data is not None:
            return ','.join(map(str, self.get_tags))
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

        # if we are given a list
        if isinstance(tags, list):
            for i in tags:
                db.session.add(DBtags(name=tags, pro=self))
                self.tag_list.append(i)
        else:
            db.session.add(DBtags(name=tags, pro=self))
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
    new_project = DBproject(name=name, description="", author=user)
    db.session.add(new_project)
    db.session.commit()

    return new_project


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
