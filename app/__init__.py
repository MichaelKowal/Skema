import os
from flask import Flask
from . import log


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    event = 'App created'
    log.add_event(event)
    app.config.from_mapping(
            SECRET_KEY='dev',
            DATABASE=os.path.join(app.instance_path, 'skemaDB.sqlite')
    )
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # create an instance folder if none exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        event = 'Instance path already exists'
        log.add_event(event)

    from .views import views
    app.register_blueprint(views)

    from . import database
    database.init_app(app)

    return app
