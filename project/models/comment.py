from project import db

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    comment = db.Column(db.String(250))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)