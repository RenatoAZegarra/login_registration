from flask import render_template, request, redirect, session, flash
from flask_app.models import users_model
from flask_app import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if not users_model.User.validate_user(request.form):
        return redirect('/')
    else:
        # hash password before storing in database
        hashed_pw = users_model.User.encrypt_string(request.form['password'])
        new_user_data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': hashed_pw
        }
        user_id = users_model.User.create_one(new_user_data)
        session['user_id'] = user_id
        return redirect('/success')

@app.route('/login', methods=['POST'])
def login():
    current_user = users_model.User.get_one_by_email(request.form)
    if current_user and users_model.User.validate_password(request.form['password'], current_user.password):
        session['user_id'] = current_user.id
        session['full_name'] = current_user.first_name + " " + current_user.last_name
        return redirect('/success')
    else:
        return redirect('/')

@app.route('/success')
def success():
    if 'user_id' not in session:
        return redirect('/')
    else:
        return render_template('welcome.html')

@app.route('/logout' , methods=['POST'])
def process_logout():
    session.clear()
    return redirect('/')