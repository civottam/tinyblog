class Config(object):
    """Base config class."""
    SECRET_KEY = '490db25515e9894fe268c66bad00b7c9'
    RECAPTCHA_PUBLIC_KEY = '6LffkVkUAAAAANsOYU0ou_jejR5g470w_UlDACDP'
    RECAPTCHA_PRIVATE_KEY = '6LffkVkUAAAAAP8u34LjbMIMazMQkvsnzfKH8tJL'

class ProdConfig(Config):
    """Production config class."""
    pass

class DevConfig(Config):
    """Development config class."""
    # Open the DEBUG
    DEBUG = True
    # sqlalchemy configuration
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:rootroot@127.0.0.1:3306/tinyblog'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # celery configuration
    CELERY_RESULT_BACKEND = "amqp://guest:guest@localhost:5672//"
    CELERY_BROKER_URL = "amqp://guest:guest@localhost:5672//"
    # flask-mail configuration
    MAIL_SERVER = 'smtp-mail.outlook.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'tinyblog@outlook.com'
    MAIL_PASSWORD = 'T1nybl0g@'