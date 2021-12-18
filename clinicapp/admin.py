from flask_admin import  BaseView, expose,AdminIndexView
from flask import  redirect
from flask_admin import Admin
from clinicapp import app, db, utils
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user, login_required
from clinicapp.models import *

class BackHome(BaseView):
    @expose('/')
    def index(self):
        return redirect('/')

class AboutUsView(BaseView):
    @expose("/")
    def index(seft):
        return seft.render('admin/about-us.html')
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')

class LogoutView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated
    @expose("/")
    def index(seft):
        logout_user()
        return redirect('/admin')

class MedicalBillView(ModelView):
    column_filters = ['create_date']
    column_labels = {
        'create_date':"Ngày lập phiếu khám",
        'diagnosis': "Chuẩn đoán",
        'symptom': "Triệu chứng"
    }
    column_exclude_list = ['user']
    column_searchable_list = ['diagnosis','symptom']
    form_columns = ('create_date','user','diagnosis','symptom')
    can_view_details = True;
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class MedicineView(ModelView):
    column_filters = ['name']
    column_labels = {
        'name':"Tên thuốc",
        'effect': "Tác dụng",
    }
    column_searchable_list = ['name','effect']
    form_columns = ('name','effect')
    can_view_details = True;
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class UserView(ModelView):
    column_filters = ['name','user_role','joined_date']
    column_labels = {
        'name':"Tên",
        'username': "Tên đăng nhập",
        'password': "Mật khẩu",
        'joined_date': "Ngày khởi tạo",
        'user_role': "Vai trò",
        'avatar':'Ảnh đại diện'
    }
    column_exclude_list = ['avatar','medical_bills']
    column_searchable_list = ['name','username','joined_date']
    form_columns = ('name','username','user_role')
    can_view_details = True;
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class Profit_stats_view(BaseView):
    @expose('/')
    @login_required
    def index(self):
        return self.render('admin/profit_stats.html', stats=utils.stat_profit())

class Medicine_stats_view(BaseView):
    @expose('/')
    @login_required
    def index(self):
        return self.render('admin/profit_stats.html', stats=utils.stat_medicine())

admin=Admin(app=app, name='Quản Trị Hệ Thống', template_mode='bootstrap4', index_view=MyAdminIndexView())
admin.add_view(UserView(User, db.session,name="Tài Khoản"))
admin.add_view(MedicalBillView(Medical_bill, db.session,name="Phiếu Khám"))
admin.add_view(MedicineView(Medicine, db.session,name="Danh Mục Thuốc"))
admin.add_view(AboutUsView(name = "Về Chúng Tôi"))
admin.add_view(Profit_stats_view(name="Thống kê doanh thu"))
admin.add_view(Medicine_stats_view(name="Thống kê tần suất sử dụng thuốc"))
admin.add_view(BackHome(name="Trở Về"))
admin.add_view(LogoutView(name="Đăng Xuất"))