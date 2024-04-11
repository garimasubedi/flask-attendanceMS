import functools

from flask import (
    Flask,Blueprint, flash, g, redirect, render_template, request, session, url_for
)


from flaskr.db import get_db
from flaskr.course import get_course_list
from werkzeug.exceptions import abort
import os
import cv2
import numpy as np
import shutil
import face_recognition
import numpy as np
import pandas as pd

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

UPLOAD_PATH = PROJECT_ROOT+ '\static\img\profile'

app = Flask(__name__)
bp = Blueprint('student', __name__, url_prefix='/student')
app.config['UPLOAD_FOLDER'] = UPLOAD_PATH

@bp.route('/list', methods=['GET'])
def index():
    db = get_db()
    students  = db.execute(
        'SELECT s.id, s.first_name, s.last_name, s.email, c.course_name, b.batch_year batch_name FROM student s'
        ' JOIN course c ON c.id = s.course_id'
        ' JOIN batch b on b.id = s.batch_id'
    ).fetchall()
    return render_template('student/list.html', students=students)

def get_batch_list():
    batchs = get_db().execute(
        'SELECT id,batch_year,batch_name'
        ' FROM batch '
    ).fetchall()
    return batchs
@bp.route('/add', methods=['GET','POST'])
def add():
    course_list = get_course_list()
    batch_list = get_batch_list()
    if request.method == 'POST':
        first_name = request.form['txtFirstName']
        last_name = request.form['txtLastName']
        email = request.form['txtEmail']
        batch_id = request.form['slcBatch']
        course_id = request.form['slcCourse']
        error = None
        if 'txtFileUpload' in request.files:
            image = request.files['txtFileUpload']
            if image.filename != '':
                temp_image_path = app.config['UPLOAD_FOLDER'] + '\profiletemp\\'+image.filename
                #print(temp_image_path,'UP:P ROOT PATH')
                image.save(temp_image_path)
                #print(temp_image_path,'temp image path')

                # img = cv2.imread(temp_image_path)
                # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                # # Load the pre-trained Haar cascade for face detection
                # face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

                # # Detect faces in the image
                # faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

                # # Count the number of faces detected
                # num_faces = len(faces)
                # print(num_faces ,'number of faces')
                # if num_faces <= 0:
                #     error = "No person face in image"
                # elif num_faces > 1:
                #     error = "More than one face is present."
                # else:
                #     image.save(os.path.join(app.config['UPLOAD_FOLDER'], 'hell.jpg'))
                #     image_path = '\static\img\profile\\'+'hell.jpg'
            else:
                error = 'Image is required.'

        else:
            error = 'Image is required.'

        if not first_name:
            error = 'First name is required.'
        if not last_name:
            error = 'Last name is required.'
        if not email:
            error = 'Email is required.'
        if not batch_id or batch_id == '0':
            error = 'Batch is required.'
        if not course_id or course_id == '0':
            error = 'Course is required.'
          

        if error is not None:
            flash(error,"danger")
        else:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                'Insert into student(first_name,last_name,email,course_id,batch_id,image)'
                ' VALUES (?, ?, ?, ?, ?, ?)',
                (first_name, last_name, email, course_id, batch_id,'')
            )
            db.commit()
            inserted_id = cursor.lastrowid
#=============================================================================================
            img_name = str(inserted_id)+'.jpg'
            profile_img_path = app.config['UPLOAD_FOLDER'] + '\\'+img_name
            shutil.copy(temp_image_path, profile_img_path)

#=============================================================================================
#=============================================================================================
            img = cv2.imread(profile_img_path)
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_encoding = face_recognition.face_encodings(rgb_img)[0]
            df = pd.read_csv(
                    os.path.join(PROJECT_ROOT, 'ml\encoding\encodings.csv'))
            en = df["Encodings"].tolist()
            n = df["Persons"].tolist()
            en.append(img_encoding)
            n.append(inserted_id)
            df = pd.DataFrame({"Persons": n, "Encodings": en})
            df.to_csv(
                    os.path.join(PROJECT_ROOT, 'ml\encoding\encodings.csv'), index=False)
#=============================================================================================
#=============================================================================================


            cursor.execute(
                'UPDATE student set image = ?'
                ' WHERE id = ?',
                ('/static/img/profile/'+str(inserted_id)+'.jpg',inserted_id)
            )

            db.commit()
            flash("Successfully added new student","success")
            return redirect(url_for('student.index'))
    return render_template('student/add.html',course_list=course_list,batch_list= batch_list)


def get_student(id):
    post = get_db().execute(
        'SELECT first_name, last_name, email, course_id, batch_id, image'
        ' FROM student '
        ' WHERE id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Student id {id} doesn't exist.")
    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    student = get_student(id)
    course_list = get_course_list()
    batch_list = get_batch_list()
    if request.method == 'POST':
        first_name = request.form['txtFirstName']
        last_name = request.form['txtLastName']
        email = request.form['txtEmail']
        batch_id = request.form['slcBatch']
        course_id = request.form['slcCourse']
        error = None
        profile_img_path = None
        if 'txtFileUpload' in request.files:
            print('txtfilepath')
            image = request.files['txtFileUpload']
            if image.filename != '':
                print('txtfilepath dyddd')
                csv_file_path = os.path.join(PROJECT_ROOT, 'ml\encoding\encodings.csv')
                img_name = str(id)+'.jpg'
                profile_img_path = app.config['UPLOAD_FOLDER'] + '\\'+img_name
                image.save(profile_img_path)
                img = cv2.imread(profile_img_path)
                rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img_encoding = face_recognition.face_encodings(rgb_img)[0]
                df = pd.read_csv(csv_file_path)
                id_exists = id in df['Persons'].values
                if id_exists:
                    index_to_update = df.index[df['Persons'] == id][0] 
                    df.at[index_to_update, 'Encodings'] = img_encoding
                else:
                    en = df["Encodings"].tolist()
                    n = df["Persons"].tolist()
                    en.append(img_encoding)
                    n.append(id)
                    df = pd.DataFrame({"Persons": n, "Encodings": en})
                df.to_csv(csv_file_path, index=False)
                
            else:
                error = 'Image is required.'
        if not first_name:
            error = 'First name is required.'
        if not last_name:
            error = 'Last name is required.'
        if not email:
            error = 'Email is required.'
        if not batch_id or batch_id == '0':
            error = 'Batch is required.'
        if not course_id or course_id == '0':
            error = 'Course is required.'
        print(profile_img_path)
        if error is not None:
            flash(error,'danger')
        else:
            db = get_db()
            db.execute(
                'UPDATE student SET first_name = ?, last_name = ?, email = ?, course_id = ?, batch_id = ?, image = ?'
                ' WHERE id = ?',
                (first_name, last_name,email, course_id, batch_id, '/static/img/profile/'+str(id)+'.jpg', id)
            )
            db.commit()
            flash("Successfully updated student","success")
            return redirect(url_for('student.index'))

    return render_template('student/update.html', student=student,course_list=course_list,batch_list= batch_list)

@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    get_student(id)
    db = get_db()
    db.execute('DELETE FROM student WHERE id = ?', (id,))
    db.commit()
    csv_file_path = os.path.join(PROJECT_ROOT, 'ml\encoding\encodings.csv')
    df = pd.read_csv(csv_file_path)
    index_to_delete = df[df['Persons'] == id].index
    df.drop(index_to_delete, inplace=True)
    flash("Successfully deleted student","success")
    return redirect(url_for('student.index'))