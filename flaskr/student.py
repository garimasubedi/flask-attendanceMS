import functools

from flask import (
    Flask,Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.course import get_course_list
app = Flask(__name__)
bp = Blueprint('student', __name__, url_prefix='/student')
from flaskr.db import get_db
from werkzeug.exceptions import abort

@bp.route('/list', methods=['GET'])
def index():
    db = get_db()
    students  = db.execute(
        'SELECT * FROM student'
    ).fetchall()
    return render_template('student/list.html', students=students)

@bp.route('/add', methods=['GET','POST'])

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
        error = None

        if not first_name:
            error = 'First name is required.'
        if not last_name:
            error = 'Last name is required.'
        if not email:
            error = 'Email is required.'

        if error is not None:
            flash(error,"danger")
        else:
            db = get_db()
            db.execute(
                'Insert into student(first_name,last_name,email)'
                ' VALUES (?, ?, ?)',
                (first_name, last_name, email)
            )
            db.commit()
            flash("Successfully added new student","success")
            return redirect(url_for('student.index'))
    return render_template('student/add.html',course_list=course_list,batch_list= batch_list)


def get_student(id):
    post = get_db().execute(
        'SELECT first_name, last_name, email'
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
    if request.method == 'POST':
        first_name = request.form['txtFirstName']
        last_name = request.form['txtLastName']
        email = request.form['txtEmail']
        error = None

        if not first_name:
            error = 'First name is required.'
        if not last_name:
            error = 'Last name is required.'
        if not email:
            error = 'Email is required.'

        if error is not None:
            flash(error,'danger')
        else:
            db = get_db()
            db.execute(
                'UPDATE student SET first_name = ?, last_name = ?, email = ?'
                ' WHERE id = ?',
                (first_name, last_name,email, id)
            )
            db.commit()
            flash("Successfully updated student","success")
            return redirect(url_for('student.index'))

    return render_template('student/update.html', student=student)

@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    get_student(id)
    db = get_db()
    db.execute('DELETE FROM student WHERE id = ?', (id,))
    db.commit()
    flash("Successfully deleted student","success")
    return redirect(url_for('student.index'))