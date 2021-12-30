from sqlalchemy import Column, Integer, String, Enum, Float, Boolean, Date, ForeignKey, Text, Table
from sqlalchemy.orm import relationship
from clinicapp import db, utils
from datetime import datetime
from enum import Enum as UserEnum
from flask_login import UserMixin, current_user
import hashlib

class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class UserRole(UserEnum):
    ADMIN = 1
    NURSE = 2
    DOCTOR = 3


class User(BaseModel, UserMixin):
    __tablename__='user'
    __table_args__ = {'extend_existing': True}
    name = Column(String(100), nullable=False)
    username = Column(String(20), nullable=False, unique=False)
    password = Column(String(255), nullable=False, default=str(hashlib.md5(str(1).encode("utf-8")).hexdigest()))
    avatar = Column(String(100), default='')
    joined_date = Column(Date, default=datetime.now())
    user_role = Column(Enum(UserRole), default=UserRole.NURSE)
    medical_bills = relationship('Medical_bill', backref='user', lazy=True)

    def __str__(self):
        return self.name


class Medical_bill(BaseModel):
    __tablename__ = 'medical_bill'
    __table_args__ = {'extend_existing': True}
    create_date = Column(Date, default=datetime.now())
    diagnosis = Column(Text)
    symptom = Column(Text)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    medical_bill_detail = relationship('Medical_bill_detail', backref='medical_bill', lazy=True)
    bill = relationship('Bill', backref='medical_bill', lazy=True)


class Bill(BaseModel):
    __tablename__ = 'bill'
    __table_args__ = {'extend_existing': True}
    value = Column(Float, default=0)
    medical_bill_id = Column(Integer, ForeignKey(Medical_bill.id), nullable=False)


class Medicine(BaseModel):
    __tablename__ = 'medicine'
    __table_args__ = {'extend_existing': True}
    name = Column(String(255), nullable=False)
    effect = Column(Text)
    medicine_units = relationship('Medicine_unit', backref='medicine', lazy=True)

    def __str__(self):
        return self.name


class Unit_tag(BaseModel):
    __tablename__ = 'unit_tag'
    __table_args__ = {'extend_existing': True}
    name = Column(String(50), nullable=False, unique=True)
    medicine_units = relationship('Medicine_unit', backref='unit_tag', lazy=True)

    def __str__(self):
        return self.name

class Medicine_unit(BaseModel):
    __tablename__ = 'medicine_unit'
    __table_args__ = {'extend_existing': True}
    unit_id = Column(Integer, ForeignKey(Unit_tag.id), nullable=False)
    price = Column(Float, default=0)
    medicine_id = Column(Integer, ForeignKey(Medicine.id), nullable=False)
    medical_bill_details = relationship('Medical_bill_detail', backref='medicine_unit', lazy=True)

    def __str__(self):
        return str(self.medicine) + "-" + str(self.unit_tag)

class Medical_bill_detail(db.Model):
    __tablename__ = 'medicine_bill_detail'
    __table_args__ = {'extend_existing': True}
    medical_bill_id = Column(Integer, ForeignKey(Medical_bill.id), nullable=False, primary_key=True)
    medicine_unit_id = Column(Integer, ForeignKey(Medicine_unit.id), nullable=False, primary_key=True)
    quantity = Column(Integer, default=0)

    def __str__(self):
        return "id:" + str(self.medical_bill_id) + "-" + self.medicine_unit.medicine + "-" + self.medicine_unit.unit_tag

if __name__ == '__main__':
    db.create_all()