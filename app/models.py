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
    decided = db.Column(db.String(25))

    def __init__(self, name, computing_id, dorm, year, pic):
        self.name = name
        self.computing_id = computing_id
        self.dorm = dorm
        self.year = year
        self.pic = self.upload_to_imgur(pic)
        self.event = time.strftime("%Y-%m-%d")
        self.decided = False

    def __repr__(self):
        return '<Rushee #%r: %r - %r - %r - %r>' % (self.id, self.name, self.year, self.computing_id, self.dorm)

    def upload_to_imgur(self, pic):
        import pyimgur
        CLIENT_ID = "a42e0d6331c2b99"
        im = pyimgur.Imgur(CLIENT_ID)
        pic = pic[pic.find("base64,") + len("base64,"):]
        upload = im.upload_image(url=pic)
        return upload.link
