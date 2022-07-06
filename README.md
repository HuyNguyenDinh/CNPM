# CNPM
## This project was developed with Python([Flask Framework](https://flask.palletsprojects.com/en/2.1.x/)) + HTML/CSS/JS + Jinja2 Template 
### We used [MySQL](https://www.mysql.com/downloads/) for Database of this project

#### How to run this project
##### 1. Clone this project to your pc (Of course)
##### 2. Setup Database
- Install MySQL on your pc at [here](https://www.mysql.com/downloads/)
- Create an empty schema for this project with charset/collation **utf8mp4/unicode_ci** and name is option
##### 3. Config Database connection
- Go to the folder you have clone
- Open the file __init__.py in the project
- Go to this line ```app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:hieu123@localhost/clinicapp?charset=utf8mb4'``` change this part ```root:hieu123@localhost/clinicapp``` with *root* is your Database username, *hieu123* is your Database user's password, *localhost* is the host where at your MySQL server stay (default is localhost and you may be not change this). *clinicapp* is the name of empty schema which you create at Setup Database step.
##### 4. Setup project
- Your pc need to install python3 at first (if you didn't install it please go [here](https://www.python.org/downloads/)
- You need install the python package for creating virtual environment for next step. For me, I choose **venv** so you need to open your terminal and run this script ```python -m pip install venv```
- When you got Python and Python package for creating virtual environment go to the folder you clone this project, and choose **Open with terminal** in the right click for next step
- Run this script in your terminal ```python -m venv venv``` to create the virtual environment for this project
- Then run this script to activate the Virtual environment ```.\venv\Script\activate``` (if you use git bash use this script instead ```. ./venv/Script/activate```)
- Now, the last step to setup Virtual environment. Run this script to get the Python packages for this project ```python -m pip install -r requirements.txt```
- Yolo, it's time for run this project. Run this script to create the models in Database ```python .\clinicapp\models.py```
- Next, run this script to create a bit data samples for app ```python .\clinicapp\data_import_for_test.py```
- Last, run this script to start app ```python .\clinicapp\index.py```

##### 5. Test App
- Go to **http://127.0.0.1:5000/** to see the App
- To sign in with Administrator use this account (username: huy123 - password: 1)
- To sign in with Nurse use this account (username: user1 - password: 1)
