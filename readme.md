# Attendance Tracker Project

## Overview
The Attendance Tracker project is designed to automate and streamline the process of tracking student attendance for educational institutions. It utilizes various technologies and libraries to provide features such as user authentication, attendance management, visualization of attendance data, and future integration plans for advanced features like face recognition and notifications.

## Features
### User Roles
* __Admin__: Can create, manage, and maintain accounts of students, teachers, and courses. Cannot take attendance.
* __Teacher__: Can take attendance of students, print, export, download, and email collected attendance.

### Authentication
* User authentication is implemented to ensure secure access to the system.
* Used __*Werkzeug*__ Library to hash passwords.

### Attendance Management
* Teachers can mark attendance for students.
* Attendance data is stored in a SQLite database.
* Attendance can be visualized through a dashboard, showing daily, weekly, and monthly attendance statistics.

### Export and Email
* Attendance data can be exported and downloaded in various formats.
* Teachers can email attendance reports directly from the application.



# Setting Up Code
## Clone repository
```sh
git clone https://github.com/garimasubedi/flask-attendanceMS.git
```

## Create a Virtual Environment
```sh
cd flask-attendanceMS
python -m venv venv
```

## Activate a Virtual Environment
### Using Bash/Linux shell
```sh
source venv/Scripts/activate 
```
### Using Command Prompt
```sh
venv\Scripts\activate.bat
```

## Install Packages
Inside Virtual Environment run:
```sh
pip install -r requirements.txt
```

## Initialize Database
To seed data in database for the first time run:

```sh
flask --app flaskr init-db
```

## Run Flask server
```sh
flask --app flaskr run --debug
```

### Voilà! Your web application is ready to serve. Simply click on the link to access it. 🚀🔗

## To Login as a Teacher
UserName: emily.johnson@yopmail.com
Password: master

## To Login as an Admin
UserName: admin@yopmail.com
Password: master