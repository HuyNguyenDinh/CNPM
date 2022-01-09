from clinicapp import app, login
from flask import render_template, redirect, request, jsonify
from flask_login import login_user, login_required, logout_user
from flask_admin import expose
import hashlib
import cloudinary.uploader
from flask import url_for, json, session



@app.route("/")
def homepage():
    if current_user.is_authenticated:
        if current_user.user_role == UserRole.NURSE:
            return redirect('/nurse-view')
        elif current_user.user_role == UserRole.DOCTOR:
            return redirect('/doctor-view')
        else:
            return redirect('/admin')
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
    return {
        "sex": check_sex(current_user)
    }


@app.route('/employee-login', methods = ['post', 'get'])
def employee_login():
    error_ms = ''
    if current_user.is_authenticated:
        if current_user.user_role == UserRole.NURSE:
            return redirect('/nurse-view')
        elif current_user.user_role == UserRole.DOCTOR:
            return redirect('/doctor-view')
        else:
            return redirect('/admin')
    else:
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
    error_ms = request.args.get('error_ms')
    return render_template('doctor-view.html',error_ms = error_ms )

@app.route('/nurse-view')
@login_required
def nurse_view():
    error_ms = request.args.get('error_ms')
    return render_template('nurse-view.html',error_ms = error_ms)

@app.route("/user-logout")
def user_logout():
    logout_user()
    return redirect("/")

@app.route('/nurse-view/medical-register')
@login_required
def medical_register():
    return render_template('medical_register.html')

@app.route('/nurse-view/make-medical-list')
@login_required
def make_medical_list():
    d = request.args.get('date')
    temp = d
    if not d:
        temp = utils.get_last_date_of_exam()
        d = '-'.join([temp.get('year'), temp.get('month'), temp.get('day')])
    return render_template('make_medical_list.html', last_date=temp,\
                           med_list=utils.get_patient_in_exam(d), status=utils.get_status_of_exam(d))

@app.route('/nurse-view/pay-the-bill')
@login_required
def pay_the_bill():
    d = request.args.get('date')
    return render_template('pay-the-bill.html', bill=utils.get_bill_from_medicall_bill_in_day(exam_date=d))

@app.route('/nurse-view/pay-the-bill/<int:bill_id>')
@login_required
def detail_pay_the_bill(bill_id):
    bill = utils.get_bill(bill_id)
    return render_template('detail-pay-the-bill.html', bill=bill)

@app.route('/api/pay-bill', methods=['post'])
@login_required
def pay():
    data = request.json
    id = data.get('id')
    if id:
        if pay_bill(id):
            return jsonify({'code': 200})
    return jsonify({'code': 400})

@app.route('/api/create-exam', methods=['post'])
@login_required
def create():
    data = request.json
    id = data.get('id')
    if id:
        if change_status_examination(id):
            return jsonify({'code': 200})
    return jsonify({'code': 400})

@app.route('/doctor-view/make-a-medical-bill')
@login_required
def make_a_medical_bill():
    d = request.args.get('date')
    temp = d
    if not d:
        temp = utils.get_last_date_of_exam(doctor=True)
        d = '-'.join([temp.get('year'), temp.get('month'), temp.get('day')])
    pa = utils.get_patient_in_exam(exam_date=d, doctor=True)
    pati = utils.get_patient_and_medical_bill_in_exam(pa)
    return render_template('make_a_medical_bill.html', last_date=temp, pati=pati)

@app.route('/doctor-view/make-a-medical-bill/<int:patient_id>;<string:date>')
@login_required
def detail_make_a_medical_bill(patient_id, date):
    patient = utils.get_patient(patient_id)
    temp = patient[0]
    medicine = utils.get_medicine()
    return render_template('detail-make-a-medical-bill.html', patient=temp, date=date, medicine=medicine)

@app.route('/api/get_medicine', methods=['post'])
@login_required
def get_list_medicine_unit():
    return jsonify(utils.get_medicine_json())


@app.route('/change-info-user', methods = ['post', 'get'])
def change_info_user():
    if request.method.__eq__('POST'):
        error_ms = ''
        avatar = request.files.get('avatar')
        avatar_path = ''
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        sex = request.form.get('sex_of_user')
        day_of_birth = request.form.get('dob')
        phone = request.form.get('phone')
        password = request.form.get('password')
        new_password = request.form.get('new_password')
        confirm = request.form.get('confirm_password')
        try:
            if check_login_of_current_user(password, current_user):
                if (new_password != '' and confirm != '') or (new_password == '' and confirm == ''):
                    if not new_password.strip().__eq__(confirm.strip()):
                        error_ms = 'Xác nhận mật khẩu mới không khớp !!!'
                    else:
                        list = check_unique_info(username=username, phone=phone, email=email, user= current_user)
                        if len(list) == 0:
                            if avatar.filename.endswith('.png' or '.jpg' or '.jpeg') or not avatar:
                                if avatar:
                                    res = cloudinary.uploader.upload(avatar)
                                    avatar_path = res['secure_url']
                                try:
                                    check_info_for_change(user=current_user,avatar = avatar_path,name = name, username = username,day_of_birth=day_of_birth,email = email, sex=sex, phone= phone, new_password= new_password)
                                    error_ms = "Thay đổi thành công!!!"
                                except Exception as ex:
                                    error_ms = str(ex)
                            else:
                                error_ms = 'File avatar không hợp lệ (*.jpeg/*.png/*.jpg)!!!'
                        else:
                            error_ms = 'Những thông tin sau đã tồn tại: '
                            for i in range(len(list)):
                                if i != 0:
                                    error_ms += ', ' + list[i]
                                else:
                                    error_ms += list[i]

                else:
                    error_ms = 'Xác nhận mật khẩu mới không khớp !!!'

            else:
                error_ms = 'Nhập sai mật khẩu hiện tại !!!'
    #         #     if avatar:
    #         #         res = cloudinary.uploader.upload(avatar)
    #         #         avatar_path = res['secure_url']
    #         #     user_exist = check_username(username)
    #         #     if not user_exist:
    #         #         register_user(name=name, username=username, password=password, email=email, avatar=avatar_path)
    #         #         return redirect('/user-login')
    #         #     else:
    #         #         error = "Đã tồn tại username!!!"
    #         # else:
    #         #     error = "Mật khẩu không khớp!!!"
        except Exception as ex:
            error_ms = str(ex)
    return redirect(url_for(check_role_for_render(current_user), error_ms = error_ms))



if __name__ == "__main__":
    from clinicapp.admin import *
    app.run(debug=True)



