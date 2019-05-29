from sqlalchemy import UniqueConstraint
from PaintBox import db, logging
from datetime import datetime
import json


class DBtags(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    def __repr__(self):
        return f"Project('{self.name}', '{self.project_id}')"

    def delete(self):
        logging.info(f"Deleting Tag {self.name}")
        db.session.delete(self)
        db.session.commit()


# class DBPictures(db.Model):
#     __tablename__ = 'pictures'
#     id = db.Column(db.Integer, primary_key=True)
#     filename = db.Column(db.String(20), nullable=False)
#     project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
#     # stages_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
#     description = db.Column(db.Text)

class DBStage(db.Model):
    __tablename__ = 'stage'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    todos = db.relationship('DBtodo', backref='stage', lazy=True)

    __table_args__ = (UniqueConstraint('project_id', 'name', name='_name_project'),)

    def __repr__(self):
        return f"Project('{self.name}', '{self.project_id}')"

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def complete_task(self, task_id):
        task = DBtodo.query.filter_by(id=task_id).first()
        task.complete()
        db.session.commit()
        print(f"{task.name} is {task.completed}")

    def incomplete_task(self, task_id):
        task = DBtodo.query.filter_by(id=task_id).first()
        task.incomplete()
        db.session.commit()
        print(f"{task.name} is {task.completed}")

    def add_task(self, name):

        logging.debug(f'Adding a task to DB {name}')
        # if we are given a list

        # assert (tags not in old_tags), "Tag already exist"
        task = DBtodo(name=name, stage=self)
        db.session.add(task)
        db.session.commit()
        print('added task')
        return task.id

    def edit_task(self, name):

        logging.debug(f'Editting a task to DB {name}')
        # if we are given a list

        # assert (tags not in old_tags), "Tag already exist"
        task = DBtodo(name=name, stage=self)
        db.session.add(task)
        db.session.commit()
        print('added task')
        return task.id

    def get_completed(self):
        completed = []
        taskid = []
        task = DBtodo.query.filter_by(stage=self).all()
        if task is not None:
            for i in task:
                if i.completed is True:
                    completed.append(i.name)
                    taskid.append(i.id)
        return completed, taskid

    def get_started(self):
        started = []
        taskid = []
        task = DBtodo.query.filter_by(stage=self).all()
        if task is not None:
            for i in task:
                if i.completed is False:
                    started.append(i.name)
                    taskid.append(i.id)
        return started, taskid


class DBtodo(db.Model):
    __tablename__ = 'todo'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    stage_id = db.Column(db.Integer, db.ForeignKey('stage.id'), nullable=False)

    def __repr__(self):
        return f"Project('{self.name}', '{self.project_id}')"

    def complete(self):
        self.completed = True
        return True

    def incomplete(self):
        self.completed = False
        return False

    def delete(self):
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
    stages = db.relationship('DBStage', backref='stage', lazy=True)

    __table_args__ = (UniqueConstraint('user_id', 'name', name='_name_user'),)

    def __repr__(self):
        return f"Project('{self.name}', '{self.date_posted}')"

    def to_dict(self):
        return dict({'name': self.name, 'id': self.id, 'description': self.description})

    def get_id(self):
        return self.id

    def delete(self):
        print("Deleting project")
        for i in self.get_tag_dbs():
            i.delete()
        db.session.delete(self)
        db.session.commit()

    def set_name(self, name):
        self.name = name

    def get_name(self, name):
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
            # assert (tags not in old_tags), "Tag already exist"
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

    def add_stage(self, name):
        logging.debug(f'Adding a stage to DB {name}')
        old_tags = self.get_tags()
        # if we are given a list

        # assert (tags not in old_tags), "Tag already exist"
        db.session.add(DBStage(name=name, stage=self))
        db.session.commit()
        print('added stage')

    def get_stages(self):
        stages_list = []
        tags = DBStage.query.filter_by(stage=self).all()
        if tags is not None:
            for i in tags:
                stages_list.append(i)
        return stages_list


def get_db(id):
    return DBproject.query.filter_by(id=id).first()


def get_stage(id):
    return DBStage.query.filter_by(id=id).first()


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
    # print(data)
    for item in data:
        logging.info(f"Project('{item.name}', '{item.id}', '{item.description}')")
        project_list.append(item)

    return project_list


def get_projects_json(user):
    """

    :rtype: object
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
