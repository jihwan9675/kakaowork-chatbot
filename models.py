from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Complement(db.Model):
    __tablename__ = 'colawork'

    id = db.Column(db.Integer, primary_key=True)
    senderid = db.Column(db.Integer)
    complement_value = db.Column(db.String(16))
    complement_content = db.Column(db.String(128))

    def __repr__(self):
        return "<('%s','%s','%s','%s')>" % (self.id, self.senderid, self.complement_value, self.complement_content)
    
    def message_notify(self):
        return "%s님이 %s님에게 칭찬을 하였습니다." % (self.senderid, self.id)