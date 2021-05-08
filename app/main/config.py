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

    params = urllib.parse.quote_plus(
        "Driver={ODBC Driver 17 for SQL Server};Server=tcp:organizerdb.database.windows.net,1433;Database=organizerdb;Uid=adminas;Pwd=slaptazodis1A.;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgres: // vmyedshomcjtgj: 6e0e584bc46342dc27cf732f8e3f7228c81146b448c8744a6dfc4908eb4a728f@ec2-3-91-127-228.compute-1.amazonaws.com: 5432/d74an82tip9b3g"
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
