from clinicapp import app, login
from flask import render_template, redirect, request
from flask_login import login_user, login_required, logout_user
from flask_admin import expose
import hashlib

@app.route("/")
def homepage():
    return render_template('index.html')

@app.route("/return-admin")
def return_admin_page():
    return redirect('/admin')


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


@app.context_processor
def common_response():
    path = find_path(current_user)
    return {
        "path_role": path
    }

@app.route('/employee-login', methods = ['post', 'get'])
def employee_login():
    error_ms = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user = check_login(username=username, password=password)
        if user:
            login_user(user=user)
            if user.user_role == UserRole.ADMIN:
                return redirect('/admin')
            elif user.user_role == UserRole.NURSE:
                return redirect('/nurse-view')
            return redirect('/doctor-view')
        else:
            error_ms = "Sai tên đăng nhập hoặc mật khẩu!!!"
    return render_template('login-user.html', error_ms=error_ms)

@app.route('/doctor-view')
@login_required
def doctor_view():
    return render_template('doctor-view.html')

@app.route('/nurse-view')
@login_required
def nurse_view():
    return render_template('nurse-view.html')

@app.route("/user-logout")
def user_logout():
    logout_user()
    return redirect("/")

if __name__ == "__main__":
    from clinicapp.admin import *
    app.run(debug=True)



