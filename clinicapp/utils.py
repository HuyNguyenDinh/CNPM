from clinicapp.models import Medical_bill, Medicine, Medicine_unit, Medical_bill_detail, Bill, Unit_tag, User, UserRole
from clinicapp import db
from sqlalchemy import func, extract, desc
from datetime import date, datetime
import hashlib

def add_medicine_unit():
    pass


def get_medical_bill_value(mb_id=None):
    bills = db.session.query(Medical_bill_detail.medical_bill_id,
                             func.sum(Medical_bill_detail.quantity * Medicine_unit.price)) \
                            .join(Medicine_unit, Medicine_unit.id == Medical_bill_detail.medicine_unit_id, isouter=True) \
                            .group_by(Medical_bill_detail.medical_bill_id)
    if mb_id:
        bills= bills.filter(Medical_bill.id.__eq__(int(mb_id)))
    return bills.all()

def get_bill_with_create_date(cd=None):
    bills = db.session.query(Medical_bill.create_date, func.sum(Bill.value))\
                    .join(Bill, Medical_bill.id == Bill.medical_bill_id, isouter=True)\
                    .group_by(Medical_bill.create_date)
    if cd:
        bills = bills.filter(extract('day', Medical_bill.create_date) == cd.day,\
                             extract('month', Medical_bill.create_date) == cd.month,\
                             extract('year', Medical_bill.create_date) == cd.year)
    return bills.all()

def get_last_month_in_bill():
    last_month_in_bill = db.session.query(Medical_bill.create_date).order_by(Medical_bill.create_date.desc()).first()
    last_month = int(last_month_in_bill[0].strftime("%m"))
    last_year = int(last_month_in_bill[0].strftime("%Y"))
    return {'month': last_month, 'year': last_year}

def stat_profit(month=None, year=None):
    bills = None
    if not month or not year:
        tempe = get_last_month_in_bill()
        month = tempe.get('month')
        year = tempe.get('year')
    if month and year:
        if type(month) is not int and month is not None:
            month = int(month)
        if type(year) is not int and year is not None:
            year = int(year)
        bills = db.session.query(Medical_bill.create_date, func.sum(Bill.value), func.count(Medical_bill.id)) \
                                    .join(Bill, Medical_bill.id == Bill.medical_bill_id) \
                                    .group_by(Medical_bill.create_date)\
                                    .filter(extract('month', Medical_bill.create_date) == month, \
                                            extract('year', Medical_bill.create_date) == year)
    if not bills:
        return None
    return bills.all()

def get_total_bill_in_month(month=None, year=None):
    tempe = stat_profit(month, year)
    total_profit=0
    if tempe:
        for t in tempe:
            total_profit += t[1]
    return total_profit

def stat_medicine(month=None, year=None):
    med_unit = None
    if not month or not year:
        tempe = get_last_month_in_bill()
        month = tempe.get('month')
        year = tempe.get('year')
    if month and year:
        if type(month) is not int and month is not None:
            month = int(month)
        if type(year) is not int and year is not None:
            year = int(year)
        med_unit = db.session.query(Medicine.name, Unit_tag.name, func.sum(Medical_bill_detail.quantity), Medicine_unit.unit_id,\
                                func.count(Medical_bill_detail.medicine_unit_id), Medical_bill.create_date)\
                                .join(Unit_tag, Unit_tag.id == Medicine_unit.unit_id)\
                                .join(Medicine, Medicine.id == Medicine_unit.medicine_id)\
                                .join(Medical_bill_detail, Medical_bill_detail.medicine_unit_id == Medicine_unit.id)\
                                .join(Medical_bill, Medical_bill_detail.medical_bill_id == Medical_bill.id)\
                                .group_by(Medicine.name, Unit_tag.name, Medical_bill.create_date) \
                                .filter(extract('month', Medical_bill.create_date) == month, \
                                        extract('year', Medical_bill.create_date) == year)
    if not med_unit:
        return None
    return med_unit.all()

def get_list_admin(user):
    dsqtv = []
    if user.is_authenticated:
        dsqtv = User.query.filter(User.user_role == UserRole.ADMIN, User.name != user.name).all()
    return dsqtv

def check_login(username , password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        return User.query.filter(User.username.__eq__(username.strip()), User.password.__eq__(password)).first()

def check_role(user):
    if user.is_authenticated:
        if user.user_role == UserRole.ADMIN:
            return "Quản trị viên hệ thống"
        elif user.user_role == UserRole.NURSE:
            return  "Y tá"
        return "Bác sĩ"
def find_path(user):
    if user.is_authenticated:
        if user.user_role == UserRole.DOCTOR:
            return "doctor_view"
        elif user.user_role == UserRole.NURSE:
            return  "nurse_view"
        return "return_admin_page"
