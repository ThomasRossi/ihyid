from flask import Blueprint, Flask
from flask_restplus import Api

from app.main.config import config_by_name
from app.main.controller.auth_controller import api as auth_ns
from app.main.controller.user_controller import api as user_ns
from app.main.controller.organisation_controller import api as organisation_ns
from app.main.controller.contact_controller import api as contact_ns
from app.main.services import db, flask_bcrypt
from app.main.celery import init_celery
from app.main.service.user_service import create_admin_first_startup

def create_app(**kwargs):
    """ create the flask app, then initalise the services: db, bycrypt, celery; finally preapre the api blueprint"""
    config_name=kwargs.get("config_name")
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    flask_bcrypt.init_app(app)
    if(kwargs.get("celery")):
      init_celery(kwargs.get("celery"), app)

    blueprint = Blueprint('api', __name__)
    api = Api(blueprint,
              title='IHYID',
              version='1.0',
              description='IHY-ID based on Eonbasics restplus web service with JWT')
    api.add_namespace(user_ns, path='/user')
    api.add_namespace(auth_ns)
    api.add_namespace(organisation_ns, path='/organisation')
    api.add_namespace(contact_ns, path='/contact')
    app.register_blueprint(blueprint)

    app.app_context().push()

    create_admin_first_startup()

    return app
