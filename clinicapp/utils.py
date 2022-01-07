from clinicapp.models import Medical_bill, Medicine, Medicine_unit, Medical_bill_detail, Bill, Unit_tag, User, UserRole,\
    Examination, Patient, Exam_patient, Sex
from clinicapp import db
from sqlalchemy import func, extract, desc, alias, update
import hashlib

def get_medical_bill_value(mb_id=None):
    bills = db.session.query(Medical_bill_detail.medical_bill_id,
                             func.sum(Medical_bill_detail.quantity * Medicine_unit.price)) \
                            .join(Medicine_unit, Medicine_unit.id == Medical_bill_detail.medicine_unit_id, isouter=True) \
                            .group_by(Medical_bill_detail.medical_bill_id)
    if mb_id:
        bills = bills.filter(Medical_bill_detail.medical_bill_id.__eq__(int(mb_id)))
        return bills.first()
    return bills.all()

def get_bill_with_create_date(cd=None, id=None):
    bills = db.session.query(Medical_bill.create_date, func.sum(Bill.value))\
                    .join(Bill, Medical_bill.id == Bill.medical_bill_id, isouter=True)\
                    .group_by(Medical_bill.create_date)
    if cd:
        temp = cd.split('-')
        year = temp[0]
        month = temp[1]
        day = temp[2]
        bills = bills.filter(extract('day', Medical_bill.create_date) == day,\
                             extract('month', Medical_bill.create_date) == month,\
                             extract('year', Medical_bill.create_date) == year)
    return bills.all()

def get_last_month_in_bill():
    last_month_in_bill = db.session.query(Medical_bill.create_date).order_by(Medical_bill.create_date.desc()).first()
    last_month = last_month_in_bill[0].strftime("%m")
    last_year = last_month_in_bill[0].strftime("%Y")
    return {'month': last_month, 'year': last_year}

def stat_profit(month=None, year=None):
    bills = db.session.query(Medical_bill.create_date, func.sum(Bill.value), func.count(Medical_bill.id)) \
                    .join(Bill, Medical_bill.id == Bill.medical_bill_id) \
                    .group_by(Medical_bill.create_date)
    if not month or not year:
        tempe = get_last_month_in_bill()
        month = tempe.get('month')
        year = tempe.get('year')
    if month and year:
        if type(month) is not int and month is not None:
            month = int(month)
        if type(year) is not int and year is not None:
            year = int(year)
        bills = bills.filter(extract('month', Medical_bill.create_date) == month, \
                                            extract('year', Medical_bill.create_date) == year)
    if len(bills.all()) <= 0:
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
    med_unit = db.session.query(Medicine.name, Unit_tag.name, func.sum(Medical_bill_detail.quantity),\
                                Medicine_unit.unit_id, \
                                func.count(Medical_bill_detail.medicine_unit_id), Medical_bill.create_date) \
                                .join(Unit_tag, Unit_tag.id == Medicine_unit.unit_id) \
                                .join(Medicine, Medicine.id == Medicine_unit.medicine_id) \
                                .join(Medical_bill_detail, Medical_bill_detail.medicine_unit_id == Medicine_unit.id) \
                                .join(Medical_bill, Medical_bill_detail.medical_bill_id == Medical_bill.id) \
                                .group_by(Medicine.name, Unit_tag.name, Medical_bill.create_date)
    if not month or not year:
        tempe = get_last_month_in_bill()
        month = tempe.get('month')
        year = tempe.get('year')
    if month and year:
        if type(month) is not int and month is not None:
            month = int(month)
        if type(year) is not int and year is not None:
            year = int(year)
        med_unit = med_unit.filter(extract('month', Medical_bill.create_date) == month, \
                                    extract('year', Medical_bill.create_date) == year)
    if len(med_unit.all()) <= 0:
        return None
    return med_unit.all()

def count_patient_in_exam(exam_date=None):
    count = db.session.query(func.count(Exam_patient.c.patient_id)) \
                            .join(Examination, Examination.id == Exam_patient.c.exam_id)
    if exam_date:
        temp = exam_date.split('-')
        year = temp[0]
        month = temp[1]
        day = temp[2]
        count = count.filter(extract('day', Examination.date) == day,\
                                        extract('month', Examination.date) == month, \
                                        extract('year', Examination.date) == year)
    if len(count.all()) <= 0:
        return None
    return count.first()[0]

