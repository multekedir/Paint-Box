from PaintBox import db, logging
from datetime import datetime


class DBtodo(db.Model):
    """
    Db for a list of tasks
    """
    __tablename__ = 'todo'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    stage_id = db.Column(db.Integer, db.ForeignKey('stage.id'), nullable=False)

    def __repr__(self):
        return f"Project('{self.name}', '{self.stage_id}')"

    def set_name(self, newname):
        """
        change the name task
        :param newname: (str)
        :return: (str)
        """
        self.name = newname
        return self.name

    def complete(self):
        """
        makes a task complete

        :return: (bool)
        """
        self.completed = True
        return self.completed

    def incomplete(self):
        """
        makes a task in-complete

        :return: (bool)
        """
        self.completed = False
        return not self.completed

    def delete(self):
        """
        removes task from db
        :return:
        """
        logging.info(f"Deleting Tag {self.name}")
        db.session.delete(self)