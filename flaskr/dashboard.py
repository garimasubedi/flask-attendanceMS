import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.auth import login_required
bp = Blueprint('dashboard', __name__, url_prefix='')


@bp.route('/', methods=['GET'])
@login_required
def index():
    return render_template('dashboard/index.html')