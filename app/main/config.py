import urllib.parse
class Config:
    SECRET_KEY = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
    DEBUG = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'vitalijus.alsauskas@gmail.com'
    MAIL_PASSWORD = 'mariukas'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

#Dev config
class DevelopmentConfig(Config):
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgres://jrfowfbeerorar:505a9e414de46031fe0c5fbfb7a4d409f3cc3892580f271d0c020df04f94f361@ec2-54-217-195-234.eu-west-1.compute.amazonaws.com:5432/deplhosaj6s9j2'
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
