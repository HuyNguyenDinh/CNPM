from clinicapp import app, login
from flask import render_template, redirect, request
from flask_login import login_user
from flask_admin import expose
import hashlib

@app.route("/")
def homepage():
    return render_template('index.html')
@app.route("/admin/login", methods=['POST', 'GET'])
def login_admin():
    if request.method == "POST":
        username = request.form.get('userN')
        password = request.form.get('passW', '')
        password = str(hashlib.md5(password.encode("utf-8")).hexdigest())
        user = User.query.filter(User.username == username, User.password == password).first()
        if user:
            login_user(user=user)
    return redirect('/admin')

@expose('/')
@app.route('/user')
def edit_profile():
    return redirect('/admin/user')
@login.user_loader
def get_user(user_id):
    return User.query.get(user_id)

if __name__ == "__main__":
    from clinicapp.admin import *
    app.run(debug=True)



