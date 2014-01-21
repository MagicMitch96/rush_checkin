from app import db, basedir
import os
import time

class Rushee(db.Model):
    __tablename__ = 'rushee'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(25))
    computing_id = db.Column(db.String(7))
    dorm = db.Column(db.String(25))
    year = db.Column(db.String(25))
    pic = db.Column(db.String(100))
    event = db.Column(db.String(10))
    decided = db.Column(db.String(1))

    def __init__(self, name, computing_id, dorm, year, pic):
        self.name = name
        self.computing_id = computing_id
        self.dorm = dorm
        self.year = year
        pic_path = os.path.join(basedir, 
                                'static/images/rushees/%s.png' %
                                (computing_id))
        pic = pic[pic.find('base64,') + len('base64,'):]
        with open(pic_path, "wb") as pic_file:
            pic_file.write(pic.decode('base64'))
        self.pic = 'images/rushees/%s.png' % (computing_id)
        self.event = time.strftime("%Y-%m-%d")
        self.decided = 0

    def __repr__(self):
        return '<Rushee #%r: %r - %r - %r - %r>' % (self.id, self.name, self.year, self.computing_id, self.dorm)
