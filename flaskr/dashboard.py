import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.auth import login_required
from flaskr.db import get_db
bp = Blueprint('dashboard', __name__, url_prefix='')


@bp.route('/', methods=['GET'])
@login_required
def index():
    class_count = total_class()
    student_count = total_student()
    subject_count = total_subject()
    daily_attendance_data = daily_attendance()
    weekly_attendance_data = weekly_attendance()
    monthly_attendance_data = monthly_attendance()

    return render_template('dashboard/index.html',
                           student_count = student_count,
                           class_count = class_count,
                           subject_count = subject_count,
                           daily_attendance_data = daily_attendance_data,
                           weekly_attendance_data = weekly_attendance_data,
                           monthly_attendance_data = monthly_attendance_data)


def total_student():
    students = get_db().execute(
        'SELECT COUNT(*) AS total_students FROM student'
    ).fetchone()
    return students


def total_class():
    classes = get_db().execute(
        'SELECT COUNT(DISTINCT attendance.id) AS total_classes FROM attendance'
    ).fetchone()
    return classes


def total_subject():
    subjects = get_db().execute(
        'SELECT COUNT(DISTINCT id) AS total_subjects FROM subject;'
    ).fetchone()
    return subjects


def daily_attendance():
    daily_attendances = get_db().execute(
        'SELECT attendance_date, COUNT(DISTINCT id) Count FROM attendance GROUP BY attendance_date'
    ).fetchall()
    labels = [attendance[0] for attendance in daily_attendances]
    counts = [attendance[1] for attendance in daily_attendances]
    response = {'labels':labels,'counts':counts}
    return response


def weekly_attendance ():
    weekly_attendances  = get_db().execute(
        '''SELECT start_date || ' - ' || end_date AS week_range, COUNT(DISTINCT a.id) Count
            FROM (SELECT strftime("%W", attendance_date) AS week_number,MIN(attendance_date) AS start_date,MAX(attendance_date) AS end_date
            FROM attendance GROUP BY week_number) w 
            JOIN attendance a ORDER BY start_date;'''
    ).fetchall()
    labels = [attendance[0] for attendance in weekly_attendances]
    counts = [attendance[1] for attendance in weekly_attendances]
    response = {'labels':labels,'counts':counts}
    return response


def monthly_attendance  ():
    monthly_attendances  = get_db().execute(
        'SELECT strftime("%Y-%m", attendance_date) AS month, COUNT(DISTINCT id) Count FROM attendance GROUP BY month'
    ).fetchall()
    labels = [attendance[0] for attendance in monthly_attendances]
    counts = [attendance[1] for attendance in monthly_attendances]
    response = {'labels':labels,'counts':counts}
    return response

