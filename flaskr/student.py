import functools

from flask import (
    Flask,Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.db import get_db
from flaskr.course import get_course_list
from werkzeug.exceptions import abort
import os
app = Flask(__name__)
bp = Blueprint('student', __name__, url_prefix='/student')
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
UPLOAD_PATH = PROJECT_ROOT+ '\\static\\img\\profile'
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
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
                image_path = '\static\img\profile\\'+image.filename

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
            db.execute(
                'Insert into student(first_name,last_name,email,course_id,batch_id,image)'
                ' VALUES (?, ?, ?, ?, ?, ?)',
                (first_name, last_name, email, course_id, batch_id,image_path)
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
            flash(error,'danger')
        else:
            db = get_db()
            db.execute(
                'UPDATE student SET first_name = ?, last_name = ?, email = ?, course_id = ?, batch_id = ?'
                ' WHERE id = ?',
                (first_name, last_name,email, id, course_id, batch_id)
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
    flash("Successfully deleted student","success")
    return redirect(url_for('student.index'))