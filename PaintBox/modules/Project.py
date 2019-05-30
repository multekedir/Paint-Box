from sqlalchemy import UniqueConstraint
from PaintBox import db, logging
from datetime import datetime

from PaintBox.modules.Stage import DBStage
from PaintBox.modules.Tag import DBTag

import json


class DBproject(db.Model, object):
    __tablename__ = 'project'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tags = db.relationship('DBTag', backref='pro', lazy=True)
    stages = db.relationship('DBStage', backref='stage', lazy=True)

    __table_args__ = (UniqueConstraint('user_id', 'name', name='_name_user'),)

    def __repr__(self):
        return f"Project('{self.name}', '{self.date_posted}')"

    def to_dict(self):
        """
        project information as a dictionary
        :return: (dict)
        """
        return dict({'name': self.name, 'id': self.id, 'description': self.description})

    def get_id(self):
        """
        gets project id

        :return: (ID)
        """
        return self.id

    def delete(self):
        """
        deletes project from database
        :return:
        """
        logging.info("Deleting project")

        # get a list of tags related to project
        for i in self.get_tag_dbs():
            i.delete()
        db.session.delete(self)
        db.session.commit()

    def set_name(self, name):
        """
        change the name of project
        :param name:
        :return: none
        """
        self.name = name

    def get_name(self):
        """
        get the name of a the project
        :return: (str) name
        """
        return self.name

    def set_description(self, description):
        """
        change the description of a project
        :param description:
        :return:
        """
        self.description = description

    def get_description(self):
        """
        get description of the project
        :return: (str) description
        """
        return self.description

    def update_project(self, newname, newtags, newdescription):
        """
        Checks if there is a change and applies the change to a
        newname, newtag, or newdescription.


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
        """
        add a tag
        :param tags:
        :return:
        """
        logging.debug(f'Adding a tag to DB {tags}')
        old_tags = self.get_tags()
        # if we are given a list
        if isinstance(tags, list) and not []:
            # remove duplicates
            for i in list(set(tags)):
                # check if tag already exist
                # assert (i not in old_tags), "Tag already exist"
                db.session.add(DBTag(name=i, pro=self))
        else:
            # assert (tags not in old_tags), "Tag already exist"
            db.session.add(DBTag(name=tags, pro=self))

    def get_tags(self):
        """

        :return: list of tags
        """
        tag_list = []
        tags = DBTag.query.filter_by(pro=self).all()
        if tags is not None:
            for i in tags:
                tag_list.append(i.name)
        return tag_list

    def get_tag_dbs(self):
        """

        :return: list of db rows
        """
        tag_list = []
        tags = DBTag.query.filter_by(pro=self).all()
        if tags is not None:
            for i in tags:
                tag_list.append(i)
        return tag_list

    def get_tags_csv(self):
        """
        projects sparted by commas
        :return: (str)
        """
        data = self.get_tags()
        if data is not None:
            return ','.join(map(str, self.get_tags))
        return ""

    def add_stage(self, name):
        """
        adds new stage to project
        :param name:
        :return: (DBStage)
        """

        stage = DBStage(name=name, stage=self)
        db.session.add(stage)
        db.session.commit()

        logging.info(f'Added a stage to DB {stage}')
        return stage

    def get_stages(self):
        """
        gets all the stages related to project
        :return: (list)
        """
        stages_list = []
        stage = DBStage.query.filter_by(stage=self).all()
        if stage is not None:
            for i in stage:
                stages_list.append(i)

        return stages_list


def get_db(id):
    """
    finds a project
    :param id:
    :return: (DBproject)
    """
    return DBproject.query.filter_by(id=id).first()


def get_stage(id):
    """
       finds a stage
       :param id:
       :return: (DBStage)
       """
    return DBStage.query.filter_by(id=id).first()


def add_project(name, user):
    """
    add new project to db
    :param name:
    :param user:
    :return: (DBproject)
    """
    logging.info('Adding project to DB')
    new_project = DBproject(name=name, description="", author=user)
    db.session.add(new_project)
    db.session.commit()

    return new_project


def get_projects(user):
    """
    Finds a list of project under the a user
    :param user: (DBUser)
    :return: (list)
    """
    # list of projects
    project_list = []
    logging.debug('getting projects from db')
    # load all projects from db using user id filter
    data = DBproject.query.filter_by(author=user).all()

    for item in data:
        logging.info(f"Project('{item.name}', '{item.id}', '{item.description}')")
        project_list.append(item)

    return project_list


def get_projects_json(user):
    """
    Finds a list of project under the a user
    :param user: (DBUser)
    :return: (json)
    """
    # list of projects
    project_list = []
    logging.debug('getting projects from db')
    # load all projects from db using user id filter
    data = DBproject.query.filter_by(author=user).all()
    # print(data)
    for item in data:
        logging.info(f"Project('{item.name}', '{item.id}', '{item.description}')")
        print(item.to_dict())
        project_list.append(item.to_dict())

    return json.dumps(project_list)
