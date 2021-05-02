from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Complement(db.Model):
    __tablename__ = 'colawork'

    id = db.Column(db.Integer, primary_key=True)
    senderid = db.Column(db.Integer)
    complement_value = db.Column(db.String(16))
    complement_content = db.Column(db.String(128))