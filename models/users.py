from db import db
import json


class UsersModel(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(30), nullable=False)
  password = db.Column(db.String(102), nullable=False)
  email = db.Column(db.String(50), nullable=False)
  name = db.Column(db.String(50), nullable=False)
  date_created = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
  date_modified = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

  def __repr__(self):
    return 'User ' + str(self.id)

  def json(self):
    return {
        'id': self.id,
        'username': self.username,
        'email': self.email,
        'name': self.name,
        'date_created': self.date_created.__str__(),
        'date_modified': self.date_modified.__str__()
    }

  @classmethod
  def find_by_id(cls, id):
    return cls.query.filter_by(id=id).first()

  @classmethod
  def find_by_username(cls, username):
    return cls.query.filter_by(username=username).first()

  def save(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()


def updateField(self, field, value):
  setattr(self, field, value)


def update(self, **fields):
  for field, value in fields.items():
    self.updateField(field, value)
