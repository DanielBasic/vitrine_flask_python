import os
from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SECRET_KEY'] = 'secret'
db = SQLAlchemy(app)

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


@app.route("/")
def index():
  if 'user_id' not in session:
    return redirect('/login')
  user_id = session['user_id']
  vitrine = Vitrine.query.all()
  return render_template("index.html", vitrine = vitrine)

@app.route("/ad_product", methods=["POST"])
def ad_product():
  if 'user_id' not in session:
    return redirect('/login')
  user_id = session['user_id']

  name_nw_product = request.form.get("name_nw_product")
  price_nw_product = request.form.get("price_nw_product")
  new_product = Vitrine(title = name_nw_product, price = price_nw_product)

  db.session.add(new_product)
  db.session.commit()
  return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
  if 'user_id' not in session:
    return redirect('/login')

  product = Vitrine.query.filter_by(id=id).first()
  db.session.delete(product)
  db.session.commit()
  return redirect("/")

@app.route("/update/<int:id>", methods=["POST"])
def update(id):
  if 'user_id' not in session:
    return redirect('/login')

  product = Vitrine.query.filter_by(id = id).first()
  title = request.form.get("name_nw_product")
  product.title = title
  price = request.form.get("price_nw_product")
  product.price = price
  
  db.session.commit()
  return redirect("/")

@app.route('/login')
def login():
 return render_template('login.html')

@app.route('/signin', methods=['POST'])
def signin():
 email = request.form.get('email')
 password = request.form.get('password')
 user = User.query.filter_by(email=email).first()
 if not user or not check_password_hash(user.password, password):
  return redirect('/login')
 else:
  session['user_id'] = user.id
  return redirect('/')

@app.route('/signup', methods=['POST'])
def signup():
 name = request.form.get('name')
 email = request.form.get('email')
 password = request.form.get('password')
 user = User.query.filter_by(email=email).first()
 if user:
  return redirect('/register')

 new_user = User(
  email=email, name=name,
  password=generate_password_hash(password, method='sha256')
 )
 db.session.add(new_user)
 db.session.commit()
 return redirect('/login')

@app.route('/register')
def register():
 return render_template('register.html')

@app.route('/logout')
def logout():
 if 'user_id' in session:
  session.pop('user_id', None)
  return redirect('/')


if __name__ == "__main__":
  db.create_all()
  port = int(os.environ.get('PORT', 5000))
  app.run(host="0.0.0.0", port = port)