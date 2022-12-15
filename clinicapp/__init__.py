from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY',"@pdot324g942##$%$^$@%#%^%$^*&*(&)(3jifgj34-94")
db_host = os.getenv('DB_HOST', 'localhost')
db_port = os.getenv('DB_PORT', 3306)
db_name = os.getenv('DB_NAME', 'clinicapp')
db_user = os.getenv('DB_USER', 'clinicapp')
db_password = os.getenv('DB_PASSWORD', 'clinicapp')
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}?charset=utf8mb4"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
login = LoginManager(app=app)
login.init_app(app)
cloudinary.config(
    cloud_name = os.getenv('CLOUD_NAME','dec25'),
    api_key = os.getenv('API_KEY' ,'752682513512722'),
    api_secret = os.getenv('API_SECRET' ,'P6Sb5YZCvBFpcMYAyumZnIpewNU')
)
db = SQLAlchemy(app=app)
