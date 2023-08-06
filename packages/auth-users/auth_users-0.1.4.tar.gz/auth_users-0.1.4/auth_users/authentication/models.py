import base64
import hashlib

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import func


class UsersModel:
    """Represents the user table."""

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=True)
    password = Column(String(255), nullable=False)
    created_on = Column(DateTime, default=func.now())
    updated_on = Column(DateTime, default=func.now(), server_onupdate=func.now())

    REQUIRED_FIELDS = {'username', 'password'}

    @declared_attr
    def authtoken(cls):
        return relationship('AuthTokens', lazy=True)


    def init(self, username, password):
        self.username = username
        self.password = password

    def is_correct_password(self, encrypted_str):
        string_ = base64.b64decode(encrypted_str).decode('utf-8')
        return hashlib.sha256(string_.encode()).hexdigest() == self.password

    def __repr__(self):
        return f'<User: {self.username} - {self.email}>'

    def to_dict(self):
        data = self.__dict__
        if data.get('created_on'):
            data['created_on'] = data.get('created_on').strftime("%d/%m/%Y, %H:%M:%S")
        if data.get('updated_on'):
            data['updated_on'] = data.get('updated_on').strftime("%d/%m/%Y, %H:%M:%S")
        if '_sa_instance_state' in data:
            del data['_sa_instance_state']
        return data

    def save_instance(self):
        raise NotImplementedError
