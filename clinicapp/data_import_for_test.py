from clinicapp import db, utils, models
from datetime import datetime

if __name__ == '__main__':
    u1 = models.User(name="Thu", username="thu123", user_role=models.UserRole.ADMIN)
    u2 = models.User(name="Hieu", username="hieu123", user_role=models.UserRole.ADMIN)
    u3 = models.User(name="Huy", username="huy123", user_role=models.UserRole.ADMIN)
    u4 = models.User(name="Huynh", username="huynh123", user_role=models.UserRole.ADMIN)
    users = [u1, u2, u3, u4]
    for u in users:
        db.session.add(u)
    db.session.commit()

    mb1 = models.Medical_bill(user_id=1, diagnosis="abc", symptom="xyz")
    mb2 = models.Medical_bill(user_id=2, diagnosis="abc", symptom="xyz", create_date=datetime(2021, 12, 16))
    mb3 = models.Medical_bill(user_id=3, diagnosis="abc", symptom="xyz", create_date=datetime(2021, 12, 15))
    mb4 = models.Medical_bill(user_id=4, diagnosis="abc", symptom="xyz")
    mb5 = models.Medical_bill(user_id=3, diagnosis="abc", symptom="xyz", create_date=datetime(2021, 12, 15))
    mb6 = models.Medical_bill(user_id=4, diagnosis="abc", symptom="xyz", create_date=datetime(2021, 5, 20))
    mb7 = models.Medical_bill(user_id=2, diagnosis="abc", symptom="xyz", create_date=datetime(2021, 5, 19))
    mb8 = models.Medical_bill(user_id=4, diagnosis="abc", symptom="xyz", create_date=datetime(2021, 5, 17))
    mbs = [mb1, mb2, mb3, mb4, mb5, mb6, mb7, mb8]
    for mb in mbs:
        db.session.add(mb)
    db.session.commit()

    md1 = models.Medicine(name="acepron")
    md2 = models.Medicine(name="allerphast")
    md3 = models.Medicine(name="allvitamine")
    md4 = models.Medicine(name="avarino")
    mds = [md1, md2, md3, md4]
    for md in mds:
        db.session.add(md)
    db.session.commit()

    unt1 = models.Unit_tag(name='ống')
    unt2 = models.Unit_tag(name='vỉ')
    unt3 = models.Unit_tag(name='hộp')
    unts = [unt1, unt2, unt3]
    for unt in unts:
        db.session.add(unt)
    db.session.commit()

    mdu1 = models.Medicine_unit(unit_id=1, price=50000, medicine_id=1)
    mdu2 = models.Medicine_unit(unit_id=2, price=30000, medicine_id=1)
    mdu3 = models.Medicine_unit(unit_id=3, price=70000, medicine_id=2)
    mdu4 = models.Medicine_unit(unit_id=3, price=200000, medicine_id=2)
    mdu5 = models.Medicine_unit(unit_id=2, price=80000, medicine_id=3)
    mdu6 = models.Medicine_unit(unit_id=1, price=30000, medicine_id=3)
    mdu7 = models.Medicine_unit(unit_id=2, price=80000, medicine_id=4)
    mdu8 = models.Medicine_unit(unit_id=1, price=30000, medicine_id=3)
    mdus = [mdu1, mdu2, mdu3, mdu4, mdu5, mdu6, mdu7, mdu8]
    for mdu in mdus:
        db.session.add(mdu)
    db.session.commit()

    mbd1 = models.Medical_bill_detail(medical_bill_id=1,  medicine_unit_id=1, quantity=2)
    mbd2 = models.Medical_bill_detail(medical_bill_id=1, medicine_unit_id=2, quantity=1)
    mbd3 = models.Medical_bill_detail(medical_bill_id=2, medicine_unit_id=4, quantity=3)
    mbd4 = models.Medical_bill_detail(medical_bill_id=2, medicine_unit_id=6, quantity=10)
    mbd5 = models.Medical_bill_detail(medical_bill_id=2, medicine_unit_id=2, quantity=5)
    mbd6 = models.Medical_bill_detail(medical_bill_id=3, medicine_unit_id=3, quantity=8)
    mbd7 = models.Medical_bill_detail(medical_bill_id=3, medicine_unit_id=6, quantity=3)
    mbd8 = models.Medical_bill_detail(medical_bill_id=4, medicine_unit_id=5, quantity=9)
    mbd9 = models.Medical_bill_detail(medical_bill_id=4, medicine_unit_id=7, quantity=3)
    mbd10 = models.Medical_bill_detail(medical_bill_id=4, medicine_unit_id=8, quantity=15)
    mbd11 = models.Medical_bill_detail(medical_bill_id=5, medicine_unit_id=1, quantity=5)
    mbd12 = models.Medical_bill_detail(medical_bill_id=5, medicine_unit_id=4, quantity=7)
    mbd13 = models.Medical_bill_detail(medical_bill_id=6, medicine_unit_id=2, quantity=1)
    mbd14 = models.Medical_bill_detail(medical_bill_id=6, medicine_unit_id=3, quantity=4)
    mbd15 = models.Medical_bill_detail(medical_bill_id=7, medicine_unit_id=7, quantity=6)
    mbd16 = models.Medical_bill_detail(medical_bill_id=7, medicine_unit_id=4, quantity=3)
    mbd17 = models.Medical_bill_detail(medical_bill_id=8, medicine_unit_id=5, quantity=9)
    mbd18 = models.Medical_bill_detail(medical_bill_id=8, medicine_unit_id=8, quantity=3)
    mbds = [mbd1, mbd2, mbd3, mbd4, mbd5, mbd6, mbd7, mbd8, mbd9, mbd10, mbd11, mbd12, mbd13, mbd14, mbd15, mbd16, mbd17, mbd18]
    for mbd in mbds:
        db.session.add(mbd)
    db.session.commit()

    bills = utils.get_medical_bill_value()
    for b in bills:
        bill = models.Bill(medical_bill_id=b[0], value=b[1])
        db.session.add(bill)
    db.session.commit()

    db.create_all()