class Config(object):
    """Base config class."""
    SECRET_KEY = '490db25515e9894fe268c66bad00b7c9'
    RECAPTCHA_PUBLIC_KEY = '<public key>'
    RECAPTCHA_PRIVATE_KEY = '<private key>'

class ProdConfig(Config):
    """Production config class."""
    pass

class DevConfig(Config):
    """Development config class."""
    # Open the DEBUG
    DEBUG = True
    # sqlalchemy configuration
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://<database user>:<database password>@127.0.0.1:3306/tinyblog'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # celery configuration
    CELERY_RESULT_BACKEND = "amqp://guest:guest@localhost:5672//"
    CELERY_BROKER_URL = "amqp://guest:guest@localhost:5672//"
    # flask-mail configuration
    MAIL_SERVER = '<email server>'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = '<email account>'
    MAIL_PASSWORD = '<email password>'