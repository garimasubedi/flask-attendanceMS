import functools

from flask import (
    Flask,Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.auth import admin_login_required
from flaskr.db import get_db
from werkzeug.exceptions import abort

app = Flask(__name__)
bp = Blueprint('course', __name__, url_prefix='/course')


@bp.route('/list', methods=['GET'])
@admin_login_required
def index():
    db = get_db()
    courses  = db.execute(
        'SELECT c.id,c.course_name,GROUP_CONCAT(s.subject_name,",") subjects FROM course c'
        ' LEFT JOIN course_subject cs on c.id = cs.course_id'
        ' LEFT JOIN subject s on s.id = cs.subject_id'
        ' GROUP BY c.id'
    ).fetchall()
    return render_template('course/list.html', courses=courses)


@bp.route('/<int:id>/list', methods=['GET'])
@admin_login_required
def subject_list(id):
    db = get_db()
    subjects  = db.execute(
        'SELECT cs.id,c.id cid,c.course_name,s.subject_name,s.subject_code,t.first_name,t.last_name FROM course c'
        ' JOIN course_subject cs on c.id = cs.course_id'
        ' JOIN subject s on s.id = cs.subject_id'
        ' JOIN teacher t on s.teacher_id = t.id'
        ' WHERE c.id = ?',(id,)
    ).fetchall()
    return render_template('course/subject_list.html', subjects=subjects)


def get_subject(id):
    subject = get_db().execute(
        'SELECT id'
        ' FROM course_subject '
        ' WHERE id = ?',
        (id,)
    ).fetchone()

    if subject is None:
        abort(404, f"subject id {id} doesn't exist.")
    return subject


@bp.route('/<int:cid>/<int:id>/delete', methods=('POST',))
@admin_login_required
def delete(cid,id):
    get_subject(id)
    db = get_db()
    db.execute('DELETE FROM course_subject WHERE id = ?', (id,))
    db.commit()
    flash("Successfully deleted subject","success")
    return redirect(url_for('course.subject_list',id=cid))


def check_exist(course_id,subject_id):
    subject = get_db().execute(
        'SELECT id'
        ' FROM course_subject '
        ' WHERE course_id = ? AND subject_id = ?',
        (course_id,subject_id)
    ).fetchone()

    if subject is not None:
        flash('already exist',"danger")
    return subject


def get_course_list():
    post = get_db().execute(
        'SELECT id,course_name'
        ' FROM course '
    ).fetchall()

    return post


def get_subject_list():
    post = get_db().execute(
        'SELECT id,subject_name'
        ' FROM subject '
    ).fetchall()

    return post


@bp.route('/add', methods=['GET','POST'])
@admin_login_required
def add():
    course_list = get_course_list()
    subject_list = get_subject_list()
    if request.method == 'POST':
        course_id = request.form['slcCourse']
        subject_id = request.form['slcSubject']
        error = None

        if not course_id or course_id == '0':
            error = 'Course is required.'
        if not subject_id or subject_id == '0':
            error = 'Subject is required.'

        if error is not None:
            flash(error,"danger")
        
        else:
            if check_exist(course_id,subject_id) is None:
                db = get_db()
                cursor = db.cursor()
                
                cursor.execute(
                    'Insert into course_subject(course_id,subject_id)'
                    ' VALUES (?, ?);',
                    (course_id,subject_id)
                )
                db.commit()
                flash("Successfully added new subject to course","success")
                return redirect(url_for('course.index'))
    return render_template('course/add_subject.html',course_list=course_list,subject_list=subject_list)