import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')

class DevelopmentConfig(Config):
    ADMIN_EMAIL = 'admin@admin.com'
    ADMIN_USERNAME = 'admin'
    ADMIN_PASSWORD = 'password'
    KMI_TYPE = 'DEV'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'ihyid_dev.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = 'redis://localhost:6379'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379'
    EONPASS_URL = ''
    EONPASS_USER = ''
    EONPASS_PWD = ''
    LOCAL_FLASK_PORT = 5000


class TestingConfig(Config):
    ADMIN_EMAIL = 'admin@admin.com'
    ADMIN_USERNAME = 'admin'
    ADMIN_PASSWORD = 'password'
    KMI_TYPE = 'DEV'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'ihyid_test.db')
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = 'redis://localhost:6379'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379'
    EONPASS_URL = ''
    EONPASS_USER = ''
    EONPASS_PWD = ''
    LOCAL_FLASK_PORT = 5000



class ProductionConfig(Config):
    ADMIN_EMAIL = 'change@this.com'
    ADMIN_USERNAME = 'change this'
    ADMIN_PASSWORD = 'change this'
    KMI_TYPE = 'PYKMIP'
    DEBUG = False
    # uncomment the line below to use postgres
    # postgres_local_base = os.environ['DATABASE_URL']
    # SQLALCHEMY_DATABASE_URI = postgres_local_base
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = 'redis://localhost:6379'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379'
    EONPASS_URL = ''
    EONPASS_USER = ''
    EONPASS_PWD = ''
    LOCAL_FLASK_PORT = 5000


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY