import os
import tempfile

from pytest import fixture
from Crypto.PublicKey import RSA
from jwt import encode
from pyutils.auth.flaskjwt import Claims

from application import Config, Application, create_app


@fixture(scope="session")
def client(public_key):
    db_fd, db_filename = tempfile.mkstemp()
    Config.TESTING = True
    Config.SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_filename}"
    Config.RSA_PUBLIC_KEY = public_key
    app = create_app()
    with app.test_client() as client:
        with app.app_context():
            Application.db.create_all()
        yield client
    os.close(db_fd)
    os.unlink(db_filename)


@fixture(scope="session")
def rsa_key():
    return RSA.generate(2048)


@fixture(scope="session")
def private_key(rsa_key):
    return rsa_key.exportKey("PEM")


@fixture(scope="session")
def public_key(rsa_key):
    return rsa_key.publickey().exportKey("PEM")


@fixture(scope="session")
def jwt(private_key):
    claims = dict(
        sub="123456789",
        exp=2516239022
    )
    return encode(claims, private_key, "RS256")
