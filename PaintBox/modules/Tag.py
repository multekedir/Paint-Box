from PaintBox import db, logging


class DBTag(db.Model):
    """
    Database for tags
    """
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    def __repr__(self):
        return f"Project('{self.name}', '{self.project_id}')"

    def delete(self):
        """
        removes tag from db
        :return:
        """
        logging.info(f"Deleting Tag {self.name}")
        db.session.delete(self)
        db.session.commit()
