from datetime import datetime

from PaintBox import db, logging
from sqlalchemy import UniqueConstraint

from PaintBox.modules.Todo import DBtodo


class DBStage(db.Model):
    """
    DB for stages
    """
    __tablename__ = 'stage'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    todos = db.relationship('DBtodo', backref='stage', lazy=True)

    __table_args__ = (UniqueConstraint('project_id', 'name', name='_name_project'),)

    def __repr__(self):
        return f"Stage('{self.name}', '{self.project_id}')"

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    @staticmethod
    def complete_task(task_id):
        """
        mark a task complete

        :return: true if complete
        """
        task = DBtodo.query.filter_by(id=task_id).first()
        task.complete()
        db.session.commit()
        logging.info(f"{task.name} is {task.completed}")
        return task.completed is True

    @staticmethod
    def incomplete_task(task_id):
        """
        marks a task incomplete

        :param task_id: id of task
        :return: true if incomplete
        """
        task = DBtodo.query.filter_by(id=task_id).first()
        task.incomplete()
        db.session.commit()
        logging.info(f"{task.name} is {task.completed}")
        return task.completed is False

    def add_task(self, name):
        """
        adds task to db

        :param name:
        :return: id of task
        """
        logging.info(f'Adding a task to DB {name}')

        task = DBtodo(name=name, stage=self)
        db.session.add(task)
        db.session.commit()

        logging.info('added task')
        return task.id

    @staticmethod
    def edit_task(task_id, newname):
        """
        changes the name of a task

        :param taskid: id of a task
        :param newname: change task name to new name
        :return:
        """

        task = DBtodo.query.filter_by(id=task_id).first()
        print(task_id)
        logging.info(f'Editing a task to DB {task}')

        task.set_name(newname)
        db.session.commit()
        logging.info(f'Task edited to {task}')

        return task.id

    @staticmethod
    def delete_task(task_id):
        """
        deletes task from db

        :param taskid: id of a task
        :param newname: change task name to new name
        :return: bool
        """
        task = DBtodo.query.filter_by(id=task_id).first()
        logging.info(f'Deleting task from DB {task}')

        task.delete()
        db.session.commit()
        return DBtodo.query.filter_by(id=task_id).first() is None

    def get_completed(self):
        """
        finds list of task that are completed

        :return: list of completed tasks with id
        """
        completed = []
        taskid = []

        # get all tasks
        task = DBtodo.query.filter_by(stage=self).all()
        if task is not None:
            for i in task:
                if i.completed is True:
                    completed.append(i.name)
                    taskid.append(i.id)
        return completed, taskid

    def get_started(self):
        """
       finds list of task that are in-completed

       :return: list of in-completed tasks with id
       """
        started = []
        taskid = []
        task = DBtodo.query.filter_by(stage=self).all()
        if task is not None:
            for i in task:
                if i.completed is False:
                    started.append(i.name)
                    taskid.append(i.id)
        return started, taskid
