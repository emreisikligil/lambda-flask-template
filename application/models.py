from contextlib import contextmanager
from datetime import datetime

from sqlalchemy.sql import func
from pyutils.sql.model2dict import model2dict

from application import Application

db = Application.db


@model2dict
class Pet(db.Model):
    __table_name__ = "pet"
    id = db.Column(db.Integer, primary_key=True)
    pet_type = db.Column(db.String(32), nullable=False)
    breed = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(512), nullable=True)
    owner = db.Column(db.String(128), nullable=True)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = db.session
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
