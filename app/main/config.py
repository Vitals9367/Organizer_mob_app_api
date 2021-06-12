import urllib.parse
class Config:
    SECRET_KEY = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    DEBUG = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'email'
    MAIL_PASSWORD = 'password'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

#Dev config
class DevelopmentConfig(Config):
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True

#Test config
class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../test_database.db'
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True

#Production config
class ProductionConfig(Config):
    DEBUG = False



config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
