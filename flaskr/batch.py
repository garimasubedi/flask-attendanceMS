import functools

from flask import (
    Flask,Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.auth import admin_login_required
from flaskr.db import get_db
from werkzeug.exceptions import abort
app = Flask(__name__)
bp = Blueprint('batch', __name__, url_prefix='/batch')
batch_index = "batch.index"


@bp.route('/list', methods=['GET'])
@admin_login_required
def index():
    db = get_db()
    batchs = db.execute(
        'SELECT * FROM batch'
    ).fetchall()
    return render_template('batch/list.html', batchs=batchs)


@bp.route('/add', methods=['GET','POST'])
@admin_login_required
def add():
    intake_list = ["spring","fall"]
    if request.method == 'POST':
        batch_year = request.form['txtBatchYear']
        batch_intake = request.form['txtBatchIntake']
        batch_name = request.form['txtBatchName']
        error = None

        if not batch_year:
            error = 'Batch year is required.'
        if not batch_intake:
            error = 'Batch intake is required.'
        if not batch_name:
            error = 'Batch name is required.'

        if error is not None:
            flash(error,"danger")
        else:
            db = get_db()
            cursor = db.cursor()
            
            cursor.execute(
                'Insert into batch(batch_year,batch_intake,batch_name)'
                ' VALUES (?, ?, ?);',
                (batch_year,batch_intake, batch_name)
            )
            
            flash("Successfully added new batch","success")
            return redirect(url_for(batch_index))
    return render_template('batch/add.html',intake_list=intake_list)


def get_batch(id):
    post = get_db().execute(
        'SELECT batch_year,batch_intake,batch_name'
        ' FROM batch '
        ' WHERE id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"batch id {id} doesn't exist.")
    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@admin_login_required
def update(id):
    batch = get_batch(id)
    intake_list = ["spring","fall"]
    if request.method == 'POST':
        batch_year = request.form['txtBatchYear']
        batch_intake = request.form['txtBatchIntake']
        batch_name = request.form['txtBatchName']
        error = None

        if not batch_year:
            error = 'Batch year is required.'
        if not batch_intake:
            error = 'Batch intake is required.'
        if not batch_name:
            error = 'Batch name is required.'

        if error is not None:
            flash(error,'danger')
        else:
            db = get_db()
            db.execute(
                'UPDATE batch SET batch_year = ?, batch_intake = ?, batch_name = ?'
                ' WHERE id = ?',
                (batch_year, batch_intake,batch_name, id)
            )
            db.commit()
            flash("Successfully updated batch","success")
            return redirect(url_for(batch_index))

    return render_template('batch/update.html', batch=batch,intake_list=intake_list)


@bp.route('/<int:id>/delete', methods=('POST',))
@admin_login_required
def delete(id):
    get_batch(id)
    db = get_db()
    db.execute('DELETE FROM batch WHERE id = ?', (id,))
    db.commit()
    flash("Successfully deleted batch","success")
    return redirect(url_for(batch_index))