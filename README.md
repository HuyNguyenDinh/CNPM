# Clinic Managing Web Application
## Deploy at http://165.22.57.62/ and http://www.nguyendinhhuy.tech/
## This project was developed with Python3([Flask Framework](https://flask.palletsprojects.com/en/2.1.x/)) + HTML/CSS/JS + Jinja2 Template 
### We used [MySQL](https://www.mysql.com/downloads/) for Database of this project

#### How to run this project
##### 1. Clone this project to your pc (Of course)
##### 2. Change your current directory to this project on your local machine (Terminal or PowerShell on Window)
##### 3. Setup Database
- Run sql script `mysql_script.sql` with 'root' role in MySQL server to create database and user for application (For windows)
- If you are using linux/ubuntu just run 
```
source ./clinicapp/mysql_script.sh
```
!Important check your environment variables for `$DB_HOST $DB_NAME $DB_USER $DB_PASSWORD` if you are using or project cannot connect to database. 
##### 4. Setup project
- Your pc need to install python3 at first (if you didn't install it please go [here](https://www.python.org/downloads/)
- You need install the python package for creating virtual environment for next step. For me, I choose **venv** so you need to open your terminal and run this script
```
python -m pip install venv
```
- When you got Python and Python package for creating virtual environment go to the folder you clone this project, and choose **Open with terminal** in the right click for next step
- Run this script in your terminal to create the virtual environment for this project 
```
python -m venv venv
``` 
- Then run this script to activate the Virtual environment 
```
.\venv\Script\activate
``` 
- If you use git bash use this script instead 
```
. ./venv/Script/activate
```
- Now, the last step to setup Virtual environment. Run this script to get the Python packages for this project 
```
python -m pip install -r requirements.txt
```
- Yolo, it's time for run this project. Run this script to create the models in Database 
```
python -m clinicapp.models
```
- Next, run this script to create a bit data samples for app 
```
python -m clinicapp.data_import_for_test
```
- Last, run this script to start app 
```
python -m clinicapp.index
```

##### 5. Test App
- Go to **http://127.0.0.1:5000/** to see the App
- To sign in with *Administrator* use this account (username: huy123 - password: 1)
- To sign in with *Nurse* use this account (username: user1 - password: 1)
