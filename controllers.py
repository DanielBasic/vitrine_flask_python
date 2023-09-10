from flask import render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import Vitrine, db, User


class VitrineController():
  def index():
    if 'user_id' not in session:
      return redirect('/login')
    user_id = session['user_id']
    vitrine = Vitrine.query.filter_by(user_id = user_id).all()
    return render_template("index.html", vitrine = vitrine)

  def ad_product():
    if 'user_id' not in session:
      return redirect('/login')
    user_id = session['user_id']

    name_nw_product = request.form.get("name_nw_product")
    price_nw_product = request.form.get("price_nw_product")
    new_product = Vitrine(title = name_nw_product, price = price_nw_product, user_id = user_id)

    db.session.add(new_product)
    db.session.commit()
    return redirect("/")

  def delete(id):
    if 'user_id' not in session:
      return redirect('/login')

    product = Vitrine.query.filter_by(id=id).first()
    if product:
      db.session.delete(product)
      db.session.commit()
    return redirect("/")

  def update(id):
    if 'user_id' not in session:
      return redirect('/login')

    product = Vitrine.query.filter_by(id = id).first()
    title = request.form.get("name_nw_product")
    product.title = title
    price = request.form.get("price_nw_product")
    if len(price):
      price = 0
    elif not price.isnumeric():
      price = product.price
    product.price = price
    
    db.session.commit()
    return redirect("/")

class UserController():
  def login(): 
    return render_template('login.html')

  def signin():
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
      return redirect('/login')
    else:
      session['user_id'] = user.id
      return redirect('/')

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

  def register():
    return render_template('register.html')

  def logout():
    if 'user_id' in session:
      session.pop('user_id', None)
      return redirect('/')
  

