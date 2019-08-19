from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(10), default='user')
    gender = db.Column(db.Boolean)
    description = db.Column(db.Text, nullable=True)
    stu_id = db.Column(db.Integer)

    username = db.Column(db.String(30))
    pwd_hash = db.Column(db.String(30))

    def __init__(self, **kwargs):
        super().__init__()
        for k, v in kwargs.items():
            setattr(self, k, v)


class Challenge(db.Model):
    __tablename__ = 'challenges'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30))
    category = db.Column(db.String(100))
    description = db.Column(db.Text)


class Submission(db.Model):
    __tablename__ = 'submissions'
    id = db.Column(db.Integer, primary_key=True)
    solver_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    challenge_id = db.Column(db.Integer, db.ForeignKey("challenges.id"))
    answer = db.Column(db.Text)
