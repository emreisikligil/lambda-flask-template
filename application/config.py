from os import getenv
from distutils.util import strtobool


class Config:
    TESTING = False
    RSA_PUBLIC_KEY = getenv("RSA_PUBLIC_KEY", None)
    SQLALCHEMY_DATABASE_URI = getenv("SQLALCHEMY_DATABASE_URI", None)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    S3_BUCKET = getenv("S3_BUCKET", None)
