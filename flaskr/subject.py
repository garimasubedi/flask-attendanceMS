import functools

from flask import (
    Flask,Blueprint, flash, g, redirect, render_template, request, session, url_for
)

app = Flask(__name__)
bp = Blueprint('subject', __name__, url_prefix='/subject')
from flaskr.db import get_db
from werkzeug.exceptions import abort
from flaskr.auth import admin_login_required

@bp.route('/list', methods=['GET'])
@admin_login_required
def index():
    db = get_db()
    subjects  = db.execute(
        '''SELECT s.id, t.first_name, t.last_name,s.subject_name,s.subject_code
            FROM  subject s
            JOIN teacher t ON t.id = s.teacher_id'''
    ).fetchall()
    
    return render_template('subject/list.html', subjects=subjects)
def get_teacher_list():
    post = get_db().execute(
        'SELECT id,first_name, last_name, email'
        ' FROM teacher '
    ).fetchall()

    return post

@bp.route('/add', methods=['GET','POST'])
@admin_login_required
def add():
    if request.method == 'POST':
        subject_name = request.form['txtSubjectName']
        subject_code = request.form['txtSubjectCode']
        teacher_id = request.form['slcTeacher']
        error = None

        if not subject_name:
            error = 'Subject name is required.'
        if not subject_code:
            error = 'Subject code is required.'
        if not teacher_id or teacher_id == '0':
            error = 'Teacher is required.'

        if error is not None:
            flash(error,"danger")
        else:
            db = get_db()
            db.execute(
                'Insert into subject(subject_name, subject_code, teacher_id)'
                ' VALUES (?, ?, ?)',
                (subject_name, subject_code, teacher_id)
            )
            db.commit()
            flash("Successfully added new subject","success")
            return redirect(url_for('subject.index'))
    teacher_list = get_teacher_list()
    return render_template('subject/add.html',teacher_list= teacher_list)

def get_subject(id):
    post = get_db().execute(
        'SELECT subject_name, subject_code, teacher_id'
        ' FROM subject '
        ' WHERE id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")
    return post
def get_subject_list_ddl():
   
    subjects = get_db().execute(
         'SELECT s.id, s.subject_name,s.subject_code'
         ' FROM  subject s'
         ' JOIN teacher t ON t.id = s.teacher_id where t.user_id = ?',(g.user['id'],)
    ).fetchall()
    
    return subjects

@bp.route('/<int:id>/delete', methods=('POST',))
@admin_login_required
def delete(id):
    get_subject(id)
    db = get_db()
    db.execute('DELETE FROM subject WHERE id = ?', (id,))
    db.commit()
    flash("Successfully deleted subject","success")
    return redirect(url_for('subject.index'))


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@admin_login_required
def update(id):
    subject = get_subject(id)
    teacher_list = get_teacher_list()
    if request.method == 'POST':
        subject_name = request.form['txtSubjectName']
        subject_code = request.form['txtSubjectCode']
        teacher_id = request.form['slcTeacher']
        error = None

        if not subject_name:
            error = 'Subject name is required.'
        if not subject_code:
            error = 'Subject code is required.'
        if not teacher_id or teacher_id == '0':
            error = 'Teacher is required.'

        if error is not None:
            flash(error,'danger')
        else:
            db = get_db()
            db.execute(
                'UPDATE subject SET subject_name = ?, subject_code = ?, teacher_id = ?'
                ' WHERE id = ?',
                (subject_name, subject_code,teacher_id, id)
            )
            db.commit()
            flash("Successfully updated subject","success")
            return redirect(url_for('subject.index'))

    return render_template('subject/update.html', subject=subject,teacher_list=teacher_list)