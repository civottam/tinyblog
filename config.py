class Config(object):
    """Base config class."""
    SECRET_KEY = '490db25515e9894fe268c66bad00b7c9'

class ProdConfig(Config):
    """Production config class."""
    pass

class DevConfig(Config):
    """Development config class."""
    # Open the DEBUG
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:rootroot@127.0.0.1:3306/tinyblog'
    SQLALCHEMY_TRACK_MODIFICATIONS = True