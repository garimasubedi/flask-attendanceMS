import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import dashboard,teacher,subject,student,auth,attendance,batch,course
    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(teacher.bp)
    app.register_blueprint(subject.bp)
    app.register_blueprint(student.bp)
    app.register_blueprint(batch.bp)
    app.register_blueprint(course.bp)
    app.register_blueprint(attendance.bp)
    from . import db
    db.init_app(app)
    
    return app

