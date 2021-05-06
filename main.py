import os
from flask import Flask
from database import db
from controllers import VitrineController, UserController

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SECRET_KEY'] = 'secret'

db.init_app(app)

@app.route("/")
def index():
  return VitrineController.index()

@app.route("/ad_product", methods=["POST"])
def ad_product():
  return VitrineController.ad_product()

@app.route("/delete/<int:id>")
def delete(id):
  return VitrineController.delete(id)

@app.route("/update/<int:id>", methods=["POST"])
def update(id):
  return VitrineController.update(id)  

@app.route('/login')
def login():
  return UserController.login()

@app.route('/signin', methods=['POST'])
def signin():
  return UserController.signin()

@app.route('/signup', methods=['POST'])
def signup():
  return UserController.signup()

@app.route('/register')
def register():
  return UserController.register()

@app.route('/logout')
def logout():
  return UserController.logout()

with app.app_context():
  db.create_all()

if __name__ == "__main__":
  port = int(os.environ.get('PORT', 5000))
  app.run(host="0.0.0.0", port = port)