def get_patient_in_exam(exam_date=None, doctor=False, sub=None):
    pati = db.session.query(Examination.date, Patient.last_name, Patient.first_name, Patient.sex, Patient.date_of_birth,\
                            Patient.phone_number, Patient.id, Examination.id, Examination.apply)\
                            .join(Exam_patient, Exam_patient.c.patient_id == Patient.id) \
                            .join(Examination, Examination.id == Exam_patient.c.exam_id)
    if exam_date:
        temp = exam_date.split('-')
        year = temp[0]
        month = temp[1]
        day = temp[2]
        pati = pati.filter(extract('day', Examination.date) == day, \
                                        extract('month', Examination.date) == month, \
                                        extract('year', Examination.date) == year)
        if doctor:
            pati = pati.filter(Examination.apply.__eq__(True))
        if len(pati.all()) <= 0:
            return None
        if sub:
            return pati
        else:
            return pati.all()
    else:
        return None

def get_last_date_of_exam(doctor=False):
    temp = db.session.query(Examination.date, Examination.apply).order_by(Examination.date.desc())
    if doctor:
        temp = temp.filter(Examination.apply.__eq__(True)).first()
    else:
        temp = temp.first()
    day = temp[0].strftime("%d")
    month = temp[0].strftime("%m")
    year = temp[0].strftime("%Y")
    return {'day': day, 'month': month, 'year': year}

def get_status_of_exam(exam_date=None):
    if exam_date:
        temp = exam_date.split('-')
        year = temp[0]
        month = temp[1]
        day = temp[2]
        status = db.session.query(Examination.apply, Examination.date)\
                                .filter(extract('day', Examination.date) == day, \
                                        extract('month', Examination.date) == month, \
                                        extract('year', Examination.date) == year)
        if len(status.all()) > 0:
            return status.first()[0]
        else:
            return False
    else:
        return None

def change_status_examination(exam_id=None):
    if exam_id:
        Examination.query.filter_by(id=int(exam_id)).update(dict(apply=True))
        db.session.commit()
        return True
    else:
        return False

def get_medical_bill_of_patient_in_an_exam(pte_id=None, exam_date=None, sub=None):
    mb = db.session.query(Patient.last_name, Patient.first_name, Medical_bill.create_date, Medical_bill.id) \
                        .join(Medical_bill, Patient.id == Medical_bill.patient_id)
    if pte_id:
        mb = mb.filter(Patient.id.__eq__(int(pte_id)))
    if exam_date:
        temp = exam_date.split('-')
        year = temp[0]
        month = temp[1]
        day = temp[2]
        mb = mb.filter(extract('day', Medical_bill.create_date) == day,\
                                extract('month', Medical_bill.create_date) == month,\
                                extract('year', Medical_bill.create_date) == year)
    if len(mb.all()) <= 0:
        if sub:
            return mb
        else:
            return mb.all()
    else:
        return None

def get_bill_from_medicall_bill_in_day(exam_date=None):
    bills = db.session.query(Medical_bill.create_date, Patient.last_name, Patient.first_name,\
                             Patient.date_of_birth, Bill.value, Bill.pay,Bill.id)\
                            .join(Bill, Bill.medical_bill_id == Medical_bill.id)\
                            .join(Patient, Medical_bill.patient_id == Patient.id)
    if exam_date:
        temp = exam_date.split('-')
        year = temp[0]
        month = temp[1]
        day = temp[2]
        bills = bills.filter(extract('day', Medical_bill.create_date) == day, \
                       extract('month', Medical_bill.create_date) == month, \
                       extract('year', Medical_bill.create_date) == year)
    if len(bills.all()) > 0:
        return bills.all()
    else:
        return None

def get_bill(id=None):
    if id:
        temp = db.session.query(Bill.id, Bill.value, Patient.last_name, Patient.first_name, Patient.phone_number,\
                                Patient.date_of_birth, Medical_bill.create_date)\
                                .join(Medical_bill, Medical_bill.id == Bill.medical_bill_id)\
                                .join(Patient, Patient.id == Medical_bill.patient_id)\
                                .filter(Bill.id.__eq__(int(id)))
        return temp.first()
    else:
        return None

def pay_bill(id=None):
    if id:
        Bill.query.filter_by(id=int(id)).update(dict(pay=True))
        db.session.commit()
        return True
    else:
        return False

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
            return "Y tá"
        return "Bác sĩ"

def check_sex(user):
    if user.is_authenticated:
        if user.sex == Sex.MALE:
            return "Nam"
        elif user.sex == Sex.FEMALE:
            return  "Nữ"
        return "Không muốn trả lời"

