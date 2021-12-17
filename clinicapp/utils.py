from clinicapp.models import Medical_bill, Medicine, Medicine_unit, Medical_bill_detail, Bill
from clinicapp import db
from sqlalchemy import func, extract, desc
from datetime import date, datetime

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


def stat_profit():
    bills = db.session.query(Medical_bill.create_date, func.sum(Bill.value)) \
        .join(Bill, Medical_bill.id == Bill.medical_bill_id, isouter=True) \
        .group_by(Medical_bill.create_date)
    last_bill = bills.order_by(Medical_bill.create_date.desc()).first()
    if last_bill:
        month = int(last_bill[0].strftime("%m"))
        year = int(last_bill[0].strftime("%Y"))
        bills = bills.filter(extract('month', Medical_bill.create_date) == month, \
                             extract('year', Medical_bill.create_date) == year)
    else:
        pass
    return bills.all()

def stat_medicine():
    pass