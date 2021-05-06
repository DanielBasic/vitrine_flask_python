from database import db

class Vitrine(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(65))
  price = db.Column(db.Numeric(10,2))
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(1000))
  email = db.Column(db.String(100), unique=True)
  password = db.Column(db.String(100))  