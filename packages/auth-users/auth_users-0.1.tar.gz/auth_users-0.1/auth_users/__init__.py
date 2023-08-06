
import base64
import hashlib

from sqlalchemy import exc

from app import db


class HelperModel:
    def save_instance(self):
        try:
            db.session.add(self)
            db.session.commit()
            return
        except exc.SQLAlchemyError as e:
            return e


    def delete_instance(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return
        except exc.SQLAlchemyError as e:
            return e


def encrypt_password(password):
    if isinstance(password, bytes):
        password = password.decode('utf-8')
    password = base64.b64decode(password).decode('utf-8')
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    if isinstance(password_hash, bytes):
        password_hash = password_hash.decode('utf-8')
    return password_hash
